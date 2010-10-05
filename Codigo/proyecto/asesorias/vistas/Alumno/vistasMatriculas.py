from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias import models, forms

PATH = 'asesorias/UsuarioAlumno/'

def showMatriculacionActual(request, curso_academico):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia del alumno.
    instancia_alumno = vistasAlumno.obtenerAlumno(dni_pasaporte)
    # Si existe se edita.
    if instancia_alumno:
        # Se comprueba las matriculas del curso academico actual del
        # alumno.
        lista_matriculas = models.Matricula.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico).order_by('curso_academico')
    # El alumno no existe.
    else:
        form = False
        lista_matriculas = ''
    return render_to_response(PATH + 'showMatriculacionActual.html',
        {'user': request.user,
        'curso_academico': curso_academico,
        'lista_matriculas': lista_matriculas})
