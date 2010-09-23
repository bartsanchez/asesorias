from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasPlantillas',
    url(r'^listPlantillasOficiales/(?P<orden>[\s\w]*)/$',
        'listPlantillasOficiales',
        name='listPlantillasOficiales_Asesor'),
)
