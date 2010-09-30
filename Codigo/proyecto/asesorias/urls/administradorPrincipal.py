from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.AdministradorPrincipal.'

# -------------------------------- #
# Url's de administrador principal #
# -------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAdministradorPrincipal',

    ### URLS del menu horizontal. ###

    url(r'^$', 'administrador_inicio', name='administrador_inicio'),

    url(r'^organizacion_institucional/$',
        'administrador_org_institucional',
        name='administrador_org_institucional'),

    url(r'^organizacion_docente/$',
        'administrador_org_docente', name='administrador_org_docente'),

    url(r'^alumnos/$',
        'administrador_alumnos', name='administrador_alumnos'),

    url(r'^reuniones/$',
        'administrador_reuniones', name='administrador_reuniones'),

    url(r'^plantillas/$',
        'administrador_plantillas', name='administrador_plantillas'),

    ### Includes a cada entidad ###

    (r'^centro/',
        include(URLS + 'centro')),

    (r'^administradorCentro/',
        include(URLS + 'administradorCentro')),

    (r'^titulacion/',
        include(URLS + 'titulacion')),

    (r'^asignatura/',
        include(URLS + 'asignatura')),

    (r'^asignaturaCursoAcademico/',
        include(URLS + 'asignaturaCursoAcademico')),

    (r'^departamento/',
        include(URLS + 'departamento')),

    (r'^asesor/',
        include(URLS + 'asesor')),

    (r'^asesorCursoAcademico/',
        include(URLS + 'asesorCursoAcademico')),

    (r'^plantillaEntrevistaAsesor/',
        include(URLS + 'plantillaEntrevistaAsesor')),

    (r'^preguntaAsesor/',
        include(URLS + 'preguntaAsesor')),

    (r'^alumno/',
        include(URLS + 'alumno')),

    (r'^alumnoCursoAcademico/',
        include(URLS + 'alumnoCursoAcademico')),

    (r'^matricula/',
        include(URLS + 'matricula')),

    (r'^calificacionConvocatoria/',
        include(URLS + 'calificacionConvocatoria')),

    (r'^plantillaEntrevistaOficial/',
        include(URLS + 'plantillaEntrevistaOficial')),

    (r'^preguntaOficial/',
        include(URLS + 'preguntaOficial')),

    (r'^reunion/',
        include(URLS + 'reunion')),

    (r'^centro_administradorCentro/',
        include(URLS + 'centro_administradorCentro')),

    (r'^reunion_preguntaAsesor/',
        include(URLS + 'reunion_preguntaAsesor')),

    (r'^reunion_preguntaOficial/',
        include(URLS + 'reunion_preguntaOficial')),
)
