from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import vistasDepartamento
from asesorias.utils import vistasPDF

PATH = 'asesorias/AsesorCursoAcademico/'

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

def addAsesorCursoAcademico(request, dni_pasaporte):
    # Se comprueba que exista el asesor, en caso de introducirlo.
    if (dni_pasaporte != ''):
        # Se comprueba que exista el asesor.
        instancia_asesor = vistasAsesor.obtenerAsesor(dni_pasaporte)

        # Si no existe, se redirige.
        if not instancia_asesor:
            return HttpResponseRedirect(
                reverse('selectAsesor_AsesorCursoAcademico'))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.AsesorCursoAcademicoForm(request.POST)

        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()

            # Se obtiene el departamento y el asesor para redirigir.
            dni_pasaporte = request.POST['dni_pasaporte']

            # Redirige a la pagina de listar asesores curso academico.
            return HttpResponseRedirect(
                reverse('listAsesorCursoAcademico',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'orden': 'curso_academico'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.AsesorCursoAcademicoForm(
            initial={'dni_pasaporte': dni_pasaporte})
    return render_to_response(PATH + 'addAsesorCursoAcademico.html',
        {'user': request.user, 'form': form})

def editAsesorCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesor_curso_academico= obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se edita.
    if instancia_asesor_curso_academico:
        # Se guarda el anterior dni_pasaporte y curso academico.
        dni_pasaporte_antiguo = dni_pasaporte
        curso_academico_antiguo = curso_academico

        # Se carga el formulario para la asignatura existente.
        form = forms.AsesorCursoAcademicoForm(
            instance=instancia_asesor_curso_academico)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.AsesorCursoAcademicoForm(request.POST,
                instance=instancia_asesor_curso_academico)
            # Si es valido se guarda.
            if form.is_valid():
                instancia_asesor_curso_academico.editar(
                    dni_pasaporte_antiguo, curso_academico_antiguo)
                form.save()

                # Se obtiene el departamento y el asesor para redirigir.
                nombre_departamento = \
                    instancia_asesor_curso_academico.id_departamento
                dni_pasaporte = \
                    instancia_asesor_curso_academico.dni_pasaporte

                # Redirige a la pagina de listar asesores curso
                # academico.
                return HttpResponseRedirect(
                    reverse('listAsesorCursoAcademico',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'orden': 'curso_academico'}))
    # El asesor curso academico no existe.
    else:
        form = False
    return render_to_response(PATH + 'editAsesorCursoAcademico.html',
        {'user': request.user, 'form': form})

def delAsesorCursoAcademico(request, dni_pasaporte, curso_academico):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesor_curso_academico= obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)
    # Si existe se elimina.
    if instancia_asesor_curso_academico:
        nombre_departamento = \
            instancia_asesor_curso_academico.id_departamento

        instancia_asesor_curso_academico.borrar()
        # Redirige a la pagina de listar asesores curso academico.
        return HttpResponseRedirect(
            reverse('listAsesorCursoAcademico',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'orden': 'curso_academico'}))
    # El asesor curso academico no existe.
    else:
        error = True
    return render_to_response(PATH + 'delAsesorCursoAcademico.html',
        {'user': request.user, 'error': error})

def selectAsesor(request):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.AsesorFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            asesor = request.POST['asesor']

            return HttpResponseRedirect(
                reverse('listAsesorCursoAcademico',
                kwargs={'dni_pasaporte': asesor,
                'orden': 'curso_academico'}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_AsesorCursoAcademico'))

    else:
        form = forms.AsesorFormSelect()

    return render_to_response(PATH + 'selectAsesor.html',
        {'user': request.user, 'form': form})

def listAsesorCursoAcademico(request, dni_pasaporte, orden):
    # Se comprueba que exista el asesor pasado por argumento.
    existe_asesor = models.Asesor.objects.filter(
        dni_pasaporte=dni_pasaporte)

    # El asesor no existe, se redirige.
    if not (existe_asesor):
        return HttpResponseRedirect(
            reverse('selectAsesor_AsesorCursoAcademico'))


    # Se establece el ordenamiento inicial.
    if ((orden == 'nombre_departamento') or
        (orden == '_nombre_departamento')):
        orden_inicial = 'id_departamento'
        orden_secundario = 'curso_academico'
    else:
        orden_inicial = 'curso_academico'
        orden_secundario = 'id_departamento'

    # Se obtiene una lista con todos los asesores curso academico.
    lista_asesores_curso_academico = \
        models.AsesorCursoAcademico.objects.filter(
        dni_pasaporte=dni_pasaporte).order_by(
        orden_inicial, orden_secundario)

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
                cadena = (unicode(asesor.curso_academico) +
                    unicode(asesor.id_departamento))

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

        if ((orden == '_curso_academico') or
            (orden == '_nombre_departamento')):
            lista_asesores_curso_academico = \
                reversed(lista_asesores_curso_academico)

    return render_to_response(PATH + 'listAsesorCursoAcademico.html',
        {'user': request.user, 'form': form,
        'lista_asesores_curso_academico':
        lista_asesores_curso_academico,
        'busqueda': busqueda,
        'asesor': dni_pasaporte, 'orden': orden})

def generarPDFListaAsesoresCursoAcademico(request, dni_pasaporte,
    busqueda):
    # Se comprueba que exista el asesor pasado por argumento.
    existe_asesor_curso_academico = \
        models.AsesorCursoAcademico.objects.filter(
        dni_pasaporte=dni_pasaporte)

    # El asesor no existe, se redirige.
    if not (existe_asesor_curso_academico):
        return HttpResponseRedirect(
            reverse('selectAsesor_AsesorCursoAcademico'))

    # Se obtiene una lista con todos los asesores curso academico.
    lista_asesores_curso_academico = \
        models.AsesorCursoAcademico.objects.filter(
        dni_pasaporte=dni_pasaporte).order_by('curso_academico')

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
            cadena = (unicode(asesor.curso_academico) +
                unicode(asesor.id_departamento))

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(asesor)

        # La lista final a devolver sera la lista auxiliar.
        lista_asesores_curso_academico = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_asesores_curso_academico,
        'name': 'asesores curso academico',})
