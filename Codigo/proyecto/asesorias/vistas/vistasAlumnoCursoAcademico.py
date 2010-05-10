from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un alumno curso academico y, de ser asi, la devuelve.
def obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico):
	try:
		# Obtiene la instancia de alumno curso academico.
		resultado = models.AlumnoCursoAcademico.objects.get(dni_pasaporte=dni_pasaporte, curso_academico=curso_academico)
	except:
		resultado = False
	return resultado

def addAlumnoCursoAcademico(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AlumnoCursoAcademicoForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar alumnos curso academico.
			return HttpResponseRedirect( reverse('listAlumnoCursoAcademico') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AlumnoCursoAcademicoForm()
	return render_to_response('asesorias/AlumnoCursoAcademico/addAlumnoCursoAcademico.html', {'form': form})

def editAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
	# Se obtiene la instancia del alumno curso academico.
	instancia_alumno_curso_academico= obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico)
	# Si existe se edita.
	if instancia_alumno_curso_academico:
		# Se carga el formulario para la asignatura existente.
		form = forms.AlumnoCursoAcademicoForm(instance=instancia_alumno_curso_academico)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.AlumnoCursoAcademicoForm(request.POST, instance=instancia_alumno_curso_academico)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar alumnos curso academico.
				return HttpResponseRedirect( reverse('listAlumnoCursoAcademico') )
	# El alumno curso academico no existe.
	else:
		form = False
	return render_to_response('asesorias/AlumnoCursoAcademico/editAlumnoCursoAcademico.html', {'form': form})

def delAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
	# Se obtiene la instancia del alumno curso academico.
	instancia_alumno_curso_academico= obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico)
	# Si existe se elimina.
	if instancia_alumno_curso_academico:
		instancia_alumno_curso_academico.delete()
		# Redirige a la pagina de listar alumnos curso academico.
		return HttpResponseRedirect( reverse('listAlumnoCursoAcademico') )
	# El alumno curso academico no existe.
	else:
		error = True
	return render_to_response('asesorias/AlumnoCursoAcademico/delAlumnoCursoAcademico.html', {'error': error})

def listAlumnoCursoAcademico(request):
	# Se obtiene una lista con todos las alumnos curso academico.
	lista_alumnos_curso_academico = models.AlumnoCursoAcademico.objects.all()
	return render_to_response('asesorias/AlumnoCursoAcademico/listAlumnoCursoAcademico.html', {'lista_alumnos_curso_academico': lista_alumnos_curso_academico})
