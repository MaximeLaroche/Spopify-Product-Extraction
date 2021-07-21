from bs4 import BeautifulSoup as bs
import requests
import time

site = 'https://direktvomfeld.eu'
all_products_page = '/collections/all'
handle_seperator = '/products/'
output = 'products.csv'

req = requests.get(site + all_products_page)
soup = bs(req.text,'lxml')
class option:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class variant:
    def __init__(self):
        self.sku = ''
        self.grams = ''
        self.inventory_tracker = ''
        #assume we can not get this value
        self.inventory_qty = 0
        self.inventory_policy = ''
        self.fufillment_service = ''
        #must assign value later
        self.price = 0


class product:
    def __init__(self,handle):
        self.handle = handle
        self.title = ''
        self.body = ''
        self.vendor = ''
        self.type = ''
        self.tags = ''
        self.published = True
        self.options = []


products = []
#get the URLs
i=0
for tag in soup.findAll("a",href=True):
    if tag['href'].startswith(all_products_page):
        
        handle = tag['href'].split(handle_seperator,1)
        if len(handle) == 2:
            products.append(product(handle[1]))
            print(products[i].handle)
            i+=1

#go through all products:
for product in products:
    req = requests.get(site + all_products_page + handle_seperator + product.handle)
    soup = bs(req.text, 'lxml')
    #product title
    product.title = soup.find('h1', 'h2 product-single__title').text
    
    #body
    product.body = soup.find('div', 'grid__item grid__item--description')
    print(f'---------------------------------------------------------\n\n{product.title}\n{product.body}')

    #vendor
    product.vendor = soup.find()
    with open("Output.html","w",encoding="utf8") as file:
        file.write(req.text)
    file.close()
    time.sleep(60)


        
      