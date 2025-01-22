from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# UTILE POUR LES FICHIERS STATIC 
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Si je veux envoyer des vrais mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'monzooarcadia@gmail.com'
EMAIL_HOST_PASSWORD = 'pbocfkwegsyuhplk'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False