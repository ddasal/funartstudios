"""
WSGI config for funartstudios project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import dotenv
import pathlib
from django.core.wsgi import get_wsgi_application

DOT_ENV_PATH = pathlib.Path() / '.env'
if DOT_ENV_PATH.exists():
    dotenv.read_dotenv(str(DOT_ENV_PATH))
else:
    print('No .env found, be sure to add it.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funartstudios.settings')

application = get_wsgi_application()
