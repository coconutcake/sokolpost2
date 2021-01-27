from django.conf import settings
import os

DB = getattr(settings, 'DATABASES')
SETTINGS_CWD = getattr(settings, 'CWD')
APPCONFIG_CWD = os.path.realpath(__file__)
DATABASE_CWD = getattr(settings, 'DATABASE_CWD')