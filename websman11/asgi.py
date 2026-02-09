"""
ASGI config for websman11 project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websman11.settings')

application = get_asgi_application()
