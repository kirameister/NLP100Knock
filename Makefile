
target_files = hightemp.txt jawiki-country.json neko.txt neko.txt.mecab neko.txt.cabocha nlp.txt artist.json rt-polaritydata.README.1.0.txt enwiki-20150112-400-r10-105752.txt enwiki-20150112-400-r10-105752.txt.bz2

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

# Ch7
artist.json: 
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/artist.json.gz
	gzip -d artist.json.gz

# Ch8
rt-polaritydata.README.1.0.txt:
	wget http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.README.1.0.txt

# Ch9
enwiki-20150112-400-r10-105752.txt.bz2:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/enwiki-20150112-400-r10-105752.txt.bz2
enwiki-20150112-400-r10-105752.txt: enwiki-20150112-400-r10-105752.txt.bz2
	bzip2 -d enwiki-20150112-400-r10-105752.txt.bz2

temporary_files = col1.txt col2.txt

clean:
	$(RM) $(temporary_files) split* knock44_output.jpeg

clean_all:
	$(RM) $(target_files) $(temporary_files) split* knock44_output.jpeg


