from nltk.tokenize import sent_tokenize , word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import sys
import inspect
import re
from bs4 import BeautifulSoup
import os
    
#structure data in nodes
class Node:
    def __init__(self ,docId, freq = None):
        self.freq = freq
        self.doc = docId
        self.nextval = None

class SlinkedList:
    def __init__(self ,head = None):
        self.head = head

    #helper functions
def finding_all_unique_words_and_freq(words):
    words = list(words)
    words_unique = []
    word_freq = {}
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq

def tokenize_text(text):
    Stopwords = set(stopwords.words('russian'))
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]

    return finding_all_unique_words_and_freq(words)

def format_words(words):
    i = 0
    while i < len(words):
        words[i] = ''.join( c for c in words[i] if '\\/|&()[]{}+~=@$%^*_'.find(c) == -1 )
        if words[i] == '':
            words.pop(i)
            i = i-1
        else: 
            i = i+1

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
    


# query documents algorithm
def find_files_by_keywords(words, file_names, words_num_in_files, query):

    total_files = len(file_names)
    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []

    for word in (query):
        if word.lower() in words:
            zeroes_and_ones = [0] * total_files
            linkedlist = words_num_in_files[word.lower()].head
            while linkedlist.nextval is not None:
                zeroes_and_ones[linkedlist.nextval.doc - 1] = 1
                linkedlist = linkedlist.nextval
            zeroes_and_ones_of_all_words.append(zeroes_and_ones)
        else:
            print(word," not found")
            sys.exit()
        word_list = zeroes_and_ones_of_all_words[0]
        bitwise_op = [ 1 & w for w in word_list ]
        zeroes_and_ones_of_all_words.remove(word_list)
        zeroes_and_ones_of_all_words.insert(0, bitwise_op)
            
    files = []    
    print(zeroes_and_ones_of_all_words)
    lis = zeroes_and_ones_of_all_words[0]
    cnt = 0
    for index in lis:
        if index == 1:
            files.append(file_names[cnt])
        cnt = cnt+1
        
    print(files) 

def find_author_name(text):
    print('Author:')
    sentences = sent_tokenize(text)
    for sentence in sentences:

        words = word_tokenize(sentence)
        format_words(words)
        words = pos_tag( words, lang='rus')
        
        
        #TODO refactor name recognition criteria
        author_key_word = False
        key_words = ['изготвил', 'съставил', 'написал', 'предал', 'автор']

        for w in words:
            for kw in key_words:
                author_key_word |= w[0].lower().find(kw) != -1 

            if author_key_word:
                if w[1] == 'S' and len(w[0]) >= 2 and w[0][0].isupper() and not w[0][1].isupper():
                    print(w[0])

               


def find_faculty_num(text):
    print('Faculty num:', end=' ')
    sentences = sent_tokenize(text)
    for sentence in sentences:

        words = word_tokenize(sentence)
        words = pos_tag( words, lang='rus')
        
        faculty_num_key_word = False
        key_words = ['фак', 'ном', 'ф.н.', '№', '#']

        for w in words:
            for kw in key_words:
                faculty_num_key_word |= w[0].lower().find(kw) != -1 

            if faculty_num_key_word:
                if w[1] == 'NUM=ciph':  
                    print(w[0])

def find_thesis_title(path):
    if path.find('.pdf') != -1:
        #parse pdf to html
        os.system('pdf2txt.py -o out.html -t html {}'.format(path))
        sentences = get_file_meta_and_text('out.html')
        #if os is windws: os.system('del out.html')
        os.system('rm out.html')
        font_size = 0
        idx = 0
        for sent in sentences:
            if int(sent[1]) > font_size:
                font_size = int(sent[1])
                print(sent[0])
            elif sent[0].lower().find('тема') != -1 and idx < len(sentences)-1:
                print(sentences[idx + 1][0])
            idx = idx + 1
            
    elif path.find('.doc') != -1:
        print(path)