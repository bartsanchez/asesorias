from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasPlantillas',
    url(r'^listPlantillasOficiales/(?P<orden>[\s\w]*)/$',
        'listPlantillasOficiales',
        name='listPlantillasOficiales_Asesor'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaPlantillasEntrevistaOficial',
        name='generarPDFListaPlantillasEntrevistaOficial_Asesor'),

    url(r'^listPreguntasOficiales/(?P<entrevista_oficial>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listPreguntaOficial', name='listPreguntaOficial_Asesor'),
)
