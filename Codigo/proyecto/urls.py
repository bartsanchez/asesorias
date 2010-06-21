from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	url(r'^asesorias/asesor/$', 'proyecto.asesorias.views.asesor', name='vista_asesor'),
	url(r'^asesorias/alumno/$', 'proyecto.asesorias.views.alumno', name='vista_alumno'),
)

# -------------------------------- #
# Url's de administrador principal #
# -------------------------------- #
urlpatterns += patterns('',
	url(r'^asesorias/administrador/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_inicio', name='administrador_inicio'),
	url(r'^asesorias/administrador/organizacion_institucional/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_org_institucional', name='administrador_org_institucional'),
	url(r'^asesorias/administrador/organizacion_docente/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_org_docente', name='administrador_org_docente'),
	url(r'^asesorias/administrador/alumnos/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_alumnos', name='administrador_alumnos'),
	url(r'^asesorias/administrador/reuniones/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_reuniones', name='administrador_reuniones'),
	url(r'^asesorias/administrador/plantillas/$', 'proyecto.asesorias.vistas.vistasAdministradorPrincipal.administrador_plantillas', name='administrador_plantillas'),
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
	url(r'^asesorias/centro/add/$', 'proyecto.asesorias.vistas.vistasCentro.addCentro', name='addCentro'),
	url(r'^asesorias/centro/(?P<centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro.editCentro', name='editCentro'),
	url(r'^asesorias/centro/(?P<centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro.delCentro', name='delCentro'),
	url(r'^asesorias/centro/list/$', 'proyecto.asesorias.vistas.vistasCentro.listCentro', name='listCentro'),
	url(r'^asesorias/centro/generarPDF/$', 'proyecto.asesorias.vistas.vistasCentro.generarPDFListaCentros', name='generarPDFListaCentros'),
)

# -------------------------------- #
# Url's de administrador de centro #
# -------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.addAdministradorCentro', name='addAdministradorCentro'),
	url(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.editAdministradorCentro', name='editAdministradorCentro'),
	url(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.delAdministradorCentro', name='delAdministradorCentro'),
	url(r'^asesorias/administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.listAdministradorCentro', name='listAdministradorCentro'),
	url(r'^asesorias/administradorCentro/generarPDF/$', 'proyecto.asesorias.vistas.vistasAdministradorCentro.generarPDFListaAdministradoresCentro', name='generarPDFListaAdministradoresCentro'),
)

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/titulacion/add/$', 'proyecto.asesorias.vistas.vistasTitulacion.addTitulacion', name='addTitulacion'),
	url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasTitulacion.editTitulacion', name='editTitulacion'),
	url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$', 'proyecto.asesorias.vistas.vistasTitulacion.delTitulacion', name='delTitulacion'),
	url(r'^asesorias/titulacion/list/$', 'proyecto.asesorias.vistas.vistasTitulacion.listTitulacion', name='listTitulacion'),
	url(r'^asesorias/titulacion/generarPDF/$', 'proyecto.asesorias.vistas.vistasTitulacion.generarPDFListaTitulaciones', name='generarPDFListaTitulaciones'),
)

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asignatura/add/$', 'proyecto.asesorias.vistas.vistasAsignatura.addAsignatura', name='addAsignatura'),
	url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignatura.editAsignatura', name='editAsignatura'),
	url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsignatura.delAsignatura', name='delAsignatura'),
	url(r'^asesorias/asignatura/list/$', 'proyecto.asesorias.vistas.vistasAsignatura.listAsignatura', name='listAsignatura'),
)

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asignaturaCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.addAsignaturaCursoAcademico', name='addAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.editAsignaturaCursoAcademico', name='editAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.delAsignaturaCursoAcademico', name='delAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.listAsignaturaCursoAcademico', name='listAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/generarPDF/$', 'proyecto.asesorias.vistas.vistasAsignaturaCursoAcademico.generarPDFListaAsignaturasCursoAcademico', name='generarPDFListaAsignaturasCursoAcademico'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/departamento/add/$', 'proyecto.asesorias.vistas.vistasDepartamento.addDepartamento', name='addDepartamento'),
	url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasDepartamento.editDepartamento', name='editDepartamento'),
	url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasDepartamento.delDepartamento', name='delDepartamento'),
	url(r'^asesorias/departamento/list/$', 'proyecto.asesorias.vistas.vistasDepartamento.listDepartamento', name='listDepartamento'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asesor/add/$', 'proyecto.asesorias.vistas.vistasAsesor.addAsesor', name='addAsesor'),
	url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesor.editAsesor', name='editAsesor'),
	url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAsesor.delAsesor', name='delAsesor'),
	url(r'^asesorias/asesor/list/$', 'proyecto.asesorias.vistas.vistasAsesor.listAsesor', name='listAsesor'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asesorCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.addAsesorCursoAcademico', name='addAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.editAsesorCursoAcademico', name='editAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.delAsesorCursoAcademico', name='delAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAsesorCursoAcademico.listAsesorCursoAcademico', name='listAsesorCursoAcademico'),
)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/plantillaEntrevistaAsesor/add/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.addPlantillaEntrevistaAsesor', name='addPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.editPlantillaEntrevistaAsesor', name='editPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.delPlantillaEntrevistaAsesor', name='delPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/list/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaAsesor.listPlantillaEntrevistaAsesor', name='listPlantillaEntrevistaAsesor'),
)

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns += patterns('',
	url(r'^asesorias/preguntaAsesor/add/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.addPreguntaAsesor', name='addPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.editPreguntaAsesor', name='editPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.delPreguntaAsesor', name='delPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/list/$', 'proyecto.asesorias.vistas.vistasPreguntaAsesor.listPreguntaAsesor', name='listPreguntaAsesor'),
)

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns += patterns('',
	url(r'^asesorias/alumno/add/$', 'proyecto.asesorias.vistas.vistasAlumno.addAlumno', name='addAlumno'),
	url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasAlumno.editAlumno', name='editAlumno'),
	url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasAlumno.delAlumno', name='delAlumno'),
	url(r'^asesorias/alumno/list/$', 'proyecto.asesorias.vistas.vistasAlumno.listAlumno', name='listAlumno'),
)

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/alumnoCursoAcademico/add/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.addAlumnoCursoAcademico', name='addAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.editAlumnoCursoAcademico', name='editAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.delAlumnoCursoAcademico', name='delAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/list/$', 'proyecto.asesorias.vistas.vistasAlumnoCursoAcademico.listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),
)

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns += patterns('',
	url(r'^asesorias/matricula/add/$', 'proyecto.asesorias.vistas.vistasMatricula.addMatricula', name='addMatricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasMatricula.editMatricula', name='editMatricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasMatricula.delMatricula', name='delMatricula'),
	url(r'^asesorias/matricula/list/$', 'proyecto.asesorias.vistas.vistasMatricula.listMatricula', name='listMatricula'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/calificacionConvocatoria/add/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.addCalificacionConvocatoria', name='addCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.editCalificacionConvocatoria', name='editCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.delCalificacionConvocatoria', name='delCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/list/$', 'proyecto.asesorias.vistas.vistasCalificacionConvocatoria.listCalificacionConvocatoria', name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/plantillaEntrevistaOficial/add/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.addPlantillaEntrevistaOficial', name='addPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.editPlantillaEntrevistaOficial', name='editPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.delPlantillaEntrevistaOficial', name='delPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/list/$', 'proyecto.asesorias.vistas.vistasPlantillaEntrevistaOficial.listPlantillaEntrevistaOficial', name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/preguntaOficial/add/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.addPreguntaOficial', name='addPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.editPreguntaOficial', name='editPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/del/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.delPreguntaOficial', name='delPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/list/$', 'proyecto.asesorias.vistas.vistasPreguntaOficial.listPreguntaOficial', name='listPreguntaOficial'),
)

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns += patterns('',
	url(r'^asesorias/reunion/add/$', 'proyecto.asesorias.vistas.vistasReunion.addReunion', name='addReunion'),
	url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasReunion.editReunion', name='editReunion'),
	url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$', 'proyecto.asesorias.vistas.vistasReunion.delReunion', name='delReunion'),
	url(r'^asesorias/reunion/list/$', 'proyecto.asesorias.vistas.vistasReunion.listReunion', name='listReunion'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/centro_administradorCentro/add/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro', name='addCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/edit/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro', name='editCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro', name='delCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/list/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.listCentro_administradorCentro', name='listCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/generarPDF/$', 'proyecto.asesorias.vistas.vistasCentro_administradorCentro.generarPDFListaCentros_administradorCentro', name='generarPDFListaCentros_administradorCentro'),
)

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/reunion_preguntaAsesor/add/$', 'proyecto.asesorias.vistas.vistasReunion_preguntaAsesor.addReunion_preguntaAsesor', name='addReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/edit/$', 'proyecto.asesorias.vistas.vistasReunion_preguntaAsesor.editReunion_preguntaAsesor', name='editReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/del/$', 'proyecto.asesorias.vistas.vistasReunion_preguntaAsesor.delReunion_preguntaAsesor', name='delReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/list/$', 'proyecto.asesorias.vistas.vistasReunion_preguntaAsesor.listReunion_preguntaAsesor', name='listReunion_preguntaAsesor'),
)
