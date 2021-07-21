from bs4 import BeautifulSoup as bs
import requests
import time
import json
import pandas as pd

url = 'https://direktvomfeld.eu/products.json'

output = 'products.csv'

req = requests.get(url)
data = req.json()

line = ' handle,title,body,price'
line += '\n'


product_list = []
for product in data['products']:
    print(product['title'])
for product in data['products']:
    
    variants=0
    while variants<len(product['variants']):
        var = product['variants'][variants]
        prod = {
            'handle':product['handle'],
            'title':product['title'],
            'description':product['body_html'],
            'Vendor':product['vendor'],
            'type':product['product_type'],
            'id':id
        }
        i=1
     
        prod[f'Option{i} Name'] = var['option1']
        prod[f'Option{i} Value'] = var['title']
            # for value in option['values']:
            #     prod[f'Option{i} Value'] += value +' '
            #prod[f'Option{i} Values'] = option['values']
            # i+=1
        prod['Compare At Price'] = var['compare_at_price']
        prod['price'] = var['price']
        image = str(var['featured_image'])
        alt = image.split("\'alt\': ",1)
        pos = image.split("\'pos\': ",1)
        src = image.split("\'src\': ",1)
        
        if len(alt)>1:
            index=1
            prod['Image Alt Text'] = ''
            while index<len(alt):
                prod['Image Alt Text'] += alt[index].split(',',1)[0] + " "
                prod['Image Alt Text'] = prod['Image Alt Text'].replace('\'',' ')
                index+=1
        if len(pos)>1:
            index=1
            prod['Image Position'] = ''
            while index<len(pos):
                prod['Image Position'] += pos[index].split(',',1)[0] + " "
                prod['Image Position'] = prod['Image Position'].replace('\'',' ')
                index+=1
        if len(src)>1:
            index=1
            prod['Image URL'] = ''
            while index<len(src):
                prod['Image URL'] += src[index].split(',',1)[0] + " "
                prod['Image URL'] = prod['Image URL'].replace('\'','')
                index+=1
            #print(prod['Image URL'])
            #prod['Variant image'] = prod['Image URL']
        prod['Published'] = var['available']
        prod['Requires Shipping'] = var['requires_shipping']
        prod['SKU'] = var['sku']
        prod['Tags']=''
        for tag in product['tags']:
            prod['Tags'] += tag + '\n'
        prod['Taxable'] = var['taxable']
        prod['Weight in grams'] = var['grams']
        #if var['title'] != "Default Title":
            #prod['title'] = var['title']
        product_list.append(prod)




        variants+=1
    for image in product['images']:
        prod = {

            'handle' : product['handle'],
            'Weight in grams': '',
            'Image URL' : image['src'],
            'Image Position': image['position']
        }
        #print(prod['Image URL'])
        product_list.append(prod)

        # prod['Tags'] = ''
        # for tag in product['tags']:
        #     prod['Tags'] += tag + ' '

        # #prod['Published'] = product['available']
        # i=1
        # for option in product['options']:
        #     prod[f'option{i} Name'] = option['name']
        #     prod[f'option{i} value'] = option['values']
        #     i+=1

        


df = pd.DataFrame(product_list)
df.to_csv('output.csv',encoding="utf-8")




# with open('x.csv','w',encoding='UTF-8') as file:
#     file.write('handle,title,description,Vendor,type,id,Option1 Name,Option1 Value,Compare At Price,price,Published,Requires Shipping,SKU,Tags,Taxable,Weight in grams,Image URL,Image Position,Image Alt Text\n')
#     rows='handle,title,description,Vendor,type,id,Option1 Name,Option1 Value,Compare At Price,price,Published,Requires Shipping,SKU,Tags,Taxable,Weight in grams,Image URL,Image Position,Image Alt Text'.split(',')
#     i=0
#     for prod in product_list:
#         line=''
#         for row in rows:
#             try:
#                 line += str(prod[row])
#             except:
#                 pass
#             line+=','
#             line.replace("\"","xxyy")
#             line.replace("xx","\"")
#             line.replace("yy","\"")
#         print(i)
#         line+='\n'
#         file.write(line)
#         i+=1

