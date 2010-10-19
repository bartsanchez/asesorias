from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasCalificacionConvocatoria',
    url(r'^add/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)$',

        'addCalificacionConvocatoria',
        name='addCalificacionConvocatoria_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/edit/$',

        'editCalificacionConvocatoria',
        name='editCalificacionConvocatoria_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/del/$',

        'delCalificacionConvocatoria',
        name='delCalificacionConvocatoria_administradorCentro'),

    url(r'^list/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/'+
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria_administradorCentro'),

    url(r'^selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_CalificacionConvocatoria' +
        '_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura',
        name='selectAsignatura_CalificacionConvocatoria' +
        '_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCA_CalificacionConvocatoria' +
        '_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/(?P<tipo>[\s\w]+)/$',

        'selectAlumno', name='selectAlumno_CalificacionConvocatoria' +
        '_administradorCentro'),

    url(r'^generarPDF/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaCalificacionesConvocatoria',
        name='generarPDFListaCalificacionesConvocatoria' +
        '_administradorCentro'),
)
