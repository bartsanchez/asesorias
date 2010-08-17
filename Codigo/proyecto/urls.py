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

    (r'^asesorias/administrador/',
        include(URLS + 'administradorPrincipal')),

    (r'^asesorias/centro/',
        include(URLS + 'centro')),

    (r'^asesorias/administradorCentro/',
        include(URLS + 'administradorCentro')),

    (r'^asesorias/titulacion/',
        include(URLS + 'titulacion')),

    (r'^asesorias/asignatura/',
        include(URLS + 'asignatura')),

    (r'^asesorias/asignaturaCursoAcademico/',
        include(URLS + 'asignaturaCursoAcademico')),

    (r'^asesorias/departamento/',
        include(URLS + 'departamento')),

    (r'^asesorias/asesor/',
        include(URLS + 'asesor')),

    (r'^asesorias/asesorCursoAcademico/',
        include(URLS + 'asesorCursoAcademico')),

    (r'^asesorias/plantillaEntrevistaAsesor/',
        include(URLS + 'plantillaEntrevistaAsesor')),

    (r'^asesorias/preguntaAsesor/',
        include(URLS + 'preguntaAsesor')),

    (r'^asesorias/alumno/',
        include(URLS + 'alumno')),

    (r'^asesorias/alumnoCursoAcademico/',
        include(URLS + 'alumnoCursoAcademico')),

    (r'^asesorias/matricula/',
        include(URLS + 'matricula')),

    (r'^asesorias/calificacionConvocatoria/',
        include(URLS + 'calificacionConvocatoria')),

    (r'^asesorias/plantillaEntrevistaOficial/',
        include(URLS + 'plantillaEntrevistaOficial')),

    (r'^asesorias/preguntaOficial/',
        include(URLS + 'preguntaOficial')),

    (r'^asesorias/reunion/',
        include(URLS + 'reunion')),

    (r'^asesorias/centro_administradorCentro/',
        include(URLS + 'centro_administradorCentro')),

    (r'^asesorias/reunion_preguntaAsesor/',
        include(URLS + 'reunion_preguntaAsesor')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
