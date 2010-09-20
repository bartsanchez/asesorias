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
    (r'^admin/', include(admin.site.urls)),

    (r'^asesorias/administradorPrincipal/',
        include(URLS + 'administradorPrincipal')),

    (r'^asesorias/asesor/(?P<curso_academico>\d+)/',
        include(URLS + 'asesor')),

    (r'^asesorias/alumno/',
        include(URLS + 'alumno')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
