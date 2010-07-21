from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsesor, vistasDepartamento
from asesorias.utils import vistasPDF

# Comprueba si existe un asesor curso academico y, de ser asi, la devuelve.
def obtenerAsesorCursoAcademico(dni_pasaporte, curso_academico):
	try:
		# Obtiene la instancia de asesor curso academico.
		resultado = models.AsesorCursoAcademico.objects.get(dni_pasaporte=dni_pasaporte, curso_academico=curso_academico)
	except:
		resultado = False
	return resultado

def addAsesorCursoAcademico(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AsesorCursoAcademicoForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar asesores curso academico.
			return HttpResponseRedirect( reverse('listAsesorCursoAcademico') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsesorCursoAcademicoForm()
	return render_to_response('asesorias/AsesorCursoAcademico/addAsesorCursoAcademico.html', {'form': form})

def editAsesorCursoAcademico(request, dni_pasaporte, curso_academico):
	# Se obtiene la instancia del asesor curso academico.
	instancia_asesor_curso_academico= obtenerAsesorCursoAcademico(dni_pasaporte, curso_academico)
	# Si existe se edita.
	if instancia_asesor_curso_academico:
		# Se carga el formulario para la asignatura existente.
		form = forms.AsesorCursoAcademicoForm(instance=instancia_asesor_curso_academico)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.AsesorCursoAcademicoForm(request.POST, instance=instancia_asesor_curso_academico)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar asesores curso academico.
				return HttpResponseRedirect( reverse('listAsesorCursoAcademico') )
	# El asesor curso academico no existe.
	else:
		form = False
	return render_to_response('asesorias/AsesorCursoAcademico/editAsesorCursoAcademico.html', {'form': form})

def delAsesorCursoAcademico(request, dni_pasaporte, curso_academico):
	# Se obtiene la instancia del asesor curso academico.
	instancia_asesor_curso_academico= obtenerAsesorCursoAcademico(dni_pasaporte, curso_academico)
	# Si existe se elimina.
	if instancia_asesor_curso_academico:
		instancia_asesor_curso_academico.delete()
		# Redirige a la pagina de listar asesores curso academico.
		return HttpResponseRedirect( reverse('listAsesorCursoAcademico') )
	# El asesor curso academico no existe.
	else:
		error = True
	return render_to_response('asesorias/AsesorCursoAcademico/delAsesorCursoAcademico.html', {'error': error})

def selectDepartamentoOAsesor(request):
	return render_to_response('asesorias/AsesorCursoAcademico/selectDepartamentoOAsesor.html', {'user': request.user})

def selectDepartamento(request):
	# Se ha introducido un departamento.
	if request.method == 'POST':

		# Se obtiene el departamento y se valida.
		form = forms.DepartamentoFormSelect(request.POST)

		# Si es valido se redirige a listar departamentos.
		if form.is_valid():
			departamento = request.POST['departamento']

			# Se crea una instancia del departamento para pasar el nombre de departamento por argumento.
			instancia_departamento = models.Departamento.objects.get(pk=departamento)

			return HttpResponseRedirect( reverse('selectAsesorDepartamento_AsesorCursoAcademico', kwargs={'nombre_departamento': instancia_departamento.nombre_departamento}) )

		else:
			HttpResponseRedirect( reverse('selectDepartamento_AsesorCursoAcademico') )

	else:
		form = forms.DepartamentoFormSelect()

	return render_to_response('asesorias/AsesorCursoAcademico/selectDepartamento.html', {'user': request.user, 'form': form})

def selectAsesorDepartamento(request, nombre_departamento):
	# Se obtiene el posible departamento.
	instancia_departamento = vistasDepartamento.obtenerDepartamento(nombre_departamento)

	# Se comprueba que exista el departamento.
	if not instancia_departamento:
		return HttpResponseRedirect( reverse('selectDepartamento_AsesorCursoAcademico') )
	else:
		id_departamento = instancia_departamento.id_departamento

	# Se ha introducido un asesor.
	if request.method == 'POST':

		# Se obtiene el asesor y se valida.
		form = forms.AsesorDepartamentoFormSelect(id_departamento, request.POST)

		# Si es valido se redirige a listar asesores curso academico.
		if form.is_valid():
			asesor = request.POST['asesor']

			return HttpResponseRedirect( reverse('listAsesorCursoAcademico_Departamento', kwargs={'nombre_departamento': nombre_departamento, 'dni_pasaporte': asesor, 'orden': 'curso_academico'}) )

		else:
			return HttpResponseRedirect( reverse('selectTitulacion_Asignatura', kwargs={'nombre_centro': nombre_centro}) )

	else:
		form = forms.AsesorDepartamentoFormSelect(id_departamento=id_departamento)

	return render_to_response('asesorias/AsesorCursoAcademico/selectAsesorDepartamento.html', {'user': request.user, 'form': form, 'nombre_departamento': nombre_departamento})

def selectAsesor(request):
	# Se ha introducido un asesor.
	if request.method == 'POST':

		# Se obtiene el asesor y se valida.
		form = forms.AsesorFormSelect(request.POST)

		# Si es valido se redirige a listar asesores curso academico.
		if form.is_valid():
			asesor = request.POST['asesor']

			# Se crea una instancia del asesor para pasar el nombre de asesor por argumento.
			instancia_asesor = models.Asesor.objects.get(pk=asesor)

			return HttpResponseRedirect( reverse('listAsesorCursoAcademico_Asesor', kwargs={'dni_pasaporte': asesor, 'orden': 'curso_academico'}) )

		else:
			HttpResponseRedirect( reverse('selectAsesor_AsesorCursoAcademico') )

	else:
		form = forms.AsesorFormSelect()

	return render_to_response('asesorias/AsesorCursoAcademico/selectAsesor.html', {'user': request.user, 'form': form})

def listAsesorCursoAcademico_Departamento(request, nombre_departamento, dni_pasaporte, orden):
	# Se comprueba que exista el departamento pasado por argumento.
	instancia_departamento = vistasDepartamento.obtenerDepartamento(nombre_departamento)

	# El departamento no existe, se redirige.
	if not (instancia_departamento):
		return HttpResponseRedirect( reverse('selectDepartamentoOAsesor_AsesorCursoAcademico') )

	# Se comprueba que exista el asesor pasado por argumento.
	existe_asesor_curso_academico = models.AsesorCursoAcademico.objects.filter(id_departamento=instancia_departamento.id_departamento, dni_pasaporte=dni_pasaporte)

	# El asesor no existe, se redirige.
	if not (existe_asesor_curso_academico):
		return HttpResponseRedirect( reverse('selectDepartamentoOAsesor_AsesorCursoAcademico') )

	# Se obtiene una lista con todos los asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.filter(id_departamento=instancia_departamento.id_departamento, dni_pasaporte=dni_pasaporte).order_by('dni_pasaporte')

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
			for asesor in lista_asesores_curso_academico:
				# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
				cadena = unicode(instancia_asesor.curso_academico)

				# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
				if cadena.find(busqueda) >= 0:
					lista_aux.append(asesor)

			# La lista final a devolver sera la lista auxiliar.
			lista_asesores_curso_academico = lista_aux

		else:
			busqueda = False
	# No se ha realizado busqueda.
	else:
		# Formulario para una posible busqueda.
		form = forms.SearchForm()
		busqueda = False

		if (orden == '_dni_pasaporte'):
			lista_asesores_curso_academico = reversed(lista_asesores_curso_academico)

	return render_to_response('asesorias/AsesorCursoAcademico/listAsesorCursoAcademico_Departamento.html', {'user': request.user, 'form': form, 'lista_asesores_curso_academico': lista_asesores_curso_academico, 'busqueda': busqueda, 'nombre_departamento': nombre_departamento, 'asesor': dni_pasaporte, 'orden': orden})

def listAsesorCursoAcademico_Asesor(request, dni_pasaporte, orden):
	# Se comprueba que exista el asesor pasado por argumento.
	instancia_asesor = vistasAsesor.obtenerAsesor(dni_pasaporte)

	# El asesor no existe, se redirige.
	if not (instancia_asesor):
		return HttpResponseRedirect( reverse('selectDepartamentoOAsesor_AsesorCursoAcademico') )

	# Se obtiene una lista con todos los asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.filter(dni_pasaporte=dni_pasaporte).order_by('curso_academico')

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
			for asesor in lista_asesores_curso_academico:
				# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
				cadena = unicode(asesor.curso_academico)

				# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
				if cadena.find(busqueda) >= 0:
					lista_aux.append(asesor)

			# La lista final a devolver sera la lista auxiliar.
			lista_asesores_curso_academico = lista_aux

		else:
			busqueda = False
	# No se ha realizado busqueda.
	else:
		# Formulario para una posible busqueda.
		form = forms.SearchForm()
		busqueda = False

		if (orden == '_curso_academico'):
			lista_asesores_curso_academico = reversed(lista_asesores_curso_academico)

	return render_to_response('asesorias/AsesorCursoAcademico/listAsesorCursoAcademico_Asesor.html', {'user': request.user, 'form': form, 'lista_asesores_curso_academico': lista_asesores_curso_academico, 'busqueda': busqueda, 'asesor': dni_pasaporte, 'orden': orden})

def generarPDFListaAsesoresCursoAcademico(request):
	# Se obtiene una lista con todos los asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.all()

	return vistasPDF.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_asesores_curso_academico, 'name': 'asesores curso academico',} )
