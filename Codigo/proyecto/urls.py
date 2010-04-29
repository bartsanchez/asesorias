from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	(r'^asesorias/$', 'proyecto.asesorias.views.authentication'),
	(r'^asesorias/administrador/$', 'proyecto.asesorias.views.administrador'),
	(r'^asesorias/alumnos/(?P<username>[\s\w]+)/$', 'proyecto.asesorias.views.alumnos'),
)

# --------------- #
# Url's de centro #
# --------------- #

urlpatterns += patterns('',
	(r'^asesorias/centro/add/$', 'proyecto.asesorias.vistas.vistasCentro.addCentro'),
	(r'^asesorias/centro/(?P<centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro.editCentro'),
	(r'^asesorias/centro/(?P<centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro.delCentro'),
	url(r'^asesorias/centro/list/$', 'proyecto.asesorias.vistas.vistasCentro.listCentro', name='listCentro'),
)

# -------------------------------- #
# Url's de administrador de centro #
# -------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.addAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.editAdministradorCentro'),
	(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.delAdministradorCentro'),
	url(r'^asesorias/administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.listAdministradorCentro', name='listAdministradorCentro'),
)

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns += patterns('',
	(r'^asesorias/titulacion/add/$', 'proyecto.asesorias.vistas.vistasTitulacion.addTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasTitulacion.editTitulacion'),
	(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$', 'proyecto.asesorias.vistas.vistasTitulacion.delTitulacion'),
	url(r'^asesorias/titulacion/list/$', 'proyecto.asesorias.vistas.vistasTitulacion.listTitulacion', name='listTitulacion'),
)

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns += patterns('',
	(r'^asesorias/asignatura/add/$', 'proyecto.asesorias.vistas.vistasAsignatura.addAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignatura.editAsignatura'),
	(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsignatura.delAsignatura'),
	url(r'^asesorias/asignatura/list/$', 'proyecto.asesorias.vistas.vistasAsignatura.listAsignatura', name='listAsignatura'),
)

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/asignaturaCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.addAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.editAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.delAsignaturaCursoAcademico'),
	(r'^asesorias/asignaturaCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.listAsignaturaCursoAcademico'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns('',
	(r'^asesorias/departamento/add/$', 'proyecto.asesorias.vistas.vistasDepartamento.addDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasDepartamento.editDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasDepartamento.delDepartamento'),
	(r'^asesorias/departamento/list/$', 'proyecto.asesorias.vistas.vistasDepartamento.listDepartamento'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns('',
	(r'^asesorias/asesor/add/$', 'proyecto.asesorias.vistas.vistasAsesor.addAsesor'),
	(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesor.editAsesor'),
	(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsesor.delAsesor'),
	(r'^asesorias/asesor/list/$', 'proyecto.asesorias.vistas.vistasAsesor.listAsesor'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/asesorCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.addAsesorCursoAcademico'),
	(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.editAsesorCursoAcademico'),
	(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.delAsesorCursoAcademico'),
	(r'^asesorias/asesorCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.listAsesorCursoAcademico'),

)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #
urlpatterns += patterns('',
	(r'^asesorias/plantillaEntrevistaAsesor/add/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.addPlantillaEntrevistaAsesor'),
	(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.editPlantillaEntrevistaAsesor'),
	(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.delPlantillaEntrevistaAsesor'),
	(r'^asesorias/plantillaEntrevistaAsesor/list/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.listPlantillaEntrevistaAsesor'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/centro_administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.listCentro_administradorCentro'),
)
