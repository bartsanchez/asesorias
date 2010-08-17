from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns = patterns(VISTAS + 'vistasAlumno',
    url(r'^add/$',
        'addAlumno', name='addAlumno'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/edit/$',
        'editAlumno', name='editAlumno'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/del/$',
        'delAlumno', name='delAlumno'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listAlumno', name='listAlumno'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaAlumnos',
        name='generarPDFListaAlumnos'),
)
