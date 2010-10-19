from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns = patterns(VISTAS + 'vistasMatricula',
    url(r'^add/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)$',

        'addMatricula', name='addMatricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/edit/$',

        'editMatricula', name='editMatricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/_edit/$',

        'editMatricula2', name='editMatricula2'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/del/$',

        'delMatricula', name='delMatricula'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/_del/$',

        'delMatricula2', name='delMatricula2'),

    url(r'^list/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/'+
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listMatricula', name='listMatricula_administradorCentro'),

    url(r'^selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_Matricula_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura',
        name='selectAsignatura_Matricula_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCursoAcademico_Matricula' +
        '_administradorCentro'),

    url(r'^generarPDF/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaMatriculas', name='generarPDFListaMatriculas'),

    url(r'^_generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaMatriculas2',name='generarPDFListaMatriculas2'),
)
