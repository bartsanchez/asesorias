# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
					# Redirige a la pagina de alumnos.
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

@login_required()
def alumnos(request, username):
	msg = []
	from proyecto.asesorias.models import Alumno
	alumno = Alumno.objects.get(pk=username)
	msg.append(alumno.correo_electronico)
	return render_to_response('asesorias/alumnos.html', {'alumno': alumno, 'msg': msg})
