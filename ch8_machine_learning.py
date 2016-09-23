# -*- coding: utf-8 -*-
# 第8章: 機械学習

import argparse
import codecs
import nltk
import pickle
import random
import re
import sklearn
import sklearn.linear_model as LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


'''
本章では，Bo Pang氏とLillian Lee氏が公開しているMovie Review Data (http://www.cs.cornell.edu/people/pabo/movie-review-data/) のsentence polarity dataset v1.0 (http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.README.1.0.txt) を用い，文を肯定的（ポジティブ）もしくは否定的（ネガティブ）に分類するタスク（極性分析）に取り組む．
'''

'''
70. データの入手・整形
文に関する極性分析の正解データ (http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz) を用い，以下の要領で正解データ（sentiment.txt）を作成せよ．

rt-polarity.posの各行の先頭に"+1 "という文字列を追加する（極性ラベル"+1"とスペースに続けて肯定的な文の内容が続く）
rt-polarity.negの各行の先頭に"-1 "という文字列を追加する（極性ラベル"-1"とスペースに続けて否定的な文の内容が続く）
上述1と2の内容を結合（concatenate）し，行をランダムに並び替える
sentiment.txtを作成したら，正例（肯定的な文）の数と負例（否定的な文）の数を確認せよ．
'''
def knock70():
    pos_list = []
    neg_list = []
    with codecs.open("./rt-polaritydata/rt-polarity.pos", 'r', "latin-1") as fd:
        for line in fd:
            pos_list.append("+ "+line)
    with codecs.open("./rt-polaritydata/rt-polarity.neg", 'r', "latin-1") as fd:
        for line in fd:
            neg_list.append("- "+line)
    dst_list = pos_list + neg_list
    random.shuffle(dst_list)
    with codecs.open("./sentiment.txt", 'w', "utf-8") as fd:
        for line in dst_list:
            fd.write(line)
    return("pos: " + str(len(pos_list)) + "\t neg: " + str(len(neg_list)))

'''
71. ストップワード
英語のストップワードのリスト（ストップリスト）を適当に作成せよ．さらに，引数に与えられた単語（文字列）がストップリストに含まれている場合は真，それ以外は偽を返す関数を実装せよ．さらに，その関数に対するテストを記述せよ．
'''
def check_stopword(word, stop_words_set):
    word = word.lower()
    if(word in stop_words_set):
        return(True)
    else:
        return(False)

def knock71(text):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    text = re.sub('\.', ' .', text)
    text = re.sub('\,', ' ,', text)
    words = text.split(' ')
    for word in words:
        if(check_stopword(word, stop_words)):
            print(word + " is a stopword")
        else:
            print(word + " is NOT a stopword")
    return("completed")

'''
72. 素性抽出
極性分析に有用そうな素性を各自で設計し，学習データから素性を抽出せよ．素性としては，レビューからストップワードを除去し，各単語をステミング処理したものが最低限のベースラインとなるであろう．
'''
def n_gram(n, mode, string, delimiter):
    return_ngram = list()
    if(mode.startswith("w")):
        string_list = string.split() # word-based n-gram
    else:
        string_list = list(string) # char-based n-gram
    for i in range(len(string_list)-n+1):
        temp_string = ""
        for j in range(0, n):
            if(temp_string == ""):
                temp_string = string_list[i+j]
            else:
                temp_string = temp_string + delimiter + string_list[i+j]
        return_ngram.append(temp_string)
    return(return_ngram)

def knock72_word_bigram(line: str):
    # This function takes both stemmed words and word-based bi-gram as feature input
    # In order to let TfidfVectorizer use this function on one go, this function also contains the same functionality as baseline. 
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    return_list = []
    line = line.rstrip()
    line = re.sub('\.', '', line)
    line = re.sub('\,', '', line)
    line = re.sub('\s+$', '', line)
    words = line.split(' ')
    for word in words:
        if(check_stopword(word, stop_words)):
            continue
        word = stemmer.stem(word)
        return_list.append(word)
    return_list.extend(n_gram(2, 'w', line, "__"))
    return(return_list)

def knock72_baseline(line: str):
    # This function only takes the stemmed words as feature input
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    return_list = []
    line = line.rstrip()
    line = re.sub('\.', '', line)
    line = re.sub('\,', '', line)
    line = re.sub('\s+$', '', line)
    words = line.split(' ')
    for word in words:
        if(check_stopword(word, stop_words)):
            continue
        word = stemmer.stem(word)
        return_list.append(word)
    return(return_list)

def knock72():
    return_list = []
    pos_list = []
    neg_list = []

    with codecs.open("./rt-polaritydata/rt-polarity.pos", 'r', "latin-1") as fd_pos:
        for line in fd_pos:
            pos_list.extend(knock72_baseline(line))
    with codecs.open("./rt-polaritydata/rt-polarity.neg", 'r', "latin-1") as fd_neg:
        for line in fd_neg:
            neg_list.extend(knock72_baseline(line))
    return(pos_list, neg_list)

'''
73. 学習
72で抽出した素性を用いて，ロジスティック回帰モデルを学習せよ．
'''
def knock73():
    #tfidf = TfidfVectorizer(analyzer=knock72_baseline)
    tfidf = TfidfVectorizer(analyzer=knock72_word_bigram)
    (pos_list, neg_list) = knock72()

    train_X = pos_list[:]
    train_X.extend(neg_list)
    pos_list_y = [0] * len(pos_list)
    neg_list_y = [1] * len(neg_list)
    train_Y = pos_list_y
    train_Y.extend(neg_list_y)
    tfs = tfidf.fit_transform(train_X)
    model = sklearn.linear_model.LogisticRegression()
    model.fit(tfs, train_Y)
    return(tfidf, model)

'''
74. 予測
73で学習したロジスティック回帰モデルを用い，与えられた文の極性ラベル（正例なら"+1"，負例なら"-1"）と，その予測確率を計算するプログラムを実装せよ．
'''
def knock74(tfidf_filename:str, model_filename:str, input_line: str):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    return_string = ""
    token_list = []
    input_line = input_line.rstrip()
    input_line = re.sub('\.', '', input_line)
    input_line = re.sub('\,', '', input_line)
    words = input_line.split(' ')
    line_to_feed = ""
    for word in words:
        if(not check_stopword(word, stop_words)):
            line_to_feed += word + " "
    line_to_feed = re.sub(" $", "", line_to_feed)
    #token_list.extend(knock72_baseline(line_to_feed))
    token_list.extend(knock72_word_bigram(line_to_feed))

    with open(tfidf_filename, 'rb') as fd:
        tfidf = pickle.load(fd)
    with open(model_filename, 'rb') as fd:
        model = pickle.load(fd)
    #print(token_list)
    test = tfidf.transform(token_list)

    probability_result = model.predict_proba(test).sum(axis=0)
    if(probability_result[0] > probability_result[1]):
        return_string = "+1"
    else:
        return_string = "-1"
    return(return_string + "\t" + str(probability_result))

'''
75. 素性の重み
73で学習したロジスティック回帰モデルの中で，重みの高い素性トップ10と，重みの低い素性トップ10を確認せよ．
'''
def knock75(tfidf_filename:str, model_filename:str):
    with open(tfidf_filename, 'rb') as fd:
        tfidf = pickle.load(fd)
    with open(model_filename, 'rb') as fd:
        model = pickle.load(fd)
    features = list(tfidf.get_feature_names())
    weights  = list(model.coef_[0])
    feature_weights = dict(zip(features, weights))
    print(len(features))
    print(len(weights))
    return(sorted(feature_weights.items(), key=lambda x: x[1], reverse=True))

'''
76. ラベル付け
学習データに対してロジスティック回帰モデルを適用し，正解のラベル，予測されたラベル，予測確率をタブ区切り形式で出力せよ．
'''
def knock76():
    stop_words = set(nltk.corpus.stopwords.words("english"))
    token_list = []
    return_list = []
    with open(tfidf_filename, 'rb') as fd:
        tfidf = pickle.load(fd)
    with open(model_filename, 'rb') as fd:
        model = pickle.load(fd)
    with codecs.open("./sentiment.txt", 'r', "utf-8") as fd:
        for test_line_src in fd:
            line_to_feed = ""
            predicted = ""
            test_line = test_line_src.rstrip()
            test_line = re.sub('\.', '', test_line)
            test_line = re.sub('\,', '', test_line)
            words = test_line.split(' ')
            expected = words.pop(0)
            for word in words:
                if(not check_stopword(word, stop_words)):
                    line_to_feed += word + " "
            line_to_feed = re.sub(" $", "", line_to_feed)
            token_list = knock72_word_bigram(line_to_feed)
            test = tfidf.transform(token_list)
            probability_result = model.predict_proba(test).sum(axis=0)
            if(probability_result[0] > probability_result[1]):
                predicted = "+"
            else:
                predicted = "-"
            return_list.append(expected + "\t" + predicted + "\t" + str(probability_result[0]) + "\t" + str(probability_result[1]))
    return(return_list)

'''
77. 正解率の計測
76の出力を受け取り，予測の正解率，正例に関する適合率，再現率，F1スコアを求めるプログラムを作成せよ．
'''
def knock77():
    return_string = ""
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    src_list = knock76()
    for line in src_list:
        (expected, predicted, pos_score, neg_score) = line.split("\t")
        if(expected == "+" and predicted == "+"):
            TP += 1
        if(expected == "+" and predicted == "-"):
            FN += 1
        if(expected == "-" and predicted == "+"):
            FP += 1
        if(expected == "-" and predicted == "-"):
            TN += 1
    precision = TP / (TP + FP)
    return_string += "Precision: \t" + str(precision) + "\n"
    recall    = TP / (TP + FN)
    return_string += "Recall: \t" + str(recall) + "\n"
    f_measure = (2 * recall * precision) / (recall + precision)
    return_string += "F1: \t" + str(f_measure)
    return(return_string)

'''
78. 5分割交差検定
76-77の実験では，学習に用いた事例を評価にも用いたため，正当な評価とは言えない．すなわち，分類器が訓練事例を丸暗記する際の性能を評価しており，モデルの汎化性能を測定していない．そこで，5分割交差検定により，極性分類の正解率，適合率，再現率，F1スコアを求めよ．
'''
def knock78():
    stop_words = set(nltk.corpus.stopwords.words("english"))
    # This is a dirty way to conduct cross validation with TFIDF..
    # split the obtained data into training and testing, and train the model. 
    tfidf = TfidfVectorizer(analyzer=knock72_word_bigram)
    dataset_list_tuple = []
    pattern = re.compile('^(.) (.*)$')
    with codecs.open("./sentiment.txt", 'r', "utf-8") as fd:
        for line in fd:
            m = pattern.search(line)
            expected = m.groups()[0]
            line = m.groups()[1]
            if(expected == "+"):
                expected = 0
            else:
                expected = 1
            dataset_list_tuple.append((line, expected))
    # randomize the order in order to ensure further randomness
    random.shuffle(dataset_list_tuple)
    # split the randomized text into train and test set, but they have not been tokenized..
    test_list_tuple   = dataset_list_tuple[0:len(dataset_list_tuple)//5]
    train_list_tuple  = dataset_list_tuple[len(dataset_list_tuple)//5:len(dataset_list_tuple)]
    # Start training..
    train_list_X = []
    train_list_Y = []
    for i,val in enumerate(train_list_tuple):
        temp_list_result = (knock72_word_bigram(train_list_tuple[i][0]))
        train_list_X.extend(temp_list_result)
        train_list_Y.extend(train_list_tuple[i][1] for x in range(len(temp_list_result)))
    tfs = tfidf.fit_transform(train_list_X)
    model = sklearn.linear_model.LogisticRegression()
    model.fit(tfs, train_list_Y)
    return
    # Test for each line in testset..
    for i in enumerate(test_list_tuple):
        pass


    (pos_list, neg_list) = knock72()
    all_data_list = []
    for i in pos_list:
        all_data_list.append((i, 0))
    for i in neg_list:
        all_data_list.append((i, 1))
    random.shuffle(all_data_list)
    test_list = all_data_list[0:len(all_data_list)//5]
    test_list_utts = [x[0] for x in test_list]
    print(test_list_utts[0:10])
    return
    train_list  = all_data_list[len(all_data_list)//5:len(all_data_list)]
    tfs = tfidf.fit_transform([x[0] for x in train_list])
    model = sklearn.linear_model.LogisticRegression()
    model.fit(tfs, [x[1] for x in train_list])
    # test the model using test partition.
    test_list_utts = [x[0] for x in test_list]
    for i in enumerate(test_list_utts):
        print(test_list_utts[i])

    return(None)

'''
79. 適合率-再現率グラフの描画
ロジスティック回帰モデルの分類の閾値を変化させることで，適合率-再現率グラフを描画せよ．
'''
def knock79():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 8')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()
    tfidf_filename = "./knock73_tfidf"
    model_filename = "./knock73_model"

    if(args.knock == 0 or args.knock == 70):
        print(knock70())
    if(args.knock == 1 or args.knock == 71):
        if(not args.arg):
            args.arg = "This is a pen."
        print(knock71(args.arg))
    if(args.knock == 2 or args.knock == 72):
        print(knock72())
    if(args.knock == 3 or args.knock == 73):
        #print(knock73())
        (tfidf, model) = knock73()
        with open(tfidf_filename, 'wb') as fd:
            pickle.dump(tfidf, fd)
        with open(model_filename, 'wb') as fd:
            pickle.dump(model, fd)
        print("TFIDF dumped file: " + tfidf_filename)
        print("Model dumped file: " + model_filename)
    if(args.knock == 4 or args.knock == 74):
        if(not args.arg):
            args.arg = "This is really great and exciting"
        print(knock74(tfidf_filename, model_filename, args.arg))
    if(args.knock == 5 or args.knock == 75):
        sorted_feature_weights = knock75(tfidf_filename, model_filename)
        print("== Features with highest weight ==")
        for index in range(20):
            print(sorted_feature_weights[index])
        print("== Features with lowest weight ==")
        for index in range(len(sorted_feature_weights)-20, len(sorted_feature_weights)):
            print(sorted_feature_weights[index])
    if(args.knock == 6 or args.knock == 76):
        print("Exp\tPred\tPositive_Score\tNegative_Score")
        print("\n".join(knock76()))
    if(args.knock == 7 or args.knock == 77):
        print(knock77())
    if(args.knock == 8 or args.knock == 78):
        print(knock78())
    if(args.knock == 9 or args.knock == 79):
        print(knock79())


