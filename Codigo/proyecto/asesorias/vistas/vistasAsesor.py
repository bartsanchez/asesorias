from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAsesor/'

@login_required()
def asesor_inicio(request, curso_academico):
    return render_to_response(PATH + 'asesor_inicio.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_informacion_personal(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_informacion_personal.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_alumnos(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_alumnos.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_plantillas(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_plantillas.html',
        {'user': request.user, 'curso_academico': curso_academico})
