from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

PATH = 'asesorias/AdministradorPrincipal/'

# Funcion decoradora para comprobar el administrador principal.
def checkAdministradorPrincipal(funcion):
    def inner(request, *args, **kwargs):
        usuario = request.user
        if usuario.is_authenticated() and usuario.is_staff:
            return funcion(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('logout'))
    return inner

@checkAdministradorPrincipal
@login_required
def administrador_inicio(request):
    return render_to_response(PATH + 'administrador_inicio.html',
        {'user': request.user})

@checkAdministradorPrincipal
@login_required
def administrador_org_institucional(request):
    return render_to_response(
        PATH + 'administrador_org_institucional.html',
        {'user': request.user})

@checkAdministradorPrincipal
@login_required
def administrador_org_docente(request):
    return render_to_response(PATH + 'administrador_org_docente.html',
        {'user': request.user})

@checkAdministradorPrincipal
@login_required
def administrador_alumnos(request):
    return render_to_response(PATH + 'administrador_alumnos.html',
        {'user': request.user})

@checkAdministradorPrincipal
@login_required
def administrador_reuniones(request):
    return render_to_response(PATH + 'administrador_reuniones.html',
        {'user': request.user})

@checkAdministradorPrincipal
@login_required
def administrador_plantillas(request):
    return render_to_response(PATH + 'administrador_plantillas.html',
        {'user': request.user})
