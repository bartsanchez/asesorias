from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasCentro

# Obtiene una lista con las asignaturas de una determinada titulacion.
def obtenerAsignaturasDeTitulacion(instancia_titulacion):
	try:
		# Obtiene todas las asignaturas que pertenecen a la titulacion pasada por argumento.
		resultado = models.Asignatura.objects.filter(codigo_titulacion=instancia_titulacion.codigo_titulacion)
	except:
		resultado = False
	return resultado

# Obtiene una lista ordenada con los ids de las asignaturas de una determinada titulacion.
def obtenerListaDeIdsAsignaturasDeTitulacion(instancia_titulacion):
	if instancia_titulacion:
		# Se obtiene una lista con las asignaturas de una determinada titulacion.
		lista_asignaturas_de_titulacion = obtenerAsignaturasDeTitulacion(instancia_titulacion)
		# Lista que albergara los ids de las asignaturas.
		lista_ids_asignaturas= []

		# Si existen asignaturas en la titulacion extraen sus ids.
		if lista_asignaturas_de_titulacion:
			# Por cada titulacion del centro se extrae su id y se inserta en la nueva lista.
			for asignatura in lista_asignaturas_de_titulacion:
				lista_ids_asignaturas.append(asignatura.id_asignatura)
			# Ordena la lista con los ids de las asignaturas de menor a mayor.
			lista_ids_asignaturas.sort()
		# Resultado sera una lista de ids, o una lista vacia si la titulacion no tiene asignaturas.
		resultado = lista_ids_asignaturas
	# En el caso de que no exista la titulacion se devuelve False.
	else:
		resultado = False
	return resultado

# Determina el primer id_asignatura disponible para una determinada titulacion.
def determinarSiguienteIdAsignaturaEnTitulacion(lista_ids_asignaturas):
	# Inicializamos el contador a 1, que es el primer valor valido para un id.
	contador = 1
	# Recorre el bucle determinando si una posicion se encuentra o no.
	while True:
		# La posicion determinada por contador aparece en la lista, por lo tanto se encuentra la id_asignatura en la titulacion.
		if lista_ids_asignaturas.count(contador) > 0:
			contador += 1
		# No existe tal id_asignatura en la titulacion.
		else:
			break
	return contador

def addAsignatura(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		id_titulacion = request.POST['titulacion']
		nombre_asignatura= request.POST['nombre_asignatura']
		curso = request.POST['curso']
		tipo = request.POST['tipo']
		n_creditos_teoricos = request.POST['nCreditosTeoricos']
		n_creditos_practicos= request.POST['nCreditosPracticos']

		# Se obtiene una instancia de la titulacion a traves de su id.
		instancia_titulacion = models.Titulacion.objects.get(pk=id_titulacion)

		# Se determina el id_centro para esa titulacion.
		instancia_centro = vistasCentro.obtenerCentro(unicode(instancia_titulacion.id_centro))
		id_centro = instancia_centro.getId()

		# Se crea una lista temporal que albergara los ids de las asignaturas existentes en la titulacion para determinar la siguiente id_asignatura.
		lista_ids_asignaturas= []
		lista_ids_asignaturas= obtenerListaDeIdsAsignaturasDeTitulacion(instancia_titulacion)
		id_asignatura = determinarSiguienteIdAsignaturaEnTitulacion(lista_ids_asignaturas)

		# Datos necesarios para crear la nueva titulacion
		datos_asignatura = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'nombre_asignatura': nombre_asignatura, 'curso': curso, 'tipo': tipo, 'nCreditosTeoricos': n_creditos_teoricos, 'nCreditosPracticos': n_creditos_practicos, 'titulacion': id_titulacion}

		# Se obtienen los valores y se valida.
		form = forms.AsignaturaForm(datos_asignatura)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
			print form.errors
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsignaturaForm()
		error = False
	return render_to_response('asesorias/Asignatura/addAsignatura.html', {'form': form, 'error': error})
