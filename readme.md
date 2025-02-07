# Jeux Olympiques 2024

Cette application permet aux utilisateurs d’acheter des e-billets pour assister aux Jeux Olympiques de Paris 2024. Les billets seront envoyés directement à l'adresse e-mail de l'utilisateur après l'achat.

## Fonctionnalités

- Tout utilisateur souhaitant acheter des tickets doit créer un compte privé avant de passer à l'étape de paiement.
- Chaque billet sera envoyé à l'adresse e-mail associée au compte.
- Possibilité de **modifier, supprimer et visualiser** son compte utilisateur.
- Chaque utilisateur dispose d’un **panier** pour gérer ses achats.
- Accès à la liste des différentes épreuves des JO.

## Installation pour un environnement Windows

L'application est développée en **Python** avec le framework **Django**.

### Vérifier si Python est installé

Ouvrez un terminal ou une invite de commande

> python --version

Si une version de Python s'affiche, c'est que Python est déjà installé.
Si vous obtenez une erreur, passez à l'étape suivante pour l'installation. 

### Installer Python

Téléchargez Python 3.0 ou une version plus récente depuis le site officiel :

https://www.python.org/downloads/

Lors de l’installation, cochez impérativement l’option :
- "Add Python to PATH"

Ensuite, cliquez sur "Install Now" et suivez les instructions.

### Vérification l'installation de Python et pip

Après l’installation, ouvrez un terminal et vérifiez à nouveau Python :

> python --version

Assurez-vous également que pip (le gestionnaire de paquets) est bien installé :

> pip --version

Si pip n'est pas détecté, installez-le avec :

> python -m ensurepip --default-pip

### Installation de Django

Installez Django avec la commande suivante :

> pip install django

Vérifiez ensuite que l'installation s'est bien effectuée en affichant la version de Django :

> django-admin --version

## Configuration

1. Créer un fichier .env pour stocker les variables d’environnement
2. Créer un fichier requirements.txt :
   - Ce fichier permettra d’installer automatiquement toutes les dépendances nécessaires à l'application.
   - Pour générer ce fichier avec toutes les dépendances installées :
     > pip freeze > requirements.txt
3. Lancer l'application

> python manage.py migrate <br>
> python manage.py runserver

## Licence

Ce projet est sous license **MIT**. Vous êtes libre de l'utiliser et de le modifier.
