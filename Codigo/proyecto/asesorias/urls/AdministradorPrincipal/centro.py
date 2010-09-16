from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# --------------- #
# Url's de centro #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasCentro',
    url(r'^add/$', 'addCentro', name='addCentro'),

    url(r'^(?P<centro>[\s\w]+)/edit/$',
        'editCentro', name='editCentro'),

    url(r'^(?P<centro>[\s\w]+)/del/$',
        'delCentro', name='delCentro'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listCentro', name='listCentro'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaCentros', name='generarPDFListaCentros'),
)
