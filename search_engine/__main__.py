import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import glob
import re
import os
import sys
from search_engine import engine
from search_engine import read_documents

if __name__ == "__main__":

    dict_global = {}
    src_dir = 'src/*'
    idx = 0
    file_names = {}


    docs = read_documents.read_files_from_dir(src_dir)

    #collect all unique words and index documents
    for doc in docs:
        words = engine.tokenize_to_words( docs[doc] )
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
        words = engine.tokenize_to_words(docs[doc])
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
                sentences = sent_tokenize(docs[doc])
                engine.find_author_name(sentences)
                engine.find_faculty_num(sentences)
                engine.find_university_name(engine.tokenize_to_sentences(docs[doc]))
                # path = ''.join(c for c in src_dir if not c.find('*') != -1) + os.path.basename(doc)
                # engine.find_thesis_title(path)
                print('--------------------------------------------------------------------------------')
            break
        else:
            options = input("Invalid search option!\n Enter search option: ")