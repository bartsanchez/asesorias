from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasCentro
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/Titulacion/'

# Comprueba si existe una titulacion y, de ser asi, la devuelve.
def obtenerTitulacion(nombre_centro, nombre_titulacion, plan_estudios):
    try:
        # Obtiene la instancia de centro para posteriormente obtener
        # el id.
        instancia_centro = vistasCentro.obtenerCentro(nombre_centro)
        # Obtiene la titulacion cuyo centro es centro y el nombre de la
        #titulacion es nombre_titulacion.
        resultado = models.Titulacion.objects.get(
            id_centro=instancia_centro.id_centro,
            nombre_titulacion=nombre_titulacion,
            plan_estudios=plan_estudios)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las titulaciones de un determinado centro.
def obtenerTitulacionesDeCentro(centro):
    try:
        instancia_centro = vistasCentro.obtenerCentro(centro)
        # Obtiene todas las titulaciones que pertenece al centro pasado
        # por argumento.
        resultado = models.Titulacion.objects.filter(
            id_centro=instancia_centro.id_centro)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las titulaciones de un
# determinado centro.
def obtenerListaDeIdsTitulacionesDeCentro(centro):
    # Se comprueba si existe el centro.
    existe_centro = vistasCentro.obtenerCentro(centro)

    if existe_centro:
        # Se obtiene una lista con las titulaciones de un determinado
        # centro.
        lista_titulaciones_de_centro = \
            obtenerTitulacionesDeCentro(centro)
        # Lista que albergara los ids de los centros.
        lista_ids_titulaciones = []

        # Si existen titulaciones en el centro se extraen sus ids.
        if lista_titulaciones_de_centro:
            # Por cada titulacion del centro se extrae su id y se
            # inserta en la nueva lista.
            for titulacion in lista_titulaciones_de_centro:
                lista_ids_titulaciones.append(titulacion.id_titulacion)
            # Ordena la lista con los ids de las titulaciones de menor
            # a mayor.
            lista_ids_titulaciones.sort()
        # Resultado sera una lista de ids, o una lista vacia si el
        # centro no tiene titulaciones
        resultado = lista_ids_titulaciones
    # En el caso de que no exista el centro se devuelve False.
    else:
        resultado = False
    return resultado

# Determina el primer id_titulacion disponible para un determinado
# centro.
def determinarSiguienteIdTitulacionEnCentro(instancia_centro):
    # Se obtiene una lista ordenada con los ids de las titulaciones
    # existentes en el centro.
    lista_ids_titulaciones= obtenerListaDeIdsTitulacionesDeCentro(
        instancia_centro.nombre_centro)

    # Inicializamos el contador a 1, que es el primer valor valido para
    # un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_titulacion en el centro.
        if lista_ids_titulaciones.count(contador) > 0:
            contador += 1
        # No existe tal id_titulacion en el centro.
        else:
            break
    return contador

@checkAdministradorPrincipal
@login_required
def addTitulacion(request, nombre_centro):
    # Se comprueba que exista el centro en caso de introducir uno.
    if nombre_centro != '':
        # Se comprueba que exista el centro pasado por argumento.
        instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

        # El centro no existe, se redirige.
        if not (instancia_centro):
            return HttpResponseRedirect(
                reverse('selectCentro_Titulacion'))

        id_centro = instancia_centro.id_centro
    # No se ha introducido un centro para la titulacion.
    else:
        id_centro = ''

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        id_centro = request.POST['id_centro']
        nombre_titulacion = request.POST['nombre_titulacion']
        plan_estudios = request.POST['plan_estudios']

        # Se obtiene una instancia del centro a traves de su id.
        instancia_centro = models.Centro.objects.get(pk=id_centro)

        # Se determina el siguiente id_titulacion para el centro.
        id_titulacion = determinarSiguienteIdTitulacionEnCentro(
            instancia_centro)

        # Datos necesarios para crear la nueva titulacion
        datos_titulacion = {'id_centro': id_centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'id_titulacion': id_titulacion}

        # Se obtienen los valores y se valida.
        form = forms.TitulacionForm(datos_titulacion)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Redirige a la pagina de listar titulaciones.
            return HttpResponseRedirect(reverse('listTitulacion',
                kwargs={'nombre_centro': instancia_centro.nombre_centro,
                'orden': 'nombre_titulacion' }) )
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.TitulacionForm(initial={'id_centro': id_centro})
    return render_to_response(PATH + 'addTitulacion.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def editTitulacion(request, nombre_centro, nombre_titulacion,
    plan_estudios):
    # Se obtiene la instancia de la titulacion.
    instancia_titulacion = obtenerTitulacion(nombre_centro,
        nombre_titulacion, plan_estudios)
    # Si existe se edita.
    if instancia_titulacion:
        # Se guarda el anterior id_centro e id_titulacion.
        id_centro_antigua = instancia_titulacion.id_centro_id
        id_titulacion_antigua = instancia_titulacion.id_titulacion

        # Se carga el formulario para la titulacion existente.
        form = forms.TitulacionForm(instance=instancia_titulacion)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se obtienen el resto de valores necesarios a traves
            # de POST.
            id_centro = request.POST['id_centro']
            nombre_titulacion = request.POST['nombre_titulacion']
            plan_estudios = request.POST['plan_estudios']

            # Obtenemos una instancia del centro
            instancia_centro = models.Centro.objects.get(pk=id_centro)

            # Se determina el siguiente id_titulacion para el centro.
            id_titulacion = determinarSiguienteIdTitulacionEnCentro(
                instancia_centro)

            # Datos necesarios para crear la nueva titulacion
            datos_titulacion = {'id_centro': id_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'id_titulacion': id_titulacion}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.TitulacionForm(datos_titulacion,
                instance=instancia_titulacion)

            # Si es valido se guarda.
            if form.is_valid():
                instancia_titulacion.editar(id_centro_antigua,
                    id_titulacion_antigua)
                form.save()

                # Redirige a la pagina de listar titulaciones.
                return HttpResponseRedirect(reverse('listTitulacion',
                    kwargs={'nombre_centro':
                    instancia_centro.nombre_centro,
                    'orden': 'nombre_centro'}))
    # La titulacion no existe
    else:
        form = False
    return render_to_response(PATH + 'editTitulacion.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def delTitulacion(request, nombre_centro, nombre_titulacion,
    plan_estudios):
    # Se obtiene la instancia de la titulacion.
    instancia_titulacion= obtenerTitulacion(nombre_centro,
        nombre_titulacion, plan_estudios)
    # Si existe se elimina.
    if instancia_titulacion:
        instancia_titulacion.borrar()
        # Redirige a la pagina de listar titulaciones.
        return HttpResponseRedirect(reverse('listTitulacion',
            kwargs={'nombre_centro': nombre_centro,
            'orden': 'nombre_centro'}))
    # La titulacion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delTitulacion.html',
        {'user': request.user, 'error': error})

@checkAdministradorPrincipal
@login_required
def selectCentro(request):
    # Se ha introducido un centro.
    if request.method == 'POST':

        # Se obtiene el centro y se valida.
        form = forms.CentroFormSelect(request.POST)

        # Si es valido se redirige a listar centros.
        if form.is_valid():
            centro = request.POST['centro']

            # Se crea una instancia del centro para pasar el nombre de
            # centro por argumento.
            instancia_centro = models.Centro.objects.get(pk=centro)

            return HttpResponseRedirect(reverse('listTitulacion',
                kwargs={'nombre_centro': instancia_centro.nombre_centro,
                'orden': 'nombre_titulacion'}))

        else:
            HttpResponseRedirect(reverse('selectCentro_Titulacion'))

    else:
        form = forms.CentroFormSelect()

    return render_to_response(PATH + 'selectCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def listTitulacion(request, nombre_centro, orden):
    # Se comprueba que exista el centro pasado por argumento.
    instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

    # El centro no existe, se redirige.
    if not (instancia_centro):
        return HttpResponseRedirect(reverse('selectCentro_Titulacion'))

    # Se establece el ordenamiento inicial.
    if (orden == 'plan_estudios') or (orden == '_plan_estudios'):
        orden_inicial = 'plan_estudios'
        orden_secundario = 'nombre_titulacion'
    else:
        orden_inicial = 'nombre_titulacion'
        orden_secundario = 'plan_estudios'

    # Se obtiene una lista con todos las titulaciones.
    lista_titulaciones = models.Titulacion.objects.filter(
        id_centro=instancia_centro.id_centro).order_by(
        orden_inicial, orden_secundario)

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
            for titulacion in lista_titulaciones:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (unicode(titulacion.nombre_titulacion) +
                    unicode(titulacion.plan_estudios))

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(titulacion)

            # La lista final a devolver sera la lista auxiliar.
            lista_titulaciones = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if ((orden == '_nombre_titulacion') or
            (orden == '_plan_estudios')):
            lista_titulaciones = reversed(lista_titulaciones)

    return render_to_response(PATH + 'listTitulacion.html',
        {'user': request.user, 'form': form,
        'lista_titulaciones': lista_titulaciones,
        'busqueda': busqueda, 'centro': nombre_centro, 'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaTitulaciones(request, nombre_centro, busqueda):
    # Se comprueba que exista el centro pasado por argumento.
    instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

    # El centro no existe, se redirige.
    if not (instancia_centro):
        return HttpResponseRedirect(reverse('selectCentro_Titulacion'))

    # Se obtiene una lista con todos las titulaciones.
    lista_titulaciones = models.Titulacion.objects.filter(
        id_centro=instancia_centro.id_centro).order_by(
        'nombre_titulacion', 'plan_estudios')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
        # la busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con
        # la busqueda.
        for titulacion in lista_titulaciones:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = (unicode(titulacion.nombre_titulacion) +
                unicode(titulacion.plan_estudios))

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(titulacion)

        # La lista final a devolver sera la lista auxiliar.
        lista_titulaciones = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_titulaciones, 'name': 'titulaciones',})
