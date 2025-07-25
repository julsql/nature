"""
Django's settings for config project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '51.222.136.185', 'speciarium.julsql.fr', 'www.speciarium.julsql.fr', 'nature']

# Application definition

INSTALLED_APPS = [
    "daphne",
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'main/core/frontend/advanced_search/templates',
            BASE_DIR / 'main/core/frontend/advanced_search_result/templates',
            BASE_DIR / 'main/core/frontend/table/templates',
            BASE_DIR / 'main/core/frontend/login/templates',
            BASE_DIR / 'main/core/frontend/home/templates',
            BASE_DIR / 'main/core/frontend/errors/templates',
            BASE_DIR / 'main/core/frontend/upload_images/templates',
            BASE_DIR / 'main/core/frontend/carte/templates',
            BASE_DIR / 'main/core/frontend/photos/templates',
            BASE_DIR / 'main/core/frontend/profile/templates',
            BASE_DIR / 'main/core/frontend/auth/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'config.asgi.application'

ENV = config('DJANGO_ENV')
# Configurer le Channel Layer en fonction de l'environnement
if ENV == 'production':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [('redis', 6379)],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_DB = config('POSTGRES_DB')

if config('DJANGO_ENV') == 'production':
    db_host = 'postgres'
else:
    db_host = "localhost"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': db_host,
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CSRF_TRUSTED_ORIGINS = [
    'https://speciarium.julsql.fr',  # Remplacez par votre domaine de production
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr'

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

APPEND_SLASH = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'main.AppUser'
AUTHENTICATION_FAILURE = _(
    'Veuillez entrer un nom d\'utilisateur et un mot de passe valides. Notez que les deux champs peuvent être sensibles à la casse.')
LOGOUT_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'main' / 'static/'
LOGS_FILE = BASE_DIR / 'logs' / 'app.logs'

# Répertoire pour les fichiers uploadés
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Taille maximale de fichier en Mo (ici 200 Mo)
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # default 2621440 (i.e. 2.5 MB)

# Taille maximale d'un fichier de formulaire multipart (ici 200 Mo)
FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200  # default 2621440 (i.e. 2.5 MB)

DATA_UPLOAD_MAX_NUMBER_FILES = 1000  # default 100 files

CSRF_USE_SESSIONS = False  # Le cookie CSRF doit être envoyé séparément, pas stocké dans la session
CSRF_COOKIE_NAME = 'csrftoken'  # Nom du cookie (par défaut : 'csrftoken')
CSRF_COOKIE_HTTPONLY = False  # Le cookie doit être accessible par le client (Postman)
CSRF_COOKIE_SECURE = False  # Mettez `True` uniquement si vous utilisez HTTPS

DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')

if ENV == 'production':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
