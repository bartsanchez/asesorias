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
)
