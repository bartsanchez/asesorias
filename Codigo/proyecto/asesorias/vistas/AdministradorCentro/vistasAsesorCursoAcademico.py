from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import vistasCentro
from asesorias.vistas.AdministradorPrincipal import vistasDepartamento
from asesorias.utils import vistasPDF

PATH = 'asesorias/UsuarioAdministradorCentro/AsesorCursoAcademico/'

# Comprueba si existe un asesor curso academico y, de ser asi,
# la devuelve.
def obtenerAsesorCursoAcademico(dni_pasaporte, curso_academico):
    try:
        # Obtiene la instancia de asesor curso academico.
        resultado = models.AsesorCursoAcademico.objects.get(
            dni_pasaporte=dni_pasaporte,
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
                reverse('listAsesorCursoAcademico_administradorCentro',
                kwargs={'centro': centro,
                'curso_academico': curso_academico,
                'orden': 'dni_pasaporte'}))
    else:
        form = forms.CursoAcademicoFormSelect()

    return render_to_response(PATH + 'selectCursoAcademico.html',
        {'user': request.user, 'form': form,
        'centro': centro})

def listAsesorCursoAcademico(request, centro, curso_academico, orden):
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
        curso_academico=curso_academico)

    # Lista auxiliar que albergara los dni's de los asesores.
    lista_asesores_aux = []
    for alumno in lista_alumnos_curso_academico:
        lista_asesores_aux.append(
            alumno.codigo_asesorCursoAcademico.dni_pasaporte)

    # Se obtiene una lista con todos los asesores curso academico.
    lista_asesores_curso_academico = \
        models.AsesorCursoAcademico.objects.filter(
        dni_pasaporte__in=lista_asesores_aux,
        curso_academico=curso_academico)

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
            for asesor in lista_asesores_curso_academico:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (unicode(asesor.dni_pasaporte) +
                    unicode(asesor.dni_pasaporte.nombre) +
                    unicode(asesor.dni_pasaporte.apellidos) +
                    unicode(asesor.id_departamento.nombre_departamento))

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(asesor)

            # La lista final a devolver sera la lista auxiliar.
            lista_asesores_curso_academico = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if ((orden == '_dni_pasaporte') or (orden == '_nombre') or
            (orden == '_apellidos') or (orden == '_departamento')):
            lista_asesores_curso_academico = \
                reversed(lista_asesores_curso_academico)

    return render_to_response(PATH + 'listAsesorCursoAcademico.html',
        {'user': request.user, 'form': form,
        'lista_asesores_curso_academico':
        lista_asesores_curso_academico,
        'busqueda': busqueda, 'orden': orden,
        'centro': centro, 'curso_academico': curso_academico})

def generarPDFListaAsesoresCursoAcademico(request, centro,
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
        curso_academico=curso_academico)

    # Lista auxiliar que albergara los dni's de los asesores.
    lista_asesores_aux = []
    for alumno in lista_alumnos_curso_academico:
        lista_asesores_aux.append(
            alumno.codigo_asesorCursoAcademico.dni_pasaporte)

    # Se obtiene una lista con todos los asesores curso academico.
    lista_asesores_curso_academico = \
        models.AsesorCursoAcademico.objects.filter(
        dni_pasaporte__in=lista_asesores_aux,
        curso_academico=curso_academico)

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de la
        # busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con la
        # busqueda.
        for asesor in lista_asesores_curso_academico:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = (unicode(asesor.dni_pasaporte) +
                    unicode(asesor.dni_pasaporte.nombre) +
                    unicode(asesor.dni_pasaporte.apellidos) +
                    unicode(asesor.id_departamento.nombre_departamento))

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(asesor)

        # La lista final a devolver sera la lista auxiliar.
        lista_asesores_curso_academico = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_asesores_curso_academico,
        'name': 'asesores curso academico',})
