import requests
from bs4 import BeautifulSoup

url = 'https://www.analyticsvidhya.com/glossary-of-common-statistics-and-machine-learning-terms/'
source_code = requests.get(url)
code_in_text = source_code.text

# crawling setup
soup = BeautifulSoup(code_in_text, 'lxml')

text_content = soup.find('div', {'class': 'text-content'})

for su_table in text_content.find_all('div', {'class': 'su-table'}):
    table = su_table.find('table')
    if table:
        for rows in table.find_all('tr'):
            first_column = rows.find('td')
            if first_column:
                print(first_column)

# tables = soup.find_all('table')
#
# for table in tables:
#     for row in table.find_all('tr'):
#         column = row.find('td')
#         if column:
#             print(column)


