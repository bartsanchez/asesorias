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

# Comprueba si existe un asesor y, de ser asi, lo devuelve.
def obtenerAsesor(dni_pasaporte):
    try:
        # Obtiene el asesor cuyo dni es dni_pasaporte.
        resultado = models.Asesor.objects.get(pk=dni_pasaporte)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addAsesor(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.AsesorForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Se crea un usuario django.
            username = request.POST['dni_pasaporte']
            email = request.POST['correo_electronico']
            password = User.objects.make_random_password()

            user = User.objects.create_user(username, email, password)
            user.save()

            vistas.vistasGestionUsuarios.enviar_mail_creacion_usuario(
                request, email, username, password)

            # Redirige a la pagina de listar asesores.
            return HttpResponseRedirect(reverse('listAsesor',
                kwargs={'orden': 'nombre_asesor'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AsesorForm()
    return render_to_response('asesorias/Asesor/addAsesor.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def editAsesor(request, dni_pasaporte):
    # Se obtiene la instancia del asesor.
    instancia_asesor = obtenerAsesor(dni_pasaporte)
    # Si existe se edita.
    if instancia_asesor:
        # Se carga el formulario para el asesor existente.
        form = forms.AsesorForm(instance=instancia_asesor)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se extraen los valores pasados por el metodo POST.
            correo_electronico= request.POST['correo_electronico']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            telefono = request.POST['telefono']

            # Datos necesarios para crear el nuevo asesor.
            datos_asesor = {'dni_pasaporte': dni_pasaporte,
                'correo_electronico': correo_electronico,
                'nombre': nombre,
                'apellidos': apellidos,
                'telefono': telefono}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.AsesorForm(datos_asesor,
                instance=instancia_asesor)
            # Si es valido se guarda.
            if form.is_valid():
                user = User.objects.get(
                    username=dni_pasaporte)
                user.email=unicode(correo_electronico)
                user.save()
                
                form.save()
                # Redirige a la pagina de listar asesores.
                return HttpResponseRedirect(reverse('listAsesor',
                    kwargs={'orden': 'nombre_asesor'}))
    # El asesor no existe.
    else:
        form = False
    return render_to_response('asesorias/Asesor/editAsesor.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte})

@checkAdministradorPrincipal
@login_required
def delAsesor(request, dni_pasaporte):
    # Se obtiene la instancia del asesor.
    instancia_asesor = obtenerAsesor(dni_pasaporte)
    # Si existe se elimina.
    if instancia_asesor:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_asesor.borrar()
            # Redirige a la pagina de listar asesores.
            return HttpResponseRedirect(reverse('listAsesor',
                kwargs={'orden': 'nombre_asesor'}))
    # El asesor no existe.
    else:
        form = True
    return render_to_response('asesorias/Asesor/delAsesor.html',
        {'user': request.user, 'form': form})

@checkAdministradorPrincipal
@login_required
def listAsesor(request, orden):
    # Se obtiene una lista con todos los asesores.
    lista_asesores = models.Asesor.objects.order_by('dni_pasaporte')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']
            lista_asesores = lista_asesores.filter(
                dni_pasaporte__contains=busqueda)
        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_nombre_asesor':
            lista_asesores = lista_asesores.reverse()

    return render_to_response('asesorias/Asesor/listAsesor.html',
        {'user': request.user, 'form': form,
        'lista_asesores': lista_asesores, 'busqueda': busqueda,
        'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaAsesores(request, busqueda):
    # Se obtiene una lista con todos los asesores.
    lista_asesores = models.Asesor.objects.order_by('dni_pasaporte')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_asesores = lista_asesores.filter(
            dni_pasaporte__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_asesores , 'name': 'asesores',})
