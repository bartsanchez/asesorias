from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ----------------------------------- #
# Url's de reunion - pregunta oficial #
# ----------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion_preguntaOficial',
    url(r'^selectAsesor/(?P<tipo>[\s\w]+)/$',
        'selectAsesor', name='selectAsesor_Reunion_preguntaOficial'),
)
