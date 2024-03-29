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

    url(r'^(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/' +
        'edit/$',

        'editReunion_preguntaOficial',
        name='editReunion_preguntaOficial'),

    url(r'^(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/'+
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/' +
        'del/$',

        'delReunion_preguntaOficial',
        name='delReunion_preguntaOficial'),

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<orden>[\s\w]*)/$',

        'listReunion_preguntaOficial',
        name='listReunion_preguntaOficial'),

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

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaReuniones_preguntaOficial',
        name='generarPDFListaReuniones_preguntaOficial'),
)
