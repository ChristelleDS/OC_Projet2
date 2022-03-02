# Importation des modules
import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime

#répertoire de travail
os.chdir("C:\\Users\\Chris\\OneDrive\\Documents\\OCP2\\Exports")
print(str("Répertoire d'export: "+ os.getcwd()) )
#recupérer la valeur du repo dans un fichier de param?

#Amelioration : création auto d'un répertoire d'export pour les fichiers du jour

#variables globales
date = datetime.datetime.today().strftime('%Y%m%d')

#FONCTIONS GLOBALES
"""
def extraire_donnees(elements):
    resultat = []
    for element in elements:
        resultat.append(element.string)
    return resultat
"""
"""
 fonction scrapper une page
def get_soup(url):
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
"""

## HOMEPAGE : récupération des catégories
url= 'http://books.toscrape.com'
reponse = requests.get(url)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

categories = soup.find("ul", class_="nav nav-list").find_all('a')

for row in categories:
    category= dict()
    category_name = row.string
    # bypasser la categorie parente "books"
    if str.strip(category_name) == "Books":
        continue
    else :
        #enregistrer la catégorie
        category['url'] = str("http://books.toscrape.com/"+row['href']) 
        category['name'] = str.strip(category_name)
        print("Début de traitement de la catégorie : "+category['name'])
        #initialisation du fichier d'export pour la catégorie
        #amelioration : vérifier existence du fichier avant création
        nom_fichier = str("f_export_"+ category['name'] +"_"+ date +".csv")
        en_tete = ["product_page_url", "universal_ product_code","title","price_including_tax","price_excluding_tax","number_available", "product_description", "category","review_rating","image_url"]
        with open(nom_fichier, 'w', newline='', encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(en_tete)
            print("fichier: " + nom_fichier + " initié")
        # scrapping de la page catégorie
        url = category['url']
        ### TO DO ########
        # gestion des pages multiples
        ###
        reponse = requests.get(url)
        page = reponse.content
        soup = BeautifulSoup(page, "html.parser")
        # récupération des pages articles de la catégorie
        h3 = soup.find_all('h3')
        for link in h3:
            page_article = str("http://books.toscrape.com/catalogue/")+str(link.find('a').get('href'))[9:]
            #print("Page article en cours de traitement: "+page_article)
            # scrapping de la page article
            url=page_article
            reponse = requests.get(url)
            page = reponse.content
            soup = BeautifulSoup(page, "html.parser")
            url_pdt = page_article
            # récupération des informations sur l'article
            upc = soup.find_all('td')[0].get_text()
            product_title = soup.find("li", class_="active").get_text()
            p_ttc = soup.find_all('td')[3].get_text()
            p_ht = soup.find_all('td')[2].get_text()
            stock = str.strip(soup.find("p", class_="instock availability").get_text())
            desc =  soup.find_all('p')[3].get_text()
            description = desc.replace(';',',')
            category = str.strip(category_name) #category['name']
            rating = " a retravailler " 
            #str(soup.find("p", class_="star-rating One")).count('icon-star')
            src = soup.find("img")['src']
            img = str("http://books.toscrape.com/"+src[6:])
            # chargement des données dans le fichier d'export
            ligne = [url_pdt,upc,product_title,p_ttc,p_ht,stock,description,category,rating,img]
            #Ecriture des infos de l'article dans le fichier de la categorie
            with open(nom_fichier, 'a',newline='', encoding="utf-8") as fichier_csv:
                w =csv.writer(fichier_csv,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                w.writerow(ligne)
        #amelioration : ajout d'une ligne nombre total de livres traités par catégories

print("fin du programme")

"""
# initialisation du fichier csv exporté pour la catégorie en cours
nom_fichier = str("f_export_"+ category['name'] +"_"+ date +".csv")
en_tete = ["product_page_url", "universal_ product_code","title","price_including_tax","price_excluding_tax","number_available", "product_description", "category","review_rating","image_url"]

def init_fichier(nom_fichier, en_tete):
    with open(nom_fichier, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        print("fichier: " + nom_fichier + " initié")

init_fichier(nom_fichier, en_tete)
"""

## PAGE PRODUIT
"""
url="http://books.toscrape.com/catalogue/the-passion-of-dolssa_351/index.html"
reponse = requests.get(url)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")
url_pdt = url #page_article
# récupération des informations sur l'article
upc = soup.find_all('td')[0].get_text()
product_title = soup.find("li", class_="active").get_text()
p_ttc = soup.find_all('td')[3].get_text()
p_ht = soup.find_all('td')[2].get_text()
stock = str.strip(soup.find("p", class_="instock availability").get_text())
desc =  soup.find_all('p')[3].get_text()
description = desc.replace(';',',')
category = str.strip(category_name) #category['name']
rating = " a retravailler " 
#str(soup.find("p", class_="star-rating One")).count('icon-star')
src = soup.find("img")['src']
img = str("http://books.toscrape.com/"+src[6:])
# chargement des données dans le fichier d'export
ligne = [url_pdt,upc,product_title,p_ttc,p_ht,stock,description,category,rating,img]
print(ligne)


nom_fichier = "test.csv"
with open(nom_fichier, 'w',newline='', encoding="utf-8") as fichier_csv:
    w =csv.writer(fichier_csv,delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL )
    w.writerow(ligne)

"""

## Récupération du tableau contenant les informations produits
#tab_produit = soup.find('table', {'class' : 'table table-striped'})

