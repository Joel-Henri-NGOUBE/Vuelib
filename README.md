# VUELIB

VUELIB est une application open source développée en Python pour faciliter les déplacements en vélo dans la ville de Paris en utilisant les informations des stations Vélib'.

## Fonctionnalités

- Affichage de la carte de Paris avec les stations Vélib' marquées.

- Affichage de la liste des stations avec leurs informations détaillées. 

- Consultation des informations en temps réel sur les stations Vélib' (nombre de vélos disponibles, nombre de places disponibles).

- Recherche de stations à proximité.

- Ajouter vos stations préférées en favoris.

## Configuration

- Importer la base de donnée depuis `/Alice/Server/Database/`.
  
- Activer les ports de MySQL et Apache sur XAMPP (Si vous n'avez pas de configuration particulière au préalable).
  
- Installer préalablement le connecteur C de MariaDB en choisissant le OS MS Windows via l'adresse https://mariadb.com/downloads/connectors/.

-- Installer virtualenv --
- Installer le CLI de virtualenv `python -m pip install virtualenv`.

- Créer un environnement virtuel avec la commande `python -m venv .venv` depuis `/Alice/`.

## Installation

- Se déplacer dans `Alice` en faisant `cd Alice`.

- Se déplacer vers l'environnement virtuel grâce à la commande `./.venv/Scripts/Activate.ps1`.
  
--Installer MARIADB--
Exécuter la commande `pip install mariadb`.

--Installer FLASK--
Exécuter la commande `pip install flask`.

## Lancement du projet:

- Lancer le serveur Alice :
`flask --app ./Server/server.py run` (Depuis `/Alice/`).

- Lancer le serveur Bob:
`python ./Bob/Server/server.py` (Depuis `/Vuelib/`).

Vous pouvez maintenant accéder à l'application sur votre navigateur à l'adresse http indiquée par Alice. 