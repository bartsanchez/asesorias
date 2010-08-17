from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns = patterns(VISTAS + 'vistasDepartamento',
    url(r'^add/$',
        'addDepartamento', name='addDepartamento'),

    url(r'^(?P<nombre_departamento>[\s\w]+)/edit/$',

        'editDepartamento', name='editDepartamento'),

    url(r'^(?P<nombre_departamento>[\s\w]+)/del/$',

        'delDepartamento', name='delDepartamento'),

    url(r'^list/(?P<orden>[\s\w]*)/$',
        'listDepartamento', name='listDepartamento'),

    url(r'^generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaDepartamentos',
        name='generarPDFListaDepartamentos'),
)
