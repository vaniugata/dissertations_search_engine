import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
import glob
import re
import os
import sys

from search_engine import engine
from search_engine import read_pdfs

if __name__ == "__main__":
    
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

    #structure data in nodes
    class Node:
        def __init__(self ,docId, freq = None):
            self.freq = freq
            self.doc = docId
            self.nextval = None
    
    class SlinkedList:
        def __init__(self ,head = None):
            self.head = head


    dict_global = {}
    src_dir = 'src/*'
    idx = 1
    files_with_index = {}


    docs = read_pdfs.read_files_from_dir(src_dir)

    #collect all unique words and index documents
    for doc in docs:
        words = tokenize_text( docs[doc] )
        dict_global.update( finding_all_unique_words_and_freq(words) )
        files_with_index[idx] = os.path.basename(doc)
        idx = idx + 1
    
    unique_words_all = set(dict_global.keys())

    linked_list_data = {}

    for word in unique_words_all:
        linked_list_data[word] = SlinkedList()
        linked_list_data[word].head = Node(1,Node)
    
    word_freq_in_doc = {}
    idx = 1

    for doc in docs:
        words = tokenize_text(docs[doc])
        word_freq_in_doc = finding_all_unique_words_and_freq(words)
        for word in word_freq_in_doc.keys():
            linked_list = linked_list_data[word].head
            while linked_list.nextval is not None:
                linked_list = linked_list.nextval
            linked_list.nextval = Node(idx ,word_freq_in_doc[word])
        idx = idx + 1


    query = input('Enter your query:')
    query = word_tokenize(query)
    engine.find_files_by_keywords( unique_words_all, files_with_index, linked_list_data, query )