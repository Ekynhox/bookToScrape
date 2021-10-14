from os import write
import requests
import csv
import urllib
from PIL import Image
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

soup_quantite_livre= soup.find_all("ul", {"class", "pager"})

link_next_page = []


url_page = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"






print(soup_quantite_livre)