# -*- coding: utf-8 -*-
#第9章: ベクトル空間法 (I)

import argparse
import collections
import random
import re
import sys


'''
enwiki-20150112-400-r10-105752.txt.bz2は，2015年1月12日時点の英語のWikipedia記事のうち，約400語以上で構成される記事の中から，ランダムに1/10サンプリングした105,752記事のテキストをbzip2形式で圧縮したものである．このテキストをコーパスとして，単語の意味を表すベクトル（分散表現）を学習したい．第9章の前半では，コーパスから作成した単語文脈共起行列に主成分分析を適用し，単語ベクトルを学習する過程を，いくつかの処理に分けて実装する．第9章の後半では，学習で得られた単語ベクトル（300次元）を用い，単語の類似度計算やアナロジー（類推）を行う．

なお，問題83を素直に実装すると，大量（約7GB）の主記憶が必要になる． メモリが不足する場合は，処理を工夫するか，1/100サンプリングのコーパスenwiki-20150112-400-r100-10576.txt.bz2を用いよ．
'''

'''
80. コーパスの整形
文を単語列に変換する最も単純な方法は，空白文字で単語に区切ることである． ただ，この方法では文末のピリオドや括弧などの記号が単語に含まれてしまう． そこで，コーパスの各行のテキストを空白文字でトークンのリストに分割した後，各トークンに以下の処理を施し，単語から記号を除去せよ．
- トークンの先頭と末尾に出現する次の文字を削除: .,!?;:()[]'"
- 空文字列となったトークンは削除

以上の処理を適用した後，トークンをスペースで連結してファイルに保存せよ．
'''
def knock80(src_filename: str, dst_filename: str):
    with open(src_filename, 'r') as fds:
        with open(dst_filename, 'w') as fdd:
            for line in fds:
                words = line.split(' ')
                line = ""
                for word in words:
                    word = re.sub('^[\.,\!\?;:\(\)\[\]\'\"]+', '', word)
                    word = re.sub('[\.,\!\?;:\(\)\[\]\'\"]+$', '', word)
                    if(word == ""):
                        continue
                    line = line + " " + word
                line = re.sub('^ ', '', line)
                line = re.sub(' $', '', line)
                fdd.write(line)
    return("Completed")

'''
81. 複合語からなる国名への対処
英語では，複数の語の連接が意味を成すことがある．例えば，アメリカ合衆国は"United States"，イギリスは"United Kingdom"と表現されるが，"United"や"States"，"Kingdom"という単語だけでは，指し示している概念・実体が曖昧である．そこで，コーパス中に含まれる複合語を認識し，複合語を1語として扱うことで，複合語の意味を推定したい．しかしながら，複合語を正確に認定するのは大変むずかしいので，ここでは複合語からなる国名を認定したい．

インターネット上から国名リストを各自で入手し，80のコーパス中に出現する複合語の国名に関して，スペースをアンダーバーに置換せよ．例えば，"United States"は"United_States"，"Isle of Man"は"Isle_of_Man"になるはずである．
'''
def knock81(src_filename: str, dst_filename: str):
    countries = collections.OrderedDict()
    countries["Antigua and Barbuda"] = "Antigua_and_Barbuda" 
    countries["Bosnia and Herzegovina"] =  "Bosnia_and_Herzegovina"
    countries["Burkina Faso"] = "Burkina_Faso"
    countries["Cabo Verde"] = "Cabo_Verde"
    countries["Central African Republic"] = "Central_African_Republic"
    countries["Costa Rica"] = "Costa_Rica"
    countries["Cote d\'Ivoire"] = "Cote_d\'Ivoire"
    countries["Czech Republic"] = "Czech_Republic"
    countries["Democratic Republic of the Congo"] = "Democratic_Republic_of_the_Congo"
    countries["Dominican Republic"] = "Dominican_Republic"
    countries["East Timor"] = "East_Timor"
    countries["El Salvador"] = "El_Salvador"
    countries["Equatorial Guinea"] = "Equatorial_Guinea"
    countries["Guinea Bissau"] = "Guinea_Bissau"
    countries["Holy See"] = "Holy_See"
    countries["Hong Kong"] = "Hong_Kong"
    countries["Marshall Islands"] = "Marshall_Islands"
    countries["New Zealand"] = "New_Zealand"
    countries["North Korea"] = "North_Korea"
    countries["Palestinian Territories"] = "Palestinian_Territories"
    countries["Papua New Guinea"] = "Papua_New_Guinea"
    countries["Republic of the Congo "] = "Republic_of_the_Congo "
    countries["Saint Kitts and Nevis"] = "Saint_Kitts_and_Nevis"
    countries["Saint Lucia"] = "Saint_Lucia"
    countries["Saint Vincent and the Grenadines"] = "Saint_Vincent_and_the_Grenadines"
    countries["San Marino"] = "San_Marino"
    countries["Sao Tome and Principe"] = "Sao_Tome_and_Principe"
    countries["Saudi Arabia"] = "Saudi_Arabia"
    countries["Sierra Leone"] = "Sierra_Leone" 
    countries["Sint Maarten"] = "Sint_Maarten"
    countries["Solomon Islands"] = "Solomon_Islands"
    countries["South Africa"] = "South_Africa" 
    countries["South Korea"] = "South_Korea" 
    countries["South Sudan"] = "South_Sudan"
    countries["Sri Lanka"] = "Sri_Lanka"
    countries["The Bahamas"] = "The_Bahamas"
    countries["The Gambia"] = "The_Gambia"
    countries["Timor Leste"] = "Timor_Leste"
    countries["Trinidad and Tobago"] = "Trinidad_and_Tobago"
    countries["United Arab Emirates"] = "United_Arab_Emirates"
    countries["United Kingdom"] = "United_Kingdom"
    countries["United States of America"] = "United_States_of_America"
    countries["United States"] = "United_States" 
    with open(src_filename, 'r') as fds:
        with open(dst_filename, 'w') as fdd:
            for line in fds:
                for pattern in countries.keys():
                    if(re.search(pattern, line)):
                        line = re.sub(pattern, countries[pattern], line)
                fdd.write(line)
    return("Completed")

'''
82. 文脈の抽出
81で作成したコーパス中に出現するすべての単語 t に関して，単語 t と文脈語 c のペアをタブ区切り形式ですべて書き出せ．ただし，文脈語の定義は次の通りとする．
- ある単語 t の前後 d 単語を文脈語 c として抽出する（ただし，文脈語に単語 t そのものは含まない）
- 単語 t を選ぶ度に，文脈幅 d は {1,2,3,4,5} の範囲でランダムに決める．
'''
def knock82(src_filename:str, dst_filename:str):
    with open(src_filename, 'r') as fds:
        with open(dst_filename, 'w') as fdd:
            for line in fds:
                line = line.rstrip()
                words = line.split(' ')
                for index, word in enumerate(words):
                    index_range_pos = random.randint(1, 5)
                    index_range_neg = index_range_pos * -1
                    for index_delta in range(index_range_neg, index_range_pos):
                        if(index_delta == 0):
                            continue
                        if(index + index_delta < 0):
                            continue
                        if(index + index_delta > len(words)-1):
                            continue
                        fdd.write(word + "\t" + words[index + index_delta] + "\n")
    return("Completed")

'''
83. 単語／文脈の頻度の計測
82の出力を利用し，以下の出現分布，および定数を求めよ．
- f(t,c): 単語 t と文脈語 c の共起回数
- f(t,∗): 単語 t の出現回数
- f(∗,c): 文脈語 c の出現回数
- N: 単語と文脈語のペアの総出現回数
'''
def knock83(src_filename:str, dst_wco_filename:str, dst_wo_filename:str, dst_ct_filename:str, dst_total_count_filename:str):
    pair_total_count   = 0
    word_context_occur = dict()
    word_occur         = dict()
    context_occur      = dict()
    with open(src_filename, 'r') as fds:
        for line in fds:
            #(word, context) = line.rstrip().split('\t')
            (word, context) = line.split('\t')
            context = context.rstrip()
            word_context = word + "\t" + context
            word_context_occur[word_context] = word_context_occur.get(word_context, 0) + 1
            word_occur[word] = word_occur.get(word, 0) + 1
            context_occur[context] = context_occur.get(context, 0) + 1
            pair_total_count += 1
    with open(dst_wco_filename, 'w') as fdd:
        for key,value in word_context_occur.items():
            fdd.write(key + "\t" + str(value) + "\n")
    with open(dst_wo_filename, 'w') as fdd:
        for key,value in word_occur.items():
            fdd.write(key + "\t" + str(value) + "\n")
    with open(dst_ct_filename, 'w') as fdd:
        for key,value in context_occur.items():
            fdd.write(key + "\t" + str(value) + "\n")
    with open(dst_total_count_filename, 'w') as fdd:
        fdd.write(str(pair_total_count) + "\n")
    return("Completed")

'''
84. 単語文脈行列の作成
83の出力を利用し，単語文脈行列XXを作成せよ．ただし，行列 X の各要素 Xtc は次のように定義する．
- f(t,c)≥10f(t,c)≥10ならば，X_{tc} = PPMI(t,c)=max{ log( N×f(t,c) / f(t,∗)×f(∗,c) ), 0}
- f(t,c)<10f(t,c)<10ならば，X_{tc} = 0
ここで，PPMI(t,c) は Positive Pointwise Mutual Information（正の相互情報量）と呼ばれる統計量である．なお，行列 X の行数・列数は数百万オーダとなり，行列のすべての要素を主記憶上に載せることは無理なので注意すること．幸い，行列 X のほとんどの要素は 0 になるので，非 0 の要素だけを書き出せばよい．
'''
def knock84():
    return(None)

'''
85. 主成分分析による次元圧縮
84で得られた単語文脈行列に対して，主成分分析を適用し，単語の意味ベクトルを300次元に圧縮せよ．
'''
def knock85():
    return(None)

'''
86. 単語ベクトルの表示
85で得た単語の意味ベクトルを読み込み，"United States"のベクトルを表示せよ．ただし，"United States"は内部的には"United_States"と表現されていることに注意せよ．
'''
def knock86():
    return(None)

'''
87. 単語の類似度
85で得た単語の意味ベクトルを読み込み，"United States"と"U.S."のコサイン類似度を計算せよ．ただし，"U.S."は内部的に"U.S"と表現されていることに注意せよ．
'''
def knock87():
    return(None)

'''
88. 類似度の高い単語10件
85で得た単語の意味ベクトルを読み込み，"England"とコサイン類似度が高い10語と，その類似度を出力せよ．
'''
def knock88():
    return(None)

'''
89. 加法構成性によるアナロジー
85で得た単語の意味ベクトルを読み込み，vec("Spain") - vec("Madrid") + vec("Athens")を計算し，そのベクトルと類似度の高い10語とその類似度を出力せよ．
'''
def knock89():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 9')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 80):
        print(knock80("enwiki-20150112-400-r100-10576.txt", "ch9_knock90_enwiki.txt"))
    if(args.knock == 1 or args.knock == 81):
        print(knock81("ch9_knock90_enwiki.txt", "ch9_knock91_enwiki.txt"))
    if(args.knock == 2 or args.knock == 82):
        print(knock82("ch9_knock91_enwiki.txt", "ch9_knock92_enwiki.txt"))
    if(args.knock == 3 or args.knock == 83):
        print(knock83("ch9_knock92_enwiki.txt", "ch9_knock93_word_context.txt",
            "ch9_knock93_word.txt", "ch9_knock93_context,txt", "ch9_knock93_pair_occurrence.txt"))
    if(args.knock == 4 or args.knock == 84):
        print(knock84())
    if(args.knock == 5 or args.knock == 85):
        print(knock85())
    if(args.knock == 6 or args.knock == 86):
        print(knock86())
    if(args.knock == 7 or args.knock == 87):
        print(knock87())
    if(args.knock == 8 or args.knock == 88):
        print(knock88())
    if(args.knock == 9 or args.knock == 89):
        print(knock89())



