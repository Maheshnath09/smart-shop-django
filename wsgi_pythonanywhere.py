"""
PythonAnywhere WSGI Configuration

Copy this content to your PythonAnywhere WSGI file.
Replace 'yourusername' with your actual PythonAnywhere username.
"""

import os
import sys

# Add your project directory to the sys.path
# IMPORTANT: Replace 'yourusername' with your PythonAnywhere username
project_home = '/home/yourusername/my_store'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
# Using production settings for PythonAnywhere
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_pythonanywhere'

# Load environment variables from .env file
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(project_home) / '.env'
load_dotenv(dotenv_path=env_path)

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
