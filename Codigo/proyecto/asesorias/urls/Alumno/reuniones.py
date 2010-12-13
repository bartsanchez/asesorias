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

    url(r'^editRespuestaOficial/(?P<id_reunion>\d+)/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/' +
        '(?P<id_pregunta_oficial>[\s\w]+)/$',

        'editRespuestaOficial',
        name='editRespuestaOficial_Alumno'),

    url(r'^editRespuestaAsesor/(?P<id_reunion>\d+)/' +
        '(?P<id_entrevista_asesor>[\s\w]+)/' +
        '(?P<id_pregunta_asesor>[\s\w]+)/$',

        'editRespuestaAsesor',
        name='editRespuestaAsesor_Alumno'),
)
