from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasPlantillaEntrevistaAsesor',
    url(r'^add/$',
        'addPlantillaEntrevistaAsesor',
        name='addPlantillaEntrevistaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/edit/$',

        'editPlantillaEntrevistaAsesor',
        name='editPlantillaEntrevistaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/del/$',

        'delPlantillaEntrevistaAsesor',
        name='delPlantillaEntrevistaAsesor'),

    url(r'^list/$',
        'listPlantillaEntrevistaAsesor',
        name='listPlantillaEntrevistaAsesor'),
)
