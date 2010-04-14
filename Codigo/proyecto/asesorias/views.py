from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import forms, models

def authentication(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			# Se autentifica el usuario.
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			# Si existe el usuario.
			if user is not None:
				if user.is_active:
					login(request, user)
					# Obtiene el rol del usuario (Administrador centro, asesor o alumno).
					rol = obtenerRol(username)
					# Si es alumno se redirige a la pagina de alumnos.
					if rol == 'alumno':
						return HttpResponseRedirect(reverse('proyecto.asesorias.views.alumnos', args=(username,)))
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
	return render_to_response('asesorias/autentificacion.html', {'form': form, 'error': error})

def obtenerRol(username):
	if esAdministradorCentro(username):
		rol = 'administradorCentro'
	elif esAsesor(username):
		rol = 'asesor'
	elif esAlumno(username):
		rol = 'alumno'
	else:
		rol = 'inactivo'
	return rol

# Comprueba si el usuario es Administrador de centro.
def esAdministradorCentro(username):
	try:
		models.AdministradorCentro.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

# Comprueba si el usuario es Asesor.
def esAsesor(username):
	try:
		models.Asesor.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

# Comprueba si el usuario es Alumno.
def esAlumno(username):
	try:
		models.Alumno.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

@login_required()
def alumnos(request, username):
	if esAlumno(username):
		alumno = models.Alumno.objects.get(pk=username)
		return render_to_response('asesorias/alumnos.html', {'alumno': alumno})
	else:
		error = True
		return render_to_response('asesorias/alumnos.html', {'error': error})

def addCentro(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.CentroForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Se redirige
			return HttpResponseRedirect('/asesorias')
		else:
			error = 'Formulario invalido'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.CentroForm()
		error = 'sin errores'
	return render_to_response('asesorias/addCentro.html', {'form': form, 'error': error})

def editCentro(request, centro):
	# Comprobamos que exista el centro.
	try:
		c = models.Centro.objects.get(nombre_centro=centro)
		# Obtiene los datos del centro.
		form = forms.CentroForm(instance=c)
		error = False
		return render_to_response('asesorias/editCentro.html', {'form': form, 'error': error})
	# El centro no existe
	except:
		error = True
	return render_to_response('asesorias/editCentro.html', {'error': error})
