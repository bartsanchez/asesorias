from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAlumno/'

@login_required()
def alumno_inicio(request, curso_academico):
    return render_to_response(PATH + 'alumno_inicio.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def alumno_informacion_personal(request, curso_academico):
    return render_to_response(
        PATH + 'alumno_informacion_personal.html',
        {'user': request.user, 'curso_academico': curso_academico})
