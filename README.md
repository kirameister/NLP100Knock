# NLP100Knock
[言語処理100本ノック 2015](http://www.cl.ecei.tohoku.ac.jp/nlp100/)

## 動作環境

Python 3.5 での動作を想定しています。

必要になるライブラリがあることを保証するため virtualenv 環境を作成し、必要なパッケージを (init.sh 経由で) pip によりインストールすることを想定しています。
git clone を行った後は、以下のコマンドにより必要なパッケージを virtualenv 内に構築してください:
```
sh ./init.sh
```

構築した後で別セッション / 新規セッションを起動した場合、以下のコマンドにより環境内に入ることができます:
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

第七章の前半部 (knock60 から knock63 まで) では NoSQL DB として Redis を使用しています。スクリプトを起動する前にローカル環境で Redis のサーバープロセスを起動させておく必要があります (IP アドレス: 127.0.0.1、ポート: 6379)。



