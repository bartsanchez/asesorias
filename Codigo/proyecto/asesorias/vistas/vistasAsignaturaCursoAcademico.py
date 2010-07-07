from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms, views
from asesorias.vistas import vistasAsignatura

# Comprueba si existe una asignatura curso academico y, de ser asi, la devuelve.
def obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	try:
		# Obtiene la instancia de asignatura para posteriormente obtener el id.
		instancia_asignatura= vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)

		# Obtiene la instancia de la asignatura curso academico.
		resultado = models.AsignaturaCursoAcademico.objects.get(id_centro=instancia_asignatura.id_centro, id_titulacion=instancia_asignatura.id_titulacion, id_asignatura=instancia_asignatura.id_asignatura, curso_academico=curso_academico)
	except:
		resultado = False
	return resultado

def addAsignaturaCursoAcademico(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		codigo_asignatura = request.POST['asignatura']
		curso_academico = request.POST['curso_academico']

		# Se obtiene una instancia de la asignatura a traves de su id.
		instancia_asignatura= models.Asignatura.objects.get(pk=codigo_asignatura)

		# Se determina el id_centro, id_titulacion e id_asignatura para esa asignatura.
		id_centro = instancia_asignatura.id_centro
		id_titulacion = instancia_asignatura.id_titulacion
		id_asignatura = instancia_asignatura.id_asignatura

		# Datos necesarios para crear la nueva asignatura curso academico
		datos_asignatura_curso_academico = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'curso_academico': curso_academico, 'asignatura': codigo_asignatura}

		# Se obtienen los valores y se valida.
		form = forms.AsignaturaCursoAcademicoForm(datos_asignatura_curso_academico)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar asignaturas curso academico.
			return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'orden': 'nombre_centro'}) )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsignaturaCursoAcademicoForm()
	return render_to_response('asesorias/AsignaturaCursoAcademico/addAsignaturaCursoAcademico.html', {'form': form})

def editAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	# Se obtiene la instancia de la asignatura curso academico.
	instancia_asignatura_curso_academico= obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico)
	# Si existe se edita.
	if instancia_asignatura_curso_academico:
		# Se carga el formulario para la asignatura existente.
		form = forms.AsignaturaCursoAcademicoForm(instance=instancia_asignatura_curso_academico, initial={'asignatura': vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura).codigo_asignatura})
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se obtienen el resto de valores necesarios a traves de POST.
			codigo_asignatura = request.POST['asignatura']
			curso_academico = request.POST['curso_academico']

			# Se obtiene una instancia de la asignatura a traves de su id.
			instancia_asignatura= models.Asignatura.objects.get(pk=codigo_asignatura)

			# Se determina el id_centro, id_titulacion e id_asignatura para esa asignatura.
			id_centro = instancia_asignatura.id_centro
			id_titulacion = instancia_asignatura.id_titulacion
			id_asignatura = instancia_asignatura.id_asignatura

			# Datos necesarios para crear la nueva asignatura curso academico
			datos_asignatura_curso_academico = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'curso_academico': curso_academico, 'asignatura': codigo_asignatura}

			# Se actualiza el formulario con la nueva informacion.
			form = forms.AsignaturaCursoAcademicoForm(datos_asignatura_curso_academico, instance=instancia_asignatura_curso_academico)

			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar asignaturas curso academico.
				return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'orden': 'nombre_centro'}) )
	# La asignatura curso academico no existe
	else:
		form = False
	return render_to_response('asesorias/AsignaturaCursoAcademico/editAsignaturaCursoAcademico.html', {'form': form})

def delAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	# Se obtiene la instancia de la asignatura curso academico.
	instancia_asignatura_curso_academico= obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico)
	# Si existe se elimina.
	if instancia_asignatura_curso_academico:
		instancia_asignatura_curso_academico.delete()
		# Redirige a la pagina de listar asignaturas curso academico.
		return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'orden': 'nombre_centro'}) )
	# La asignatura no existe.
	else:
		error = True
	return render_to_response('asesorias/AsignaturaCursoAcademico/delAsignaturaCursoAcademico.html', {'error': error})

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

def ordenarPorAsignatura(lista_asignaturas):
	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Se recorre la lista de asignaturas obteniendo los nombres de asignatura de cada asignatura.
	for asignatura in lista_asignaturas:
		# Se introducen los nombres de centro en la nueva lista.
		lista_aux.append(asignatura.determinarNombreAsignatura())
	# Obtenemos un set (valores unicos) ordenado con los valores de la lista.
	set_aux = sorted( set(lista_aux) )

	# Lista auxiliar que albergara la nueva lista.
	lista_aux = []

	# Para cada nombre de asignatura (de manera ordenada) se crea una lista con las asignaturas en el orden correcto.
	for s in set_aux:
		for asignatura in lista_asignaturas:
			if ( asignatura.determinarNombreAsignatura() == s):
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

def listAsignaturaCursoAcademico(request, orden):
	# Se establece el ordenamiento inicial.
	if (orden == 'nombre_titulacion') or (orden == '_nombre_titulacion'):
		orden_inicial = 'id_titulacion'
	elif (orden == 'nombre_asignatura') or (orden == '_nombre_asignatura'):
		orden_inicial = 'id_asignatura'
	elif (orden == 'curso_academico') or (orden == '_curso_academico'):
		orden_inicial = 'curso_academico'
	else:
		orden_inicial = 'id_centro'

	# Se obtiene una lista con todos las asignaturas curso academico.
	lista_asignaturas_curso_academico = models.AsignaturaCursoAcademico.objects.order_by(orden_inicial)

	# Se debe hacer el ordenamiento de manera especial ya que estos atributos son enteros y ordenamos alfabeticamente.
	if (orden == 'plan_estudios') or (orden == '_plan_estudios'):
		lista_asignaturas_curso_academico = ordenarPorPlanEstudios(lista_asignaturas_curso_academico)
	elif (orden_inicial == 'id_centro'):
		lista_asignaturas_curso_academico = ordenarPorCentro(lista_asignaturas_curso_academico)
	elif (orden_inicial == 'id_titulacion'):
		lista_asignaturas_curso_academico = ordenarPorTitulacion(lista_asignaturas_curso_academico)
	elif (orden_inicial == 'id_asignatura'):
		lista_asignaturas_curso_academico =  ordenarPorAsignatura(lista_asignaturas_curso_academico)

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
			for asignatura in lista_asignaturas_curso_academico:
				# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
				cadena = unicode(asignatura.determinarNombreCentro()) + unicode(asignatura.determinarNombreTitulacion()) + unicode(asignatura.determinarNombreAsignatura()) + unicode(asignatura.curso_academico) + unicode(asignatura.determinarPlanEstudios())

				# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
				if cadena.find(busqueda) >= 0:
					lista_aux.append(asignatura)

			# La lista final a devolver sera la lista auxiliar.
			lista_asignaturas_curso_academico = lista_aux

		else:
			busqueda = False
	# No se ha realizado busqueda.
	else:
		# Formulario para una posible busqueda.
		form = forms.SearchForm()
		busqueda = False

		# Si el orden es descendente se invierte la lista.
		if (orden == '_nombre_centro') or (orden == '_nombre_titulacion') or (orden == '_nombre_asignatura') or (orden == '_curso_academico') or (orden == '_plan_estudios'):
			lista_asignaturas_curso_academico = reversed(lista_asignaturas_curso_academico)

	return render_to_response('asesorias/AsignaturaCursoAcademico/listAsignaturaCursoAcademico.html', {'user': request.user, 'form': form, 'lista_asignaturas_curso_academico': lista_asignaturas_curso_academico, 'busqueda': busqueda, 'orden': orden})

def generarPDFListaAsignaturasCursoAcademico(request):
	# Se obtiene una lista con todos las asignaturas curso academico.
	lista_asignaturas_curso_academico = models.AsignaturaCursoAcademico.objects.all()

	return views.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_asignaturas_curso_academico, 'name': 'asignaturas curso academico',} )
