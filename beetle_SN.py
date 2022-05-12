# Created by:       Brad Arrowood
# Created on:       2022.05.09
# Last updated:     2022.05.12
# Script name:      beetle_SN.py
# Description:      script to return top 20 for word frequency count of a file, less common words
#
# References:
# https://en.wikipedia.org/wiki/Most_common_words_in_English
# https://code.tutsplus.com/tutorials/counting-word-frequency-in-a-file-using-python--cms-25965
# https://stackoverflow.com/questions/20510768/count-frequency-of-words-in-a-list-and-sort-by-frequency
# https://stackoverflow.com/questions/20304824/sort-dict-by-highest-value


import itertools
import re
import string
from os import system, name

common_words = []                           # for the common words pulled from the related file
file_common_words = 'common_words.txt'      # txt file with a list of common words to filter with
file_INC_data_dump = 'data_dump.txt'        # txt file of the INC tickets to search through
frequency = {}                              # for the number of instances a word is used
N_filter = 5                                # remove any words with under this number of instances
N_top = 20                                  # how many of the most frequent words to display
sorted_report = {}                          # to have a high-to-low value sorted dic
temp_report = {}                            # a pass thru dic from one func to another
word_report = {}                            


def clear():
    # for windows
    if name =='nt':
        _ = system('cls')
    # for linux & mac (here, os.name is 'posix')
    else:
        _ = system('clear')

def data_pull():
    # this opens the data dump file and pulls the info to be processed before closing the file
    # from the info we find all the words and add them to a list
    # the completed list is then returning for sorting and filtering
    document_text = open(file_INC_data_dump, 'r', encoding="utf8")
    text_string = document_text.read().lower()
    document_text.close()

    match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
    
    return match_pattern

def data_count(match_pattern):
    # this checks each word in the list and totals up the number of times it's found
    # it then pairs each word with the frequency count into a dic
    for word in match_pattern:
        count = frequency.get(word,0)
        frequency[word] = count + 1
        
    frequency_list = frequency.keys()
    for words in frequency_list:
        word_report[words] = frequency[words]
    
    return word_report

def data_filter(word_report):
    # this checks temp_report for values 5 or higher to then add the key:value to a new dic
    for k,v in list(word_report.items()):
        if v <= N_filter:
            word_report.pop(k)

    sorted_values = sorted(word_report.values(), reverse=True)
    for i in sorted_values:
        for k in word_report.keys():
            if word_report[k] == i:
                sorted_report[k] = word_report[k]

    with open(file_common_words, "r") as f:
        common_words = f.readlines()
        for w in common_words:
            for k in list(sorted_report):
                if k == w.rstrip():
                    sorted_report.pop(k)
#            print(w.rstrip())

    return sorted_report



clear()
match_pattern = data_pull()
word_report = data_count(match_pattern)
sorted_report = data_filter(word_report)

out = dict(itertools.islice(sorted_report.items(), N_top))
for i in out:
    print(i,out[i])
