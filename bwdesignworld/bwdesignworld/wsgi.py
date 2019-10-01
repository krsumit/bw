"""
WSGI config for bwhr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import site
sys.path.append('/var/www/html/bwdesignworld/bwdesignworld/bwdesignworld')
sys.path.append('/var/www/html/bwdesignworld/bwdesignworld')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bwdesignworld.settings")
from django.core.wsgi import get_wsgi_application



application = get_wsgi_application()
