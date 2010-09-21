from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasAlumno',
    url(r'^show/$',
        'showAlumnos', name='showAlumnos_Asesor'),

    url(r'^show/(?P<dni_pasaporte>[\s\w]+)/$',

        'showAlumno', name='showAlumno_Asesor'),
)
