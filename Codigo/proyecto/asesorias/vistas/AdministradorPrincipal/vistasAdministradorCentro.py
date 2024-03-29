from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias import vistas
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

# Comprueba si existe un administrador de centro y, de ser asi,
# lo devuelve.
def obtenerAdministradorCentro(administrador_centro):
    try:
        # Obtiene el administrador centro cuyo nombre es
        # administrador_centro.
        resultado = models.AdministradorCentro.objects.get(
            id_adm_centro=administrador_centro)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addAdministradorCentro(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.AdministradorCentroForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            instancia_admin_centro = form.save()

            # Se crea un usuario django.
            username = \
                unicode(instancia_admin_centro.correo_electronico)
            password = User.objects.make_random_password()
            email = unicode(instancia_admin_centro.correo_electronico)
            name = unicode(instancia_admin_centro.nombre_adm_centro)

            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.save()

            vistas.vistasGestionUsuarios.enviar_mail_creacion_usuario(
                request, email, username, password)

            # Redirige a la pagina de listar administradores de centro.
            return HttpResponseRedirect(
                reverse('listAdministradorCentro',
                kwargs={'orden': 'nombre_adm_centro'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AdministradorCentroForm()
    return render_to_response(
        'asesorias/AdministradorCentro/addAdministradorCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def editAdministradorCentro(request, administrador_centro):
    # Se obtiene la instancia del administrador de centro.
    instancia_admin_centro = obtenerAdministradorCentro(
        administrador_centro)
    # Si existe se edita.
    if instancia_admin_centro:
        correo_electronico_antiguo = \
            unicode(instancia_admin_centro.correo_electronico)        
        # Se carga el formulario para el administrador de centro centro
        # existente.
        form = forms.AdministradorCentroForm(
            instance=instancia_admin_centro)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.AdministradorCentroForm(request.POST,
                instance=instancia_admin_centro)
            # Si es valido se guarda.
            if form.is_valid():
                correo_electronico_nuevo = \
                        request.POST['correo_electronico']

                user = User.objects.get(
                    username=correo_electronico_antiguo)
                user.username = correo_electronico_nuevo
                user.email = correo_electronico_nuevo
                user.save()

                form.save()

                # Redirige a la pagina de listar administradores de
                # centro.
                return HttpResponseRedirect(reverse(
                    'listAdministradorCentro',
                    kwargs={'orden': 'nombre_adm_centro'}))
    # El administrador de centro no existe
    else:
        form = False
    return render_to_response(
        'asesorias/AdministradorCentro/editAdministradorCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def delAdministradorCentro(request, administrador_centro):
    # Se obtiene la instancia del administrador de centro.
    instancia_admin_centro = obtenerAdministradorCentro(
        administrador_centro)
    # Si existe se elimina.
    if instancia_admin_centro:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()

        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                username = \
                    unicode(instancia_admin_centro.correo_electronico)
                instancia_admin_centro.borrar()
                user = User.objects.get(username__exact=username)
                user.delete()

            # Redirige a la pagina de listar administradores de centro.
            return HttpResponseRedirect(
                reverse('listAdministradorCentro',
                kwargs={'orden': 'nombre_adm_centro'}) )
    # El administrador de centro no existe.
    else:
        form = True
    return render_to_response(
        'asesorias/AdministradorCentro/delAdministradorCentro.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def listAdministradorCentro(request, orden):
    # Se establece el ordenamiento inicial.
    if ((orden == 'nombre_adm_centro') or
        (orden == '_nombre_adm_centro')):
        orden_inicial = 'nombre_adm_centro'
        orden_secundario = 'correo_electronico'
    else:
        orden_inicial = 'correo_electronico'
        orden_secundario = 'nombre_adm_centro'

    # Se obtiene una lista con todos los centros.
    lista_administradores_centro = \
        models.AdministradorCentro.objects.order_by(orden_inicial,
        orden_secundario)

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']
            lista_administradores_centro = \
                lista_administradores_centro.filter(
                    nombre_adm_centro__contains=busqueda)
        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if ((orden == '_nombre_adm_centro') or
            (orden == '_correo_electronico')):
            lista_administradores_centro = \
                lista_administradores_centro.reverse()

    return render_to_response(
        'asesorias/AdministradorCentro/listAdministradorCentro.html',
        {'user': request.user, 'form': form,
        'lista_administradores_centro': lista_administradores_centro,
        'busqueda': busqueda, 'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaAdministradoresCentro(request, busqueda):
    # Se obtiene una lista con todos los administradores de centro.
    lista_administradores_centro = \
        models.AdministradorCentro.objects.order_by('nombre_adm_centro')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_administradores_centro = \
            lista_administradores_centro.filter(
                nombre_adm_centro__contains=busqueda)

    return vistasPDF.render_to_pdf(
        'asesorias/plantilla_pdf.html',
        {'mylist': lista_administradores_centro,
        'name': 'administradores de centro',})
