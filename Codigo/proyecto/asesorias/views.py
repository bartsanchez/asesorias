# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm
from proyecto.asesorias.models import AdministradorCentro, Asesor, Alumno


def authentication(request):
	msg = []
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					# Redirige a la pagina de alumnos.
					rol = obtenerRol(username)
					if rol == 'alumno':
						return HttpResponseRedirect(reverse('proyecto.asesorias.views.alumnos', args=(username,)))
				else:
					msg.append('Cuenta desactivada.')
				# Return a 'disabled account' error message
			else:
				msg.append('Login no valido.')
			# Return an 'invalid login' error message.
		else:
			msg.append('Formulario erroneo')
	else:
		form = LoginForm()
	return render_to_response('asesorias/autentificacion.html', {'form': form, 'error': msg})


def obtenerRol(username):
	def esAdministradorCentro():
		try:
			AdministradorCentro.objects.get(pk=username)
			resultado = True
		except:
			resultado = False
		return resultado

	def esAsesor():
		try:
			Asesor.objects.get(pk=username)
			resultado = True
		except:
			resultado = False
		return resultado

	def esAlumno():
		try:
			a = Alumno.objects.get(pk=username)
			resultado = True
		except:
			resultado = False
		return resultado

	if esAdministradorCentro():
		rol = 'administradorCentro'
	elif esAsesor():
		rol = 'asesor'
	elif esAlumno():
		rol = 'alumno'
	else:
		rol = 'inactivo'
	return rol

@login_required()
def alumnos(request, username):
	try:
		alumno = Alumno.objects.get(pk=username)
		return render_to_response('asesorias/alumnos.html', {'alumno': alumno})
	except:
		error = True
		return render_to_response('asesorias/alumnos.html', {'error': error})

