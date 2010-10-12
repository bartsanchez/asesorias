from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorCentro.'

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsignatura',
    url(r'^add/(?P<nombre_titulacion>[\s\w]*)/(?P<plan_estudios>\d*)/$',

        'addAsignatura', name='addAsignatura_administradorCentro'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/edit/$',

        'editAsignatura', name='editAsignatura'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/del/$',

        'delAsignatura', name='delAsignatura'),

    url(r'^list/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/'+
        '(?P<orden>[\s\w]*)/$',

        'listAsignatura', name='listAsignatura_administradorCentro'),

    url(r'^selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion',
        name='selectTitulacion_Asignatura_administradorCentro'),

    url(r'^generarPDF/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsignaturas',
        name='generarPDFListaAsignaturas_administradorCentro'),
)
