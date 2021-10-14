import os
import requests
import csv
import urllib
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fonctions import get_category_url, get_all_books, get_data_book, get_image_book

#on stock l'url et on la request via  get
url = "http://books.toscrape.com/"

#on stock les liens de la page
#links = soup.find_all("a")
categorie_links = get_category_url(url)

print("Début du code:")
try:
    os.mkdir('images_livres')
except:
    print('le dossier images_livres existe déjà')

try:
    os.mkdir('csv_livre')
except:
    print('le dossier csv_livre existe déjà')
#on boucle à partir du deuxième élément de la liste de catégorie
for categorie_url in categorie_links[1:]:

    #on récupère le nom de la catégorie via l'url pour nommer le csv
    categorie_link_splits = categorie_url.split("/books/")
    categorie_name = categorie_link_splits[1].split("_")[0]
    print("Récupération des données de la catégorie : " + categorie_name)
    #on appelle la fonction pour récupérer tous les livres
    liens_livres = get_all_books(categorie_url)
    #on créée le fichier csv
    with open(f'csv_livre/{categorie_name}.csv', 'w') as csv_file:  
        fieldnames = ['lien du livre', 'UPC', 'Product Type', 'Price (excl. tax)','Price (incl. tax)', 'Tax', 'Availability','Number of reviews', 'titre', 'image']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #on récupère les images des livres
        for book_url in liens_livres:
            data_livres = get_data_book(book_url)
            writer.writerow(data_livres)
            get_image_book(data_livres["image"], data_livres["titre"].replace(':',''))

print("Terminé.")

            



