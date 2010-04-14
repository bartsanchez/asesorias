from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

# Comprueba si existe un administrador de centro.
def existeAdministradorCentro(admin_centro):
	try:
		models.AdministradorCentro.objects.get(pk=admin_centro)
		resultado = True
	except:
		resultado = False
	return resultado
