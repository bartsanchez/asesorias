from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns = patterns(VISTAS + 'vistasPreguntaAsesor',
    url(r'^add/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>[\s\w]+)/(?P<entrevista_asesor>[\s\w]+)/$',

        'addPreguntaAsesor', name='addPreguntaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/edit/$',

        'editPreguntaAsesor', name='editPreguntaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/del/$',

        'delPreguntaAsesor', name='delPreguntaAsesor'),

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<orden>[\s\w]+)/$',

        'listPreguntaAsesor', name='listPreguntaAsesor'),

    url(r'^selectAsesor/(?P<tipo>[\s\w]+)/$',
        'selectAsesor', name='selectAsesor_PreguntaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAsesorCursoAcademico/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectAsesorCursoAcademico',
        name='selectAsesorCA_PreguntaAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>[\s\w]+)/' +
        'selectAsesorCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectPlantillaEntrevistaAsesor',
        name='selectPEA_PreguntaAsesor'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
    '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
    '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaPreguntasAsesor',
        name='generarPDFListaPreguntasAsesor'),
)
