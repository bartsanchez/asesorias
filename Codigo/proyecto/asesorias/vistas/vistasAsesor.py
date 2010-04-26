from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un asesor y, de ser asi, lo devuelve.
def obtenerAsesor(dni_pasaporte):
	try:
		# Obtiene el asesor cuyo dni es dni_pasaporte.
		resultado = models.Asesor.objects.get(pk=dni_pasaporte)
	except:
		resultado = False
	return resultado

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

def delAsesor(request, dni_pasaporte):
	# Se obtiene la instancia del asesor.
	instancia_asesor = obtenerAsesor(dni_pasaporte)
	# Si existe se elimina.
	if instancia_asesor:
		instancia_asesor.delete()
		return HttpResponseRedirect('/asesorias/asesor/list')
	# El asesor no existe.
	else:
		error = True
	return render_to_response('asesorias/Asesor/delAsesor.html', {'error': error})

def listAsesor(request):
	# Se obtiene una lista con todos los asesores.
	lista_asesores = models.Asesor.objects.all()
	return render_to_response('asesorias/Asesor/listAsesor.html', {'lista_asesores': lista_asesores })