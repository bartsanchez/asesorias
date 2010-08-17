from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion_preguntaAsesor',
    url(r'^add/$',
        'addReunion_preguntaAsesor',
        name='addReunion_preguntaAsesor'),

    url(r'^(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'edit/$',

        'editReunion_preguntaAsesor',
        name='editReunion_preguntaAsesor'),

    url(r'^(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'del/$',

        'delReunion_preguntaAsesor',
        name='delReunion_preguntaAsesor'),

    url(r'^list/$',
        'listReunion_preguntaAsesor',
        name='listReunion_preguntaAsesor'),
)
