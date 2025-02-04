import os
from waitress import serve
from jo.wsgi import application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jo.settings.production')

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=8000)
