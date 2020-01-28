import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
import glob
import re
import os
import sys
from search_engine import engine
from search_engine import read_pdfs

if __name__ == "__main__":

    dict_global = {}
    src_dir = 'src/*'
    idx = 0
    file_names = {}


    docs = read_pdfs.read_files_from_dir(src_dir)

    #collect all unique words and index documents
    for doc in docs:
        words = engine.tokenize_text( docs[doc] )
        dict_global.update( engine.finding_all_unique_words_and_freq(words) )
        file_names[idx] = os.path.basename(doc)
        idx = idx + 1
    
    unique_words_all = set(dict_global.keys())

    linked_list_data = {}

    for word in unique_words_all:
        linked_list_data[word] = engine.SlinkedList()
        linked_list_data[word].head = engine.Node(1,engine.Node)
    
    word_freq_in_doc = {}
    idx = 1

    for doc in docs:
        words = engine.tokenize_text(docs[doc])
        word_freq_in_doc = engine.finding_all_unique_words_and_freq(words)
        for word in word_freq_in_doc.keys():
            linked_list = linked_list_data[word].head
            while linked_list.nextval is not None:
                linked_list = linked_list.nextval
            linked_list.nextval = engine.Node(idx ,word_freq_in_doc[word])
        idx = idx + 1

    options = input("Enter search option:\n(1)[query words in files]\n(2)[query human names in file]\n")

    while True:
        if options == '1':
            query = input('Enter your query:')
            query = engine.word_tokenize(query)
            engine.find_files_by_keywords( unique_words_all, file_names, linked_list_data, query )
            break
        elif options == '2':
            for doc in docs:
                engine.find_author_name(docs[doc])
            break
        else:
            options = input("Invalid search option!\n Enter search option: ")
    
    