from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAlumno, vistasAlumnoCursoAcademico

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
            reverse('selectAlumnoCursoAcademico_Reunion',
            kwargs={'dni_pasaporte': dni_pasaporte}))

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
                'curso_academico': curso_academico}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.ReunionForm()
    return render_to_response(PATH + 'addReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

def editReunion(request, dni_pasaporte, curso_academico, id_reunion):
    # Se obtiene la instancia de la reunion.
    instancia_reunion = obtenerReunion(dni_pasaporte, curso_academico,
        id_reunion)
    # Si existe se edita.
    if instancia_reunion:
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
                'curso_academico': curso_academico}))
    # La reunion no existe.
    else:
        form = False
    return render_to_response(PATH + 'editReunion.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
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
                'curso_academico': curso_academico}))
    # La reunion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delReunion.html',
        {'user': request.user, 'error': error})

def selectAlumno(request):
    # Se ha introducido un alumno.
    if request.method == 'POST':

        # Se obtiene el alumno y se valida.
        form = forms.AlumnoFormSelect(request.POST)

        # Si es valido se redirige a seleccionar curso academico.
        if form.is_valid():
            alumno = request.POST['alumno']

            return HttpResponseRedirect(
                reverse('selectAlumnoCursoAcademico_Reunion',
                kwargs={'dni_pasaporte': alumno}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumno_Reunion'))

    else:
        form = forms.AlumnoFormSelect()

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form})

def selectAlumnoCursoAcademico(request, dni_pasaporte):
    # Se obtiene el posible alumno.
    instancia_alumno = vistasAlumno.obtenerAlumno(dni_pasaporte)

    # Se comprueba que exista el alumno.
    if not instancia_alumno:
        return HttpResponseRedirect(
            reverse('selectAlumno_Reunion'))

    # Se ha introducido un alumno curso academico.
    if request.method == 'POST':
        # Se obtiene el alumno curso academico y se valida.
        form = forms.AlumnoCursoAcademico2FormSelect(dni_pasaporte,
            request.POST)

        # Si es valido se redirige a listar matriculas.
        if form.is_valid():
            alumno_curso_academico = \
                request.POST['alumno_curso_academico']

            curso_academico = models.AlumnoCursoAcademico.objects.get(
                pk=alumno_curso_academico).curso_academico

            return HttpResponseRedirect(
                reverse('listReunion',
                kwargs={'dni_pasaporte': dni_pasaporte,
                'curso_academico': curso_academico}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumnoCursoAcademico_Reunion',
                kwargs={'dni_pasaporte': dni_pasaporte}))

    else:
        form = forms.AlumnoCursoAcademico2FormSelect(
            dni_pasaporte=dni_pasaporte)

    return render_to_response(PATH + 'selectAlumnoCursoAcademico.html',
        {'user': request.user, 'form': form,
        'dni_pasaporte': dni_pasaporte})

def listReunion(request, dni_pasaporte, curso_academico):
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
    if request.method == 'POST':
        # Se obtienen los valores y se valida.
        form = forms.SearchForm(request.POST)
        ## Si es valido se realiza la busqueda.
        #if form.is_valid():
            #busqueda = request.POST['busqueda']

            ## Se crea una lista auxiliar que albergara el resultado de
            ## la busqueda.
            #lista_aux = []

            ## Se recorren los elementos determinando si coinciden con
            ## la busqueda.
            #for matricula in lista_matriculas:
                ## Se crea una cadena auxiliar para examinar si se
                ## encuentra el resultado de la busqueda.
                #cadena = (unicode(matricula.determinarNombreCentro()) +
                    #unicode(matricula.determinarNombreTitulacion()) +
                    #unicode(matricula.determinarPlanEstudios()) +
                    #unicode(matricula.determinarNombreAsignatura()))

                ## Si se encuentra la busqueda el elemento se incluye en
                ## la lista auxiliar.
                #if cadena.find(busqueda) >= 0:
                    #lista_aux.append(matricula)

            ## La lista final a devolver sera la lista auxiliar.
            #lista_matriculas = lista_aux

        #else:
            #busqueda = False
    ## No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

    return render_to_response(PATH + 'listReunion.html',
        {'user': request.user, 'form': form,
        'lista_reuniones': lista_reuniones,
        'busqueda': busqueda,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})
