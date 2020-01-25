from nltk.tokenize import sent_tokenize , word_tokenize
import sys
import inspect

# query documents algorithm
def find_files_by_keywords(words, file_names, words_num_in_files, query):

    total_files = len(file_names)
    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []

    for word in (query):
        if word.lower() in words:
            zeroes_and_ones = [0] * total_files
            linkedlist = words_num_in_files[word].head
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
    cnt = 1
    for index in lis:
        if index == 1:
            files.append(file_names[cnt])
        cnt = cnt+1
        
    print(files) 