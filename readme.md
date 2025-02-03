# Jeux Olympiques 2024

Cette application permet aux utilisateurs d’acheter des e-billets pour assister aux Jeux Olympiques de Paris 2024. Les billets seront envoyés directement à l'adresse e-mail de l'utilisateur après l'achat.

## Fonctionnalités

- Tout utilisateur souhaitant acheter des tickets doit créer un compte privé avant de passer à l'étape de paiement.
- Chaque billet sera envoyé à l'adresse e-mail associée au compte.
- Possibilité de **modifier, supprimer et visualiser** son compte utilisateur.
- Chaque utilisateur dispose d’un **panier** pour gérer ses achats.
- Accès à la liste des différentes épreuves des JO.

## Installation

L'application est développée en **Python** avec le framework **Django**.

### Vérification de la version de Python

> python --version

Python 3.4 et supérieur inclut déjà pip (le gestionnaire de paquets). Si vous utilisez une version plus ancienne, vous devrez l’installer manuellement.

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
