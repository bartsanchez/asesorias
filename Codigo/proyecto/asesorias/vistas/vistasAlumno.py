from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un alumno y, de ser asi, lo devuelve.
def obtenerAlumno(dni_pasaporte):
	try:
		# Obtiene el alumno cuyo dni es dni_pasaporte.
		resultado = models.Alumno.objects.get(pk=dni_pasaporte)
	except:
		resultado = False
	return resultado

def addAlumno(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AlumnoForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar asesores.
			return HttpResponseRedirect( reverse('listAlumno') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AlumnoForm()
	return render_to_response('asesorias/Alumno/addAlumno.html', {'form': form})

def editAlumno(request, dni_pasaporte):
	# Se obtiene la instancia del alumno.
	instancia_alumno = obtenerAlumno(dni_pasaporte)
	# Si existe se edita.
	if instancia_alumno:
		# Se carga el formulario para el alumno existente.
		form = forms.AlumnoForm(instance=instancia_alumno)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.AlumnoForm(request.POST, instance=instancia_alumno)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar asesores.
				return HttpResponseRedirect( reverse('listAlumno') )
	# El alumno no existe.
	else:
		form = False
	return render_to_response('asesorias/Alumno/editAlumno.html', {'form': form})

def delAlumno(request, dni_pasaporte):
	# Se obtiene la instancia del alumno.
	instancia_alumno = obtenerAlumno(dni_pasaporte)
	# Si existe se elimina.
	if instancia_alumno:
		instancia_alumno.delete()
		# Redirige a la pagina de listar alumnos.
		return HttpResponseRedirect( reverse('listAlumno') )
	# El alumno no existe.
	else:
		error = True
	return render_to_response('asesorias/Alumno/delAlumno.html', {'error': error})

def listAlumno(request):
	# Se obtiene una lista con todos los alumnos.
	lista_alumnos = models.Alumno.objects.all()
	return render_to_response('asesorias/Alumno/listAlumno.html', {'lista_alumnos': lista_alumnos})