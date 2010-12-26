from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.'

# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^asesorias/administradorPrincipal/',
        include(URLS + 'administradorPrincipal')),

    (r'^asesorias/administradorCentro/(?P<centro>[\s\w]+)/',
        include(URLS + 'administradorCentro')),

    (r'^asesorias/asesor/(?P<curso_academico>\d+)/',
        include(URLS + 'asesor')),

    (r'^asesorias/alumno/(?P<curso_academico>\d+)/',
        include(URLS + 'alumno')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/recordarPassword/$',
        'recordar_password', name='recordar_password'),

    url(r'^asesorias/determinarCentro/$',
        'determinarCentro_AdministradorCentro',
        name='determinarCentro_AdministradorCentro'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
