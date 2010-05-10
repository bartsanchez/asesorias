from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe una pregunta oficial y, de ser asi, la devuelve.
def obtenerPreguntaOficial(id_entrevista_oficial, id_pregunta_oficial):
	try:
		# Obtiene la pregunta oficial.
		resultado = models.PreguntaOficial.objects.get(id_entrevista_oficial=id_entrevista_oficial, id_pregunta_oficial=id_pregunta_oficial)
	except:
		resultado = False
	return resultado

# Obtiene una lista con las preguntas de una determinada plantilla oficial.
def obtenerPreguntasDePlantillaOficial(instancia_plantilla_entrevista_oficial):
	try:
		# Obtiene todas las preguntas que pertenecen a una plantilla oficial pasado por argumento.
		resultado = models.PreguntaOficial.objects.filter(id_entrevista_oficial=instancia_plantilla_entrevista_oficial.id_entrevista_oficial)
	except:
		resultado = False
	return resultado

# Obtiene una lista ordenada con los ids de las preguntas de una determinada plantilla oficial.
def obtenerListaDeIdsPreguntasDePlantillaOficial(instancia_plantilla_entrevista_oficial):
	if instancia_plantilla_entrevista_oficial:
		# Se obtiene una lista con las preguntas de una determinada plantilla oficial.
		lista_preguntas_oficiales = obtenerPreguntasDePlantillaOficial(instancia_plantilla_entrevista_oficial)
		# Lista que albergara los ids de las preguntas.
		lista_ids_preguntas_oficiales = []

		# Si existen preguntas en la plantilla oficial extraen sus ids.
		if lista_preguntas_oficiales:
			# Por cada pregunta de la plantilla oficial se extrae su id y se inserta en la nueva lista.
			for pregunta_oficial in lista_preguntas_oficiales:
				lista_ids_preguntas_oficiales.append(pregunta_oficial.id_pregunta_oficial)
			# Ordena la lista con los ids de las preguntas de menor a mayor.
			lista_ids_preguntas_oficiales.sort()
		# Resultado sera una lista de ids, o una lista vacia si la plantilla no tiene preguntas.
		resultado = lista_ids_preguntas_oficiales
	# En el caso de que no exista la plantilla se devuelve False.
	else:
		resultado = False
	return resultado

# Determina el primer id_pregunta_oficial disponible para una determinada plantilla oficial.
def determinarSiguienteIdPreguntaDePlantillaOficial(instancia_plantilla_entrevista_oficial):
	# Se obtiene una lista ordenada con los ids de las preguntas existentes para la plantilla oficial.
	lista_ids_preguntas_oficiales = obtenerListaDeIdsPreguntasDePlantillaOficial(instancia_plantilla_entrevista_oficial)

	# Inicializamos el contador a 1, que es el primer valor valido para un id.
	contador = 1
	# Recorre el bucle determinando si una posicion se encuentra o no.
	while True:
		# La posicion determinada por contador aparece en la lista, por lo tanto se encuentra la id_pregunta_oficial para la plantilla oficial.
		if lista_ids_preguntas_oficiales.count(contador) > 0:
			contador += 1
		# No existe tal id_pregunta_oficial para la plantilla oficial.
		else:
			break
	return contador

def addPreguntaOficial(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		codigo_plantilla_entrevista_oficial = request.POST['plantilla_entrevista_oficial']
		enunciado = request.POST['enunciado']
		ultima_modificacion = request.POST['ultima_modificacion']

		# Se obtiene una instancia de la plantilla oficial a traves de su id.
		instancia_plantilla_entrevista_oficial = models.PlantillaEntrevistaOficial.objects.get(pk=codigo_plantilla_entrevista_oficial)

		# Se determina el id_entrevista_oficial para esa plantilla oficial.
		id_entrevista_oficial = instancia_plantilla_entrevista_oficial.id_entrevista_oficial

		# Se determina el siguiente id_pregunta_oficial para la plantilla de entrevista oficial.
		id_pregunta_oficial = determinarSiguienteIdPreguntaDePlantillaOficial(instancia_plantilla_entrevista_oficial)

		# Datos necesarios para crear la nueva plantilla.
		datos_pregunta_oficial = {'id_entrevista_oficial': id_entrevista_oficial, 'id_pregunta_oficial': id_pregunta_oficial, 'enunciado': enunciado, 'ultima_modificacion': ultima_modificacion, 'plantilla_entrevista_oficial': codigo_plantilla_entrevista_oficial}

		# Se obtienen los valores y se valida.
		form = forms.PreguntaOficialForm(datos_pregunta_oficial)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar preguntas de plantilla oficiales.
			return HttpResponseRedirect( reverse('listPreguntaOficial') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.PreguntaOficialForm()
	return render_to_response('asesorias/PreguntaOficial/addPreguntaOficial.html', {'form': form})

def delPreguntaOficial(request, id_entrevista_oficial, id_pregunta_oficial):
	# Se obtiene la instancia de la pregunta oficial.
	instancia_pregunta_oficial = obtenerPreguntaOficial(id_entrevista_oficial, id_pregunta_oficial)
	# Si existe se elimina.
	if instancia_pregunta_oficial:
		instancia_pregunta_oficial.delete()
		# Redirige a la pagina de listar preguntas oficiales.
		return HttpResponseRedirect( reverse('listPreguntaOficial') )
	# La pregunta no existe.
	else:
		error = True
	return render_to_response('asesorias/PreguntaOficial/delPreguntaOficial.html', {'error': error})

def listPreguntaOficial(request):
	# Se obtiene una lista con todos las preguntas oficiales.
	lista_preguntas_oficiales = models.PreguntaOficial.objects.all()
	return render_to_response('asesorias/PreguntaOficial/listPreguntaOficial.html', {'lista_preguntas_oficiales': lista_preguntas_oficiales})