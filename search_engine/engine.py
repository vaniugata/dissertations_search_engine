from nltk.tokenize import sent_tokenize , word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import sys
import inspect
import os
from search_engine import read_documents

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

def tokenize_to_words(text):
    Stopwords = set(stopwords.words('russian'))
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]

    return finding_all_unique_words_and_freq(words)

def tokenize_to_sentences(text):
    ai_classification = sent_tokenize(text, language='russian')
    sentences = []
    for sent in ai_classification:
        new_sent = ''
        should_append = True
        for c in sent:
            if c == '\n':
                sentences.append(new_sent)
                new_sent = ''
                should_append = False
            else:
                new_sent = new_sent + c
                should_append = True
        if should_append:
            sentences.append(new_sent)
    
    return sentences
                
def format_words(words):
    i = 0
    while i < len(words):
        words[i] = ''.join( c for c in words[i] if '\\/|&()[]{}+~=@$%^*_'.find(c) == -1 )
        if words[i] == '':
            words.pop(i)
            i = i-1
        else: 
            i = i+1

def remove_symbols_from_string(text, symbols):
    return ''.join( c for c in text if symbols.find(c) == -1 )

def get_matching_chars(lhs, rhs):
    res = ''
    i = 0
    if len(lhs) > len(rhs):
        while i < len(rhs):
            if rhs[i].find(lhs[i]) != -1:
                res = res + res.join(rhs[i])
            i = i + 1
    else:
        while i < len(lhs):
            if lhs[i].find(rhs[i]) != -1:
                res = res + res.join(lhs[i])
            i = i + 1
    return res


def extract_data(docs, src_dir):
    doc_data = {}
    for doc in docs:
        print('extracting data from: {}'.format(doc))
        sentences = sent_tokenize(docs[doc])
        author_name = find_author_name(sentences)
        fac_num = find_faculty_num(sentences)
        uni_name = find_university_name(tokenize_to_sentences(docs[doc]))
        path = ''.join(c for c in src_dir if not c.find('*') != -1) + os.path.basename(doc)
        doc_info = (author_name, fac_num, uni_name)
        title = find_thesis_title(path, doc_info)
        doc_data[doc] = doc_info + (title, path)
    return doc_data

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

def find_author_name(sentences):
    for sentence in sentences:

        words = word_tokenize(sentence)
        format_words(words)
        words = pos_tag( words, lang='rus')
         
        #TODO refactor name recognition criteria
        author_keyword = False
        keywords = ['изготвил', 'съставил', 'написал', 'предал', 'автор']
        
        res = ''
        for w in words:
            for kw in keywords:
                author_keyword |= w[0].lower().find(kw) != -1 

            if author_keyword:
                if w[1] == 'S' and len(w[0]) >= 2 and w[0][0].isupper() and not w[0][1].isupper():
                    res = res + w[0] + ' '

        if res != '':
            return res[:-1]

    return 'failed to retrieve author'

def find_faculty_num(sentences):
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
                    return w[0]
    return 'failed to extract info'

def find_thesis_title(path, doc_info):
    # 0 - author_name, 1 - fac_num, 2 - uni_name, 3 - title
    #read documents
    sentences = []
    if path.find('.pdf') != -1:
        #parse pdf to html
        os.system('pdf2txt.py -o out.html -t html {}'.format(path))
        sentences = read_documents.get_file_meta_and_text('out.html')
        os.system('rm out.html')
        os.system('del out.html')    
    elif path.find('.doc') != -1:
        sentences = read_documents.read_MSword(path)

    stop_tag = '#stop#'
    keywords = ['тема', 'задача', 'задание']
    doc_info = doc_info + ('изготвил', 'съставил', 'проверил')
    title = ''
    max_font_size = 0
    extract_data = False
    for sentence in sentences:
        #Find title by keyword and stop tag
        # replace extracted data with stop tags
        for val in doc_info:
            formated_sentence = remove_symbols_from_string(sentence[0], ',.:!?\'\"\\/')
            if min_edit_dist(formated_sentence.lower(),val.lower()) <= 2 or formated_sentence.find(val) != -1:
                if(sentence[0].find(stop_tag) == -1):
                    sentences.remove(sentence)
                sentence = (sentence[0].replace(sentence[0], stop_tag), sentence[1], sentence[2], sentence[3])
        # search for keyword
        for kw in keywords:
            extract_data |= min_edit_dist(sentence[0].lower(), kw) <= 2 
        # extract title
        if extract_data:
            title = title + sentence[0]
            extract_data &= not sentence[0].find(stop_tag) != -1
        #Find title by font size
        elif sentence[1] is not None and int(sentence[1]) > max_font_size:
            max_font_size = int(sentence[1])
    
    for sentence in sentences:
        if sentence[1] is not None and int(sentence[1]) == max_font_size:
            title = title + sentence[0]
            break
    if title == '' or title == stop_tag:
        print('failed to exrtract title.')
    return title.replace(stop_tag, '')
    
def find_university_name(sentences):
    file = open('universities_names_dictionary.txt', 'r')
    lines = file.readlines()
    file.close()

    for sentence in sentences:
        sent = ''.join(c for c in sentence if c.isalnum())
        for line in lines:
            line = ''.join(c for c in line if c.isalnum())
            if line != '' and sent != '' and sent.lower() == line.lower():
                return sentence
    
    return 'failed to extract info'

#spellchecker
def min_edit_dist(word1,word2):
    len_1=len(word1)
    len_2=len(word2)
    x = [[0]*(len_2+1) for _ in range(len_1+1)]#the matrix whose last element ->edit distance
    for i in range(0,len_1+1):  
        #initialization of base case values
        x[i][0]=i
        for j in range(0,len_2+1):
            x[0][j]=j
    for i in range (1,len_1+1):
        for j in range(1,len_2+1):
            if word1[i-1]==word2[j-1]:
                x[i][j] = x[i-1][j-1]
            else :
                x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1
    return x[i][j]


def retrieve_text(word):
    path="universities_names_dictionary.txt"
    ffile=open(path,'r')
    lines=ffile.readlines()
    ffile.close()
    distance_list=[]
    res = ''
    for i in range( 0, len(lines)-1 ):
        dist=min_edit_dist(word,lines[i])
        distance_list.append(dist)
    for j in range( 0, len(lines)-1 ):
        if distance_list[j]<=5:
            res.join(lines[j] + ' ')  
    
    return res        

def search( query_data, doc_data, ui_mgr ):
# 0 - author_name, 1 - fac_num, 2 - uni_name, 3 - title
    res = []
    for data_el in doc_data:
        idx = 0
        for val in query_data:
            if val == '' or doc_data[data_el][idx] == '':
                idx = idx + 1
                continue
            elif doc_data[data_el][idx].find( val ) != -1:
                res.append(doc_data[data_el])
            idx = idx + 1

    ui_mgr.print_result(res)    

def doc_evaluation( doc, dictionary_path ):

    doc = word_tokenize(doc)
    frequency_of_words = finding_all_unique_words_and_freq(doc)

    file = open(dictionary_path, 'r')
    lines = file.readlines()
    file.close()

    dictionary = {}
    for line in lines:
        pair = tuple(line.split())
        if len(pair) > 0:
            dictionary[ pair[0] ] = int(pair[1]) 

    evaluation = 0
    passes = 0
    word_count = 0
    for w_coef in dictionary:
        for w in frequency_of_words:
            if w.lower().find(w_coef) != -1:
                evaluation = evaluation + dictionary[w_coef] * frequency_of_words[w]   
            if passes == 0:
                word_count = word_count + frequency_of_words[w] 
        passes = 1

    return evaluation + word_count