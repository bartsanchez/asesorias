from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms, views

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
			# Redirige a la pagina de listar administradores de centro.
			return HttpResponseRedirect( reverse('listAdministradorCentro') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AdministradorCentroForm()
	return render_to_response('asesorias/AdministradorCentro/addAdministradorCentro.html', {'user': request.user, 'form': form})

def editAdministradorCentro(request, administrador_centro):
	# Se obtiene la instancia del administrador de centro.
	instancia_admin_centro = obtenerAdministradorCentro(administrador_centro)
	# Si existe se edita.
	if instancia_admin_centro:
		# Se carga el formulario para el administrador de centro centro existente.
		form = forms.AdministradorCentroForm(instance=instancia_admin_centro)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.AdministradorCentroForm(request.POST, instance=instancia_admin_centro)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar administradores de centro.
				return HttpResponseRedirect( reverse('listAdministradorCentro') )
	# El administrador de centro no existe
	else:
		form = False
	return render_to_response('asesorias/AdministradorCentro/editAdministradorCentro.html', {'user': request.user, 'form': form})

def delAdministradorCentro(request, administrador_centro):
	# Se obtiene la instancia del administrador de centro.
	instancia_admin_centro = obtenerAdministradorCentro(administrador_centro)
	# Si existe se elimina.
	if instancia_admin_centro:
		instancia_admin_centro.delete()
		# Redirige a la pagina de listar administradores de centro.
		return HttpResponseRedirect( reverse('listAdministradorCentro') )
	# El administrador de centro no existe.
	else:
		error = True
	return render_to_response('asesorias/AdministradorCentro/delAdministradorCentro.html', {'user': request.user, 'error': error})

def listAdministradorCentro(request):
	# Se obtiene una lista con todos los administradores de centro.
	lista_administradores_centro = models.AdministradorCentro.objects.all()
	return render_to_response('asesorias/AdministradorCentro/listAdministradorCentro.html', {'user': request.user, 'lista_administradores_centro': lista_administradores_centro})

def generarPDFListaAdministradoresCentro(request):
	# Se obtiene una lista con todos los administradores de centro.
	lista_administradores_centro = models.AdministradorCentro.objects.all()

	return views.render_to_pdf( 'asesorias/plantilla_pdf.html', {'mylist': lista_administradores_centro, 'name': 'administradores de centro',} )
