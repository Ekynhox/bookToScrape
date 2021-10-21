from os import write
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import webbrowser
from slugify import slugify




def get_category_url(lien):
#on récupère les liens de chaque catégories
  page = requests.get(lien)
  soup = BeautifulSoup(page.content, 'html.parser')
  soup_category = soup.find('div', {'class', 'side_categories'})
  links = [lien + a.get('href') for a in soup_category.find_all('a', href=True)]
  return links

#on récupère les livres de chaque catégories
def get_all_books(categorie_url):
  book_urls = []
  #je récupere le nbre d'element sur la page, division entiere par 20 /+ 1 et boucle sur le nombre de page 
  page = requests.get(categorie_url)
  soup = BeautifulSoup(page.content, 'html.parser')
  #on récupère le nombre de livres par catégories
  get_all_strong= soup.find_all("strong")
  get_strong = get_all_strong[1].get_text()
  nombre_de_page = (int(get_strong)//20)+1
  if nombre_de_page > 1:
    for i in range(1, nombre_de_page+1):     
      categorie_url_pagination = categorie_url.replace("index.html", f"page-{i}.html")
      page = requests.get(categorie_url_pagination)
      soup = BeautifulSoup(page.content, 'html.parser')
      soup_books = soup.find_all("article", {"class", "product_pod"})
      for elements in soup_books:
        books_images = elements.find("a")
        lien = books_images["href"]
        # print(lien)
        new_liens = "https://books.toscrape.com/catalogue/"+ lien.replace("../", "")
        book_urls.append(new_liens)
  else:
    soup_books = soup.find_all("article", {"class", "product_pod"})
    for elements in soup_books:
      books_images = elements.find("a")
      lien = books_images["href"]
      # print(lien)
      new_liens = "https://books.toscrape.com/catalogue/"+ lien.replace("../", "")
      book_urls.append(new_liens)
  return book_urls 

def get_data_book(lien_livre):
  lien_du_livre = lien_livre
  page_data = requests.get(lien_livre)
  soup_data = BeautifulSoup(page_data.content,'html.parser')

  soup_data_titre = soup_data.find('h1')
  soup_data_price = soup_data.find('p',{'class', 'price_color'})
  soup_data_book = soup_data.find_all('tr')
  # soup_book_note = soup_data.find('p', 'class', 'star-rating')
  soup_image = soup_data.find('img')
  titre = soup_data_titre.get_text()
  prix = soup_data_price.get_text()
 
  image = soup_image['src']

  lien_image = urljoin('https://books.toscrape.com/', image)

  upc = soup_data_book[0].get_text()
  type_produit = soup_data_book[1].get_text()
  prix_sans_taxe = soup_data_book[2].get_text()
  prix_avec_taxe = soup_data_book[3].get_text()
  taxe = soup_data_book[4].get_text()
  disponibilite = soup_data_book[5].get_text()
  review = soup_data_book[6].get_text()

  liste_data = []
  
  liste_data = [lien_du_livre, upc, type_produit, prix_sans_taxe, prix_avec_taxe, taxe, disponibilite, review, titre, lien_image]
  dic_data_book = {}
  #on créée la liste des clés
  keys = ['lien du livre', 'UPC', 'Product Type', 'Price (excl. tax)','Price (incl. tax)', 'Tax', 'Availability','Number of reviews', 'titre', 'image']
  #on loop dans les clés et la liste de données  
  for key, values in zip(keys, liste_data):
    values = values.replace(key,'').strip()
    dic_data_book[key] = values

  return dic_data_book
 
def get_image_book(image_link, book_name):
  image_save = requests.get(image_link).content
  with open(f'images_livres/{slugify(book_name[:50])}.jpg','wb') as handler:
    handler.write(image_save)

#récupère les données dans un csv
#pas bien agencé dans le csv
def write_book_csv(dictionnaire):
   with open('data_books.csv', 'w',encoding="utf-8-sig" ) as csv_file:  
      fieldnames = ['lien du livre', 'UPC', 'Product Type', 'Price (excl. tax)','Price (incl. tax)', 'Tax', 'Availability','Number of reviews', 'titre', 'image']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerow(dictionnaire)

      