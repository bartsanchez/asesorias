from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsesorCursoAcademico',
    url(r'^(?P<curso_academico>\d+)/(?P<orden>[\s\w]*)/list/$',

        'listAsesorCursoAcademico',
        name='listAsesorCursoAcademico_administradorCentro'),

    url(r'^selectCursoAcademico/$',
        'selectCursoAcademico',
        name='selectCursoAcademico_AsesorCursoAcademico' +
        '_administradorCentro'),

    url(r'^generarPDF/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsesoresCursoAcademico',
        name='generarPDFListaAsesoresCursoAcademico' +
        '_administradorCentro'),
)
