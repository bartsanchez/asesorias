from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/PlantillaEntrevistaOficial/'

# Comprueba si existe una plantilla y, de ser asi, lo devuelve.
def obtenerPlantillaEntrevistaOficial(id_entrevista_oficial):
    try:
        # Obtiene la plantilla cuyo id es id_entrevista_oficial.
        resultado = models.PlantillaEntrevistaOficial.objects.get(
            pk=id_entrevista_oficial)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addPlantillaEntrevistaOficial(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.PlantillaEntrevistaOficialForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar plantillas de entrevista
            # oficiales.
            return HttpResponseRedirect(
                reverse('listPlantillaEntrevistaOficial',
                kwargs={'orden': 'descripcion'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PlantillaEntrevistaOficialForm()
    return render_to_response(PATH +
        'addPlantillaEntrevistaOficial.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def editPlantillaEntrevistaOficial(request, id_entrevista_oficial):
    # Se obtiene la instancia de la plantilla.
    instancia_plantilla_entrevista_oficial = \
        obtenerPlantillaEntrevistaOficial(id_entrevista_oficial)
    # Si existe se edita.
    if instancia_plantilla_entrevista_oficial:
        # Se carga el formulario para la plantilla existente.
        form = forms.PlantillaEntrevistaOficialForm(
            instance=instancia_plantilla_entrevista_oficial)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.PlantillaEntrevistaOficialForm(
                request.POST,
                instance=instancia_plantilla_entrevista_oficial)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar plantillas de
                # entrevista oficiales.
                return HttpResponseRedirect(
                    reverse('listPlantillaEntrevistaOficial',
                    kwargs={'orden': 'descripcion'}))
    # La plantilla no existe.
    else:
        form = False
    return render_to_response(PATH +
        'editPlantillaEntrevistaOficial.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def delPlantillaEntrevistaOficial(request, id_entrevista_oficial):
    # Se obtiene la instancia del asesor.
    instancia_plantilla_entrevista_oficial = \
        obtenerPlantillaEntrevistaOficial(id_entrevista_oficial)
    # Si existe se elimina.
    if instancia_plantilla_entrevista_oficial:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_plantilla_entrevista_oficial.borrar()
            # Redirige a la pagina de listar plantillas de entrevista
            # oficiales.
            return HttpResponseRedirect(
                reverse('listPlantillaEntrevistaOficial',
                kwargs={'orden': 'descripcion'}))
    # La plantilla no existe.
    else:
        form = True
    return render_to_response(PATH +
        'delPlantillaEntrevistaOficial.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def listPlantillaEntrevistaOficial(request, orden):
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
        'listPlantillaEntrevistaOficial.html',
        {'user': request.user, 'form': form,
        'lista_plantillas_entrevista_oficial':
        lista_plantillas_entrevista_oficial,
        'busqueda': busqueda, 'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaPlantillasEntrevistaOficial(request, busqueda):
    lista_plantillas_entrevista_oficial = \
        models.PlantillaEntrevistaOficial.objects.order_by(
        'descripcion')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_plantillas_entrevista_oficial = \
            lista_plantillas_entrevista_oficial.filter(
            descripcion__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_plantillas_entrevista_oficial,
        'name': 'plantillas de entrevista oficial',})
