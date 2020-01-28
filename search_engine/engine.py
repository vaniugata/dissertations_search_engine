from nltk.tokenize import sent_tokenize , word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import sys
import inspect
import re
    
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
    Stopwords = set(stopwords.words('bulgarian'))
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]

    return finding_all_unique_words_and_freq(words)

def format_words(words):
    i = 0
    while i < len(words):
        words[i] = ''.join( c for c in words[i] if c.isalnum() )
        if words[i] == '':
            words.pop(i)
            i = i-1
        else: 
            i = i+1
    


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
    sentences = sent_tokenize(text)
    for sentence in sentences:

        words = word_tokenize(sentence)
        format_words(words)
        words = pos_tag( words, lang='rus')
        author_key_word = False
        key_words = ['изготвил', 'съставил', 'написал', 'предал', 'автор']

        for w in words:
            for kw in key_words:
                author_key_word |= w[0].lower().find(kw) != -1

            if author_key_word:
                if w[1] == 'S':
                    print(w)
            

        #TODO refactor name recognition criteria