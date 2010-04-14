from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un centro.
def existeCentro(centro):
	try:
		models.Centro.objects.get(nombre_centro=centro)
		resultado = True
	except:
		resultado = False
	return resultado

def obtenerCentro(centro):
	if existeCentro(centro):
		# Obtiene el centro cuyo nombre de centro es nombre_centro.
		resultado = models.Centro.objects.get(nombre_centro=centro)
	else:
		resultado = False
	return resultado

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
	return render_to_response('asesorias/Centro/addCentro.html', {'form': form, 'error': error})

def editCentro(request, centro):
	instancia_centro = obtenerCentro(centro)
	if instancia_centro:
		form = forms.CentroForm(instance=instancia_centro)
		error = False
		return render_to_response('asesorias/Centro/editCentro.html', {'form': form, 'error': error})
	# El centro no existe
	else:
		error = True
	return render_to_response('asesorias/Centro/editCentro.html', {'error': error})

def delCentro(request, centro):
	# Se obtiene la instancia del centro.
	instancia_centro = obtenerCentro(centro)
	# Si existe se elimina.
	if instancia_centro:
		instancia_centro.delete()
		error = False
	# El centro no existe.
	else:
		error = True
	return render_to_response('asesorias/Centro/delCentro.html', {'error': error})
