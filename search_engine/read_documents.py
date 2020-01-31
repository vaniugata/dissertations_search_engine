#!/usr/bin/env python3

from docx import Document 

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import glob
import os

def read_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    file = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 3
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()
    return text

def read_MSword(path):
    file = open(path, 'rb')
    doc = Document(file)
    file.close()
    text = ''.join(p.text for p in doc.paragraphs)
    return text
    
def read_files_from_dir(path):
    docs = {}
    for file_path in glob.glob(path):
        print( 'reading doc: {}'.format(file_path) )
        if file_path.find('.pdf') != -1:
            docs[os.path.basename(file_path)] = read_pdf(file_path)
        elif file_path.find('.docx') != -1:
            docs[os.path.basename(file_path)] = read_MSword(file_path)
        else:
            print('Error! Opening file:{} -> Failed!\n Reason: Unsupported file format')
    
    return docs
     

    

