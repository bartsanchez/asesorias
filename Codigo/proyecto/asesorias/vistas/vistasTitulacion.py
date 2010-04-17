from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasCentro

# Comprueba si existe una titulacion y, de ser asi, la devuelve.
def obtenerTitulacion(centro, titulacion):
	try:
		# Obtiene la instancia de centro para posteriormente obtener el id.
		instancia_centro = vistasCentro.obtenerCentro(centro)
		# Obtiene la titulacion cuyo centro es centro y el nombre de la titulacion es nombre_titulacion.
		resultado = models.Titulacion.objects.get(id_centro=instancia_centro.getId(), nombre_titulacion=titulacion)
	except:
		resultado = False
	return resultado

# Obtiene una lista con las titulaciones de un determinado centro.
def obtenerTitulacionesDeCentro(centro):
	try:
		instancia_centro = vistasCentro.obtenerCentro(centro)
		# Obtiene todas las titulaciones que pertenece al centro pasado por argumento.
		resultado = models.Titulacion.objects.filter(id_centro=instancia_centro.getId())
	except:
		resultado = False
	return resultado

# Obtiene una lista ordenada con los ids de las titulaciones de un determinado centro.
def obtenerListaDeIdsTitulacionesDeCentro(centro):
	# Se comprueba si existe el centro.
	existe_centro = vistasCentro.obtenerCentro(centro)

	if existe_centro:
		# Se obtiene una lista con las titulaciones de un determinado centro.
		lista_titulaciones_de_centro = obtenerTitulacionesDeCentro(centro)
		# Lista que albergara los ids de los centros.
		lista_ids_titulaciones = []

		# Si existen titulaciones en el centro se extraen sus ids.
		if lista_titulaciones_de_centro:
			# Por cada titulacion del centro se extrae su id y se inserta en la nueva lista.
			for titulacion in lista_titulaciones_de_centro:
				lista_ids_titulaciones.append(titulacion.id_titulacion)
			# Ordena la lista con los ids de las titulaciones de menor a mayor.
			lista_ids_titulaciones.sort()
		# Resultado sera una lista de ids, o una lista vacia si el centro no tiene titulaciones
		resultado = lista_ids_titulaciones
	# En el caso de que no exista el centro se devuelve False.
	else:
		resultado = False

	return resultado

#def determinarSiguienteIdTitulacionEnCentro(centro):
	#while True:
		#if

def addTitulacion(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.TitulacionForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.TitulacionForm()
		error = False
	return render_to_response('asesorias/Titulacion/addTitulacion.html', {'form': form, 'error': error})

#def editTitulacion(request, titulacion):
	## Se obtiene la instancia de la titulacion.
	#instancia_titulacion = obtenerTitulacion(titulacion)
	## Si existe se edita.
	#if instancia_titulacion:
		## Se carga el formulario para la titulacion existente.
		#form = forms.TitulacionForm(instance=titulacion)
		#error = False
		## Se ha modificado el formulario original.
		#if request.method == 'POST':
			## Se actualiza el formulario con la nueva informacion.
			#form = forms.TitulacionForm(request.POST, instance=instancia_titulacion)
			## Si es valido se guarda.
			#if form.is_valid():
				#form.save()
				## Redirige a la pagina de inicio.
				#return HttpResponseRedirect('/asesorias/')
			#else:
				#error = 'Formulario invalido'
		#return render_to_response('asesorias/Titulacion/editTitulacion.html', {'form': form, 'error': error})
	## La titulacion no existe
	#else:
		#error = True
	#return render_to_response('asesorias/Titulacion/editTitulacion.html', {'error': error})

#def delTitulacion(request, titulacion):
	## Se obtiene la instancia de la titulacion.
	#instancia_titulacion= obtenerTitulacion(titulacion)
	## Si existe se elimina.
	#if instancia_titulacion:
		#instancia_titulacion.delete()
		#error = False
	## La titulacion no existe.
	#else:
		#error = 'No se ha podido eliminar la titulacion.'
	#return render_to_response('asesorias/Titulacion/delTitulacion.html', {'error': error})