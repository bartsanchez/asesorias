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

    url(r'^add/plantillasAsesor/$',

        'addPlantillaEntrevistaAsesor',
        name='addPlantillaEntrevistaAsesor_Asesor'),

    url(r'^plantillasAsesor/(?P<id_entrevista_asesor>\d+)/edit/$',

        'editPlantillaEntrevistaAsesor',
        name='editPlantillaEntrevistaAsesor_Asesor'),

    url(r'^plantillasAsesor/(?P<id_entrevista_asesor>\d+)/del/$',

        'delPlantillaEntrevistaAsesor',
        name='delPlantillaEntrevistaAsesor_Asesor'),

    url(r'^listPlantillasAsesor/(?P<orden>[\s\w]*)/$',
        'listPlantillasAsesor',
        name='listPlantillasAsesor_Asesor'),

    url(r'^generarPDF/plantillasAsesor/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPlantillasEntrevistaAsesor',
        name='generarPDFListaPlantillasEntrevistaAsesor_Asesor'),

    url(r'^add/preguntasAsesor/(?P<entrevista_asesor>[\s\w]+)/$',
        'addPreguntaAsesor', name='addPreguntaAsesor_Asesor'),

    url(r'^preguntasAsesor/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/edit/$',

        'editPreguntaAsesor', name='editPreguntaAsesor_Asesor'),

    url(r'^preguntasAsesor/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/del/$',

        'delPreguntaAsesor', name='delPreguntaAsesor_Asesor'),

    url(r'^listPreguntasAsesor/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<orden>[\s\w]+)/$',

        'listPreguntaAsesor', name='listPreguntaAsesor_Asesor'),

    url(r'^generarPDF/preguntasAsesor/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPreguntasAsesor',
        name='generarPDFListaPreguntasAsesor_Asesor'),
)
