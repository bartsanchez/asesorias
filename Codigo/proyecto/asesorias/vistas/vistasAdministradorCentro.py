from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAdministradorCentro/'

@login_required()
def administradorCentro_inicio(request):
    return render_to_response(PATH + 'administradorCentro_inicio.html',
        {'user': request.user})

@login_required()
def administradorCentro_org_institucional(request):
    return render_to_response(
        PATH + 'administradorCentro_org_institucional.html',
        {'user': request.user})

@login_required()
def administradorCentro_org_docente(request):
    return render_to_response(PATH +
        'administradorCentro_org_docente.html',
        {'user': request.user})

@login_required()
def administradorCentro_alumnos(request):
    return render_to_response(PATH + 'administradorCentro_alumnos.html',
        {'user': request.user})

@login_required()
def administradorCentro_reuniones(request):
    return render_to_response(PATH +
        'administradorCentro_reuniones.html',
        {'user': request.user})

@login_required()
def administradorCentro_plantillas(request):
    return render_to_response(PATH +
        'administradorCentro_plantillas.html',
        {'user': request.user})
