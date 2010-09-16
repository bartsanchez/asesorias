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

    url(r'^asesorias/alumno/$', 'asesorias.views.alumno',
        name='vista_alumno'),

    (r'^asesorias/administradorPrincipal/',
        include(URLS + 'administradorPrincipal')),

    (r'^asesorias/asesor/',
        include(URLS + 'asesor')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)
