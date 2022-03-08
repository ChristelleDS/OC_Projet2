# Importation des modules
import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime
import time

date = datetime.datetime.today().strftime('%Y%m%d')

repo_day = str("./Exports/"+date)
if not os.path.exists(repo_day):
    os.makedirs(repo_day)

if not os.path.exists(repo_day+"/Images"):
    os.makedirs(repo_day+"/Images")

os.chdir(repo_day)
print(str("Répertoire d'export: "+ os.getcwd()))

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
    def __insertInFile__(self):
        nom_fichier = str("f_export_"+ c.name +"_"+ date +".csv")
        with open(nom_fichier, 'a', newline='',encoding="utf-8") as fichier_csv:
            ligne = [url_pdt,upc,product_title,p_ttc,p_ht,stock,description,category,rating,img]
            w =csv.writer(fichier_csv,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(ligne)


## HOMEPAGE : récupération des catégories
url_main= 'http://books.toscrape.com'

#Récupération des pages catégories
for row in get_soup(url_main).find("ul", class_="nav nav-list").find_all('a'):
    category_name = row.string
    c=Category(str.strip(category_name), str("http://books.toscrape.com/"+row['href']))
    if str.strip(category_name) == "Books":  # ne rien faire pour la categorie parente "books"
        continue
    else :
        c.__createFile__()       #initialisation du fichier d'export pour la catégorie 
        #enregistrer la page index de la catégorie dans le dictionnaire pages_cat
        pages_cat=[]
        pages_cat.append(c.url)
        #gestion des catégories de plusieurs pages
        try:  # présence d'un bouton "next"
            next = get_soup(c.url).find("li", class_="next").find('a').get('href')
            url_cat = c.url[0:-10]
            p_max = int(str.strip(get_soup(c.url).find("li", class_="current").get_text())[10:])  #nb de pages
            i = 2
            #enregistrement des url des pages 2 et +
            while i <= p_max:
                pages_cat.append(f"{url_cat}page-{i}.html")
                i = i+1
        except AttributeError:  #pas de bouton "next" = une seule page
            pass
        for page in pages_cat :  # parsing des pages catégories pour retrouver les articles
            links = []
            links = get_soup(page).find_all('h3') 
            for link in links:  #pour chaque article: parser la page
                url_pdt = str("http://books.toscrape.com/catalogue/")+str(link.find('a').get('href'))[9:]
                soup = get_soup(url_pdt)
                #extraire les informations recherchées:
                upc = soup.find_all('td')[0].get_text()
                product_title = soup.find("li", class_="active").get_text()
                p_ttc = soup.find_all('td')[3].get_text()
                p_ht = soup.find_all('td')[2].get_text()
                stock = str.strip(soup.find("p", class_="instock availability").get_text())
                desc =  soup.find_all('p')[3].get_text().strip()
                description = desc.replace(';',',')
                category = c.name
                rating =""
                soup_rating =str(soup.find('p', {'class' : 'star-rating'}))[22:25]
                if soup_rating == "One":
                    rating = 1
                elif soup_rating == "Two":
                    rating = 2
                elif soup_rating == "Thr":
                    rating = 3
                elif soup_rating == "Fou":
                    rating = 4
                elif soup_rating == "Fiv":
                    rating = 5
                src = soup.find("img")['src']
                img = str("http://books.toscrape.com/"+src[6:])
                # chargement des données dans le fichier d'export de la catégorie
                c.__insertInFile__()
                # téléchargement et enregistrement de l'image
                img_data = requests.get(img).content
                img_file = str(c.name+"_"+upc+'.jpg')  #nom du fichier image
                os.chdir("./Images")
                with open(img_file, 'wb') as jpg:
                    jpg.write(img_data)
                os.chdir(os.pardir)

print("fin du programme")
