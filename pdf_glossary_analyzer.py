# -----------------------------[OVERALL]--------------------------------
# This py will compile all mini glossaries into a big one, called 'ml_glossary_all.txt'
# convert the pdf as string and remove those unwanted char
# then do the counting and sorting to produce a spectrum of
# ML glossaries and frequencies
# (OR)
# if given 'ml_glossary_all2.csv' which is glossary by categories, then it will first put the keywords
# into a long list as above as well. The categorization of keywords was done in pdf_clustering_machine.py
#
# imported files: words_counter_utils.py + ml_glossary_all.txt (or) ml_glossary_all2.csv
# it will then do the analysis for every pdf inside pdf_storage() and save their overall statistic
# to Table_of_glossary_frequency.csv and get ready for pdf_clustering_machine.py
# [PDF DATABASE] - Please make sure all of your pdf-s to be analyzed are downloaded by Mendeley Desktop
# saved and properly renamed at C:\Users\YH\AppData\Local\Mendeley Ltd\Mendeley Desktop\Downloaded.
# Follow the tutorial at Evernote

from nltk.stem import WordNetLemmatizer
import numpy as np
import matplotlib.pyplot as plt
# import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re
import random
import pandas as pd
from os import listdir
from os.path import isfile, join
# my own library
from word_counter_utils import sort_from_highest, ProgressBarForLoop


# this is to replace the pdf_bank()
# it will directly access all pdf inside the folder of Mendeley
# so place all papers without renaming into the mendeley then they will be accessed through here
def pdf_storage():
    # this is the path of folder where mendeley used to contains pdf with filenames
    # path_mendeley = 'C://Users//YH//AppData//Local//Mendeley Ltd//Mendeley Desktop//Downloaded//'
    path_mendeley = 'C://Users//YH//Desktop//New Reference Papers//New Reference Papers//'
    # listdir(path) will return a list of file path
    all_file_path = [(path_mendeley + f) for f in listdir(path_mendeley) if isfile(join(path_mendeley, f))]
    # list of all filename only
    all_filename = listdir(path_mendeley)

    # create a df storing the short form and pdf name
    short_pdf = ['PDF[{}]'.format(i + 1) for i in range(len(all_filename))]
    # put everything in df
    df = pd.DataFrame(data=all_filename, index=short_pdf)
    df.to_csv('LRC_citation.csv')
    return all_file_path, short_pdf


# group all ml_glossary_1, _2, _3.txt, convert to lowercase and save in a new txt
def glossary_database_accumulate():
    # extract all words from all mini glossaries
    mini_glossary = ['ml_glossary_1.txt', 'ml_glossary_2.txt', 'ml_glossary_3.txt']
    temp = []
    for files in mini_glossary:
        with open(files, 'r') as f:
            for word in f:
                # write all words in lowercase
                temp.append(word.lower())
    print('Extraction Completed !')
    # sort alphabetically
    temp.sort()
    # save all extracted to another files
    with open('ml_glossary_all.txt', 'w') as f:
        for word in temp:
            f.write(word)
    print('Saving Completed !')


# # PyPDF2[works with unsolved bugs, use pdfminer instead]
# def pdf_to_text_pypdf2(pdf_filename):
#     # Retrieved fr:
#     # https://stackoverflow.com/questions/32667398/best-tool-for-text-extraction-from-pdf-in-python-3-4
#     pdf_filename = pdf_filename
#     pdf_file_obj = open(pdf_filename, 'rb')
#     pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
#     page_obj = pdf_reader.getPage(1)
#     # convert to text
#     text = page_obj.extractText()
#     return text


# Pdf Miner that extract .pdf as string, remove all unwanted char and returned
def pdf_to_text_pdfminer(pdf_filename, char_filter=False):
    print('Converting \'{}\' to text...'.format(pdf_filename), end='')  # use end to continue printing
    pdf_filename = pdf_filename
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()  # if use ByteIO, the hex code appears in the text
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # extract text
    with open(pdf_filename, 'rb') as fp:
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
    # get text from ByteIO
    text = sio.getvalue()
    # close
    device.close()
    sio.close()
    # char filter
    if char_filter:
        # remove all char specified inside first '' of re.sub()
        # Note that use of '[]' will treat each char inside as a separate single char, e.g.
        # '[(@]' will replace '(' and '@'
        # While without the use of [] list, a string of char inside '' will be treated as entity, e.g.
        # '(@' will replace '(@' only and not single '(' and '@'
        text = re.sub('[({[\])’*‘,.;:]', '', text)
        text = re.sub('-\n', '', text)
    print('[Completed]')
    # return in string in lower case
    return text.lower()


# count the keywords of ML from the input processed string of .pdf and return a dict of {'word':freq}
# this method will directly count from entire string without splitting
def glossary_counter_method_1(glossary_filename, pdf_string, visualize=False):
    database = []
    with open(glossary_filename, 'r') as f:
        for word in f:
            database.append(word.rstrip())  # discharge the '\n'
    # create another list of '0' as int with the same length as database
    frequency = [0] * len(database)
    # counts f of every word and store the freq to frequency of corresponding position
    for word in database:
        word_freq = pdf_string.count(word)
        frequency[database.index(word)] += word_freq
    # summarize to a dict
    spectrum = dict(zip(database, frequency))
    sorted_spectrum = sort_from_highest(spectrum)
    print('ML Glossary Spectrums: ', sorted_spectrum)

    # plot a histogram
    if visualize:
        plt.plot(database, frequency, 'x')
        plt.show()
        plt.savefig(fname='spectrum.jpg')


# plot a horizontal bar chart
# the words will only be plotted on bar chart if the frequency of the word is greater than [threshold]
def horizontal_bar_chart(sorted_spectrum, threshold=0, title=None):
    threshold = threshold
    # take only the words(tuples) if the frequency is greater than 'threshold'
    sorted_spectrum_without_zero = [pair for pair in sorted_spectrum if pair[0] > threshold]
    # x is the one glossary that will appear on y-axis, while y is the freq
    y, x = zip(*sorted_spectrum_without_zero)
    x_pos = np.arange(len(x))
    plt.rcdefaults()
    fig, ax = plt.subplots()
    # create bar chart horizontal
    ax.barh(x_pos,
            y,
            align='center',
            color='green',
            ecolor='black',
            zorder=3)  # z-order controls the overlapping of the bar over the grid
    # make the words align with the bars
    ax.set_yticks(x_pos)
    # label the words on the y-axis
    ax.set_yticklabels(x)
    # labels read from top to bottom
    ax.invert_yaxis()
    # labeling of titles
    ax.set_xlabel('Frequency of Appearance')
    if title is None:
        ax.set_title('Machine Learning Glossary Spectrum')
    else:
        ax.set_title(title)
    ax.grid(zorder=0)  # ensure the grid is below the bar
    plt.show()


def save_spectrum_to_csv(sorted_spectrum, save_mode='all', title='Unknown', append=False):
    print('Saving to csv....', end='')
    # append on old file or not
    if append:
        write_mode = 'a'
    else:
        write_mode = 'w'
    # take only none zero f words
    sorted_spectrum_without_zero = [pair for pair in sorted_spectrum if pair[0] > 0]
    # open the file and write
    with open('glossary_spectrum.csv', write_mode) as f:
        # write title first
        f.write(title + '\n')
        # ---[Mode 'all' or 'random']----
        # save all non-zeros-f words
        if save_mode == 'all':
            for item in sorted_spectrum_without_zero:
                f.write('{}, {} \n'.format(item[1], item[0]))
        # save only 5 random non-zero-f words, for accuracy testing purpose
        elif save_mode == 'random':
            rand_list = [i for i in range(0, len(sorted_spectrum_without_zero), 1)]
            random.shuffle(rand_list)
            for i in rand_list[:5]:
                f.write('{}, {} \n'.format(sorted_spectrum_without_zero[i][1],
                                           sorted_spectrum_without_zero[i][0]))
    print('[Completed]')


# this methods will split() the words down to single word den only do the comparison
# [glossary_filename] -> the glossary.txt that provide all glossaries for searching
# [pdf_string] -> the pdf to be searched but ady in preprocessed by pdf_to_text_pdfminer() to string
# [visualize] -> print the bar chart with the title in [bar_chart_title]
def glossary_counter_method_2(glossary_filename, pdf_string, visualize=False,
                              bar_chart_title=None, save_csv=False):
    # setting words to count
    database = []
    # check glossary file format (.csv or .txt)
    if glossary_filename.endswith('.txt'):  # for ml_glossary+all.txt
        with open(glossary_filename, 'r') as f:
            for word in f:
                database.append(word.rstrip())  # discharge the '\n'
    elif glossary_filename.endswith('.csv'):
        # this is for glossary in the form of Categorical CSV, == ml_glossary_all2.csv
        df = pd.read_csv(glossary_filename)
        for col in df:
            temp = df[col].dropna().tolist()
            database += temp
    else:
        raise FileNotFoundError('[YH] ONLY USE (.csv) OR (.txt) AS glossary_filename')

    # modify the global variable database_len for error handling purpose
    global database_len
    database_len = len(database)

    # create another list of '0' as int with the same length as database
    frequency = [0] * len(database)
    pdf_string_split = pdf_string.split()

    # ---[LEMMATIZING]---
    # prepare for lemmatizing
    # setup progress bar for lemmatizing
    pb = ProgressBarForLoop('Lemmatizing', end=len(pdf_string_split))
    pdf_string_split_root = []
    wordnet_lemmatizer = WordNetLemmatizer()
    # convert all nouns to root word
    for word in pdf_string_split:
        pdf_string_split_root.append(wordnet_lemmatizer.lemmatize(word))
        # update prog bar
        pb.update(pdf_string_split.index(word))
    pb.destroy()

    # ---[COUNTING]--
    # setup progress bar for converting
    pb = ProgressBarForLoop('Counting', end=len(database))
    # iteration for every phrase in database
    for i in range(len(database)):
        counter = 0  # for f of each keywords
        phrase = database[i].split()
        # iteration through every word in pdf_string_split
        for j in range(len(pdf_string_split_root) - len(phrase) + 1):
            match_flag = 1
            # iterate thru word by word in the phrase
            for k in range(len(phrase)):
                # if encounter one unmatched this loop will break
                if pdf_string_split_root[j + k] == phrase[k]:
                    # do this if first and subsequent words match
                    continue
                # do the following whenever 1 unmatched detected
                match_flag = 0
                break
            counter += match_flag
        frequency[i] += counter
        # progress bar update
        pb.update(i)
    pb.destroy()
    # zip 2 list into a dict
    spectrum = dict(zip(database, frequency))  # dict
    # sort from highest frequency to lowest, returned in list of tuples
    f_sorted_spectrum = sort_from_highest(spectrum)  # list of tuples
    print('SORTED SPECTRUM: ', f_sorted_spectrum[:5])

    # visualize [configure the Bar Chart & Saving setting HERE]
    if visualize:
        horizontal_bar_chart(sorted_spectrum=f_sorted_spectrum,
                             threshold=0,
                             title=bar_chart_title)

    # saving the dict to csv [configure the saving method HERE]
    if save_csv:
        save_spectrum_to_csv(sorted_spectrum=f_sorted_spectrum,
                             save_mode='all',
                             title=bar_chart_title,
                             append=True)  # only when u wan to analyze several pdf tgt
    # return
    return database, frequency, len(pdf_string_split)


# --------------------------------[DO THE WORK]--------------------------------
# this is to prevent the code fr here onwards is executed when
# this file is imported as a module
if __name__ == '__main__':
    # this pass all the PDF needed to analyze
    pdf_full_path, short_of_pdf = pdf_storage()
    frequency_list_of_all = []
    database_len = 89  # IMPORTANT !! Please Make sure tis no always equal to no. of glossary  !!!!
    for pdf in pdf_full_path[50:60]:
        print('[{}/{}]'.format(pdf_full_path.index(pdf) + 1, len(pdf_full_path)))
        # this error handling is to prevent the program terminate when one file out of many failed to be opened.
        try:
            # PDF Extraction as string and remove unwanted char
            pdf_text = pdf_to_text_pdfminer(pdf_filename=pdf,
                                            char_filter=True)
            # do the counting for specific phrase
            keyword_list, frequency_list, pdf_full_len = \
                glossary_counter_method_2(glossary_filename='ml_glossary_all2.csv',
                                          pdf_string=pdf_text,
                                          visualize=False,
                                          bar_chart_title=pdf,
                                          save_csv=False)
            # append all f list in to a bigger list, b4 that, NORMALIZE each of the f respect to own pdf total len
            frequency_list_of_all.append([int(round(f / pdf_full_len * 10000)) for f in frequency_list])
            print('Ext: {}, Int: {}'.format(len(frequency_list_of_all),
                                            len(frequency_list_of_all[len(frequency_list_of_all) - 1])))
        except (PDFSyntaxError, OSError):
            print('[ERROR: CANT OPEN FILE !]')
            frequency_list_of_all.append(['x'] * database_len)
            print('Ext: {}, Int: {}'.format(len(frequency_list_of_all),
                                            len(frequency_list_of_all[len(frequency_list_of_all) - 1])))
            continue
        except TypeError:
            print('[ERROR: UNSUPPORTED OPERAND]')
            frequency_list_of_all.append(['x'] * database_len)
            print('Ext: {}, Int: {}'.format(len(frequency_list_of_all),
                                            len(frequency_list_of_all[len(frequency_list_of_all) - 1])))
            continue
    # create a data frame to contain all of the data, gt ready for saving to csv in a format suitable for clustering
    data = np.array(frequency_list_of_all)
    table = pd.DataFrame(data=data.T, index=keyword_list, columns=short_of_pdf[50:60])
    # save to csv
    table.to_csv('Table_of_glossary_frequency.csv')
    print('Table_of_glossary_frequency.csv....[UPDATED]')


# -------------------------------[LOG RECORDS]---------------------------------
# StatusRecords[2 Jan, 6pm]
# -> the 'r' will be counted as 2 from 'rigorous' which supposed to be 0.
# -> 'model' also counted by 'mode'
# Suggestion -> need to split() the string into single words only do the '==' counting
#
# StatusRecords[3 Jan, 5pm]
# -> successfully added glossary_counter_method_2() that split the words first before counting
# -> e.g. 'r' is no longer counted from 'right'
# Suggestion -> add the root word converter so that statistic & statistics treated as same thing
#
# StatusRecords[5 Jan, 1pm]
# -> wordnet_lemmatizer cant apply directly to a string but only word by word, hence loops require
# -> it take quiet long to execute only few words
# Suggestion -> ignore this feature
# -> i did a accuracy checking by comparing the acrobat search result with my result.
#    and i realize words in graphs appear in pdf also counted like 'ann' used as labels
# -> the hyphenated words are successfully counted, tested out 4 words and the accuracy is 100%
#
# ACCURACY TESTING[5 Jan, 3pm]
# -> choose 5 pdf, manually counts the FIRST FIVE words that appear on the spectrum, then, COMPARE
# -> 99% accuracy except the words with like mode, modes are not counted as same thing
#
# StatusRecords[8 Jan, 2pm]
# -> using nltk.lemmatizer to solve plural nouns, like 'statistics' -> 'statistic'
#
# StatusRecords[11 Jan, 11am]
# -> adding dataframe bfore heatmap
#
# StatusRecords[22 Jan]
# -> realize that quiet a number of terms in ml_glossary_all.txt like 'model', 'correlation' e.t.c are too
#    common already, hence it will be useless to include them as features
# -> manually design the ml_glossary_all2.txt based on the mindmap from
#    https://machinelearningmastery.com/a-tour-of-machine-learning-algorithms/
#
# StatusRecords[26 Jan]
# -> lemmatize the glossary also bfore counting !! [replace with manual lemmatize 29 Jan]
#
# StatusRecords[29 Jan]
# -> percentage table looks good, but recommendation will be to stop counting after 'reference' keywords so
#    the counting is not affected by the references in a paper.
# -> Recommend add NRW checker to check for existance of some words like NRW, leakage and so on. use oly those
#    hit pdf to generate the connection.


