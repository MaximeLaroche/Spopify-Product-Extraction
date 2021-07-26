from bs4 import BeautifulSoup as bs
import requests
import time
import json
import pandas as pd

home_page = 'https://doncarne.de/de'
product_page = "/produkt/"



class product:
    def __init__(self):
        self.handle = ''
        self.title = ''
        self.description = ''
        self.type = ''
        self.option1Name = ''
        self.option1Value = ''
        self.compareAtPrice = ''
        self.price = ''
        self.published = ''
        self.requires_shipping = ''
        self.SKU = ''
        self.tags = ''
        self.taxable = ''
        self.grams = ''
        self.imageURL = ''
        self.imagePosition = ''
        self.imageAltText = ''

        self.url=''

        


products = []

#Get the product list
req = requests.get(home_page + product_page)
soup = bs(req.text,'html.parser')

#main info
cards = soup.find_all('div',class_="product--bottom-container")

for card in cards:
    p = product()
    p.price = card.find('span',class_='price--default is--nowrap').text.split('€',1)[0]
    p.title = card.find('a',class_='product--title')['title']
    p.url = card.find('a',class_='product--title')['href']
    
    kg=''
    try:
        kg= card.find('div',class_ = 'price--scale is--nowrap').text.split('€',1)[0].replace(',','')
        kg = float(kg)/100
        p.grams = kg / 1000
        p.grams = p.price / p.grams
        print(p.grams)
    except :
        pass

    try:
        tags = card.find_all('li')
        for tag in tags:
            p.tags += f' {tag.text}'
        
    except :
        pass

    products.append(p)

for p in products:
    p.requires_shipping = 'True'
    p.taxable = 'True'
    page = requests.get(p.url)
    soup = bs(page.text,'html.parser')

    #description cote
    description = soup.find('div',class_ = 'product--buybox-container')
    
    for div in description.find_all('div'):
        if not ('form' in div.text or 'price' not in div.text):
            p.description += str(div.html)

    try:
        p.description += str(soup.find('div',class_ = 'dc-product-details--entry dc-element--originrace').html)
    except :
        pass
    try:
        p.description += str(soup.find('div',class_ = 'container').html)
    except :
        pass

    #images 
    images = soup.find_all('div', class_ = 'image--box image-slider--item')
    
    i=1
    for image in images:
        img = image['style'].split('url(',2)[2].split('\')',1)[0]
        p.imageURL += ' ' + img
        p.imagePosition = f'{i}'
        i+=1

    #variants
    try:
        variants = soup.find_all('option')
        for variant in variants:
            v = product()
            v.handle = p.handle
             


            v.url=''
    except:
        pass

    








#in the product pages
