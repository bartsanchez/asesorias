from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns = patterns(VISTAS + 'vistasPreguntaOficial',
    url(r'^add/$',
        'addPreguntaOficial', name='addPreguntaOficial'),

    url(r'^(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/edit/$',

        'editPreguntaOficial', name='editPreguntaOficial'),

    url(r'^(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/del/$',

        'delPreguntaOficial', name='delPreguntaOficial'),

    url(r'^list/$',
        'listPreguntaOficial', name='listPreguntaOficial'),
)
