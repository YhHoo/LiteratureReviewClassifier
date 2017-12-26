import requests
from bs4 import BeautifulSoup

url = 'https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/'
source_code = requests.get(url)
code_in_text = source_code.text

# crawling setup
soup = BeautifulSoup(code_in_text, 'lxml')  
tables = soup.find_all('table')

for table in tables:
    for row in table.find_all('td', {'style': 'text-align: center;'}):
        print(row)

