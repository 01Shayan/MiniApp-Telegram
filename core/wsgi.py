import os
from django.core.wsgi import get_wsgi_application
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
print("WSGI loaded")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
