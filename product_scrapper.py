from bs4 import BeautifulSoup as bs
import requests

url = 'direktvomfeld.eu/collections/all'

req = requests.get(url)
soup = bs(req.text,'html.parser')