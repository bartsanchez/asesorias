import os, sys

sys.path.append('/ruta-proyecto/')
sys.path.append('/ruta-proyecto/proyecto/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
