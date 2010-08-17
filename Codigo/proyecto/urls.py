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

    (r'^asesorias/calificacionConvocatoria/',
        include('asesorias.urls.calificacionConvocatoria')),

    (r'^asesorias/plantillaEntrevistaOficial/',
        include('asesorias.urls.plantillaEntrevistaOficial')),

    (r'^asesorias/preguntaOficial/',
        include('asesorias.urls.preguntaOficial')),

    (r'^asesorias/reunion/',
        include('asesorias.urls.reunion')),

    (r'^asesorias/centro_administradorCentro/',
        include('asesorias.urls.centro_administradorCentro')),

    (r'^asesorias/reunion_preguntaAsesor/',
        include('asesorias.urls.reunion_preguntaAsesor')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
