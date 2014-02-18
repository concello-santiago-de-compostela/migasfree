# -*- coding: utf-8 -*-

from .migasfree import *
from .base import *
from .ajax_select import *

# development environment
TEMPLATE_DEBUG = DEBUG = True

MIGASFREE_DB_DIR = os.path.dirname(MIGASFREE_PROJECT_DIR)
MIGASFREE_REPO_DIR = os.path.join(MIGASFREE_PROJECT_DIR, 'repo')
MIGASFREE_KEYS_DIR = os.path.join(MIGASFREE_APP_DIR, 'keys')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MIGASFREE_DB_DIR, 'migasfree.db'),
    }
}

INSTALLED_APPS += ("debug_toolbar",)
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)