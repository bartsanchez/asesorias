from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.utils import vistasPDF

# Comprueba si existe un alumno y, de ser asi, lo devuelve.
def obtenerAlumno(dni_pasaporte):
    try:
        # Obtiene el alumno cuyo dni es dni_pasaporte.
        resultado = models.Alumno.objects.get(pk=dni_pasaporte)
    except:
        resultado = False
    return resultado

def addAlumno(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.AlumnoForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Se crea un usuario django.
            username = request.POST['dni_pasaporte']
            email = request.POST['correo_electronico']
            password = username

            user = User.objects.create_user(username, email, password)
            user.save()

            # Redirige a la pagina de listar asesores.
            return HttpResponseRedirect(reverse('listAlumno',
                kwargs={'orden': 'nombre_alumno'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AlumnoForm()
    return render_to_response('asesorias/Alumno/addAlumno.html',
        {'user': request.user, 'form': form})

def editAlumno(request, dni_pasaporte):
    # Se obtiene la instancia del alumno.
    instancia_alumno = obtenerAlumno(dni_pasaporte)
    # Si existe se edita.
    if instancia_alumno:
        # Se carga el formulario para el alumno existente.
        form = forms.AlumnoForm(instance=instancia_alumno)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se extraen los valores pasados por el metodo POST.
            correo_electronico = request.POST['correo_electronico']
            nombre =  request.POST['nombre']
            apellidos = request.POST['apellidos']
            fecha_nacimiento =  request.POST['fecha_nacimiento']
            direccion_cordoba =  request.POST['direccion_cordoba']
            localidad_familiar =  request.POST['localidad_familiar']
            provincia_familiar =  request.POST['provincia_familiar']
            codigo_postal =  request.POST['codigo_postal']
            telefono_familiar =  request.POST['telefono_familiar']
            ingreso =  request.POST['ingreso']
            otros_estudios_universitarios =  \
                request.POST['otros_estudios_universitarios']
            modalidad_acceso_universidad =  \
                request.POST['modalidad_acceso_universidad']
            calificacion_acceso =  request.POST['calificacion_acceso']

            # Datos necesarios para crear el nuevo alumno.
            datos_alumno = {'dni_pasaporte': dni_pasaporte,
                'correo_electronico': correo_electronico,
                'nombre': nombre,
                'apellidos': apellidos,
                'fecha_nacimiento': fecha_nacimiento,
                'direccion_cordoba': direccion_cordoba,
                'localidad_familiar': localidad_familiar,
                'provincia_familiar': provincia_familiar,
                'codigo_postal': codigo_postal,
                'telefono_familiar': telefono_familiar,
                'ingreso': ingreso,
                'otros_estudios_universitarios':
                otros_estudios_universitarios,
                'modalidad_acceso_universidad':
                modalidad_acceso_universidad,
                'calificacion_acceso': calificacion_acceso}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.AlumnoForm(datos_alumno,
                instance=instancia_alumno)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar asesores.
                return HttpResponseRedirect(reverse('listAlumno',
                    kwargs={'orden': 'nombre_asesor'}))
    # El alumno no existe.
    else:
        form = False
    return render_to_response('asesorias/Alumno/editAlumno.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte})

def delAlumno(request, dni_pasaporte):
    # Se obtiene la instancia del alumno.
    instancia_alumno = obtenerAlumno(dni_pasaporte)
    # Si existe se elimina.
    if instancia_alumno:
        instancia_alumno.delete()
        # Redirige a la pagina de listar alumnos.
        return HttpResponseRedirect(reverse('listAlumno',
            kwargs={'orden': 'nombre_asesor'}))
    # El alumno no existe.
    else:
        error = True
    return render_to_response('asesorias/Alumno/delAlumno.html',
        {'user': request.user, 'error': error})

def listAlumno(request, orden):
    # Se obtiene una lista con todos los alumnos.
    lista_alumnos = models.Alumno.objects.order_by('dni_pasaporte')

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']
            lista_alumnos = lista_alumnos.filter(
                dni_pasaporte__contains=busqueda)
        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_nombre_alumno':
            lista_alumnos = lista_alumnos.reverse()

    return render_to_response('asesorias/Alumno/listAlumno.html',
        {'user': request.user, 'form': form,
        'lista_alumnos': lista_alumnos,
        'busqueda': busqueda,
        'orden': orden})

def generarPDFListaAlumnos(request, busqueda):
    # Se obtiene una lista con todos los alumnos.
    lista_alumnos = models.Alumno.objects.order_by('dni_pasaporte')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_alumnos = lista_alumnos.filter(
            dni_pasaporte__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_alumnos, 'name': 'alumnos',})
