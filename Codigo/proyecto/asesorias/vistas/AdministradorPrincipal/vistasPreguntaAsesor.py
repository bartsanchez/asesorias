from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaAsesor as vistasPEA
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/PreguntaAsesor/'

# Comprueba si existe una pregunta de asesor y, de ser asi, la devuelve.
def obtenerPreguntaAsesor(dni_pasaporte, curso_academico,
    id_entrevista_asesor, id_pregunta_asesor):
    try:
        # Obtiene la pregunta de asesor.
        resultado = models.PreguntaAsesor.objects.get(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico,
            id_entrevista_asesor=id_entrevista_asesor,
            id_pregunta_asesor=id_pregunta_asesor)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las preguntas de una determinada plantilla de
# asesor.
def obtenerPreguntasDePlantillaDeAsesor(
    instancia_plantilla_entrevista_asesor):
    try:
        # Obtiene todas las preguntas que pertenecen a una plantilla de
        # asesor pasado por argumento.
        resultado = models.PreguntaAsesor.objects.filter(
            dni_pasaporte=
            instancia_plantilla_entrevista_asesor.dni_pasaporte,
            curso_academico=
            instancia_plantilla_entrevista_asesor.curso_academico,
            id_entrevista_asesor=
            instancia_plantilla_entrevista_asesor.id_entrevista_asesor)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las preguntas de una
# determinada plantilla de asesor.
def obtenerListaDeIdsPreguntasDePlantillaDeAsesor(
    instancia_plantilla_entrevista_asesor):
    if instancia_plantilla_entrevista_asesor:
        # Se obtiene una lista con las preguntas de una determinada
        # plantilla de asesor.
        lista_preguntas_de_asesor= obtenerPreguntasDePlantillaDeAsesor(
            instancia_plantilla_entrevista_asesor)
        # Lista que albergara los ids de las preguntas.
        lista_ids_preguntas_de_asesor = []

        # Si existen preguntas en la plantilla de asesor extrae sus ids.
        if lista_preguntas_de_asesor:
            # Por cada pregunta de la plantilla de asesor se extrae su
            # id y se inserta en la nueva lista.
            for pregunta_de_asesor in lista_preguntas_de_asesor:
                lista_ids_preguntas_de_asesor.append(
                    pregunta_de_asesor.id_pregunta_asesor)
            # Ordena la lista con los ids de las preguntas de menor a
            # mayor.
            lista_ids_preguntas_de_asesor.sort()
        # Resultado sera una lista de ids, o una lista vacia si la
        # plantilla no tiene preguntas.
        resultado = lista_ids_preguntas_de_asesor
    # En el caso de que no exista la plantilla se devuelve False.
    else:
        resultado = False
    return resultado

# Determina el primer id_pregunta_asesor disponible para una determinada
# plantilla de asesor.
def determinarSiguienteIdPreguntaDePlantillaDeAsesor(
    instancia_plantilla_entrevista_asesor):
    # Se obtiene una lista ordenada con los ids de las preguntas
    # existentes para la plantilla de asesor.
    lista_ids_preguntas_de_asesor = \
        obtenerListaDeIdsPreguntasDePlantillaDeAsesor(
        instancia_plantilla_entrevista_asesor)

    # Inicializamos el contador a 1, que es el primer valor valido para
    # un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_pregunta_asesor para la plantilla
        # de asesor.
        if lista_ids_preguntas_de_asesor.count(contador) > 0:
            contador += 1
        # No existe tal id_pregunta_asesor para la plantilla de asesor.
        else:
            break
    return contador

@checkAdministradorPrincipal
@login_required
def addPreguntaAsesor(request, dni_pasaporte, curso_academico,
    entrevista_asesor):
    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(reverse('selectPEA_PreguntaAsesor',
        kwargs={'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': 'add'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        enunciado = request.POST['enunciado']

        # Se determina el siguiente id_pregunta_asesor para la plantilla
        # de entrevista de asesor.
        id_pregunta_asesor = \
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
            return HttpResponseRedirect(reverse('listPreguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_entrevista_asesor': entrevista_asesor,
                'orden': 'list'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PreguntaAsesorForm()
    return render_to_response(PATH + 'addPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'entrevista_asesor': entrevista_asesor})

@checkAdministradorPrincipal
@login_required
def editPreguntaAsesor(request, dni_pasaporte, curso_academico,
    id_entrevista_asesor, id_pregunta_asesor):
    # Se obtiene la instancia de la pregunta de asesor.
    instancia_pregunta_asesor = obtenerPreguntaAsesor(dni_pasaporte,
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
            id_pregunta_asesor = \
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
                    reverse('listPreguntaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_entrevista_asesor': id_entrevista_asesor,
                    'orden': 'list'}))
    # La pregunta de asesor no existe.
    else:
        form = False
    return render_to_response(PATH + 'editPreguntaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'entrevista_asesor': id_entrevista_asesor})

@checkAdministradorPrincipal
@login_required
def delPreguntaAsesor(request, dni_pasaporte, curso_academico,
    id_entrevista_asesor, id_pregunta_asesor):
    # Se obtiene la instancia de la pregunta de asesor.
    instancia_pregunta_asesor = obtenerPreguntaAsesor(
        dni_pasaporte, curso_academico, id_entrevista_asesor,
        id_pregunta_asesor)
    # Si existe se elimina.
    if instancia_pregunta_asesor:
        instancia_pregunta_asesor.delete()
        # Redirige a la pagina de listar preguntas de asesor.
        return HttpResponseRedirect(reverse('listPreguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_entrevista_asesor': id_entrevista_asesor,
                'orden': 'list'}))
    # La pregunta no existe.
    else:
        error = True
    return render_to_response(PATH + 'delPreguntaAsesor.html',
        {'user': request.user, 'error': error})

@checkAdministradorPrincipal
@login_required
def selectAsesor(request, tipo):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.AsesorFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            asesor = request.POST['asesor']

            return HttpResponseRedirect(
                reverse('selectAsesorCA_PreguntaAsesor',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_PreguntaAsesor',
                kwargs={'tipo': tipo}))

    else:
        form = forms.AsesorFormSelect()

    return render_to_response(PATH + 'selectAsesor.html',
        {'user': request.user, 'form': form, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectAsesorCursoAcademico(request, dni_pasaporte, tipo):
    # Se obtiene el posible asesor.
    instancia_asesor = vistasAsesor.obtenerAsesor(dni_pasaporte)

    # Se comprueba que exista el asesor.
    if not instancia_asesor:
        return HttpResponseRedirect(
            reverse('selectAsesor_PreguntaAsesor',
            kwargs={'tipo': tipo}))

    # Se ha introducido un asesor curso academico.
    if request.method == 'POST':
        # Se obtiene el alumno curso academico y se valida.
        form = forms.AsesorCursoAcademicoFormSelect(dni_pasaporte,
            request.POST)

        # Si es valido se redirige a listar plantillas.
        if form.is_valid():
            asesor_curso_academico = \
                request.POST['asesor_curso_academico']

            curso_academico = models.AsesorCursoAcademico.objects.get(
                pk=asesor_curso_academico).curso_academico

            return HttpResponseRedirect(
                reverse('selectPEA_PreguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_PreguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'tipo': tipo}))

    else:
        form = forms.AsesorCursoAcademicoFormSelect(
            dni_pasaporte=dni_pasaporte)

    return render_to_response(PATH + 'selectAsesorCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectPlantillaEntrevistaAsesor(request, dni_pasaporte,
    curso_academico, tipo):
    # Se obtiene el posible asesor curso academico.
    instancia_asesor_curso_academico = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesor_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_PreguntaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': tipo}))

    # Se ha introducido una plantilla de entrevista de asesor.
    if request.method == 'POST':
        # Se obtiene la plantilla de entrevista de asesor y se valida.
        form = forms.PlantillaEntrevistaAsesorFormSelect(dni_pasaporte,
            curso_academico, request.POST)

        # Si es valido se redirige a listar preguntas.
        if form.is_valid():
            codigo_entrevista_asesor = \
                request.POST['entrevista_asesor']

            entrevista_asesor = \
                models.PlantillaEntrevistaAsesor.objects.get(
                pk=codigo_entrevista_asesor).id_entrevista_asesor

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addPreguntaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'entrevista_asesor': entrevista_asesor}))

            else:
                return HttpResponseRedirect(
                    reverse('listPreguntaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_entrevista_asesor': entrevista_asesor,
                    'orden': 'descripcion'}))

    else:
        form = forms.PlantillaEntrevistaAsesorFormSelect(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico)

    return render_to_response(PATH +
        'selectPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def listPreguntaAsesor(request, dni_pasaporte, curso_academico,
    id_entrevista_asesor, orden):
    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(reverse('selectPEA_PreguntaAsesor',
        kwargs={'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': 'list'}))

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
        'lista_preguntas_asesor': lista_preguntas_asesor,
        'busqueda': busqueda,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'entrevista_asesor': id_entrevista_asesor,
        'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaPreguntasAsesor(request, dni_pasaporte,
    curso_academico, id_entrevista_asesor, busqueda):
    # Se comprueba que exista la plantilla de entrevista de asesor
    # pasada por argumento.
    instancia_entrevista_asesor = \
        vistasPEA.obtenerPlantillaEntrevistaAsesor(dni_pasaporte,
        curso_academico, id_entrevista_asesor)

    # La plantilla de entrevista de asesor no existe, se redirige.
    if not instancia_entrevista_asesor:
        return HttpResponseRedirect(reverse('selectPEA_PreguntaAsesor',
        kwargs={'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': 'list'}))

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
