# -----------------[OVERALL]------------------
# This py will compile all mini glossaries into a big one,
# convert the pdf as string and remove those unwanted char
# then do the counting and sorting to produce a spectrum of
# ML glossaries and frequencies
# imported files: words_frequency_counter.py + ml_glossary_all.txt

import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re
import words_frequency_counter as wfc


# group all ml_glossary_1, _2, _3.txt and save in a new txt
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


# PyPDF2[not really works]
def pdf_to_text_pypdf2(filename):
    # Retrieved fr:
    # https://stackoverflow.com/questions/32667398/best-tool-for-text-extraction-from-pdf-in-python-3-4
    pdf_filename = filename
    pdf_file_obj = open(pdf_filename, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    page_obj = pdf_reader.getPage(1)
    # convert to text
    text = page_obj.extractText()
    return text


# Pdf Miner that extract .pdf as string, remove all unwanted char and returned
def pdf_to_text_pdfminer(filename, char_filter=False):
    pdf_filename = filename
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
    # return in string
    return text


# count the keywords of ML from the input processed string of .pdf and return a dict of {'word':freq}
def glossary_counter(glossary, pdf_string, visualize=False):
    database = []
    with open(glossary, 'r') as f:
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
    sorted_spectrum = wfc.sort_from_highest(spectrum)
    print('ML Glossary Spectrums: ', sorted_spectrum)
    # plot a histogram
    if visualize:
        plt.plot(database, frequency, 'x')
        plt.show()
        plt.savefig(fname='spectrum.jpg')


# do the work
# pdf_text = pdf_to_text_pdfminer(filename='ML_in_human_migration.pdf', char_filter=True)
# glossary_counter('ml_glossary_all.txt', pdf_string=pdf_text, visualize=False)


# control string for debugging
s1 = 'ANN ANN bayesian statistics is the bayesian statistics and convergence, ' \
     'hence convergence thus discrete variable activation function hence activation function bla bla sjd'
s_split = s1.split()  # list
print(s_split)
phrase_len = 2
counter = 0
for i in range(len(s_split) - phrase_len + 1):
    if s_split[i] == 'activation':
        if s_split[i+1] == 'function':
            counter += 1
print(counter)







# StatusRecords[2 Jan, 6pm]
# -> the 'r' will be counted as 2 from 'rigorous' which supposed to be 0.
# -> 'model' also counted by 'mode'
# Suggestion -> need to split() the string into single words only do the '==' counting
