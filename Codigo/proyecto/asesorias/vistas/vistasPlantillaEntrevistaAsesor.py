from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsesor, vistasAsesorCursoAcademico
from asesorias.utils import vistasPDF

PATH = 'asesorias/PlantillaEntrevistaAsesor/'

# Comprueba si existe una plantilla de entrevista de asesor y, de ser
# asi, la devuelve.
def obtenerPlantillaEntrevistaAsesor(dni_pasaporte, curso_academico,
    id_entrevista_asesor):
    try:
        # Obtiene la plantilla de entrevista de asesor.
        resultado = models.PlantillaEntrevistaAsesor.objects.get(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico,
            id_entrevista_asesor=id_entrevista_asesor)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las plantillas de un determinado asesor curso
# academico.
def obtenerPlantillasDeAsesorCursoAcademico(
    instancia_asesor_curso_academico):
    try:
        # Obtiene todas las plantillas que pertenecen a un asesor pasado
        # por argumento.
        resultado = models.PlantillaEntrevistaAsesor.objects.filter(
            dni_pasaporte=
            instancia_asesor_curso_academico.dni_pasaporte_id,
            curso_academico=
            instancia_asesor_curso_academico.curso_academico)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las plantillas de un
# determinado asesor curso academico.
def obtenerListaDeIdsPlantillasDeAsesorCursoAcademico(
    instancia_asesor_curso_academico):
    if instancia_asesor_curso_academico:
        # Se obtiene una lista con las plantillas de un determinado
        # asesor curso academico.
        lista_plantillas_de_asesor= \
            obtenerPlantillasDeAsesorCursoAcademico(
            instancia_asesor_curso_academico)
        # Lista que albergara los ids de las asignaturas.
        lista_ids_plantillas_de_asesor = []

        # Si existen plantillas de asesor curso academico extraen sus
        # ids.
        if lista_plantillas_de_asesor:
            # Por cada plantilla de asesor curso academico se extrae su
            # id y se inserta en la nueva lista.
            for plantilla_de_asesor in lista_plantillas_de_asesor:
                lista_ids_plantillas_de_asesor.append(
                    plantilla_de_asesor.id_entrevista_asesor)
            # Ordena la lista con los ids de las plantillas de menor a
            # mayor.
            lista_ids_plantillas_de_asesor.sort()
        # Resultado sera una lista de ids, o una lista vacia si el
        # asesor curso academico no tiene plantillas.
        resultado = lista_ids_plantillas_de_asesor
    # En el caso de que no exista el asesor curso academico se devuelve
    # False.
    else:
        resultado = False
    return resultado

# Determina el primer id_entrevista_asesor disponible para un
# determinado asesor curso academico.
def determinarSiguienteIdPlantillaDeAsesorCursoAcademico(
    instancia_asesor_curso_academico):
    # Se obtiene una lista ordenada con los ids de las plantillas
    # existentes para el asesor curso academico.
    lista_ids_plantillas_de_asesor = \
        obtenerListaDeIdsPlantillasDeAsesorCursoAcademico(
        instancia_asesor_curso_academico)

    # Inicializamos el contador a 1, que es el primer valor valido para
    # un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_entrevista_asesor para el asesor
        # curso academico.
        if lista_ids_plantillas_de_asesor.count(contador) > 0:
            contador += 1
        # No existe tal id_entrevista_asesor para el asesor curso
        # academico.
        else:
            break
    return contador

def addPlantillaEntrevistaAsesor(request, dni_pasaporte,
    curso_academico):
    # Se comprueba que exista el asesor curso academico pasado por
    # argumento.
    instancia_asesor_curso_academico = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # El asesor curso academico no existe, se redirige.
    if not (instancia_asesor_curso_academico):
        return HttpResponseRedirect(
            reverse('selectAsesorCA_PlantillaEntrevistaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': 'add'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        descripcion = request.POST['descripcion']

        # Se determina el siguiente id_entrevista_asesor para el asesor
        # curso academico.
        id_entrevista_asesor = \
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
                reverse('listPlantillaEntrevistaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'orden': 'descripcion'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.PlantillaEntrevistaAsesorForm()
    return render_to_response(PATH +'addPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

def editPlantillaEntrevistaAsesor(request, dni_pasaporte,
    curso_academico, id_entrevista_asesor):
    # Se obtiene la instancia de la plantilla de entrevista de asesor.
    instancia_plantilla_entrevista_asesor = \
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

            # Se determina el siguiente id_entrevista_asesor para el
            # asesor curso academico.
            id_entrevista_asesor = \
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
                form.save()
                # Redirige a la pagina de listar plantillas de
                # entrevista de asesor.
                return HttpResponseRedirect(
                    reverse('listPlantillaEntrevistaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'orden': 'descripcion'}))
    # La plantilla de asesor no existe.
    else:
        form = False
    return render_to_response(PATH +
        'editPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

def delPlantillaEntrevistaAsesor(request, dni_pasaporte,
    curso_academico, id_entrevista_asesor):
    # Se obtiene la instancia de la asignatura curso academico.
    instancia_plantilla_entrevista_asesor = \
        obtenerPlantillaEntrevistaAsesor(dni_pasaporte, curso_academico,
        id_entrevista_asesor)
    # Si existe se elimina.
    if instancia_plantilla_entrevista_asesor:
        instancia_plantilla_entrevista_asesor.delete()
        # Redirige a la pagina de listar plantillas de entrevista de
        # asesor.
        return HttpResponseRedirect(
            reverse('listPlantillaEntrevistaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'orden': 'descripcion'}))
    # La plantilla no existe.
    else:
        error = True
    return render_to_response(PATH +'delPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'error': error})

def selectAsesor(request, tipo):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.AsesorFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            asesor = request.POST['asesor']

            return HttpResponseRedirect(
                reverse('selectAsesorCA_PlantillaEntrevistaAsesor',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_PlantillaEntrevistaAsesor',
                kwargs={'tipo': tipo}))

    else:
        form = forms.AsesorFormSelect()

    return render_to_response(PATH + 'selectAsesor.html',
        {'user': request.user, 'form': form, 'tipo': tipo})

def selectAsesorCursoAcademico(request, dni_pasaporte, tipo):
    # Se obtiene el posible asesor.
    instancia_asesor = vistasAsesor.obtenerAsesor(dni_pasaporte)

    # Se comprueba que exista el asesor.
    if not instancia_asesor:
        return HttpResponseRedirect(
            reverse('selectAsesor_PlantillaEntrevistaAsesor',
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

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addPlantillaEntrevistaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico}))

            else:
                return HttpResponseRedirect(
                    reverse('listPlantillaEntrevistaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'orden': 'descripcion'}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_PlantillaEntrevistaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'tipo': tipo}))

    else:
        form = forms.AsesorCursoAcademicoFormSelect(
            dni_pasaporte=dni_pasaporte)

    return render_to_response(PATH + 'selectAsesorCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte, 'tipo': tipo})

def listPlantillaEntrevistaAsesor(request, dni_pasaporte,
    curso_academico, orden):
    # Se obtiene el posible asesor curso academico.
    instancia_asesor_curso_academico = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesor_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_PlantillaEntrevistaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': 'list'}))

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
        'listPlantillaEntrevistaAsesor.html',
        {'user': request.user, 'form': form,
        'lista_plantillas_entrevista_asesor':
        lista_plantillas_entrevista_asesor,
        'busqueda': busqueda,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'orden': orden})

def generarPDFListaPlantillasEntrevistaAsesor(request, dni_pasaporte,
    curso_academico,busqueda):
    # Se obtiene el posible asesor curso academico.
    instancia_asesor_curso_academico = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesor_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_PlantillaEntrevistaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': 'list'}))

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
