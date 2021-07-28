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


def getDescription(soup,p):
    #description cote
    buybox = soup.select("div.product--buybox-container")[0]
    ##print(buybox)
    title = buybox.select('h1.product--title')[0]
    title.decompose()
    try:
        scripts = soup.select('script')
        for script in scripts:
            script.decompose()
    except :
        pass
    try:
        stars = buybox.select('div.product--stars')
        
        for component in stars:
            # 
            component.decompose()
        stars = vuybox.select('div#ts_product_widget_position')
        for component in stars:
            
            component.decompose()
    except:
        pass
        #print
    try:
        sku = buybox.select('ul.product--base-info')
        
        for component in sku:
             
            component.decompose()

        
    except:
        pass
        #print
    
    try:
        variants = buybox.select('div.product--configurator')
        for component in variants:
            component.decompose()
    except:
        pass
        #print("error in removing variants")
    try:
        price = buybox.select('span.price--content')[0]
        price.decompose()
        #print("removed price")
    except:
        pass
        #print("error in removing price")
    try:
        qty = buybox.select('div.buybox--button-container')[0]
        qty.decompose()
        #print("removed tqy")
    except:
        pass
        #print("error in removing qty")
    des = str(buybox)
    
    

    
    try:
        des += str(soup.select('div.dc-product-details'))
    except :
        pass
        ##print('Got axception in description container')
    try:
        reviews = soup.select('div#product--rating')[0]
        reviews.decompose()

    except :
        pass
    try:
        des += str(soup.select('div.product--accordion-container')[0])
    except :
        pass
        #print('Got axception in description container')
    try:
        p['description'] = str(des.replace('\n','').replace('[','').replace(']','').replace('background-image:','patatipatata').replace("\"\"","hahahaha"))
        p['description'] = p['description'].replace('patatipatata','background-size:cover; height:300px; background-image:').replace("hahaha","\"")
        
        ##print('description' + p['description'])
    except :
        pass
        
    try:
        p['description'] = p['description'].replace('display: none;','display: block;')
        p['description'] = p['description'].replace('\'showRating\' : \'true\'','\'showRating\' : \'false\'')
    except :
        #print("exception in changing display")
        pass
    return p
#Get the product list
req = requests.get(home_page + product_page)
soup = bs(req.text,'html.parser')

#main info
cards = soup.find_all('div',class_="product--bottom-container")

##print(f'amount of cars {len(cards)}')
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
    'option1 Name':'Title',
    'option1 Value':'Default Title',
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
        ###print(p['Weight in Grams'])
    except :
        pass
        ##print('Got axception with weight')

    try:
        tags = card.find_all('li')
        i=0
        if len(tags)>0:
            t='\"'
            while i<len(tags)-1:
                t+=tags[i].text + ", "
                i+=1
            t += tags[i].text + '\"'
            p['tags'] = t
           # print(t)
    except :
        pass
        print('Got axception with tags')

    products.append(p)
#driver = webdriver.Chrome(ChromeDriverManager().install())
numProduct = 0
variantList = []

for p in products:
    numProduct += 1
    # if numProduct > 5:
    #     break
    print(f'-----------------------------Making product {numProduct}/{len(products)}----------------------------------------')
    
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


    images = soup.find_all('div', class_ = 'image--box image-slider--item')
    
    i=1
    p = getDescription(soup,p)
    p['image URL'] =''
    containerimg=[]
    for image in images:
        im = {}
        for key in p:
            if not (key == "description" or key == "option1 Name" or key == "option1 Title"):
                im[key] = p[key]
        #im = {'handle': p['handle']} 
        if i==1:
            im['description'] = p["description"]
        
        img = image['style'].split('url(',2)[2].split('\')',1)[0]
        img = img.replace('\'','')
        containerimg.append(img)
        im['image URL'] = img  #was im
        #im['Variant Description'] = 'Default description'
        im['image Position'] = f'{i}'
        variantList.append(im)
        i+=1
    #p = getDescription(soup,p)
    #p['image URL'] ='; '.join(containerimg)
    
    
    # try:
    #     variants = soup.find('div',class_='product--configurator')
    #     variants = variants.find_all('option')
    #     if len(variants)>1:
    #         driver.get(p['url'])
    #         try:
    #             WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))).click()
    #         except :
    #             pass
    #             ##print('Got axception no cookies')
    #         i=1
            
    #         for variant in variants:
    #             v = {}
    #             v['handle'] = p['handle']

    #             selectField = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "select-field")))
    #             selectField.click()
    #             ###print("selectField")
    #             option = WebDriverWait(selectField,15).until(EC.presence_of_all_elements_located((By.XPATH,".//*")))
    #             #option = selectField.find_elements_by_xpath(".//*")
    #             ###print("Option Declared")
    #             option[i].click()
                
    #             page = driver.page_source
                
    #             vsoup = bs(page,'html.parser')
                
    #             v['title'] = str(vsoup.find('h1', class_='product--title').text).strip()
                
    #             v['price'] = vsoup.find('span', class_='price--content content--default').text.split('€',1)[0].strip().replace(',','.')
    #             ###print(v['price'])
    #             v['Weight in Grams'] = vsoup.find("div",class_="product--unit").text.split('. ',1)[1].split(' ',1)[0]
    #             ###print(v['Weight in Grams'])
    #             v['option1 Name']='Option'
    #             v['option1 Value'] = variant.text.strip()
                
    #             #v = getDescription(vsoup,v)



    #             i +=1
                
    #             variantList.append(v) 




            
    # except:
    #     pass
    #     ##print('Got axception somewhere in variants')
    

for variant in variantList:
    products.append(variant)
df = pd.DataFrame(products)
try:
    df = df.drop_duplicates()
except :
    pass
df.sort_values(by='handle')
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
