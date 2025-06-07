"""
WSGI config for FirstProjecct project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FirstProjecct.settings')
# Naming is really important here, the FirstProjecct beside the settings should be a name describing your project. this is the outer name that should describe what the app does. 

application = get_wsgi_application()
