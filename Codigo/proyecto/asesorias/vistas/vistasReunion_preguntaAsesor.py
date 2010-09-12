from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAlumnoCursoAcademico
from asesorias.vistas import vistasAsesor, vistasAsesorCursoAcademico
from asesorias.vistas import vistasReunion, vistasPreguntaAsesor

PATH = 'asesorias/Reunion_PreguntaAsesor/'

# Comprueba si existe una reunion - pregunta de asesor y, de ser asi, la
# devuelve.
def obtenerReunion_preguntaAsesor(dni_pasaporte_alumno, curso_academico,
    id_reunion, dni_pasaporte_asesor, id_entrevista_asesor,
    id_pregunta_asesor):
    try:
        # Obtiene la instancia de reunion - pregunta de asesor.
        resultado = models.ReunionPreguntaAsesor.objects.get(
            dni_pasaporte_alumno=dni_pasaporte_alumno,
            curso_academico=curso_academico,
            id_reunion=id_reunion,
            dni_pasaporte_asesor=dni_pasaporte_asesor,
            id_entrevista_asesor=id_entrevista_asesor,
            id_pregunta_asesor=id_pregunta_asesor)
    except:
        resultado = False
    return resultado

def addReunion_preguntaAsesor(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        #Se extraen los valores pasados por el metodo POST.
        codigo_reunion = request.POST['reunion']
        codigo_pregunta_asesor = request.POST['pregunta_asesor']
        respuesta = request.POST['respuesta']

        # Se obtiene una instancia de la reunion a traves de su id.
        instancia_reunion = models.Reunion.objects.get(
            pk=codigo_reunion)

        # Se determina dni_pasaporte_alumno, curso_academico e
        # id_reunion para esa reunion.
        dni_pasaporte_alumno = instancia_reunion.dni_pasaporte
        curso_academico = instancia_reunion.curso_academico
        id_reunion = instancia_reunion.id_reunion

        # Se obtiene una instancia de la pregunta de asesor a traves de
        # su id.
        instancia_pregunta_asesor = models.PreguntaAsesor.objects.get(
            pk=codigo_pregunta_asesor)

        # Se determina el dni_pasaporte_asesor, id_entrevista_asesor,
        # id_pregunta_asesor para esa pregunta de asesor.
        dni_pasaporte_asesor = instancia_pregunta_asesor.dni_pasaporte
        id_entrevista_asesor = \
            instancia_pregunta_asesor.id_entrevista_asesor
        id_pregunta_asesor = \
            instancia_pregunta_asesor.id_pregunta_asesor

        # Datos necesarios para crear la nueva reunion - pregunta de
        # asesor.
        datos_reunion_preguntaAsesor = {
            'dni_pasaporte_alumno': dni_pasaporte_alumno,
            'curso_academico': curso_academico,
            'id_reunion': id_reunion,
            'dni_pasaporte_asesor': dni_pasaporte_asesor,
            'id_entrevista_asesor': id_entrevista_asesor,
            'id_pregunta_asesor': id_pregunta_asesor,
            'respuesta': respuesta,
            'reunion': codigo_reunion,
            'pregunta_asesor': codigo_pregunta_asesor}

        # Se obtienen los valores y se valida.
        form = forms.Reunion_PreguntaAsesorForm(
            datos_reunion_preguntaAsesor)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar reuniones - preguntas de
            # asesor.
            return HttpResponseRedirect(
                reverse('listReunion_preguntaAsesor'))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.Reunion_PreguntaAsesorForm()
    return render_to_response(PATH + 'addReunion_preguntaAsesor.html',
        {'form': form})

def editReunion_preguntaAsesor(request, dni_pasaporte_alumno,
    curso_academico, id_reunion, dni_pasaporte_asesor,
    id_entrevista_asesor, id_pregunta_asesor):
    # Se obtiene la instancia de la reunion - pregunta de asesor.
    instancia_reunion_preguntaAsesor = \
        obtenerReunion_preguntaAsesor(
        dni_pasaporte_alumno, curso_academico, id_reunion,
        dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor)
    # Si existe se edita.
    if instancia_reunion_preguntaAsesor:
        # Se carga el formulario para la reunion - pregunta de asesor
        # existente.
        form = forms.Reunion_PreguntaAsesorForm(
            instance=instancia_reunion_preguntaAsesor,
            initial={'reunion':
            vistasReunion.obtenerReunion(dni_pasaporte_alumno,
            curso_academico, id_reunion).codigo_reunion,
            'pregunta_asesor':
            vistasPreguntaAsesor.obtenerPreguntaAsesor(
            dni_pasaporte_asesor, curso_academico, id_entrevista_asesor,
            id_pregunta_asesor).codigo_preguntaAsesor})
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            #Se extraen los valores pasados por el metodo POST.
            codigo_reunion = request.POST['reunion']
            codigo_pregunta_asesor = request.POST['pregunta_asesor']
            respuesta = request.POST['respuesta']

            # Se obtiene una instancia de la reunion a traves de su id.
            instancia_reunion = models.Reunion.objects.get(
                pk=codigo_reunion)

            # Se determina dni_pasaporte_alumno, curso_academico e
            # id_reunion para esa reunion.
            dni_pasaporte_alumno = instancia_reunion.dni_pasaporte
            curso_academico = instancia_reunion.curso_academico
            id_reunion = instancia_reunion.id_reunion

            # Se obtiene una instancia de la pregunta de asesor a traves
            # de su id.
            instancia_pregunta_asesor = \
                models.PreguntaAsesor.objects.get(
                pk=codigo_pregunta_asesor)

            # Se determina el dni_pasaporte_asesor,
            # id_entrevista_asesor, id_pregunta_asesor para esa pregunta
            # de asesor.
            dni_pasaporte_asesor = \
                instancia_pregunta_asesor.dni_pasaporte
            id_entrevista_asesor = \
                instancia_pregunta_asesor.id_entrevista_asesor
            id_pregunta_asesor = \
                instancia_pregunta_asesor.id_pregunta_asesor

            # Datos necesarios para crear la nueva reunion - pregunta de
            # asesor.
            datos_reunion_preguntaAsesor = {
                'dni_pasaporte_alumno': dni_pasaporte_alumno,
                'curso_academico': curso_academico,
                'id_reunion': id_reunion,
                'dni_pasaporte_asesor': dni_pasaporte_asesor,
                'id_entrevista_asesor': id_entrevista_asesor,
                'id_pregunta_asesor': id_pregunta_asesor,
                'respuesta': respuesta,
                'reunion': codigo_reunion,
                'pregunta_asesor': codigo_pregunta_asesor}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.Reunion_PreguntaAsesorForm(
                datos_reunion_preguntaAsesor,
                instance=instancia_reunion_preguntaAsesor)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar reuniones - preguntas
                # de asesor.
                return HttpResponseRedirect(
                    reverse('listReunion_preguntaAsesor'))
    # La matricula no existe
    else:
        form = False
    return render_to_response(PATH + 'editReunion_preguntaAsesor.html',
        {'form': form})

def delReunion_preguntaAsesor(request, dni_pasaporte_alumno,
    curso_academico, id_reunion, dni_pasaporte_asesor,
    id_entrevista_asesor, id_pregunta_asesor):
    # Se obtiene la instancia de la reunion - pregunta de asesor.
    instancia_reunion_preguntaAsesor = obtenerReunion_preguntaAsesor(
        dni_pasaporte_alumno, curso_academico, id_reunion,
        dni_pasaporte_asesor, id_entrevista_asesor, id_pregunta_asesor)

    # Si existe se elimina.
    if instancia_reunion_preguntaAsesor:
        instancia_reunion_preguntaAsesor.delete()
        # Redirige a la pagina de listar reuniones - preguntas de asesor.
        return HttpResponseRedirect(
            reverse('listReunion_preguntaAsesor'))
    # La reunion - pregunta de asesor no existe.
    else:
        error = True
    return render_to_response(PATH + 'delReunion_preguntaAsesor.html',
        {'error': error})

def selectAsesor(request, tipo):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.AsesorFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            asesor = request.POST['asesor']

            return HttpResponseRedirect(
                reverse('selectAsesorCA_Reunion_preguntaAsesor',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_Reunion_preguntaAsesor',
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
            reverse('selectAsesor_Reunion_preguntaAsesor',
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
                reverse('selectAlumno_Reunion_preguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_Reunion_preguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'tipo': tipo}))

    else:
        form = forms.AsesorCursoAcademicoFormSelect(
            dni_pasaporte=dni_pasaporte)

    return render_to_response(PATH + 'selectAsesorCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte, 'tipo': tipo})

def selectAlumno(request, dni_pasaporte, curso_academico, tipo):
    # Se obtiene el posible asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesorCA:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_Reunion_preguntaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'tipo': tipo}))

    # Se ha introducido un alumno.
    if request.method == 'POST':

        # Se obtiene el alumno y se valida.
        form = forms.AlumnosDeAsesorForm(
            instancia_asesorCA.codigo_asesorCursoAcademico,
            request.POST)

        # Si es valido se redirige a listar alumnos curso academico.
        if form.is_valid():
            alumno = request.POST['alumno']

            # Se crea una instancia del alumno para pasar el nombre de
            # alumno por argumento.
            instancia_alumnoCA = \
                models.AlumnoCursoAcademico.objects.get(pk=alumno)

            return HttpResponseRedirect(
                reverse('selectReunion_Reunion_preguntaAsesor',
                kwargs={'dni_pasaporte':
                instancia_alumnoCA.dni_pasaporte_alumno,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumno_Reunion_preguntaAsesor',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

    else:
        form = forms.AlumnosDeAsesorForm(
            codigo_asesorCursoAcademico=
            instancia_asesorCA.codigo_asesorCursoAcademico)

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'tipo': tipo})

def selectReunion(request, dni_pasaporte, curso_academico, tipo):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion_preguntaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumno_curso_academico.codigo_asesorCursoAcademico

    # Se ha introducido un alumno.
    if request.method == 'POST':
        # Se obtiene el alumno y se valida.
        form = forms.ReunionFormSelect(dni_pasaporte,request.POST)

        # Si es valido se redirige.
        if form.is_valid():
            reunion = request.POST['reunion']

            # Obtiene una instancia de la reunion.
            instancia_reunion = models.Reunion.objects.get(pk=reunion)

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addReunion_preguntaAsesor'))

            else:
                return HttpResponseRedirect(
                    reverse('listReunion_preguntaAsesor',
                    kwargs={'dni_pasaporte': dni_pasaporte,
                    'curso_academico': curso_academico,
                    'id_reunion': instancia_reunion.id_reunion,
                    'orden': 'pregunta_asesor'}))

    else:
        form = forms.ReunionFormSelect(dni_pasaporte=dni_pasaporte)

    return render_to_response(PATH + 'selectReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'tipo': tipo})

def listReunion_preguntaAsesor(request, dni_pasaporte, curso_academico,
    id_reunion, orden):
    # Se obtiene la posible reunion.
    instancia_reunion = \
        vistasReunion.obtenerReunion(dni_pasaporte, curso_academico,
            id_reunion)

    # Se comprueba que exista la reunion.
    if not instancia_reunion:
        return HttpResponseRedirect(
            reverse('selectReunion_Reunion_preguntaAsesor',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del alumno curso academico.
    instancia_alumnoCA = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = instancia_alumnoCA.codigo_asesorCursoAcademico

    # Se obtiene una lista con todas las reuniones - pregunta de asesor.
    lista_reuniones_pregunta_de_asesor = \
        models.ReunionPreguntaAsesor.objects.filter(
        dni_pasaporte_alumno=dni_pasaporte,
        curso_academico=curso_academico,
        id_reunion=id_reunion)

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
            for reunion_pregunta in lista_reuniones_pregunta_de_asesor:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(reunion_pregunta.id_pregunta_asesor)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion_pregunta)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones_pregunta_de_asesor = lista_aux

        else:
            busqueda = False
    ## No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_fecha':
            lista_reuniones_pregunta_de_asesor = \
                lista_reuniones_pregunta_de_asesor.reverse()

    return render_to_response(PATH + 'listReunion_preguntaAsesor.html',
        {'user': request.user, 'form': form,
        'lista_reuniones_pregunta_de_asesor':
        lista_reuniones_pregunta_de_asesor,
        'busqueda': busqueda,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'reunion': id_reunion,
        'orden': orden})
