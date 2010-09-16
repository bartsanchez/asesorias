from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasCentro_administradorCentro',
    url(r'^add/(?P<nombre_centro>[\s\w]*)/$',

        'addCentro_administradorCentro',
        name='addCentro_administradorCentro'),

    url(r'^(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/edit/$',

        'editCentro_administradorCentro',
        name='editCentro_administradorCentro'),

    url(r'^(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$',

        'delCentro_administradorCentro',
        name='delCentro_administradorCentro'),

    url(r'^list/(?P<centro>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listCentro_administradorCentro',
        name='listCentro_administradorCentro'),

    url(r'^select/$',
        'selectCentro',
        name='selectCentro_CentroAdministradorCentro'),

    url(r'^generarPDF/(?P<centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaCentros_administradorCentro',
        name='generarPDFListaCentros_administradorCentro'),
)
