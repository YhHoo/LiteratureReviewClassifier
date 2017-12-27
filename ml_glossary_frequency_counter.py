import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
import re


def glossary_counter(glossary, pdf_string, visualize=False):
    database = []
    with open(glossary, 'r') as f:
        for word in f:
            database.append(word)
    # create another list of '0' with the same length as database
    frequency = np.zeros(len(database))
    # counts f of every word and store the freq to frequency of corresponding position
    for word in database:
        word_freq = pdf_string.count(word)
        frequency[database.index(word)] += word_freq

    if visualize:
        plt.plot(database, frequency)


# groups all mini glossaries of txt and save in a new txt
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


# temporary for testing the pdf miner
pdf_filename = 'journal_test.pdf'
pdf_file_obj = open(pdf_filename, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
page_obj = pdf_reader.getPage(1)
# convert to text
text = page_obj.extractText()
# remove some characters
text = re.sub('[({[\])]', '', text)
print(text)
