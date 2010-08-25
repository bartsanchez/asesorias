from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns = patterns(VISTAS + 'vistasPreguntaOficial',
    url(r'^add/(?P<id_entrevista_oficial>[\s\w]*)/$',
        'addPreguntaOficial', name='addPreguntaOficial'),

    url(r'^(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/edit/$',

        'editPreguntaOficial', name='editPreguntaOficial'),

    url(r'^(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/del/$',

        'delPreguntaOficial', name='delPreguntaOficial'),

    url(r'^list/(?P<entrevista_oficial>[\s\w]+)/(?P<orden>[\s\w]*)/$',
        'listPreguntaOficial', name='listPreguntaOficial'),

    url(r'^select/$',
        'selectEntrevistaOficial',
        name='selectEntrevistaOficial_PreguntaOficial'),
)
