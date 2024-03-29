from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasPlantillaEntrevistaAsesor',
    url(r'^add/(?P<dni_pasaporte>[\s\w]*)/' +
        '(?P<curso_academico>[\s\w]*)/$',

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

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listPlantillaEntrevistaAsesor',
        name='listPlantillaEntrevistaAsesor'),

    url(r'^selectAsesor/(?P<tipo>[\s\w]+)/$',
        'selectAsesor', name='selectAsesor_PlantillaEntrevistaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAsesorCursoAcademico/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectAsesorCursoAcademico',
        name='selectAsesorCA_PlantillaEntrevistaAsesor'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPlantillasEntrevistaAsesor',
        name='generarPDFListaPlantillasEntrevistaAsesor'),
)
