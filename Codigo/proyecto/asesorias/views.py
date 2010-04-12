# Create your views here.
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm
from django.contrib.auth import authenticate, login

def login(request):

	def errorHandle(error):
		form = LoginForm()
		return render_to_response('asesorias/login.html', {
				'error' : error,
				'form' : form,
		})

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					error = u'exito'
					return errorHandle(error)
				# Redirect to a success page.
				else:
					error = u'Cuenta desactivada.'
					return errorHandle(error)
				# Return a 'disabled account' error message
			else:
				error = u'Login no valido.'
				return errorHandle(error)
			# Return an 'invalid login' error message.
		else:
			error = u'Formulario erroneo'
			return errorHandle(error)
	else:
		form = LoginForm()
	return render_to_response('asesorias/login.html', {'form': form})