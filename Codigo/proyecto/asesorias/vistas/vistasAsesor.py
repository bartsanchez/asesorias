from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

def addAsesor(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.AsesorForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de inicio.
			return HttpResponseRedirect('/asesorias/asesor/list')
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.AsesorForm()
	return render_to_response('asesorias/Asesor/addAsesor.html', {'form': form})

def listAsesor(request):
	# Se obtiene una lista con todos los asesores.
	lista_asesores = models.Asesor.objects.all()
	return render_to_response('asesorias/Asesor/listAsesor.html', {'lista_asesores': lista_asesores })