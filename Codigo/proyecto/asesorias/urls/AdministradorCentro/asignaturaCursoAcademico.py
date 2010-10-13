from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsignaturaCursoAcademico',
    url(r'^add/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/$',

        'addAsignaturaCursoAcademico',
        name='addAsignaturaCursoAcademico_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        'editAsignaturaCursoAcademico',
        name='editAsignaturaCursoAcademico_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        'delAsignaturaCursoAcademico',
        name='delAsignaturaCursoAcademico_administradorCentro'),

    url(r'^list/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listAsignaturaCursoAcademico',
        name='listAsignaturaCursoAcademico_administradorCentro'),

    url(r'^selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_AsignaturaCursoAcademico' +
        '_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura',
        name='selectAsignatura_AsignaturaCursoAcademico' +
        '_administradorCentro'),

    url(r'generarPDF/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsignaturasCursoAcademico',
        name='generarPDFListaAsignaturasCursoAcademico' +
        '_administradorCentro'),
)
