import os

DEBUG = os.getenv('DEBUG', False)
CSRF_ENABLED = os.getenv('CSRF_ENABLED', True)
CACHE_MOVIES_TIMEOUT = os.getenv('CACHE_MOVIES_TIMEOUT', 43200)
