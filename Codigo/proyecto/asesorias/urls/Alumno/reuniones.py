from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.Alumno.'

# ------------------------#
# Url's de usuario alumno #
# ------------------------#

urlpatterns = patterns(VISTAS + 'vistasReuniones',
    url(r'^listReunion/(?P<orden>[\s\w]*)/$',
        'listReunion', name='listReunion_Alumno'),

    url(r'^showReunion/(?P<id_reunion>\d+)/$',

        'showReunion', name='showReunion_Alumno'),
)
