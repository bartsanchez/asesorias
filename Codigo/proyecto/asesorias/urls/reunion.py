from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion',
    url(r'^add/$',
        'addReunion', name='addReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        'editReunion', name='editReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        'delReunion', name='delReunion'),

    url(r'^list/$',
        'listReunion', name='listReunion'),
)
