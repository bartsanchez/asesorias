# Create your views here.
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm
from django.contrib.auth import authenticate, login

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