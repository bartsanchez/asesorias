from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un administrador de centro.
def existeAdministradorCentro(admin_centro):
	try:
		models.AdministradorCentro.objects.get(pk=admin_centro)
		resultado = True
	except:
		resultado = False
	return resultado

def addAdministradorCentro(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AdministradorCentroForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AdministradorCentroForm()
		error = False
	return render_to_response('asesorias/AdministradorCentro/addAdministradorCentro.html', {'form': form, 'error': error})
