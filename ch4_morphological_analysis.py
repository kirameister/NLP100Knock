# -*- coding: utf-8 -*-
# 第4章: 形態素解析

import argparse


'''
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をMeCabを使って形態素解析し，その結果をneko.txt.mecabというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．

なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．
'''

'''
30. 形態素解析結果の読み込み
形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をキーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．第4章の残りの問題では，ここで作ったプログラムを活用せよ．
'''
def knock30():
    return(None)

'''
31. 動詞
動詞の表層形をすべて抽出せよ．
'''
def knock31():
    return(None)

'''
32. 動詞の原形
動詞の原形をすべて抽出せよ．
'''
def knock32():
    return(None)

'''
33. サ変名詞
サ変接続の名詞をすべて抽出せよ．
'''
def knock33():
    return(None)

'''
34. 「AのB」
2つの名詞が「の」で連結されている名詞句を抽出せよ．
'''
def knock34():
    return(None)

'''
35. 名詞の連接
名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
'''
def knock35():
    return(None)

'''
36. 単語の出現頻度
文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
'''
def knock36():
    return(None)

'''
37. 頻度上位10語
出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
'''
def knock37():
    return(None)

'''
38. ヒストグラム
単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
'''
def knock38():
    return(None)

'''
39. Zipfの法則
単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
'''
def knock39():
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

