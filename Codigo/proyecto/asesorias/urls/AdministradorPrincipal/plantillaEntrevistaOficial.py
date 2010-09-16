from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasPlantillaEntrevistaOficial',
    url(r'^add/$',
        'addPlantillaEntrevistaOficial',
        name='addPlantillaEntrevistaOficial'),

    url(r'^(?P<id_entrevista_oficial>[\s\w]+)/edit/$',

        'editPlantillaEntrevistaOficial',
        name='editPlantillaEntrevistaOficial'),

    url(r'^(?P<id_entrevista_oficial>[\s\w]+)/del/$',

        'delPlantillaEntrevistaOficial',
        name='delPlantillaEntrevistaOficial'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listPlantillaEntrevistaOficial',
        name='listPlantillaEntrevistaOficial'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaPlantillasEntrevistaOficial',
        name='generarPDFListaPlantillasEntrevistaOficial'),
)

