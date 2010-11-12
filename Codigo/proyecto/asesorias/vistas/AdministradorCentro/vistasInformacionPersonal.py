from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias import models, forms

PATH = 'asesorias/UsuarioAdministradorCentro/'

def modificarClave(request, centro):
    error = False
    user = request.user
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.ModificarClaveForm(request.POST)
        if form.is_valid():
            antigua_clave = request.POST['old_password']
            nueva_clave = request.POST['new_password']
            nueva_clave2 = request.POST['new_password2']

            # Se comprueba que la clave actual sea correcta.
            if (user.check_password(antigua_clave)):

                # Comprueba que haya insertado dos veces la misma nueva
                # clave.
                if (nueva_clave == nueva_clave2):
                    user.set_password(nueva_clave)
                    user.save()

                    return HttpResponseRedirect(
                        reverse('administradorCentro_inicio',
                        kwargs={'centro': centro}))
                else:
                    error = True
            else:
                error = True

    else:
        form = forms.ModificarClaveForm()
    return render_to_response(PATH + 'InformacionPersonal/' +
        'modificarClave.html',
        {'user': user, 'form': form, 'error': error,
        'centro': centro})
