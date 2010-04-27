from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

def addAsesorCursoAcademico(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AsesorCursoAcademicoForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/asesorCursoAcademico/list')
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsesorCursoAcademicoForm()
	return render_to_response('asesorias/AsesorCursoAcademico/addAsesorCursoAcademico.html', {'form': form})

def listAsesorCursoAcademico(request):
	# Se obtiene una lista con todos las asesores curso academico.
	lista_asesores_curso_academico = models.AsesorCursoAcademico.objects.all()
	return render_to_response('asesorias/AsesorCursoAcademico/listAsesorCursoAcademico.html', {'lista_asesores_curso_academico': lista_asesores_curso_academico})
