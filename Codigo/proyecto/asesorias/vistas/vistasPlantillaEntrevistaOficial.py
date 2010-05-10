from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe una plantilla y, de ser asi, lo devuelve.
def obtenerPlantillaEntrevistaOficial(id_entrevista_oficial):
	try:
		# Obtiene la plantilla cuyo id es id_entrevista_oficial.
		resultado = models.PlantillaEntrevistaOficial.objects.get(pk=id_entrevista_oficial)
	except:
		resultado = False
	return resultado

def addPlantillaEntrevistaOficial(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.PlantillaEntrevistaOficialForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar plantillas de entrevista oficiales.
			return HttpResponseRedirect( reverse('listPlantillaEntrevistaOficial') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.PlantillaEntrevistaOficialForm()
	return render_to_response('asesorias/PlantillaEntrevistaOficial/addPlantillaEntrevistaOficial.html', {'form': form})

def editPlantillaEntrevistaOficial(request, id_entrevista_oficial):
	# Se obtiene la instancia de la plantilla.
	instancia_plantilla_entrevista_oficial = obtenerPlantillaEntrevistaOficial(id_entrevista_oficial)
	# Si existe se edita.
	if instancia_plantilla_entrevista_oficial:
		# Se carga el formulario para la plantilla existente.
		form = forms.PlantillaEntrevistaOficialForm(instance=instancia_plantilla_entrevista_oficial)
		# Se ha modificado el formulario original.
		if request.method == 'POST':
			# Se actualiza el formulario con la nueva informacion.
			form = forms.PlantillaEntrevistaOficialForm(request.POST, instance=instancia_plantilla_entrevista_oficial)
			# Si es valido se guarda.
			if form.is_valid():
				form.save()
				# Redirige a la pagina de listar plantillas de entrevista oficiales.
				return HttpResponseRedirect( reverse('listPlantillaEntrevistaOficial') )
	# La plantilla no existe.
	else:
		form = False
	return render_to_response('asesorias/PlantillaEntrevistaOficial/editPlantillaEntrevistaOficial.html', {'form': form})

def delPlantillaEntrevistaOficial(request, id_entrevista_oficial):
	# Se obtiene la instancia del asesor.
	instancia_plantilla_entrevista_oficial = obtenerPlantillaEntrevistaOficial(id_entrevista_oficial)
	# Si existe se elimina.
	if instancia_plantilla_entrevista_oficial:
		instancia_plantilla_entrevista_oficial.delete()
		# Redirige a la pagina de listar plantillas de entrevista oficiales.
		return HttpResponseRedirect( reverse('listPlantillaEntrevistaOficial') )
	# La plantilla no existe.
	else:
		error = True
	return render_to_response('asesorias/PlantillaEntrevistaOficial/delPlantillaEntrevistaOficial.html', {'error': error})

def listPlantillaEntrevistaOficial(request):
	# Se obtiene una lista con todos las plantillas de entrevista oficiales.
	lista_plantillas_entrevista_oficial = models.PlantillaEntrevistaOficial.objects.all()
	return render_to_response('asesorias/PlantillaEntrevistaOficial/listPlantillaEntrevistaOficial.html', {'lista_plantillas_entrevista_oficial': lista_plantillas_entrevista_oficial})