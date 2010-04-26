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
	(r'^asesorias/administrador/$', 'proyecto.asesorias.views.administrador'),
	(r'^asesorias/alumnos/(?P<username>[\s\w]+)/$', 'proyecto.asesorias.views.alumnos'),

	(r'^asesorias/centro/add/$', 'proyecto.asesorias.vistas.vistasCentro.addCentro'),
	(r'^asesorias/centro/(?P<centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro.editCentro'),
	(r'^asesorias/centro/(?P<centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro.delCentro'),
	(r'^asesorias/centro/list/$', 'proyecto.asesorias.vistas.vistasCentro.listCentro'),

	(r'^asesorias/administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.addAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.editAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.delAdministradorCentro'),
	(r'^asesorias/administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.listAdministradorCentro'),

	(r'^asesorias/titulacion/add/$', 'proyecto.asesorias.vistas.vistasTitulacion.addTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasTitulacion.editTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$', 'proyecto.asesorias.vistas.vistasTitulacion.delTitulacion'),
	(r'^asesorias/titulacion/list/$', 'proyecto.asesorias.vistas.vistasTitulacion.listTitulacion'),

	(r'^asesorias/asignatura/add/$', 'proyecto.asesorias.vistas.vistasAsignatura.addAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignatura.editAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsignatura.delAsignatura'),
	(r'^asesorias/asignatura/list/$', 'proyecto.asesorias.vistas.vistasAsignatura.listAsignatura'),

	(r'^asesorias/asignaturaCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.addAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.editAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.delAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.listAsignaturaCursoAcademico'),

	(r'^asesorias/departamento/add/$', 'proyecto.asesorias.vistas.vistasDepartamento.addDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasDepartamento.editDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasDepartamento.delDepartamento'),
	(r'^asesorias/departamento/list/$', 'proyecto.asesorias.vistas.vistasDepartamento.listDepartamento'),

	(r'^asesorias/asesor/add/$', 'proyecto.asesorias.vistas.vistasAsesor.addAsesor'),
	(r'^asesorias/asesor/list/$', 'proyecto.asesorias.vistas.vistasAsesor.listAsesor'),

	(r'^asesorias/centro_administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.listCentro_administradorCentro'),
)
