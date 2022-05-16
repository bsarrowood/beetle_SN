# Created by:       Brad Arrowood
# Created on:       2022.05.09
# Last updated:     2022.05.16
# Script name:      beetle_SN.py
# Description:      script to return top 50 for word frequency count of a file, less common words
#
# References:
# https://en.wikipedia.org/wiki/Most_common_words_in_English
# https://code.tutsplus.com/tutorials/counting-word-frequency-in-a-file-using-python--cms-25965
# https://stackoverflow.com/questions/20510768/count-frequency-of-words-in-a-list-and-sort-by-frequency
# https://stackoverflow.com/questions/20304824/sort-dict-by-highest-value
# https://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
# https://stackoverflow.com/questions/62116101/no-output-on-the-screen-word-cloud-with-matplotlib
# https://predictivehacks.com/?all-tips=how-to-create-word-clouds-from-dictionaries
# https://www.datacamp.com/tutorial/wordcloud-python

import itertools                                # slice and dice to pull the top results from the dic
import matplotlib.pyplot as plt                 # for graphically ploting the results
import re                                       # the regular expression snyax for finding all the words and dividing them up
from wordcloud import WordCloud                 # to convert results into a word cloud

common_words = []                               # for the common words pulled from the related file
file_common_words = 'common_words.txt'          # txt file with a list of common words to filter with
file_INC_data_dump = 'data_dump.txt'            # txt file of the INC tickets to search through
frequency = {}                                  # for the number of instances a word is used
N_filter = 5                                    # remove any words with under this number of instances
N_top = 50                                      # how many of the most frequent words to display
sorted_report = {}                              # dic of filtered and high-to-low value sorted words and frequency counts
word_report = {}                                # dic of all the words and frequency counts before filtering


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
    # this checks word_report for values at a specific amount or lower to remove those key:value from the dic
    # the func then sorts the dic by pulling all the keys into a list, ordering them, 
    #   then reordering the dic based off the sorted list to make the sorted dic
    # finally from the sorted dic the top specific number of results are pulled and returned
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
    
    filtered_report = dict(itertools.islice(sorted_report.items(), N_top))

    return filtered_report

def word_cloud(filtered_report):
    # here we are setting the parameters for creating the word cloud
    # we then create the word cloud from the filtered dic and output/display the resulting image
    # we can change this to auto-create an image export of the results if wanted at a later time
    wc = WordCloud(background_color='white', width=1000, height=500, relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(filtered_report)
    plt.figure(figsize=(15,8))
    plt.imshow(wc)
    plt.axis('off')
    #plt.show()
    plt.savefig('figure_1.png', format='png')


match_pattern = data_pull()
word_report = data_count(match_pattern)
filtered_report = data_filter(word_report)

# was used for printing each result and frequency count line by line
#for i in filtered_report:
#    print(i,filtered_report[i])

word_cloud(filtered_report)
