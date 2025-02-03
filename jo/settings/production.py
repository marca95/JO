from .base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = ['*']

STATIC_ROOT = BASE_DIR / "staticfiles"

ASGI_APPLICATION = 'jo.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nom_base_production',
        'USER': 'utilisateur_production',
        'PASSWORD': 'mot_de_passe_production',
        'HOST': 'adresse_serveur',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False