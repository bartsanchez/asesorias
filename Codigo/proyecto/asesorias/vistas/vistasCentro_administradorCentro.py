from django.core.urlresolvers import reverse
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
		resultado = models.CentroAdministradorCentro.objects.get(id_centro=instancia_centro.id_centro, id_adm_centro=instancia_administrador_centro.getId())
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
			# Redirige a la pagina de listar centro - administradorCentro.
			return HttpResponseRedirect( reverse('listCentro_administradorCentro') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.Centro_AdministradorCentroForm()
	return render_to_response('asesorias/Centro_AdministradorCentro/addCentro_administradorCentro.html', {'form': form})

def editCentro_administradorCentro(request, centro, administrador_centro):
	# Se obtiene la instancia del centro_administradorCentro.
	instancia_centro_administradorCentro = obtenerCentro_administradorCentro(centro, administrador_centro)
	# Si existe se edita.
	if instancia_centro_administradorCentro:
		# Se carga el formulario para el centro existente.
		form = forms.Centro_AdministradorCentroForm(instance=instancia_centro_administradorCentro)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.Centro_AdministradorCentroForm(request.POST, instance=instancia_centro_administradorCentro)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar centro - administradorCentro.
				return HttpResponseRedirect( reverse('listCentro_administradorCentro') )
	# El centro_administradorCentro no existe
	else:
		form = False
	return render_to_response('asesorias/Centro_AdministradorCentro/editCentro_administradorCentro.html', {'form': form})

def delCentro_administradorCentro(request, centro, administrador_centro):
	# Se obtiene la instancia del centro_administradorCentro.
	instancia_centro_administradorCentro = obtenerCentro_administradorCentro(centro, administrador_centro)
	# Si existe se elimina.
	if instancia_centro_administradorCentro:
		instancia_centro_administradorCentro.delete()
		# Redirige a la pagina de listar centro - administradorCentro.
		return HttpResponseRedirect( reverse('listCentro_administradorCentro') )
	# El centro_administradorCentro no existe.
	else:
		error = True
	return render_to_response('asesorias/Centro_AdministradorCentro/delCentro_administradorCentro.html', {'error': error})

def listCentro_administradorCentro(request):
	# Se obtiene una lista con todos los centros administrador de centro.
	lista_centros_administradorCentro = models.CentroAdministradorCentro.objects.all()
	return render_to_response('asesorias/Centro_AdministradorCentro/listCentro_administradorCentro.html', {'lista_centros_administradorCentro': lista_centros_administradorCentro})
