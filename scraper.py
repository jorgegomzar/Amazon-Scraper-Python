import requests
from bs4 import BeautifulSoup
import smtplib
import json
import os

def check_price(product):
    """ Checks the current price of a product.
    If the price is below the MAX_PRICE chose by the user
    sends him an email. """

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

    # This parses the price until there is no ',' in it.
    last_char = 5
    while True:
        parsed_price = price[0:last_char]
        if ',' not in parsed_price:
            break
        else:
            last_char -= 1

    actual_price = float(parsed_price)

    print('·', title.strip(), '-', actual_price, translations['currency'])

    if(actual_price < MAX_PRICE):
        send_mail(product)
    else:
        print(translations['scraper']['greater'], '{:.2f}'.format(MAX_PRICE), translations['currency'])

def send_mail(product):
    """ Sends an email to the user using his credentials,
    from the data/credentials.json file. """
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

    print(translations['scraper']['less'])

    server.quit()

def scraper():
    """ Starts the scraping of the products """

    if(os.path.isfile('data/products.json') and os.path.isfile('data/credentials.json')):
        with open('data/products.json', 'rt') as f:
            products = json.load(f)
        for product in products:
            check_price(product)
            print('\n')
    else:
        print(translations['warning'])
    
    os.system('pause')

def add_product():
    """ Adds a new product to the products.json file """

    os.system('cls')
    name = input(translations['addition']['name'])
    url = input(translations['addition']['url'])
    price = float(input(translations['addition']['price']))

    if(os.path.isfile('data/products.json')):
        with open('data/products.json', 'r') as f:
            products = json.load(f)
    else:
        products = []

    products.append({
        'name': name,
        'url': url,
        'max_price': price
    })

    with open('data/products.json', 'w') as f:
        json.dump(products, f)

def set_credentials():
    """ Sets the credentials for the mail notification """

    os.system('cls')
    server = input(translations['credentials']['server'])
    port = int(input(translations['credentials']['port']))
    mailFrom = input(translations['credentials']['mailFrom'])
    mailTo = input(translations['credentials']['mailTo'])
    password = input(translations['credentials']['password'])

    with open('data/credentials.json', 'w') as f:
        json.dump({
            "server": server,
            "port": port,
            "mailFrom": mailFrom,
            "mailTo": mailTo,
            "password": password,
        }, f)

def set_language():
    """ Checks if the user has already been asked for his language,
    if not, asks him the language preferred and loads the translations """

    global translations

    if(not os.path.isfile('data/config.json')):
        while(True):
            language = input('Language/Idioma (en for English / es para Español): ').lower()
            if(language == 'en' or language == 'es'):
                with open('data/config.json', 'w') as f:
                    json.dump({ "language": language },f)
                break
    else:
        with open('data/config.json', 'r') as f:
            config = json.load(f)
            language = config['language']
    

    with open('translations/{}.json'.format(language), encoding='utf-8') as f:
        translations = json.load(f)

def print_main_menu():
    """ Just prints main menu, duh """

    print("{:*^50s}".format('')) 
    print("*{: ^48s}*".format("Amazon Scraper".upper()))
    print("{:*^50s}".format('')) 
    print("*  {: <46s}*".format(translations['menu']['opt0']))
    print("*  {: <46s}*".format(translations['menu']['opt1']))
    print("*  {: <46s}*".format(translations['menu']['opt2']))
    # print("*  {: <46s}*".format(translations['menu']['opt3']))
    print("*  {: <46s}*".format(translations['menu']['opt4']))
    print("{:*^50s}".format(''))

def main():
    """ Where everything starts.
    Loads the main menu and calls functions to please the user's choices """

    set_language()

    while(True):
        while(True):
            os.system('cls')
            print_main_menu()
            option = int(input(translations['choice']))
            if(option >= 0 and option < 5):
                break
        if(option == 0):
            break
        elif(option == 1):
            scraper()
        elif(option == 2):
            add_product()
        else:
            set_credentials()

translations = {}

if(__name__ == '__main__'):
    main()

