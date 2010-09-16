from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns = patterns(VISTAS + 'vistasTitulacion',
    url(r'^add/(?P<nombre_centro>[\s\w]*)/$',
         'addTitulacion', name='addTitulacion'),

    url(r'^(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/edit/$',

        'editTitulacion', name='editTitulacion'),

    url(r'^(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/del/$',

        'delTitulacion', name='delTitulacion'),

    url(r'^list/(?P<nombre_centro>[\s\w]+)/(?P<orden>[\s\w]*)/$',
        'listTitulacion', name='listTitulacion'),

    url(r'^select/$', 'selectCentro', name='selectCentro_Titulacion'),

    url(r'^generarPDF/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaTitulaciones',
        name='generarPDFListaTitulaciones'),
)
