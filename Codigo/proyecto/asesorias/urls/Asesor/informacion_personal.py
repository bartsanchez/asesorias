from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------#
# Url's de usuario asesor #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasPrueba',
    url(r'^show/$',
        'show_info', name='show_info_asesor'),
)
