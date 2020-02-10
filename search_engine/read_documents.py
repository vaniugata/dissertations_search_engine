#!/usr/bin/env python3

from docx import Document 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import glob
import os
from bs4 import BeautifulSoup
import re
from nltk.tokenize import sent_tokenize

def read_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    file = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 2
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(file, pagenos, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()
    return text

def get_file_meta_and_text(path):
    # credits to akash karothiya: 
    # https://stackoverflow.com/questions/39012739/need-to-extract-all-the-font-sizes-and-the-text-using-beautifulsoup/39015419#39015419
    # open the html file
    htmlData = open(path, 'r', encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(htmlData, features='lxml')

    font_spans = [ data for data in soup.select('span') if 'font-size' in str(data) ]
    output = []
    for i in font_spans:
        tup = ()
        # extract fonts-size
        fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(i.get('style'))).group(2)
        # extract into font-family and font-style
        fonts_family = re.search(r'(?is)(font-family:)(.*?)(;)',str(i.get('style'))).group(2)
        # split fonts-type and fonts-style
        try:
            fonts_type = fonts_family.strip().split(',')[0]
            fonts_style = fonts_family.strip().split(',')[1]
        except IndexError:
            fonts_type = fonts_family.strip()
            fonts_style = None
        tup = (str(i.text).strip(),fonts_size.strip(),fonts_type, fonts_style)
        output.append(tup)
    return output

def read_MSword(path):
    file = open(path, 'rb')
    doc = Document(file)
    file.close()

    result = []
    br_count = 0
    for p in doc.paragraphs:
        sentences = sent_tokenize(p.text)
        for sentence in sentences:
            result.append((sentence, p.style.font.size, p.style.font.name, p.paragraph_format.alignment))
        for run in p.runs:
            if 'lastRenderedPageBreak' in run._element.xml or 'w:br' in run._element.xml and 'type="page"' in run._element.xml:
                br_count = br_count + 1
        # if br_count > 3:
        #     break

    return result

    
def read_files_from_dir(path):
    docs = {}
    for file_path in glob.glob(path):
        print( 'reading doc: {}'.format(file_path) )
        if file_path.find('.pdf') != -1:
            docs[os.path.basename(file_path)] = read_pdf(file_path)
        elif file_path.find('.docx') != -1:
            doc = read_MSword(file_path)
            text = ''.join(sentence[0] for sentence in doc)
            docs[os.path.basename(file_path)] = text
        else:
            print('Error! Opening file:{} -> Failed!\n Reason: Unsupported file format')
    
    return docs
     

    

