"""
Based on:

https://devcenter.heroku.com/articles/getting-started-with-django
"""

from settings import *
import os


DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = {'default': dj_database_url.config() }

WSGI_APPLICATION = 'pdxtrees.wsgi_deploy.application'

SECRET_KEY = os.environ.get('SECRET_KEY')

AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID') 
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY') 

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)