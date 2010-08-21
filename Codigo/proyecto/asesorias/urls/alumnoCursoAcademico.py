from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAlumnoCursoAcademico',
    url(r'^add/(?P<dni_pasaporte>[\s\w]*)/$',
        'addAlumnoCursoAcademico', name='addAlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$',

        'editAlumnoCursoAcademico', name='editAlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$',

        'delAlumnoCursoAcademico', name='delAlumnoCursoAcademico'),

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),

    url(r'^selectAlumno/$',
        'selectAlumno', name='selectAlumno_AlumnoCursoAcademico'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAlumnosCursoAcademico',
        name='generarPDFListaAlumnosCursoAcademico'),
)
