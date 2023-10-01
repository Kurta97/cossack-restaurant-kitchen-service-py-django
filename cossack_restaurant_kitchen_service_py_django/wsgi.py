"""
WSGI config for cossack_restaurant_kitchen_service_py_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "cossack_restaurant_kitchen_service_py_django.settings"
)

application = get_wsgi_application()
