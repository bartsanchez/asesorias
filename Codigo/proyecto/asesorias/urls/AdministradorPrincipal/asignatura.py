from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.AdministradorPrincipal.'

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns = patterns(VISTAS + 'vistasAsignatura',
    url(r'^add/(?P<nombre_centro>[\s\w]*)/' +
        '(?P<nombre_titulacion>[\s\w]*)/(?P<plan_estudios>\d*)/$',

        'addAsignatura', name='addAsignatura'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/edit/$',

        'editAsignatura', name='editAsignatura'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/del/$',

        'delAsignatura', name='delAsignatura'),

    url(r'^list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listAsignatura', name='listAsignatura'),

    url(r'^selectCentro/(?P<tipo>[\s\w]+)/$',
        'selectCentro', name='selectCentro_Asignatura'),

    url(r'^(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion', name='selectTitulacion_Asignatura'),

    url(r'^generarPDF/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsignaturas',
        name='generarPDFListaAsignaturas'),
)
