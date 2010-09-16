from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasInformacionPersonal',
    url(r'^show/$',
        'showInfo', name='showInfo_Asesor'),
)
