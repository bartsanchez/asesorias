import os, sys

sys.path.append('/home/elbarto/pfc/Codigo/')
sys.path.append('/home/elbarto/pfc/Codigo/proyecto/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
