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
separator = "f9ha"


# class product:
#     def __init__(self):
#         self.handle = ''
#         self.title = ''
#         self.description = ''
#         self.type = ''
#         self.option1 Name = ''
#         self.option1 Value = ''
#         self.compareAtPrice = ''
#         self.price = ''
#         self.published = ''
#         self.requires_shipping = ''
#         self.SKU = ''
#         self.tags = ''
#         self.taxable = ''
#         self.grams = ''
#         self.image URL = ''
#         self.image Position = ''
#         self.imageAltText = ''

#         self.url=''

dummy = {
    'title':'',
    'price':'',
    'Weight in Grams':'',
    'handle':'',
    'Requires':'',
    'Requires Shipping':'',
    'title':'',
    'image URL':'',
    'image Position':'',
    'image URL':'',
    'option1 Name':'',
    'option1 Value':'',
    'taxable':'',
    'url':'',
    'description':''
    
}
def dict_to_string(dictionary):
    line = ''
    line += str(dictionary['handle'])                 + separator
    line += str(dictionary['title'])                 + separator
    line += str(dictionary['price'])                 + separator
    # line += str(dictionary['url'])                   + separator
    line += str(dictionary['Weight in Grams'])       + separator
    line += str(dictionary['Requires Shipping'])     + separator
    line += str(dictionary['image URL'])             + separator
    line += str(dictionary['image Position'])        + separator
    line += str(dictionary['option1 Name'])          + separator
    line += str(dictionary['option1 Value'])         + separator
    line += str(dictionary['description'])  
    line += "\n"
    return line

products = []

#Get the product list
req = requests.get(home_page + product_page)
soup = bs(req.text,'html.parser')

#main info
cards = soup.find_all('div',class_="product--bottom-container")

#print(f'amount of cars {len(cards)}')
for card in cards:
    p = {
        'title':'',
    'price':'',
    'Weight in Grams':'',
    'handle':'',
    'Requires':'',
    'Requires Shipping':'',
    'title':'',
    'image URL':'',
    'image Position':'',
    'image URL':'',
    'option1 Name':'',
    'option1 Value':'',
    'taxable':'',
    'url':'',
    'description':''
    }
    
    p['price'] = card.find('span',class_='price--default is--nowrap').text.split('€',1)[0]
    p['title'] = card.find('a',class_='product--title')['title']
    p['url'] = card.find('a',class_='product--title')['href']
    
    kg=''
    try:
        kg= card.find('div',class_ = 'price--scale is--nowrap').text.split('€',1)[0].replace(',','')
        kg = float(kg)/100
        p['Weight in Grams'] = kg / 1000
        p['Weight in Grams'] = p['price'] / p['Weight in Grams']
        ##print(p['Weight in Grams'])
    except :
        pass
        #print('Got axception with weight')

    try:
        tags = card.find_all('li')
        for tag in tags:
            p['tags'] += f' {tag.text}'
        
    except :
        pass
        #print('Got axception with tags')

    products.append(p)
driver = webdriver.Chrome(ChromeDriverManager().install())
numProduct = 0
variantList = []
with open('output2.csv','w',encoding="UTF-8") as outfile:
    line = ''
    numKeys = 1

    
    line += 'handle'                + separator
    line += 'title'                 + separator
    line += 'price'                 + separator
    # line += 'url'                   + separator
    line += 'Weight in Grams'       + separator
    line += 'Requires Shipping'     + separator
    line += 'image URL'             + separator
    line += 'image Position'        + separator
    line += 'option1 Name'          + separator
    line += 'option1 value'         + "\n"
    line += 'description'           + separator
    outfile.write(line)
    for p in products:
        numProduct += 1
        if numProduct > 3:
            break
        print(f'\n\n\n\n-----------------------------Making product {numProduct}/{len(products)}----------------------------------------\n')
        
        p['handle'] = p['url'].split('/')[-1]
        p['handle'] = p['handle'].split('?')[0]
        p['Requires Shipping'] = 'True'
        p['taxable'] = 'True'
        #Category tags
        
        
        #driver.get(p['url'])

        #WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))).click()
        
        #page = driver.execute_script('return document.documentElement.outerHTML')
        #with open(f'outter.html','w',encoding="UTF-8") as file:
            #file.write(page)
        
        page = requests.get(p['url'])
        soup = bs(page.text,'html.parser')#""".text"""

    
        #description cote
        buybox = soup.select("div.product--buybox-container")[0]
        print(buybox)
        title = buybox.select('h1.product--title')[0]
        title.decompose()
        title = buybox.select('div.product--stars')[0]
        title.decompose()
        
        des = str(buybox)
       
        

        # try:
        #     p['description'] += str(soup.select('div.dc-product-details--entry'))
        #     # #print(descriptions)
        #     # for des in descriptions:
        #     #     p['description'] += str(des.html)
        #     #     #print(p['description'])
        # except :
        #     #print('Got axception in description dc-product-details--entry')
        try:
            des += str(soup.select('div.dc-product-details'))
        except :
            pass
            #print('Got axception in description container')
        try:
            des += str(soup.select('div.product--accordion-container'))
        except :
            pass
            #print('Got axception in description container')
        try:
            p['description'] = str(des.replace('\n','').replace('[','').replace(']','').replace('background-image:','patatipatata').replace("\"\"","hahahaha"))
            p['description'] = p['description'].replace('patatipatata','background-size:cover; height:300px; background-image:').replace("hahaha","\"")
            
            #print('description' + p['description'])
        except :
            pass
            #print('exception trying to replace new lines')
        #print('description')
        #print(p['description'])
        #images 
        images = soup.find_all('div', class_ = 'image--box image-slider--item')
        
        i=1
        p['image URL'] =''
        for image in images:
            im = {
                'handle' : p['handle']
            }
            
            img = image['style'].split('url(',2)[2].split('\')',1)[0]
            img = img.replace('\'','')
            im['image URL'] = img
            im['image Position'] = f'{i}'
            variantList.append(im)
            i+=1


        outfile.write(dict_to_string(p))
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
                    #print('Got axception no cookies')
                i=1
                
                for variant in variants:
                    v = {}
                    v['handle'] = p['handle']

                    selectField = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "select-field")))
                    selectField.click()
                    ##print("selectField")
                    option = WebDriverWait(selectField,15).until(EC.presence_of_all_elements_located((By.XPATH,".//*")))
                    #option = selectField.find_elements_by_xpath(".//*")
                    ##print("Option Declared")
                    option[i].click()
                    
                    page = driver.page_source
                    
                    soup = bs(page,'html.parser')
                    
                    v['title'] = str(soup.find('h1', class_='product--title').text).strip()
                    
                    v['price'] = soup.find('span', class_='price--content content--default').text.split('€',1)[0].strip().replace(',','.')
                    ##print(v['price'])
                    v['Weight in Grams'] = soup.find("div",class_="product--unit").text.split('. ',1)[1].split(' ',1)[0]
                    ##print(v['Weight in Grams'])
                    v['option1 Name']='Option'
                    v['option1 Value'] = variant.text.strip()
                    
                   #description cote
                    des = str(soup.select("div.product--buybox-container"))
                
                    

                    # try:
                    #     p['description'] += str(soup.select('div.dc-product-details--entry'))
                    #     # #print(descriptions)
                    #     # for des in descriptions:
                    #     #     p['description'] += str(des.html)
                    #     #     #print(p['description'])
                    # except :
                    #     #print('Got axception in description dc-product-details--entry')
                    try:
                        des += str(soup.select('div.dc-product-details--entry'))
                    except :
                        pass
                        #print('Got axception in description container')
                    
                    try:
                        v['description'] = str(des.replace('\n',''))
                        #print('description' + p['description'])
                    except :
                        pass



                    i +=1
                    outfile.write(dict_to_string(v))
                    variantList.append(v) 




                
        except:
            pass
            #print('Got axception somewhere in variants')

for variant in variantList:
    products.append(variant)
df = pd.DataFrame(products)
df = df.drop_duplicates()
df.to_csv('Output.csv')

l = []
with open("Output.csv",'r+',encoding="UTF-8") as file:
    for line in file:
        l.append(line)

i=0
while i<len(l):
    j=0
    while j<len(l):
        if l[i] == l[j] and not i==j:
            del l[j]
        j += 1
    i += 1
with open("output2.csv",'w',encoding="UTF-8") as file:
    for x in l:
        file.write(x)
df.to_json('Output.js')
    
#print(products[1]['title'])                 
#print(products[1]['price'])                 
#print(products[1]['url'])                   
#print(products[1]['Weight in Grams'])       
#print(products[1]['Requires Shipping'])     
##print(products[1]['description'])           
#print(products[1]['image URL'])             
#print(products[1]['image Position'])        
#print(products[1]['option1 Name'])          
#print(products[1]['option1 Value'])







#in the product pages
