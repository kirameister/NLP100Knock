# -*- coding: utf-8 -*-
# 第5章: 係り受け解析

from signal import signal, SIGPIPE, SIG_DFL
import argparse
import re
import pydot
signal(SIGPIPE,SIG_DFL)


'''
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をCaboChaを使って係り受け解析し，その結果をneko.txt.cabochaというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．
'''

'''
40. 係り受け解析結果の読み込み（形態素）
形態素を表すクラスMorphを実装せよ．このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つこととする．さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
'''
class Morph(object):
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base    = base
        self.pos     = pos
        self.pos1    = pos1

def knock40():
    submorph_list = []
    morph_list    = []
    validation_pattern = re.compile("(.*?)\t")
    with open("./neko.txt.cabocha") as f:
        for line in f:
            if(re.match("\t.*\t",line)):
                continue
            if('\t' in line):
                (surface, remaining) = line.split("\t")
                base = remaining.split(',')[6]
                pos  = remaining.split(',')[0]
                pos1 = remaining.split(',')[1]
                morph = Morph(surface, base, pos, pos1)
                submorph_list.append(morph)
            if(line.rstrip() == u"EOS"):
                morph_list.append(submorph_list)
                submorph_list = []
    return(morph_list)

'''
41. 係り受け解析結果の読み込み（文節・係り受け）
40に加えて，文節を表すクラスChunkを実装せよ．このクラスは形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．さらに，入力テキストのCaboChaの解析結果を読み込み，１文をChunkオブジェクトのリストとして表現し，8文目の文節の文字列と係り先を表示せよ．第5章の残りの問題では，ここで作ったプログラムを活用せよ．
'''
class Chunk(object):
    # This class represents one chunk, NOT one sentence. 
    def __init__(self, morphs, dst, srcs):
        self.morphs = morphs # list of Morph classes
        self.dst    = dst    # int: ID of that chunk in sentence
        self.srcs   = srcs   # list of IDs referring to this chunk
    def get_base(self):
        base_text = ""
        for morph in self.morphs:
            base_text += " " + morph.base
        return(base_text)
    def get_surface(self):
        surface_text = ""
        for morph in self.morphs:
            surface_text += " " + morph.surface
        return(surface_text)
    def get_surface_without_punctuation(self):
        surface_text = ""
        for morph in self.morphs:
            if(u"記号" in morph.pos):
                continue
            surface_text += " " + morph.surface
        return(surface_text)
    def get_list_of_pos(self):
        return_list = []
        for morph in self.morphs:
            return_list.append(morph.pos)
        return(return_list)

def knock41():
    return_sentence_list = []
    chunk_list           = []
    morph_list           = []
    srcs                 = []
    chunk_number         = 0
    with open("./neko.txt.cabocha", 'r') as f:
        for line in f:
            if(re.search(u"^\*", line)):
                # line with dependency information
                elements = line.split(" ")
                chunk_number = int(elements[1])
                dst = int(elements[2].rstrip("D"))
                # because the actual text is shown AFTER this line, this is only initialization
                chunk_list.append(Chunk(morphs=[], dst=dst, srcs=[]))
                morph_list = []
            if('\t' in line):
                # storing morphme
                (surface, remaining) = line.split("\t")
                base = remaining.split(',')[6]
                pos  = remaining.split(',')[0]
                pos1 = remaining.split(',')[1]
                morph = Morph(surface, base, pos, pos1)
                chunk_list[chunk_number].morphs.append(morph)
            if(line.rstrip() == u"EOS"):
                # end of the sentence = need to wrap up for this sentence
                ## Update the srcs list for each chunk in the sentence 
                for i in range(chunk_number):
                    if(chunk_list[i].dst == -1):
                        continue
                    chunk_list[chunk_list[i].dst].srcs.append(int(i))
                return_sentence_list.append(chunk_list)
                chunk_list = []
                morph_list = []
                srcs = []
                chunk_number = 0
    return(return_sentence_list)

'''
42. 係り元と係り先の文節の表示
係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
'''
def knock42():
    return_list = []
    for sentence in knock41():
        return_list.append("New sentence")
        for chunk in sentence:
            if(chunk.dst == -1):
                continue
            return_list.append(chunk.get_surface() + "\t" + sentence[chunk.dst].get_surface_without_punctuation())
    return(return_list)

'''
43. 名詞を含む文節が動詞を含む文節に係るものを抽出
名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．ただし，句読点などの記号は出力しないようにせよ．
'''
def knock43():
    return_list = []
    for sentence in knock41():
        return_list.append("New sentence")
        for i, chunk in enumerate(sentence):
            j = sentence[i].dst
            src_pos_list = sentence[i].get_list_of_pos()
            dst_pos_list = sentence[j].get_list_of_pos()
            if(u"名詞" in src_pos_list and u"動詞" in dst_pos_list):
                return_list.append(sentence[i].get_surface() + "\t" + sentence[j].get_surface_without_punctuation())
    return(return_list)

'''
44. 係り受け木の可視化
与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
'''
def knock44(sentence_id):
    return_list = []
    sentence = knock41()[sentence_id]
    for i, chunk in enumerate(sentence):
        j = sentence[i].dst
        referring = sentence[i].get_surface()
        referred  = sentence[j].get_surface()
        return_list.append((referring, referred))
    return(return_list)

'''
45. 動詞の格パターンの抽出
今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を調査したい． 動詞を述語，動詞に係っている文節の助詞を格と考え，述語と格をタブ区切り形式で出力せよ． ただし，出力は以下の仕様を満たすようにせよ．
- 動詞を含む文節において，最左の動詞の基本形を述語とする
- 述語に係る助詞を格とする
- 述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる

「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
    始める  で
    見る    は を
このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
- コーパス中で頻出する述語と格パターンの組み合わせ
- 「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
-- python ch5_dependency_parsing.py 5 | egrep "^(する|見る|与える)" | sort | uniq -c | sort -nr
'''
def knock45():
    return_list = []
    for sentence in knock41():
        for chunk in sentence:
            if(chunk.morphs[0].pos == u"動詞"):
                particle_list = []
                for src_id in chunk.srcs:
                    for morph in sentence[src_id].morphs:
                        if(morph.pos == u"助詞"):
                            particle_list.append(morph.base)
                if(len(particle_list) > 0):
                    particles = " ".join(particle_list)
                    return_list.append(chunk.morphs[0].base + "\t" + particles)
    return(return_list)

'''
46. 動詞の格フレーム情報の抽出
45のプログラムを改変し，述語と格パターンに続けて項（述語に係っている文節そのもの）をタブ区切り形式で出力せよ．45の仕様に加えて，以下の仕様を満たすようにせよ．
- 項は述語に係っている文節の単語列とする（末尾の助詞を取り除く必要はない）
- 述語に係る文節が複数あるときは，助詞と同一の基準・順序でスペース区切りで並べる

「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
    始める  で      ここで
    見る    は を   吾輩は ものを
'''
def knock46():
    return_list = []
    for sentence in knock41():
        for chunk in sentence:
            if(chunk.morphs[0].pos == u"動詞"):
                particle_list = []
                chunk_text_list = []
                for src_id in chunk.srcs:
                    for morph in sentence[src_id].morphs:
                        if(morph.pos == u"助詞"):
                            particle_list.append(morph.base)
                            surface_text = re.sub(' ', '', sentence[src_id].get_surface())
                            chunk_text_list.append(surface_text)
                if(len(particle_list) > 0):
                    particles   = " ".join(particle_list)
                    chunk_texts = " ".join(chunk_text_list)
                    return_list.append(chunk.morphs[0].base + "\t" + particles + "\t" + chunk_texts)
    return(return_list)

'''
47. 機能動詞構文のマイニング
動詞のヲ格にサ変接続名詞が入っている場合のみに着目したい．46のプログラムを以下の仕様を満たすように改変せよ．
- 「サ変接続名詞+を（助詞）」で構成される文節が動詞に係る場合のみを対象とする
- 述語は「サ変接続名詞+を+動詞の基本形」とし，文節中に複数の動詞があるときは，最左の動詞を用いる
- 述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
- 述語に係る文節が複数ある場合は，すべての項をスペース区切りで並べる（助詞の並び順と揃えよ）

例えば「別段くるにも及ばんさと、主人は手紙に返事をする。」という文から，以下の出力が得られるはずである．
    返事をする      と に は        及ばんさと 手紙に 主人は
このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
- コーパス中で頻出する述語（サ変接続名詞+を+動詞）
- コーパス中で頻出する述語と助詞パターン
'''
def knock47():
    return_list = []
    return(return_list)

'''
48. 名詞から根へのパスの抽出
文中のすべての名詞を含む文節に対し，その文節から構文木の根に至るパスを抽出せよ． ただし，構文木上のパスは以下の仕様を満たすものとする．
- 各文節は（表層形の）形態素列で表現する
- パスの開始文節から終了文節に至るまで，各文節の表現を"->"で連結する

「吾輩はここで始めて人間というものを見た」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
    吾輩は -> 見た
    ここで -> 始めて -> 人間という -> ものを -> 見た
    人間という -> ものを -> 見た
    ものを -> 見た
'''
def knock48():
    return(None)

'''
49. 名詞間の係り受けパスの抽出
文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．ただし，名詞句ペアの文節番号が i と j （i<j）のとき，係り受けパスは以下の仕様を満たすものとする．
- 問題48と同様に，パスは開始文節から終了文節に至るまでの各文節の表現（表層形の形態素列）を"->"で連結して表現する
- 文節 i と j に含まれる名詞句はそれぞれ，X と Y に置換する

また，係り受けパスの形状は，以下の2通りが考えられる．
- 文節 i から構文木の根に至る経路上に文節 j が存在する場合: 文節 i から文節 j のパスを表示
- 上記以外で，文節 i と文節 j から構文木の根に至る経路上で共通の文節 k で交わる場合: 文節 i から文節 k に至る直前のパスと文節 j から文節 k に至る直前までのパス，文節 k の内容を "|" で連結して表示

例えば，「吾輩はここで始めて人間というものを見た。」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
    Xは | Yで -> 始めて -> 人間という -> ものを | 見た
    Xは | Yという -> ものを | 見た
    Xは | Yを | 見た
    Xで -> 始めて -> Y
    Xで -> 始めて -> 人間という -> Y
    Xという -> Y
'''
def knock49():
    return(None)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 5')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    parser.add_argument('-n', '--num', help="Sentence ID to process for knock44")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 40):
        for morph in knock40()[2]:
            print(morph.surface + "\t" + morph.pos + "\t" + morph.pos1)
    if(args.knock == 1 or args.knock == 41):
        if(not args.arg):
            args.arg = 7
        print("ID \t surface \t DST \t SRCS")
        for (i, chunk) in enumerate(knock41()[int(args.arg)]):
            surface_text = chunk.get_surface()
            src_text = ""
            for src in chunk.srcs:
                src_text += " " + str(src)
            print(str(i) + "\t" + surface_text + "\t" + str(chunk.dst) + "\t" + src_text)
    if(args.knock == 2 or args.knock == 42):
        print("\n".join(knock42()))
    if(args.knock == 3 or args.knock == 43):
        print("\n".join(knock43()))
    if(args.knock == 4 or args.knock == 44):
        if(not args.num):
            args.num = 7
        if(not args.arg):
            args.arg = "knock44_output"
        if(not ( args.arg.endswith("jpg") or args.arg.endswith("jpeg") ) ):
            args.arg += ".jpeg"
        returned_list = knock44(int(args.num))
        print(returned_list)
        print("Output file: " + args.arg)
        g = pydot.graph_from_edges(returned_list)
        g.set_type('digraph')
        g.write_jpeg(args.arg, prog="dot")
    if(args.knock == 5 or args.knock == 45):
        print("\n".join(knock45()))
    if(args.knock == 6 or args.knock == 46):
        print("\n".join(knock46()))
    if(args.knock == 7 or args.knock == 47):
        print(knock47())
    if(args.knock == 8 or args.knock == 48):
        print(knock48())
    if(args.knock == 9 or args.knock == 49):
        print(knock49())

