import os
import sys

# Menambahkan direktori saat ini ke sys.path agar module project terbaca
sys.path.insert(0, os.path.dirname(__file__))

# Arahkan ke file settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'websman11.settings'

# Import application dari wsgi.py
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
