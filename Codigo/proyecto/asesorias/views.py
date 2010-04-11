# Create your views here.
from django.shortcuts import render_to_response
from asesorias.forms import LoginForm

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
	else:
		form = LoginForm()
	return render_to_response('asesorias/login.html', {'form': form})