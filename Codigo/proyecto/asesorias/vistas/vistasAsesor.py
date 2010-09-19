from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAsesor/'

@login_required()
def asesor_inicio(request):
    return render_to_response(PATH + 'asesor_inicio.html',
        {'user': request.user})

@login_required()
def asesor_informacion_personal(request):
    return render_to_response(
        PATH + 'asesor_informacion_personal.html',
        {'user': request.user})

@login_required()
def asesor_alumnos(request):
    return render_to_response(
        PATH + 'asesor_alumnos.html',
        {'user': request.user})
