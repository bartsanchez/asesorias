from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from asesorias import models
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAdministradorCentro/'

# Funcion decoradora para comprobar el centro.
def checkCentro(funcion):
    def inner(request, centro, *args, **kwargs):
        # Se crea una instancia del centro para pasar el nombre de
        # centro por argumento.
        instancia_centro = models.Centro.objects.get(
            nombre_centro=centro)

        # Determina el id del administrador de centro, quitando
        # los 10 primeros caracteres que son: 'AdminCentro'.
        user = unicode(request.user)[11:]

        try:
            models.CentroAdministradorCentro.objects.get(
                id_centro=instancia_centro.id_centro,
                id_adm_centro=user)
        except:
            return HttpResponseRedirect(reverse('logout'))
        return funcion(request, centro, *args, **kwargs)
    return inner

@checkCentro
@login_required
def administradorCentro_inicio(request, centro):
    return render_to_response(PATH + 'administradorCentro_inicio.html',
        {'user': request.user, 'centro': centro})

@checkCentro
@login_required
def administradorCentro_org_institucional(request, centro):
    return render_to_response(
        PATH + 'administradorCentro_org_institucional.html',
        {'user': request.user, 'centro': centro})

@checkCentro
@login_required
def administradorCentro_org_docente(request, centro):
    return render_to_response(PATH +
        'administradorCentro_org_docente.html',
        {'user': request.user, 'centro': centro})


