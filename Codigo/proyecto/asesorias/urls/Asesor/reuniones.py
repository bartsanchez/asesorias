from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasReuniones',
    url(r'^selectAlumno/$',
        'selectAlumno', name='selectAlumno_Asesor'),

    url(r'^addReunion/(?P<dni_pasaporte>[\s\w]+)/$',
        'addReunion', name='addReunion_Asesor'),

    url(r'^delReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'delReunion', name='delReunion_Asesor'),

    url(r'^listReunion/(?P<orden>[\s\w]*)/$',
        'listReunion', name='listReunion_Asesor'),

    url(r'^showReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'showReunion', name='showReunion_Asesor'),

    url(r'^addPlantillaAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista>\d*)/' +
        '(?P<tipo>[\s\w]*)/$',

        'addPlantillaAReunion', name='addPlantillaAReunion'),

    url(r'^addPlantillaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/$',

        'addPlantillaOficialAReunion',
        name='addPlantillaOficialAReunion'),

    url(r'^addPlantillaAsesorAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_asesor>[\s\w]+)/$',

        'addPlantillaAsesorAReunion',
        name='addPlantillaAsesorAReunion'),

    url(r'^addPreguntaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'addPreguntaOficialAReunion',
        name='addPreguntaOficialAReunion'),

    url(r'^delPreguntaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'delPreguntaOficialAReunion',
        name='delPreguntaOficialAReunion'),

    url(r'^delPreguntaAsesorAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'delPreguntaAsesorAReunion',
        name='delPreguntaAsesorAReunion'),
)
