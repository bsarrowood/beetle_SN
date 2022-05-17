# Created by:       Brad Arrowood
# Created on:       2022.05.09
# Last updated:     2022.05.17
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
# https://www.programcreek.com/python/example/95887/tkinter.filedialog.askopenfilenames
# https://stackoverflow.com/questions/66663179/how-to-use-windows-file-explorer-to-select-and-return-a-directory-using-python
# https://www.programiz.com/python-programming/datetime/current-time


import itertools
from time import sleep                                # slice and dice to pull the top results from the dic
from tkinter import filedialog                  # for prompting user which files to be compared
import matplotlib.pyplot as plt                 # for graphically ploting the results
import re                                       # the regular expression snyax for finding all the words and dividing them up
import tkinter                                  # used to ask user to select each file to be compared
from datetime import date,datetime,timedelta    # used to create unique date stamp for file name
from os import system, name                     # used to pull os info for clearing the screen
from wordcloud import WordCloud                 # to convert results into a word cloud

common_words = []                               # for the common words pulled from the related file
file_common_words = 'common_words.txt'          # txt file with a list of common words to filter with
frequency = {}                                  # dic of the words and the number of instances a word is used
N_filter = 5                                    # remove any words with under this number of instances; currently not used
N_top = 100                                      # how many of the most frequent words to display
match_pattern = []                              # list of all words pulled from file
frequency_list = []                             # list of the frequency for each of the words
filtered_report = {}                            # dic of final pass for filtered, high-to-low value sorted words and frequency counts
sorted_report = {}                              # dic of sorted high-to-low value words and their frequency counts
word_report = {}                                # dic of all the words and frequency counts before filtering

def clear():
    # used to clear the text screen
    # for windows
    if name =='nt':
        _ = system('cls')
    # for linux & mac (here, os.name is 'posix')
    else:
        _ = system('clear')

def get_file(run_count):
    
    if run_count == 1:
        print('Please select the file with the newest info....')
    elif run_count == 2:
        print('Please select the file with the older info....')
    
    tkinter.Tk().withdraw()

    file_INC_data_set = filedialog.askopenfilename(filetypes= [
        ('txt files', '*.txt'),
        ('csv file', '*.csv'),
        ('json file', '*.json'),
    ])

    print('Processing....')
    match_pattern = data_pull(file_INC_data_set)
    word_report = data_count(match_pattern)
    filtered_report = data_filter(word_report)

    return filtered_report

def data_pull(file_INC_data_set):
    # this opens the data dump file and pulls the info to be processed before closing the file
    # from the info we find all the words and add them to a list
    # the completed list is then returning for sorting and filtering
    document_text = ''
    match_pattern = []
    text_string = ''

    document_text = open(file_INC_data_set, 'r', encoding="utf8")
    text_string = document_text.read().lower()
    document_text.close()
    
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
    print('Total word count:      ' + str(len(match_pattern)))
    
    return match_pattern

def data_count(match_pattern):
    # this checks each word in the list and totals up the number of times it's found
    # it then pairs each word with the frequency count into a dic
    frequency = {}
    frequency_list = []
    word_report = {}
    word = ''
    words = ''
    
    for word in match_pattern:
        count = frequency.get(word,0)
        frequency[word] = count + 1

    frequency_list = frequency.keys()
    for words in frequency_list:
        word_report[words] = frequency[words]
    
    print('Total unique words:   ', len(word_report))

    return word_report

def high_low(word_report):
    i = ''
    k = ''
    sorted_report = {}

    sorted_values = sorted(word_report.values(), reverse=True)
    for i in sorted_values:
        for k in word_report.keys():
            if word_report[k] == i:
                sorted_report[k] = word_report[k]
    
    return sorted_report

def data_filter(word_report):
    # this checks word_report for values at a specific amount or lower to remove those key:value from the dic
    # the func then sorts the dic by pulling all the keys into a list, ordering them, 
    #   then reordering the dic based off the sorted list to make the sorted dic
    # finally from the sorted dic the top specific number of results are pulled and returned
    k = ''
    w = ''
    filtered_report = {}
    words_removed = 0

    # commenting this out to keep all words to be compared between data sets
    #for k,v in list(word_report.items()):
    #    if v <= N_filter:
    #        word_report.pop(k)

    sorted_report = high_low(word_report)

    with open(file_common_words, "r") as f:
        common_words = f.readlines()
        for w in common_words:
            for k in list(sorted_report):
                if k == w.rstrip():
                    sorted_report.pop(k)
    
    words_removed = int(len(word_report)) - int(len(sorted_report))
    print('Common words removed: ', words_removed, '\n')
    
    # moving this to word cloud func
    #filtered_report = dict(itertools.islice(sorted_report.items(), N_top))

    return sorted_report

def compare_reports(filtered_report_NEW,filtered_report_OLD):
    # this func is for comparing the new and old data sets and calc their differences
    # with the calc result being added to a new dic which will be returned
    k = ''
    diff_report = {}

    for k in filtered_report_NEW:
        if k in filtered_report_OLD:
            difference = filtered_report_NEW[k] - filtered_report_OLD[k]
            diff_report[k] = difference
    
    diff_report = high_low(diff_report)

    return diff_report

def word_cloud(passed_report):
    # first we create a unique ID based on the YYYY-MM-DD to be used for the file name
    # then we set the parameters for creating the word cloud
    # next we create the word cloud from the filtered dic and, formally, output/display the resulting image
    #   we set the background color, width, height, scaling, and made plural words combined
    # finally, we changed the code to not display result but instead auto-create an image export of the results
    uniqueID_DATE = date.today() - timedelta(0)
    now = datetime.now()
    uniqueID_TIME = now.strftime('%H%M%S')
    uniqueID = str(uniqueID_DATE) + '_' + str(uniqueID_TIME)

    final_report = dict(itertools.islice(passed_report.items(), N_top))

    wc = WordCloud(background_color='white', width=1000, height=500, relative_scaling=0.5, normalize_plurals=True).generate_from_frequencies(final_report)
    plt.figure(figsize=(15,8))
    plt.imshow(wc)
    plt.axis('off')
    #plt.show()
    plt.savefig(str(uniqueID) + '_wordcloud.png', format='png')

def bar_chart():
    print('Placeholder')

def main():
    # first we prompt the user for the newest data file
    # we then run each func to process the data
    # next we prompt the user for the older data file
    # we then run each func to process the data
    # then we'll hand both processed data sets to the func to be compared
    # the returned data will be handed off to create chart graph and exported as a PNG word cloud
    clear()
    filtered_report_NEW = get_file(1)
    filtered_report_OLD = get_file(2)
    compared_report = compare_reports(filtered_report_NEW,filtered_report_OLD)
    word_cloud(compared_report)

    # this will need to be moved down further after 2 data lists have run, sorted, and filtered
    # we'll then need to compare the 2 filtered reports to check for differences
    # we can then create 2 export reports: 
    #   1) A bar chart showing which words have become more-to-less frequent
    #   2) A word cloud of the highest 10/20/50/100 uptrend in word freqency
    #word_cloud(filtered_report_NEW)
    #sleep(1)
    #word_cloud(filtered_report_OLD)


if __name__ == '__main__':
    main()
