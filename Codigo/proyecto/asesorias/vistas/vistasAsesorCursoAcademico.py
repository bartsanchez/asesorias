from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasDepartamento

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

def selectDepartamento(request):
	# Se ha introducido un centro.
	if request.method == 'POST':

		# Se obtiene el departamento y se valida.
		form = forms.DepartamentoFormSelect(request.POST)

		# Si es valido se redirige a listar departamentos.
		if form.is_valid():
			departamento = request.POST['departamento']

			# Se crea una instancia del departamento para pasar el nombre de departamento por argumento.
			instancia_departamento = models.Departamento.objects.get(pk=departamento)

			return HttpResponseRedirect( reverse('selectAsesor_AsesorCursoAcademico', kwargs={'nombre_departamento': instancia_departamento.nombre_departamento}) )

		else:
			HttpResponseRedirect( reverse('selectDepartamento_AsesorCursoAcademico') )

	else:
		form = forms.DepartamentoFormSelect()

	return render_to_response('asesorias/AsesorCursoAcademico/selectDepartamento.html', {'user': request.user, 'form': form})

def selectAsesor(request, nombre_departamento):
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
		form = forms.TitulacionFormSelect(id_centro, request.POST)

		# Si es valido se redirige a listar asesores curso academico.
		if form.is_valid():
			asesor = request.POST['asesor_curso_academico']

			# Se crea una instancia del asesor para pasar los argumentos.
			instancia_asesor = models.AsesorCursoAcademico.objects.get(pk=asesor)

			return HttpResponseRedirect( reverse('listAsesorCursoAcademico', kwargs={'nombre_departamento': nombre_departamento, 'asesor': instancia_asesor.nombre_asesor, 'orden': 'dni_pasaporte'}) )

		else:
			return HttpResponseRedirect( reverse('selectTitulacion_Asignatura', kwargs={'nombre_centro': nombre_centro}) )

	else:
		form = forms.AsesorCursoAcademicoFormSelect(id_departamento=id_departamento)

	return render_to_response('asesorias/AsesorCursoAcademico/selectAsesor.html', {'user': request.user, 'form': form, 'nombre_departamento': nombre_departamento})

def listAsesorCursoAcademico(request):
	# Se obtiene una lista con todos las asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.all()
	return render_to_response('asesorias/AsesorCursoAcademico/listAsesorCursoAcademico.html', {'lista_asesores_curso_academico': lista_asesores_curso_academico})
