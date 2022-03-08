# OC_Projet2

# Invite de commande :
# Se positionner dans le répertoire souhaité et y déposer les livrables
cd <répertoire>
# vérifier le contenu : le répertoire doit contenir les fichiers P2_script.py , requirements.txt
ls
# Création et activation de l'environnement virtuel
python -m venv env
#Windows
env/Scripts/Activate.bat
#Autre
source env/bin/activate
# Installation des modules requirements:
pip install -r requirements.txt
# Exécution du programme d'export
python P2_script.py


