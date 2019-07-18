import requests
from bs4 import BeautifulSoup
import smtplib
import json



def check_price(product):
    URL = product['url']
    MAX_PRICE = product['max_price']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')

    soup = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()

    last_char = 5
    while True:
        parsed_price = price[0:last_char]
        if ',' not in parsed_price:
            break
        else:
            last_char -= 1

    actual_price = float(parsed_price)

    print('·', title.strip(), '-', actual_price, '€')

    if(actual_price < MAX_PRICE):
        send_mail(product)
    else:
        print('  [-] El precio es superior a', MAX_PRICE, '€')

def send_mail(product):

    with open('data/credentials.json', 'rt') as f:
        credentials = json.load(f)

    server = smtplib.SMTP(credentials['server'], credentials['port'])
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(credentials['mailFrom'], credentials['password'])

    subject = 'REBAJA - ' + product['name']
    body = 'Haz click en el siguiente enlace: ' + product['url']
    msg = f'Subject: {subject}\n\n{body}'
    
    server.sendmail(
        credentials['mailFrom'],
        credentials['mailTo'],
        msg
    )

    print('  [+] El producto está rebajado. Correo enviado.')

    server.quit()


with open('data/products.json', 'rt') as f:
    products = json.load(f)

for product in products:
    check_price(product)
    print('\n')
