from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un administrador de centro y, de ser asi, lo devuelve.
def obtenerAdministradorCentro(administrador_centro):
	try:
		# Obtiene el administrador centro cuyo nombre es administrador_centro.
		resultado = models.AdministradorCentro.objects.get(nombre_adm_centro=administrador_centro)
	except:
		resultado = False
	return resultado

def addAdministradorCentro(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AdministradorCentroForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AdministradorCentroForm()
		error = False
	return render_to_response('asesorias/AdministradorCentro/addAdministradorCentro.html', {'form': form, 'error': error})

def editAdministradorCentro(request, administrador_centro):
	# Se obtiene la instancia del administrador de centro.
	instancia_admin_centro = obtenerAdministradorCentro(administrador_centro)
	# Si existe se edita.
	if instancia_admin_centro:
		# Se carga el formulario para el administrador de centro centro existente.
		form = forms.AdministradorCentroForm(instance=instancia_admin_centro)
		error = False
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.AdministradorCentroForm(request.POST, instance=instancia_admin_centro)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de inicio.
				return HttpResponseRedirect('/asesorias/')
			else:
				error = 'Formulario invalido'
		return render_to_response('asesorias/AdministradorCentro/editAdministradorCentro.html', {'form': form, 'error': error})
	# El administrador de centro no existe
	else:
		error = 'No existe tal administrador de centro'
	return render_to_response('asesorias/AdministradorCentro/editAdministradorCentro.html', {'error': error})

def delAdministradorCentro(request, administrador_centro):
	# Se obtiene la instancia del administrador de centro.
	instancia_admin_centro = obtenerAdministradorCentro(administrador_centro)
	# Si existe se elimina.
	if instancia_admin_centro:
		instancia_admin_centro.delete()
		error = False
	# El administrador de centro no existe.
	else:
		error = 'No se ha podido eliminar el administrador de centro.'
	return render_to_response('asesorias/AdministradorCentro/delAdministradorCentro.html', {'error': error})
