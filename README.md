"# Vuelib" 

# VUELIB

VUELIB est une application open source développée en Python pour faciliter les déplacements en vélo dans la ville de Paris en utilisant les informations des stations Vélib'.

## Fonctionnalités

- Affichage de la carte de Paris avec les stations Vélib' marquées.

- Affichage de la liste des stations avec leurs informations détaillées. 

- Consultation des informations en temps réel sur les stations Vélib' (nombre de vélos disponibles, nombre de places disponibles).

- Recherche de stations à proximité ou par adresse.

- Ajouter vos stations préféré en favoris 

## Installation

- Clonez le dépôt depuis GitHub :

`git clone https://github.com/Joel-Henri-NGOUBE/Vuelib.git`

- Impoter la base de donnée :

- Créer une nouvelle base de donnée vuelib sur MySQL

- Aller dans le fichier /Alice/Server/Database/ et importer le fichier vuelib.sql


## Configuration

Installer le connecteur C de MariaDB en choisissant le OS MS Windows via l'adresse https://mariadb.com/downloads/connectors/.

--Installer MARIADB--
Exécuter la commande `pip install mariadb`

--Installer requests--
Exécuter la commande `pip install requests`

--Installer FLASK--
Exécuter la commande `pip install flask`

-- Installer virtualenv --
Ppour créer un environnement virtuel avec la commande `python -m pip install virtualenv`

-Dans le serveur Alice, créer l'environnement virtuel en faisant `python -m venv .venv` 

- Se déplacer vers l'environnement virtuel grâce à la commande `./.venv/Scripts/Activate.ps1`

- Lancer le serveur Alice : 
`flask --app ./Server/server.py run`

- Lancer le serveur Bob:
`python ./Bob/Server/server.py depuis /Vuelib/`

 Vous pouvez maintenant accéder à l'application sur votre navigateur à l'adresse http indiquer par Alice. 