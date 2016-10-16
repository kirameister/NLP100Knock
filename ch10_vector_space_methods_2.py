# -*- coding: utf-8 -*-
#第10章: ベクトル空間法 (II)


import argparse
import json
import logging
import re

from gensim.models import word2vec
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.cluster import Ward
import numpy as np
import scipy
import scipy.spatial.distance

'''
第10章では，前章に引き続き単語ベクトルの学習に取り組む．
'''

'''
90. word2vecによる学習
81で作成したコーパスに対してword2vecを適用し，単語ベクトルを学習せよ．さらに，学習した単語ベクトルの形式を変換し，86-89のプログラムを動かせ．
'''
def knock90(src_filename:str, dst_filename:str):
    data = word2vec.Text8Corpus(src_filename)
    model = word2vec.Word2Vec(data, size=300)
    model.save(dst_filename)
    print("Knock86: ", end="")
    print(model['United_States'])
    print("Knock87: ", end="")
    print(model.similarity('United_States', 'U.S'))
    print("Knock88: ", end="")
    print(model.most_similar(positive=["England"]))
    print("Knock89: ", end="")
    print(model.most_similar(positive=["Spain", "Athens"], negative=["Madrid"]))
    return("Completed")

'''
91. アナロジーデータの準備
単語アナロジーの評価データ (https://word2vec.googlecode.com/svn/trunk/questions-words.txt) をダウンロードせよ．このデータ中で": "で始まる行はセクション名を表す．例えば，": capital-common-countries"という行は，"capital-common-countries"というセクションの開始を表している．ダウンロードした評価データの中で，"family"というセクションに含まれる評価事例を抜き出してファイルに保存せよ．
'''
def knock91(src_text_filename:str, dst_filename:str):
    with open(src_text_filename, 'r') as fds:
        with open(dst_filename, 'w') as fdd:
            for line in fds:
                if(re.match('^: family', line)):
                    break
            for line in fds:
                if(re.match('^:', line)):
                    break
                fdd.write(line)
    return("Completed")

'''
92. アナロジーデータへの適用
91で作成した評価データの各事例に対して，vec(2列目の単語) - vec(1列目の単語) + vec(3列目の単語)を計算し，そのベクトルと類似度が最も高い単語と，その類似度を求めよ．求めた単語と類似度は，各事例の末尾に追記せよ．このプログラムを85で作成した単語ベクトル，90で作成した単語ベクトルに対して適用せよ．
'''
def knock92(question_words_filename:str, wv_90_filename:str, wv_85_model_filename:str, wv_85_dict_filename:str):
    return_value = ""
    model_90 = Word2Vec.load(wv_90_filename)
    model_85 = np.load(wv_85_model_filename)
    with open(wv_85_dict_filename, 'r') as fds:
        dict_85 = json.load(fds)
    with open(question_words_filename, 'r') as fds:
        for line in fds:
            word_similarity_dict = dict()
            line = line.rstrip()
            (word1, word2, word3, word4) = line.split(' ')
            try:
                similar_word = model_90.most_similar(positive=[word2, word3], negative=[word1])
                vec = model_85[dict_85[word2]] - model_85[dict_85[word1]] + model_85[dict_85[word3]]
                #print("Model90\t" + word2 + " - " + word1 + " + " + word3 + " ==> " + similar_word[0][0] + " (" + str(similar_word[0][1]) + ")")
                return_value += "Model90\t" + word2 + " - " + word1 + " + " + word3 + " ==> " + similar_word[0][0] + " (" + str(similar_word[0][1]) + ")\n"
                for key,value in dict_85.items():
                    similarity = scipy.spatial.distance.cosine(model_85[dict_85[key]], vec)
                    word_similarity_dict[key] = similarity
                (word, value) = sorted(word_similarity_dict.items(), key=lambda x:x[1])[0]
                #print("Model85\t" + word2 + " - " + word1 + " + " + word3 + " ==> " + word + " (" + str(value) + ")")
                return_value += "Model85\t" + word2 + " - " + word1 + " + " + word3 + " ==> " + word + " (" + str(value) + ")\n"
            except KeyError:
                # this is required in order to avoid OOV error (we simply ignore it)
                continue
    return(return_value)

'''
93. アナロジータスクの正解率の計算
92で作ったデータを用い，各モデルのアナロジータスクの正解率を求めよ．
'''
def knock93(question_words_filename:str, wv_90_filename:str, wv_85_model_filename:str, wv_85_dict_filename:str):
    lines = knock92(question_words_filename, wv_90_filename, wv_85_model_filename, wv_85_dict_filename)
    lines_list = lines.split('\n')
    total = 0
    correct = 0
    while(True):
        try:
            expected = lines_list.pop(0)
            predicted = lines_list.pop(0)
        except:
            break
        expected_word  = re.sub(r'^.*==> (.*?) \(.*$', '\\1', expected)
        predicted_word = re.sub(r'^.*==> (.*?) \(.*$', '\\1', predicted)
        if(expected_word.lower() == predicted_word.lower()):
            correct += 1
        total += 1
    return(float(correct / total))

'''
94. WordSimilarity-353 での類似度計算
The WordSimilarity-353 Test Collection (http://www.cs.technion.ac.il/~gabr/resources/data/wordsim353/) の評価データを入力とし，1列目と2列目の単語の類似度を計算し，各行の末尾に類似度の値を追加するプログラムを作成せよ．このプログラムを85で作成した単語ベクトル，90で作成した単語ベクトルに対して適用せよ．
'''
def knock94_word2vec(word1:str, word2, wv_90_model):
    try:
        return_value = wv_90_model.similarity(word1, word2)
    except KeyError:
        return_value = 0.0
    return(return_value)

def knock94_myword2vec(word1:str, word2:str, wv_85_model:str, wv_85_dict:str):
    try:
        return_value = scipy.spatial.distance.cosine(wv_85_model[wv_85_dict[word1]], wv_85_model[wv_85_dict[word2]])
    except KeyError:
        return_value = 0.0
    return(return_value)

def knock94(eval_set_filename:str, wv_90_filename:str, wv_85_model_filename:str, wv_85_dict_filename:str):
    print("== Results using using Word2Vec ==")
    model_90 = Word2Vec.load(wv_90_filename)
    with open(eval_set_filename, 'r') as fds:
        for line in fds:
            words_list = line.split('\t')
            word1 = words_list[0]
            word2 = words_list[1]
            if(word1 == 'Word 1' and str(word2) == 'Word 2'):
                continue
            similarity = knock94_word2vec(word1, word2, model_90)
            print(word1 + " " + word2 + ": " + str(similarity))

    print("== Results using using PCA from knock85 ==")
    model_85 = np.load(wv_85_model_filename)
    with open(wv_85_dict_filename, 'r') as fds:
        dict_85 = json.load(fds)
    with open(eval_set_filename, 'r') as fds:
        for line in fds:
            words_list = line.split('\t')
            word1 = words_list[0]
            word2 = words_list[1]
            if(word1 == 'Word 1' and str(word2) == 'Word 2'):
                continue
            similarity = knock94_myword2vec(word1, word2, model_85, dict_85)
            print(word1 + " " + word2 + ": " + str(similarity))

    return("Complete")

'''
95. WordSimilarity-353での評価
94で作ったデータを用い，各モデルが出力する類似度のランキングと，人間の類似度判定のランキングの間のスピアマン相関係数を計算せよ．
'''
def knock95(eval_set_filename:str, wv_90_filename:str, wv_85_model_filename:str, wv_85_dict_filename:str):
    return_value = ""
    model_90 = Word2Vec.load(wv_90_filename)
    model_85 = np.load(wv_85_model_filename)
    model_90_similarity_list = []
    model_90_human_list      = []
    model_85_similarity_list = []
    model_85_human_list      = []
    with open(wv_85_dict_filename, 'r') as fds:
        dict_85 = json.load(fds)

    with open(eval_set_filename, 'r') as fds:
        for line in fds:
            words_list = line.split('\t')
            word1 = words_list[0]
            word2 = words_list[1]
            human_score = words_list[2]
            if(word1 == 'Word 1' and str(word2) == 'Word 2'):
                continue
            similarity_90 = knock94_word2vec(word1, word2, model_90)
            similarity_85 = knock94_myword2vec(word1, word2, model_85, dict_85)
            if(similarity_90 != 0.0):
                model_90_similarity_list.append(similarity_90)
                model_90_human_list.append(human_score)
            if(similarity_85 != 0.0):
                model_85_similarity_list.append(similarity_85)
                model_85_human_list.append(human_score)
    return_value = str(scipy.stats.stats.spearmanr(model_90_similarity_list, model_90_human_list)[0])
    return_value += "\t" + str(scipy.stats.stats.spearmanr(model_85_similarity_list, model_85_human_list)[0])
    return(return_value)

'''
96. 国名に関するベクトルの抽出
word2vecの学習結果から，国名に関するベクトルのみを抜き出せ．
'''
def knock96(wv_90_filename:str):
    country_list = [ "Antigua_and_Barbuda", "Bosnia_and_Herzegovina", "Burkina_Faso", "Cabo_Verde", "Central_African_Republic", "Costa_Rica", "Cote_d\'Ivoire", "Czech_Republic", "Democratic_Republic_of_the_Congo", "Dominican_Republic", "East_Timor", "El_Salvador", "Equatorial_Guinea", "Guinea_Bissau", "Holy_See", "Hong_Kong", "Marshall_Islands", "New_Zealand", "North_Korea", "Palestinian_Territories", "Papua_New_Guinea", "Republic_of_the_Congo", "Saint_Kitts_and_Nevis", "Saint_Lucia", "Saint_Vincent_and_the_Grenadines", "San_Marino", "Sao_Tome_and_Principe", "Saudi_Arabia", "Sierra_Leone", "Sint_Maarten", "Solomon_Islands", "South_Africa", "South_Korea", "South_Sudan", "Sri_Lanka", "The_Bahamas", "The_Gambia", "Timor_Leste", "Trinidad_and_Tobago", "United_Arab_Emirates", "United_Kingdom", "United_States_of_America", "United_States" ]
    model_90 = Word2Vec.load(wv_90_filename)
    for country in country_list:
        try:
            print(country + "\t" + str(model_90[country]))
        except KeyError:
            print("Skipping " + country + "..")
    return("Completed")

'''
97. k-meansクラスタリング
96の単語ベクトルに対して，k-meansクラスタリングをクラスタ数 k=5 として実行せよ．
'''
def knock97(wv_90_filename:str):
    country_list = [ "Antigua_and_Barbuda", "Bosnia_and_Herzegovina", "Burkina_Faso", "Cabo_Verde", "Central_African_Republic", "Costa_Rica", "Cote_d\'Ivoire", "Czech_Republic", "Democratic_Republic_of_the_Congo", "Dominican_Republic", "East_Timor", "El_Salvador", "Equatorial_Guinea", "Guinea_Bissau", "Holy_See", "Hong_Kong", "Marshall_Islands", "New_Zealand", "North_Korea", "Palestinian_Territories", "Papua_New_Guinea", "Republic_of_the_Congo", "Saint_Kitts_and_Nevis", "Saint_Lucia", "Saint_Vincent_and_the_Grenadines", "San_Marino", "Sao_Tome_and_Principe", "Saudi_Arabia", "Sierra_Leone", "Sint_Maarten", "Solomon_Islands", "South_Africa", "South_Korea", "South_Sudan", "Sri_Lanka", "The_Bahamas", "The_Gambia", "Timor_Leste", "Trinidad_and_Tobago", "United_Arab_Emirates", "United_Kingdom", "United_States_of_America", "United_States" ]
    model_90 = Word2Vec.load(wv_90_filename)
    cluster_list = []
    country_src_list = []

    for country in country_list:
        try:
            cluster_list.append(model_90[country])
            country_src_list.append(country)
        except KeyError:
            pass
    cluster_nparray = np.array(cluster_list)
    kmeans_model = KMeans(n_clusters=5, random_state=10).fit(cluster_nparray)
    labels = kmeans_model.labels_
    for i in range(len(labels)):
        print(country_src_list[i] + "\t" + str(labels[i]))
    return(None)

'''
98. Ward法によるクラスタリング
96の単語ベクトルに対して，Ward 法による階層型クラスタリングを実行せよ．さらに，クラスタリング結果をデンドログラムとして可視化せよ．
'''
def knock98(wv_90_filename:str):
    return(None)

'''
99. t-SNEによる可視化
96の単語ベクトルに対して，ベクトル空間を t-SNE で可視化せよ．
'''
def knock99():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 10')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 90):
        print(knock90("temp_knock81_enwiki.txt", "temp_knock90"))
    if(args.knock == 1 or args.knock == 91):
        print(knock91("questions-words.txt", "temp_knock91"))
    if(args.knock == 2 or args.knock == 92):
        #print(knock90("temp_knock81_enwiki.txt", "temp_knock90"))
        print(knock92("temp_knock91", "temp_knock90", "temp_knock85_matrix.npy", "temp_knock85_word_dict.json"))
    if(args.knock == 3 or args.knock == 93):
        print(knock93("temp_knock91", "temp_knock90", "temp_knock85_matrix.npy", "temp_knock85_word_dict.json"))
    if(args.knock == 4 or args.knock == 94):
        print(knock94("combined.tab", "temp_knock90", "temp_knock85_matrix.npy", "temp_knock85_word_dict.json"))
    if(args.knock == 5 or args.knock == 95):
        print(knock95("combined.tab", "temp_knock90", "temp_knock85_matrix.npy", "temp_knock85_word_dict.json"))
    if(args.knock == 6 or args.knock == 96):
        print(knock96("temp_knock90"))
    if(args.knock == 7 or args.knock == 97):
        print(knock97("temp_knock90"))
    if(args.knock == 8 or args.knock == 98):
        print(knock98("temp_knock90"))
    if(args.knock == 9 or args.knock == 99):
        print(knock99())


