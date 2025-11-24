"""
ASGI config for Confectionery Catalog project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.settings.production')

application = get_asgi_application()
