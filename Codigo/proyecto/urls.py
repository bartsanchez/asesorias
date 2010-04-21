from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^proyecto/', include('proyecto.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^asesorias/$', 'proyecto.asesorias.views.authentication'),
	(r'^asesorias/alumnos/(?P<username>\w+)/$', 'proyecto.asesorias.views.alumnos'),

	(r'^asesorias/centro/add/$', 'proyecto.asesorias.vistas.vistasCentro.addCentro'),
	(r'^asesorias/centro/(?P<centro>\w+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro.editCentro'),
	(r'^asesorias/centro/(?P<centro>\w+)/del/$', 'proyecto.asesorias.vistas.vistasCentro.delCentro'),

	(r'^asesorias/administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.addAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>\w+)/edit/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.editAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>\w+)/del/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.delAdministradorCentro'),

	(r'^asesorias/centro_administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>\w+)/(?P<administrador_centro>\w+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>\w+)/(?P<administrador_centro>\w+)/del/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro'),

	(r'^asesorias/titulacion/add/$', 'proyecto.asesorias.vistas.vistasTitulacion.addTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>\w+)/(?P<nombre_titulacion>\w+)/(?P<plan_estudios>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasTitulacion.editTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>\w+)/(?P<nombre_titulacion>\w+)/(?P<plan_estudios>\d+)/del/$', 'proyecto.asesorias.vistas.vistasTitulacion.delTitulacion'),

	(r'^asesorias/asignatura/add/$', 'proyecto.asesorias.vistas.vistasAsignatura.addAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>\w+)/(?P<nombre_titulacion>\w+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>\w+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignatura.editAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>\w+)/(?P<nombre_titulacion>\w+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>\w+)/del/$', 'proyecto.asesorias.vistas.vistasAsignatura.delAsignatura'),
)
