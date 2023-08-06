import xml.etree.ElementTree as ET
import os
file_list = []

root_dir = "/home/yixi/project/scisumm-corpus/data/Training-Set-2019/Task2/From-ScisummNet-2019"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = dirnames
    break
filter_files=[]

def parse_rec(filename):
    file = os.path.join(root_dir,filename,"Reference_XML",filename+".xml")
    tree = ET.parse(file)  # 解析读取xml函数


    # Element.findall()查找当前元素的直接子元素中带有指定标签的元素
    # Element.find()找带有特定标签的第一个子级
    # Elemtn.text 访问元素的文本内容
    # Element.get 访问元素的属性。
    body_text = ""

    if len(tree.findall('SECTION'))>0:
        for section in tree.findall('SECTION'):
            if "Introduction" in section.get("title") or "Conclusion" in section.get("title") or "1" in section.get("title"):
                for s in section.findall("S"):
                    body_text += s.text
                    body_text += " "
    else:
        filter_files.append(filename)
    # else:
        # for s in tree.findall("S"):
        #     if s.text is not None:
        #         body_text += s.text
        #         body_text += " "
        # print(filename)

    with open(os.path.join(root_dir,filename,filename+".txt"),"w") as f:
        f.write(body_text)

    return body_text

for file in file_list:
    s = parse_rec(file)

print("Finished.")
print(filter_files)
