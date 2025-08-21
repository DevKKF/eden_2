## VASES D'HONNEUR CENTRE INFLUENCE EDEN 2

Conçu pour le centre influence, ce projet de Vases d'Honneur est destiné à être utilisé dans le but de former les futurs mariés avant leur entrée dans le <b>mariage</b>.

## Technologies utilisées
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/bootstrap-5-logo-icon.svg" alt="" width="10"> Bootstrap
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/hand-gestures/endorsement-icon.svg" alt="" width="10"> Font Awesome
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/git-icon.svg" alt="" width="10"> Git
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-icon.svg" alt="" width="10"> GitHub
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/visual-studio-code-icon.svg" alt="" width="10"> Visual Studio Code
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/pycharm-icon.svg" alt="" width="10"> PyCharm
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/html-icon.png" alt="" width="10"> HTML
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/file-and-folder-type/css-file-format-icon.png" alt="" width="10"> CSS
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/javascript-programming-language-icon.png" alt="" width="10"> JavaScript
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/python-programming-language-icon.svg" alt="" width="10"> Python
- <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/django-icon.svg" alt="" width="10"> Framework Django

## Installation
Pour installer le projet, il vous suffit de cloner le dépôt GitHub en utilisant la commande suivante dans votre terminal :

```bash
git clone https://github.com/DevKKF/eden_2.git
```
Ensuite, naviguez dans le répertoire du projet :

Ouvrez l'application principal `eden` créé votre fichier de configuration 
```bash
.env
```
Copiez le code suivant dans le fichier `.env` :

```plaintext
SECRET_KEY='Cle secret de votre application'
DEBUG=True
MFA=False
NAME_APP="VASES D'HONNEUR CENTRE INFLUENCE EDEN 2"
VERSION_APP="1.0.0"
BASE='PREPROD'
ENVIRONMENT='DEV'
ALLOWED_HOSTS='127.0.0.1'


SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


DATABASE_HOST='127.0.0.1'
DATABASE_NAME='Nom de la base de données'
DATABASE_USER='root'
DATABASE_PWD='Mot de passe de votre base de données'
DATABASE_PORT='3306'


EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER='Votre mail'
EMAIL_HOST_PASSWORD='Mot de passe de votre mail'
DEFAULT_FROM_EMAIL=${EMAIL_HOST_USER}
DEFAULT_FROM_NAME_APP="VASES D'HONNEUR CENTRE INFLUENCE EDEN 2"
```

Ensuite, installez les dépendances nécessaires en utilisant pip :

```bash
pip install -r requirements.txt
```

Après avoir créé le fichier `.env` et avoir installé les dépendances, vous devez configurer la base de données. Assurez-vous d'avoir installé `MySQL` ou `MariaDB` ou encore `PostgreSQL` et créez une base de données avec le nom que vous avez spécifié dans le fichier `.env`.
Exécutez les migrations pour créer les tables nécessaires dans la base de données :

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed
python manage.py generate_error_pages
```
La commande `makemigrations` crée les migrations nécessaires pour les modèles définis dans votre application, tandis que `migrate` applique ces migrations à la base de données. La commande `seed` permet de remplir la base de données avec des données initiales, et `generate_error_pages` génère les pages d'erreur personnalisées.

Enfin, vous pouvez démarrer le serveur de développement Django avec la commande suivante :

```bash
python manage.py runserver
```
