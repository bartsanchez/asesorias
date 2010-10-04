from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.utils import vistasPDF


PATH = 'asesorias/UsuarioAsesor/'

def showAlumnos(request, curso_academico, orden):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se establece el ordenamiento inicial.
        if (orden == 'apellidos') or (orden == '_apellidos'):
            orden_inicial = 'dni_pasaporte_alumno__apellidos'
            orden_secundario = 'dni_pasaporte_alumno__nombre'
        else:
            orden_inicial = 'dni_pasaporte_alumno__nombre'
            orden_secundario = 'dni_pasaporte_alumno__apellidos'

        # Se obtiene una lista con todos los alumnos.
        lista_alumnosCA = models.AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico =
            instancia_asesorCA.codigo_asesorCursoAcademico).order_by(
            orden_inicial, orden_secundario)

    # El asesor aun no presta asesoria en este curso academico.
    else:
        lista_alumnosCA = ''

    # Se ha realizado una busqueda.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        # Si es valido se realiza la busqueda.
        if form.is_valid():
            busqueda = request.POST['busqueda']

            # Se crea una lista auxiliar que albergara el resultado
            # de la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden
            # con la busqueda.
            for alumno in lista_alumnosCA:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (unicode(alumno.dni_pasaporte_alumno.nombre) +
                    unicode(alumno.dni_pasaporte_alumno.apellidos))

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(alumno)

            # La lista final a devolver sera la lista auxiliar.
            lista_alumnosCA = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if ((orden == '_nombre') or
            (orden == '_apellidos')):
            lista_alumnosCA = reversed(lista_alumnosCA)

    return render_to_response(PATH + 'showAlumnos.html',
        {'user': request.user, 'form': form,
        'lista_alumnosCA': lista_alumnosCA,
        'busqueda': busqueda,
        'orden': orden,
        'curso_academico': curso_academico})

def generarPDFListaAlumnos(request, curso_academico, busqueda):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene una lista con todos los alumnos curso academico
        # para ese asesor.
        lista_aux = models.AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico =
            instancia_asesorCA.codigo_asesorCursoAcademico).order_by(
            'dni_pasaporte_alumno__nombre',
            'dni_pasaporte_alumno__apellidos')

        # Se ha realizado una busqueda.
        if busqueda != 'False':
            # Se crea una lista auxiliar que albergara el resultado
            # de la busqueda.
            lista_aux2 = []

            # Se recorren los elementos determinando si coinciden
            # con la busqueda.
            for alumno in lista_aux:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (unicode(alumno.dni_pasaporte_alumno.nombre) +
                    unicode(alumno.dni_pasaporte_alumno.apellidos))

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux2.append(alumno)

            # La lista final a devolver sera la lista auxiliar.
            lista_aux = lista_aux2

        # Se obtienen los nombres y los apellidos para los AlCA.
        lista_alumnosCA = []
        for alumno in lista_aux:
            lista_alumnosCA.append(alumno.nombre() + ' ' +
                alumno.apellidos())

    # El asesor aun no presta asesoria en este curso academico.
    else:
        lista_alumnosCA = ''
    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_alumnosCA,
        'name': 'alumnos asesorados',})

def showAlumno(request, curso_academico, dni_pasaporte):
    # Se obtiene la instancia del alumno.
    instancia_alumno = vistasAlumno.obtenerAlumno(dni_pasaporte)
    # Si existe se edita.
    if instancia_alumno:
        # Se carga el formulario para el asesor existente.
        form = forms.AlumnoForm(instance=instancia_alumno)

        # Se comprueba las matriculas del curso academico actual del
        # alumno.
        lista_matriculas = models.Matricula.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico).order_by('curso_academico')

        # Se comprueban las matriculas de distinto curso academico del
        # alumno.
        lista_matriculas_historica = models.Matricula.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico__lt=curso_academico).order_by(
            'curso_academico')
    # El alumno no existe.
    else:
        form = False
        lista_matriculas = ''
        lista_matriculas_historica = ''
    return render_to_response(PATH + 'showAlumno.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'lista_matriculas': lista_matriculas,
        'lista_matriculas_historica': lista_matriculas_historica})
