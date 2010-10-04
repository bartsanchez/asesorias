from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasReuniones',
    url(r'^listReunion/(?P<orden>[\s\w]*)/$',
        'listReunion', name='listReunion_Asesor'),
)
