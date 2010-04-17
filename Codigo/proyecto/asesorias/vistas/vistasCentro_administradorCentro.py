from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasCentro, vistasAdministradorCentro

# Comprueba si existe un centro_administradorCentro y, de ser asi, lo devuelve.
def obtenerCentro_administradorCentro(centro, administrador_centro):
	try:
		# Obtiene las instancias de centro y del administrador para posteriormente obtener los id's.
		instancia_centro = vistasCentro.obtenerCentro(centro)
		instancia_administrador_centro = vistasAdministradorCentro.obtenerAdministradorCentro(administrador_centro)
		# Obtiene el centro_administradorCentro cuyo centro es centro y cuyo administrador de centro es administrador_centro, a traves de los id's.
		resultado = models.CentroAdministradorCentro.objects.get(id_centro=instancia_centro.getId(), id_adm_centro=instancia_administrador_centro.getId())
	except:
		resultado = False
	return resultado

def addCentro_administradorCentro(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.Centro_AdministradorCentroForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/')
		else:
			error = 'Formulario invalido.'
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.Centro_AdministradorCentroForm()
		error = False
	return render_to_response('asesorias/Centro_AdministradorCentro/addCentro_administradorCentro.html', {'form': form, 'error': error})

def editCentro_administradorCentro(request, centro, administrador_centro):
	# Se obtiene la instancia del centro_administradorCentro.
	instancia_centro_administradorCentro = obtenerCentro_administradorCentro(centro, administrador_centro)
	# Si existe se edita.
	if instancia_centro_administradorCentro:
		# Se carga el formulario para el centro existente.
		form = forms.Centro_AdministradorCentroForm(instance=instancia_centro_administradorCentro)
		error = False
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.Centro_AdministradorCentroForm(request.POST, instance=instancia_centro_administradorCentro)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de inicio.
				return HttpResponseRedirect('/asesorias/')
			else:
				error = 'Formulario invalido'
		return render_to_response('asesorias/Centro_AdministradorCentro/editCentro_administradorCentro.html', {'form': form, 'error': error})
	# El centro_administradorCentro no existe
	else:
		error = 'No existe tal administrador de centro en dicho centro.'
	return render_to_response('asesorias/Centro_AdministradorCentro/editCentro_administradorCentro.html', {'error': error})

def delCentro_administradorCentro(request, centro, administrador_centro):
	# Se obtiene la instancia del centro_administradorCentro.
	instancia_centro_administradorCentro = obtenerCentro_administradorCentro(centro, administrador_centro)
	# Si existe se elimina.
	if instancia_centro_administradorCentro:
		instancia_centro_administradorCentro.delete()
		error = False
	# El centro_administradorCentro no existe.
	else:
		error = 'No se ha podido eliminar el centro_administradorCentro.'
	return render_to_response('asesorias/Centro_AdministradorCentro/delCentro_administradorCentro.html', {'error': error})