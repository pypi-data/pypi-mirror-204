import os
import numpy as np
import requests

url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"


def res(text):

    payload = {
        "enable_google_results": "true",
        "enable_memory": False,
        "input_text": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "c7d55448-fb45-4d76-af54-2ce50bd01531"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.text

root_dir = "/home/dingyx/project/SciAssist/data/pdfs/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_l = files
    break
file_l.sort()
file_list=[]
for i in file_l:
    if i[-4:]==".txt":
        file_list.append(i)

mad = []
for i in file_list:
    file_name = os.path.join(root_dir, i)
    input_text = ""
    with open(file_name, "r") as f:
        input_text = f.readlines()
        input_text = [i.strip() for i in input_text]
        input_text = " ".join(input_text)
    for j in range(5):
        length = (j+1)*50
        prompt = f"Give a summary of the following text, which has about {length} words: "
        summ = res(prompt+input_text)
        MAD = abs(len(summ) - length)/50
        mad.append(MAD)

print(np.mean(mad))
