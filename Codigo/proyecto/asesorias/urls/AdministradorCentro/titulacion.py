from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns = patterns(VISTAS + 'vistasTitulacion',
    url(r'^add/$',
         'addTitulacion', name='addTitulacion_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'edit/$',

        'editTitulacion', name='editTitulacion_administradorCentro'),

    url(r'^(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$',

        'delTitulacion', name='delTitulacion_administradorCentro'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listTitulacion', name='listTitulacion_administradorCentro'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaTitulaciones',
        name='generarPDFListaTitulaciones_administradorCentro'),
)
