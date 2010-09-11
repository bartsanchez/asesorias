from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAlumno, vistasAlumnoCursoAcademico
from asesorias.vistas import vistasAsesor, vistasAsesorCursoAcademico
from asesorias.utils import vistasPDF

PATH = 'asesorias/Reunion/'

# Comprueba si existe una reunion y, de ser asi, la devuelve.
def obtenerReunion(dni_pasaporte, curso_academico, id_reunion):
    try:
        # Obtiene la reunion.
        resultado = models.Reunion.objects.get(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico,
            id_reunion=id_reunion)
    except:
        resultado = False
    return resultado

# Obtiene una lista con las reuniones de un determinado alumno curso
# academico.
def obtenerReunionesDeAlumnoCursoAcademico(
    instancia_alumno_curso_academico):
    try:
        # Obtiene todas las reuniones que pertenecen a un alumno pasado
        # por argumento.
        resultado = models.Reunion.objects.filter(
            dni_pasaporte=
            instancia_alumno_curso_academico.dni_pasaporte_id,
            curso_academico=
            instancia_alumno_curso_academico.curso_academico)
    except:
        resultado = False
    return resultado

# Obtiene una lista ordenada con los ids de las reuniones de un
# determinado alumno curso academico.
def obtenerListaDeIdsReunionesDeAlumnoCursoAcademico(
    instancia_alumno_curso_academico):
    if instancia_alumno_curso_academico:
        # Se obtiene una lista con las reuniones de un determinado
        # alumno curso academico.
        lista_reuniones_de_alumno = \
            obtenerReunionesDeAlumnoCursoAcademico(
            instancia_alumno_curso_academico)
        # Lista que albergara los ids de las reuniones.
        lista_ids_reuniones_de_alumno = []

        # Si existen reuniones de alumno curso academico extraen sus
        # ids.
        if lista_reuniones_de_alumno:
            # Por cada reunion de alumno curso academico se extrae su id
            # y se inserta en la nueva lista.
            for reunion_de_alumno in lista_reuniones_de_alumno:
                lista_ids_reuniones_de_alumno.append(
                    reunion_de_alumno.id_reunion)
            # Ordena la lista con los ids de las reuniones de menor a
            # mayor.
            lista_ids_reuniones_de_alumno.sort()
        # Resultado sera una lista de ids, o una lista vacia si el
        # alumno curso academico no tiene reuniones.
        resultado = lista_ids_reuniones_de_alumno
    # En el caso de que no exista el alumno curso academico se devuelve
    # False.
    else:
        resultado = False
    return resultado

# Determina el primer id_reunion disponible para un determinado alumno
# curso academico.
def determinarSiguienteIdReunionDeAlumnoCursoAcademico(
    instancia_alumno_curso_academico):
    # Se obtiene una lista ordenada con los ids de las reuniones
    # existentes para el alumno curso academico.
    lista_ids_reuniones_de_alumno = \
        obtenerListaDeIdsReunionesDeAlumnoCursoAcademico(
        instancia_alumno_curso_academico)

    # Inicializamos el contador a 1, que es el primer valor valido para
    # un id.
    contador = 1
    # Recorre el bucle determinando si una posicion se encuentra o no.
    while True:
        # La posicion determinada por contador aparece en la lista, por
        # lo tanto se encuentra la id_reunion para el alumno curso
        # academico.
        if lista_ids_reuniones_de_alumno.count(contador) > 0:
            contador += 1
        # No existe tal id_reunion para el alumno curso academico.
        else:
            break
    return contador

def addReunion(request, dni_pasaporte, curso_academico):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsesorCA_Reunion',
            kwargs={'dni_pasaporte': dni_pasaporte, 'tipo': 'add'}))

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
        id_reunion = \
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
            return HttpResponseRedirect(reverse('listReunion',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'orden': 'fecha'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.ReunionForm()
    return render_to_response(PATH + 'addReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte})

def editReunion(request, dni_pasaporte, curso_academico, id_reunion):
    # Se obtiene la instancia de la reunion.
    instancia_reunion = obtenerReunion(dni_pasaporte, curso_academico,
        id_reunion)
    # Si existe se edita.
    if instancia_reunion:
        # Se crea una instancia del asesor curso academico.
        instancia_asesorCA = \
            vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
            dni_pasaporte,curso_academico).codigo_asesorCursoAcademico

        dni_pasaporte_asesor = instancia_asesorCA.dni_pasaporte

        # Se carga el formulario para la plantilla existente.
        form = forms.ReunionForm(instance=instancia_reunion)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se extraen los valores pasados por el metodo POST.
            fecha = request.POST['fecha']
            tipo = request.POST['tipo']
            comentario_asesor = request.POST['comentario_asesor']
            comentario_alumno = request.POST['comentario_alumno']

            # Se obtiene una instancia del alumno curso academico a
            # traves de su id.
            instancia_alumno_curso_academico = \
                vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
                dni_pasaporte, curso_academico)

            # Se determina el siguiente id_reunion para el alumno curso
            # academico.
            id_reunion = \
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

            # Se actualiza el formulario con la nueva informacion.
            form = forms.ReunionForm(datos_reunion,
                instance=instancia_reunion)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar reuniones.
                return HttpResponseRedirect(reverse('listReunion',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'orden': 'fecha'}))
    # La reunion no existe.
    else:
        form = False
        dni_pasaporte_asesor = ''
    return render_to_response(PATH + 'editReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte_asesor': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'id_reunion': id_reunion})

def delReunion(request, dni_pasaporte, curso_academico, id_reunion):
    # Se obtiene la instancia de la reunion.
    instancia_reunion= obtenerReunion(dni_pasaporte, curso_academico,
        id_reunion)
    # Si existe se elimina.
    if instancia_reunion:
        instancia_reunion.delete()
        # Redirige a la pagina de listar reuniones.
        return HttpResponseRedirect(reverse('listReunion',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'orden': 'fecha'}))
    # La reunion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delReunion.html',
        {'user': request.user, 'error': error})

def selectAsesor(request, tipo):
    # Se ha introducido un asesor.
    if request.method == 'POST':

        # Se obtiene el asesor y se valida.
        form = forms.AsesorFormSelect(request.POST)

        # Si es valido se redirige a listar asesores curso academico.
        if form.is_valid():
            asesor = request.POST['asesor']

            return HttpResponseRedirect(
                reverse('selectAsesorCA_Reunion',
                kwargs={'dni_pasaporte': asesor, 'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesor_Reunion',
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
            reverse('selectAsesor_Reunion',
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
                reverse('selectAlumno_Reunion',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsesorCA_Reunion',
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
            reverse('selectAsesorCA_Reunion',
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


            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addReunion', kwargs={
                    'dni_pasaporte':
                    instancia_alumnoCA.dni_pasaporte_alumno,
                    'curso_academico': curso_academico}))
            else:
                return HttpResponseRedirect(reverse('listReunion',
                kwargs={'dni_pasaporte':
                instancia_alumnoCA.dni_pasaporte_alumno,
                'curso_academico': curso_academico,
                'orden': 'fecha'}))

        else:
            HttpResponseRedirect(
                reverse('selectAlumno_Reunion',
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

def listReunion(request, dni_pasaporte, curso_academico, orden):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion',
            kwargs={'dni_pasaporte': dni_pasaporte,
            'curso_academico': curso_academico,
            'tipo': 'list'}))

    # Se crea una instancia del asesor curso academico.
    instancia_asesorCA = \
        instancia_alumno_curso_academico.codigo_asesorCursoAcademico

    # Se obtiene una lista con todos las reuniones.
    lista_reuniones = models.Reunion.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico).order_by('id_reunion')

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
            for reunion in lista_reuniones:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(reunion.fecha)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones = lista_aux

        else:
            busqueda = False
    ## No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if orden == '_fecha':
            lista_reuniones = lista_reuniones.reverse()

    return render_to_response(PATH + 'listReunion.html',
        {'user': request.user, 'form': form,
        'lista_reuniones': lista_reuniones,
        'busqueda': busqueda,
        'dni_pasaporte_asesor': instancia_asesorCA.dni_pasaporte,
        'curso_academico': curso_academico,
        'dni_pasaporte_alumno': dni_pasaporte,
        'orden': orden})

def generarPDFListaReuniones(request, dni_pasaporte,
    curso_academico, busqueda):
    # Se obtiene el posible alumno_curso_academico.
    instancia_alumno_curso_academico = \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
        dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumno_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAlumnoCursoAcademico_Reunion',
            kwargs={'dni_pasaporte': dni_pasaporte}))

    # Se obtiene una lista con todos las reuniones.
    lista_reuniones = models.Reunion.objects.filter(
        dni_pasaporte=dni_pasaporte,
        curso_academico=curso_academico).order_by('id_reunion')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        lista_reuniones = lista_reuniones.filter(
            fecha__contains=busqueda)

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_reuniones,
        'name': 'reuniones',})
