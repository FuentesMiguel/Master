import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
 
# https://www.psycopg.org/install/
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Basedatos',
        'USER': 'root',
        'PASSWORD': 'Me.182-f',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Sistema_Gestion',
        'USER': 'root',
        'PASSWORD': 'Me.182-f',
        'HOST': 'localhost',
        'PORT': '',
    }
}