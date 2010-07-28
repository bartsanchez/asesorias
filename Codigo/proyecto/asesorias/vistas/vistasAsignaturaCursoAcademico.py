from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsignatura, vistasCentro, vistasTitulacion
from asesorias.utils import vistasPDF

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

def addAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se extraen los valores pasados por el metodo POST.
		codigo_asignatura = vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura).codigo_asignatura
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
			return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'nombre_centro': instancia_asignatura.determinarNombreCentro(), 'nombre_titulacion': instancia_asignatura.determinarNombreTitulacion(), 'plan_estudios': instancia_asignatura.determinarPlanEstudios(), 'nombre_asignatura': instancia_asignatura.nombre_asignatura,'orden': 'nombre_centro'}) )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsignaturaCursoAcademicoForm()
	return render_to_response('asesorias/AsignaturaCursoAcademico/addAsignaturaCursoAcademico.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': nombre_asignatura})

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
				return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'nombre_centro': instancia_asignatura.determinarNombreCentro(), 'nombre_titulacion': instancia_asignatura.determinarNombreTitulacion(), 'plan_estudios': instancia_asignatura.determinarPlanEstudios(), 'nombre_asignatura': instancia_asignatura.nombre_asignatura,'orden': 'nombre_centro'}) )
	# La asignatura curso academico no existe
	else:
		form = False
	return render_to_response('asesorias/AsignaturaCursoAcademico/editAsignaturaCursoAcademico.html', {'user': request.user, 'form': form})

def delAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	# Se obtiene la instancia de la asignatura curso academico.
	instancia_asignatura_curso_academico= obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico)
	# Si existe se elimina.
	if instancia_asignatura_curso_academico:
		instancia_asignatura_curso_academico.delete()
		# Redirige a la pagina de listar asignaturas curso academico.
		return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': nombre_asignatura, 'orden': 'nombre_centro'}) )
	# La asignatura no existe.
	else:
		error = True
	return render_to_response('asesorias/AsignaturaCursoAcademico/delAsignaturaCursoAcademico.html', {'user': request.user, 'error': error})

def selectCentro(request, tipo):
	# Se ha introducido un centro.
	if request.method == 'POST':

		# Se obtiene el centro y se valida.
		form = forms.CentroFormSelect(request.POST)

		# Si es valido se redirige a listar centros.
		if form.is_valid():
			centro = request.POST['centro']

			# Se crea una instancia del centro para pasar el nombre de centro por argumento.
			instancia_centro = models.Centro.objects.get(pk=centro)

			return HttpResponseRedirect( reverse('selectTitulacion_AsignaturaCursoAcademico', kwargs={'nombre_centro': instancia_centro.nombre_centro, 'tipo': tipo}) )

		else:
			return HttpResponseRedirect( reverse('selectCentro_AsignaturaCursoAcademico', kwargs={'tipo': tipo}) )

	else:
		form = forms.CentroFormSelect()

	return render_to_response('asesorias/AsignaturaCursoAcademico/selectCentro.html', {'user': request.user, 'form': form, 'tipo': tipo})

def selectTitulacion(request, nombre_centro, tipo):
	# Se obtiene el posible centro.
	instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

	# Se comprueba que exista el centro.
	if not instancia_centro:
		return HttpResponseRedirect( reverse('selectCentro_AsignaturaCursoAcademico') )
	else:
		id_centro = instancia_centro.id_centro

	# Se ha introducido una titulacion.
	if request.method == 'POST':

		# Se obtiene la titulacion y se valida.
		form = forms.TitulacionFormSelect(id_centro, request.POST)

		# Si es valido se redirige a listar asignaturas.
		if form.is_valid():
			titulacion = request.POST['titulacion']

			# Se crea una instancia de la titulacion para pasar los argumentos.
			instancia_titulacion = models.Titulacion.objects.get(pk=titulacion)

			return HttpResponseRedirect( reverse('selectAsignatura_AsignaturaCursoAcademico', kwargs={'nombre_centro': instancia_titulacion.determinarNombreCentro(), 'nombre_titulacion': instancia_titulacion.nombre_titulacion, 'plan_estudios': instancia_titulacion.plan_estudios, 'tipo': tipo}) )

		else:
			return HttpResponseRedirect( reverse('selectTitulacion_AsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'tipo': tipo}) )

	else:
		form = forms.TitulacionFormSelect(id_centro=id_centro)

	return render_to_response('asesorias/AsignaturaCursoAcademico/selectTitulacion.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro, 'tipo': tipo})

def selectAsignatura(request, nombre_centro, nombre_titulacion, plan_estudios, tipo):
	# Se obtiene la posible titulacion.
	instancia_titulacion = vistasTitulacion.obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios)

	# Se comprueba que exista la titulacion.
	if not instancia_titulacion:
		return HttpResponseRedirect( reverse('selectTitulacion_AsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'tipo': tipo}) )
	else:
		id_centro = instancia_titulacion.id_centro_id
		id_titulacion = instancia_titulacion.id_titulacion

	# Se ha introducido una titulacion.
	if request.method == 'POST':

		# Se obtiene la titulacion y se valida.
		form = forms.AsignaturaFormSelect(id_centro, id_titulacion, request.POST)

		# Si es valido se redirige a listar asignaturas curso academico.
		if form.is_valid():
			asignatura = request.POST['asignatura']

			# Se crea una instancia de la asignatura para pasar los argumentos.
			instancia_asignatura = models.Asignatura.objects.get(pk=asignatura)

			if tipo == 'add':
				return HttpResponseRedirect( reverse('addAsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': instancia_asignatura.nombre_asignatura}) )
			else:
				return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': instancia_asignatura.nombre_asignatura, 'orden': 'curso_academico'}) )

		else:
			return HttpResponseRedirect( reverse('selectAsignatura_AsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios}) )

	else:
		form = forms.AsignaturaFormSelect(id_centro=id_centro, id_titulacion=id_titulacion)

	return render_to_response('asesorias/AsignaturaCursoAcademico/selectAsignatura.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'tipo': tipo})

def listAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, orden):
	# Se obtiene la posible asignatura.
	instancia_asignatura = vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)

	# Se comprueba que exista la asignatura.
	if not instancia_asignatura:
		return HttpResponseRedirect( reverse('selectCentro_AsignaturaCursoAcademico') )
	else:
		id_centro = instancia_asignatura.id_centro
		id_titulacion = instancia_asignatura.id_titulacion
		id_asignatura = instancia_asignatura.id_asignatura

	# Se obtiene una lista con todos las asignaturas curso academico.
	lista_asignaturas_curso_academico = models.AsignaturaCursoAcademico.objects.filter(id_centro=id_centro, id_titulacion=id_titulacion, id_asignatura=id_asignatura).order_by('curso_academico')

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
				cadena = unicode(asignatura.curso_academico)

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
		if (orden == '_curso_academico'):
			lista_asignaturas_curso_academico = reversed(lista_asignaturas_curso_academico)

	return render_to_response('asesorias/AsignaturaCursoAcademico/listAsignaturaCursoAcademico.html', {'user': request.user, 'form': form, 'lista_asignaturas_curso_academico': lista_asignaturas_curso_academico, 'busqueda': busqueda, 'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': nombre_asignatura, 'orden': orden})

def generarPDFListaAsignaturasCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, busqueda):
	# Se obtiene la posible asignatura.
	instancia_asignatura = vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)

	# Se comprueba que exista la asignatura.
	if not instancia_asignatura:
		return HttpResponseRedirect( reverse('selectCentro_AsignaturaCursoAcademico') )
	else:
		id_centro = instancia_asignatura.id_centro
		id_titulacion = instancia_asignatura.id_titulacion
		id_asignatura = instancia_asignatura.id_asignatura

	# Se obtiene una lista con todos las asignaturas curso academico.
	lista_asignaturas_curso_academico = models.AsignaturaCursoAcademico.objects.filter(id_centro=id_centro, id_titulacion=id_titulacion, id_asignatura=id_asignatura).order_by('curso_academico')

	# Se ha realizado una busqueda.
	if busqueda != 'False':
		# Se crea una lista auxiliar que albergara el resultado de la busqueda.
		lista_aux = []

		# Se recorren los elementos determinando si coinciden con la busqueda.
		for asignatura in lista_asignaturas_curso_academico:
			# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
			cadena = unicode(asignatura.curso_academico)

			# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
			if cadena.find(busqueda) >= 0:
				lista_aux.append(asignatura)

		# La lista final a devolver sera la lista auxiliar.
		lista_asignaturas_curso_academico = lista_aux

	return vistasPDF.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_asignaturas_curso_academico, 'name': 'asignaturas curso academico',} )
