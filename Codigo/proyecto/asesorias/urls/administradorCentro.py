from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# -------------------------------- #
# Url's de administrador de centro #
# -------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAdministradorCentro',
    url(r'^add/$',
        'addAdministradorCentro', name='addAdministradorCentro'),

    url(r'^(?P<administrador_centro>[\s\w]+)/edit/$',
        'editAdministradorCentro', name='editAdministradorCentro'),

    url(r'^(?P<administrador_centro>[\s\w]+)/del/$',
        'delAdministradorCentro', name='delAdministradorCentro'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listAdministradorCentro', name='listAdministradorCentro'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaAdministradoresCentro',
        name='generarPDFListaAdministradoresCentro'),
)
