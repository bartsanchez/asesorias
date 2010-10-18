from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAlumnoCursoAcademico',
    url(r'^(?P<curso_academico>\d+)/(?P<orden>[\s\w]*)/list/$',

        'listAlumnoCursoAcademico',
        name='listAlumnoCursoAcademico_administradorCentro'),

    url(r'^selectCursoAcademico/$',
        'selectCursoAcademico',
        name='selectCursoAcademico_AlumnoCursoAcademico' +
        '_administradorCentro'),

    url(r'^generarPDF/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAlumnosCursoAcademico',
        name='generarPDFListaAlumnosCursoAcademico' +
        '_administradorCentro'),
)
