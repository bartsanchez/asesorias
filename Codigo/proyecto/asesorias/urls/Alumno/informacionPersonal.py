from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Alumno.'

# ------------------------#
# Url's de usuario alumno #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasInformacionPersonal',
    url(r'^show/$',
        'showInfo', name='showInfo_Alumno'),

    url(r'^modificarClave/$',
        'modificarClave', name='modificarClave_Alumno'),
)
