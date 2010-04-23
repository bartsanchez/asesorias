from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasCentro

# Comprueba si existe una titulacion y, de ser asi, la devuelve.
def obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios):
	try:
		# Obtiene la instancia de centro para posteriormente obtener el id.
		instancia_centro = vistasCentro.obtenerCentro(nombre_centro)
		# Obtiene la titulacion cuyo centro es centro y el nombre de la titulacion es nombre_titulacion.
		resultado = models.Titulacion.objects.get(id_centro=instancia_centro.getId(), nombre_titulacion=nombre_titulacion, plan_estudios=plan_estudios)
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

# Determina el primer id_titulacion disponible para un determinado centro.
def determinarSiguienteIdTitulacionEnCentro(instancia_centro):
	# Se obtiene una lista ordenada con los ids de las titulaciones existentes en el centro.
	lista_ids_titulaciones= obtenerListaDeIdsTitulacionesDeCentro(instancia_centro.nombre_centro)

	# Inicializamos el contador a 1, que es el primer valor valido para un id.
	contador = 1
	# Recorre el bucle determinando si una posicion se encuentra o no.
	while True:
		# La posicion determinada por contador aparece en la lista, por lo tanto se encuentra la id_titulacion en el centro.
		if lista_ids_titulaciones.count(contador) > 0:
			contador += 1
		# No existe tal id_titulacion en el centro.
		else:
			break
	return contador

def addTitulacion(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		id_centro = request.POST['id_centro']
		nombre_titulacion = request.POST['nombre_titulacion']
		plan_estudios = request.POST['plan_estudios']

		# Se obtiene una instancia del centro a traves de su id.
		instancia_centro = models.Centro.objects.get(pk=id_centro)

		# Se determina el siguiente id_titulacion para el centro.
		id_titulacion = determinarSiguienteIdTitulacionEnCentro(instancia_centro)

		# Datos necesarios para crear la nueva titulacion
		datos_titulacion = {'id_centro': id_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'id_titulacion': id_titulacion}

		# Se obtienen los valores y se valida.
		form = forms.TitulacionForm(datos_titulacion)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/titulacion/list')
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.TitulacionForm()
	return render_to_response('asesorias/Titulacion/addTitulacion.html', {'form': form})

def editTitulacion(request, nombre_centro, nombre_titulacion, plan_estudios):
	# Se obtiene la instancia de la titulacion.
	instancia_titulacion = obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios)
	# Si existe se edita.
	if instancia_titulacion:
		# Se carga el formulario para la titulacion existente.
		form = forms.TitulacionForm(instance=instancia_titulacion)
		error = False
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se obtienen el resto de valores necesarios a traves de POST.
			id_centro = request.POST['id_centro']
			nombre_titulacion = request.POST['nombre_titulacion']
			plan_estudios = request.POST['plan_estudios']

			# Obtenemos una instancia del centro
			instancia_centro = models.Centro.objects.get(pk=id_centro)

			# Se determina el siguiente id_titulacion para el centro.
			id_titulacion = determinarSiguienteIdTitulacionEnCentro(instancia_centro)

			# Datos necesarios para crear la nueva titulacion
			datos_titulacion = {'id_centro': id_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'id_titulacion': id_titulacion}

			# Se actualiza el formulario con la nueva informacion.
			form = forms.TitulacionForm(datos_titulacion, instance=instancia_titulacion)

			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de inicio.
				return HttpResponseRedirect('/asesorias/titulacion/list')
	# La titulacion no existe
	else:
		form = False
	return render_to_response('asesorias/Titulacion/editTitulacion.html', {'form': form})

def delTitulacion(request, nombre_centro, nombre_titulacion, plan_estudios):
	# Se obtiene la instancia de la titulacion.
	instancia_titulacion= obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios)
	# Si existe se elimina.
	if instancia_titulacion:
		instancia_titulacion.delete()
		return HttpResponseRedirect('/asesorias/titulacion/list')
	# La titulacion no existe.
	else:
		error = True
	return render_to_response('asesorias/Titulacion/delTitulacion.html', {'error': error})

def listTitulacion(request):
	# Se obtiene una lista con todas las titulaciones.
	lista_titulaciones= models.Titulacion.objects.all()
	# Al menos existe una titulacion.
	if lista_titulaciones:
		error = False
	# No existen titulaciones actualmente.
	else:
		error = 'No existen titulaciones actualmente en el sistema.'
	return render_to_response('asesorias/Titulacion/listTitulacion.html', {'lista_titulaciones': lista_titulaciones, 'error': error})
