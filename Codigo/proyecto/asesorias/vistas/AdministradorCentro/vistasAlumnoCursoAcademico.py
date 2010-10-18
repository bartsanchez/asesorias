from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import vistasCentro
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.utils import vistasPDF

PATH = 'asesorias/UsuarioAdministradorCentro/AlumnoCursoAcademico/'

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

def selectCursoAcademico(request, centro):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.CursoAcademicoFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            curso_academico = request.POST['curso_academico']

            return HttpResponseRedirect(
                reverse('listAlumnoCursoAcademico_administradorCentro',
                kwargs={'centro': centro,
                'curso_academico': curso_academico,
                'orden': 'dni_pasaporte'}))
    else:
        form = forms.CursoAcademicoFormSelect()

    return render_to_response(PATH + 'selectCursoAcademico.html',
        {'user': request.user, 'form': form,
        'centro': centro})

def listAlumnoCursoAcademico(request, centro, curso_academico, orden):
    # Se obtiene el posible centro.
    instancia_centro = vistasCentro.obtenerCentro(centro)

    # Se comprueba que exista el centro.
    if not instancia_centro:
        return HttpResponseRedirect(
            reverse('administradorCentro_inicio',
            kwargs={'centro': centro}))

    # Se establece el ordenamiento inicial.
    if ((orden == 'nombre') or (orden == '_nombre')):
        orden_inicial = 'dni_pasaporte_alumno__nombre'
        orden_secundario = 'dni_pasaporte_alumno__apellidos'
    elif ((orden == 'apellidos') or (orden == '_apellidos')):
        orden_inicial = 'dni_pasaporte_alumno__apellidos'
        orden_secundario = 'dni_pasaporte_alumno__nombre'
    else:
        orden_inicial = 'dni_pasaporte_alumno'
        orden_secundario = 'dni_pasaporte_alumno__nombre'

    # Se obtiene una lista con todas las matriculas de ese centro
    # en el curso academico pasado por argumento.
    lista_matriculas = models.Matricula.objects.filter(
        id_centro=instancia_centro.id_centro,
        curso_academico=curso_academico).values_list(
        'dni_pasaporte', flat=True).distinct()

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_alumno__in=lista_matriculas,
        curso_academico=curso_academico).order_by(orden_inicial,
        orden_secundario)

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
                cadena = (
                    unicode(alumno.dni_pasaporte_alumno.dni_pasaporte) +
                    unicode(alumno.dni_pasaporte_alumno.nombre) +
                    unicode(alumno.dni_pasaporte_alumno.apellidos))

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

        if ((orden == '_dni_pasaporte') or (orden == '_nombre') or
            (orden == '_apellidos')):
            lista_alumnos_curso_academico = \
                reversed(lista_alumnos_curso_academico)

    return render_to_response(PATH + 'listAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'lista_alumnos_curso_academico': lista_alumnos_curso_academico,
        'busqueda': busqueda,
        'curso_academico': curso_academico,
        'orden': orden, 'centro': centro})

def generarPDFListaAlumnosCursoAcademico(request, centro,
    curso_academico, busqueda):
    # Se obtiene el posible centro.
    instancia_centro = vistasCentro.obtenerCentro(centro)

    # Se comprueba que exista el centro.
    if not instancia_centro:
        return HttpResponseRedirect(
            reverse('administradorCentro_inicio',
            kwargs={'centro': centro}))

    # Se obtiene una lista con todas las matriculas de ese centro
    # en el curso academico pasado por argumento.
    lista_matriculas = models.Matricula.objects.filter(
        id_centro=instancia_centro.id_centro,
        curso_academico=curso_academico).values_list(
        'dni_pasaporte', flat=True).distinct()

    # Se obtiene una lista con todos los alumnos curso academico.
    lista_alumnos_curso_academico = \
        models.AlumnoCursoAcademico.objects.filter(
        dni_pasaporte_alumno__in=lista_matriculas,
        curso_academico=curso_academico).order_by(
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
            cadena = (
                    unicode(alumno.dni_pasaporte_alumno.dni_pasaporte) +
                    unicode(alumno.dni_pasaporte_alumno.nombre) +
                    unicode(alumno.dni_pasaporte_alumno.apellidos))

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(alumno)

        # La lista final a devolver sera la lista auxiliar.
        lista_alumnos_curso_academico = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_alumnos_curso_academico,
        'name': 'alumnos curso academico',})
