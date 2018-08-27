# encoding: utf-8
import os
import dj_database_url

#
# This project variables
#
TWITTER_C_KEY = os.environ.get('TWITTER_C_KEY')
TWITTER_C_SECRET = os.environ.get('TWITTER_C_SECRET')
TWITTER_A_TOKEN = os.environ.get('TWITTER_A_TOKEN')
TWITTER_A_TOKEN_SECRET = os.environ.get('TWITTER_A_TOKEN_SECRET')

#
# Core configuration
#

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  # Disable Django's own staticfiles handling in favour of WhiteNoise, for
  # greater consistency between gunicorn and `./manage.py runserver`. See:
  # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
  'whitenoise.runserver_nostatic',
  'django.contrib.staticfiles',

  'django.contrib.humanize',

  'virkamiesbot',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
]

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wsgi.application'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#
# Database
#

is_windows = os.name == 'nt'

if is_windows:
  DEFAULT_DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
else:
  DEFAULT_DATABASE_URL = 'sqlite:////' + os.path.join(BASE_DIR, 'database.db')

DATABASES = {
  'default': dj_database_url.config(default=DEFAULT_DATABASE_URL),
}


#
# Internationalization
#

LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#
# Static files
#

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'..', 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


try:
  from local_settings import *
except ImportError:
  pass