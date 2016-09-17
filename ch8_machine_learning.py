# -*- coding: utf-8 -*-
# 第8章: 機械学習

import argparse
import codecs
import nltk
import random
import re


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

def knock72_imp2(file_name):
    # This function produces stemmed words, word-based N-gram, and char-based N-gram as feature input
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    dict_pos = {}
    dict_neg = {}
    pass

def knock72_imp1(file_name):
    # This function takes both stemmed words and word-based N-gram as feature input
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    dict_pos = {}
    dict_neg = {}
    with codecs.open(file_name, 'r', "utf-8") as fd:
        for line in fd:
            line = re.sub('\.', '', line)
            line = re.sub('\,', '', line)
            words = line.split(' ')
            flag = words.pop(0)
            n_gram_input = ""
            for word in words:
                if(not check_stopword(word, stop_words)):
                    word = stemmer.stem(word)
                    n_gram_input += " " + word
                    if(flag == u"+"):
                        dict_pos[word] = dict_pos.get(word, 0) + 1
                    elif(flag == u"-"):
                        dict_neg[word] = dict_neg.get(word, 0) + 1
            # Obtain and process n-gram, bi-gram for simplicity
            n_gram_result = n_gram(2, 'w', n_gram_input, "__")
            for token in n_gram_result:
                if(flag == u"+"):
                    dict_pos[token] = dict_pos.get(token, 0) + 1
                elif(flag == u"-"):
                    dict_neg[token] = dict_neg.get(token, 0) + 1
    dict_pos = sorted(dict_pos.items(), key=lambda x:x[1], reverse=True)
    dict_neg = sorted(dict_neg.items(), key=lambda x:x[1], reverse=True)
    return(dict_pos, dict_neg)

def knock72_baseline(file_name):
    # This function only takes the stemmed words as feature input
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    dict_pos = {}
    dict_neg = {}
    with codecs.open(file_name, 'r', "utf-8") as fd:
        for line in fd:
            line = re.sub('\.', '', line)
            line = re.sub('\,', '', line)
            words = line.split(' ')
            flag = words.pop(0)
            for word in words:
                if(not check_stopword(word, stop_words)):
                    word = stemmer.stem(word)
                    if(flag == u"+"):
                        dict_pos[word] = dict_pos.get(word, 0) + 1
                    elif(flag == u"-"):
                        dict_neg[word] = dict_neg.get(word, 0) + 1
    dict_pos = sorted(dict_pos.items(), key=lambda x:x[1], reverse=True)
    dict_neg = sorted(dict_neg.items(), key=lambda x:x[1], reverse=True)
    return(dict_pos, dict_neg)

def knock72():
    return(knock72_imp1("./sentiment.txt"))
    return(knock72_baseline("./sentiment.txt"))

'''
73. 学習
72で抽出した素性を用いて，ロジスティック回帰モデルを学習せよ．
'''
def knock73():
    return(None)

'''
74. 予測
73で学習したロジスティック回帰モデルを用い，与えられた文の極性ラベル（正例なら"+1"，負例なら"-1"）と，その予測確率を計算するプログラムを実装せよ．
'''
def knock74():
    return(None)

'''
75. 素性の重み
73で学習したロジスティック回帰モデルの中で，重みの高い素性トップ10と，重みの低い素性トップ10を確認せよ．
'''
def knock75():
    return(None)

'''
76. ラベル付け
学習データに対してロジスティック回帰モデルを適用し，正解のラベル，予測されたラベル，予測確率をタブ区切り形式で出力せよ．
'''
def knock76():
    return(None)

'''
77. 正解率の計測
76の出力を受け取り，予測の正解率，正例に関する適合率，再現率，F1スコアを求めるプログラムを作成せよ．
'''
def knock77():
    return(None)

'''
78. 5分割交差検定
76-77の実験では，学習に用いた事例を評価にも用いたため，正当な評価とは言えない．すなわち，分類器が訓練事例を丸暗記する際の性能を評価しており，モデルの汎化性能を測定していない．そこで，5分割交差検定により，極性分類の正解率，適合率，再現率，F1スコアを求めよ．
'''
def knock78():
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

    if(args.knock == 0 or args.knock == 70):
        print(knock70())
    if(args.knock == 1 or args.knock == 71):
        if(not args.arg):
            args.arg = "This is a pen."
        print(knock71(args.arg))
    if(args.knock == 2 or args.knock == 72):
        print(knock72())
    if(args.knock == 3 or args.knock == 73):
        print(knock73())
    if(args.knock == 4 or args.knock == 74):
        print(knock74())
    if(args.knock == 5 or args.knock == 75):
        print(knock75())
    if(args.knock == 6 or args.knock == 76):
        print(knock76())
    if(args.knock == 7 or args.knock == 77):
        print(knock77())
    if(args.knock == 8 or args.knock == 78):
        print(knock78())
    if(args.knock == 9 or args.knock == 79):
        print(knock79())


