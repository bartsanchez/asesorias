from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/AdministradorPrincipal/'

@login_required()
def administrador_inicio(request):
    return render_to_response(PATH + 'administrador_inicio.html',
        {'user': request.user})

@login_required()
def administrador_org_institucional(request):
    return render_to_response(
        PATH + 'administrador_org_institucional.html',
        {'user': request.user})

@login_required()
def administrador_org_docente(request):
    return render_to_response(PATH + 'administrador_org_docente.html',
        {'user': request.user})

@login_required()
def administrador_alumnos(request):
    return render_to_response(PATH + 'administrador_alumnos.html',
        {'user': request.user})

@login_required()
def administrador_reuniones(request):
    return render_to_response(PATH + 'administrador_reuniones.html',
        {'user': request.user})

@login_required()
def administrador_plantillas(request):
    return render_to_response(PATH + 'administrador_plantillas.html',
        {'user': request.user})
