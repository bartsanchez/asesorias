from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

def addPreguntaOficial(request):
	# Se ha rellenado el formulario.
	if request.method == 'POST':
		# Se obtienen los valores y se valida.
		form = forms.PreguntaOficialForm(request.POST)
		if form.is_valid():
			# Se guarda la informacion del formulario en el sistema.
			form.save()
			# Redirige a la pagina de listar preguntas oficiales.
			return HttpResponseRedirect( reverse('listPreguntaOficial') )
	# Si aun no se ha rellenado el formulario, se genera uno en blanco.
	else:
		form = forms.PreguntaOficialForm()
	return render_to_response('asesorias/PreguntaOficial/addPreguntaOficial.html', {'form': form})

def listPreguntaOficial(request):
	# Se obtiene una lista con todos las preguntas oficiales.
	lista_preguntas_oficiales = models.PreguntaOficial.objects.all()
	return render_to_response('asesorias/PreguntaOficial/listPreguntaOficial.html', {'lista_preguntas_oficiales': lista_preguntas_oficiales})