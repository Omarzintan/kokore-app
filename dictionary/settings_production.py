"""
Production settings for PythonAnywhere deployment.
This file contains settings specific to the production environment.
"""

import os
from .settings import *  # Import base settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts for PythonAnywhere
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']  # Replace with your actual PythonAnywhere username

# Database
# Use MySQL database on PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$kokore',  # Replace with your database name
        'USER': 'yourusername',  # Replace with your PythonAnywhere username
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),  # Set this in PythonAnywhere bash console
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',  # Replace with your MySQL host
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files configuration for PythonAnywhere
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
