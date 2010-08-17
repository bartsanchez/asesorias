from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsesorCursoAcademico',
    url(r'^add/' +
        '(?P<nombre_departamento>[\s\w]*)/(?P<dni_pasaporte>[\s\w]*)/$',

         'addAsesorCursoAcademico', name='addAsesorCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$',

        'editAsesorCursoAcademico', name='editAsesorCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$',

        'delAsesorCursoAcademico', name='delAsesorCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/list/$',

        'listAsesorCursoAcademico', name='listAsesorCursoAcademico'),

    url(r'^selectAsesor/$',
        'selectAsesor', name='selectAsesor_AsesorCursoAcademico'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsesoresCursoAcademico',
        name='generarPDFListaAsesoresCursoAcademico'),
)
