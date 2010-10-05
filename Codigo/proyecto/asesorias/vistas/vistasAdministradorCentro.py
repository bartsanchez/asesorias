from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

PATH = 'asesorias/UsuarioAdministradorCentro/'

@login_required()
def administradorCentro_inicio(request):
    return render_to_response(PATH + 'administradorCentro_inicio.html',
        {'user': request.user})
