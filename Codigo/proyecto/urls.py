from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.'

# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^asesorias/asesor/$', 'asesorias.views.asesor',
        name='vista_asesor'),

    url(r'^asesorias/alumno/$', 'asesorias.views.alumno',
        name='vista_alumno'),

    (r'^asesorias/administradorPrincipal/',
        include(URLS + 'administradorPrincipal')),

    (r'^asesorias/administradorPrincipal/centro/',
        include(URLS + 'centro')),

    (r'^asesorias/administradorPrincipal/administradorCentro/',
        include(URLS + 'administradorCentro')),

    (r'^asesorias/administradorPrincipal/titulacion/',
        include(URLS + 'titulacion')),

    (r'^asesorias/administradorPrincipal/asignatura/',
        include(URLS + 'asignatura')),

    (r'^asesorias/administradorPrincipal/asignaturaCursoAcademico/',
        include(URLS + 'asignaturaCursoAcademico')),

    (r'^asesorias/administradorPrincipal/departamento/',
        include(URLS + 'departamento')),

    (r'^asesorias/administradorPrincipal/asesor/',
        include(URLS + 'asesor')),

    (r'^asesorias/administradorPrincipal/asesorCursoAcademico/',
        include(URLS + 'asesorCursoAcademico')),

    (r'^asesorias/administradorPrincipal/plantillaEntrevistaAsesor/',
        include(URLS + 'plantillaEntrevistaAsesor')),

    (r'^asesorias/administradorPrincipal/preguntaAsesor/',
        include(URLS + 'preguntaAsesor')),

    (r'^asesorias/administradorPrincipal/alumno/',
        include(URLS + 'alumno')),

    (r'^asesorias/administradorPrincipal/alumnoCursoAcademico/',
        include(URLS + 'alumnoCursoAcademico')),

    (r'^asesorias/administradorPrincipal/matricula/',
        include(URLS + 'matricula')),

    (r'^asesorias/administradorPrincipal/calificacionConvocatoria/',
        include(URLS + 'calificacionConvocatoria')),

    (r'^asesorias/administradorPrincipal/plantillaEntrevistaOficial/',
        include(URLS + 'plantillaEntrevistaOficial')),

    (r'^asesorias/administradorPrincipal/preguntaOficial/',
        include(URLS + 'preguntaOficial')),

    (r'^asesorias/administradorPrincipal/reunion/',
        include(URLS + 'reunion')),

    (r'^asesorias/administradorPrincipal/centro_administradorCentro/',
        include(URLS + 'centro_administradorCentro')),

    (r'^asesorias/administradorPrincipal/reunion_preguntaAsesor/',
        include(URLS + 'reunion_preguntaAsesor')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
