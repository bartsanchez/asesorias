from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaOficial as vistasPEO
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaAsesor as vistasPEA
from asesorias.utils import vistasPDF

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

def generarPDFListaPlantillasEntrevistaOficial(request, curso_academico,
    busqueda):
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

def listPreguntaOficial(request, curso_academico, entrevista_oficial,
    orden):
    # Se comprueba que exista la entrevista pasada por argumento.
    instancia_entrevista_oficial = \
        vistasPEO.obtenerPlantillaEntrevistaOficial(entrevista_oficial)

    # La plantilla no existe, se redirige.
    if not instancia_entrevista_oficial:
        return HttpResponseRedirect(
            reverse('listPlantillasOficiales_Asesor',
            kwargs={'curso_academico': curso_academico,
            'orden': 'descripcion'}))

    # Se obtiene una lista con todos las preguntas oficiales de la
    # plantilla pasada por argumento.
    lista_preguntas_oficiales = models.PreguntaOficial.objects.filter(
        id_entrevista_oficial=entrevista_oficial).order_by(
        'enunciado')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']

            # Se crea una lista auxiliar que albergara el resultado de
            # la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden con
            # la busqueda.
            for pregunta_oficial in lista_preguntas_oficiales:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(pregunta_oficial.enunciado)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(pregunta_oficial)

            # La lista final a devolver sera la lista auxiliar.
            lista_preguntas_oficiales = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

    if (orden == '_enunciado'):
        lista_preguntas_oficiales = reversed(lista_preguntas_oficiales)

    return render_to_response(PATH + 'listPreguntaOficial.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'lista_preguntas_oficiales': lista_preguntas_oficiales,
        'busqueda': busqueda,
        'entrevista_oficial': entrevista_oficial,
        'orden': orden})

def generarPDFListaPreguntasOficiales(request, curso_academico,
    entrevista_oficial, busqueda):
    # Se comprueba que exista la entrevista pasada por argumento.
    instancia_entrevista_oficial = \
        vistasPEO.obtenerPlantillaEntrevistaOficial(entrevista_oficial)

    # La plantilla no existe, se redirige.
    if not instancia_entrevista_oficial:
        return HttpResponseRedirect(
            reverse('listPreguntaOficial_Asesor',
            kwargs={'curso_academico': curso_academico,
            'entrevista_oficial': entrevista_oficial,
            'orden': enunciado}))

    # Se obtiene una lista con todos las preguntas oficiales de la
    # plantilla pasada por argumento.
    lista_preguntas_oficiales = models.PreguntaOficial.objects.filter(
        id_entrevista_oficial=entrevista_oficial).order_by(
        'enunciado')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
        # la busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con
        # la busqueda.
        for pregunta_oficial in lista_preguntas_oficiales:
            # Se crea una cadena auxiliar para examinar si se
            # encuentra el resultado de la busqueda.
            cadena = unicode(pregunta_oficial.enunciado)

            # Si se encuentra la busqueda el elemento se incluye en
            # la lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(pregunta_oficial)

        # La lista final a devolver sera la lista auxiliar.
        lista_preguntas_oficiales = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_preguntas_oficiales,
        'name': 'preguntas oficiales',})

def listPlantillasAsesor(request, curso_academico, orden):
    dni_pasaporte = unicode(request.user)

    # Se obtiene una lista con todos las plantillas de entrevista de
    # asesor.
    lista_plantillas_entrevista_asesor = \
        models.PlantillaEntrevistaAsesor.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico).order_by('descripcion')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']

            # Se crea una lista auxiliar que albergara el resultado de
            # la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden con
            # la busqueda.
            for plantilla in lista_plantillas_entrevista_asesor:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(plantilla.descripcion)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(plantilla)

            # La lista final a devolver sera la lista auxiliar.
            lista_plantillas_entrevista_asesor = lista_aux

        else:
            busqueda = False
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_descripcion':
            lista_plantillas_entrevista_asesor = \
                lista_plantillas_entrevista_asesor.reverse()

    return render_to_response(PATH +
        'listPlantillasAsesor.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'lista_plantillas_entrevista_asesor':
        lista_plantillas_entrevista_asesor,
        'busqueda': busqueda,
        'orden': orden})

def generarPDFListaPlantillasEntrevistaAsesor(request,
    curso_academico,busqueda):
    dni_pasaporte = unicode(request.user)

    # Se obtiene una lista con todos las plantillas de entrevista de
    # asesor.
    lista_plantillas_entrevista_asesor = \
        models.PlantillaEntrevistaAsesor.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico).order_by('descripcion')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_plantillas_entrevista_asesor = \
            lista_plantillas_entrevista_asesor.filter(
            descripcion__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_plantillas_entrevista_asesor,
        'name': 'plantillas de entrevista de asesor',})

def listPreguntaAsesor(request, curso_academico, id_entrevista_asesor,
    orden):
    dni_pasaporte = unicode(request.user)

    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(
            reverse('listPlantillasOficiales_Asesor',
            kwargs={'curso_academico': curso_academico,
            'tipo': 'descripcion'}))

    # Se obtiene una lista con todas las preguntas de asesor.
    lista_preguntas_asesor = models.PreguntaAsesor.objects.filter(
        dni_pasaporte=dni_pasaporte, curso_academico=curso_academico,
        id_entrevista_asesor=id_entrevista_asesor).order_by('enunciado')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']

            # Se crea una lista auxiliar que albergara el resultado de
            # la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden con
            # la busqueda.
            for pregunta in lista_preguntas_asesor:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(pregunta.enunciado)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(pregunta)

            # La lista final a devolver sera la lista auxiliar.
            lista_preguntas_asesor = lista_aux

        else:
            busqueda = False
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_enunciado':
            lista_preguntas_asesor = lista_preguntas_asesor.reverse()

    return render_to_response(PATH + 'listPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'lista_preguntas_asesor': lista_preguntas_asesor,
        'busqueda': busqueda,
        'entrevista_asesor': id_entrevista_asesor,
        'orden': orden})

def generarPDFListaPreguntasAsesor(request, curso_academico,
    id_entrevista_asesor, busqueda):
    dni_pasaporte = unicode(request.user)

    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(reverse('listPreguntaAsesor_Asesor',
            kwargs={'curso_academico': curso_academico,
            'entrevista_oficial': entrevista_oficial,
            'orden': enunciado}))

    # Se obtiene una lista con todas las preguntas de asesor.
    lista_preguntas_asesor = models.PreguntaAsesor.objects.filter(
        dni_pasaporte=dni_pasaporte, curso_academico=curso_academico,
        id_entrevista_asesor=id_entrevista_asesor).order_by('enunciado')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_preguntas_asesor = lista_preguntas_asesor.filter(
            enunciado__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_preguntas_asesor,
        'name': 'preguntas de asesor',})
