from .base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR / "staticfiles")

ASGI_APPLICATION = 'jo.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME_PROD'),
        'USER': config('DB_USER_PROD'),
        'PASSWORD': config('DB_PASSWORD_PROD'),
        'HOST': config('DB_HOST_PROD'),
        'PORT': config('DB_PORT_PROD'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False