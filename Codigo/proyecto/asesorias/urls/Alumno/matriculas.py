from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Alumno.'

# ------------------------#
# Url's de usuario alumno #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasMatriculas',
    url(r'^showMatriculacionActual/$',

        'showMatriculacionActual',
        name='showMatriculacionActual_Alumno'),
)
