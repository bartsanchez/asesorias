from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/AlumnoCursoAcademico/'

# Comprueba si existe un alumno curso academico y, de ser asi, la
# devuelve.
def obtenerAlumnoCursoAcademico(dni_pasaporte, curso_academico):
    try:
        # Obtiene la instancia de alumno curso academico.
        resultado = models.AlumnoCursoAcademico.objects.get(
            dni_pasaporte_alumno=dni_pasaporte,
            curso_academico=curso_academico)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addAlumnoCursoAcademico(request, dni_pasaporte_asesor,
    curso_academico, dni_pasaporte_alumno):
    # Se comprueba que exista el asesor curso academico pasado por
    # argumento.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte_asesor, curso_academico)

    # El asesor curso academico no existe, se redirige.
    if not (instancia_asesorCA):
        return HttpResponseRedirect(
            reverse('selectAsesorCA_AlumnoCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte_asesor,
            'tipo': 'add'}))

    # Se comprueba que exista el alumno.
    instancia_alumno = vistasAlumno.obtenerAlumno(
        dni_pasaporte_alumno)

    # Si no existe, se redirige.
    if not instancia_alumno:
        return HttpResponseRedirect(
            reverse('selectAlumno_AlumnoCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte_asesor,
            'curso_academico': curso_academico,
            'tipo': 'add'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        observaciones = request.POST['observaciones']

        datos_alumno_curso_academico = {
            'dni_pasaporte_alumno': dni_pasaporte_alumno,
            'curso_academico': curso_academico,
            'observaciones': observaciones,
            'dni_pasaporte_asesor': dni_pasaporte_asesor}

        # Se obtienen los valores y se valida.
        form = forms.AlumnoCursoAcademicoForm(
            datos_alumno_curso_academico)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Redirige a la pagina de listar alumnos curso academico.
            return HttpResponseRedirect(
                reverse('listAlumnoCursoAcademico', kwargs={
                    'dni_pasaporte_asesor': dni_pasaporte_asesor,
                    'curso_academico': curso_academico,
                    'orden': 'dni_pasaporte'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AlumnoCursoAcademicoForm(
            initial={'dni_pasaporte_asesor': dni_pasaporte_asesor,
            'curso_academico': curso_academico,
            'dni_pasaporte_alumno': dni_pasaporte_alumno})
    return render_to_response(PATH + 'addAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte_alumno})

@checkAdministradorPrincipal
@login_required
def editAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del alumno curso academico.
    instancia_alumnoCA = obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se edita.
    if instancia_alumnoCA:
        # Se carga el formulario para la asignatura existente.
        form = forms.AlumnoCursoAcademicoForm(
            instance=instancia_alumnoCA)

        dni_pasaporte_asesor = instancia_alumnoCA.dni_pasaporte_asesor

        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se extraen los valores pasados por el metodo POST.
            observaciones = request.POST['observaciones']

            datos_alumno_curso_academico = {
                'dni_pasaporte_alumno': dni_pasaporte,
                'curso_academico': curso_academico,
                'observaciones': observaciones,
                'dni_pasaporte_asesor':
                dni_pasaporte_asesor}

            # Se obtienen los valores y se valida.
            form = forms.AlumnoCursoAcademicoForm(
                datos_alumno_curso_academico,
                instance=instancia_alumnoCA)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar alumnos curso
                # academico.
                return HttpResponseRedirect(
                    reverse('listAlumnoCursoAcademico', kwargs={
                    'dni_pasaporte_asesor': dni_pasaporte_asesor,
                    'curso_academico': curso_academico,
                    'orden': 'dni_pasaporte'}))
    # El alumno curso academico no existe.
    else:
        form = False
        dni_pasaporte_asesor = ''
    return render_to_response(PATH + 'editAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte})

@checkAdministradorPrincipal
@login_required
def delAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del alumno curso academico.
    instancia_alumno_curso_academico= obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se elimina.
    if instancia_alumno_curso_academico:
        # Se carga el formulario de confirmacion.
        form = forms.RealizarConfirmacion()
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            form = forms.RealizarConfirmacion(request.POST)
            confirmacion = request.POST['confirmacion']

            if confirmacion == 'True':
                instancia_alumno_curso_academico.borrar()
            # Redirige a la pagina de listar alumnos curso academico.
            return HttpResponseRedirect(reverse('listAlumnoCursoAcademico',
                kwargs={
                'dni_pasaporte_asesor':
                instancia_alumno_curso_academico.dni_pasaporte_asesor,
                'curso_academico': curso_academico,
                'orden': 'dni_pasaporte'}))
    # El alumno curso academico no existe.
    else:
        form = True
    return render_to_response(PATH + 'delAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form})

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
                reverse('selectAsesorCA_AlumnoCursoAcademico',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_AlumnoCursoAcademico',
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
            reverse('selectAsesor_AlumnoCursoAcademico',
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
                    reverse('selectAlumno_AlumnoCursoAcademico',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'tipo': tipo}))

            else:
                return HttpResponseRedirect(
                    reverse('listAlumnoCursoAcademico',
                    kwargs={'dni_pasaporte_asesor': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'orden': 'dni_pasaporte'}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_AlumnoCursoAcademico',
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
def selectAlumno(request, dni_pasaporte, curso_academico, tipo):
    # Se obtiene el posible asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesorCA:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_AlumnoCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': tipo}))

    # Se ha introducido un alumno.
    if request.method == 'POST':

        # Se obtiene el alumno y se valida.
        form = forms.AlumnoFormSelect(request.POST)

        # Si es valido se redirige a listar alumnos curso academico.
        if form.is_valid():
            alumno = request.POST['alumno']

            # Se crea una instancia del alumno para pasar el nombre de
            # alumno por argumento.
            instancia_alumno = models.Alumno.objects.get(pk=alumno)

            return HttpResponseRedirect(
                reverse('addAlumnoCursoAcademico',
                kwargs={'dni_pasaporte_asesor': dni_pasaporte,
                'curso_academico': curso_academico,
                'dni_pasaporte_alumno': alumno}))

        else:
            HttpResponseRedirect(
                reverse('selectAlumno_AlumnoCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

    else:
        form = forms.AlumnoFormSelect()

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def listAlumnoCursoAcademico(request, dni_pasaporte_asesor,
    curso_academico, orden):
    # Se comprueba que exista el asesor curso academico pasado por
    # argumento.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte_asesor, curso_academico)

    # El asesor curso academico no existe, se redirige.
    if not (instancia_asesorCA):
        return HttpResponseRedirect(
            reverse('selectAsesorCA_AlumnoCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte_asesor,
            'tipo': 'list'}))

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_asesor=instancia_asesorCA.dni_pasaporte,
        curso_academico=curso_academico).order_by(
        'dni_pasaporte_alumno')

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
            for alumno in lista_alumnos_curso_academico:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(alumno.dni_pasaporte_alumno)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(alumno)

            # La lista final a devolver sera la lista auxiliar.
            lista_alumnos_curso_academico = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if (orden == '_dni_pasaporte'):
            lista_alumnos_curso_academico = \
                reversed(lista_alumnos_curso_academico)

    return render_to_response(PATH + 'listAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'lista_alumnos_curso_academico': lista_alumnos_curso_academico,
        'busqueda': busqueda,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaAlumnosCursoAcademico(request, dni_pasaporte,
    curso_academico, busqueda):
    # Se comprueba que exista el asesor curso academico pasado por
    # argumento.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # El asesor curso academico no existe, se redirige.
    if not (instancia_asesorCA):
        return HttpResponseRedirect(
            reverse('selectAsesorCA_AlumnoCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': 'list'}))

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_asesor=
        instancia_asesorCA.dni_pasaporte).order_by(
        'dni_pasaporte_alumno')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de la
        # busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con la
        # busqueda.
        for alumno in lista_alumnos_curso_academico:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = unicode(alumno.dni_pasaporte_alumno)

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(alumno)

        # La lista final a devolver sera la lista auxiliar.
        lista_alumnos_curso_academico = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_alumnos_curso_academico,
        'name': 'alumnos curso academico',})
