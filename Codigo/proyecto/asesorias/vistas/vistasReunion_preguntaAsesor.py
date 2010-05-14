from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

def addReunion_preguntaAsesor(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		#Se extraen los valores pasados por el metodo POST.
		codigo_reunion = request.POST['reunion']
		codigo_pregunta_asesor = request.POST['pregunta_asesor']
		respuesta = request.POST['respuesta']

		# Se obtiene una instancia de la reunion a traves de su id.
		instancia_reunion = models.Reunion.objects.get(pk=codigo_reunion)

		# Se determina dni_pasaporte_alumno, curso_academico e id_reunion para esa reunion.
		dni_pasaporte_alumno = instancia_reunion.dni_pasaporte
		curso_academico = instancia_reunion.curso_academico
		id_reunion = instancia_reunion.id_reunion

		# Se obtiene una instancia de la pregunta de asesor a traves de su id.
		instancia_pregunta_asesor = models.PreguntaAsesor.objects.get(pk=codigo_pregunta_asesor)

		# Se determina el dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor para esa pregunta de asesor.
		dni_pasaporte_asesor = instancia_pregunta_asesor.dni_pasaporte
		id_entrevista_asesor = instancia_pregunta_asesor.id_entrevista_asesor
		id_pregunta_asesor = instancia_pregunta_asesor.id_pregunta_asesor

		# Datos necesarios para crear la nueva reunion - pregunta de asesor.
		datos_reunion_preguntaAsesor = {'dni_pasaporte_alumno': dni_pasaporte_alumno, 'curso_academico': curso_academico, 'id_reunion': id_reunion, 'dni_pasaporte_asesor': dni_pasaporte_asesor, 'id_entrevista_asesor': id_entrevista_asesor, 'id_pregunta_asesor': id_pregunta_asesor, 'respuesta': respuesta, 'reunion': codigo_reunion, 'pregunta_asesor': codigo_pregunta_asesor}

		# Se obtienen los valores y se valida.
		form = forms.Reunion_PreguntaAsesorForm(datos_reunion_preguntaAsesor)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar reuniones - preguntas de asesor.
			return HttpResponseRedirect( reverse('listReunion_preguntaAsesor') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.Reunion_PreguntaAsesorForm()
	return render_to_response('asesorias/Reunion_PreguntaAsesor/addReunion_preguntaAsesor.html', {'form': form})

def listReunion_preguntaAsesor(request):
	# Se obtiene una lista con todas las reuniones - pregunta de asesor.
	lista_reuniones_pregunta_de_asesor = models.ReunionPreguntaAsesor.objects.all()
	return render_to_response('asesorias/Reunion_PreguntaAsesor/listReunion_preguntaAsesor.html', {'lista_reuniones_pregunta_de_asesor': lista_reuniones_pregunta_de_asesor})
