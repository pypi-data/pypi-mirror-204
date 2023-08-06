import os

import nltk
from SciAssist import BASE_CACHE_DIR
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



# root_dir = "/home/dingyx/project/SciAssist/data/FLANT5_keyword/"
# root_dir = "/home/dingyx/project/SciAssist/data/MUP_CTRLkeyword"
#
root_dir = "/home/dingyx/project/SciAssist/data/pdfs/summary_ours/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = files
    break

from nltk.stem.porter import *
stemmer = PorterStemmer()

suc = 0
total = 0
stop_words = set(stopwords.words('english'))
for i in file_list:
    if i[-4:]==".txt" and (int(i[:-4])) % 1 == 0:
        with open(os.path.join(root_dir,i),"r") as f:
            file = f.readlines()
            file = " ".join(file)
            # print(file)
            kw = file.strip().split(" => ")[0].strip()
            kw = word_tokenize(kw)
            kw = [stemmer.stem(k.strip()) for k in kw]

            text = file.strip().split(" => ")[1].strip()
            text = word_tokenize(text)
            text = [stemmer.stem(k.strip()) for k in text]
            kw = " ".join(kw)
            text = " ".join(text)

            # f = res(kw, text)[0]
            # f = word_tokenize(f)
            # kw = word_tokenize(kw)
            # print(f)
            # print(len(f))
            # rate = len(f)/len(kw)
            # suc += rate

            # print(kw)
            # print(text)
            if kw in text:
                suc+=1
            total+=1
        # for k in kw:
        #     # print(text)
        #     if k in stop_words:
        #         continue
        #     if k in text:
        #         suc+=1
        #     total+=1
print(suc, total)
print(suc/total)