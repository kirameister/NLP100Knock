# -*- coding: utf -8 -*-
# 第3章: 正規表現

import argparse
import codecs
import json
import re


'''
Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．

1行に1記事の情報がJSON形式で格納される
各行には記事名が"title"キーに，記事本文が"text"キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
ファイル全体はgzipで圧縮される
以下の処理を行うプログラムを作成せよ．
'''

'''
20. JSONデータの読み込み
Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．
'''
def knock20():
    return_string = ""
    with codecs.open("jawiki-country.json", 'r', 'utf-8') as fd:
        for line in fd:
            data = json.loads(line)
            if(data["title"] == u"イギリス"):
                return_string = return_string + str(data["text"])
    return(return_string)

'''
21. カテゴリ名を含む行を抽出
記事中でカテゴリ名を宣言している行を抽出せよ．
'''
def knock21():
    return_string = ""
    pattern = re.compile(u"\[\[Category.*\]\]")
    data = knock20().split() # Need to consider it as array otherwise 
    for line in data:
        if(pattern.search(line)):
            return_string += line + "\n"
    return(return_string)

'''
22. カテゴリ名の抽出
記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．
'''
def knock22():
    return_string = ""
    pattern = re.compile(u"\[\[Category:(.*)\]\]")
    data = knock20().split()
    for line in data:
        if(pattern.search(line)):
            match_result = pattern.search(line)
            return_string += match_result.group(1) + "\n"
    return(return_string)

'''
23. セクション構造
記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．
'''
def knock23():
    return_string = ""
    levels = re.compile(u"^(=+)([^=]+?)(=+)$")
    data = knock20().split()
    for line in data:
        if(levels.search(line)):
            match_result = levels.search(line)
            return_string += str(len(match_result.group(1))-1) + ": " + match_result.group(2) + "\n"
    return(return_string)

'''
24. ファイル参照の抽出
記事から参照されているメディアファイルをすべて抜き出せ．
'''
def knock24():
    return(None)

'''
25. テンプレートの抽出
記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．
'''
def knock25():
    return(None)

'''
26. 強調マークアップの除去
25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ（参考: マークアップ早見表）．
'''
def knock26():
    return(None)

'''
27. 内部リンクの除去
26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ（参考: マークアップ早見表）．
'''
def knock27():
    return(None)

'''
28. MediaWikiマークアップの除去
27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．
'''
def knock28():
    return(None)

'''
29. 国旗画像のURLを取得する
テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）
'''
def knock29():
    return(None)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 3')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 20):
        print(knock20())
    if(args.knock == 1 or args.knock == 21):
        print(knock21())
    if(args.knock == 2 or args.knock == 22):
        print(knock22())
    if(args.knock == 3 or args.knock == 23):
        print(knock23())
    if(args.knock == 4 or args.knock == 24):
        print(knock24())
    if(args.knock == 5 or args.knock == 25):
        print(knock25())
    if(args.knock == 6 or args.knock == 26):
        print(knock26())
    if(args.knock == 7 or args.knock == 27):
        print(knock27())
    if(args.knock == 8 or args.knock == 28):
        print(knock28())
    if(args.knock == 9 or args.knock == 29):
        print(knock29())

