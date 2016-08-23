
# Ch2
wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/hightemp.txt

# Ch3
wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/jawiki-country.json.gz
gzip -d jawiki-country.json.gz

# Ch4
wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/neko.txt
mecab neko.txt | nkf -w > neko.txt.mecab

# Ch5
cabocha neko.txt > neko.txt.cabocha

# Ch6
wget http://www.cl.ecei.tohoku.ac.jp/nlp100/data/nlp.txt
