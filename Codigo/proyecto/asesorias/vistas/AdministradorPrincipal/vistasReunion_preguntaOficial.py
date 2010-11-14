from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesor, vistasAsesorCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasReunion, vistasPreguntaOficial
from asesorias.vistas.AdministradorPrincipal import \
    vistasPlantillaEntrevistaOficial \
    as vistasPEO
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF

PATH = 'asesorias/Reunion_PreguntaOficial/'

# Comprueba si existe una reunion - pregunta oficial y, de ser asi, la
# devuelve.
def obtenerReunion_preguntaOficial(dni_pasaporte, curso_academico,
    id_reunion, id_entrevista_oficial, id_pregunta_oficial):
    try:
        # Obtiene la instancia de reunion - pregunta oficial.
        resultado = models.ReunionPreguntaOficial.objects.get(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico,
            id_reunion=id_reunion,
            id_entrevista_oficial=id_entrevista_oficial,
            id_pregunta_oficial=id_pregunta_oficial)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addReunion_preguntaOficial(request, dni_pasaporte, curso_academico,
    id_reunion, id_entrevista_oficial, id_pregunta_oficial):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumnoCA = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumnoCA:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se obtiene la instancia de la reunion.
    instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
        curso_academico, id_reunion)

    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se obtiene la instancia de la pregunta oficial.
    instancia_pregunta_oficial = \
        vistasPreguntaOficial.obtenerPreguntaOficial(
        id_entrevista_oficial, id_pregunta_oficial)

    if not instancia_pregunta_oficial:
        return HttpResponseRedirect(
            reverse('selectPreguntaOficial_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_reunion': id_reunion,
            'id_entrevista_oficial': id_entrevista_oficial}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumnoCA.codigo_asesorCursoAcademico

    dni_pasaporte_asesor = instancia_asesorCA.dni_pasaporte

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        #Se extraen los valores pasados por el metodo POST.
        respuesta = request.POST['respuesta']

        # Datos necesarios para crear la nueva reunion - pregunta
        # oficial.
        datos_reunion_preguntaOficial = {
            'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_reunion': id_reunion,
            'id_entrevista_oficial': id_entrevista_oficial,
            'id_pregunta_oficial': id_pregunta_oficial,
            'respuesta': respuesta}

        # Se obtienen los valores y se valida.
        form = forms.Reunion_PreguntaOficialForm(
            datos_reunion_preguntaOficial)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar reuniones - preguntas de
            # asesor.
            return HttpResponseRedirect(
                reverse('listReunion_preguntaOficial',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_reunion': instancia_reunion.id_reunion,
                    'orden': 'pregunta_asesor'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.Reunion_PreguntaOficialForm()
    return render_to_response(PATH + 'addReunion_preguntaOficial.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'id_reunion': id_reunion,
        'fecha_reunion': instancia_reunion.fecha,
        'id_entrevista_oficial': id_entrevista_oficial,
        'id_pregunta_oficial': id_pregunta_oficial})

@checkAdministradorPrincipal
@login_required
def editReunion_preguntaOficial(request, dni_pasaporte_alumno,
    curso_academico, id_reunion, dni_pasaporte_asesor,
    id_entrevista_oficial, id_pregunta_oficial):
    # Se obtiene la instancia de la reunion - pregunta oficial.
    instancia_reunion_preguntaOficial = \
        obtenerReunion_preguntaOficial(
        dni_pasaporte_alumno, curso_academico, id_reunion,
        id_entrevista_oficial, id_pregunta_oficial)

    # Si existe se edita.
    if instancia_reunion_preguntaOficial:
        # Se obtiene la instancia de la reunion.
        fecha_reunion = vistasReunion.obtenerReunion(
            dni_pasaporte_alumno, curso_academico, id_reunion).fecha

        # Se carga el formulario para la reunion - pregunta oficial
        # existente.
        form = forms.Reunion_PreguntaOficialForm(
            instance=instancia_reunion_preguntaOficial)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            #Se extraen los valores pasados por el metodo POST.
            respuesta = request.POST['respuesta']

            # Datos necesarios para crear la nueva reunion - pregunta de
            # asesor.
            datos_reunion_preguntaOficial = {
                'dni_pasaporte': dni_pasaporte_alumno,
                'curso_academico': curso_academico,
                'id_reunion': id_reunion,
                'id_entrevista_oficial': id_entrevista_oficial,
                'id_pregunta_oficial': id_pregunta_oficial,
                'respuesta': respuesta}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.Reunion_PreguntaOficialForm(
                datos_reunion_preguntaOficial,
                instance=instancia_reunion_preguntaOficial)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar reuniones - preguntas
                # de asesor.
                return HttpResponseRedirect(
                    reverse('listReunion_preguntaOficial',
                    kwargs={'dni_pasaporte': dni_pasaporte_alumno,
                    'curso_academico': curso_academico,
                    'id_reunion': id_reunion,
                    'orden': 'pregunta_oficial'}))
    # La matricula no existe
    else:
        form = False
        fecha_reunion = ''
    return render_to_response(PATH + 'editReunion_preguntaOficial.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte_alumno,
        'id_reunion': id_reunion,
        'fecha_reunion': fecha_reunion,
        'id_entrevista_oficial': id_entrevista_oficial,
        'id_pregunta_oficial': id_pregunta_oficial})

@checkAdministradorPrincipal
@login_required
def delReunion_preguntaOficial(request, dni_pasaporte_alumno,
    curso_academico, id_reunion, dni_pasaporte_asesor,
    id_entrevista_oficial, id_pregunta_oficial):
    # Se obtiene la instancia de la reunion - pregunta oficial.
    instancia_reunion_preguntaOficial = obtenerReunion_preguntaOficial(
        dni_pasaporte_alumno, curso_academico, id_reunion,
        id_entrevista_oficial, id_pregunta_oficial)

    # Si existe se elimina.
    if instancia_reunion_preguntaOficial:
        instancia_reunion_preguntaOficial.delete()
        # Redirige a la pagina de listar reuniones-preguntas oficiales.
        return HttpResponseRedirect(
            reverse('listReunion_preguntaOficial',
                    kwargs={'dni_pasaporte': dni_pasaporte_alumno,
                    'curso_academico': curso_academico,
                    'id_reunion': id_reunion,
                    'orden': 'pregunta_oficial'}))
    # La reunion - pregunta oficial no existe.
    else:
        error = True
    return render_to_response(PATH + 'delReunion_preguntaOficial.html',
        {'user': request.user, 'error': error})

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
                reverse('selectAsesorCA_Reunion_preguntaOficial',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_Reunion_preguntaOficial',
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
            reverse('selectAsesor_Reunion_preguntaOficial',
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
                reverse('selectAlumno_Reunion_preguntaOficial',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_Reunion_preguntaOficial',
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
            reverse('selectAsesorCA_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': tipo}))

    # Se ha introducido un alumno.
    if request.method == 'POST':

        # Se obtiene el alumno y se valida.
        form = forms.AlumnosDeAsesorForm(
            instancia_asesorCA.codigo_asesorCursoAcademico,
            curso_academico, request.POST)

        # Si es valido se redirige a listar alumnos curso academico.
        if form.is_valid():
            alumno = request.POST['alumno']

            # Se crea una instancia del alumno para pasar el nombre de
            # alumno por argumento.
            instancia_alumnoCA = \
                models.AlumnoCursoAcademico.objects.get(pk=alumno)

            return HttpResponseRedirect(
                reverse('selectReunion_Reunion_preguntaOficial',
                kwargs={'dni_pasaporte':
                instancia_alumnoCA.dni_pasaporte_alumno,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumno_Reunion_preguntaOficial',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

    else:
        form = forms.AlumnosDeAsesorForm(
            codigo_asesorCursoAcademico=
            instancia_asesorCA.codigo_asesorCursoAcademico,
            curso_academico=curso_academico)

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectReunion(request, dni_pasaporte, curso_academico, tipo):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumno_curso_academico.codigo_asesorCursoAcademico

    # Se ha introducido un alumno.
    if request.method == 'POST':
        # Se obtiene el alumno y se valida.
        form = forms.ReunionFormSelect(dni_pasaporte, curso_academico,
            request.POST)

        # Si es valido se redirige.
        if form.is_valid():
            reunion = request.POST['reunion']

            # Obtiene una instancia de la reunion.
            instancia_reunion = models.Reunion.objects.get(pk=reunion)

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse(
                    'selectEntrevistaOficial_Reunion_preguntaOficial',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_reunion': instancia_reunion.id_reunion}))

            else:
                return HttpResponseRedirect(
                    reverse('listReunion_preguntaOficial',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_reunion': instancia_reunion.id_reunion,
                    'orden': 'pregunta_oficial'}))

    else:
        form = forms.ReunionFormSelect(dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico)

    return render_to_response(PATH + 'selectReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectEntrevistaOficial(request, dni_pasaporte, curso_academico,
    id_reunion):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se obtiene la posible reunion.
    instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
        curso_academico, id_reunion)

    # Se comprueba que exista la reunion.
    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumno_curso_academico.codigo_asesorCursoAcademico

    dni_pasaporte_asesor = instancia_asesorCA.dni_pasaporte

    # Se ha introducido un alumno.
    if request.method == 'POST':
        # Se obtiene el alumno y se valida.
        form = forms.PlantillaEntrevistaOficialFormSelect(request.POST)

        # Si es valido se redirige.
        if form.is_valid():
            entrevista_oficial = request.POST['entrevista_oficial']

            # Se crea una instancia de la entrevista oficial.
            instancia_entrevista_oficial = \
                models.PlantillaEntrevistaOficial.objects.get(
                pk=entrevista_oficial)

            return HttpResponseRedirect(
                reverse('selectPreguntaOficial_Reunion_preguntaOficial',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_reunion': id_reunion,
                'id_entrevista_oficial':
                instancia_entrevista_oficial.id_entrevista_oficial}))

    else:
        form = forms.PlantillaEntrevistaOficialFormSelect()

    return render_to_response(PATH + 'selectEntrevistaOficial.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'id_reunion': id_reunion,
        'fecha_reunion': instancia_reunion.fecha})

@checkAdministradorPrincipal
@login_required
def selectPreguntaOficial(request, dni_pasaporte, curso_academico,
    id_reunion, id_entrevista_oficial):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumnoCA = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumnoCA:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se obtiene la instancia de la reunion.
    instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
        curso_academico, id_reunion)

    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se obtiene la instancia de la entrevista oficial.
    instancia_entrevista_oficial = \
        vistasPEO.obtenerPlantillaEntrevistaOficial(
        id_entrevista_oficial)

    if not instancia_entrevista_oficial:
        return HttpResponseRedirect(
            reverse('selectEntrevistaOficial_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_reunion': id_reunion}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumnoCA.codigo_asesorCursoAcademico

    dni_pasaporte_asesor = instancia_asesorCA.dni_pasaporte

    # Se ha introducido un alumno.
    if request.method == 'POST':
        # Se obtiene el alumno y se valida.
        form = forms.PreguntaOficialFormSelect(id_entrevista_oficial,
            request.POST)

        # Si es valido se redirige.
        if form.is_valid():
            pregunta_oficial = request.POST['pregunta_oficial']

            # Se crea una instancia de la pregunta oficial.
            instancia_pregunta_oficial = \
                models.PreguntaOficial.objects.get(
                pk=pregunta_oficial)

            return HttpResponseRedirect(
                reverse('addReunion_preguntaOficial',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'id_reunion': id_reunion,
                'id_entrevista_oficial': id_entrevista_oficial,
                'id_pregunta_oficial':
                instancia_pregunta_oficial.id_pregunta_oficial}))

    else:
        form = forms.PreguntaOficialFormSelect(
            id_entrevista_oficial=id_entrevista_oficial)

    return render_to_response(PATH + 'selectPreguntaOficial.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'id_reunion': id_reunion,
        'fecha_reunion': instancia_reunion.fecha,
        'id_entrevista_oficial': id_entrevista_oficial})

@checkAdministradorPrincipal
@login_required
def listReunion_preguntaOficial(request, dni_pasaporte, curso_academico,
    id_reunion, orden):
    # Se obtiene la posible reunion.
    instancia_reunion = \
        vistasReunion.obtenerReunion(dni_pasaporte, curso_academico,
            id_reunion)

    # Se comprueba que exista la reunion.
    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del alumno curso academico.
    instancia_alumnoCA = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = instancia_alumnoCA.codigo_asesorCursoAcademico

    # Se obtiene una lista con todas las reuniones - pregunta oficiales.
    lista_reuniones_pregunta_oficial = \
        models.ReunionPreguntaOficial.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico,
        id_reunion=id_reunion).order_by('id_pregunta_oficial')

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
            for reunion_pregunta in lista_reuniones_pregunta_oficial:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (
                    unicode(reunion_pregunta.id_entrevista_oficial)
                    + unicode(reunion_pregunta.id_pregunta_oficial) +
                    unicode(reunion_pregunta.respuesta))

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion_pregunta)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones_pregunta_oficial = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_pregunta_oficial':
            lista_reuniones_pregunta_oficial = \
                lista_reuniones_pregunta_oficial.reverse()

    return render_to_response(PATH + 'listReunion_preguntaOficial.html',
        {'user': request.user, 'form': form,
        'lista_reuniones_pregunta_oficial':
        lista_reuniones_pregunta_oficial,
        'busqueda': busqueda,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'id_reunion': id_reunion,
        'fecha_reunion': instancia_reunion.fecha,
        'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaReuniones_preguntaOficial(request, dni_pasaporte,
    curso_academico, id_reunion, busqueda):
    # Se obtiene la posible reunion.
    instancia_reunion = \
        vistasReunion.obtenerReunion(dni_pasaporte, curso_academico,
            id_reunion)

    # Se comprueba que exista la reunion.
    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaOficial',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del alumno curso academico.
    instancia_alumnoCA = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = instancia_alumnoCA.codigo_asesorCursoAcademico

    # Se obtiene una lista con todas las reuniones - pregunta oficial.
    lista_reuniones_pregunta_oficial = \
        models.ReunionPreguntaOficial.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico,
        id_reunion=id_reunion).order_by('id_pregunta_oficial')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
            # la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden con
            # la busqueda.
            for reunion_pregunta in lista_reuniones_pregunta_oficial:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (
                    unicode(reunion_pregunta.id_entrevista_oficial)
                    + unicode(reunion_pregunta.id_pregunta_oficial) +
                    unicode(reunion_pregunta.respuesta))

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion_pregunta)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones_pregunta_oficial = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_reuniones_pregunta_oficial,
        'name': 'reuniones - preguntas oficiales',})
