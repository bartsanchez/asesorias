from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasCalificacionConvocatoria',
    url(r'^add/$',
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

    url(r'^list/$',
        'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria'),
)
