from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------------#
# Url's de usuario alumno #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasInformacionPersonal',
    url(r'^modificarClave/$',
        'modificarClave', name='modificarClave_AdministradorCentro'),
)
