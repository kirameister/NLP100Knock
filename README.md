# NLP100Knock
[言語処理100本ノック 2015](http://www.cl.ecei.tohoku.ac.jp/nlp100/)

## 動作環境

Python 3.5 での動作を想定しています。

必要になるライブラリがあることを保証するため Virtualenv を使っています。以下のコマンドにより環境内に入ることができます:
```
source ./bin/activate
```

## 動作に必要なファイル

必要なファイルは Makefile にて記述されています。以下のコマンドにより、スクリプトの入力ファイルが取得されます:
```
make
```

## 動作

第六章では以下の様なコマンドにより、Stanford CoreNLP Server を起動する必要があります:
```
cd stanford-corenlp-full-2015-12-09/
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
```



