from django.conf.urls.defaults import *
from proyecto import asesorias

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

VISTAS = 'asesorias.vistas.'

# ----------------- #
# Url's principales #
# ----------------- #

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url(r'^asesorias/asesor/$', 'asesorias.views.asesor',
        name='vista_asesor'),

    url(r'^asesorias/alumno/$', 'asesorias.views.alumno',
        name='vista_alumno'),

    (r'^asesorias/administrador/',
        include('asesorias.urls.administradorPrincipal')),

    (r'^asesorias/centro/',
        include('asesorias.urls.centro')),

    (r'^asesorias/administradorCentro/',
        include('asesorias.urls.administradorCentro')),

    (r'^asesorias/titulacion/',
        include('asesorias.urls.titulacion')),

    (r'^asesorias/asignatura/',
        include('asesorias.urls.asignatura')),

    (r'^asesorias/asignaturaCursoAcademico/',
        include('asesorias.urls.asignaturaCursoAcademico')),
)

# ------------------------- #
# Url's gestion de usuarios #
# ------------------------- #

urlpatterns += patterns(VISTAS + 'vistasGestionUsuarios',
    url(r'^asesorias/$', 'authentication', name='authentication'),

    url(r'^asesorias/logout/$', 'logout_view', name='logout'),
)

# --------------------- #
# Url's de departamento #
# --------------------- #

urlpatterns += patterns(VISTAS + 'vistasDepartamento',
    url(r'^asesorias/departamento/add/$',
        'addDepartamento', name='addDepartamento'),

    url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/' +
        'edit/$',

        'editDepartamento', name='editDepartamento'),

    url(r'^asesorias/departamento/(?P<nombre_departamento>[\s\w]+)/' +
        'del/$',

        'delDepartamento', name='delDepartamento'),

    url(r'^asesorias/departamento/list/(?P<orden>[\s\w]*)/$',
        'listDepartamento', name='listDepartamento'),

    url(r'^asesorias/departamento/generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaDepartamentos',
        name='generarPDFListaDepartamentos'),
)

# --------------- #
# Url's de asesor #
# --------------- #

urlpatterns += patterns(VISTAS + 'vistasAsesor',
    url(r'^asesorias/asesor/add/$',
        'addAsesor', name='addAsesor'),

    url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/edit/$',
        'editAsesor', name='editAsesor'),

    url(r'^asesorias/asesor/(?P<dni_pasaporte>[\s\w]+)/del/$',
        'delAsesor', name='delAsesor'),

    url(r'^asesorias/asesor/list/(?P<orden>[\s\w]*)/$',
        'listAsesor', name='listAsesor'),

    url(r'^asesorias/asesor/generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaAsesores',
        name='generarPDFListaAsesores'),
)

# ------------------------------- #
# Url's de asesor curso academico #
# ------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasAsesorCursoAcademico',
    url(r'^asesorias/asesorCursoAcademico/add/' +
        '(?P<nombre_departamento>[\s\w]*)/(?P<dni_pasaporte>[\s\w]*)/$',

         'addAsesorCursoAcademico', name='addAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        'editAsesorCursoAcademico', name='editAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        'delAsesorCursoAcademico', name='delAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<orden>[\s\w]*)/list/$',

        'listAsesorCursoAcademico', name='listAsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/selectAsesor/$',
        'selectAsesor', name='selectAsesor_AsesorCursoAcademico'),

    url(r'^asesorias/asesorCursoAcademico/generarPDF/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAsesoresCursoAcademico',
        name='generarPDFListaAsesoresCursoAcademico'),
)

# ------------------------------------------- #
# Url's de plantillas de entrevista de asesor #
# ------------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasPlantillaEntrevistaAsesor',
    url(r'^asesorias/plantillaEntrevistaAsesor/add/$',
        'addPlantillaEntrevistaAsesor',
        name='addPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/edit/$',

        'editPlantillaEntrevistaAsesor',
        name='editPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_entrevista_asesor>\d+)/del/$',

        'delPlantillaEntrevistaAsesor',
        name='delPlantillaEntrevistaAsesor'),

    url(r'^asesorias/plantillaEntrevistaAsesor/list/$',
        'listPlantillaEntrevistaAsesor',
        name='listPlantillaEntrevistaAsesor'),
)

# -----------------------------#
# Url's de preguntas de asesor #
# -----------------------------#

urlpatterns += patterns(VISTAS + 'vistasPreguntaAsesor',
    url(r'^asesorias/preguntaAsesor/add/$',
        'addPreguntaAsesor', name='addPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/edit/$',

        'editPreguntaAsesor', name='editPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_entrevista_asesor>\d+)/' +
        '(?P<id_pregunta_asesor>\d+)/del/$',

        'delPreguntaAsesor', name='delPreguntaAsesor'),

    url(r'^asesorias/preguntaAsesor/list/$',
        'listPreguntaAsesor', name='listPreguntaAsesor'),
)

# ----------------#
# Url's de alumno #
# ----------------#

urlpatterns += patterns(VISTAS + 'vistasAlumno',
    url(r'^asesorias/alumno/add/$',
        'addAlumno', name='addAlumno'),

    url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/edit/$',
        'editAlumno', name='editAlumno'),

    url(r'^asesorias/alumno/(?P<dni_pasaporte>[\s\w]+)/del/$',
        'delAlumno', name='delAlumno'),

    url(r'^asesorias/alumno/list/(?P<orden>[\s\w]*)/$',
        'listAlumno', name='listAlumno'),

    url(r'^asesorias/alumno/generarPDF/(?P<busqueda>[\s\w]+)/$',
        'generarPDFListaAlumnos',
        name='generarPDFListaAlumnos'),
)

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasAlumnoCursoAcademico',
    url(r'^asesorias/alumnoCursoAcademico/add/$',
        'addAlumnoCursoAcademico', name='addAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/edit/$',

        'editAlumnoCursoAcademico', name='editAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/del/$',

        'delAlumnoCursoAcademico', name='delAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/list/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/selectAlumno/$',
        'selectAlumno', name='selectAlumno_AlumnoCursoAcademico'),

    url(r'^asesorias/alumnoCursoAcademico/generarPDF/' +
        '(?P<dni_pasaporte>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAlumnosCursoAcademico',
        name='generarPDFListaAlumnosCursoAcademico'),
)

# ------------------ #
# Url's de matricula #
# ------------------ #

urlpatterns += patterns(VISTAS + 'vistasMatricula',
    url(r'^asesorias/matricula/add/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/$',

        'addMatricula', name='addMatricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/edit/$',

        'editMatricula', name='editMatricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<dni_pasaporte>[\s\w]+)/del/$',

        'delMatricula', name='delMatricula'),

    url(r'^asesorias/matricula/list/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<orden>[\s\w]*)/$',

        'listMatricula', name='listMatricula'),

    url(r'^asesorias/matricula/select/$',
        'selectAsignaturaOAlumnoCursoAcademico',
        name='selectAsignaturaOAlumnoCursoAcademico'),

    url(r'^asesorias/matricula/selectCentro/(?P<tipo>[\s\w]+)/$',
        'selectCentro', name='selectCentro_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        'selectTitulacion/(?P<tipo>[\s\w]+)/$',

        'selectTitulacion', name='selectTitulacion_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        'selectAsignatura/(?P<tipo>[\s\w]+)/$',

        'selectAsignatura', name='selectAsignatura_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/' +
        'selectAsignaturaCursoAcademico/(?P<tipo>[\s\w]+)/$',

        'selectAsignaturaCursoAcademico',
        name='selectAsignaturaCursoAcademico_Matricula'),

    url(r'^asesorias/matricula/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/$',

        'selectAlumno', name='selectAlumno_Matricula'),

    url(r'^asesorias/matricula/generarPDF/(?P<nombre_centro>[\s\w]+)/' +
        '(?P<nombre_titulacion>[\s\w]+)/(?P<plan_estudios>\d+)/' +
        '(?P<nombre_asignatura>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaMatriculas', name='generarPDFListaMatriculas'),
)

# ---------------------------------- #
# Url's de calificacion convocatoria #
# ---------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasCalificacionConvocatoria',
    url(r'^asesorias/calificacionConvocatoria/add/$',
        'addCalificacionConvocatoria',
        name='addCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/edit/$',

        'editCalificacionConvocatoria',
        name='editCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/' +
        '(?P<nombre_centro>[\s\w]+)/(?P<nombre_titulacion>[\s\w]+)/' +
        '(?P<plan_estudios>\d+)/(?P<nombre_asignatura>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<convocatoria>[\s\w]+)/del/$',

        'delCalificacionConvocatoria',
        name='delCalificacionConvocatoria'),

    url(r'^asesorias/calificacionConvocatoria/list/$',
        'listCalificacionConvocatoria',
        name='listCalificacionConvocatoria'),
)

# ---------------------------------------- #
# Url's de plantilla de entrevista oficial #
# ---------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasPlantillaEntrevistaOficial',
    url(r'^asesorias/plantillaEntrevistaOficial/add/$',
        'addPlantillaEntrevistaOficial',
        name='addPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/edit/$',

        'editPlantillaEntrevistaOficial',
        name='editPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/' +
        '(?P<id_entrevista_oficial>[\s\w]+)/del/$',

        'delPlantillaEntrevistaOficial',
        name='delPlantillaEntrevistaOficial'),

    url(r'^asesorias/plantillaEntrevistaOficial/list/$',
        'listPlantillaEntrevistaOficial',
        name='listPlantillaEntrevistaOficial'),
)

# ---------------------------- #
# Url's de preguntas oficiales #
# ---------------------------- #

urlpatterns += patterns(VISTAS + 'vistasPreguntaOficial',
    url(r'^asesorias/preguntaOficial/add/$',
        'addPreguntaOficial', name='addPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/edit/$',

        'editPreguntaOficial', name='editPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/(?P<id_entrevista_oficial>\d+)/' +
        '(?P<id_pregunta_oficial>\d+)/del/$',

        'delPreguntaOficial', name='delPreguntaOficial'),

    url(r'^asesorias/preguntaOficial/list/$',
        'listPreguntaOficial', name='listPreguntaOficial'),
)

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns += patterns(VISTAS + 'vistasReunion',
    url(r'^asesorias/reunion/add/$',
        'addReunion', name='addReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        'editReunion', name='editReunion'),

    url(r'^asesorias/reunion/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        'delReunion', name='delReunion'),

    url(r'^asesorias/reunion/list/$',
        'listReunion', name='listReunion'),
)

# ----------------------------------------- #
# Url's de centro - administrador de centro #
# ----------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasCentro_administradorCentro',
    url(r'^asesorias/centro_administradorCentro/add/' +
        '(?P<nombre_centro>[\s\w]*)/$',

        'addCentro_administradorCentro',
        name='addCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/edit/$',

        'editCentro_administradorCentro',
        name='editCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/(?P<centro>[\s\w]+)/' +
        '(?P<administrador_centro>[\s\w]+)/del/$',

        'delCentro_administradorCentro',
        name='delCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/list/' +
        '(?P<centro>[\s\w]+)/(?P<orden>[\s\w]*)/$',

        'listCentro_administradorCentro',
        name='listCentro_administradorCentro'),

    url(r'^asesorias/centro_administradorCentro/select/$',
        'selectCentro',
        name='selectCentro_CentroAdministradorCentro'),

    url(r'^asesorias/centro_administradorCentro/generarPDF/' +
        '(?P<centro>[\s\w]+)/(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaCentros_administradorCentro',
        name='generarPDFListaCentros_administradorCentro'),
)

# ------------------------------------- #
# Url's de reunion - pregunta de asesor #
# ------------------------------------- #

urlpatterns += patterns(VISTAS + 'vistasReunion_preguntaAsesor',
    url(r'^asesorias/reunion_preguntaAsesor/add/$',
        'addReunion_preguntaAsesor',
        name='addReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'edit/$',

        'editReunion_preguntaAsesor',
        name='editReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/' +
        '(?P<dni_pasaporte_alumno>[\s\w]+)/(?P<curso_academico>\d+)/' +
        '(?P<id_reunion>\d+)/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<id_entrevista_asesor>\d+)/(?P<id_pregunta_asesor>\d+)/' +
        'del/$',

        'delReunion_preguntaAsesor',
        name='delReunion_preguntaAsesor'),

    url(r'^asesorias/reunion_preguntaAsesor/list/$',
        'listReunion_preguntaAsesor',
        name='listReunion_preguntaAsesor'),
)
