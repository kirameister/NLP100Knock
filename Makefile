
target_files = hightemp.txt jawiki-country.json neko.txt neko.txt.mecab neko.txt.cabocha nlp.txt

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
	cabocha neko.txt > neko.txt.cabocha

# Ch6
nlp.txt:
	wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/nlp.txt


temporary_files = col1.txt col2.txt

clean:
	$(RM) $(temporary_files) split*

clean_all:
	$(RM) $(target_files) $(temporary_files)


