from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasCentro
from asesorias.vistas.AdministradorPrincipal import vistasTitulacion
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/Asignatura/'

# Comprueba si existe una asignatura y, de ser asi, la devuelve.
def obtenerAsignatura(nombre_centro, nombre_titulacion, plan_estudios,
    nombre_asignatura):
    try:
        # Obtiene la instancia de titulacion para posteriormente obtener
        # el id.
        instancia_titulacion = vistasTitulacion.obtenerTitulacion(
            nombre_centro, nombre_titulacion, plan_estudios)

        # Obtiene la instancia de la asignatura.
        resultado = models.Asignatura.objects.get(
            id_centro=instancia_titulacion.id_centro_id,
            id_titulacion=instancia_titulacion.id_titulacion,
            nombre_asignatura=nombre_asignatura)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las asignaturas de una determinada titulacion.
def obtenerAsignaturasDeTitulacion(instancia_titulacion):
    try:
        # Obtiene todas las asignaturas que pertenecen a la titulacion
        # pasada por argumento.
        resultado = models.Asignatura.objects.filter(
            id_titulacion=instancia_titulacion.id_titulacion)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las asignaturas de una
# determinada titulacion.
def obtenerListaDeIdsAsignaturasDeTitulacion(instancia_titulacion):
    if instancia_titulacion:
        # Se obtiene una lista con las asignaturas de una determinada
        # titulacion.
        lista_asignaturas_de_titulacion = \
            obtenerAsignaturasDeTitulacion(instancia_titulacion)
        # Lista que albergara los ids de las asignaturas.
        lista_ids_asignaturas= []

        # Si existen asignaturas en la titulacion extraen sus ids.
        if lista_asignaturas_de_titulacion:
            # Por cada titulacion del centro se extrae su id y se
            # inserta en la nueva lista.
            for asignatura in lista_asignaturas_de_titulacion:
                lista_ids_asignaturas.append(asignatura.id_asignatura)
            # Ordena la lista con los ids de las asignaturas de menor
            # a mayor.
            lista_ids_asignaturas.sort()
        # Resultado sera una lista de ids, o una lista vacia si la
        # titulacion no tiene asignaturas.
        resultado = lista_ids_asignaturas
    # En el caso de que no exista la titulacion se devuelve False.
    else:
        resultado = False
    return resultado

# Determina el primer id_asignatura disponible para una determinada
# titulacion.
def determinarSiguienteIdAsignaturaEnTitulacion(instancia_titulacion):
    # Se obtiene una lista ordenada con los ids de las asignaturas
    # existentes en la titulacion.
    lista_ids_asignaturas = obtenerListaDeIdsAsignaturasDeTitulacion(
        instancia_titulacion)

    # Inicializamos el contador a 1, que es el primer valor valido
    # para un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_asignatura en la titulacion.
        if lista_ids_asignaturas.count(contador) > 0:
            contador += 1
        # No existe tal id_asignatura en la titulacion.
        else:
            break
    return contador

@checkAdministradorPrincipal
@login_required
def addAsignatura(request, nombre_centro, nombre_titulacion,
    plan_estudios):
    # Se obtiene la posible titulacion.
    instancia_titulacion = vistasTitulacion.obtenerTitulacion(
        nombre_centro, nombre_titulacion, plan_estudios)

    # Se comprueba que exista la titulacion.
    if not instancia_titulacion:
        return HttpResponseRedirect(reverse('selectCentro_Asignatura',
            kwargs={'tipo': 'add'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        codigo_titulacion = vistasTitulacion.obtenerTitulacion(
            nombre_centro, nombre_titulacion,
            plan_estudios).codigo_titulacion

        nombre_asignatura= request.POST['nombre_asignatura']
        curso = request.POST['curso']
        tipo = request.POST['tipo']
        n_creditos_teoricos = request.POST['nCreditosTeoricos']
        n_creditos_practicos= request.POST['nCreditosPracticos']

        # Se obtiene una instancia de la titulacion a traves de su id.
        instancia_titulacion = models.Titulacion.objects.get(
            pk=codigo_titulacion)

        # Se determina el id_centro e id_titulacion para esa titulacion.
        id_centro = instancia_titulacion.id_centro_id
        id_titulacion = instancia_titulacion.id_titulacion

        # Se determina el siguiente id_asignatura para la titulacion.
        id_asignatura = determinarSiguienteIdAsignaturaEnTitulacion(
            instancia_titulacion)

        # Datos necesarios para crear la nueva asignatura
        datos_asignatura = {'id_centro': id_centro,
            'id_titulacion': id_titulacion,
            'id_asignatura': id_asignatura,
            'nombre_asignatura': nombre_asignatura,
            'curso': curso, 'tipo': tipo,
            'nCreditosTeoricos': n_creditos_teoricos,
            'nCreditosPracticos': n_creditos_practicos,
            'titulacion': codigo_titulacion}

        # Se obtienen los valores y se valida.
        form = forms.AsignaturaForm(datos_asignatura)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Redirige a la pagina de listar asignaturas.
            return HttpResponseRedirect(reverse('listAsignatura',
                kwargs={'nombre_centro':
                instancia_titulacion.determinarNombreCentro(),
                'nombre_titulacion':
                instancia_titulacion.nombre_titulacion,
                'plan_estudios': instancia_titulacion.plan_estudios,
                'orden': 'nombre_centro'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AsignaturaForm()
    return render_to_response(PATH + 'addAsignatura.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios})

@checkAdministradorPrincipal
@login_required
def editAsignatura(request, nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura):
    # Se obtiene la instancia de la asignatura.
    instancia_asignatura= obtenerAsignatura(nombre_centro,
        nombre_titulacion, plan_estudios, nombre_asignatura)
    # Si existe se edita.
    if instancia_asignatura:
        # Se guarda el anterior id_asignatura.
        id_asignatura_antiguo = instancia_asignatura.id_asignatura

        # Se carga el formulario para la asignatura existente.
        form = forms.AsignaturaForm(instance=instancia_asignatura,
            initial={'titulacion': vistasTitulacion.obtenerTitulacion(
                nombre_centro, nombre_titulacion,
                plan_estudios).codigo_titulacion})
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            codigo_titulacion = vistasTitulacion.obtenerTitulacion(
                nombre_centro, nombre_titulacion,
                plan_estudios).codigo_titulacion

            nombre_asignatura= request.POST['nombre_asignatura']
            curso = request.POST['curso']
            tipo = request.POST['tipo']
            n_creditos_teoricos = request.POST['nCreditosTeoricos']
            n_creditos_practicos= request.POST['nCreditosPracticos']

            # Se crea una instancia de la titulacion.
            instancia_titulacion = models.Titulacion.objects.get(
                pk=codigo_titulacion)

            # Se determina el id_centro e id_titulacion para esa
            # titulacion.
            id_centro = instancia_titulacion.id_centro_id
            id_titulacion = instancia_titulacion.id_titulacion

            # Se determina el siguiente id_titulacion para el centro.
            id_asignatura = determinarSiguienteIdAsignaturaEnTitulacion(
                instancia_titulacion)

            # Datos necesarios para crear la nueva asignatura
            datos_asignatura = {'id_centro': id_centro,
                'id_titulacion': id_titulacion,
                'id_asignatura': id_asignatura,
                'nombre_asignatura': nombre_asignatura,
                'curso': curso, 'tipo': tipo,
                'nCreditosTeoricos': n_creditos_teoricos,
                'nCreditosPracticos': n_creditos_practicos,
                'titulacion': codigo_titulacion}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.AsignaturaForm(datos_asignatura,
                instance=instancia_asignatura)

            # Si es valido se guarda.
            if form.is_valid():
                instancia_asignatura.editar(id_asignatura_antiguo)
                form.save()
                # Redirige a la pagina de listar asignaturas.
                return HttpResponseRedirect(reverse('listAsignatura',
                    kwargs={'nombre_centro':
                    instancia_titulacion.determinarNombreCentro(),
                    'nombre_titulacion':
                    instancia_titulacion.nombre_titulacion,
                    'plan_estudios': instancia_titulacion.plan_estudios,
                    'orden': 'nombre_centro'}))
    # La asignatura no existe
    else:
        form = False
    return render_to_response(PATH + 'editAsignatura.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios})

@checkAdministradorPrincipal
@login_required
def delAsignatura(request, nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura):
    # Se obtiene la instancia de la asignatura.
    instancia_asignatura= obtenerAsignatura(nombre_centro,
        nombre_titulacion, plan_estudios, nombre_asignatura)
    # Si existe se elimina.
    if instancia_asignatura:
        # Se carga el formulacion de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_asignatura.borrar()
            # Redirige a la pagina de listar asignaturas.
            return HttpResponseRedirect(reverse('listAsignatura',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'orden': 'nombre_centro'}))
    # La asignatura no existe.
    else:
        form = True
    return render_to_response(PATH + 'delAsignatura.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def selectCentro(request, tipo):
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

            return HttpResponseRedirect(
                reverse('selectTitulacion_Asignatura',
                kwargs={'nombre_centro': instancia_centro.nombre_centro,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectCentro_Asignatura',
                kwargs={'tipo': tipo}))

    else:
        form = forms.CentroFormSelect()

    return render_to_response(PATH + 'selectCentro.html',
        {'user': request.user, 'form': form, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectTitulacion(request, nombre_centro, tipo):
    # Se obtiene el posible centro.
    instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

    # Se comprueba que exista el centro.
    if not instancia_centro:
        return HttpResponseRedirect(
            reverse('selectCentro_Asignatura',
            kwargs={'tipo': tipo}))
    else:
        id_centro = instancia_centro.id_centro

    # Se ha introducido una titulacion.
    if request.method == 'POST':

        # Se obtiene la titulacion y se valida.
        form = forms.TitulacionFormSelect(id_centro, request.POST)

        # Si es valido se redirige a listar asignaturas.
        if form.is_valid():
            titulacion = request.POST['titulacion']

            # Se crea una instancia de la titulacion para pasar los
            # argumentos.
            instancia_titulacion = models.Titulacion.objects.get(
                pk=titulacion)

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addAsignatura',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion':
                    instancia_titulacion.nombre_titulacion,
                    'plan_estudios':
                    instancia_titulacion.plan_estudios}))
            else:
                return HttpResponseRedirect(reverse('listAsignatura',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion':
                    instancia_titulacion.nombre_titulacion,
                    'plan_estudios': instancia_titulacion.plan_estudios,
                    'orden': 'nombre_asignatura'}))

        else:
            return HttpResponseRedirect(
                reverse('selectTitulacion_Asignatura',
                kwargs={'nombre_centro': nombre_centro,
                'tipo': tipo}))

    else:
        form = forms.TitulacionFormSelect(id_centro=id_centro)

    return render_to_response(PATH + 'selectTitulacion.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def listAsignatura(request, nombre_centro, nombre_titulacion,
    plan_estudios, orden):
    # Se obtiene la posible titulacion.
    instancia_titulacion = vistasTitulacion.obtenerTitulacion(
        nombre_centro, nombre_titulacion, plan_estudios)

    # Se comprueba que exista la titulacion.
    if not instancia_titulacion:
        return HttpResponseRedirect(reverse('selectCentro_Asignatura',
            kwargs={'tipo': 'list'}))
    else:
        id_centro = instancia_titulacion.id_centro_id
        id_titulacion = instancia_titulacion.id_titulacion

    # Se obtiene una lista con todas las asignaturas.
    lista_asignaturas = models.Asignatura.objects.filter(
        id_centro=id_centro,
        id_titulacion=id_titulacion).order_by('nombre_asignatura')

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
            for asignatura in lista_asignaturas:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(asignatura.nombre_asignatura)

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(asignatura)

            # La lista final a devolver sera la lista auxiliar.
            lista_asignaturas = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        # Si el orden es descendente se invierte la lista.
        if (orden == '_nombre_asignatura'):
            lista_asignaturas = reversed(lista_asignaturas)

    return render_to_response(PATH + 'listAsignatura.html',
        {'user': request.user, 'form': form,
        'lista_asignaturas': lista_asignaturas,
        'busqueda': busqueda, 'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios, 'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaAsignaturas(request, nombre_centro,
    nombre_titulacion, plan_estudios, busqueda):
    # Se obtiene la posible titulacion.
    instancia_titulacion = vistasTitulacion.obtenerTitulacion(
        nombre_centro, nombre_titulacion, plan_estudios)

    # Se comprueba que exista la titulacion.
    if not instancia_titulacion:
        return HttpResponseRedirect(
            reverse('selectCentro_Asignatura'))
    else:
        id_centro = instancia_titulacion.id_centro_id
        id_titulacion = instancia_titulacion.id_titulacion

    # Se obtiene una lista con todas las asignaturas.
    lista_asignaturas = models.Asignatura.objects.filter(
        id_centro=id_centro,
        id_titulacion=id_titulacion).order_by('nombre_asignatura')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
        # la busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con la
        # busqueda.
        for asignatura in lista_asignaturas:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = unicode(asignatura.nombre_asignatura)

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(asignatura)

        # La lista final a devolver sera la lista auxiliar.
        lista_asignaturas = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_asignaturas, 'name': 'asignaturas',})
