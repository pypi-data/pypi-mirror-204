from nltk.text import TextCollection
from nltk.tokenize import word_tokenize
import datasets
import pandas as pd
import os
from tqdm import tqdm




file_list = []


root_dir = "/home/yixi/project/sciassist/data/pdfs/text"
for dirpath,dirnames,files in os.walk(root_dir):
    file_l = files
    break
file_l.sort()
file_list=[]
for i in file_l:
    if i[-4:]==".txt":
        file_list.append(i)

def keyword_extraction(input_text):
    cnts = {}
    input_text = list(set(input_text))
    for i in input_text:
        tfidf = corpus.tf_idf(i,corpus)
        cnts[i]=tfidf
    cnts = sorted(cnts.items(), key=lambda d: d[1], reverse=True)
    keywords_res = cnts
    print(keywords_res)
    keyword_str = ",".join(keywords_res)
    # print(keyword_str)
    return keyword_str


# In[197]:


# ### Different setting of keyword extraction

# In[841]:

raw_datasets = datasets.load_dataset(
    "allenai/mup",
    cache_dir="/home/yixi/.cache/sciassist"
)

print("loading finished.")
file_list = raw_datasets["train"]


# summ = file_list["summary"]
summ = file_list["text"]
sents=[word_tokenize(sent) for sent in summ]

corpus=TextCollection(sents)

# scisumm = {"File": file_list}
# print(scisumm["File"])
scisumm = {"title": file_list["paper_name"], "summary":file_list["summary"], "text":summ }
scisumm = pd.DataFrame(scisumm)
tqdm.pandas(desc='progress bar')
scisumm['keyword']=scisumm["text"].progress_apply(keyword_extraction,args=())

scisumm.to_csv(os.path.join(root_dir,"test_tfidf.csv"), index=True)