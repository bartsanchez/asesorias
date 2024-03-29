from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasCentro
from asesorias.vistas.AdministradorPrincipal import \
    vistasAdministradorCentro
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/Centro_AdministradorCentro/'

# Comprueba si existe un centro_administradorCentro y, de ser asi,
# lo devuelve.
def obtenerCentro_administradorCentro(centro, administrador_centro):
    try:
        # Obtiene las instancias de centro y del administrador para
        # posteriormente obtener los id's.
        instancia_centro = vistasCentro.obtenerCentro(centro)
        instancia_administrador_centro = \
            vistasAdministradorCentro.obtenerAdministradorCentro(
                administrador_centro)
        # Obtiene el centro_administradorCentro cuyo centro es centro y
        # cuyo administrador de centro es administrador_centro, a traves
        # de los id's.
        resultado = models.CentroAdministradorCentro.objects.get(
            id_centro=instancia_centro.id_centro,
            id_adm_centro=instancia_administrador_centro.id_adm_centro)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addCentro_administradorCentro(request, nombre_centro):
    # Se comprueba que exista el centro en caso de introducir uno.
    if nombre_centro != '':
        # Se comprueba que exista el centro pasado por argumento.
        instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

        # El centro no existe, se redirige.
        if not (instancia_centro):
            return HttpResponseRedirect(
                reverse('selectCentro_CentroAdministradorCentro'))

        id_centro = instancia_centro.id_centro
    # No se ha introducido un centro para la titulacion.
    else:
        id_centro = ''

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.Centro_AdministradorCentroForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Determina el centro al que inserta.
            id_centro = request.POST['id_centro']
            centro = models.Centro.objects.get(id_centro=id_centro)

            # Redirige a la pagina de listar
            # centro - administradorCentro.
            return HttpResponseRedirect(
                reverse('listCentro_administradorCentro',
                kwargs={'centro': centro, 'orden': 'nombre_adm_centro'})
                )
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.Centro_AdministradorCentroForm(
            initial={'id_centro': id_centro})
    return render_to_response(
        PATH + 'addCentro_administradorCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def editCentro_administradorCentro(request, centro,
    administrador_centro):
    # Se obtiene la instancia del centro_administradorCentro.
    instancia_centro_administradorCentro = \
        obtenerCentro_administradorCentro(centro, administrador_centro)
    # Si existe se edita.
    if instancia_centro_administradorCentro:
        # Se carga el formulario para el centro existente.
        form = forms.Centro_AdministradorCentroForm(
            instance=instancia_centro_administradorCentro)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.Centro_AdministradorCentroForm(request.POST,
                instance=instancia_centro_administradorCentro)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()

                # Redirige a la pagina de listar
                # centro - administradorCentro.
                return HttpResponseRedirect(
                    reverse('listCentro_administradorCentro',
                    kwargs={'centro':
                    instancia_centro_administradorCentro.id_centro,
                    'orden': 'nombre_adm_centro'}))
    # El centro_administradorCentro no existe
    else:
        form = False
    return render_to_response(
        PATH + 'editCentro_administradorCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def delCentro_administradorCentro(request,centro, administrador_centro):
    # Se obtiene la instancia del centro_administradorCentro.
    instancia_centro_administradorCentro = \
        obtenerCentro_administradorCentro(centro, administrador_centro)
    # Si existe se elimina.
    if instancia_centro_administradorCentro:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_centro_administradorCentro.delete()
            # Redirige a la pagina de listar centro - administradorCentro.
            return HttpResponseRedirect(
                reverse('listCentro_administradorCentro',
                kwargs={'centro': centro, 'orden': 'nombre_adm_centro'}))
    # El centro_administradorCentro no existe.
    else:
        form = True
    return render_to_response(
        PATH + 'delCentro_administradorCentro.html',
        {'user': request.user, 'form': form, 'centro': centro})

def ordenarPorAdministradorCentro(lista_centros_administradorCentro):
    # Lista auxiliar que albergara la nueva lista.
    lista_aux = []

    # Se recorre la lista de centros obteniendo los nombres de
    # administrador de centro de cada centro.
    for centro in lista_centros_administradorCentro:
        # Se introducen los nombres de centro en la nueva lista.
        lista_aux.append(centro.determinarNombreAdministradorCentro())
    # Obtenemos un set (valores unicos) ordenado con los valores de
    # la lista.
    set_aux = sorted(set(lista_aux))

    # Lista auxiliar que albergara la nueva lista.
    lista_aux = []

    # Para cada nombre de administrador de centro (de manera ordenada)
    # se crea una lista con los centros en el orden correcto.
    for s in set_aux:
        for centro in lista_centros_administradorCentro:
            if (centro.determinarNombreAdministradorCentro() == s):
                lista_aux.append(centro)

    return lista_aux

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

            return HttpResponseRedirect(
                reverse('listCentro_administradorCentro',
                kwargs={'centro': instancia_centro.nombre_centro,
                'orden': 'nombre_adm_centro'}))

        else:
            HttpResponseRedirect(
                reverse('selectCentro_CentroAdministradorCentro'))

    else:
        form = forms.CentroFormSelect()

    return render_to_response(
        PATH + 'selectCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def listCentro_administradorCentro(request, centro, orden):
    # Se comprueba que exista el centro pasado por argumento.
    instancia_centro = vistasCentro.obtenerCentro(centro)

    # El centro no existe, se redirige.
    if not (instancia_centro):
        return HttpResponseRedirect(
            reverse('selectCentro_CentroAdministradorCentro'))

    # Se obtiene una lista con todos los centros administrador
    # de centro.
    lista_centros_administradorCentro = \
        models.CentroAdministradorCentro.objects.filter(
            id_centro=instancia_centro.id_centro).order_by(
            'id_adm_centro')

    # Se debe hacer el ordenamiento de manera especial ya que estos
    # atributos son enteros y ordenamos alfabeticamente.
    lista_centros_administradorCentro = \
        ordenarPorAdministradorCentro(lista_centros_administradorCentro)

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
            for centro_adm_centro in lista_centros_administradorCentro:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(centro_adm_centro.id_adm_centro)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(centro_adm_centro)

            # La lista final a devolver sera la lista auxiliar.
            lista_centros_administradorCentro = lista_aux

        else:
            busqueda = False

    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        # Si el orden es descendente se invierte la lista.
        if (orden == '_nombre_adm_centro'):
            lista_centros_administradorCentro = \
                reversed(lista_centros_administradorCentro)

    return render_to_response(
        PATH + 'listCentro_administradorCentro.html',
        {'user': request.user, 'form': form,
        'lista_centros_administradorCentro':
        lista_centros_administradorCentro, 'busqueda': busqueda,
        'centro': centro, 'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaCentros_administradorCentro(request, centro,
    busqueda):
    # Se comprueba que exista el centro pasado por argumento.
    instancia_centro = vistasCentro.obtenerCentro(centro)

    # El centro no existe, se redirige.
    if not (instancia_centro):
        return HttpResponseRedirect(
            reverse('selectCentro_CentroAdministradorCentro'))

    # Se obtiene una lista con todos los centros.
    lista_centros_administradorCentro = \
        models.CentroAdministradorCentro.objects.filter(
            id_centro=instancia_centro.id_centro).order_by(
            'id_adm_centro')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
        # la busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con
        # la busqueda.
        for centro_adm_centro in lista_centros_administradorCentro:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = unicode(centro_adm_centro.id_adm_centro)

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(centro_adm_centro)

        # La lista final a devolver sera la lista auxiliar.
        lista_centros_administradorCentro = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_centros_administradorCentro,
        'name': 'centros-administrador de centro',})
