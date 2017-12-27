# --------[Web Crawler 2 & 3]---------
# customized to crawl other website
# refer step by step explanation fr comments in web_glossary_crawler.py

import requests
from bs4 import BeautifulSoup


def web_crawler_2():

    url = 'http://www.datascienceglossary.org/'
    source_code = requests.get(url)
    code_in_text = source_code.text

    glossary = []

    soup = BeautifulSoup(code_in_text, 'lxml')

    for keywords in soup.find_all('dfn'):
        glossary.append(keywords.get_text())

    print('Glossary Extraction Completed !\n', glossary)
    # saving
    with open('ml_glossary_2.txt', 'w') as f:
        for words in glossary:
            f.write(words + '\n')

    print('Saving Completed !')


def web_crawler_3():
    url = 'https://developers.google.com/machine-learning/glossary/'
    source_code = requests.get(url)
    code_in_text = source_code.text

    glossary = []

    soup = BeautifulSoup(code_in_text, 'lxml')

    for keywords in soup.find_all('h2', {'class': 'hide-from-toc'}):
        glossary.append(keywords.get_text())

    print('Glossary Extraction Completed !\n', glossary)

    with open('ml_glossary_3.txt', 'w') as f:
        for words in glossary:
            f.write(words + '\n')

    print('Saving Completed !')


web_crawler_3()