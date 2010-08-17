from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

VISTAS = 'asesorias.vistas.'

# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^asesorias/asesor/$', 'asesorias.views.asesor',
        name='vista_asesor'),

    url(r'^asesorias/alumno/$', 'asesorias.views.alumno',
        name='vista_alumno'),

    (r'^asesorias/administrador/',
        include('asesorias.urls.administradorPrincipal')),

    (r'^asesorias/centro/',
        include('asesorias.urls.centro')),

    (r'^asesorias/administradorCentro/',
        include('asesorias.urls.administradorCentro')),

    (r'^asesorias/titulacion/',
        include('asesorias.urls.titulacion')),

    (r'^asesorias/asignatura/',
        include('asesorias.urls.asignatura')),

    (r'^asesorias/asignaturaCursoAcademico/',
        include('asesorias.urls.asignaturaCursoAcademico')),

    (r'^asesorias/departamento/',
        include('asesorias.urls.departamento')),

    (r'^asesorias/asesor/',
        include('asesorias.urls.asesor')),

    (r'^asesorias/asesorCursoAcademico/',
        include('asesorias.urls.asesorCursoAcademico')),

    (r'^asesorias/plantillaEntrevistaAsesor/',
        include('asesorias.urls.plantillaEntrevistaAsesor')),

    (r'^asesorias/preguntaAsesor/',
        include('asesorias.urls.preguntaAsesor')),

    (r'^asesorias/alumno/',
        include('asesorias.urls.alumno')),

    (r'^asesorias/alumnoCursoAcademico/',
        include('asesorias.urls.alumnoCursoAcademico')),

    (r'^asesorias/matricula/',
        include('asesorias.urls.matricula')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasCalificacionConvocatoria',
    url(r'^asesorias/calificacionConvocatoria/add/$',
        'addCalificacionConvocatoria',
        name='addCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/edit/$',

        'editCalificacionConvocatoria',
        name='editCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/del/$',

        'delCalificacionConvocatoria',
        name='delCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/list/$',
        'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasPlantillaEntrevistaOficial',
    url(r'^asesorias/plantillaEntrevistaOficial/add/$',
        'addPlantillaEntrevistaOficial',
        name='addPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/edit/$',

        'editPlantillaEntrevistaOficial',
        name='editPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/del/$',

        'delPlantillaEntrevistaOficial',
        name='delPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/list/$',
        'listPlantillaEntrevistaOficial',
        name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns(VISTAS + 'vistasPreguntaOficial',
    url(r'^asesorias/preguntaOficial/add/$',
        'addPreguntaOficial', name='addPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/edit/$',

        'editPreguntaOficial', name='editPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/del/$',

        'delPreguntaOficial', name='delPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/list/$',
        'listPreguntaOficial', name='listPreguntaOficial'),
)

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns += patterns(VISTAS + 'vistasReunion',
    url(r'^asesorias/reunion/add/$',
        'addReunion', name='addReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        'editReunion', name='editReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        'delReunion', name='delReunion'),

    url(r'^asesorias/reunion/list/$',
        'listReunion', name='listReunion'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasCentro_administradorCentro',
    url(r'^asesorias/centro_administradorCentro/add/' +
        '(?P<nombre_centro>[\s\w]*)/$',

        'addCentro_administradorCentro',
        name='addCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/edit/$',

        'editCentro_administradorCentro',
        name='editCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/del/$',

        'delCentro_administradorCentro',
        name='delCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/list/' +
        '(?P<centro>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listCentro_administradorCentro',
        name='listCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/select/$',
        'selectCentro',
        name='selectCentro_CentroAdministradorCentro'),

    url(r'^asesorias/centro_administradorCentro/generarPDF/' +
        '(?P<centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaCentros_administradorCentro',
        name='generarPDFListaCentros_administradorCentro'),
)

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasReunion_preguntaAsesor',
    url(r'^asesorias/reunion_preguntaAsesor/add/$',
        'addReunion_preguntaAsesor',
        name='addReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'edit/$',

        'editReunion_preguntaAsesor',
        name='editReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'del/$',

        'delReunion_preguntaAsesor',
        name='delReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/list/$',
        'listReunion_preguntaAsesor',
        name='listReunion_preguntaAsesor'),
)
