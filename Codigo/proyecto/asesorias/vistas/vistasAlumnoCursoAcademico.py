from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAlumno
from asesorias.vistas import vistasAsesor, vistasAsesorCursoAcademico
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
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': 'add'}))

    # Se comprueba que exista el alumno, en caso de introducirlo.
    if (dni_pasaporte_alumno != ''):
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
        # Se obtienen los valores y se valida.
        form = forms.AlumnoCursoAcademicoForm(request.POST)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            dni_pasaporte = request.POST['dni_pasaporte']

            # Redirige a la pagina de listar alumnos curso academico.
            return HttpResponseRedirect(
                reverse('listAlumnoCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'orden': 'curso_academico'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AlumnoCursoAcademicoForm(
            initial={'dni_pasaporte_asesor':
            instancia_asesorCA.codigo_asesorCursoAcademico,
            'curso_academico': curso_academico,
            'dni_pasaporte_alumno': dni_pasaporte_alumno})
    return render_to_response(PATH + 'addAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form})

def editAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del alumno curso academico.
    instancia_alumno_curso_academico= obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se edita.
    if instancia_alumno_curso_academico:
        # Se carga el formulario para la asignatura existente.
        form = forms.AlumnoCursoAcademicoForm(
            instance=instancia_alumno_curso_academico)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.AlumnoCursoAcademicoForm(request.POST,
                instance=instancia_alumno_curso_academico)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar alumnos curso
                # academico.
                return HttpResponseRedirect(
                    reverse('listAlumnoCursoAcademico',
                    kwargs={'dni_pasaporte':
                    instancia_alumno_curso_academico.dni_pasaporte,
                    'orden': 'curso_academico'}))
    # El alumno curso academico no existe.
    else:
        form = False
    return render_to_response(PATH + 'editAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form})

def delAlumnoCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del alumno curso academico.
    instancia_alumno_curso_academico= obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se elimina.
    if instancia_alumno_curso_academico:
        instancia_alumno_curso_academico.delete()
        # Redirige a la pagina de listar alumnos curso academico.
        return HttpResponseRedirect(reverse('listAlumnoCursoAcademico',
            kwargs={'dni_pasaporte':
            instancia_alumno_curso_academico.dni_pasaporte,
            'orden': 'curso_academico'}))
    # El alumno curso academico no existe.
    else:
        error = True
    return render_to_response(PATH + 'delAlumnoCursoAcademico.html',
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

            return HttpResponseRedirect(
                reverse('selectAlumno_AlumnoCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

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

def selectAlumno(request, dni_pasaporte, curso_academico, tipo):
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

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addAlumnoCursoAcademico',
                    kwargs={'dni_pasaporte_asesor': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'dni_pasaporte_alumno': alumno}))

            else:
                return HttpResponseRedirect()

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

def listAlumnoCursoAcademico(request, dni_pasaporte, orden):
    # Se comprueba que exista el alumno pasado por argumento.
    instancia_alumno = vistasAlumno.obtenerAlumno(dni_pasaporte)

    # El alumno no existe, se redirige.
    if not (instancia_alumno):
        return HttpResponseRedirect(
            reverse('selectAlumno_AlumnoCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': 'list'}))

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_alumno=dni_pasaporte).order_by('curso_academico')

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
                cadena = unicode(alumno.curso_academico)

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

        if (orden == '_curso_academico'):
            lista_alumnos_curso_academico = \
                reversed(lista_alumnos_curso_academico)

    return render_to_response(PATH + 'listAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'lista_alumnos_curso_academico': lista_alumnos_curso_academico,
        'busqueda': busqueda, 'alumno': dni_pasaporte, 'orden': orden})

def generarPDFListaAlumnosCursoAcademico(request, dni_pasaporte,
    busqueda):
    # Se comprueba que exista el alumno pasado por argumento.
    existe_alumno_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte=dni_pasaporte)

    # El alumno no existe, se redirige.
    if not (existe_alumno_curso_academico):
        return HttpResponseRedirect(
            reverse('selectAlumno_AlumnoCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': 'list'}))

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_alumno=dni_pasaporte).order_by('dni_pasaporte')

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
            cadena = unicode(alumno.curso_academico)

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(alumno)

        # La lista final a devolver sera la lista auxiliar.
        lista_alumnos_curso_academico = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_alumnos_curso_academico,
        'name': 'alumnos curso academico',})
