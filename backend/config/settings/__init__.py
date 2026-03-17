"""
Settings package for Episteme.
Import the appropriate settings based on environment.
"""
import os

# Default to development if not specified
environment = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')

if environment == 'config.settings.production':
    from .production import *
else:
    from .development import *
