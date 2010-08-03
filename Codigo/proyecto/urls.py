from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	url(r'^asesorias/asesor/$', 'asesorias.views.asesor', name='vista_asesor'),
	url(r'^asesorias/alumno/$', 'asesorias.views.alumno', name='vista_alumno'),
)

# -------------------------------- #
# Url's de administrador principal #
# -------------------------------- #
urlpatterns += patterns('',
	url(r'^asesorias/administrador/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_inicio', name='administrador_inicio'),
	url(r'^asesorias/administrador/organizacion_institucional/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_org_institucional', name='administrador_org_institucional'),
	url(r'^asesorias/administrador/organizacion_docente/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_org_docente', name='administrador_org_docente'),
	url(r'^asesorias/administrador/alumnos/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_alumnos', name='administrador_alumnos'),
	url(r'^asesorias/administrador/reuniones/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_reuniones', name='administrador_reuniones'),
	url(r'^asesorias/administrador/plantillas/$', 'asesorias.vistas.vistasAdministradorPrincipal.administrador_plantillas', name='administrador_plantillas'),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/$', 'asesorias.vistas.vistasGestionUsuarios.authentication', name='authentication'),
	url(r'^asesorias/logout/$', 'asesorias.vistas.vistasGestionUsuarios.logout_view', name='logout'),
)

# --------------- #
# Url's de centro #
# --------------- #

urlpatterns += patterns('',
	url(r'^asesorias/centro/add/$', 'asesorias.vistas.vistasCentro.addCentro', name='addCentro'),
	url(r'^asesorias/centro/(?P<centro>[\s\w]+)/edit/$', 'asesorias.vistas.vistasCentro.editCentro', name='editCentro'),
	url(r'^asesorias/centro/(?P<centro>[\s\w]+)/del/$', 'asesorias.vistas.vistasCentro.delCentro', name='delCentro'),
	url(r'^asesorias/centro/list/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasCentro.listCentro', name='listCentro'),
	url(r'^asesorias/centro/generarPDF/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasCentro.generarPDFListaCentros', name='generarPDFListaCentros'),
)

# -------------------------------- #
# Url's de administrador de centro #
# -------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/administradorCentro/add/$', 'asesorias.vistas.vistasAdministradorCentro.addAdministradorCentro', name='addAdministradorCentro'),
	url(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/edit/$', 'asesorias.vistas.vistasAdministradorCentro.editAdministradorCentro', name='editAdministradorCentro'),
	url(r'^asesorias/administradorCentro/(?P<administrador_centro>[\s\w]+)/del/$', 'asesorias.vistas.vistasAdministradorCentro.delAdministradorCentro', name='delAdministradorCentro'),
	url(r'^asesorias/administradorCentro/list/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAdministradorCentro.listAdministradorCentro', name='listAdministradorCentro'),
	url(r'^asesorias/administradorCentro/generarPDF/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasAdministradorCentro.generarPDFListaAdministradoresCentro', name='generarPDFListaAdministradoresCentro'),
)

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/titulacion/add/(?P<nombre_centro>[\s\w]*)/$', 'asesorias.vistas.vistasTitulacion.addTitulacion', name='addTitulacion'),
	url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/edit/$', 'asesorias.vistas.vistasTitulacion.editTitulacion', name='editTitulacion'),
	url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$', 'asesorias.vistas.vistasTitulacion.delTitulacion', name='delTitulacion'),
	url(r'^asesorias/titulacion/list/(?P<nombre_centro>[\s\w]+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasTitulacion.listTitulacion', name='listTitulacion'),
	url(r'^asesorias/titulacion/select/$', 'asesorias.vistas.vistasTitulacion.selectCentro', name='selectCentro_Titulacion'),
	url(r'^asesorias/titulacion/generarPDF/(?P<nombre_centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasTitulacion.generarPDFListaTitulaciones', name='generarPDFListaTitulaciones'),
)

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asignatura/add/(?P<nombre_centro>[\s\w]*)/(?P<nombre_titulacion>[\s\w]*)/(?P<plan_estudios>\d*)/$', 'asesorias.vistas.vistasAsignatura.addAsignatura', name='addAsignatura'),
	url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/edit/$', 'asesorias.vistas.vistasAsignatura.editAsignatura', name='editAsignatura'),
	url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/del/$', 'asesorias.vistas.vistasAsignatura.delAsignatura', name='delAsignatura'),
	url(r'^asesorias/asignatura/list/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAsignatura.listAsignatura', name='listAsignatura'),
	url(r'^asesorias/asignatura/selectCentro/(?P<tipo>[\s\w]+)/$', 'asesorias.vistas.vistasAsignatura.selectCentro', name='selectCentro_Asignatura'),
	url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/selectTitulacion/(?P<tipo>[\s\w]+)/$', 'asesorias.vistas.vistasAsignatura.selectTitulacion', name='selectTitulacion_Asignatura'),
	url(r'^asesorias/asignatura/generarPDF/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasAsignatura.generarPDFListaAsignaturas', name='generarPDFListaAsignaturas'),
)

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asignaturaCursoAcademico/add/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.addAsignaturaCursoAcademico', name='addAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.editAsignaturaCursoAcademico', name='editAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.delAsignaturaCursoAcademico', name='delAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/list/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.listAsignaturaCursoAcademico', name='listAsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/selectCentro/(?P<tipo>[\s\w]+)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.selectCentro', name='selectCentro_AsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/selectTitulacion/(?P<tipo>[\s\w]+)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.selectTitulacion', name='selectTitulacion_AsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/selectAsignatura/(?P<tipo>[\s\w]+)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.selectAsignatura', name='selectAsignatura_AsignaturaCursoAcademico'),
	url(r'^asesorias/asignaturaCursoAcademico/generarPDF/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasAsignaturaCursoAcademico.generarPDFListaAsignaturasCursoAcademico', name='generarPDFListaAsignaturasCursoAcademico'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/departamento/add/$', 'asesorias.vistas.vistasDepartamento.addDepartamento', name='addDepartamento'),
	url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/edit/$', 'asesorias.vistas.vistasDepartamento.editDepartamento', name='editDepartamento'),
	url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/del/$', 'asesorias.vistas.vistasDepartamento.delDepartamento', name='delDepartamento'),
	url(r'^asesorias/departamento/list/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasDepartamento.listDepartamento', name='listDepartamento'),
	url(r'^asesorias/departamento/generarPDF/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasDepartamento.generarPDFListaDepartamentos', name='generarPDFListaDepartamentos'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asesor/add/$', 'asesorias.vistas.vistasAsesor.addAsesor', name='addAsesor'),
	url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'asesorias.vistas.vistasAsesor.editAsesor', name='editAsesor'),
	url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$', 'asesorias.vistas.vistasAsesor.delAsesor', name='delAsesor'),
	url(r'^asesorias/asesor/list/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAsesor.listAsesor', name='listAsesor'),
	url(r'^asesorias/asesor/generarPDF/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasAsesor.generarPDFListaAsesores', name='generarPDFListaAsesores'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/asesorCursoAcademico/add/(?P<nombre_departamento>[\s\w]*)/(?P<dni_pasaporte>[\s\w]*)/$', 'asesorias.vistas.vistasAsesorCursoAcademico.addAsesorCursoAcademico', name='addAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'asesorias.vistas.vistasAsesorCursoAcademico.editAsesorCursoAcademico', name='editAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'asesorias.vistas.vistasAsesorCursoAcademico.delAsesorCursoAcademico', name='delAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/list/$', 'asesorias.vistas.vistasAsesorCursoAcademico.listAsesorCursoAcademico', name='listAsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/selectAsesor/$', 'asesorias.vistas.vistasAsesorCursoAcademico.selectAsesor', name='selectAsesor_AsesorCursoAcademico'),
	url(r'^asesorias/asesorCursoAcademico/generarPDF/(?P<dni_pasaporte>[\s\w]+)/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasAsesorCursoAcademico.generarPDFListaAsesoresCursoAcademico', name='generarPDFListaAsesoresCursoAcademico'),
)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/plantillaEntrevistaAsesor/add/$', 'asesorias.vistas.vistasPlantillaEntrevistaAsesor.addPlantillaEntrevistaAsesor', name='addPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/edit/$', 'asesorias.vistas.vistasPlantillaEntrevistaAsesor.editPlantillaEntrevistaAsesor', name='editPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/del/$', 'asesorias.vistas.vistasPlantillaEntrevistaAsesor.delPlantillaEntrevistaAsesor', name='delPlantillaEntrevistaAsesor'),
	url(r'^asesorias/plantillaEntrevistaAsesor/list/$', 'asesorias.vistas.vistasPlantillaEntrevistaAsesor.listPlantillaEntrevistaAsesor', name='listPlantillaEntrevistaAsesor'),
)

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns += patterns('',
	url(r'^asesorias/preguntaAsesor/add/$', 'asesorias.vistas.vistasPreguntaAsesor.addPreguntaAsesor', name='addPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/edit/$', 'asesorias.vistas.vistasPreguntaAsesor.editPreguntaAsesor', name='editPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/del/$', 'asesorias.vistas.vistasPreguntaAsesor.delPreguntaAsesor', name='delPreguntaAsesor'),
	url(r'^asesorias/preguntaAsesor/list/$', 'asesorias.vistas.vistasPreguntaAsesor.listPreguntaAsesor', name='listPreguntaAsesor'),
)

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns += patterns('',
	url(r'^asesorias/alumno/add/$', 'asesorias.vistas.vistasAlumno.addAlumno', name='addAlumno'),
	url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'asesorias.vistas.vistasAlumno.editAlumno', name='editAlumno'),
	url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/del/$', 'asesorias.vistas.vistasAlumno.delAlumno', name='delAlumno'),
	url(r'^asesorias/alumno/list/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAlumno.listAlumno', name='listAlumno'),
	url(r'^asesorias/alumno/generarPDF/$', 'asesorias.vistas.vistasAlumno.generarPDFListaAlumnos', name='generarPDFListaAlumnos'),
)

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/alumnoCursoAcademico/add/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.addAlumnoCursoAcademico', name='addAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.editAlumnoCursoAcademico', name='editAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.delAlumnoCursoAcademico', name='delAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/list/(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/selectAlumno/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.selectAlumno', name='selectAlumno_AlumnoCursoAcademico'),
	url(r'^asesorias/alumnoCursoAcademico/generarPDF/$', 'asesorias.vistas.vistasAlumnoCursoAcademico.generarPDFListaAlumnosCursoAcademico', name='generarPDFListaAlumnosCursoAcademico'),
)

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns += patterns('',
	url(r'^asesorias/matricula/add/$', 'asesorias.vistas.vistasMatricula.addMatricula', name='addMatricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/edit/$', 'asesorias.vistas.vistasMatricula.editMatricula', name='editMatricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/del/$', 'asesorias.vistas.vistasMatricula.delMatricula', name='delMatricula'),
	url(r'^asesorias/matricula/list/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasMatricula.listMatricula', name='listMatricula'),
	url(r'^asesorias/matricula/select/$', 'asesorias.vistas.vistasMatricula.selectAsignaturaCursoAcademicoOAlumnoCursoAcademico', name='selectAsignaturaCursoAcademicoOAlumnoCursoAcademico'),
	url(r'^asesorias/matricula/selectCentro/$', 'asesorias.vistas.vistasMatricula.selectCentro', name='selectCentro_Matricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/selectTitulacion/$', 'asesorias.vistas.vistasMatricula.selectTitulacion', name='selectTitulacion_Matricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/selectAsignatura/$', 'asesorias.vistas.vistasMatricula.selectAsignatura', name='selectAsignatura_Matricula'),
	url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/selectAsignaturaCursoAcademicoOAlumnoCursoAcademico/$', 'asesorias.vistas.vistasMatricula.selectAsignaturaCursoAcademico', name='selectAsignaturaCursoAcademico_Matricula'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/calificacionConvocatoria/add/$', 'asesorias.vistas.vistasCalificacionConvocatoria.addCalificacionConvocatoria', name='addCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/edit/$', 'asesorias.vistas.vistasCalificacionConvocatoria.editCalificacionConvocatoria', name='editCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/(?P<convocatoria>[\s\w]+)/del/$', 'asesorias.vistas.vistasCalificacionConvocatoria.delCalificacionConvocatoria', name='delCalificacionConvocatoria'),
	url(r'^asesorias/calificacionConvocatoria/list/$', 'asesorias.vistas.vistasCalificacionConvocatoria.listCalificacionConvocatoria', name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/plantillaEntrevistaOficial/add/$', 'asesorias.vistas.vistasPlantillaEntrevistaOficial.addPlantillaEntrevistaOficial', name='addPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/edit/$', 'asesorias.vistas.vistasPlantillaEntrevistaOficial.editPlantillaEntrevistaOficial', name='editPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/(?P<id_entrevista_oficial>[\s\w]+)/del/$', 'asesorias.vistas.vistasPlantillaEntrevistaOficial.delPlantillaEntrevistaOficial', name='delPlantillaEntrevistaOficial'),
	url(r'^asesorias/plantillaEntrevistaOficial/list/$', 'asesorias.vistas.vistasPlantillaEntrevistaOficial.listPlantillaEntrevistaOficial', name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/preguntaOficial/add/$', 'asesorias.vistas.vistasPreguntaOficial.addPreguntaOficial', name='addPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/edit/$', 'asesorias.vistas.vistasPreguntaOficial.editPreguntaOficial', name='editPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/(?P<id_pregunta_oficial>\d+)/del/$', 'asesorias.vistas.vistasPreguntaOficial.delPreguntaOficial', name='delPreguntaOficial'),
	url(r'^asesorias/preguntaOficial/list/$', 'asesorias.vistas.vistasPreguntaOficial.listPreguntaOficial', name='listPreguntaOficial'),
)

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns += patterns('',
	url(r'^asesorias/reunion/add/$', 'asesorias.vistas.vistasReunion.addReunion', name='addReunion'),
	url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$', 'asesorias.vistas.vistasReunion.editReunion', name='editReunion'),
	url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$', 'asesorias.vistas.vistasReunion.delReunion', name='delReunion'),
	url(r'^asesorias/reunion/list/$', 'asesorias.vistas.vistasReunion.listReunion', name='listReunion'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/centro_administradorCentro/add/(?P<nombre_centro>[\s\w]*)/$', 'asesorias.vistas.vistasCentro_administradorCentro.addCentro_administradorCentro', name='addCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/edit/$', 'asesorias.vistas.vistasCentro_administradorCentro.editCentro_administradorCentro', name='editCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/(?P<administrador_centro>[\s\w]+)/del/$', 'asesorias.vistas.vistasCentro_administradorCentro.delCentro_administradorCentro', name='delCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/list/(?P<centro>[\s\w]+)/(?P<orden>[\s\w]*)/$', 'asesorias.vistas.vistasCentro_administradorCentro.listCentro_administradorCentro', name='listCentro_administradorCentro'),
	url(r'^asesorias/centro_administradorCentro/select/$', 'asesorias.vistas.vistasCentro_administradorCentro.selectCentro', name='selectCentro_CentroAdministradorCentro'),
	url(r'^asesorias/centro_administradorCentro/generarPDF/(?P<centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$', 'asesorias.vistas.vistasCentro_administradorCentro.generarPDFListaCentros_administradorCentro', name='generarPDFListaCentros_administradorCentro'),
)

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns += patterns('',
	url(r'^asesorias/reunion_preguntaAsesor/add/$', 'asesorias.vistas.vistasReunion_preguntaAsesor.addReunion_preguntaAsesor', name='addReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/edit/$', 'asesorias.vistas.vistasReunion_preguntaAsesor.editReunion_preguntaAsesor', name='editReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/del/$', 'asesorias.vistas.vistasReunion_preguntaAsesor.delReunion_preguntaAsesor', name='delReunion_preguntaAsesor'),
	url(r'^asesorias/reunion_preguntaAsesor/list/$', 'asesorias.vistas.vistasReunion_preguntaAsesor.listReunion_preguntaAsesor', name='listReunion_preguntaAsesor'),
)
