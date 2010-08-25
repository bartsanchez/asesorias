from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasPlantillaEntrevistaOficial as \
    vistasPEO
from asesorias.utils import vistasPDF

PATH = 'asesorias/PreguntaOficial/'

# Comprueba si existe una pregunta oficial y, de ser asi, la devuelve.
def obtenerPreguntaOficial(id_entrevista_oficial, id_pregunta_oficial):
    try:
        # Obtiene la pregunta oficial.
        resultado = models.PreguntaOficial.objects.get(
            id_entrevista_oficial=id_entrevista_oficial,
            id_pregunta_oficial=id_pregunta_oficial)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las preguntas de una determinada plantilla
# oficial.
def obtenerPreguntasDePlantillaOficial(
    instancia_entrevista_oficial):
    try:
        # Obtiene todas las preguntas que pertenecen a una plantilla
        # oficial pasado por argumento.
        resultado = models.PreguntaOficial.objects.filter(
            id_entrevista_oficial=\
            instancia_entrevista_oficial.id_entrevista_oficial)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las preguntas de una
# determinada plantilla oficial.
def obtenerListaDeIdsPreguntasDePlantillaOficial(
    instancia_plantilla_entrevista_oficial):
    if instancia_plantilla_entrevista_oficial:
        # Se obtiene una lista con las preguntas de una determinada
        # plantilla oficial.
        lista_preguntas_oficiales = obtenerPreguntasDePlantillaOficial(
            instancia_plantilla_entrevista_oficial)
        # Lista que albergara los ids de las preguntas.
        lista_ids_preguntas_oficiales = []

        # Si existen preguntas en la plantilla oficial extraen sus ids.
        if lista_preguntas_oficiales:
            # Por cada pregunta de la plantilla oficial se extrae su id
            # y se inserta en la nueva lista.
            for pregunta_oficial in lista_preguntas_oficiales:
                lista_ids_preguntas_oficiales.append(
                    pregunta_oficial.id_pregunta_oficial)
            # Ordena la lista con los ids de las preguntas de menor a
            # mayor.
            lista_ids_preguntas_oficiales.sort()
        # Resultado sera una lista de ids, o una lista vacia si la
        # plantilla no tiene preguntas.
        resultado = lista_ids_preguntas_oficiales
    # En el caso de que no exista la plantilla se devuelve False.
    else:
        resultado = False
    return resultado

# Determina el primer id_pregunta_oficial disponible para una
# determinada plantilla oficial.
def determinarSiguienteIdPreguntaDePlantillaOficial(
    instancia_plantilla_entrevista_oficial):
    # Se obtiene una lista ordenada con los ids de las preguntas
    # existentes para la plantilla oficial.
    lista_ids_preguntas_oficiales = \
        obtenerListaDeIdsPreguntasDePlantillaOficial(
        instancia_plantilla_entrevista_oficial)

    # Inicializamos el contador a 1, que es el primer valor valido para
    # un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_pregunta_oficial para la plantilla
        # oficial.
        if lista_ids_preguntas_oficiales.count(contador) > 0:
            contador += 1
        # No existe tal id_pregunta_oficial para la plantilla oficial.
        else:
            break
    return contador

def addPreguntaOficial(request, id_entrevista_oficial):
    # Se comprueba que exista la entrevista, en caso de introducir una.
    if id_entrevista_oficial != '':
        # Se comprueba que exista la entrevista pasada por argumento.
        instancia_entrevista_oficial = \
            vistasPEO.obtenerPlantillaEntrevistaOficial(
                id_entrevista_oficial)

        # La entrevista no existe, se redirige.
        if not instancia_entrevista_oficial:
            return HttpResponseRedirect(
                reverse('selectEntrevistaOficial_PreguntaOficial'))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        enunciado = request.POST['enunciado']

        # Se obtiene una instancia de la plantilla oficial a traves de
        # su id.
        instancia_entrevista_oficial = \
            vistasPEO.obtenerPlantillaEntrevistaOficial(
                id_entrevista_oficial)

        # Se determina el siguiente id_pregunta_oficial para la
        # plantilla de entrevista oficial.
        id_pregunta_oficial = \
            determinarSiguienteIdPreguntaDePlantillaOficial(
            instancia_entrevista_oficial)

        # Datos necesarios para crear la nueva plantilla.
        datos_pregunta_oficial = {
            'id_entrevista_oficial': id_entrevista_oficial,
            'id_pregunta_oficial': id_pregunta_oficial,
            'enunciado': enunciado}

        # Se obtienen los valores y se valida.
        form = forms.PreguntaOficialForm(datos_pregunta_oficial)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar preguntas de plantilla
            # oficiales.
            return HttpResponseRedirect(reverse('listPreguntaOficial',
                kwargs={'entrevista_oficial': id_entrevista_oficial,
                'orden': 'enunciado'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PreguntaOficialForm(
            initial={'id_entrevista_oficial': id_entrevista_oficial})
    return render_to_response(PATH + 'addPreguntaOficial.html',
        {'user': request.user, 'form': form})

def editPreguntaOficial(request, id_entrevista_oficial,
    id_pregunta_oficial):
    # Se obtiene la instancia de la pregunta oficial.
    instancia_pregunta_oficial = \
        obtenerPreguntaOficial(id_entrevista_oficial,
        id_pregunta_oficial)
    # Si existe se edita.
    if instancia_pregunta_oficial:
        # Se carga el formulario para la pregunta existente.
        form = forms.PreguntaOficialForm(
            instance=instancia_pregunta_oficial)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se extraen los valores pasados por el metodo POST.
            enunciado = request.POST['enunciado']

            # Se obtiene una instancia de la plantilla oficial a traves
            # de su id.
            instancia_entrevista_oficial = \
                models.PlantillaEntrevistaOficial.objects.get(
                pk=id_entrevista_oficial)

             # Se determina el siguiente id_pregunta_oficial para la
            # plantilla de entrevista oficial.
            id_pregunta_oficial = \
                determinarSiguienteIdPreguntaDePlantillaOficial(
                instancia_entrevista_oficial)

            # Datos necesarios para crear la nueva plantilla.
            datos_pregunta_oficial = {
                'id_entrevista_oficial': id_entrevista_oficial,
                'id_pregunta_oficial': id_pregunta_oficial,
                'enunciado': enunciado}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.PreguntaOficialForm(datos_pregunta_oficial,
                instance=instancia_pregunta_oficial)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar preguntas oficiales.
                return HttpResponseRedirect(
                    reverse('listPreguntaOficial',
                    kwargs={'entrevista_oficial': id_entrevista_oficial,
                    'orden': 'enunciado'}))
    # La pregunta oficial no existe.
    else:
        form = False
    return render_to_response(PATH + 'editPreguntaOficial.html',
        {'user': request.user, 'form': form})

def delPreguntaOficial(request, id_entrevista_oficial,
    id_pregunta_oficial):
    # Se obtiene la instancia de la pregunta oficial.
    instancia_pregunta_oficial = obtenerPreguntaOficial(
        id_entrevista_oficial, id_pregunta_oficial)
    # Si existe se elimina.
    if instancia_pregunta_oficial:
        instancia_pregunta_oficial.delete()
        # Redirige a la pagina de listar preguntas oficiales.
        return HttpResponseRedirect(reverse('listPreguntaOficial',
            kwargs={'entrevista_oficial': id_entrevista_oficial,
            'orden': 'enunciado'}))
    # La pregunta no existe.
    else:
        error = True
    return render_to_response(PATH + 'delPreguntaOficial.html',
        {'user': request.user, 'error': error})

def selectEntrevistaOficial(request):
    # Se ha introducido una plantilla oficial.
    if request.method == 'POST':

        # Se obtiene la plantilla y se valida.
        form = forms.PlantillaEntrevistaOficialFormSelect(request.POST)

        # Si es valido se redirige a listar las preguntas oficiales.
        if form.is_valid():
            entrevista_oficial = request.POST['entrevista_oficial']

            return HttpResponseRedirect(
                reverse('listPreguntaOficial',
                kwargs={'entrevista_oficial': entrevista_oficial,
                'orden': 'descripcion'}))

        else:
            HttpResponseRedirect(
                reverse('selectEntrevistaOficial_PreguntaOficial'))

    else:
        form = forms.PlantillaEntrevistaOficialFormSelect()

    return render_to_response(PATH + 'selectEntrevistaOficial.html',
        {'user': request.user, 'form': form})

def listPreguntaOficial(request, entrevista_oficial, orden):
    # Se comprueba que exista la entrevista pasada por argumento.
    instancia_entrevista_oficial = \
        vistasPEO.obtenerPlantillaEntrevistaOficial(entrevista_oficial)

    # La plantilla no existe, se redirige.
    if not instancia_entrevista_oficial:
        return HttpResponseRedirect(
            reverse('selectEntrevistaOficial_PreguntaOficial'))

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
        'lista_preguntas_oficiales': lista_preguntas_oficiales,
        'busqueda': busqueda,
        'entrevista_oficial': entrevista_oficial,
        'orden': orden})

def generarPDFListaPreguntasOficiales(request, entrevista_oficial, busqueda):
    # Se comprueba que exista la entrevista pasada por argumento.
    instancia_entrevista_oficial = \
        vistasPEO.obtenerPlantillaEntrevistaOficial(entrevista_oficial)

    # La plantilla no existe, se redirige.
    if not instancia_entrevista_oficial:
        return HttpResponseRedirect(
            reverse('selectEntrevistaOficial_PreguntaOficial'))

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
