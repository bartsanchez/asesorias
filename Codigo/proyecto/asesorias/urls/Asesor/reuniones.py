from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasReuniones',
    url(r'^listReunion/(?P<orden>[\s\w]*)/$',
        'listReunion', name='listReunion_Asesor'),

    url(r'^showReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'showReunion', name='showReunion_Asesor'),

    url(r'^addPreguntaAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'addPreguntaAReunion', name='addPreguntaAReunion'),

    url(r'^addPreguntaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)$',

        'addPreguntaOficialAReunion',
        name='addPreguntaOficialAReunion'),
)
