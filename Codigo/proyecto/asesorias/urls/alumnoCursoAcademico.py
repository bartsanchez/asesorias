from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ------------------------------- #
# Url's de alumno curso academico #
# ------------------------------- #

urlpatterns = patterns(VISTAS + 'vistasAlumnoCursoAcademico',
    url(r'^add/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<dni_pasaporte_alumno>[\s\w]+)/$',

        'addAlumnoCursoAcademico', name='addAlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/edit/$',

        'editAlumnoCursoAcademico', name='editAlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/del/$',

        'delAlumnoCursoAcademico', name='delAlumnoCursoAcademico'),

    url(r'^list/(?P<dni_pasaporte_asesor>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<orden>[\s\w]*)/$',

        'listAlumnoCursoAcademico', name='listAlumnoCursoAcademico'),

    url(r'^selectAsesor/(?P<tipo>[\s\w]+)/$',
        'selectAsesor', name='selectAsesor_AlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAsesorCursoAcademico/' +
        '(?P<tipo>[\s\w]+)/$',

        'selectAsesorCursoAcademico',
        name='selectAsesorCA_AlumnoCursoAcademico'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/' +
        'selectAlumno/(?P<tipo>[\s\w]+)/$',

        'selectAlumno', name='selectAlumno_AlumnoCursoAcademico'),

    url(r'^generarPDF/(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<busqueda>[\s\w]+)/$',

        'generarPDFListaAlumnosCursoAcademico',
        name='generarPDFListaAlumnosCursoAcademico'),
)
