# Importation des modules
import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime
import time

#répertoire de travail
os.chdir("C:\\Users\\Chris\\OneDrive\\Documents\\OCP2\\Exports")
print(str("Répertoire d'export: "+ os.getcwd()) )
#recupérer la valeur du repo dans un fichier de param?

#Amelioration : création auto d'un répertoire d'export pour les fichiers du jour

#variables globales
date = datetime.datetime.today().strftime('%Y%m%d')
#fonction parser une page html
def get_soup(url):
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup

# Définition des classes et leurs méthodes
class Category:
    def __init__(self, name, url):
        self.name = name
        self.url = url
    def __createFile__(self):
        en_tete = ["product_page_url", "universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description", "category","review_rating","image_url"]
        nom_fichier = str("f_export_"+ c.name +"_"+ date +".csv")
        with open(nom_fichier, 'w', newline='', encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(en_tete)
            print("fichier d'export initié pour la catégorie " +self.name)
            # amelioration : création d'un repo pour chaque catégorie afin d'y stocker le fichier export ainsi que les images
    def __createRepo__(self):
        nom_repo = c.name+"_images"
        os.makedirs( os.getcwd()+'/'+nom_repo)
    def __insertInFile__(self):
        nom_fichier = str("f_export_"+ c.name +"_"+ date +".csv")
        with open(nom_fichier, 'a', newline='',encoding="utf-8") as fichier_csv:
            ligne = [url_pdt,upc,product_title,p_ttc,p_ht,stock,description,category,rating,img]
            w =csv.writer(fichier_csv,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(ligne)


## HOMEPAGE : récupération des catégories
url_main= 'http://books.toscrape.com'
categories = get_soup(url_main).find("ul", class_="nav nav-list").find_all('a')

for row in categories:
    # bypasser la categorie parente "books"
    category_name = row.string   
    if str.strip(category_name) == "Books":
        continue
    else :
        #enregistrer la catégorie
        c=Category(str.strip(category_name), str("http://books.toscrape.com/"+row['href']))
        #initialisation du fichier d'export pour la catégorie
        c.__createFile__()
        # récupération des pages articles de la catégorie
        links = []
        links = get_soup(c.url).find_all('h3')
        print("récupération des articles")
        for link in links:
            #scrapping de la page
            url_pdt = str("http://books.toscrape.com/catalogue/")+str(link.find('a').get('href'))[9:]
            soup = get_soup(url_pdt)
            # extraction et retraitement des informations sur l'article
            upc = soup.find_all('td')[0].get_text()
            product_title = soup.find("li", class_="active").get_text()
            p_ttc = soup.find_all('td')[3].get_text()
            p_ht = soup.find_all('td')[2].get_text()
            stock = str.strip(soup.find("p", class_="instock availability").get_text())
            desc =  soup.find_all('p')[3].get_text()
            description = desc.replace(';',',')
            category = str.strip(c.name) #category['name']
            rating = " a retravailler " 
            #str(soup.find("p", class_="star-rating One")).count('icon-star')
            src = soup.find("img")['src']
            img = str("http://books.toscrape.com/"+src[6:])
            # téléchargement de l'image
            img_data = requests.get(img).content
            img_file = str(upc+'.jpg')  #nom du fichier image
            # sauvegarde du fichier image
            with open(img_file, 'wb') as jpg:
                jpg.write(img_data)
            # chargement des données article dans le fichier d'export
            c.__insertInFile__()
    time.sleep(2)
print("fin du programme")