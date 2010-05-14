from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasReunion, vistasPreguntaAsesor

# Comprueba si existe una reunion - pregunta de asesor y, de ser asi, la devuelve.
def obtenerReunion_preguntaAsesor(dni_pasaporte_alumno, curso_academico, id_reunion, dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor):
	try:
		# Obtiene la instancia de reunion - pregunta de asesor.
		resultado = models.ReunionPreguntaAsesor.objects.get(dni_pasaporte_alumno=dni_pasaporte_alumno, curso_academico=curso_academico, id_reunion=id_reunion, dni_pasaporte_asesor=dni_pasaporte_asesor, id_entrevista_asesor=id_entrevista_asesor, id_pregunta_asesor=id_pregunta_asesor)
	except:
		resultado = False
	return resultado

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

def editReunion_preguntaAsesor(request, dni_pasaporte_alumno, curso_academico, id_reunion, dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor):
	# Se obtiene la instancia de la reunion - pregunta de asesor.
	instancia_reunion_preguntaAsesor = obtenerReunion_preguntaAsesor(dni_pasaporte_alumno, curso_academico, id_reunion, dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor)
	# Si existe se edita.
	if instancia_reunion_preguntaAsesor:
		# Se carga el formulario para la reunion - pregunta de asesor existente.
		form = forms.Reunion_PreguntaAsesorForm(instance=instancia_reunion_preguntaAsesor, initial={'reunion': vistasReunion.obtenerReunion(dni_pasaporte_alumno, curso_academico, id_reunion).codigo_reunion, 'pregunta_asesor': vistasPreguntaAsesor.obtenerPreguntaAsesor(dni_pasaporte_asesor, curso_academico, id_entrevista_asesor, id_pregunta_asesor).codigo_preguntaAsesor})
		# Se ha modificado el formulario original.
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

			# Se actualiza el formulario con la nueva informacion.
			form = forms.Reunion_PreguntaAsesorForm(datos_reunion_preguntaAsesor, instance=instancia_reunion_preguntaAsesor)

			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar reuniones - preguntas de asesor.
				return HttpResponseRedirect( reverse('listReunion_preguntaAsesor') )
	# La matricula no existe
	else:
		form = False
	return render_to_response('asesorias/Reunion_PreguntaAsesor/editReunion_preguntaAsesor.html', {'form': form})

def delReunion_preguntaAsesor(request, dni_pasaporte_alumno, curso_academico, id_reunion, dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor):
	# Se obtiene la instancia de la reunion - pregunta de asesor.
	instancia_reunion_preguntaAsesor = obtenerReunion_preguntaAsesor(dni_pasaporte_alumno, curso_academico, id_reunion, dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor)

	# Si existe se elimina.
	if instancia_reunion_preguntaAsesor:
		instancia_reunion_preguntaAsesor.delete()
		# Redirige a la pagina de listar reuniones - preguntas de asesor.
		return HttpResponseRedirect( reverse('listReunion_preguntaAsesor') )
	# La reunion - pregunta de asesor no existe.
	else:
		error = True
	return render_to_response('asesorias/Reunion_PreguntaAsesor/delReunion_preguntaAsesor.html', {'error': error})

def listReunion_preguntaAsesor(request):
	# Se obtiene una lista con todas las reuniones - pregunta de asesor.
	lista_reuniones_pregunta_de_asesor = models.ReunionPreguntaAsesor.objects.all()
	return render_to_response('asesorias/Reunion_PreguntaAsesor/listReunion_preguntaAsesor.html', {'lista_reuniones_pregunta_de_asesor': lista_reuniones_pregunta_de_asesor})