import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re


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


# PyPDF2
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


# Pdf Miner
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
        # remove all char inside []
        text = re.sub('[({[\])’‘,.;:]', '', text)
    # return in string
    return text


pdf_text = pdf_to_text_pdfminer(filename='ML_in_human_migration.pdf', char_filter=True)
print(pdf_text)
