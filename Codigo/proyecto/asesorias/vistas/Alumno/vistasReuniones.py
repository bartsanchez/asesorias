from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico
from asesorias.vistas.AdministradorPrincipal import vistasReunion
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
