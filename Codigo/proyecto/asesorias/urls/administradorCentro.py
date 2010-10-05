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

    ### Includes a cada entidad ###

)
