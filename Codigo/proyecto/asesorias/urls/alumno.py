from django.conf.urls.defaults import *

VISTAS = 'asesorias.vistas.'
URLS = 'asesorias.urls.Alumno.'

# --------------- #
# Url's de alumno #
# --------------- #

urlpatterns = patterns(VISTAS + 'vistasAlumno',

    ### URLS del menu horizontal. ###

    url(r'^$', 'alumno_inicio', name='alumno_inicio'),

    url(r'^informacion_personal/$',

        'alumno_informacion_personal',
        name='alumno_informacion_personal'),

    url(r'^establecerCursoAcademico/$', 'setCursoAcademico',
        name='setCursoAcademico_Alumno'),

    ### Includes a cada entidad ###

    (r'^info/',
        include(URLS + 'informacionPersonal')),
)
