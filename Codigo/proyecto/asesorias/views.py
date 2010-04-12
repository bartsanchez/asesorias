# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm


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
					msg.append('exito')
					return HttpResponseRedirect('alumnos/')
					# Redirect to a success page.
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

def alumnos(request):
	#from proyecto.asesorias.models import Alumno
	#alumno = Alumno(dni_pasaporte='123456789')
	msg = 'hola'
	return render_to_response('asesorias/alumnos.html', {'msg': msg})
