# OC_Projet2

# Invite de commande : 
Se positionner dans le répertoire souhaité et y déposer les livrables

cd <répertoire>

# Création et activation de l'environnement virtuel
python -m venv env

#Windows:

env/Scripts/Activate.bat

#Autre:

source env/bin/activate
# Installation des modules requirements:
pip install -r requirements.txt

# Exécution du programme d'export
python P2_script_1.1.0.py

# Exploitation des fichiers générés
Pour remettre en forme les données dans les fichiers excel:
- ouvrir le fichier
- se positionner sur la colonne A
- Menu "Données" / Convertir / Choisir le type de fichier "délimité" / Séparateur : ","
