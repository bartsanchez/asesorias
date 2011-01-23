from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaOficial as vistasPEO
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaAsesor as vistasPEA
from asesorias.vistas.AdministradorPrincipal import vistasPreguntaAsesor
from asesorias.utils import vistasPDF

PATH = 'asesorias/UsuarioAsesor/'

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def addPlantillaEntrevistaAsesor(request, curso_academico):
    dni_pasaporte = unicode(request.user)

    # Se comprueba que exista el asesor curso academico pasado por
    # argumento.
    instancia_asesor_curso_academico = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # El asesor curso academico no existe, se redirige.
    if not (instancia_asesor_curso_academico):
        return HttpResponseRedirect(
            reverse('listPlantillasAsesor_Asesor',
            kwargs={'curso_academico': curso_academico,
            'orden': 'descripcion'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        descripcion = request.POST['descripcion']

        # Se determina el siguiente id_entrevista_asesor para el asesor
        # curso academico.
        id_entrevista_asesor = vistasPEA.\
            determinarSiguienteIdPlantillaDeAsesorCursoAcademico(
            instancia_asesor_curso_academico)

        # Datos necesarios para crear la nueva plantilla.
        datos_plantilla_entrevista_asesor = {
            'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_entrevista_asesor': id_entrevista_asesor,
            'descripcion': descripcion}

        # Se obtienen los valores y se valida.
        form = forms.PlantillaEntrevistaAsesorForm(
            datos_plantilla_entrevista_asesor)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar plantillas de entrevista de
            # asesor.
            return HttpResponseRedirect(
                reverse('listPlantillasAsesor_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'descripcion'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PlantillaEntrevistaAsesorForm()
    return render_to_response(PATH +'addPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

@login_required
def editPlantillaEntrevistaAsesor(request, curso_academico,
    id_entrevista_asesor):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia de la plantilla de entrevista de asesor.
    instancia_plantilla_entrevista_asesor = vistasPEA.\
        obtenerPlantillaEntrevistaAsesor(
        dni_pasaporte, curso_academico, id_entrevista_asesor)
    # Si existe se edita.
    if instancia_plantilla_entrevista_asesor:
        # Se carga el formulario para la plantilla existente.
        form = forms.PlantillaEntrevistaAsesorForm(
            instance=instancia_plantilla_entrevista_asesor)

        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            descripcion = request.POST['descripcion']

            # Se obtiene una instancia del asesor curso academico a
            # traves de su id.
            instancia_asesor_curso_academico = \
                vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
                dni_pasaporte, curso_academico)

            # Se guarda la anterior id.
            id_entrevista_asesor_antigua = id_entrevista_asesor

            # Se determina el siguiente id_entrevista_asesor para el
            # asesor curso academico.
            id_entrevista_asesor = vistasPEA.\
                determinarSiguienteIdPlantillaDeAsesorCursoAcademico(
                instancia_asesor_curso_academico)

            # Datos necesarios para crear la nueva plantilla.
            datos_plantilla_entrevista_asesor = {
                'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_entrevista_asesor': id_entrevista_asesor,
                'descripcion': descripcion}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.PlantillaEntrevistaAsesorForm(
                datos_plantilla_entrevista_asesor,
                instance=instancia_plantilla_entrevista_asesor)

            # Si es valido se guarda.
            if form.is_valid():
                instancia_plantilla_entrevista_asesor.editar(
                    id_entrevista_asesor_antigua)
                form.save()
                # Redirige a la pagina de listar plantillas de
                # entrevista de asesor.
                return HttpResponseRedirect(
                    reverse('listPlantillasAsesor_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'orden': 'descripcion'}))
    # La plantilla de asesor no existe.
    else:
        form = False
    return render_to_response(PATH +
        'editPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

@login_required
def delPlantillaEntrevistaAsesor(request, curso_academico,
    id_entrevista_asesor):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia de la asignatura curso academico.
    instancia_plantilla_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor)
    # Si existe se elimina.
    if instancia_plantilla_entrevista_asesor:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_plantilla_entrevista_asesor.borrar()
            # Redirige a la pagina de listar plantillas de entrevista de
            # asesor.
            return HttpResponseRedirect(
                reverse('listPlantillasAsesor_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'descripcion'}))
    # La plantilla no existe.
    else:
        form = True
    return render_to_response(PATH +'delPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico})

@login_required
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

@login_required
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

@login_required
def addPreguntaAsesor(request, curso_academico, entrevista_asesor):
    dni_pasaporte = unicode(request.user)

    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(reverse('listPreguntaAsesor_Asesor',
        kwargs={'curso_academico': curso_academico,
        'id_entrevista_asesor': entrevista_asesor,
        'orden': 'enunciado'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        enunciado = request.POST['enunciado']

        # Se determina el siguiente id_pregunta_asesor para la plantilla
        # de entrevista de asesor.
        id_pregunta_asesor = vistasPreguntaAsesor.\
            determinarSiguienteIdPreguntaDePlantillaDeAsesor(
            instancia_entrevista_asesor)

        # Datos necesarios para crear la nueva plantilla.
        datos_pregunta_asesor = {'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_entrevista_asesor': entrevista_asesor,
            'id_pregunta_asesor': id_pregunta_asesor,
            'enunciado': enunciado}

        # Se obtienen los valores y se valida.
        form = forms.PreguntaAsesorForm(datos_pregunta_asesor)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar preguntas de plantilla de
            # asesor.
            return HttpResponseRedirect(
                reverse('listPreguntaAsesor_Asesor',
                kwargs={'curso_academico': curso_academico,
                'id_entrevista_asesor': entrevista_asesor,
                'orden': 'enunciado'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PreguntaAsesorForm()
    return render_to_response(PATH + 'addPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'entrevista_asesor': entrevista_asesor})

@login_required
def editPreguntaAsesor(request, curso_academico, id_entrevista_asesor,
    id_pregunta_asesor):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia de la pregunta de asesor.
    instancia_pregunta_asesor = \
        vistasPreguntaAsesor.obtenerPreguntaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor, id_pregunta_asesor)
    # Si existe se edita.
    if instancia_pregunta_asesor:
        # Se carga el formulario para la pregunta existente.
        form = forms.PreguntaAsesorForm(
            instance=instancia_pregunta_asesor)

        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            enunciado = request.POST['enunciado']

            # Se obtiene una instancia de la plantilla de asesor a
            # traves de su id.
            instancia_entrevista_asesor = \
                vistasPEA.obtenerPlantillaEntrevistaAsesor(
                dni_pasaporte, curso_academico, id_entrevista_asesor)

            # Se determina el siguiente id_pregunta_asesor para la
            # plantilla de entrevista de asesor.
            id_pregunta_asesor = vistasPreguntaAsesor.\
                determinarSiguienteIdPreguntaDePlantillaDeAsesor(
                instancia_entrevista_asesor)

            # Datos necesarios para crear la nueva plantilla.
            datos_pregunta_asesor = {'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_entrevista_asesor': id_entrevista_asesor,
                'id_pregunta_asesor': id_pregunta_asesor,
                'enunciado': enunciado}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.PreguntaAsesorForm(datos_pregunta_asesor,
                instance=instancia_pregunta_asesor)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar preguntas de asesor.
                return HttpResponseRedirect(
                    reverse('listPreguntaAsesor_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'id_entrevista_asesor': id_entrevista_asesor,
                    'orden': 'enunciado'}))
    # La pregunta de asesor no existe.
    else:
        form = False
    return render_to_response(PATH + 'editPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'entrevista_asesor': id_entrevista_asesor})

@login_required
def delPreguntaAsesor(request, curso_academico, id_entrevista_asesor,
    id_pregunta_asesor):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia de la pregunta de asesor.
    instancia_pregunta_asesor = \
        vistasPreguntaAsesor.obtenerPreguntaAsesor(
        dni_pasaporte, curso_academico, id_entrevista_asesor,
        id_pregunta_asesor)
    # Si existe se elimina.
    if instancia_pregunta_asesor:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_pregunta_asesor.borrar()
            # Redirige a la pagina de listar preguntas de asesor.
            return HttpResponseRedirect(reverse(
                'listPreguntaAsesor_Asesor',
                kwargs={'curso_academico': curso_academico,
                'id_entrevista_asesor': id_entrevista_asesor,
                'orden': 'enunciado'}))
    # La pregunta no existe.
    else:
        form = True
    return render_to_response(PATH + 'delPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'entrevista_asesor': id_entrevista_asesor,
        'curso_academico': curso_academico})

@login_required
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
            reverse('listPlantillasAsesor_Asesor',
            kwargs={'curso_academico': curso_academico,
            'orden': 'descripcion'}))

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

@login_required
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
