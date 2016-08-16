# Dummy Django settings
SECRET_KEY = 'dummy-key'

from autobreadcrumbs.settings import *

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'autobreadcrumbs',
)
