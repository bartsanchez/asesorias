from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion',
    url(r'^add/(?P<dni_pasaporte>[\s\w]*)/' +
        '(?P<curso_academico>[\s\w]*)/$',

        'addReunion', name='addReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        'editReunion', name='editReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        'delReunion', name='delReunion'),

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listReunion', name='listReunion'),

    url(r'^selectAlumno/(?P<tipo>[\s\w]+)/$',
        'selectAlumno', name='selectAlumno_Reunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAlumnoCursoAcademico/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectAlumnoCursoAcademico',
        name='selectAlumnoCursoAcademico_Reunion'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaReuniones',
        name='generarPDFListaReuniones'),
)
