from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

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
            curso_academico=curso_academico)

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
