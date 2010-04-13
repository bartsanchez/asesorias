from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm
from proyecto.asesorias.models import AdministradorCentro, Asesor, Alumno

def authentication(request):
	# Mensaje para visualizar errores.
	msg = []
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = LoginForm(request.POST)
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
					if rol == 'alumno':
						return HttpResponseRedirect(reverse('proyecto.asesorias.views.alumnos', args=(username,)))
				else:
					msg.append('Cuenta desactivada.')
			else:
				msg.append('Login no valido.')
		else:
			msg.append('Formulario erroneo')
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = LoginForm()
	return render_to_response('asesorias/autentificacion.html', {'form': form, 'error': msg})

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
		AdministradorCentro.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

# Comprueba si el usuario es Asesor.
def esAsesor(username):
	try:
		Asesor.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

# Comprueba si el usuario es Alumno.
def esAlumno(username):
	try:
		Alumno.objects.get(pk=username)
		resultado = True
	except:
		resultado = False
	return resultado

@login_required()
def alumnos(request, username):
	if esAlumno(username):
		alumno = Alumno.objects.get(pk=username)
		return render_to_response('asesorias/alumnos.html', {'alumno': alumno})
	else:
		error = True
		return render_to_response('asesorias/alumnos.html', {'error': error})

