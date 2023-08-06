import requests
from bs4 import BeautifulSoup

url = 'https://www.minusrus.com/'
r = requests.get(url)

bs = BeautifulSoup(r.text, 'html.parser')

def personnel(item):
    total = bs.find('div', class_ = 'card__amount').find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    quantity = bs.find('div', class_ = 'card__amount').find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error

def bbm(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[1].text
    total = bs.find_all('div', class_ = 'card__amount')[1].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[1].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error

def tanks(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[2].text
    total = bs.find_all('div', class_ = 'card__amount')[2].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[2].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error
    
def artillery(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[3].text
    total = bs.find_all('div', class_ = 'card__amount')[3].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[3].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error
    
def planes(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[4].text
    total = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[4].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error
    
def helicopters(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[5].text
    total = bs.find_all('div', class_ = 'card__amount')[5].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[5].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error
    
def warships(item):
    total_code = bs.find_all('div', class_ = 'card__amount')[6].text
    total = bs.find_all('div', class_ = 'card__amount')[6].find_all('span')[0].text.replace('.', ' ').replace('~', '').strip()
    if '+' not in total_code:
        quantity = 'none'
    else:
        quantity = bs.find_all('div', class_ = 'card__amount')[6].find_all('span')[1].text.strip()
    if item == 'total':
        return total
    elif item == 'quantity':
        return quantity
    else:
        error = 'error: invalid argument'
        return error