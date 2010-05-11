from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	url(r'^asesorias/administrador/$', 'proyecto.asesorias.views.administrador', name='vista_administrador'),
	url(r'^asesorias/asesor/$', 'proyecto.asesorias.views.asesor', name='vista_asesor'),
	url(r'^asesorias/alumno/$', 'proyecto.asesorias.views.alumno', name='vista_alumno'),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/$', 'proyecto.asesorias.vistas.vistasGestionUsuarios.authentication', name='authentication'),
	url(r'^asesorias/logout/$', 'proyecto.asesorias.vistas.vistasGestionUsuarios.logout_view', name='logout'),
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
	url(r'^asesorias/asignaturaCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.listAsignaturaCursoAcademico', name='listAsignaturaCursoAcademico'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns('',
	(r'^asesorias/departamento/add/$', 'proyecto.asesorias.vistas.vistasDepartamento.addDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasDepartamento.editDepartamento'),
	(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasDepartamento.delDepartamento'),
	url(r'^asesorias/departamento/list/$', 'proyecto.asesorias.vistas.vistasDepartamento.listDepartamento', name='listDepartamento'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns('',
	(r'^asesorias/asesor/add/$', 'proyecto.asesorias.vistas.vistasAsesor.addAsesor'),
	(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesor.editAsesor'),
	(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsesor.delAsesor'),
	url(r'^asesorias/asesor/list/$', 'proyecto.asesorias.vistas.vistasAsesor.listAsesor', name='listAsesor'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/asesorCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.addAsesorCursoAcademico'),
	(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.editAsesorCursoAcademico'),
	(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.delAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.listAsesorCursoAcademico', name='listAsesorCursoAcademico'),
)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/plantillaEntrevistaAsesor/add/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.addPlantillaEntrevistaAsesor'),
	(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.editPlantillaEntrevistaAsesor'),
	(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.delPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/list/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.listPlantillaEntrevistaAsesor', name='listPlantillaEntrevistaAsesor'),
)

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns += patterns('',
	(r'^asesorias/preguntaAsesor/add/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.addPreguntaAsesor'),
	(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.editPreguntaAsesor'),
	(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.delPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/list/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.listPreguntaAsesor', name='listPreguntaAsesor'),
)

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns += patterns('',
	(r'^asesorias/alumno/add/$', 'proyecto.asesorias.vistas.vistasAlumno.addAlumno'),
	(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAlumno.editAlumno'),
	(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAlumno.delAlumno'),
	url(r'^asesorias/alumno/list/$', 'proyecto.asesorias.vistas.vistasAlumno.listAlumno', name='listAlumno'),
)

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/alumnoCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.addAlumnoCursoAcademico'),
	(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.editAlumnoCursoAcademico'),
	(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.delAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),
)

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns += patterns('',
	(r'^asesorias/matricula/add/$', 'proyecto.asesorias.vistas.vistasMatricula.addMatricula'),
	(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasMatricula.editMatricula'),
	(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasMatricula.delMatricula'),
	url(r'^asesorias/matricula/list/$', 'proyecto.asesorias.vistas.vistasMatricula.listMatricula', name='listMatricula'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/calificacionConvocatoria/add/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.addCalificacionConvocatoria'),
	(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.editCalificacionConvocatoria'),
	(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.delCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/list/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.listCalificacionConvocatoria', name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/plantillaEntrevistaOficial/add/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.addPlantillaEntrevistaOficial'),
	(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.delPlantillaEntrevistaOficial'),
	(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.editPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/list/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.listPlantillaEntrevistaOficial', name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/preguntaOficial/add/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.addPreguntaOficial'),
	(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.editPreguntaOficial'),
	(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.delPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/list/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.listPreguntaOficial', name='listPreguntaOficial'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns('',
	(r'^asesorias/centro_administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro'),
	(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.listCentro_administradorCentro', name='listCentro_administradorCentro'),
)
