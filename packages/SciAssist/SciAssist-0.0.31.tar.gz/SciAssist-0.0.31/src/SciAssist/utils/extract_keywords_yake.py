import yake

import pandas as pd
import os
from tqdm import tqdm

file_list = []

root_dir = "/home/yixi/project/scisumm-corpus/data/Training-Set-2019/Task2/From-ScisummNet-2019/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = dirnames
    break


def keyword_extraction(input_text, kw_extractor):
    # with open(os.path.join(root_dir,input_text,input_text+".txt"),"r") as f:
    with open(os.path.join(root_dir, input_text, "summary",input_text + ".scisummnet_human.txt"), "r") as f:
        input_text = f.readlines()
        input_text= " ".join(input_text[1:])
    keywords_res = kw_extractor.extract_keywords(input_text)
    keyword_str = ",".join([kw[0] for kw in keywords_res])
    return keyword_str


# In[197]:


# ### Different setting of keyword extraction

# In[841]:


language = "en"  # 文档语言
max_ngram_size = 3  # N-grams
deduplication_thresold = 0.3  # 筛选阈值,越小关键词越少
deduplication_algo = 'seqm'
windowSize = 3
numOfKeywords = 5  # 最大数量

kw_extractor = yake.KeywordExtractor(lan=language,
                                     n=max_ngram_size,
                                     dedupLim=deduplication_thresold,
                                     dedupFunc=deduplication_algo,
                                     windowsSize=windowSize,
                                     top=numOfKeywords)



scisumm = {"File":file_list}
scisumm = pd.DataFrame(scisumm)
tqdm.pandas(desc='progress bar')
scisumm['Keyword']=scisumm["File"].progress_apply(keyword_extraction,args=(kw_extractor,))

scisumm.to_csv(os.path.join(root_dir,"scisumm_keywords10_yake_bigram_src.csv"), index=False)