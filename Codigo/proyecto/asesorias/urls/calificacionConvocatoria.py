from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasCalificacionConvocatoria',
    url(r'^add/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)$',

        'addCalificacionConvocatoria',
        name='addCalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/edit/$',

        'editCalificacionConvocatoria',
        name='editCalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/del/$',

        'delCalificacionConvocatoria',
        name='delCalificacionConvocatoria'),

    url(r'^list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria'),

    url(r'^selectCentro/(?P<tipo>[\s\w]+)/$',
        'selectCentro', name='selectCentro_CalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_CalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura',
        name='selectAsignatura_CalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCA_CalificacionConvocatoria'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/(?P<tipo>[\s\w]+)/$',

        'selectAlumno', name='selectAlumno_CalificacionConvocatoria'),
)
