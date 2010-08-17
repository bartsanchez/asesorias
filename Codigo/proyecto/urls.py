from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ------------ #
# DEFINICIONES #
# ------------ #

VISTAS = 'asesorias.vistas.'

ADMINISTRADOR_PRINCIPAL = VISTAS + 'vistasAdministradorPrincipal.'
GESTION_USUARIOS = VISTAS + 'vistasGestionUsuarios.'
CENTRO = VISTAS + 'vistasCentro.'
ADMINISTRADOR_CENTRO = VISTAS + 'vistasAdministradorCentro.'
TITULACION = VISTAS + 'vistasTitulacion.'
ASIGNATURA = VISTAS + 'vistasAsignatura.'
ASIGNATURA_CA = VISTAS + 'vistasAsignaturaCursoAcademico.'
DEPARTAMENTO = VISTAS + 'vistasDepartamento.'
ASESOR = VISTAS + 'vistasAsesor.'
ASESOR_CA = VISTAS + 'vistasAsesorCursoAcademico.'
PLANTILLA_ASESOR = VISTAS + 'vistasPlantillaEntrevistaAsesor.'
PREGUNTA_ASESOR = VISTAS + 'vistasPreguntaAsesor.'
ALUMNO = VISTAS + 'vistasAlumno.'
ALUMNO_CA = VISTAS + 'vistasAlumnoCursoAcademico.'
MATRICULA = VISTAS + 'vistasMatricula.'
CALIFICACION_CONVOCATORIA = VISTAS + 'vistasCalificacionConvocatoria.'
PLANTILLA_OFICIAL = VISTAS + 'vistasPlantillaEntrevistaOficial.'
PREGUNTA_OFICIAL = VISTAS + 'vistasPreguntaOficial.'
REUNION = VISTAS + 'vistasReunion.'
CENTRO_ADM_CENTRO = VISTAS + 'vistasCentro_administradorCentro.'
REUNION_PREGUNTA_ASESOR = VISTAS + 'vistasReunion_preguntaAsesor.'

# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^asesorias/asesor/$', 'asesorias.views.asesor',
        name='vista_asesor'),

    url(r'^asesorias/alumno/$', 'asesorias.views.alumno',
        name='vista_alumno'),
)

# -------------------------------- #
# Url's de administrador principal #
# -------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/administrador/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_inicio',
        name='administrador_inicio'),

    url(r'^asesorias/administrador/organizacion_institucional/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_org_institucional',
        name='administrador_org_institucional'),

    url(r'^asesorias/administrador/organizacion_docente/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_org_docente',
        name='administrador_org_docente'),

    url(r'^asesorias/administrador/alumnos/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_alumnos',
        name='administrador_alumnos'),

    url(r'^asesorias/administrador/reuniones/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_reuniones',
        name='administrador_reuniones'),

    url(r'^asesorias/administrador/plantillas/$',
        ADMINISTRADOR_PRINCIPAL + 'administrador_plantillas',
        name='administrador_plantillas'),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/$', GESTION_USUARIOS + 'authentication',
        name='authentication'),

    url(r'^asesorias/logout/$', GESTION_USUARIOS + 'logout_view',
        name='logout'),
)

# --------------- #
# Url's de centro #
# --------------- #

urlpatterns += patterns('',
    url(r'^asesorias/centro/add/$', CENTRO + 'addCentro',
        name='addCentro'),

    url(r'^asesorias/centro/(?P<centro>[\s\w]+)/edit/$',
        CENTRO + 'editCentro', name='editCentro'),

    url(r'^asesorias/centro/(?P<centro>[\s\w]+)/del/$',
        CENTRO + 'delCentro', name='delCentro'),

    url(r'^asesorias/centro/list/(?P<orden>[\s\w]*)/$',
        CENTRO + 'listCentro', name='listCentro'),

    url(r'^asesorias/centro/generarPDF/(?P<busqueda>[\s\w]+)/$',
        CENTRO + 'generarPDFListaCentros',
        name='generarPDFListaCentros'),
)

# -------------------------------- #
# Url's de administrador de centro #
# -------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/administradorCentro/add/$',
        ADMINISTRADOR_CENTRO + 'addAdministradorCentro',
        name='addAdministradorCentro'),

    url(r'^asesorias/administradorCentro/' +
        '(?P<administrador_centro>[\s\w]+)/edit/$',

        ADMINISTRADOR_CENTRO + 'editAdministradorCentro',
        name='editAdministradorCentro'),

    url(r'^asesorias/administradorCentro/' +
        '(?P<administrador_centro>[\s\w]+)/del/$',

        ADMINISTRADOR_CENTRO + 'delAdministradorCentro',
        name='delAdministradorCentro'),

    url(r'^asesorias/administradorCentro/list/(?P<orden>[\s\w]*)/$',
        ADMINISTRADOR_CENTRO + 'listAdministradorCentro',
        name='listAdministradorCentro'),

    url(r'^asesorias/administradorCentro/generarPDF/' +
        '(?P<busqueda>[\s\w]+)/$',

        ADMINISTRADOR_CENTRO + 'generarPDFListaAdministradoresCentro',
        name='generarPDFListaAdministradoresCentro'),
)

# ------------------- #
# Url's de titulacion #
# ------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/titulacion/add/(?P<nombre_centro>[\s\w]*)/$',
        TITULACION + 'addTitulacion', name='addTitulacion'),

    url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/edit/$',

        TITULACION + 'editTitulacion', name='editTitulacion'),

    url(r'^asesorias/titulacion/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/del/$',

        TITULACION + 'delTitulacion', name='delTitulacion'),

    url(r'^asesorias/titulacion/list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        TITULACION + 'listTitulacion', name='listTitulacion'),

    url(r'^asesorias/titulacion/select/$',
        TITULACION + 'selectCentro', name='selectCentro_Titulacion'),

    url(r'^asesorias/titulacion/generarPDF/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        TITULACION + 'generarPDFListaTitulaciones',
        name='generarPDFListaTitulaciones'),
)

# ------------------- #
# Url's de asignatura #
# ------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/asignatura/add/(?P<nombre_centro>[\s\w]*)/' +
        '(?P<nombre_titulacion>[\s\w]*)/(?P<plan_estudios>\d*)/$',

        ASIGNATURA + 'addAsignatura', name='addAsignatura'),

    url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/edit/$',

        ASIGNATURA + 'editAsignatura', name='editAsignatura'),

    url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/del/$',

        ASIGNATURA + 'delAsignatura', name='delAsignatura'),

    url(r'^asesorias/asignatura/list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        ASIGNATURA + 'listAsignatura', name='listAsignatura'),

    url(r'^asesorias/asignatura/selectCentro/(?P<tipo>[\s\w]+)/$',
        ASIGNATURA + 'selectCentro', name='selectCentro_Asignatura'),

    url(r'^asesorias/asignatura/(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        ASIGNATURA + 'selectTitulacion',
        name='selectTitulacion_Asignatura'),

    url(r'^asesorias/asignatura/generarPDF/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<busqueda>[\s\w]+)/$',

        ASIGNATURA + 'generarPDFListaAsignaturas',
        name='generarPDFListaAsignaturas'),
)

# ----------------------------------- #
# Url's de asignatura curso academico #
# ----------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/asignaturaCursoAcademico/add/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/$',

        ASIGNATURA_CA + 'addAsignaturaCursoAcademico',
        name='addAsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        ASIGNATURA_CA + 'editAsignaturaCursoAcademico',
        name='editAsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        ASIGNATURA_CA + 'delAsignaturaCursoAcademico',
        name='delAsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/list/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/$',

        ASIGNATURA_CA + 'listAsignaturaCursoAcademico',
        name='listAsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/selectCentro/' +
        '(?P<tipo>[\s\w]+)/$',

        ASIGNATURA_CA + 'selectCentro',
        name='selectCentro_AsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/' +
        '(?P<nombre_centro>[\s\w]+)/selectTitulacion/' +
        '(?P<tipo>[\s\w]+)/$',

        ASIGNATURA_CA + 'selectTitulacion',
        name='selectTitulacion_AsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/selectAsignatura/(?P<tipo>[\s\w]+)/$',

        ASIGNATURA_CA + 'selectAsignatura',
        name='selectAsignatura_AsignaturaCursoAcademico'),

    url(r'^asesorias/asignaturaCursoAcademico/generarPDF/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        ASIGNATURA_CA + 'generarPDFListaAsignaturasCursoAcademico',
        name='generarPDFListaAsignaturasCursoAcademico'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/departamento/add/$',
        DEPARTAMENTO + 'addDepartamento', name='addDepartamento'),

    url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/' +
        'edit/$',

        DEPARTAMENTO + 'editDepartamento', name='editDepartamento'),

    url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/' +
        'del/$',

        DEPARTAMENTO + 'delDepartamento', name='delDepartamento'),

    url(r'^asesorias/departamento/list/(?P<orden>[\s\w]*)/$',
        DEPARTAMENTO + 'listDepartamento', name='listDepartamento'),

    url(r'^asesorias/departamento/generarPDF/(?P<busqueda>[\s\w]+)/$',
        DEPARTAMENTO + 'generarPDFListaDepartamentos',
        name='generarPDFListaDepartamentos'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns('',
    url(r'^asesorias/asesor/add/$',
        ASESOR + 'addAsesor', name='addAsesor'),

    url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$',
        ASESOR + 'editAsesor', name='editAsesor'),

    url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$',
        ASESOR + 'delAsesor', name='delAsesor'),

    url(r'^asesorias/asesor/list/(?P<orden>[\s\w]*)/$',
        ASESOR + 'listAsesor', name='listAsesor'),

    url(r'^asesorias/asesor/generarPDF/(?P<busqueda>[\s\w]+)/$',
        ASESOR + 'generarPDFListaAsesores',
        name='generarPDFListaAsesores'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/asesorCursoAcademico/add/' +
        '(?P<nombre_departamento>[\s\w]*)/(?P<dni_pasaporte>[\s\w]*)/$',

         ASESOR_CA + 'addAsesorCursoAcademico',
         name='addAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        ASESOR_CA + 'editAsesorCursoAcademico',
        name='editAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        ASESOR_CA + 'delAsesorCursoAcademico',
        name='delAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/list/$',

        ASESOR_CA + 'listAsesorCursoAcademico',
        name='listAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/selectAsesor/$',
        ASESOR_CA + 'selectAsesor',
        name='selectAsesor_AsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/generarPDF/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        ASESOR_CA + 'generarPDFListaAsesoresCursoAcademico',
        name='generarPDFListaAsesoresCursoAcademico'),
)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/plantillaEntrevistaAsesor/add/$',
        PLANTILLA_ASESOR + 'addPlantillaEntrevistaAsesor',
        name='addPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/edit/$',

        PLANTILLA_ASESOR + 'editPlantillaEntrevistaAsesor',
        name='editPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/del/$',

        PLANTILLA_ASESOR + 'delPlantillaEntrevistaAsesor',
        name='delPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/list/$',
        PLANTILLA_ASESOR + 'listPlantillaEntrevistaAsesor',
        name='listPlantillaEntrevistaAsesor'),
)

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns += patterns('',
    url(r'^asesorias/preguntaAsesor/add/$',
        PREGUNTA_ASESOR + 'addPreguntaAsesor',
        name='addPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/edit/$',

        PREGUNTA_ASESOR + 'editPreguntaAsesor',
        name='editPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/del/$',

        PREGUNTA_ASESOR + 'delPreguntaAsesor',
        name='delPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/list/$',
        PREGUNTA_ASESOR + 'listPreguntaAsesor',
        name='listPreguntaAsesor'),
)

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns += patterns('',
    url(r'^asesorias/alumno/add/$',
        ALUMNO + 'addAlumno', name='addAlumno'),

    url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/edit/$',
        ALUMNO + 'editAlumno', name='editAlumno'),

    url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/del/$',
        ALUMNO + 'delAlumno', name='delAlumno'),

    url(r'^asesorias/alumno/list/(?P<orden>[\s\w]*)/$',
        ALUMNO + 'listAlumno', name='listAlumno'),

    url(r'^asesorias/alumno/generarPDF/(?P<busqueda>[\s\w]+)/$',
        ALUMNO + 'generarPDFListaAlumnos',
        name='generarPDFListaAlumnos'),
)

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/alumnoCursoAcademico/add/$',
        ALUMNO_CA + 'addAlumnoCursoAcademico',
        name='addAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        ALUMNO_CA + 'editAlumnoCursoAcademico',
        name='editAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        ALUMNO_CA + 'delAlumnoCursoAcademico',
        name='delAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/list/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        ALUMNO_CA + 'listAlumnoCursoAcademico',
        name='listAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/selectAlumno/$',
        ALUMNO_CA + 'selectAlumno',
        name='selectAlumno_AlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/generarPDF/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        ALUMNO_CA + 'generarPDFListaAlumnosCursoAcademico',
        name='generarPDFListaAlumnosCursoAcademico'),
)

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns += patterns('',
    url(r'^asesorias/matricula/add/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/$',

        MATRICULA + 'addMatricula', name='addMatricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/edit/$',

        MATRICULA + 'editMatricula', name='editMatricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/del/$',

        MATRICULA + 'delMatricula', name='delMatricula'),

    url(r'^asesorias/matricula/list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        MATRICULA + 'listMatricula', name='listMatricula'),

    url(r'^asesorias/matricula/select/$',
        MATRICULA + 'selectAsignaturaOAlumnoCursoAcademico',
        name='selectAsignaturaOAlumnoCursoAcademico'),

    url(r'^asesorias/matricula/selectCentro/(?P<tipo>[\s\w]+)/$',
        MATRICULA + 'selectCentro', name='selectCentro_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        MATRICULA + 'selectTitulacion',
        name='selectTitulacion_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        MATRICULA + 'selectAsignatura',
        name='selectAsignatura_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        MATRICULA + 'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCursoAcademico_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/$',

        MATRICULA + 'selectAlumno', name='selectAlumno_Matricula'),

    url(r'^asesorias/matricula/generarPDF/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        MATRICULA + 'generarPDFListaMatriculas',
        name='generarPDFListaMatriculas'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/calificacionConvocatoria/add/$',
        CALIFICACION_CONVOCATORIA + 'addCalificacionConvocatoria',
        name='addCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/edit/$',

        CALIFICACION_CONVOCATORIA + 'editCalificacionConvocatoria',
        name='editCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/del/$',

        CALIFICACION_CONVOCATORIA + 'delCalificacionConvocatoria',
        name='delCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/list/$',
        CALIFICACION_CONVOCATORIA + 'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/plantillaEntrevistaOficial/add/$',
        PLANTILLA_OFICIAL + 'addPlantillaEntrevistaOficial',
        name='addPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/edit/$',

        PLANTILLA_OFICIAL + 'editPlantillaEntrevistaOficial',
        name='editPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/del/$',

        PLANTILLA_OFICIAL + 'delPlantillaEntrevistaOficial',
        name='delPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/list/$',
        PLANTILLA_OFICIAL + 'listPlantillaEntrevistaOficial',
        name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/preguntaOficial/add/$',
        PREGUNTA_OFICIAL + 'addPreguntaOficial',
        name='addPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/edit/$',

        PREGUNTA_OFICIAL + 'editPreguntaOficial',
        name='editPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/del/$',

        PREGUNTA_OFICIAL + 'delPreguntaOficial',
        name='delPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/list/$',
        PREGUNTA_OFICIAL + 'listPreguntaOficial',
        name='listPreguntaOficial'),
)

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns += patterns('',
    url(r'^asesorias/reunion/add/$',
        REUNION + 'addReunion', name='addReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        REUNION + 'editReunion', name='editReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        REUNION + 'delReunion', name='delReunion'),

    url(r'^asesorias/reunion/list/$',
        REUNION + 'listReunion', name='listReunion'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/centro_administradorCentro/add/' +
        '(?P<nombre_centro>[\s\w]*)/$',

        CENTRO_ADM_CENTRO + 'addCentro_administradorCentro',
        name='addCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/edit/$',

        CENTRO_ADM_CENTRO + 'editCentro_administradorCentro',
        name='editCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/del/$',

        CENTRO_ADM_CENTRO + 'delCentro_administradorCentro',
        name='delCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/list/' +
        '(?P<centro>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        CENTRO_ADM_CENTRO + 'listCentro_administradorCentro',
        name='listCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/select/$',
        CENTRO_ADM_CENTRO + 'selectCentro',
        name='selectCentro_CentroAdministradorCentro'),

    url(r'^asesorias/centro_administradorCentro/generarPDF/' +
        '(?P<centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        CENTRO_ADM_CENTRO +'generarPDFListaCentros_administradorCentro',
        name='generarPDFListaCentros_administradorCentro'),
)

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns += patterns('',
    url(r'^asesorias/reunion_preguntaAsesor/add/$',
        REUNION_PREGUNTA_ASESOR + 'addReunion_preguntaAsesor',
        name='addReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'edit/$',

        REUNION_PREGUNTA_ASESOR + 'editReunion_preguntaAsesor',
        name='editReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'del/$',

        REUNION_PREGUNTA_ASESOR + 'delReunion_preguntaAsesor',
        name='delReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/list/$',
        REUNION_PREGUNTA_ASESOR + 'listReunion_preguntaAsesor',
        name='listReunion_preguntaAsesor'),
)
