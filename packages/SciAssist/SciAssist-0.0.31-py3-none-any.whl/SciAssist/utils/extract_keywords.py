import random

import datasets
import pandas as pd
import os
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
device = "cuda:1"
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl", max_length=1024, truncation=True)
model.to(device)


file_list = []

summ = []
# root_dir = "/home/yixi/project/sciassist/data/pdfs/text"
root_dir = "/home/yixi/project/scisumm-corpus/data/Training-Set-2019/Task2/From-ScisummNet-2019/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = dirnames
    break
# root_dir = "/home/yixi/project/sciassist/data/pdfs/text/"
# for dirpath,dirnames,files in os.walk(root_dir):
#     file_l = files
#     break
# file_l.sort()
# file_list=[]
# for i in file_l:
#     if i[-4:]==".txt":
#         file_list.append(i)


with open("/home/yixi/project/concepts.txt", "r") as f:
    phrases = f.readlines()
    phrases = [i.strip() for i in phrases]
def keyword_extraction(input_text):
    # with open(os.path.join(root_dir,input_text),"r") as f:
    with open(os.path.join(root_dir, input_text, "summary",input_text + ".scisummnet_human.txt"), "r") as f:
        input_text = f.readlines()
        input_text= " ".join(input_text[1:])
    input_text = input_text.replace("\t"," ")
    input_text = input_text.replace("\n","  ")
    keywords = []
    for j in phrases:
        if j in input_text.lower():
            keywords.append(j)
    keywords = list(set(keywords))
    if len(keywords)<1:
        return ""
    keywords = sorted(keywords, key=lambda x:len(x), reverse=True)[:10]
    keywords_reverse=sorted(keywords, key=lambda x:len(x), reverse=False)
    keywords_res = []
    for i in range(len(keywords_reverse)):
        flag=0
        for j in range(i+1,len(keywords)-1):
            if keywords_reverse[i] in keywords_reverse[j]:
                flag=1
                break
        if flag==0:
           keywords_res.append(keywords_reverse[i])

    # print(keywords_reverse)
    keywords_res = [k.strip() for k in keywords_res]
    keywords_res = [k for k in keywords_res if k!=""]


    keyword_str = ",".join(keywords_res)
    # print(keyword_str)


    return keyword_str


# In[197]:


# ### Different setting of keyword extraction

# In[841]:

# raw_datasets = datasets.load_dataset(
#     "allenai/mup",
#     cache_dir="/home/yixi/.cache/sciassist"
# )

print("loading finished.")
# file_list = raw_datasets["train"]
# file_list = raw_datasets["validation"].select(range(1000))

# summ = file_list["summary"]
scisumm = {"File": file_list}
print(file_list)
# print(scisumm["File"])
# scisumm = {"title": file_list["paper_name"], "summary":summ, "text":file_list["text"] }
scisumm = pd.DataFrame(scisumm)
tqdm.pandas(desc='progress bar')
scisumm['keyword']=scisumm["File"].progress_apply(keyword_extraction,args=())
# scisumm['keyword']=scisumm["File"].progress_apply(keyword_extraction,args=())

scisumm.to_csv(os.path.join(root_dir,"forecite.csv"), index=False)