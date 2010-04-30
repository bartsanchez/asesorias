from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Obtiene una lista con las preguntas de una determinada plantilla de asesor.
def obtenerPreguntasDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor):
	try:
		# Obtiene todas las preguntas que pertenecen a una plantilla de asesor pasado por argumento.
		resultado = models.PreguntaAsesor.objects.filter(dni_pasaporte=instancia_plantilla_entrevista_asesor.dni_pasaporte, curso_academico=instancia_plantilla_entrevista_asesor.curso_academico, id_entrevista_asesor=instancia_plantilla_entrevista_asesor.id_entrevista_asesor)
	except:
		resultado = False
	return resultado

# Obtiene una lista ordenada con los ids de las preguntas de una determinada plantilla de asesor.
def obtenerListaDeIdsPreguntasDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor):
	if instancia_plantilla_entrevista_asesor:
		# Se obtiene una lista con las preguntas de una determinada plantilla de asesor.
		lista_preguntas_de_asesor= obtenerPreguntasDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor)
		# Lista que albergara los ids de las preguntas.
		lista_ids_preguntas_de_asesor = []

		# Si existen preguntas en la plantilla de asesor extraen sus ids.
		if lista_preguntas_de_asesor:
			# Por cada pregunta de la plantilla de asesor se extrae su id y se inserta en la nueva lista.
			for pregunta_de_asesor in lista_preguntas_de_asesor:
				lista_ids_preguntas_de_asesor.append(pregunta_de_asesor.id_pregunta_asesor)
			# Ordena la lista con los ids de las preguntas de menor a mayor.
			lista_ids_preguntas_de_asesor.sort()
		# Resultado sera una lista de ids, o una lista vacia si la plantilla no tiene preguntas.
		resultado = lista_ids_preguntas_de_asesor
	# En el caso de que no exista la plantilla se devuelve False.
	else:
		resultado = False
	return resultado

# Determina el primer id_pregunta_asesor disponible para una determinada plantilla de asesor.
def determinarSiguienteIdPreguntaDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor):
	# Se obtiene una lista ordenada con los ids de las preguntas existentes para la plantilla de asesor.
	lista_ids_preguntas_de_asesor = obtenerListaDeIdsPreguntasDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor)

	# Inicializamos el contador a 1, que es el primer valor valido para un id.
	contador = 1
	# Recorre el bucle determinando si una posicion se encuentra o no.
	while True:
		# La posicion determinada por contador aparece en la lista, por lo tanto se encuentra la id_pregunta_asesor para la plantilla de asesor.
		if lista_ids_preguntas_de_asesor.count(contador) > 0:
			contador += 1
		# No existe tal id_pregunta_asesor para la plantilla de asesor.
		else:
			break
	return contador

def addPreguntaAsesor(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		codigo_plantilla_entrevista_asesor = request.POST['plantilla_entrevista_asesor']
		enunciado = request.POST['enunciado']
		ultima_modificacion = request.POST['ultima_modificacion']

		# Se obtiene una instancia de la plantilla de asesor a traves de su id.
		instancia_plantilla_entrevista_asesor = models.PlantillaEntrevistaAsesor.objects.get(pk=codigo_plantilla_entrevista_asesor)

		# Se determina el dni_pasaporte, curso academico e id_entrevista_asesor para esa plantilla de asesor.
		dni_pasaporte = instancia_plantilla_entrevista_asesor.dni_pasaporte
		curso_academico = instancia_plantilla_entrevista_asesor.curso_academico
		id_entrevista_asesor = instancia_plantilla_entrevista_asesor.id_entrevista_asesor

		# Se determina el siguiente id_pregunta_asesor para la plantilla de entrevista de asesor.
		id_pregunta_asesor = determinarSiguienteIdPreguntaDePlantillaDeAsesor(instancia_plantilla_entrevista_asesor)

		# Datos necesarios para crear la nueva plantilla.
		datos_pregunta_asesor = {'dni_pasaporte': dni_pasaporte, 'curso_academico': curso_academico, 'id_entrevista_asesor': id_entrevista_asesor, 'id_pregunta_asesor': id_pregunta_asesor, 'enunciado': enunciado, 'ultima_modificacion': ultima_modificacion, 'plantilla_entrevista_asesor': codigo_plantilla_entrevista_asesor}

		# Se obtienen los valores y se valida.
		form = forms.PreguntaAsesorForm(datos_pregunta_asesor)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar preguntas de plantilla de asesor.
			return HttpResponseRedirect( reverse('listPreguntaAsesor') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.PreguntaAsesorForm()
	return render_to_response('asesorias/PreguntaAsesor/addPreguntaAsesor.html', {'form': form})

def listPreguntaAsesor(request):
	# Se obtiene una lista con todos las preguntas de asesor.
	lista_preguntas_asesor = models.PreguntaAsesor.objects.all()
	return render_to_response('asesorias/PreguntaAsesor/listPreguntaAsesor.html', {'lista_preguntas_asesor': lista_preguntas_asesor})

