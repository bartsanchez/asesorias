from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsignatura, vistasAsignaturaCursoAcademico, vistasAlumnoCursoAcademico, vistasCentro, vistasTitulacion

# Comprueba si existe una matricula y, de ser asi, la devuelve.
def obtenerMatricula(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
	try:
		# Obtiene la instancia de la asignatura para posteriormente obtener los id's correspondientes.
		instancia_asignatura = vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)

		# Obtiene la instancia del alumno curso academico para posteriormente obtener los id's correspondientes.
		instancia_alumno_curso_academico = vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico)

		# Obtiene la instancia de matricula.
		resultado = models.Matricula.objects.get(id_centro=instancia_asignatura.id_centro, id_titulacion=instancia_asignatura.id_titulacion, id_asignatura=instancia_asignatura.id_asignatura, curso_academico=instancia_alumno_curso_academico.curso_academico, dni_pasaporte=unicode(instancia_alumno_curso_academico.dni_pasaporte))
	except:
		resultado = False
	return resultado

def addMatricula(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		#Se extraen los valores pasados por el metodo POST.
		codigo_asignaturaCursoAcademico = request.POST['asignatura_curso_academico']
		codigo_alumnoCursoAcademico = request.POST['alumno_curso_academico']
		comentario = request.POST['comentario']

		# Se obtiene una instancia de la asignatura curso academico a traves de su id.
		instancia_asignatura_curso_academico = models.AsignaturaCursoAcademico.objects.get(pk=codigo_asignaturaCursoAcademico)

		# Se determina id_centro, id_titulacion e id_asignatura para esa asignatura curso academico.
		id_centro = instancia_asignatura_curso_academico.id_centro
		id_titulacion = instancia_asignatura_curso_academico.id_titulacion
		id_asignatura = instancia_asignatura_curso_academico.id_asignatura

		# Se obtiene una instancia del alumno curso academico a traves de su id.
		instancia_alumno_curso_academico = models.AlumnoCursoAcademico.objects.get(pk=codigo_alumnoCursoAcademico)

		# Se determina el curso_academico para ese alumno curso academico.
		dni_pasaporte = instancia_alumno_curso_academico.dni_pasaporte
		curso_academico = instancia_alumno_curso_academico.curso_academico

		# Datos necesarios para crear la nueva asignatura
		datos_matricula = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'curso_academico': curso_academico, 'dni_pasaporte': dni_pasaporte, 'comentario': comentario, 'asignatura_curso_academico': codigo_asignaturaCursoAcademico, 'alumno_curso_academico': codigo_alumnoCursoAcademico}

		# Se obtienen los valores y se valida.
		form = forms.MatriculaForm(datos_matricula)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar matriculas.
			return HttpResponseRedirect( reverse('listMatricula') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.MatriculaForm()
	return render_to_response('asesorias/Matricula/addMatricula.html', {'form': form})

def editMatricula(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
	# Se obtiene la instancia de la matricula.
	instancia_matricula = obtenerMatricula(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte)
	# Si existe se edita.
	if instancia_matricula:
		# Se carga el formulario para la matricula existente.
		form = forms.MatriculaForm(instance=instancia_matricula, initial={'asignatura_curso_academico': vistasAsignaturaCursoAcademico.obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico).codigo_asignaturaCursoAcademico, 'alumno_curso_academico': vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico).codigo_alumnoCursoAcademico})
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se obtienen el resto de valores necesarios a traves de POST.
			codigo_asignaturaCursoAcademico = request.POST['asignatura_curso_academico']
			codigo_alumnoCursoAcademico = request.POST['alumno_curso_academico']
			comentario = request.POST['comentario']

			# Se obtiene una instancia de la asignatura curso academico a traves de su id.
			instancia_asignatura_curso_academico = models.AsignaturaCursoAcademico.objects.get(pk=codigo_asignaturaCursoAcademico)

			# Se determina id_centro, id_titulacion e id_asignatura para esa asignatura curso academico.
			id_centro = instancia_asignatura_curso_academico.id_centro
			id_titulacion = instancia_asignatura_curso_academico.id_titulacion
			id_asignatura = instancia_asignatura_curso_academico.id_asignatura

			# Se obtiene una instancia del alumno curso academico a traves de su id.
			instancia_alumno_curso_academico = models.AlumnoCursoAcademico.objects.get(pk=codigo_alumnoCursoAcademico)

			# Se determina el curso_academico para ese alumno curso academico.
			dni_pasaporte = instancia_alumno_curso_academico.dni_pasaporte
			curso_academico = instancia_alumno_curso_academico.curso_academico

			# Datos necesarios para crear la nueva asignatura
			datos_matricula = {'id_centro': id_centro, 'id_titulacion': id_titulacion, 'id_asignatura': id_asignatura, 'curso_academico': curso_academico, 'dni_pasaporte': dni_pasaporte, 'comentario': comentario, 'asignatura_curso_academico': codigo_asignaturaCursoAcademico, 'alumno_curso_academico': codigo_alumnoCursoAcademico}

			# Se actualiza el formulario con la nueva informacion.
			form = forms.MatriculaForm(datos_matricula, instance=instancia_matricula)

			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar matriculas.
				return HttpResponseRedirect( reverse('listMatricula') )
	# La matricula no existe
	else:
		form = False
	return render_to_response('asesorias/Matricula/editMatricula.html', {'form': form})

def delMatricula(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
	# Se obtiene la instancia de la matricula.
	instancia_matricula = obtenerMatricula(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte)

	# Si existe se elimina.
	if instancia_matricula:
		instancia_matricula.delete()
		# Redirige a la pagina de listar matriculas.
		return HttpResponseRedirect( reverse('listMatricula') )
	# La matricula no existe.
	else:
		error = True
	return render_to_response('asesorias/Matricula/delMatricula.html', {'error': error})

def selectAsignaturaCursoAcademicoOAlumnoCursoAcademico(request):
	return render_to_response('asesorias/Matricula/selectAsignaturaCursoAcademicoOAlumnoCursoAcademico.html', {'user': request.user})

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

			return HttpResponseRedirect( reverse('selectTitulacion_Matricula', kwargs={'nombre_centro': instancia_centro.nombre_centro}) )

		else:
			return HttpResponseRedirect( reverse('selectCentro_Matricula') )

	else:
		form = forms.CentroFormSelect()

	return render_to_response('asesorias/Matricula/selectCentro.html', {'user': request.user, 'form': form})

def selectTitulacion(request, nombre_centro):
	# Se obtiene el posible centro.
	instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

	# Se comprueba que exista el centro.
	if not instancia_centro:
		return HttpResponseRedirect( reverse('selectCentro_Matricula') )
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

			return HttpResponseRedirect( reverse('selectAsignatura_Matricula', kwargs={'nombre_centro': instancia_titulacion.determinarNombreCentro(), 'nombre_titulacion': instancia_titulacion.nombre_titulacion, 'plan_estudios': instancia_titulacion.plan_estudios}) )

		else:
			return HttpResponseRedirect( reverse('selectTitulacion_Matricula', kwargs={'nombre_centro': nombre_centro}) )

	else:
		form = forms.TitulacionFormSelect(id_centro=id_centro)

	return render_to_response('asesorias/Matricula/selectTitulacion.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro})

def selectAsignatura(request, nombre_centro, nombre_titulacion, plan_estudios):
	# Se obtiene la posible titulacion.
	instancia_titulacion = vistasTitulacion.obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios)

	# Se comprueba que exista la titulacion.
	if not instancia_titulacion:
		return HttpResponseRedirect( reverse('selectTitulacion_Matricula', kwargs={'nombre_centro': nombre_centro}) )
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

			return HttpResponseRedirect( reverse('listAsignaturaCursoAcademico', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios, 'nombre_asignatura': instancia_asignatura.nombre_asignatura, 'orden': 'curso_academico'}) )

		else:
			return HttpResponseRedirect( reverse('selectAsignatura_Matricula', kwargs={'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios}) )

	else:
		form = forms.AsignaturaFormSelect(id_centro=id_centro, id_titulacion=id_titulacion)

	return render_to_response('asesorias/Matricula/selectAsignatura.html', {'user': request.user, 'form': form, 'nombre_centro': nombre_centro, 'nombre_titulacion': nombre_titulacion, 'plan_estudios': plan_estudios})

def listMatricula(request):
	# Se obtiene una lista con todas las matriculsa.
	lista_matriculas = models.Matricula.objects.all()
	return render_to_response('asesorias/Matricula/listMatricula.html', {'lista_matriculas': lista_matriculas})
