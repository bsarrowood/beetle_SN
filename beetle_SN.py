# Created by:       Brad Arrowood
# Created on:       2022.05.09
# Last updated:     2022.05.18
# Script name:      beetle_SN.py
# Description:      script to return top 500 for word frequency count of a file, less common words
#
# Libraries Req.:   matplotlib
#                   wordcloud
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


import itertools                                # slice and dice to pull the top results from the dic
from time import sleep                          # used to add a pause
from tkinter import filedialog                  # for prompting user which files to be compared
import matplotlib.pyplot as plt                 # for graphically ploting the results
import re                                       # the regular expression snyax for finding all the words and dividing them up
import tkinter                                  # used to ask user to select each file to be compared
from datetime import date,datetime,timedelta    # used to create unique date stamp for file name
from os import system, name, path               # used to pull os info for clearing the screen and checking path
from wordcloud import WordCloud                 # to convert results into a word cloud

common_words = []                               # for the common words pulled from the related file
file_common_words = 'common_words.txt'          # txt file with a list of common words to filter with
frequency = {}                                  # dic of the words and the number of instances a word is used
N_filter = 0                                    # remove any words with under this number of instances; currently not used
N_top = 500                                     # how many of the most frequent words to display
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

def get_file():
    
    run_count = 1
    
    while run_count < 3:
        if run_count == 1:
            print('Please select the file with the newest data set....')
            
            tkinter.Tk().withdraw()

            file_INC_data_set_NEW = filedialog.askopenfilename(filetypes= [
                ('txt files', '*.txt'),
                ('csv file', '*.csv'),
                ('json file', '*.json'),
            ])
            run_count = run_count + 1
        elif run_count == 2:
            print('Please select the file with the older data set....')

            tkinter.Tk().withdraw()

            file_INC_data_set_OLD = filedialog.askopenfilename(filetypes= [
                ('txt files', '*.txt'),
                ('csv file', '*.csv'),
                ('json file', '*.json'),
            ])
            run_count = run_count + 1

    print('Processing each data set....')
    match_pattern_NEW = data_pull(file_INC_data_set_NEW)
    word_report_NEW = data_count(match_pattern_NEW)
    filtered_report_NEW = data_filter(word_report_NEW)

    match_pattern_OLD = data_pull(file_INC_data_set_OLD)
    word_report_OLD = data_count(match_pattern_OLD)
    filtered_report_OLD = data_filter(word_report_OLD)

    return filtered_report_NEW, filtered_report_OLD

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
    #print('Total word count:      ' + str(len(match_pattern)))
    
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
    
    #print('Total unique words:   ', len(word_report))

    return word_report

def high_low(word_report):
    # pulled this to be a func since using it twice in the script
    # sorts a dic from high  to low based on the values
    # then returns the results
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
    # the func sorts the dic by pulling all the keys into a list, ordering them, 
    #   then reordering the dic based off the sorted list to make the sorted dic
    # finally from the sorted dic the top specific number of results are pulled and returned
    k = ''
    w = ''

    sorted_report = high_low(word_report)

    with open(file_common_words, "r") as f:
        common_words = f.readlines()
        for w in common_words:
            for k in list(sorted_report):
                if k == w.rstrip():
                    sorted_report.pop(k)
    
    return sorted_report

def compare_reports(filtered_report_NEW,filtered_report_OLD):
    # this func is for comparing the new and old data sets and calc their differences
    #   with the calc result being added to a new dic 
    # it then checks for all values equal to or below 0 to remove those key:value from the dic
    # the reduced dic is then returned
    
    k = ''
    v = ''
    diff_report = {}

    print('Comparing data sets....')
    for k in filtered_report_NEW:
        if k in filtered_report_OLD:
            difference = filtered_report_NEW[k] - filtered_report_OLD[k]
            diff_report[k] = difference
    
    diff_report = high_low(diff_report)

    for k,v in list(diff_report.items()):
        if v <= N_filter:
            diff_report.pop(k)

    return diff_report

def create_uniqueID():
    uniqueID_DATE = date.today() - timedelta(0)
    now = datetime.now()
    uniqueID_TIME = now.strftime('%H%M%S')
    uniqueID = str(uniqueID_DATE) + '_' + str(uniqueID_TIME)

    return uniqueID

def word_cloud(passed_report):
    # first we create a unique ID based on the YYYY-MM-DD to be used for the file name
    # then we set the parameters for creating the word cloud
    # next we create the word cloud from the filtered dic and, formally, output/display the resulting image
    #   we set the background color, width, height, scaling, and made plural words combined
    # finally, we changed the code to not display result but instead auto-create an image export of the results

    uniqueID = create_uniqueID()    
    final_report = dict(itertools.islice(passed_report.items(), N_top))

    print('Exporting word cloud image....')
    wc = WordCloud(background_color='white', width=1000, height=500, relative_scaling=0.5, normalize_plurals=True).generate_from_frequencies(final_report)
    plt.figure(figsize=(15,8))
    plt.imshow(wc)
    plt.axis('off')
    #plt.show()
    plt.savefig(str(uniqueID) + '_wordcloud.png', format='png')

def bar_chart(passed_report):
    uniqueID = create_uniqueID()
    print('Creating bar chart image....')

    final_report = dict(itertools.islice(passed_report.items(), N_top))
    keys = final_report.keys()
    values = final_report.values()

    plt.figure(figsize=(50,30))
    plt.bar(keys,values)
    #fig = plt.figure(figsize=(500,200))
    #fig.subplots_adjust(bottom=0.500)
    plt.axis('on')
    plt.xticks(rotation = 85)
    

    plt.tight_layout()
    plt.savefig(str(uniqueID) + '_bar_chart.png', format='png')
    #plt.show()

def main():
    # first we prompt the user for the newest data file
    # we then run each func to process the data
    # next we prompt the user for the older data file
    # we then run each func to process the data
    # then we'll hand both processed data sets to the func to be compared
    # the returned data will be handed off to create chart graph and exported as a PNG word cloud
    clear()
    filtered_report_NEW,filtered_report_OLD = get_file()
    compared_report = compare_reports(filtered_report_NEW,filtered_report_OLD)
    bar_chart(compared_report)
    sleep(1)
    word_cloud(compared_report)


if __name__ == '__main__':
    main()
