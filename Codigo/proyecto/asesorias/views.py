# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm

def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
	else:
		form = AuthenticationForm()
	return render_to_response('asesorias/login.html', {'form': form})