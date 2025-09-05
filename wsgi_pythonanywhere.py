"""
WSGI configuration file for PythonAnywhere deployment.
This file should be uploaded to PythonAnywhere and configured as the WSGI file.
"""

import os
import sys

# Add the project directory to the sys.path
path = '/home/zintan/kokore-app'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to use production settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'dictionary.settings_production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
