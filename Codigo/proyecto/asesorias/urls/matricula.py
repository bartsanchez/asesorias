from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns = patterns(VISTAS + 'vistasMatricula',
    url(r'^add/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/$',

        'addMatricula', name='addMatricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/edit/$',

        'editMatricula', name='editMatricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/del/$',

        'delMatricula', name='delMatricula'),

    url(r'^list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listMatricula', name='listMatricula'),

    url(r'^select/$',
        'selectAsignaturaOAlumnoCursoAcademico',
        name='selectAsignaturaOAlumnoCursoAcademico'),

    url(r'^selectCentro/(?P<tipo>[\s\w]+)/$',
        'selectCentro', name='selectCentro_Matricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion', name='selectTitulacion_Matricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura', name='selectAsignatura_Matricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCursoAcademico_Matricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/$',

        'selectAlumno', name='selectAlumno_Matricula'),

    url(r'^generarPDF/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaMatriculas', name='generarPDFListaMatriculas'),
)
