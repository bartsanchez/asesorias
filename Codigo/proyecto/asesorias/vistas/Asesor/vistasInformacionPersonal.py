from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

@login_required
def showInfo(request, curso_academico):
    user = unicode(request.user)

    # Se obtiene la instancia del asesor.
    instancia_asesor = vistasAsesor.obtenerAsesor(user)
    # Si existe se edita.
    if instancia_asesor:
        # Se carga el formulario para el asesor existente.
        form = forms.AsesorForm(instance=instancia_asesor)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            dni_pasaporte = user

            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            correo_electronico = request.POST['correo_electronico']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            telefono = request.POST['telefono']

            # Datos necesarios para actualizar el asesor.
            datos_asesor = {'dni_pasaporte': dni_pasaporte,
                'correo_electronico': correo_electronico,
                'nombre': nombre,
                'apellidos': apellidos,
                'telefono': telefono}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.AsesorForm(datos_asesor,
                instance=instancia_asesor)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar asesores.
                return HttpResponseRedirect(
                    reverse('asesor_informacion_personal',
                    kwargs={'curso_academico': curso_academico}))
    # El asesor no existe.
    else:
        form = False
    return render_to_response(PATH + 'showInfo.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico})

@login_required
def modificarClave(request, curso_academico):
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
                        reverse('asesor_inicio',
                        kwargs={'curso_academico': curso_academico}))
                else:
                    error = True
            else:
                error = True
    else:
        form = forms.ModificarClaveForm()
    return render_to_response(PATH + 'modificarClave.html',
        {'user': user, 'form': form, 'error': error,
        'curso_academico': curso_academico})
