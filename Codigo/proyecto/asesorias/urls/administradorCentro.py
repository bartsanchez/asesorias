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

    url(r'^informacion_personal/$',

        'administradorCentro_informacion_personal',
        name='administradorCentro_informacion_personal'),

    url(r'^organizacion_institucional/$',
        'administradorCentro_org_institucional',
        name='administradorCentro_org_institucional'),

    url(r'^organizacion_docente/$',
        'administradorCentro_org_docente',
        name='administradorCentro_org_docente'),

    ### Includes a cada entidad ###
    (r'^info/',
        include(URLS + 'informacionPersonal')),

    (r'^titulacion/',
        include(URLS + 'titulacion')),

    (r'^asignatura/',
        include(URLS + 'asignatura')),

    (r'^asignaturaCursoAcademico/',
        include(URLS + 'asignaturaCursoAcademico')),

    (r'^asesorCursoAcademico/',
        include(URLS + 'asesorCursoAcademico')),

    (r'^alumnoCursoAcademico/',
        include(URLS + 'alumnoCursoAcademico')),

    (r'^matricula/',
        include(URLS + 'matricula')),

    (r'^calificacionConvocatoria/',
        include(URLS + 'calificacionConvocatoria')),
)
