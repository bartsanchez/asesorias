from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un centro y, de ser asi, lo devuelve.
def obtenerCentro(centro):
	try:
		# Obtiene el centro cuyo nombre es centro.
		resultado = models.Centro.objects.get(nombre_centro=centro)
	except:
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
			# Redirige a la pagina de listar centros.
			return HttpResponseRedirect( reverse('listCentro') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.CentroForm()
		error = False
	return render_to_response('asesorias/Centro/addCentro.html', {'form': form})

def editCentro(request, centro):
	# Se obtiene la instancia del centro.
	instancia_centro = obtenerCentro(centro)
	# Si existe se edita.
	if instancia_centro:
		# Se carga el formulario para el centro existente.
		form = forms.CentroForm(instance=instancia_centro)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.CentroForm(request.POST, instance=instancia_centro)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar centros.
				return HttpResponseRedirect( reverse('listCentro') )
	# El centro no existe.
	else:
		form = False
	return render_to_response('asesorias/Centro/editCentro.html', {'form': form})

def delCentro(request, centro):
	# Se obtiene la instancia del centro.
	instancia_centro = obtenerCentro(centro)
	# Si existe se elimina.
	if instancia_centro:
		instancia_centro.delete()
		# Redirige a la pagina de listar centros.
		return HttpResponseRedirect( reverse('listCentro') )
	# El centro no existe.
	else:
		error = True
	return render_to_response('asesorias/Centro/delCentro.html', {'error': error})

def listCentro(request):
	# Se obtiene una lista con todos los centros.
	lista_centros = models.Centro.objects.all()
	return render_to_response('asesorias/Centro/listCentro.html', {'lista_centros': lista_centros})
