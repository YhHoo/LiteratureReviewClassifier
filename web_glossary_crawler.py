# --------------------[Web Crawler 1]------------------------------
# This script is just to crawl all the glossary from the website of
# https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/
# to used in analyzing the pdf.

import requests
from bs4 import BeautifulSoup

# download the page source fr URL below and convert to text
url = 'https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/'
source_code = requests.get(url)
code_in_text = source_code.text

# list to store all extracted info
glossary = []

# use lxml parser to parse the code_in_text
soup = BeautifulSoup(code_in_text, 'lxml')

# get all tables tag
tables = soup.find_all('table')

# iterate through all tables tag and do:
for table in tables:
    for row in table.find_all('tr'):
        # parse only first column
        column = row.find('td')
        if column:
            for bold_text in column.find_all('strong'):
                info = bold_text.get_text()
                print(info)
                glossary.append(info.rstrip())  # remove the trailing char like \n

with open('ml_glossary_1.txt', 'w') as f:
    for word in glossary:
        f.write(word + '\n')

print('Glossary Extraction Completed !\n', glossary)




