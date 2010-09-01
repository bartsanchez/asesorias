from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'

# ---------------- #
# Url's de reunion #
# ---------------- #

urlpatterns = patterns(VISTAS + 'vistasReunion',
    url(r'^add/(?P<dni_pasaporte>[\s\w]*)/' +
        '(?P<curso_academico>[\s\w]*)/$',

        'addReunion', name='addReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/edit/$',

        'editReunion', name='editReunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/' +
        '(?P<curso_academico>\d+)/(?P<id_reunion>\d+)/del/$',

        'delReunion', name='delReunion'),

    url(r'^list/(?P<dni_pasaporte>[\s\w]+)/(?P<curso_academico>\d+)/$',
        'listReunion', name='listReunion'),

    url(r'^selectAlumno/$',
        'selectAlumno', name='selectAlumno_Reunion'),

    url(r'^(?P<dni_pasaporte>[\s\w]+)/selectAlumnoCursoAcademico/$',

        'selectAlumnoCursoAcademico',
        name='selectAlumnoCursoAcademico_Reunion'),
)
