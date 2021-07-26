from bs4 import BeautifulSoup as bs
import requests
import time
import json
import pandas as pd

home_page = 'https://doncarne.de/de'
product_page = "/produkt/"


req = requests.get(home_page + product_page)

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

        


products = []

#Get the product list
soup = bs(req.text)

