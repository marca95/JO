from .base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = ['https://jo-2024-cb5ee4d6122b.herokuapp.com']

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
]

# Si j'utilise ASGI 
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ASGI_APPLICATION = 'jo.asgi.application'
SESSION_ENGINE = "django.contrib.sessions.backends.db"

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

SESSION_COOKIE_SECURE = True