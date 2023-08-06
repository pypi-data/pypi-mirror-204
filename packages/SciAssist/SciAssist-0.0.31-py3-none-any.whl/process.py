import os

from SciAssist.bin.doc2json.doc2json.grobid2json.process_pdf import process_pdf_file

from SciAssist.utils.pdf2text import get_bodytext

for (root,dirs,files) in os.walk("/home/dingyx/project/SciAssist/data/longsumm/pdf"):
    for file in files:
        pdf_file = os.path.join(root,file)
        try:
            json_file = process_pdf_file(input_file=pdf_file, temp_dir="/home/dingyx/project/SciAssist/data/longsumm/temp", output_dir="/home/dingyx/project/SciAssist/data/longsumm/temp")
            path = get_bodytext(json_file=json_file, output_dir = "/home/dingyx/project/SciAssist/data/longsumm/", suffix="")
        except:
            print("Unavailable")
