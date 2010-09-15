from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsignaturaCursoAcademico',
    url(r'^add/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/$',

        'addAsignaturaCursoAcademico',
        name='addAsignaturaCursoAcademico'),

    url(r'^' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        'editAsignaturaCursoAcademico',
        name='editAsignaturaCursoAcademico'),

    url(r'^' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        'delAsignaturaCursoAcademico',
        name='delAsignaturaCursoAcademico'),

    url(r'^list/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listAsignaturaCursoAcademico',
        name='listAsignaturaCursoAcademico'),

    url(r'^selectCentro/(?P<tipo>[\s\w]+)/$',

        'selectCentro',
        name='selectCentro_AsignaturaCursoAcademico'),

    url(r'^(?P<nombre_centro>[\s\w]+)/selectTitulacion/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_AsignaturaCursoAcademico'),

    url(r'^(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura',
        name='selectAsignatura_AsignaturaCursoAcademico'),

    url(r'generarPDF/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsignaturasCursoAcademico',
        name='generarPDFListaAsignaturasCursoAcademico'),
)
