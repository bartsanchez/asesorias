from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.AdministradorCentro.'

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasAdministradorCentro',

    ### URLS del menu horizontal. ###

    url(r'^$', 'administradorCentro_inicio',
        name='administradorCentro_inicio'),

    url(r'^organizacion_institucional/$',
        'administradorCentro_org_institucional',
        name='administradorCentro_org_institucional'),

    url(r'^organizacion_docente/$',
        'administradorCentro_org_docente',
        name='administradorCentro_org_docente'),

    url(r'^alumnos/$',
        'administradorCentro_alumnos',
        name='administradorCentro_alumnos'),

    url(r'^reuniones/$',
        'administradorCentro_reuniones',
        name='administradorCentro_reuniones'),

    url(r'^plantillas/$',
        'administradorCentro_plantillas',
        name='administradorCentro_plantillas'),

    ### Includes a cada entidad ###

    (r'^titulacion/',
        include(URLS + 'titulacion')),

    (r'^asignatura/',
        include(URLS + 'asignatura')),

    (r'^asignaturaCursoAcademico/',
        include(URLS + 'asignaturaCursoAcademico')),

    #(r'^departamento/',
        #include(URLS + 'departamento')),

    #(r'^asesor/',
        #include(URLS + 'asesor')),

    #(r'^asesorCursoAcademico/',
        #include(URLS + 'asesorCursoAcademico')),

    #(r'^plantillaEntrevistaAsesor/',
        #include(URLS + 'plantillaEntrevistaAsesor')),

    #(r'^preguntaAsesor/',
        #include(URLS + 'preguntaAsesor')),

    #(r'^alumno/',
        #include(URLS + 'alumno')),

    #(r'^alumnoCursoAcademico/',
        #include(URLS + 'alumnoCursoAcademico')),

    #(r'^matricula/',
        #include(URLS + 'matricula')),

    #(r'^calificacionConvocatoria/',
        #include(URLS + 'calificacionConvocatoria')),

    #(r'^plantillaEntrevistaOficial/',
        #include(URLS + 'plantillaEntrevistaOficial')),

    #(r'^preguntaOficial/',
        #include(URLS + 'preguntaOficial')),

    #(r'^reunion/',
        #include(URLS + 'reunion')),

    #(r'^centro_administradorCentro/',
        #include(URLS + 'centro_administradorCentro')),

    #(r'^reunion_preguntaAsesor/',
        #include(URLS + 'reunion_preguntaAsesor')),

    #(r'^reunion_preguntaOficial/',
        #include(URLS + 'reunion_preguntaOficial')),
)
