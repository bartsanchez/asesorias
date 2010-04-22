from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsignatura

# Comprueba si existe una asignatura curso academico y, de ser asi, la devuelve.
def obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	try:
		# Obtiene la instancia de asignatura para posteriormente obtener el id.
		instancia_asignatura= vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura)

		# Obtiene la instancia de la asignatura curso academico.
		resultado = models.AsignaturaCursoAcademico.objects.get(id_centro=instancia_asignatura.getIdCentro(), id_titulacion=instancia_asignatura.getIdTitulacion(), id_asignatura=instancia_asignatura.getIdAsignatura(), curso_academico=curso_academico)
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
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsignaturaCursoAcademicoForm()
		error = False
	return render_to_response('asesorias/AsignaturaCursoAcademico/addAsignaturaCursoAcademico.html', {'form': form, 'error': error})

def editAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	# Se obtiene la instancia de la asignatura curso academico.
	instancia_asignatura_curso_academico= obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico)
	# Si existe se edita.
	if instancia_asignatura_curso_academico:
		# Se carga el formulario para la asignatura existente.
		form = forms.AsignaturaCursoAcademicoForm(instance=instancia_asignatura_curso_academico, initial={'asignatura': vistasAsignatura.obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura).codigo_asignatura})
		error = False
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
				# Redirige a la pagina de inicio.
				return HttpResponseRedirect('/asesorias/')
			else:
				error = 'Formulario invalido'

		return render_to_response('asesorias/AsignaturaCursoAcademico/editAsignaturaCursoAcademico.html', {'form': form, 'error': error})
	# La asignatura curso academico no existe
	else:
		error = 'No existe tal asignatura curso academico.'
	return render_to_response('asesorias/AsignaturaCursoAcademico/editAsignaturaCursoAcademico.html', {'error': error})

def delAsignaturaCursoAcademico(request, nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico):
	# Se obtiene la instancia de la asignatura curso academico.
	instancia_asignatura_curso_academico= obtenerAsignaturaCursoAcademico(nombre_centro, nombre_titulacion, plan_estudios, nombre_asignatura, curso_academico)
	# Si existe se elimina.
	if instancia_asignatura_curso_academico:
		instancia_asignatura_curso_academico.delete()
		error = False
	# La asignatura no existe.
	else:
		error = 'No se ha podido eliminar la asignatura curso academico.'
	return render_to_response('asesorias/AsignaturaCursoAcademico/delAsignaturaCursoAcademico.html', {'error': error})