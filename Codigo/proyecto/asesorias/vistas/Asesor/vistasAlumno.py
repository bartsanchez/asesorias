from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico

PATH = 'asesorias/UsuarioAsesor/'

def showAlumnos(request):
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), '2010')

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene una lista con todos los alumnos.
        lista_alumnosCA = models.AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico =
            instancia_asesorCA.codigo_asesorCursoAcademico).order_by(
            'dni_pasaporte_alumno')
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
                cadena = unicode(alumno.dni_pasaporte_alumno)

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

    return render_to_response(PATH + 'showAlumnos.html',
        {'user': request.user, 'form': form,
        'lista_alumnosCA': lista_alumnosCA,
        'busqueda': busqueda})
