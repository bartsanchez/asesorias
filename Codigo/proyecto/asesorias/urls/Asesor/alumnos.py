from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasAlumno',
    url(r'^showAlumnos/(?P<orden>[\s\w]*)/$',
        'showAlumnos', name='showAlumnos_Asesor'),

    url(r'^showAlumno/(?P<dni_pasaporte>[\s\w]+)/$',

        'showAlumno', name='showAlumno_Asesor'),

    url(r'show/generarPDF/$',
        'generarPDFListaAlumnos', name='generarPDFListaAlumnos_Asesor'),
)
