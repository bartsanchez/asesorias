from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasAsesor',
    url(r'^add/$', 'addAsesor', name='addAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/edit/$',
        'editAsesor', name='editAsesor'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/del/$',
        'delAsesor', name='delAsesor'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listAsesor', name='listAsesor'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaAsesores',
        name='generarPDFListaAsesores'),
)
