# -*- coding: utf -8 -*-
# 第1章: 準備運動 

import argparse
import random
import sys


'''
00. 文字列の逆順
文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．
'''
def knock00(string):
    return(string[::-1])

'''
01. 「パタトクカシーー」
「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字列を得よ．
'''
def knock01():
    string_org = u"パタトクカシーー"
    string_new = ""
    string_list = list(string_org)
    for (i,v) in enumerate(string_list):
        if(i in (0,2,4,6)):
            string_new = string_new + v
    return(string_new)

'''
02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
'''
def knock02():
    string1 = u"パトカー"
    string2 = u"タクシー"
    return_list = list()
    for (i,j) in zip(string1, string2):
        return_list.append(i)
        return_list.append(j)
    return("".join(return_list))

'''
03. 円周率
"Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．
'''
def knock03():
    string = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
    string_list = string.split()
    numbered_list = list()
    for word in string_list:
        numbered_list.append(len(word.rstrip(",.")))
    return(numbered_list)

'''
04. 元素記号
"Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."という文を単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．
'''
def knock04():
    string = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    string_list = string.split()
    string_list_new = list()
    for (i,word) in enumerate(string_list):
        if i+1 in (1, 5, 6, 7, 8, 9, 15, 16, 19):
            string_list_new.append(word[0:1:])
        else:
            string_list_new.append(word[0:2:])
    return(string_list_new)

'''
05. n-gram
与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．
'''
def knock05(n, mode, string):
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
                temp_string = temp_string + string_list[i+j]
        return_ngram.append(temp_string)
    return(return_ngram)

'''
06. 集合
"paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．
'''
def knock06():
    string_1 = "paraparaparadise"
    string_2 = "paragraph"
    X = set(knock05(2, "c", string_1))
    Y = set(knock05(2, "c", string_2))
    print("X: " + str(X))
    print("Y: " + str(Y))
    print("X+Y: %s" % (X.union(Y)))
    print("X*Y: %s" % (X.intersection(Y)))
    print("X-Y: %s" % (X.difference(Y)))
    print("Y-X: %s" % (Y.difference(X)))

    print("Is 'se' in X?: %s" % ('se' in X))
    print("Is 'se' in Y?: %s" % ('se' in Y))

    return(None)

'''
07. テンプレートによる文生成
引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．さらに，x=12, y="気温", z=22.4として，実行結果を確認せよ．
'''
def knock07(x, y, z):
    return_string = str(x) + u"時の" + str(y) + u"は" + str(z)
    return(return_string)

'''
08. 暗号文
与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．

英小文字ならば(219 - 文字コード)の文字に置換
その他の文字はそのまま出力
この関数を用い，英語のメッセージを暗号化・復号化せよ．
'''
def knock08(string): # the name of this function should perhpas be "cipher()"
    return_string = ""
    chars = list(string)
    for char in chars:
        if(not char.islower()):
            return_string = return_string + char
            continue
        ordered = ord(char)
        ordered = 219 - ordered
        char = chr(ordered)
        return_string = return_string + char
    return(return_string)

'''
09. Typoglycemia
スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文（例えば"I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."）を与え，その実行結果を確認せよ．
'''
def knock09(string):
    return_string = ""
    words = string.split()
    for word in words:
        if(len(word)>4):
            chars = list(word)
            first_char = chars.pop(0)
            last_char  = chars.pop()
            random.shuffle(chars)
            chars.insert(0,first_char)
            chars.append(last_char)
            word = "".join(chars)
        return_string = return_string + word + " "
    return(return_string.rstrip())

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 1')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    parser.add_argument('-m', '--mode', help="mode of n-gram, either 'w' or 'c'")
    parser.add_argument('-n', '--number', help="n in n-gram for knock05")
    args = parser.parse_args()

    if(args.knock == 0):
        if(not args.arg):
            args.arg = "stressed"
        print(knock00(args.arg))
    if(args.knock == 1):
        print(knock01())
    if(args.knock == 2):
        print(knock02())
    if(args.knock == 3):
        print(knock03())
    if(args.knock == 4):
        print(knock04())
    if(args.knock == 5):
        if(not args.mode):
            args.mode = "c"
        if(not args.arg):
            args.arg = "I am an NLPer"
        if(not args.number):
            args.number = 2
        print(knock05(int(args.number), args.mode, args.arg))
    if(args.knock == 6):
        #print(knock06())
        knock06()
    if(args.knock == 7):
        print(knock07(x=12, y="気温", z=22.4))
    if(args.knock == 8):
        if(not args.arg):
            args.arg = "Cipher ABC"
        print(knock08(args.arg))
    if(args.knock == 9):
        if(not args.arg):
            args.arg = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
        print(knock09(args.arg))
