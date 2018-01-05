# -----------------[OVERALL]------------------
# This py will compile all mini glossaries into a big one,
# convert the pdf as string and remove those unwanted char
# then do the counting and sorting to produce a spectrum of
# ML glossaries and frequencies
# imported files: words_counter_utils.py + ml_glossary_all.txt

from nltk.stem import WordNetLemmatizer
import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re
# my own library
from word_counter_utils import sort_from_highest


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


# PyPDF2[works with unsolved bugs, use pdfminer instead]
def pdf_to_text_pypdf2(pdf_filename):
    # Retrieved fr:
    # https://stackoverflow.com/questions/32667398/best-tool-for-text-extraction-from-pdf-in-python-3-4
    pdf_filename = pdf_filename
    pdf_file_obj = open(pdf_filename, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    page_obj = pdf_reader.getPage(1)
    # convert to text
    text = page_obj.extractText()
    return text


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
def horizontal_bar_chart(sorted_spectrum, threshold=0):
    threshold = threshold
    # take only the tuples if the frequency is greater than 'threshold'
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
            ecolor='black')
    # make the words align with the bars
    ax.set_yticks(x_pos)
    # label the words on the y-axis
    ax.set_yticklabels(x)
    # labels read from top to bottom
    ax.invert_yaxis()
    # labeling of titles
    ax.set_xlabel('Frequency of Appearance')
    ax.set_title('Machine Learning Glossary Spectrum')
    plt.show()


# this methods will split() the words down to single word den only do the comparison
def glossary_counter_method_2(glossary_filename, pdf_string, visualize=False):
    database = []
    with open(glossary_filename, 'r') as f:
        for word in f:
            database.append(word.rstrip())  # discharge the '\n'
    # create another list of '0' as int with the same length as database
    frequency = [0] * len(database)
    pdf_string_split = pdf_string.split()
    # iteration for every phrase in database
    for i in range(len(database)):
        print('Counting \'{}\'....'.format(database[i]), end='')  # progress printing
        counter = 0  # for f of each keywords
        phrase = database[i].split()
        # iteration through every word in pdf_string_split
        for j in range(len(pdf_string_split) - len(phrase) + 1):
            match_flag = 1
            # iterate thru word by word in the phrase
            for k in range(len(phrase)):
                # if encounter one unmatched this loop will break
                if pdf_string_split[j + k] == phrase[k]:
                    # do this if first and subsequent words match
                    continue
                # do the following whenever 1 unmatched detected
                match_flag = 0
                break
            counter += match_flag
        frequency[i] += counter
        print(counter)
    spectrum = dict(zip(database, frequency))  # dict
    # sort from highest frequency to lowest, returned in list of tuples
    f_sorted_spectrum = sort_from_highest(spectrum)  # list of tuples
    print('SPECTRUM: ', f_sorted_spectrum)

    # visualize
    if visualize:
        horizontal_bar_chart(sorted_spectrum=f_sorted_spectrum, threshold=0)


# do the work
# PDF Extraction as string and remove unwanted char
pdf_text = pdf_to_text_pdfminer(pdf_filename='ML_in_human_migration.pdf', char_filter=True)
# do the counting for specific phrase
glossary_counter_method_2(glossary_filename='ml_glossary_all.txt',
                          pdf_string=pdf_text,
                          visualize=True)


# wordnet_lemmatizer = WordNetLemmatizer()
# print(wordnet_lemmatizer.lemmatize(['statistics', 'models', 'players']))


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
# StatusRecords[5 Jan, 5pm]
# -> wordnet_lemmatizer cant apply directly to a string but only word by word, hence loops require
# -> it take quiet long to execute only few words
# Suggestion -> ignore this feature
