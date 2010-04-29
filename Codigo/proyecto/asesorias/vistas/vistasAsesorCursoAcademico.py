from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

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

def listAsesorCursoAcademico(request):
	# Se obtiene una lista con todos las asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.all()
	return render_to_response('asesorias/AsesorCursoAcademico/listAsesorCursoAcademico.html', {'lista_asesores_curso_academico': lista_asesores_curso_academico})
