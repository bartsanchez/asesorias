from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasPlantillas',
    url(r'^listPlantillasOficiales/(?P<orden>[\s\w]*)/$',
        'listPlantillasOficiales',
        name='listPlantillasOficiales_Asesor'),

    url(r'^generarPDF/plantillasOficiales/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPlantillasEntrevistaOficial',
        name='generarPDFListaPlantillasEntrevistaOficial_Asesor'),

    url(r'^listPreguntasOficiales/(?P<entrevista_oficial>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listPreguntaOficial', name='listPreguntaOficial_Asesor'),

    url(r'^generarPDF/preguntasOficiales/' +
        '(?P<entrevista_oficial>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPreguntasOficiales',
        name='generarPDFListaPreguntasOficiales_Asesor'),

    url(r'^listPlantillasAsesor/(?P<orden>[\s\w]*)/$',
        'listPlantillasAsesor',
        name='listPlantillasAsesor_Asesor'),

    url(r'^generarPDF/plantillasAsesor/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPlantillasEntrevistaAsesor',
        name='generarPDFListaPlantillasEntrevistaAsesor_Asesor'),
)
