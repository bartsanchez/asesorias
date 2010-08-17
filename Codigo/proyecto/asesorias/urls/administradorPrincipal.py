from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# -------------------------------- #
# Url's de administrador principal #
# -------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAdministradorPrincipal',
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
)
