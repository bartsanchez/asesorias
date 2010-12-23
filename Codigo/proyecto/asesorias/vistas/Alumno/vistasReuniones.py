from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico
from asesorias.vistas.AdministradorPrincipal import vistasReunion
from asesorias.vistas.AdministradorPrincipal import \
    vistasReunion_preguntaAsesor as vistasRPA
from asesorias.vistas.AdministradorPrincipal import \
    vistasReunion_preguntaOficial as vistasRPO
from asesorias import models, forms

PATH = 'asesorias/UsuarioAlumno/'

def listReunion(request, curso_academico, orden):
    user = unicode(request.user)

    # Se crea una lista con todas las reuniones individuales del
    # asesor.
    lista_reuniones = models.Reunion.objects.filter(
        dni_pasaporte=user,
        curso_academico=curso_academico).order_by('fecha')

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
            lista_reuniones = \
                reversed(lista_reuniones)

    return render_to_response(PATH + 'listReunion.html',
        {'user': request.user, 'form': form,
        'lista_reuniones': lista_reuniones,
        'busqueda': busqueda,
        'orden': orden,
        'curso_academico': curso_academico})

def showReunion(request, curso_academico, id_reunion):
    user = unicode(request.user)

    instancia_alumno = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(user,
        curso_academico)

    if instancia_alumno:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(user,
            curso_academico, id_reunion)

        if instancia_reunion:
            preguntas_oficiales = \
                models.ReunionPreguntaOficial.objects.filter(
                dni_pasaporte=user,
                curso_academico=curso_academico,
                id_reunion=id_reunion)

            preguntas_asesor = \
                models.ReunionPreguntaAsesor.objects.filter(
                dni_pasaporte_alumno=user,
                curso_academico=curso_academico,
                id_reunion=id_reunion)

            if (preguntas_oficiales) or (preguntas_asesor):
                preguntas_reunion = True
            else:
                preguntas_reunion = False
        else:
            # Redirige a la pagina de listar reuniones.
            return HttpResponseRedirect(reverse('listReunion_Alumno',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))
    else:
        # Redirige a la pagina de listar reuniones.
        return HttpResponseRedirect(reverse('listReunion_Alumno',
            kwargs={'curso_academico': curso_academico,
            'orden': 'fecha'}))

    return render_to_response(PATH + 'showReunion.html',
        {'user': request.user,
        'curso_academico': curso_academico,
        'reunion': instancia_reunion,
        'preguntas_reunion': preguntas_reunion,
        'preguntas_oficiales': preguntas_oficiales,
        'preguntas_asesor': preguntas_asesor})

def editRespuestaAsesor(request, curso_academico, id_reunion,
    id_entrevista_asesor, id_pregunta_asesor):
    user = unicode(request.user)

    instancia_alumno = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(user,
        curso_academico)

    if instancia_alumno:
        # Se obtiene el dni del asesor.
        dni_pasaporte_asesor = \
            instancia_alumno.dni_pasaporte_asesor

        # Se obtiene una instancia de la reunion.
        instancia_reunion_preguntaAsesor = \
            vistasRPA.obtenerReunion_preguntaAsesor(
            user, curso_academico, id_reunion, dni_pasaporte_asesor,
            id_entrevista_asesor, id_pregunta_asesor)

        # Si existe se buscan las preguntas.
        if instancia_reunion_preguntaAsesor:
            # Se obtiene la instancia de la reunion.
            fecha_reunion = vistasReunion.obtenerReunion(
                user, curso_academico, id_reunion).fecha

            # Se carga el formulario para la reunion - pregunta oficial
            # existente.
            form = forms.Reunion_PreguntaAsesorForm(
                instance=instancia_reunion_preguntaAsesor)
            # Se ha modificado el formulario original.
            if request.method == 'POST':
                #Se extraen los valores pasados por el metodo POST.
                respuesta = request.POST['respuesta']

                # Datos necesarios para crear la nueva reunion -
                # pregunta de asesor.
                datos_reunion_preguntaAsesor = {
                    'dni_pasaporte_alumno': user,
                    'curso_academico': curso_academico,
                    'dni_pasaporte_asesor': dni_pasaporte_asesor,
                    'id_reunion': id_reunion,
                    'id_entrevista_asesor': id_entrevista_asesor,
                    'id_pregunta_asesor': id_pregunta_asesor,
                    'respuesta': respuesta}

                # Se actualiza el formulario con la nueva informacion.
                form = forms.Reunion_PreguntaAsesorForm(
                    datos_reunion_preguntaAsesor,
                    instance=instancia_reunion_preguntaAsesor)

                # Si es valido se guarda.
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        reverse('showReunion_Alumno',
                        kwargs={'curso_academico': curso_academico,
                        'id_reunion': id_reunion}))
        else:
            form = False
            fecha_reunion = ''

    return render_to_response(PATH + 'editReunion_pregunta.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'id_reunion': id_reunion,
        'fecha_reunion': fecha_reunion})

def editRespuestaOficial(request, curso_academico, id_reunion,
    id_entrevista_oficial, id_pregunta_oficial):
    user = unicode(request.user)

    instancia_alumno = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(user,
        curso_academico)

    if instancia_alumno:
        # Se obtiene el dni del asesor.
        dni_pasaporte_asesor = \
            instancia_alumno.dni_pasaporte_asesor

        # Se obtiene la instancia de la reunion - pregunta oficial.
        instancia_reunion_preguntaOficial = \
            vistasRPO.obtenerReunion_preguntaOficial(
            user, curso_academico, id_reunion,
            id_entrevista_oficial, id_pregunta_oficial)

        # Si existe se buscan las preguntas.
        if instancia_reunion_preguntaOficial:
            # Se obtiene la instancia de la reunion.
            fecha_reunion = vistasReunion.obtenerReunion(
                user, curso_academico, id_reunion).fecha

            # Se carga el formulario para la reunion - pregunta oficial
            # existente.
            form = forms.Reunion_PreguntaOficialForm(
                instance=instancia_reunion_preguntaOficial)
            # Se ha modificado el formulario original.
            if request.method == 'POST':
                #Se extraen los valores pasados por el metodo POST.
                respuesta = request.POST['respuesta']

                # Datos necesarios para crear la nueva reunion -
                #pregunta de asesor.
                datos_reunion_preguntaOficial = {
                    'dni_pasaporte': user,
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
                    return HttpResponseRedirect(
                        reverse('showReunion_Alumno',
                        kwargs={'curso_academico': curso_academico,
                        'id_reunion': id_reunion}))
        else:
            form = False
            fecha_reunion = ''

    return render_to_response(PATH + 'editReunion_pregunta.html',
        {'user': request.user, 'form': form,
        'curso_academico': curso_academico,
        'id_reunion': id_reunion,
        'fecha_reunion': fecha_reunion})
