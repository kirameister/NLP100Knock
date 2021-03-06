# -*- coding: utf-8 -*-
# 第6章: 英語テキストの処理

#from nltk.stem.snowball import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.porter import *
from pycorenlp import StanfordCoreNLP
from signal import signal, SIGPIPE, SIG_DFL
import argparse
import pydot
import re
import xml.etree.ElementTree as ET
signal(SIGPIPE,SIG_DFL)


'''
英語のテキスト（nlp.txt）に対して，以下の処理を実行せよ．
'''

'''
50. 文区切り
(. or ; or : or ? or !) → 空白文字 → 英大文字というパターンを文の区切りと見なし，入力された文書を1行1文の形式で出力せよ．
'''
def knock50():
    return_string = ""
    pattern = re.compile("[\.;:\?\!]")
    with open("./nlp.txt", 'r') as f:
        for line in f:
            line = re.sub("[\.;:\?\!]", '\n', line)
            return_string += line
    return(return_string)

'''
51. 単語の切り出し
空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．ただし，文の終端では空行を出力せよ．
'''
def knock51():
    src_string = knock50()
    return_string = ""
    for line in src_string:
        line = re.sub(' ', '\n', line)
        return_string += line
    return_string += "\n"
    return(return_string)

'''
52. ステミング
51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． Pythonでは，Porterのステミングアルゴリズムの実装としてstemmingモジュールを利用するとよい．
'''
def knock52():
    src_string = knock51().split("\n")
    return_string = ""
    stemmer = PorterStemmer()
    for line in src_string:
        line = line.rstrip()
        line = stemmer.stem(line)
        return_string += line + "\n"
    return(return_string)

'''
53. Tokenization
Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．
'''
def knock53():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for line in f:
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,ssplit', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for word in output_xml.findall(".//word"):
                return_list.append(word.text)
    return(return_list)

'''
54. 品詞タグ付け
Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．
'''
def knock54():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for line in f:
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,lemma,ssplit,pos', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for token in output_xml.findall(".//token"):
                word  = token.find('word').text
                lemma = token.find('lemma').text
                pos   = token.find("POS").text
                return_list.append(word + "\t" + lemma + "\t" + pos)
    return(return_list)

'''
55. 固有表現抽出
入力文中の人名をすべて抜き出せ．
'''
def knock55():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for line in f:
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,lemma,ssplit,pos,ner', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for token in output_xml.findall(".//token"):
                word  = token.find('word').text
                lemma = token.find('lemma').text
                pos   = token.find("POS").text
                ner   = token.find("NER").text
                if((pos == "NNP"or pos == "NNPS") and ner in ["ORGANIZATION", "MISC", "LOCATION", "PERSON"]):
                    return_list.append(word + "\t" + lemma + "\t" + pos + "\t" + ner)
    return(return_list)

'''
56. 共参照解析
Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．ただし，置換するときは，「代表参照表現（参照表現）」のように，元の参照表現が分かるように配慮せよ．
cf. http://nlp.stanford.edu/software/dcoref.shtml
'''
def knock56():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for line in f:
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,lemma,ssplit,pos,parse,dcoref', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for token in output_xml.findall(".//document/coreference/coreference"):
                for mention in token.findall("mention"):
                    attribute = mention.get("representative")
                    if(attribute):
                        mentioned = mention.find("text").text
                    else:
                        rep_mentioned = mention.find("text").text
                return_list.append(rep_mentioned + "(" + mentioned + ")")
    return(return_list)

'''
57. 係り受け解析
Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
'''
def knock57(number):
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for i, line in enumerate(f):
            # In order to avoid creating too big graph, following lines limit the input text to be specified linei in the input text. 
            if(i != number):
                continue
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,lemma,ssplit,pos,parse', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for dependency in output_xml.findall(".//dependencies[@type='collapsed-dependencies']"):
                for dep in dependency.findall(".//dep"):
                    type_name = dep.get("type")
                    governor = dep.find("governor").text
                    dependent = dep.find("dependent").text
                    print(governor + " -"+type_name+"-> " + dependent)
                    if(type_name == "punct"):
                        continue
                    return_list.append((governor, dependent))
    return(return_list)

'''
58. タプルの抽出
Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）に基づき，「主語 述語 目的語」の組をタブ区切り形式で出力せよ．ただし，主語，述語，目的語の定義は以下を参考にせよ．
- 述語: nsubj関係とdobj関係の子（dependant）を持つ単語
- 主語: 述語からnsubj関係にある子（dependent）
- 目的語: 述語からdobj関係にある子（dependent）
'''
def knock58():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    with open("./nlp.txt", 'r') as f:
        for line in f:
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'tokenize,lemma,ssplit,pos,parse', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            for dependency in output_xml.findall(".//dependencies[@type='collapsed-dependencies']"):
                dobjs  = {}
                nsubjs = {}
                # search for the subj and dobj references
                for dep in dependency.findall(".//dep"):
                    type_name = dep.get("type")
                    governor = dep.find("governor").text
                    governor_id = dep.find("governor").get("idx")
                    dependent = dep.find("dependent").text
                    dependent_id = dep.find("dependent").get("idx")
                    if(type_name == "punct"):
                        continue
                    #print(governor +"("governor_id+")" + " -"+type_name+"-> " + dependent +"("+dependent_id+")")
                    if(type_name == "nsubj"):
                        nsubjs[governor_id] = governor + "\t" + dependent
                    if(type_name == "dobj"):
                        dobjs[governor_id]  = dependent
                # extract subj->verb->dobj tuples
                for gov_id, sub_verb_value in nsubjs.items():
                    if(dobjs.get(gov_id, None)):
                        return_list.append(nsubjs[gov_id] + "\t" + dobjs[gov_id])
    return(return_list)

'''
59. S式の解析
Stanford Core NLPの句構造解析の結果（S式）を読み込み，文中のすべての名詞句（NP）を表示せよ．入れ子になっている名詞句もすべて表示すること．
'''
def knock59(number):
    nlp = StanfordCoreNLP('http://localhost:9000')
    return_list = []
    pattern = re.compile("^(\s*)(.*)")
    with open("./nlp.txt", 'r') as f:
        for i, line in enumerate(f):
            if(i != number):
                continue
            output = nlp.annotate(line, properties={'timeout': '50000', 'annotators': 'parse', 'outputFormat': 'xml' })
            output_xml = ET.fromstring(output)
            parsed_lines = output_xml.find(".//parse").text.split("\n")
            for i in range(len(parsed_lines)):
                re_result_i = pattern.search(parsed_lines[i].rstrip("\n"))
                space_len_i = len(re_result_i.group(1))
                content_i = re_result_i.group(2)
                if(content_i.startswith("(NP")):
                    current_NP = ""
                    for j in range(i, len(parsed_lines)):
                        if(i == j):
                            current_NP = content_i
                            continue
                        re_result_j = pattern.search(parsed_lines[j].rstrip("\n"))
                        space_len_j = len(re_result_j.group(1))
                        content_j = re_result_j.group(2)
                        if(space_len_i >= space_len_j):
                            break
                        else:
                            current_NP += content_j.strip("\n")
                    return_list.append(current_NP)
    return(return_list)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Ch 6')
    parser.add_argument('knock', type=int, help="Number of knock")
    parser.add_argument('-a', '--arg', help="Additional argument where appropriate")
    parser.add_argument('-n', '--number', help="Natural number")
    args = parser.parse_args()

    if(args.knock == 0 or args.knock == 50):
        print(knock50())
    if(args.knock == 1 or args.knock == 51):
        print(knock51())
    if(args.knock == 2 or args.knock == 52):
        print(knock52())
    if(args.knock == 3 or args.knock == 53):
        print("\n".join(knock53()))
    if(args.knock == 4 or args.knock == 54):
        print("\n".join(knock54()))
    if(args.knock == 5 or args.knock == 55):
        print("\n".join(knock55()))
    if(args.knock == 6 or args.knock == 56):
        print("\n".join(knock56()))
    if(args.knock == 7 or args.knock == 57):
        if(not args.arg):
            args.arg = "knock57_output"
        if(not ( args.arg.endswith("jpg") or args.arg.endswith("jpeg") ) ):
            args.arg += ".jpeg"
        if(not args.number):
            args.number = 3
        return_list = knock57(int(args.number))
        print(return_list)
        print("Output file: " + args.arg)
        g = pydot.graph_from_edges(return_list)
        g.set_type('digraph')
        g.write_jpeg(args.arg, prog="dot")
    if(args.knock == 8 or args.knock == 58):
        print("\n".join(knock58()))
    if(args.knock == 9 or args.knock == 59):
        if(not args.number):
            args.number = 3
        print("\n".join(knock59(args.number)))

