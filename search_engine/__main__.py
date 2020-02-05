import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import glob
import re
import os
import sys
from search_engine import engine
from search_engine import read_documents
from search_engine import UI

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

    # extract data
    doc_data = engine.extract_data(docs, src_dir)

    ui_mgr = UI.UIMgr()
    ui_mgr.init()

    search_callback = lambda event : engine.search( ( ui_mgr.e_name.get(), ui_mgr.e_number.get(), ui_mgr.e_university.get(), ui_mgr.e_title.get() ), doc_data, ui_mgr)
    ui_mgr.b_search.bind('<Button-1>', search_callback)
    
    ui_mgr.window.mainloop()