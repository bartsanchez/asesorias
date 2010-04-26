from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un departamento y, de ser asi, lo devuelve.
def obtenerDepartamento(nombre_departamento):
	try:
		# Obtiene el departamento cuyo nombre es departamento.
		resultado = models.Departamento.objects.get(nombre_departamento=nombre_departamento)
	except:
		resultado = False
	return resultado

def addDepartamento(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.DepartamentoForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/departamento/list')
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.DepartamentoForm()
	return render_to_response('asesorias/Departamento/addDepartamento.html', {'form': form})

def editDepartamento(request, nombre_departamento):
	# Se obtiene la instancia del departamento.
	instancia_departamento= obtenerDepartamento(nombre_departamento)
	# Si existe se edita.
	if instancia_departamento:
		# Se carga el formulario para el centro existente.
		form = forms.DepartamentoForm(instance=instancia_departamento)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.DepartamentoForm(request.POST, instance=instancia_departamento)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de inicio.
				return HttpResponseRedirect('/asesorias/departamento/list')
	# El departamento no existe.
	else:
		form = False
	return render_to_response('asesorias/Departamento/editDepartamento.html', {'form': form})

def delDepartamento(request, nombre_departamento):
	# Se obtiene la instancia del departamento.
	instancia_departamento = obtenerDepartamento(nombre_departamento)
	# Si existe se elimina.
	if instancia_departamento:
		instancia_departamento.delete()
		return HttpResponseRedirect('/asesorias/departamento/list')
	# El centro no existe.
	else:
		error = True
	return render_to_response('asesorias/Departamento/delDepartamento.html', {'error': error})

def listDepartamento(request):
	# Se obtiene una lista con todos los departamentos.
	lista_departamentos = models.Departamento.objects.all()
	return render_to_response('asesorias/Departamento/listDepartamento.html', {'lista_departamentos': lista_departamentos})
