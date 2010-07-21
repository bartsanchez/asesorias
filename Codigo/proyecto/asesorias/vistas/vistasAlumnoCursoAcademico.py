from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAlumno
from asesorias.utils import vistasPDF

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

			dni_pasaporte = request.POST['dni_pasaporte']

			# Redirige a la pagina de listar alumnos curso academico.
			return HttpResponseRedirect( reverse('listAlumnoCursoAcademico', kwargs={'dni_pasaporte': dni_pasaporte, 'orden': 'curso_academico'}) )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AlumnoCursoAcademicoForm()
	return render_to_response('asesorias/AlumnoCursoAcademico/addAlumnoCursoAcademico.html', {'user': request.user, 'form': form})

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

def selectAlumno(request):
	# Se ha introducido un alumno.
	if request.method == 'POST':

		# Se obtiene el alumno y se valida.
		form = forms.AlumnoFormSelect(request.POST)

		# Si es valido se redirige a listar alumnos curso academico.
		if form.is_valid():
			alumno = request.POST['alumno']

			# Se crea una instancia del alumno para pasar el nombre de alumno por argumento.
			instancia_alumno = models.Alumno.objects.get(pk=alumno)

			return HttpResponseRedirect( reverse('listAlumnoCursoAcademico', kwargs={'dni_pasaporte': alumno, 'orden': 'curso_academico'}) )

		else:
			HttpResponseRedirect( reverse('selectAlumno_AlumnoCursoAcademico') )

	else:
		form = forms.AlumnoFormSelect()

	return render_to_response('asesorias/AlumnoCursoAcademico/selectAlumno.html', {'user': request.user, 'form': form})

def listAlumnoCursoAcademico(request, dni_pasaporte, orden):
	# Se comprueba que exista el alumno pasado por argumento.
	instancia_alumno = vistasAlumno.obtenerAlumno(dni_pasaporte)

	# El alumno no existe, se redirige.
	if not (instancia_alumno):
		return HttpResponseRedirect( reverse('selectAlumno_AlumnoCursoAcademico') )

	# Se obtiene una lista con todos los alumnos curso academico.
	lista_alumnos_curso_academico = models.AlumnoCursoAcademico.objects.filter(dni_pasaporte=dni_pasaporte).order_by('curso_academico')

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
			for alumno in lista_alumnos_curso_academico:
				# Se crea una cadena auxiliar para examinar si se encuentra el resultado de la busqueda.
				cadena = unicode(alumno.curso_academico)

				# Si se encuentra la busqueda el elemento se incluye en la lista auxiliar.
				if cadena.find(busqueda) >= 0:
					lista_aux.append(alumno)

			# La lista final a devolver sera la lista auxiliar.
			lista_alumnos_curso_academico = lista_aux

		else:
			busqueda = False
	# No se ha realizado busqueda.
	else:
		# Formulario para una posible busqueda.
		form = forms.SearchForm()
		busqueda = False

		if (orden == '_curso_academico'):
			lista_alumnos_curso_academico = reversed(lista_alumnos_curso_academico)

	return render_to_response('asesorias/AlumnoCursoAcademico/listAlumnoCursoAcademico.html', {'user': request.user, 'form': form, 'lista_alumnos_curso_academico': lista_alumnos_curso_academico, 'busqueda': busqueda, 'alumno': dni_pasaporte, 'orden': orden})

def generarPDFListaAlumnosCursoAcademico(request):
	# Se obtiene una lista con todos los alumnos curso academico.
	lista_alumnos_curso_academico = models.AlumnoCursoAcademico.objects.all()

	return vistasPDF.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_alumnos_curso_academico, 'name': 'alumnos curso academico',} )
