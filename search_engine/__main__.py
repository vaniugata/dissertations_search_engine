import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import glob
import re
import os
import sys
from search_engine import engine
from search_engine import read_documents
from tkinter import *

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


    window = Tk()

    l_title = Label(window, text="Тема: ")
    e_title = Entry(window)
    l_university = Label(window, text="Университет: ")
    e_university = Entry(window)
    b_search = Button(window, text="Търси")

    l_name = Label(window, text="Автор: ")
    e_name = Entry(window)
    l_number = Label(window, text="Факултетен №: ")
    e_number = Entry(window)

    b_info = Button(window, text="Информация")

    complexity = IntVar()

    Radiobutton(window, text="Много сложен", variable=complexity, value=5).grid(row=3, column=0)
    Radiobutton(window, text="Сложен", variable=complexity, value=4).grid(row=3, column=1)
    Radiobutton(window, text="Нормално сложен", variable=complexity, value=3).grid(row=3, column=2)
    Radiobutton(window, text="Лесен", variable=complexity, value=2).grid(row=3, column=3)
    Radiobutton(window, text="Тривиален", variable=complexity, value=1).grid(row=3, column=4)
    Radiobutton(window, text="Всички", variable=complexity, value=0).grid(row=3, column=5)

    list_result = Listbox(window, height=10, width=100)
    sb_result = Scrollbar(window)

    temp1=("test 1", "test12", "test13")
    temp2=("test 2", "test22")
    list_a =[]
    list_a.append(temp1)
    list_a.append(temp2)

    list_result = Listbox(window, height=10, width=120)
    sb_result = Scrollbar(window)
    for item in list_a:
        list_result.insert(END, item)

    #l_directory.grid(row=0, column=0)
    #e_directory.grid(row=0, column=1, columnspan=2)
    #b_browse.grid(row=0, column=4, columnspan=2)

    l_title.grid(row=1, column=0)
    e_title.grid(row=1, column=1)
    l_university.grid(row=1, column=3)
    e_university.grid(row=1, column=4)
    b_search.grid(row=1, column=5, rowspan=2)
    b_search.bind()

    l_name.grid(row=2, column=0)
    e_name.grid(row=2, column=1)
    l_number.grid(row=2, column=3)
    e_number.grid(row=2, column=4)

    b_info.grid(row=5, column=5)

    list_result.grid(row=4, column=0, rowspan=10, columnspan=5)
    sb_result.grid(row=4, column=4, rowspan=10, sticky=E)

    list_result.configure(yscrollcommand=sb_result.set)
    sb_result.configure(command=list_result.yview)
    window.mainloop()


    # options = input("Enter search option:\n(1)[query words in files]\n(2)[query human names in file]\n")
    # while True:
    #     if options == '1':
    #         query = input('Enter your query:')
    #         query = engine.word_tokenize(query)
    #         engine.find_files_by_keywords( unique_words_all, file_names, linked_list_data, query )
    #         break
    #     elif options == '2':
    #         for doc in docs:
    #             sentences = sent_tokenize(docs[doc])
    #             engine.find_author_name(sentences)
    #             engine.find_faculty_num(sentences)
    #             engine.find_university_name(engine.tokenize_to_sentences(docs[doc]))
    #             # path = ''.join(c for c in src_dir if not c.find('*') != -1) + os.path.basename(doc)
    #             # engine.find_thesis_title(path)
    #             print('--------------------------------------------------------------------------------')
    #         break
    #     else:
    #         options = input("Invalid search option!\n Enter search option: ")