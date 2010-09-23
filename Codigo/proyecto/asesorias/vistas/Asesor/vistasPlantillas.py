from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

def listPlantillasOficiales(request, curso_academico, orden):
     # Se obtiene una lista con todos las plantillas de entrevista
    # oficiales.
    lista_plantillas_entrevista_oficial = \
        models.PlantillaEntrevistaOficial.objects.order_by(
        'descripcion')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']
            lista_plantillas_entrevista_oficial = \
                lista_plantillas_entrevista_oficial.filter(
                descripcion__contains=busqueda)
        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_descripcion':
            lista_plantillas_entrevista_oficial = \
                lista_plantillas_entrevista_oficial.reverse()

    return render_to_response(PATH +
        'listPlantillasOficiales.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'lista_plantillas_entrevista_oficial':
        lista_plantillas_entrevista_oficial,
        'busqueda': busqueda, 'orden': orden})
