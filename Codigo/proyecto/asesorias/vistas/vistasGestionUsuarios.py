#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
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
                        return HttpResponseRedirect(
                            reverse(
                            'determinarCentro_AdministradorCentro'))
                    elif rol == 'asesor':
                        return HttpResponseRedirect(
                            reverse('asesor_inicio',
                            kwargs={'curso_academico':curso_academico}))
                    elif rol == 'alumno':
                        return HttpResponseRedirect(
                            reverse('alumno_inicio',
                            kwargs={'curso_academico':curso_academico}))

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

def determinarCentro_AdministradorCentro(request):
    # Se ha introducido un centro.
    if request.method == 'POST':

        # Se obtiene el centro y se valida.
        form = forms.CentroFormSelect(request.POST)

        # Si es valido se redirige a listar centros.
        if form.is_valid():
            centro = request.POST['centro']

            # Se crea una instancia del centro para pasar el nombre de
            # centro por argumento.
            instancia_centro = models.Centro.objects.get(pk=centro)

            # Determina el id del administrador de centro, quitando
            # los 10 primeros caracteres que son: 'AdminCentro'.
            user = unicode(request.user)[11:]

            try:
                models.CentroAdministradorCentro.objects.get(
                    id_centro=instancia_centro.id_centro,
                    id_adm_centro=user)
            except:
                return HttpResponseRedirect(
                    reverse('determinarCentro_AdministradorCentro'))
            return HttpResponseRedirect(
                reverse('administradorCentro_inicio',
                kwargs={'centro': instancia_centro.nombre_centro}))
        else:
            HttpResponseRedirect(
                reverse('determinarCentro_AdministradorCentro'))

    else:
        form = forms.CentroFormSelect()
    return render_to_response('asesorias/Login/login_admin_centro.html',
        {'user': request.user, 'form': form})

# Vista que controla la salida del sistema de un usuario.
def logout_view(request):
    logout(request)

    # Redirige a la pagina inicial.
    return HttpResponseRedirect( reverse('authentication') )

def determinarCursoAcademico():
    today = date.today()

    # Comprueba si ha llegado septiembre para devolver un curso
    # academico o el anterior.
    if (today.month > 8):
        curso_academico = today.year
    else:
        curso_academico = (today.year - 1)

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

# Funcion para enviar correos electronicos.
def enviar_mail_creacion_usuario(request, correo_destino,
    username, password):
    try:
        tema = 'Asesorías académicas: Registro de usuario'
        contenido = ('Un usuario ha sido creado para este correo ' +
            'electrónico con los siguientes datos:\n\n' +
            'Tipo: Administrador de centro\n' +
            'Usuario: ' + str(username) + '\n' +
            'Contraseña: ' + str(password) + '\n')

        send_mail(tema, contenido, request.user.email, [correo_destino])

        enviado = True
    except:
        enviado = False
    return enviado
