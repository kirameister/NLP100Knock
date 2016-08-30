# -*- coding: utf-8 -*-
# 第7章: データベース

import argparse


'''
artist.json.gzは，オープンな音楽データベースMusicBrainzの中で，アーティストに関するものをJSON形式に変換し，gzip形式で圧縮したファイルである．このファイルには，1アーティストに関する情報が1行にJSON形式で格納されている．JSON形式の概要は以下の通りである．

フィールド      型                              内容                    例
id              ユニーク識別子                  整数                    20660
gid             グローバル識別子                文字列                  "ecf9f3a3-35e9-4c58-acaa-e707fba45060"
name            アーティスト名                  文字列                  "Oasis"
sort_name       アーティスト名（辞書順整列用）  文字列                  "Oasis"
area            活動場所                        文字列                  "United Kingdom"
aliases         別名                            辞書オブジェクトのリスト    
aliases[].name  別名                            文字列                  "オアシス"
aliases[].sort_name 別名（整列用）              文字列                  "オアシス"
begin           活動開始日                      辞書    
begin.year      活動開始年                      整数                    1991
begin.month     活動開始月                      整数    
begin.date      活動開始日                      整数    
end             活動終了日                      辞書    
end.year        活動終了年                      整数                    2009
end.month       活動終了月                      整数                    8
end.date        活動終了日                      整数                    28
tags            タグ                            辞書オブジェクトのリスト    
tags[].count    タグ付けされた回数              整数                    1
tags[].value    タグ内容                        文字列                  "rock"
rating          レーティング                    辞書オブジェクト    
rating.count    レーティングの投票数            整数                    13
rating.value    レーティングの値（平均値）      整数                    86

artist.json.gzのデータをKey-Value-Store (KVS) およびドキュメント志向型データベースに格納・検索することを考える．KVSとしては，LevelDB，Redis，KyotoCabinet等を用いよ．ドキュメント志向型データベースとして，MongoDBを採用したが，CouchDBやRethinkDB等を用いてもよい．
'''


'''
60. KVSの構築
Key-Value-Store (KVS) を用い，アーティスト名（name）から活動場所（area）を検索するためのデータベースを構築せよ．
'''
def knock60():
    return(None)

'''
61. KVSの検索
60で構築したデータベースを用い，特定の（指定された）アーティストの活動場所を取得せよ．
'''
def knock61():
    return(None)

'''
62. KVS内の反復処理
60で構築したデータベースを用い，活動場所が「Japan」となっているアーティスト数を求めよ．
'''
def knock62():
    return(None)

'''
63. オブジェクトを値に格納したKVS
KVSを用い，アーティスト名（name）からタグと被タグ数（タグ付けされた回数）のリストを検索するためのデータベースを構築せよ．さらに，ここで構築したデータベースを用い，アーティスト名からタグと被タグ数を検索せよ．
'''
def knock63():
    return(None)

'''
64. MongoDBの構築
アーティスト情報（artist.json.gz）をデータベースに登録せよ．さらに，次のフィールドでインデックスを作成せよ: name, aliases.name, tags.value, rating.value
'''
def knock64():
    return(None)

'''
65. MongoDBの検索
MongoDBのインタラクティブシェルを用いて，"Queen"というアーティストに関する情報を取得せよ．さらに，これと同様の処理を行うプログラムを実装せよ．
'''
def knock65():
    return(None)

'''
66. 検索件数の取得
MongoDBのインタラクティブシェルを用いて，活動場所が「Japan」となっているアーティスト数を求めよ．
'''
def knock66():
    return(None)

'''
67. 複数のドキュメントの取得
特定の（指定した）別名を持つアーティストを検索せよ．
'''
def knock67():
    return(None)

'''
68. ソート
"dance"というタグを付与されたアーティストの中でレーティングの投票数が多いアーティスト・トップ10を求めよ．
'''
def knock68():
    return(None)

'''
69. Webアプリケーションの作成
ユーザから入力された検索条件に合致するアーティストの情報を表示するWebアプリケーションを作成せよ．アーティスト名，アーティストの別名，タグ等で検索条件を指定し，アーティスト情報のリストをレーティングの高い順などで整列して表示せよ．
'''
def knock69():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 7')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 60):
        print(knock60())
    if(args.knock == 1 or args.knock == 61):
        print(knock61())
    if(args.knock == 2 or args.knock == 62):
        print(knock62())
    if(args.knock == 3 or args.knock == 63):
        print(knock63())
    if(args.knock == 4 or args.knock == 64):
        print(knock64())
    if(args.knock == 5 or args.knock == 65):
        print(knock65())
    if(args.knock == 6 or args.knock == 66):
        print(knock66())
    if(args.knock == 7 or args.knock == 67):
        print(knock67())
    if(args.knock == 8 or args.knock == 68):
        print(knock68())
    if(args.knock == 9 or args.knock == 69):
        print(knock69())

