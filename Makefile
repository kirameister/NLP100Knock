
target_files = hightemp.txt jawiki-country.json neko.txt neko.txt.mecab neko.txt.cabocha nlp.txt artist.json rt-polaritydata.README.1.0.txt enwiki-20150112-400-r10-105752.txt enwiki-20150112-400-r10-105752.txt.bz2 stanford-corenlp-full-2015-12-09.zip rt-polaritydata.tar.gz enwiki-20150112-400-r100-10576.txt wordsim353.zip

all: $(target_files)


# Ch2
hightemp.txt: 
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/hightemp.txt

# Ch3
jawiki-country.json:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/jawiki-country.json.gz
	gzip -d jawiki-country.json.gz

# Ch4
neko.txt:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/neko.txt
neko.txt.mecab: neko.txt
	mecab neko.txt | nkf -w > neko.txt.mecab

# Ch5
neko.txt.cabocha: neko.txt
	cabocha -f1 neko.txt > neko.txt.cabocha

# Ch6
nlp.txt:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/nlp.txt
stanford-corenlp-full-2015-12-09.zip:
	wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-12-09.zip
	unzip stanford-corenlp-full-2015-12-09.zip

# Ch7
artist.json: 
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/artist.json.gz
	gzip -d artist.json.gz

# Ch8
rt-polaritydata.tar.gz:
	wget http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz
	tar -xvzf rt-polaritydata.tar.gz

# Ch9 (and Ch10)
enwiki-20150112-400-r10-105752.txt.bz2:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/enwiki-20150112-400-r10-105752.txt.bz2
enwiki-20150112-400-r10-105752.txt: enwiki-20150112-400-r10-105752.txt.bz2
	bzip2 -d enwiki-20150112-400-r10-105752.txt.bz2
enwiki-20150112-400-r100-10576.txt.bz2: 
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/enwiki-20150112-400-r100-10576.txt.bz2
enwiki-20150112-400-r100-10576.txt: enwiki-20150112-400-r100-10576.txt.bz2
	bzip2 -d enwiki-20150112-400-r100-10576.txt.bz2

source-archive.zip:
	wget https://storage.googleapis.com/google-code-archive-source/v2/code.google.com/word2vec/source-archive.zip
	unzip source-archive.zip
questions-words.txt: source-archive.zip
	cp word2vec/trunk/questions-words.txt ./
wordsim353.zip:
	wget http://www.cs.technion.ac.il/~gabr/resources/data/wordsim353/wordsim353.zip
	unzip wordsim353.zip


temporary_files = col1.txt col2.txt

clean:
	$(RM) $(temporary_files) split* knock44_output.jpeg

clean_all:
	$(RM) $(target_files) $(temporary_files) split* knock44_output.jpeg


