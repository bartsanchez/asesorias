from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias import vistas
from asesorias.utils import vistasPDF

# Comprueba si existe un administrador de centro y, de ser asi,
# lo devuelve.
def obtenerAdministradorCentro(administrador_centro):
    try:
        # Obtiene el administrador centro cuyo nombre es
        # administrador_centro.
        resultado = models.AdministradorCentro.objects.get(
            nombre_adm_centro=administrador_centro)
    except:
        resultado = False
    return resultado

def addAdministradorCentro(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.AdministradorCentroForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            instancia_admin_centro = form.save()

            # Se crea un usuario django.
            username = ('AdminCentro' +
                unicode(instancia_admin_centro.id_adm_centro))
            password = unicode(instancia_admin_centro.id_adm_centro)
            email = "aliaselbarto@gmail.com"

            user = User.objects.create_user(username, '', password)
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

def editAdministradorCentro(request, administrador_centro):
    # Se obtiene la instancia del administrador de centro.
    instancia_admin_centro = obtenerAdministradorCentro(
        administrador_centro)
    # Si existe se edita.
    if instancia_admin_centro:
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

def delAdministradorCentro(request, administrador_centro):
    # Se obtiene la instancia del administrador de centro.
    instancia_admin_centro = obtenerAdministradorCentro(
        administrador_centro)
    # Si existe se elimina.
    if instancia_admin_centro:
        username = ('AdminCentro' +
            unicode(instancia_admin_centro.id_adm_centro))

        instancia_admin_centro.delete()

        user = User.objects.get(username__exact=username)
        user.delete()

        # Redirige a la pagina de listar administradores de centro.
        return HttpResponseRedirect(
            reverse('listAdministradorCentro',
            kwargs={'orden': 'nombre_adm_centro'}) )
    # El administrador de centro no existe.
    else:
        error = True
    return render_to_response(
        'asesorias/AdministradorCentro/delAdministradorCentro.html',
        {'user': request.user, 'error': error})

def listAdministradorCentro(request, orden):
    # Se obtiene una lista con todos los centros.
    lista_administradores_centro = \
        models.AdministradorCentro.objects.order_by('nombre_adm_centro')

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

        if orden == '_nombre_adm_centro':
            lista_administradores_centro = \
                lista_administradores_centro.reverse()

    return render_to_response(
        'asesorias/AdministradorCentro/listAdministradorCentro.html',
        {'user': request.user, 'form': form,
        'lista_administradores_centro': lista_administradores_centro,
        'busqueda': busqueda, 'orden': orden})

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
