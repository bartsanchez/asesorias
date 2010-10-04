from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.Asesor.'

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasAsesor',

    ### URLS del menu horizontal. ###

    url(r'^$', 'asesor_inicio', name='asesor_inicio'),

    url(r'^informacion_personal/$',

        'asesor_informacion_personal',
        name='asesor_informacion_personal'),

    url(r'^alumnos/$', 'asesor_alumnos', name='asesor_alumnos'),

    url(r'^plantillas/$', 'asesor_plantillas',
        name='asesor_plantillas'),

    url(r'^reuniones/$', 'asesor_reuniones',
        name='asesor_reuniones'),

    url(r'^establecerCursoAcademico/$', 'setCursoAcademico',
        name='setCursoAcademico_Asesor'),

    ### Includes a cada entidad ###

    (r'^info/',
        include(URLS + 'informacionPersonal')),

    (r'^alumnos/',
        include(URLS + 'alumnos')),

    (r'^plantillas/',
        include(URLS + 'plantillas')),
)
