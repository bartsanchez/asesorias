from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Asesor.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasReuniones',

    # ------------- #
    # Ver reuniones #
    # ------------- #

    url(r'^selectAlumno/$',
        'selectAlumno', name='selectAlumno_Asesor'),

    url(r'^listReunion/(?P<orden>[\s\w]*)/$',
        'listReunion', name='listReunion_Asesor'),

    # ---------------------- #
    # Reuniones individuales #
    # ---------------------- #

    url(r'^addReunion/(?P<dni_pasaporte>[\s\w]+)/$',
        'addReunion', name='addReunion_Asesor'),

    url(r'^delReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'delReunion', name='delReunion_Asesor'),

    url(r'^determinarReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<fecha>[\s\w\-]+)/$',

        'determinarReunion',
        name='determinarReunion_Asesor'),

    url(r'^showReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/$',

        'showReunion', name='showReunion_Asesor'),

    # Plantillas individuales #

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


    # Preguntas individuales #

    url(r'^addPreguntaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'addPreguntaOficialAReunion',
        name='addPreguntaOficialAReunion'),

    url(r'^editRespuestaOficial/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'editRespuestaOficial',
        name='editRespuestaOficial_Asesor'),

    url(r'^delPreguntaOficialAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'delPreguntaOficialAReunion',
        name='delPreguntaOficialAReunion'),

    url(r'^addPreguntaAsesorAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'addPreguntaAsesorAReunion',
        name='addPreguntaAsesorAReunion'),

    url(r'^editRespuestaAsesor/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'editRespuestaAsesor',
        name='editRespuestaAsesor_Asesor'),

    url(r'^delPreguntaAsesorAReunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<id_reunion>\d+)/(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'delPreguntaAsesorAReunion',
        name='delPreguntaAsesorAReunion'),

    # ------------------ #
    # Reuniones grupales #
    # ------------------ #

    url(r'^addReunionGrupal/(?P<lista_alumnos>[\s\w\&]*)/$',
        'addReunionGrupal', name='addReunionGrupal_Asesor'),

    url(r'^delReunionGrupal/(?P<fecha>[\s\w\-]+)/$',
        'delReunionGrupal', name='delReunionGrupal_Asesor'),

    url(r'^addAlumnoAReunionGrupal/(?P<lista_alumnos>[\s\w\&]*)/' +
        '(?P<dni_pasaporte>[\s\w]+)/$',

        'addAlumnoAReunionGrupal', name='addAlumnoAReunionGrupal'),

    url(r'^delAlumnoAReunionGrupal/(?P<lista_alumnos>[\s\w\&]*)/' +
        '(?P<dni_pasaporte>[\s\w]+)/$',

        'delAlumnoAReunionGrupal', name='delAlumnoAReunionGrupal'),

    url(r'^showReunionGrupal/(?P<fecha>[\s\w\-]+)/$',
        'showReunionGrupal', name='showReunionGrupal_Asesor'),

    # Plantillas grupales #

    url(r'^addPlantillaAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista>\d*)/(?P<tipo>[\s\w]*)/$',

        'addPlantillaAReunionGrupal',
        name='addPlantillaAReunionGrupal'),

    url(r'^addPlantillaOficialAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/$',

        'addPlantillaOficialAReunionGrupal',
        name='addPlantillaOficialAReunionGrupal'),

    url(r'^addPlantillaAsesorAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_asesor>[\s\w]+)/$',

        'addPlantillaAsesorAReunionGrupal',
        name='addPlantillaAsesorAReunionGrupal'),

    # Preguntas grupales #

    url(r'^addPreguntaOficialAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'addPreguntaOficialAReunionGrupal',
        name='addPreguntaOficialAReunionGrupal'),

    url(r'^delPreguntaOficialAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'delPreguntaOficialAReunionGrupal',
        name='delPreguntaOficialAReunionGrupal'),

    url(r'^addPreguntaAsesorAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'addPreguntaAsesorAReunionGrupal',
        name='addPreguntaAsesorAReunionGrupal'),

    url(r'^delPreguntaAsesorAReunionGrupal/(?P<fecha>[\s\w\-]+)/' +
        '(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'delPreguntaAsesorAReunionGrupal',
        name='delPreguntaAsesorAReunionGrupal'),

    # Exportar a PDF #
    url(r'^generarPDF/reuniones/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaReuniones',
        name='generarPDFListaReuniones'),
)
