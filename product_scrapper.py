from bs4 import BeautifulSoup as bs
import requests
import time
import json
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re





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
    p = {}
    p['price'] = card.find('span',class_='price--default is--nowrap').text.split('€',1)[0]
    p['title'] = card.find('a',class_='product--title')['title']
    p['url'] = card.find('a',class_='product--title')['href']
    
    kg=''
    try:
        kg= card.find('div',class_ = 'price--scale is--nowrap').text.split('€',1)[0].replace(',','')
        kg = float(kg)/100
        p['grams'] = kg / 1000
        p['grams'] = p['price'] / p['grams']
        print(p['grams'])
    except :
        pass

    try:
        tags = card.find_all('li')
        for tag in tags:
            p['tags'] += f' {tag.text}'
        
    except :
        pass

    products.append(p)
driver = webdriver.Chrome(ChromeDriverManager().install())
r=0
for p in products:
    r+=1
    p['handle'] = re.sub('[^A-Za-z0-9]+','',p['title']).replace(' ','-')
    p['requires_shipping'] = 'True'
    p['taxable'] = 'True'
    
    #driver.get(p['url'])

    #WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))).click()
    
    #page = driver.execute_script('return document.documentElement.outerHTML')
    #with open(f'outter.html','w',encoding="UTF-8") as file:
        #file.write(page)
    
    page = requests.get(p['url'])
    soup = bs(page.text,'html.parser')#""".text"""

   
    #description cote
    description = soup.find('div',class_ = 'product--buybox-container')
    
    for div in description.find_all('div'):
        if not ('form' in div.text or 'price' not in div.text):
            p['description'] += str(div.html)

    try:
        p['description'] += str(soup.find('div',class_ = 'dc-product-details--entry dc-element--originrace').html)
    except :
        pass
    try:
        p['description'] += str(soup.find('div',class_ = 'container').html)
    except :
        pass

    #images 
    images = soup.find_all('div', class_ = 'image--box image-slider--item')
    
    i=1
    p['imageURL'] =''
    for image in images:
        img = image['style'].split('url(',2)[2].split('\')',1)[0]
        p['imageURL'] += ' ' + img
        p['imagePosition'] = f'{i}'
        i+=1

    #variants
    try:
        variants = soup.find('div',class_='product--configurator')
        variants = variants.find_all('option')
        if len(variants)>1:
            driver.get(p['url'])
            try:
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))).click()
            except :
                pass
            i=1
            
            for variant in variants:
                v = {}
                v['handle'] = p['handle']

                WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "select-field"))).click()
                WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, f"//div[2]/div[1]/form/div/select/option[{i}]"))).click()
                
                page = driver.execute_script('return document.documentElement.outerHTML')
                
                soup = bs(page,'html.parser')
                
                v['title'] = str(soup.find('h1', class_='product--title').text).strip()
                
                v['price'] = soup.find('span', class_='price--content content--default').text.split('€',1)[0].strip().replace(',','.')
                print(v['price'])
                v['grams'] = soup.find("div",class_="product--unit").text.split('. ',1)[1].split(' ',1)[0]
                print(v['grams'])
                v['option1Name']=variant.text.strip()
                v['option1Value'] = v['option1Name']
                
                #description cote
                description = soup.find('div',class_ = 'product--buybox-container')
                
                for div in description.find_all('div'):
                    if not ('form' in div.text or 'price' not in div.text):
                        v['description'] += str(div.html)

                try:
                    v['description'] += str(soup.find('div',class_ = 'dc-product-details--entry dc-element--originrace').html)
                except :
                    pass
                try:
                    v['description'] += str(soup.find('div',class_ = 'container').html)
                except :
                    pass

            
                i +=1

            products.append(v) 




            
    except:
        pass
    
df = pd.DataFrame(products)
df.to_csv('Output.csv')
df.to_json('Output.js')
    








#in the product pages
