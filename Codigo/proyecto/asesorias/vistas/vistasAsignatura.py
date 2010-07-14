from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms, views
from asesorias.vistas import vistasTitulacion

# Comprueba si existe una asignatura y, de ser asi, la devuelve.
def obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura):
	try:
		# Obtiene la instancia de titulacion para posteriormente obtener el id.
		instancia_titulacion = vistasTitulacion.obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios)

		# Obtiene la instancia de la asignatura.
		resultado = models.Asignatura.objects.get(id_centro=instancia_titulacion.id_centro_id, id_titulacion=instancia_titulacion.id_titulacion, nombre_asignatura=nombre_asignatura)
	except:
		resultado = False
	return resultado

# Obtiene una lista con las asignaturas de una determinada titulacion.
def obtenerAsignaturasDeTitulacion(instancia_titulacion):
	try:
		# Obtiene todas las asignaturas que pertenecen a la titulacion pasada por argumento.
		resultado = models.Asignatura.objects.filter(id_titulacion=instancia_titulacion.id_titulacion)
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
def determinarSiguienteIdAsignaturaEnTitulacion(instancia_titulacion):
	# Se obtiene una lista ordenada con los ids de las asignaturas existentes en la titulacion.
	lista_ids_asignaturas = obtenerListaDeIdsAsignaturasDeTitulacion(instancia_titulacion)

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
		codigo_titulacion = request.POST['titulacion']
		nombre_asignatura= request.POST['nombre_asignatura']
		curso = request.POST['curso']
		tipo = request.POST['tipo']
		n_creditos_teoricos = request.POST['nCreditosTeoricos']
		n_creditos_practicos= request.POST['nCreditosPracticos']

		# Se obtiene una instancia de la titulacion a traves de su id.
		instancia_titulacion = models.Titulacion.objects.get(pk=codigo_titulacion)

		# Se determina el id_centro e id_titulacion para esa titulacion.
		id_centro = instancia_titulacion.id_centro_id
		id_titulacion = instancia_titulacion.id_titulacion

		# Se determina el siguiente id_asignatura para la titulacion.
		id_asignatura = determinarSiguienteIdAsignaturaEnTitulacion(instancia_titulacion)

		# Datos necesarios para crear la nueva asignatura
		datos_asignatura = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'nombre_asignatura': nombre_asignatura, 'curso': curso, 'tipo': tipo, 'nCreditosTeoricos': n_creditos_teoricos, 'nCreditosPracticos': n_creditos_practicos, 'titulacion': codigo_titulacion}

		# Se obtienen los valores y se valida.
		form = forms.AsignaturaForm(datos_asignatura)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar asignaturas.
			return HttpResponseRedirect( reverse('listAsignatura', kwargs={'orden': 'nombre_centro'}) )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsignaturaForm()
	return render_to_response('asesorias/Asignatura/addAsignatura.html', {'form': form})

def editAsignatura(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura):
	# Se obtiene la instancia de la asignatura.
	instancia_asignatura= obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)
	# Si existe se edita.
	if instancia_asignatura:
		# Se carga el formulario para la asignatura existente.
		form = forms.AsignaturaForm(instance=instancia_asignatura, initial={'titulacion': vistasTitulacion.obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios).codigo_titulacion})
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se obtienen el resto de valores necesarios a traves de POST.
			codigo_titulacion = request.POST['titulacion']
			nombre_asignatura= request.POST['nombre_asignatura']
			curso = request.POST['curso']
			tipo = request.POST['tipo']
			n_creditos_teoricos = request.POST['nCreditosTeoricos']
			n_creditos_practicos= request.POST['nCreditosPracticos']

			# Se crea una instancia de la titulacion.
			instancia_titulacion = models.Titulacion.objects.get(pk=codigo_titulacion)

			# Se determina el id_centro e id_titulacion para esa titulacion.
			id_centro = instancia_titulacion.id_centro_id
			id_titulacion = instancia_titulacion.id_titulacion

			# Se determina el siguiente id_titulacion para el centro.
			id_asignatura = determinarSiguienteIdAsignaturaEnTitulacion(instancia_titulacion)

			# Datos necesarios para crear la nueva asignatura
			datos_asignatura = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'nombre_asignatura': nombre_asignatura, 'curso': curso, 'tipo': tipo, 'nCreditosTeoricos': n_creditos_teoricos, 'nCreditosPracticos': n_creditos_practicos, 'titulacion': codigo_titulacion}

			# Se actualiza el formulario con la nueva informacion.
			form = forms.AsignaturaForm(datos_asignatura, instance=instancia_asignatura)

			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar asignaturas.
				return HttpResponseRedirect( reverse('listAsignatura', kwargs={'orden': 'nombre_centro'}) )
	# La asignatura no existe
	else:
		form = False
	return render_to_response('asesorias/Asignatura/editAsignatura.html', {'form': form})

def delAsignatura(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura):
	# Se obtiene la instancia de la asignatura.
	instancia_asignatura= obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)
	# Si existe se elimina.
	if instancia_asignatura:
		instancia_asignatura.delete()
		# Redirige a la pagina de listar asignaturas.
		return HttpResponseRedirect( reverse('listAsignatura', kwargs={'orden': 'nombre_centro'}) )
	# La asignatura no existe.
	else:
		error = True
	return render_to_response('asesorias/Asignatura/delAsignatura.html', {'error': error})

def ordenarPorCentro(lista_asignaturas):
	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Se recorre la lista de asignaturas obteniendo los nombres de centro de cada asignatura.
	for asignatura in lista_asignaturas:
		# Se introducen los nombres de centro en la nueva lista.
		lista_aux.append(asignatura.determinarNombreCentro())
	# Obtenemos un set (valores unicos) ordenado con los valores de la lista.
	set_aux = sorted( set(lista_aux) )

	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Para cada nombre de centro (de manera ordenada) se crea una lista con las asignaturas en el orden correcto.
	for s in set_aux:
		for asignatura in lista_asignaturas:
			if ( asignatura.determinarNombreCentro() == s):
				lista_aux.append(asignatura)

	return lista_aux

def ordenarPorTitulacion(lista_asignaturas):
	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Se recorre la lista de asignaturas obteniendo los nombres de titulacion de cada asignatura.
	for asignatura in lista_asignaturas:
		# Se introducen los nombres de centro en la nueva lista.
		lista_aux.append(asignatura.determinarNombreTitulacion())
	# Obtenemos un set (valores unicos) ordenado con los valores de la lista.
	set_aux = sorted( set(lista_aux) )

	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Para cada nombre de titulacion (de manera ordenada) se crea una lista con las asignaturas en el orden correcto.
	for s in set_aux:
		for asignatura in lista_asignaturas:
			if ( asignatura.determinarNombreTitulacion() == s):
				lista_aux.append(asignatura)

	return lista_aux

def ordenarPorPlanEstudios(lista_asignaturas):
	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Se recorre la lista de asignaturas obteniendo los planes de estudios de cada asignatura.
	for asignatura in lista_asignaturas:
		# Se introducen los planes de estudio en la nueva lista.
		lista_aux.append(asignatura.determinarPlanEstudios())
	# Obtenemos un set (valores unicos) ordenado con los valores de la lista.
	set_aux = sorted( set(lista_aux) )

	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Para cada plan de estudios titulacion (de manera ordenada) se crea una lista con las asignaturas en el orden correcto.
	for s in set_aux:
		for asignatura in lista_asignaturas:
			if ( asignatura.determinarPlanEstudios() == s):
				lista_aux.append(asignatura)

	return lista_aux

def selectCentro(request):
	# Se ha introducido un centro.
	if request.method == 'POST':

		# Se obtiene el centro y se valida.
		form = forms.CentroFormSelect(request.POST)

		# Si es valido se redirige a listar centros.
		if form.is_valid():
			centro = request.POST['centro']

			# Se crea una instancia del centro para pasar el nombre de centro por argumento.
			instancia_centro = models.Centro.objects.get(pk=centro)

			return HttpResponseRedirect( reverse('selectTitulacion_Asignatura', kwargs={'nombre_centro': instancia_centro.nombre_centro}) )

		else:
			HttpResponseRedirect( reverse('selectCentro_Asignatura') )

	else:
		form = forms.CentroFormSelect()

	return render_to_response('asesorias/Asignatura/selectCentro.html', {'user': request.user, 'form': form})

def selectTitulacion(request, nombre_centro):
	# Se ha introducido una titulacion.
	if request.method == 'POST':

		# Se obtiene la titulacion y se valida.
		form = forms.TitulacionFormSelect(request.POST)

		# Si es valido se redirige a listar asignaturas.
		if form.is_valid():
			titulacion = request.POST['titulacion']

			# Se crea una instancia del centro para pasar el nombre de centro por argumento.
			instancia_titulacion = models.Titulacion.objects.get(pk=titulacion)

			return HttpResponseRedirect( reverse('listTitulacion', kwargs={'centro': nombre_centro, 'orden': 'nombre_titulacion'}) )

		else:
			HttpResponseRedirect( reverse('selectTitulacion_Asignatura') )

	else:
		form = forms.TitulacionFormSelect( id_centro=models.Centro.objects.get(nombre_centro=nombre_centro).id_centro )

	return render_to_response('asesorias/Asignatura/selectTitulacion.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro})

def listAsignatura(request, orden):
	# Se establece el ordenamiento inicial.
	if (orden == 'nombre_titulacion') or (orden == '_nombre_titulacion'):
		orden_inicial = 'id_titulacion'
	elif (orden == 'nombre_asignatura') or (orden == '_nombre_asignatura'):
		orden_inicial = 'nombre_asignatura'
	else:
		orden_inicial = 'id_centro'

	# Se obtiene una lista con todas las asignaturas.
	lista_asignaturas = models.Asignatura.objects.order_by(orden_inicial)

	# Se debe hacer el ordenamiento de manera especial ya que estos atributos son enteros y ordenamos alfabeticamente.
	if (orden == 'plan_estudios') or (orden == '_plan_estudios'):
		lista_asignaturas = ordenarPorPlanEstudios(lista_asignaturas)
	elif (orden_inicial == 'id_centro'):
		lista_asignaturas = ordenarPorCentro(lista_asignaturas)
	elif (orden_inicial == 'id_titulacion'):
		lista_asignaturas = ordenarPorTitulacion(lista_asignaturas)

	# Se ha realizado una busqueda.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.SearchForm(request.POST)
		# Si es valido se realiza la busqueda.
		if form.is_valid():
			busqueda = request.POST['busqueda']

			# Se crea una lista auxiliar que albergara el resultado de la busqueda.
			lista_aux = []

			# Se recorren los elementos determinando si coinciden con la busqueda.
			for asignatura in lista_asignaturas:
				# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
				cadena = unicode(asignatura.determinarNombreCentro()) + unicode(asignatura.determinarNombreTitulacion()) + unicode(asignatura.nombre_asignatura) + unicode(asignatura.determinarPlanEstudios())

				# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
				if cadena.find(busqueda) >= 0:
					lista_aux.append(asignatura)

			# La lista final a devolver sera la lista auxiliar.
			lista_asignaturas = lista_aux

		else:
			busqueda = False
	# No se ha realizado busqueda.
	else:
		# Formulario para una posible busqueda.
		form = forms.SearchForm()
		busqueda = False

		# Si el orden es descendente se invierte la lista.
		if (orden == '_nombre_centro') or (orden == '_nombre_titulacion') or (orden == '_nombre_asignatura') or (orden == '_plan_estudios'):
			lista_asignaturas = reversed(lista_asignaturas)

	return render_to_response('asesorias/Asignatura/listAsignatura.html', {'user': request.user, 'form': form, 'lista_asignaturas': lista_asignaturas, 'busqueda': busqueda, 'orden': orden})

def generarPDFListaAsignaturas(request):
	# Se obtiene una lista con todas las asignaturas.
	lista_asignaturas = models.Asignatura.objects.all()

	return views.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_asignaturas, 'name': 'asignaturas',} )
