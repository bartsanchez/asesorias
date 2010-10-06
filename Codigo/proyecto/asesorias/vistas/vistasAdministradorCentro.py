from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAdministradorCentro/'

@login_required()
def administradorCentro_inicio(request, centro):
    return render_to_response(PATH + 'administradorCentro_inicio.html',
        {'user': request.user, 'centro': centro})

@login_required()
def administradorCentro_org_institucional(request, centro):
    return render_to_response(
        PATH + 'administradorCentro_org_institucional.html',
        {'user': request.user, 'centro': centro})

@login_required()
def administradorCentro_org_docente(request, centro):
    return render_to_response(PATH +
        'administradorCentro_org_docente.html',
        {'user': request.user, 'centro': centro})

@login_required()
def administradorCentro_alumnos(request, centro):
    return render_to_response(PATH + 'administradorCentro_alumnos.html',
        {'user': request.user, 'centro': centro})

@login_required()
def administradorCentro_reuniones(request, centro):
    return render_to_response(PATH +
        'administradorCentro_reuniones.html',
        {'user': request.user, 'centro': centro})

@login_required()
def administradorCentro_plantillas(request, centro):
    return render_to_response(PATH +
        'administradorCentro_plantillas.html',
        {'user': request.user, 'centro': centro})

# Funcion decoradora para comprobar el centro.
def checkCentro(funcion):
    def inner(request, centro, *args, **kwargs):
        if centro == 'eps':
            return funcion(request, centro, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('logout'))
    return inner
