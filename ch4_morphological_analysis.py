# -*- coding: utf-8 -*-
# 第4章: 形態素解析

import argparse
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re


'''
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をMeCabを使って形態素解析し，その結果をneko.txt.mecabというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．

なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．
'''
def find_font(keyword):
    pattern = re.compile(".*" + keyword + ".*")
    all_fonts = fm.findSystemFonts()
    for font in all_fonts:
        if(pattern.search(font)):
            return(font)
    return(None)


'''
30. 形態素解析結果の読み込み
形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をキーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．第4章の残りの問題では，ここで作ったプログラムを活用せよ．
'''
def knock30():
    return_list = list()
    with open("./neko.txt.mecab", 'r') as f:
        for line in f:
            line = line.rstrip()
            if(line == "EOS"):
                continue
            dict = {}
            dict['surface'] = line.split('\t')[0]
            subline = line.split('\t')[1]
            dict['base'] = subline.split(',')[6]
            dict['pos'] = subline.split(',')[0]
            dict['pos1'] = subline.split(',')[1]
            return_list.append(dict)
    return(return_list)

'''
31. 動詞
動詞の表層形をすべて抽出せよ．
'''
def knock31():
    return_set = set()
    src_list = knock30()
    for item in src_list:
        if((item['pos'] == u"動詞") and (not item['surface'] in return_set)):
            return_set.add(item['surface'])
    return(return_set)

'''
32. 動詞の原形
動詞の原形をすべて抽出せよ．
'''
def knock32():
    return_set = set()
    src_list = knock30()
    for item in src_list:
        if((item['pos'] == u"動詞") and (not item['base'] in return_set)):
            return_set.add(item['base'])
    return(return_set)

'''
33. サ変名詞
サ変接続の名詞をすべて抽出せよ．
'''
def knock33():
    return_set = set()
    src_list = knock30()
    for item in src_list:
        if((item['pos'] == u"名詞") and (item['pos1'] == u"サ変接続") and (not item['surface'] in return_set)):
            return_set.add(item['surface'])
    return(return_set)

'''
34. 「AのB」
2つの名詞が「の」で連結されている名詞句を抽出せよ．
'''
def knock34():
    return_list = list()
    src_list = knock30()
    for i, item in enumerate(src_list):
        if(item["pos"] == u"名詞" and src_list[i+1]["pos1"] == u"連体化" and src_list[i+1]["base"] == u"の" and src_list[i+2]["pos"] == u"名詞"):
            return_list.append(item["surface"] + u"の" + src_list[i+2]["surface"])
    return(return_list)

'''
35. 名詞の連接
名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
'''
def knock35():
    return_list = list()
    previous_nouns = ""
    flag = 0
    src_list = knock30()
    for item in src_list:
        if(item["pos"] == u"名詞" and flag):
            previous_nouns += item["surface"]
            flag += 1
        if(item["pos"] == u"名詞" and (not flag)):
            previous_nouns = ""
            previous_nouns += item["surface"]
            previous_nouns = item["surface"]
            flag += 1
        else:
            if(previous_nouns != "" and flag > 1): 
                return_list.append(previous_nouns)
            previous_nouns = ""
            flag = 0
    return(return_list)

'''
36. 単語の出現頻度
文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
'''
def knock36():
    src_list = knock30()
    unsorted_dict = dict()
    for item in src_list:
        word = item["base"]
        unsorted_dict[word] = unsorted_dict.get(word, 0) + 1
    return(sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True))

'''
37. 頻度上位10語
出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
'''
def knock37():
    src_list = knock36()
    x = []
    x_names = []
    y = []
    for i in range(10):
        x.append(i)
        x_names.append(src_list[i][0])
        y.append(src_list[i][1])
    plt.bar(x, y, align="center")
    font_name = find_font("japanese")
    prop = fm.FontProperties(fname=font_name)
    if(prop):
        plt.xticks(x, x_names, fontproperties=prop)
    else:
        plt.xticks(x, x_names)
    plt.show()
    return(None)

'''
38. ヒストグラム
単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
'''
def knock38():
    src_list = knock36()
    size = len(src_list)
    x = []
    for i in src_list:
        x.append(i[1])
    #plt.hist(x_array, bins=size)
    plt.hist(x)
    plt.yscale('log')
    plt.show()
    return(None)

'''
39. Zipfの法則
単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
'''
def knock39():
    src_list = knock36()
    x = []
    y = []
    for i,v in enumerate(src_list):
        x.append(v[1])
        y.append(i)
    plt.plot(x,y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 4')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 30):
        print(knock30())
    if(args.knock == 1 or args.knock == 31):
        print(knock31())
    if(args.knock == 2 or args.knock == 32):
        print(knock32())
    if(args.knock == 3 or args.knock == 33):
        print(knock33())
    if(args.knock == 4 or args.knock == 34):
        print(knock34())
    if(args.knock == 5 or args.knock == 35):
        print(knock35())
    if(args.knock == 6 or args.knock == 36):
        print(knock36())
    if(args.knock == 7 or args.knock == 37):
        print(knock37())
    if(args.knock == 8 or args.knock == 38):
        print(knock38())
    if(args.knock == 9 or args.knock == 39):
        print(knock39())

