from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias.vistas.AdministradorPrincipal import \
    vistasPreguntaOficial
from asesorias.vistas.AdministradorPrincipal import vistasReunion
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

def selectAlumno(request, curso_academico):
    dni_pasaporte = unicode(request.user)

    # Se obtiene el posible asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el asesor curso academico.
    if not instancia_asesorCA:
        return HttpResponseRedirect(
            reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

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
                reverse('addReunion_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'dni_pasaporte':
                    instancia_alumnoCA.dni_pasaporte_alumno}))

        else:
            return HttpResponseRedirect(
                reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

    else:
        form = forms.AlumnosDeAsesorForm(
            codigo_asesorCursoAcademico=
            instancia_asesorCA.codigo_asesorCursoAcademico,
            curso_academico=curso_academico)

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

def addReunion(request, curso_academico, dni_pasaporte):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('listReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumno_curso_academico.codigo_asesorCursoAcademico

    dni_pasaporte_asesor = instancia_asesorCA.dni_pasaporte

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        fecha = request.POST['fecha']
        tipo = request.POST['tipo']
        comentario_asesor = request.POST['comentario_asesor']
        comentario_alumno = request.POST['comentario_alumno']

        # Se determina el siguiente id_reunion para el alumno curso
        # academico.
        id_reunion = vistasReunion.\
            determinarSiguienteIdReunionDeAlumnoCursoAcademico(
            instancia_alumno_curso_academico)

        # Datos necesarios para crear la nueva plantilla.
        datos_reunion = {'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'id_reunion': id_reunion,
            'fecha': fecha,
            'tipo': tipo,
            'comentario_asesor': comentario_asesor,
            'comentario_alumno': comentario_alumno}

        # Se obtienen los valores y se valida.
        form = forms.ReunionForm(datos_reunion)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar reuniones.
            return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.ReunionForm()
    return render_to_response(PATH + 'addReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte})

def delReunion(request, curso_academico, dni_pasaporte, id_reunion):
    # Se obtiene la instancia de la reunion.
    instancia_reunion= vistasReunion.obtenerReunion(
        dni_pasaporte, curso_academico, id_reunion)
    # Si existe se elimina.
    if instancia_reunion:
        instancia_reunion.borrar()
        # Redirige a la pagina de listar reuniones.
        return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))
    # La reunion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delReunion.html',
        {'user': request.user, 'error': error})

def listReunion(request, curso_academico, orden):
    dni_pasaporte = unicode(request.user)

    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
         # Se obtiene una lista con todos los alumnos.
        lista_alumnosCA = models.AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico =
            instancia_asesorCA.codigo_asesorCursoAcademico).values_list(
            'dni_pasaporte_alumno', flat=True)

        # Se crea una lista con todas las reuniones del asesor.
        lista_reuniones = models.Reunion.objects.filter(
            dni_pasaporte__in=lista_alumnosCA,
            curso_academico=curso_academico).order_by('fecha')

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
            for reunion in lista_reuniones:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(reunion.fecha)

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if (orden == '_fecha'):
            lista_reuniones = reversed(lista_reuniones)

    return render_to_response(PATH + 'listReunion.html',
        {'user': request.user, 'form': form,
        'lista_reuniones': lista_reuniones,
        'busqueda': busqueda,
        'orden': orden,
        'curso_academico': curso_academico})

def showReunion(request, curso_academico, dni_pasaporte, id_reunion):
    dni_pasaporte_asesor = unicode(request.user)
    form = False
    instancia_reunion = False
    preguntas_reunion = False
    preguntas_oficiales = False
    preguntas_asesor = False

    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            form = forms.ReunionForm(instance=instancia_reunion)
            preguntas_oficiales = \
                models.ReunionPreguntaOficial.objects.filter(
                dni_pasaporte=dni_pasaporte,
                curso_academico=curso_academico,
                id_reunion=id_reunion)

            preguntas_asesor = \
                models.ReunionPreguntaAsesor.objects.filter(
                dni_pasaporte_alumno=dni_pasaporte,
                curso_academico=curso_academico,
                id_reunion=id_reunion)

            if (preguntas_oficiales) or (preguntas_asesor):
                preguntas_reunion = True

    return render_to_response(PATH + 'showReunion.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'reunion': instancia_reunion,
        'preguntas_reunion': preguntas_reunion,
        'preguntas_oficiales': preguntas_oficiales,
        'preguntas_asesor': preguntas_asesor})

def addPlantillaAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista, tipo):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            plantillas_oficiales = \
                models.PlantillaEntrevistaOficial.objects.order_by(
                'id_entrevista_oficial')

            plantillas_asesor = \
                models.PlantillaEntrevistaAsesor.objects.filter(
                curso_academico=curso_academico,
                dni_pasaporte=request.user)

            if (id_entrevista and tipo):
                if tipo == 'oficial':
                    lista_preguntas = \
                        models.PreguntaOficial.objects.filter(
                        id_entrevista_oficial=id_entrevista
                        ).order_by('id_pregunta_oficial')
                elif tipo == 'asesor':
                    lista_preguntas = \
                        models.PreguntaAsesor.objects.filter(
                        curso_academico=curso_academico,
                        dni_pasaporte=request.user,
                        id_entrevista_asesor=id_entrevista
                        ).order_by('id_pregunta_asesor')
                else:
                    lista_preguntas = False
                    tipo = False
            else:
                lista_preguntas = False
                tipo = False
        else:
            return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))
    else:
        return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

    return render_to_response(PATH + 'addPlantillaAReunion.html',
        {'user': request.user,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'reunion': instancia_reunion,
        'plantillas_oficiales': plantillas_oficiales,
        'plantillas_asesor': plantillas_asesor,
        'lista_preguntas': lista_preguntas,
        'tipo': tipo})

def addPlantillaOficialAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_oficial):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            lista_preguntas_oficiales = \
                models.PreguntaOficial.objects.filter(
                id_entrevista_oficial=id_entrevista_oficial).order_by(
                'id_pregunta_oficial')

            for pregunta in lista_preguntas_oficiales:
                instancia_nueva_pregunta = \
                    models.ReunionPreguntaOficial.objects.create(
                    dni_pasaporte=dni_pasaporte,
                    curso_academico=curso_academico,
                    id_reunion=id_reunion,
                    id_entrevista_oficial=id_entrevista_oficial,
                    id_pregunta_oficial=pregunta.id_pregunta_oficial,
                    respuesta='-')
                instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))

def addPlantillaAsesorAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_asesor):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            lista_preguntas_asesor = \
                models.PreguntaAsesor.objects.filter(
                curso_academico=curso_academico,
                dni_pasaporte=unicode(request.user),
                id_entrevista_asesor=id_entrevista_asesor).order_by(
                'id_pregunta_asesor')

            for pregunta in lista_preguntas_asesor:
                instancia_nueva_pregunta = \
                    models.ReunionPreguntaAsesor.objects.create(
                    dni_pasaporte_alumno=dni_pasaporte,
                    dni_pasaporte_asesor=unicode(request.user),
                    curso_academico=curso_academico,
                    id_reunion=id_reunion,
                    id_entrevista_asesor=id_entrevista_asesor,
                    id_pregunta_asesor=pregunta.id_pregunta_asesor,
                    respuesta='-')
                instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))

def addPreguntaAReunion(request, curso_academico, dni_pasaporte,
    id_reunion):
    preguntas_oficiales = False
    preguntas_asesor = False

    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            preguntas_oficiales = \
                models.PreguntaOficial.objects.order_by(
                'id_entrevista_oficial', 'id_pregunta_oficial')

        else:
            return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))
    else:
        return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

    return render_to_response(PATH + 'addPreguntaAReunion.html',
        {'user': request.user,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'reunion': instancia_reunion,
        'preguntas_oficiales': preguntas_oficiales,
        'preguntas_asesor': preguntas_asesor})

def addPreguntaOficialAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_oficial, id_pregunta_oficial):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            instancia_pregunta_oficial = \
                vistasPreguntaOficial.obtenerPreguntaOficial(
                id_entrevista_oficial, id_pregunta_oficial)

            instancia_nueva_pregunta = \
                models.ReunionPreguntaOficial.objects.create(
                dni_pasaporte=dni_pasaporte,
                curso_academico=curso_academico,
                id_reunion=id_reunion,
                id_entrevista_oficial=id_entrevista_oficial,
                id_pregunta_oficial=id_pregunta_oficial,
                respuesta='-')
            instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))

def delPreguntaOficialAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_oficial, id_pregunta_oficial):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            instancia_reunion_pregunta_oficial = \
                models.ReunionPreguntaOficial.objects.get(
                dni_pasaporte=dni_pasaporte,
                curso_academico=curso_academico,
                id_reunion=id_reunion,
                id_entrevista_oficial=id_entrevista_oficial,
                id_pregunta_oficial=id_pregunta_oficial)
            instancia_reunion_pregunta_oficial.delete()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))

def delPreguntaAsesorAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_asesor, id_pregunta_asesor):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            instancia_reunion_pregunta_asesor = \
                models.ReunionPreguntaAsesor.objects.get(
                dni_pasaporte_alumno=dni_pasaporte,
                dni_pasaporte_asesor=unicode(request.user),
                curso_academico=curso_academico,
                id_reunion=id_reunion,
                id_entrevista_asesor=id_entrevista_asesor,
                id_pregunta_asesor=id_pregunta_asesor)
            instancia_reunion_pregunta_asesor.delete()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))
