from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasAlumno',
    url(r'^show/$',
        'showAlumnos', name='showAlumnos_Asesor'),
)
