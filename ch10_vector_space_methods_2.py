# -*- coding: utf-8 -*-
#第10章: ベクトル空間法 (II)


import argparse


'''
第10章では，前章に引き続き単語ベクトルの学習に取り組む．
'''

'''
90. word2vecによる学習
81で作成したコーパスに対してword2vecを適用し，単語ベクトルを学習せよ．さらに，学習した単語ベクトルの形式を変換し，86-89のプログラムを動かせ．
'''
def knock90():
    return(None)

'''
91. アナロジーデータの準備
単語アナロジーの評価データをダウンロードせよ．このデータ中で": "で始まる行はセクション名を表す．例えば，": capital-common-countries"という行は，"capital-common-countries"というセクションの開始を表している．ダウンロードした評価データの中で，"family"というセクションに含まれる評価事例を抜き出してファイルに保存せよ．
'''
def knock91():
    return(None)

'''
92. アナロジーデータへの適用
91で作成した評価データの各事例に対して，vec(2列目の単語) - vec(1列目の単語) + vec(3列目の単語)を計算し，そのベクトルと類似度が最も高い単語と，その類似度を求めよ．求めた単語と類似度は，各事例の末尾に追記せよ．このプログラムを85で作成した単語ベクトル，90で作成した単語ベクトルに対して適用せよ．
'''
def knock92():
    return(None)

'''
93. アナロジータスクの正解率の計算
92で作ったデータを用い，各モデルのアナロジータスクの正解率を求めよ．
'''
def knock93():
    return(None)

'''
94. WordSimilarity-353での類似度計算
The WordSimilarity-353 Test Collectionの評価データを入力とし，1列目と2列目の単語の類似度を計算し，各行の末尾に類似度の値を追加するプログラムを作成せよ．このプログラムを85で作成した単語ベクトル，90で作成した単語ベクトルに対して適用せよ．
'''
def knock94():
    return(None)

'''
95. WordSimilarity-353での評価
94で作ったデータを用い，各モデルが出力する類似度のランキングと，人間の類似度判定のランキングの間のスピアマン相関係数を計算せよ．
'''
def knock95():
    return(None)

'''
96. 国名に関するベクトルの抽出
word2vecの学習結果から，国名に関するベクトルのみを抜き出せ．
'''
def knock96():
    return(None)

'''
97. k-meansクラスタリング
96の単語ベクトルに対して，k-meansクラスタリングをクラスタ数k=5k=5として実行せよ．
'''
def knock97():
    return(None)

'''
98. Ward法によるクラスタリング
96の単語ベクトルに対して，Ward法による階層型クラスタリングを実行せよ．さらに，クラスタリング結果をデンドログラムとして可視化せよ．
'''
def knock98():
    return(None)

'''
99. t-SNEによる可視化
96の単語ベクトルに対して，ベクトル空間をt-SNEで可視化せよ．
'''
def knock99():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 10')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 90):
        print(knock90())
    if(args.knock == 1 or args.knock == 91):
        print(knock91())
    if(args.knock == 2 or args.knock == 92):
        print(knock92())
    if(args.knock == 3 or args.knock == 93):
        print(knock93())
    if(args.knock == 4 or args.knock == 94):
        print(knock94())
    if(args.knock == 5 or args.knock == 95):
        print(knock95())
    if(args.knock == 6 or args.knock == 96):
        print(knock96())
    if(args.knock == 7 or args.knock == 97):
        print(knock97())
    if(args.knock == 8 or args.knock == 98):
        print(knock98())
    if(args.knock == 9 or args.knock == 99):
        print(knock99())


