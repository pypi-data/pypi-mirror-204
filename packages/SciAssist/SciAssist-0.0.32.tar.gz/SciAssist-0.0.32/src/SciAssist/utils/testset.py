import csv
import pandas as pd

ACL = {}
kw = []
text = []
id = []
summ_ours = []
summ_flant5 = []
# scisumm = {"title": file_list["paper_name"], "summary":summ, "text":file_list["text"] }
scisumm = pd.DataFrame(ACL)

with open("/home/dingyx/project/SciAssist/data/pdfs/test.csv", 'r', newline='', encoding='ISO-8859-1') as f:
    rows = csv.reader(f)
    # Get Column names
    keys = next(rows)
    # Add values by column
    for row in rows:
        kws = row[2].split(",")

        kws = kws[0]

        with open("/home/dingyx/project/SciAssist/data/pdfs/summary_ours/" + row[0] + ".txt", "r") as f:
            file = f.readlines()
            file = " ".join(file)
            k = file.strip().split(" => ")[0].strip()
            s_ours = file.strip().split(" => ")[1].strip()
            # s_ours = file.strip()
            summ_ours.append(s_ours)

        with open("/home/dingyx/project/SciAssist/data/pdfs/summary_flant5/" + row[0] + ".txt", "r") as f:
            file = f.readlines()
            file = " ".join(file)
            k = file.strip().split(" => ")[0].strip()
            s_flant5 = file.strip().split(" => ")[1].strip()
            summ_flant5.append(s_flant5)


        kw.append(kws)
        id.append(row[1][:-9])

scisumm["Keyword"] = kw
scisumm["id"] = id
scisumm["System 1"] = summ_ours
scisumm["System 2"] = summ_flant5
scisumm.to_csv("/home/dingyx/project/SciAssist/data/pdfs/human-evaluation-repeat5.csv", index=False)
