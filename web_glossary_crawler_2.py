import requests
from bs4 import BeautifulSoup

# refer step by step explanation fr comments in web_glossary_crawler.py
url = 'http://www.datascienceglossary.org/'
source_code = requests.get(url)
code_in_text = source_code.text

glossary = []

soup = BeautifulSoup(code_in_text, 'lxml')

for keywords in soup.find_all('dfn'):
    glossary.append(keywords.get_text())

print('Glossary Extraction Completed !\n', glossary)

with open('ml_glossary_2.txt', 'w') as f:
    for words in glossary:
        f.write(words + '\n')

print('Saving Completed !')


