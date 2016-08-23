# -*- coding: utf -8 -*-
# 第2章: UNIXコマンドの基礎

from collections import OrderedDict
import argparse
import codecs
import re
import sys


'''
hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．
'''

'''
10. 行数のカウント
行数をカウントせよ．確認にはwcコマンドを用いよ．
'''
def knock10():
    with open("hightemp.txt") as f:
        lines = f.readlines()
    return(len(lines))

'''
11. タブをスペースに置換
タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．
'''
def knock11():
    return_string = ""
    with open("hightemp.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub("\t", " ", line)
            return_string = return_string + line
    return(return_string)

'''
12. 1列目をcol1.txtに，2列目をcol2.txtに保存
各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．確認にはcutコマンドを用いよ．
'''
def knock12():
    try:
        col1_fd = open("col1.txt", 'w')
        col2_fd = open("col2.txt", 'w')
    except:
        print("Unexpected Error" + sys.exec_info()[0])
        raise
    with open("hightemp.txt") as src:
        lines = src.readlines()
        for line in lines:
            col1_string = line.split('\t')[0]
            col2_string = line.split('\t')[1]
            col1_fd.write(col1_string+"\n")
            col2_fd.write(col2_string+"\n")
    col1_fd.close()
    col2_fd.close()
    return("Done")

'''
13. col1.txtとcol2.txtをマージ
12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．
'''
def knock13():
    return_string = ""
    try:
        col1_fd = open("col1.txt", 'r')
        col2_fd = open("col2.txt", 'r')
    except:
        print("Unexpected Error" + sys.exec_info()[0])
        raise
    for col1_line, col2_line in zip(col1_fd, col2_fd):
        return_string = return_string + col1_line.rstrip() + "\t" + col2_line.rstrip() + "\n"
    col1_fd.close()
    col2_fd.close()
    return(return_string)

'''
14. 先頭からN行を出力
自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．確認にはheadコマンドを用いよ．
'''
def knock14(number):
    return_string = ""
    with open("hightemp.txt") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if(index >= number):
                break
            return_string = return_string + line
    return(return_string)

'''
15. 末尾のN行を出力
自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．
'''
def knock15(number):
    return_string = ""
    with open("hightemp.txt") as f:
        lines = f.readlines()
        number_lines = len(lines)
        for index in range(number_lines - number, number_lines):
            return_string = return_string + lines[index]
    return(return_string)

'''
16. ファイルをN分割する
自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．
'''
def knock16(number):
    with open("hightemp.txt") as f:
        src_lines = f.readlines()
        all_lines_size = len(src_lines)
        each_file_size = all_lines_size // number
        for i in range(number):
            with open("split%s" % i, 'w') as dest_file:
                for j in range(each_file_size + 1):
                    try:
                        dest_file.write(src_lines[(i*(each_file_size+1))+j])
                        pass
                    except:
                        return("Done")
    return("Done")

'''
17. １列目の文字列の異なり
1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはsort, uniqコマンドを用いよ．
'''
def knock17():
    word_set = set()
    with codecs.open("hightemp.txt", 'r', "utf-8") as f:
        for line in f:
            col1 = line.split('\t')[0]
            if(col1 not in word_set):
                word_set.add(col1)
    return(word_set) # Note that the sets is returned -> need to do post-process with encoding

'''
18. 各行を3コラム目の数値の降順にソート
各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．

sort -n -r -k 3 hightemp.txt
'''
def knock18():
    org_data = []
    with codecs.open("hightemp.txt", 'r', "utf-8") as f:
        for line in f:
            org_data.append(line.rstrip().split("\t"))
    sorted_data = sorted(org_data, key=lambda x: x[2], reverse=True)
    for line in sorted_data:
        print("\t".join(line))
    return("Done") # This can be made better by handing over to the main function

'''
19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．確認にはcut, uniq, sortコマンドを用いよ．

cat hightemp.txt | cut -f 1 | sort | uniq -c | sort -nr
'''
def knock19():
    words = {}
    with codecs.open("hightemp.txt", 'r', "utf-8") as f:
        for line in f:
            word = line.split('\t')[0]
            words[word] = words.setdefault(word, 0) + 1
            #words[word] = words.get(word, 0) + 1 # another way to add existing value in dict
            #try: # yet another way to do this
            #    words[word] = words[word] + 1
            #except KeyError:
            #    words[word] = 1
    #for i,v in sorted(words.items(), key=lambda x:x[1], reverse=True):
    #    print(i.encode('utf-8') + "\t" + str(v).encode('utf-8'))
    return(OrderedDict(sorted(words.items(), key=lambda x:x[1], reverse=True)))

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 2')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    parser.add_argument('-n', '--number', help="Natural number")
    args = parser.parse_args()

    if(not args.number):
        args.number = 5

    if(args.knock == 0 or args.knock == 10):
        print(knock10())
    if(args.knock == 1 or args.knock == 11):
        print(knock11())
    if(args.knock == 2 or args.knock == 12):
        print(knock12())
    if(args.knock == 3 or args.knock == 13):
        #print(knock13(), end="")
        print(knock13())
    if(args.knock == 4 or args.knock == 14):
        #print(knock14(args.number), end="")
        print(knock14(args.number))
    if(args.knock == 5 or args.knock == 15):
        print(knock15(args.number))
    if(args.knock == 6 or args.knock == 16):
        print(knock16(args.number))
    if(args.knock == 7 or args.knock == 17):
        print(knock17())
    if(args.knock == 8 or args.knock == 18):
        print(knock18())
    if(args.knock == 9 or args.knock == 19):
        #print(str(knock19()).encode('utf-8'))
        print(knock19())

