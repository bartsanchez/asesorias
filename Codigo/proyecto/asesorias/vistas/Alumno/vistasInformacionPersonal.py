from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias import models, forms

PATH = 'asesorias/UsuarioAlumno/'

def showInfo(request):
    # Se obtiene la instancia del alumno.
    instancia_alumno = vistasAlumno.obtenerAlumno(request.user)
    # Si existe se edita.
    if instancia_alumno:
        # Se carga el formulario para el alumno existente.
        form = forms.AlumnoForm(instance=instancia_alumno)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            dni_pasaporte = request.user

            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            correo_electronico = request.POST['correo_electronico']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            telefono = request.POST['telefono']

            # Datos necesarios para actualizar el alumno.
            datos_alumno = {'dni_pasaporte': dni_pasaporte,
                'correo_electronico': correo_electronico,
                'nombre': nombre,
                'apellidos': apellidos,
                'telefono': telefono}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.AlumnoForm(datos_alumno,
                instance=instancia_alumno)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar alumnos.
                return HttpResponseRedirect(
                    reverse('alumno_informacion_personal'))
    # El alumno no existe.
    else:
        form = False
    return render_to_response(PATH + 'showInfo.html',
        {'user': request.user, 'form': form})

def modificarClave(request):
    error = False
    user = request.user
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.ModificarClaveForm(request.POST)
        if form.is_valid():
            antigua_clave = request.POST['old_password']
            nueva_clave = request.POST['new_password']

            # Se comprueba que la clave actual sea correcta.
            if (user.check_password(antigua_clave)):
                user.set_password(nueva_clave)
                user.save()

                return HttpResponseRedirect(
                            reverse('asesor_inicio'))
            else:
                error = True

    else:
        form = forms.ModificarClaveForm()
    return render_to_response(PATH + 'modificarClave.html',
        {'user': user, 'form': form, 'error': error})
