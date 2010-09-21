from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import forms, models
from datetime import date
from asesorias.vistas.AdministradorPrincipal import \
    vistasAdministradorCentro, vistasAsesor, vistasAlumno

# Vista que controla la autentificacion en el sistema.
def authentication(request):
    error = ''
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Se autentifica el usuario.
            username = request.POST['username']
            password = request.POST['password']
            rol = request.POST['rol']
            user = authenticate(username=username, password=password)
            # Si existe el usuario.
            if user is not None:
                if user.is_active:
                    login(request, user)

                    curso_academico = determinarCursoAcademico()

                    if rol == 'administradorPrincipal':
                        # Comprueba si el usuario es administrador
                        # principal.
                        if user.is_superuser:
                            return HttpResponseRedirect(
                                reverse('administrador_inicio'))

                    elif rol == 'administradorCentro':
                        print 'hola'
                    elif rol == 'asesor':
                        return HttpResponseRedirect(
                            reverse('asesor_inicio',
                            kwargs={'curso_academico':curso_academico}))
                    elif rol == 'alumno':
                        return HttpResponseRedirect(
                            reverse('alumno_inicio'))

                else:
                    error = 'Cuenta desactivada.'
            else:
                error = 'Login no valido.'
        else:
            error = 'Formulario erroneo.'
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.LoginForm()
        error = ''
    return render_to_response('asesorias/Login/login.html',
        {'form': form, 'error': error})

# Vista que controla la salida del sistema de un usuario.
def logout_view(request):
    logout(request)

    # Redirige a la pagina inicial.
    return HttpResponseRedirect( reverse('authentication') )

def determinarCursoAcademico():
    today = date.today()

    # Comprueba si ha llegado septiembre para devolver un curso
    # academico o el siguiente.
    if (today.month < 9):
        curso_academico = today.year
    else:
        curso_academico = (today.year + 1)

    return curso_academico

# Determina el con el que participa un usuario de la aplicacion.
def obtenerRol(username):
    if vistasAdministradorCentro.obtenerAdministradorCentro(username):
        rol = 'administradorCentro'
    elif vistasAsesor.obtenerAsesor(username):
        rol = 'asesor'
    elif vistasAlumno.obtenerAlumno(username):
        rol = 'alumno'
    else:
        rol = 'inactivo'
    return rol
