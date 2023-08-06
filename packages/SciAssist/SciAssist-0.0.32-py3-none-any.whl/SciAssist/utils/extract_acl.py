import os

from SciAssist.utils.pdf2text import get_bodytext, get_text_by_section, get_IC

from SciAssist.bin.doc2json.doc2json.grobid2json.process_pdf import process_pdf_file

root_dir = "/home/yixi/project/sciassist/data/pdfs/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = files
    break
file_list.sort()
for i in file_list:
    if i[-3:]!="pdf":
        continue
    filename=os.path.join(root_dir,i)

    json_file = process_pdf_file(input_file=filename)
    # Extract bodytext from pdf and save them in TEXT format.
    text_file = get_IC(json_file=json_file, output_dir="/home/yixi/project/sciassist/data/pdfs/text")