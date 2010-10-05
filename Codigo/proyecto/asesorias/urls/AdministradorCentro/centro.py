from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# --------------- #
# Url's de centro #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasCentro',
    url(r'^add/$', 'addCentro', name='addCentro_administradorCentro'),

    url(r'^(?P<centro>[\s\w]+)/edit/$',
        'editCentro', name='editCentro_administradorCentro'),

    url(r'^(?P<centro>[\s\w]+)/del/$',
        'delCentro', name='delCentro_administradorCentro'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listCentro', name='listCentro_administradorCentro'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaCentros',
        name='generarPDFListaCentros_administradorCentro'),
)
