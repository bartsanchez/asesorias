from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ----------------------------------- #
# Url's de reunion - pregunta oficial #
# ----------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion_preguntaOficial',
    url(r'^add/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/$',

        'addReunion_preguntaOficial',
        name='addReunion_preguntaOficial'),

    url(r'^selectAsesor/(?P<tipo>[\s\w]+)/$',
        'selectAsesor', name='selectAsesor_Reunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAsesorCursoAcademico/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectAsesorCursoAcademico',
        name='selectAsesorCA_Reunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/(?P<tipo>[\s\w]+)/$',

        'selectAlumno', name='selectAlumno_Reunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/'+
        'selectReunion/(?P<tipo>[\s\w]+)/$',

        'selectReunion', name='selectReunion_Reunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/selectEntrevistaOficial/$',

        'selectEntrevistaOficial',
        name='selectEntrevistaOficial_Reunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>\d+)/' +
        'selectPreguntaOficial/$',

        'selectPreguntaOficial',
        name='selectPreguntaOficial_Reunion_preguntaOficial'),
)
