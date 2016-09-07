cd ../ && virtualenv --no-site-packages --distribute -p python3 NLP100Knock && source NLP100Knock/bin/activate && pip install -r ./NLP100Knock/required_python_packages.txt
cd NLP100Knock
git checkout README.md
rm LICENSE
