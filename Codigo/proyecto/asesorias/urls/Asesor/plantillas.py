from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasPlantillas',
    url(r'^listPlantillasOficiales/$',
        'listPlantillasOficiales',
        name='listPlantillasOficiales_Asesor'),
)
