from datetime import date
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
from asesorias.vistas.AdministradorPrincipal import \
    vistasPreguntaAsesor
from asesorias.vistas.AdministradorPrincipal import \
    vistasReunion_preguntaAsesor as vistasRPA
from asesorias.vistas.AdministradorPrincipal import \
    vistasReunion_preguntaOficial as vistasRPO
from asesorias.vistas.AdministradorPrincipal import vistasReunion
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

def determinarAlumnosReunion(dni_pasaporte, curso_academico, fecha):
    lista_participantes = []
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    if instancia_asesorCA:
        lista_alumnos = \
        instancia_asesorCA.determinarAlumnos().values_list(
        'dni_pasaporte_alumno', flat=True)

        # Se obtienen todos los alumnos participantes de la reunion.
        for alumno in lista_alumnos:
            lista_reuniones = models.Reunion.objects.filter(
                dni_pasaporte=alumno,
                curso_academico=curso_academico,
                fecha=fecha,
                tipo='GRU')

            if lista_reuniones:
                instancia_alumno = \
                    vistasAlumnoCursoAcademico.\
                    obtenerAlumnoCursoAcademico(alumno,
                    curso_academico)
                lista_participantes.append(instancia_alumno)

    return lista_participantes

def determinarReunionesGrupales(dni_pasaporte, curso_academico, fecha):
    lista_reunion_grupal = []
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        dni_pasaporte, curso_academico)

    if instancia_asesorCA:
        lista_alumnos = \
        instancia_asesorCA.determinarAlumnos().values_list(
        'dni_pasaporte_alumno', flat=True)

        # Se obtienen todos los alumnos participantes de la reunion.
        for alumno in lista_alumnos:
            lista_reuniones = models.Reunion.objects.filter(
                dni_pasaporte=alumno,
                curso_academico=curso_academico,
                fecha=fecha,
                tipo='GRU')

            if lista_reuniones:
                for reunion in lista_reuniones:
                    instancia_reunion = \
                        vistasReunion.\
                        obtenerReunion(alumno,
                        curso_academico,
                        reunion.id_reunion)
                    lista_reunion_grupal.append(instancia_reunion)

    return lista_reunion_grupal

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
        {'user': dni_pasaporte, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico})

def addReunionGrupal(request, curso_academico, lista_alumnos):
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

    # La lista de alumnos no esta vacia.
    if len(lista_alumnos)>0:

        # Descompone los dnis de los alumnos que participan en la
        # reunion.
        lista_aux = lista_alumnos.rsplit('&')
        lista_aux.pop()
        lista_participantes = []

        # Por cada argumento pasado se intenta crear una instancia
        # del alumno.
        for alumno in lista_aux:
            instancia_alumno = \
                vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
                alumno, curso_academico)
            if instancia_alumno:
                if (instancia_alumno.codigo_asesorCursoAcademico_id ==
                    instancia_asesorCA.codigo_asesorCursoAcademico):
                        lista_participantes.append(instancia_alumno)
                else:
                    return HttpResponseRedirect(
                        reverse('addReunionGrupal_Asesor',
                            kwargs={'curso_academico': curso_academico,
                            'lista_alumnos': ''}))
            else:
                return HttpResponseRedirect(
                    reverse('addReunionGrupal_Asesor',
                        kwargs={'curso_academico': curso_academico,
                        'lista_alumnos': ''}))
    else:
        lista_participantes = False

    # Se obtiene la lista de alumnos disponible.
    lista_disponibles = models.AlumnoCursoAcademico.objects.filter(
        codigo_asesorCursoAcademico=
        instancia_asesorCA.codigo_asesorCursoAcademico,
        curso_academico=curso_academico)

    # Se convierten en lista en vez de queryset
    lista_aux = []
    for disponible in lista_disponibles:
        lista_aux.append(disponible)
    lista_disponibles = lista_aux

    # Se eliminan de los disponibles los ya participantes.
    if lista_participantes:
        for participante in lista_participantes:
            for disponible in lista_disponibles:
                if participante == disponible:
                    lista_disponibles.remove(disponible)

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        # Se extraen los valores pasados por el metodo POST.
        fecha_day = request.POST['fecha_day']
        fecha_month = request.POST['fecha_month']
        fecha_year = request.POST['fecha_year']

        if (fecha_day=='0' or fecha_month=='0' or fecha_year=='0'):
            return HttpResponseRedirect(
                reverse('addReunionGrupal_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'lista_alumnos': ''}))

        # Comprueba que la fecha sea correcta.
        try:
            fecha = date(int(fecha_year), int(fecha_month),
                int(fecha_day))
        except:
           return HttpResponseRedirect(
                reverse('addReunionGrupal_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'lista_alumnos': lista_alumnos}))

        tipo = 'GRU'
        comentario_asesor = request.POST['comentario_asesor']
        comentario_alumno = request.POST['comentario_alumno']

        if not lista_participantes:
            return HttpResponseRedirect(
                    reverse('addReunionGrupal_Asesor',
                        kwargs={'curso_academico': curso_academico,
                        'lista_alumnos': ''}))

        for alumno in lista_participantes:
            # Se determina el siguiente id_reunion para el alumno curso
            # academico.
            id_reunion = vistasReunion.\
                determinarSiguienteIdReunionDeAlumnoCursoAcademico(
                alumno)

            # Datos necesarios para crear la nueva plantilla.
            datos_reunion = {
                'dni_pasaporte': alumno.dni_pasaporte_alumno,
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
            else:
                return HttpResponseRedirect(
                    reverse('addReunionGrupal_Asesor',
                        kwargs={'curso_academico': curso_academico,
                        'lista_alumnos': ''}))

        return HttpResponseRedirect(
                    reverse('listReunion_Asesor',kwargs={
                    'curso_academico': curso_academico,
                    'orden': 'fecha'}))

    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.ReunionForm()

    return render_to_response(PATH + 'addReunionGrupal.html',
        {'user': dni_pasaporte, 'form': form,
        'dni_pasaporte': dni_pasaporte,
        'curso_academico': curso_academico,
        'lista_alumnos': lista_alumnos,
        'lista_participantes': lista_participantes,
        'lista_disponibles': lista_disponibles})

def delReunionGrupal(request, curso_academico, fecha):
    # Si existen, se eliminan todas las reuiones grupales del asesor
    # para tal curso academico y fecha.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
        unicode(request.user), curso_academico)

    lista_alumnos = \
        instancia_asesorCA.determinarAlumnos().values_list(
        'dni_pasaporte_alumno', flat=True)

    if lista_alumnos:
        error = False
        for dni in lista_alumnos:
            reuniones = models.Reunion.objects.filter(
                dni_pasaporte=dni,
                curso_academico= curso_academico,
                fecha=fecha,
                tipo='GRU')
            if reuniones:
                for reunion in reuniones:
                    reunion.borrar()
        return HttpResponseRedirect(
            reverse('listReunion_Asesor',kwargs={
            'curso_academico': curso_academico,
            'orden': 'fecha'}))
    else:
        error = True

    return render_to_response(PATH + 'delReunion.html',
        {'user': request.user, 'error': error,
        'curso_academico': curso_academico, 'fecha': fecha})

def addAlumnoAReunionGrupal(request, curso_academico, lista_alumnos,
    dni_pasaporte):
    # Se inserta el alumno a la reunion.
    lista_alumnos += dni_pasaporte + '&'
    return HttpResponseRedirect(reverse('addReunionGrupal_Asesor',
        kwargs={'curso_academico': curso_academico,
        'lista_alumnos': lista_alumnos}))

def delAlumnoAReunionGrupal(request, curso_academico, lista_alumnos,
    dni_pasaporte):
    # Se busca el alumno para borrarlo de la reunion.
    if not (lista_alumnos.find(dni_pasaporte)<0):
        lista_alumnos = lista_alumnos.replace(dni_pasaporte + '&', '')
    return HttpResponseRedirect(reverse('addReunionGrupal_Asesor',
        kwargs={'curso_academico': curso_academico,
        'lista_alumnos': lista_alumnos}))

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
        fecha_day = request.POST['fecha_day']
        fecha_month = request.POST['fecha_month']
        fecha_year = request.POST['fecha_year']

        if (fecha_day=='0' or fecha_month=='0' or fecha_year=='0'):
            return HttpResponseRedirect(
                reverse('addReunion_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'dni_pasaporte': dni_pasaporte}))

        # Comprueba que la fecha sea correcta.
        try:
            fecha = date(int(fecha_year), int(fecha_month),
                int(fecha_day))
        except:
           return HttpResponseRedirect(
                reverse('addReunion_Asesor',
                    kwargs={'curso_academico': curso_academico,
                    'dni_pasaporte': dni_pasaporte}))

        tipo = 'IND'
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
        {'user': request.user, 'error': error,
        'curso_academico': curso_academico})

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

        # Se crea una lista con todas las reuniones individuales del
        # asesor.
        lista_reuniones_individuales = models.Reunion.objects.filter(
            dni_pasaporte__in=lista_alumnosCA,
            curso_academico=curso_academico,
            tipo='IND').order_by('fecha')

        # Se crea una lista con todas las reuniones grupales del asesor.
        lista_reuniones_grupales = models.Reunion.objects.filter(
            dni_pasaporte__in=lista_alumnosCA,
            curso_academico=curso_academico,
            tipo='GRU').values_list('fecha', flat=True).distinct()

    # El asesor aun no presta asesoria en este curso academico.
    else:
        lista_alumnosCA = ''
        lista_reuniones_individuales = ''
        lista_reuniones_grupales = ''

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
            for reunion in lista_reuniones_individuales:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = (unicode(reunion.fecha)
                    + unicode(reunion.determinarNombreAlumno())
                    + unicode(reunion.determinarApellidosAlumno()))

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones_individuales = lista_aux

            # Se crea una lista auxiliar que albergara el resultado
            # de la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden
            # con la busqueda.
            for reunion in lista_reuniones_grupales:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(reunion)

                # Si se encuentra la busqueda el elemento se incluye
                # en la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(reunion)

            # La lista final a devolver sera la lista auxiliar.
            lista_reuniones_grupales = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        if (orden == '_fecha'):
            lista_reuniones_individuales = \
                reversed(lista_reuniones_individuales)
            lista_reuniones_grupales = \
                reversed(lista_reuniones_grupales)

    return render_to_response(PATH + 'listReunion.html',
        {'user': request.user, 'form': form,
        'lista_reuniones_individuales': lista_reuniones_individuales,
        'lista_reuniones_grupales': lista_reuniones_grupales,
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
        {'user': request.user,
        'curso_academico': curso_academico,
        'reunion': instancia_reunion,
        'preguntas_reunion': preguntas_reunion,
        'preguntas_oficiales': preguntas_oficiales,
        'preguntas_asesor': preguntas_asesor})

def showReunionGrupal(request, curso_academico, fecha):
    dni_pasaporte_asesor = unicode(request.user)
    preguntas_reunion = False

    lista_participantes = determinarAlumnosReunion(dni_pasaporte_asesor,
        curso_academico, fecha)

    if lista_participantes:
        lista_reuniones = determinarReunionesGrupales(
            dni_pasaporte_asesor, curso_academico, fecha)

        if lista_reuniones:
            instancia_primera_reunion = lista_reuniones[0]

            # Obtiene las preguntas de la reunion grupal.
            preguntas_oficiales = \
                models.ReunionPreguntaOficial.objects.filter(
                    dni_pasaporte=
                    instancia_primera_reunion.dni_pasaporte,
                    curso_academico=curso_academico,
                    id_reunion=instancia_primera_reunion.id_reunion)

            preguntas_asesor = \
                models.ReunionPreguntaAsesor.objects.filter(
                    dni_pasaporte_alumno=
                    instancia_primera_reunion.dni_pasaporte,
                    curso_academico=curso_academico,
                    id_reunion=instancia_primera_reunion.id_reunion)

            if (preguntas_oficiales) or (preguntas_asesor):
                preguntas_reunion = True
    else:
        return HttpResponseRedirect(reverse('listReunion_Asesor',
                kwargs={'curso_academico': curso_academico,
                'orden': 'fecha'}))

    return render_to_response(PATH + 'showReunionGrupal.html',
        {'user': dni_pasaporte_asesor,
        'curso_academico': curso_academico,
        'fecha': fecha,
        'lista_participantes': lista_participantes,
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
                dni_pasaporte=unicode(request.user))

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
                        dni_pasaporte=unicode(request.user),
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

def addPlantillaAReunionGrupal(request, curso_academico, fecha,
    id_entrevista, tipo):
    dni_pasaporte_asesor = unicode(request.user)
    # Se obtienen los participantes de la reunion grupal.
    lista_participantes = determinarAlumnosReunion(dni_pasaporte_asesor,
        curso_academico, fecha)

    if lista_participantes:
        instancia_reunion = models.Reunion.objects.filter(
            dni_pasaporte=lista_participantes[0].dni_pasaporte_alumno,
            curso_academico=curso_academico,
            tipo='GRU',
            fecha=fecha)

        plantillas_oficiales = \
            models.PlantillaEntrevistaOficial.objects.order_by(
            'id_entrevista_oficial')

        plantillas_asesor = \
            models.PlantillaEntrevistaAsesor.objects.filter(
            curso_academico=curso_academico,
            dni_pasaporte=unicode(request.user))

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
                    dni_pasaporte=unicode(request.user),
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

    return render_to_response(PATH + 'addPlantillaAReunionGrupal.html',
        {'user': request.user,
        'dni_pasaporte': instancia_reunion[0].dni_pasaporte,
        'curso_academico': curso_academico,
        'fecha': fecha,
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
                if not (vistasRPO.obtenerReunion_preguntaOficial(
                    dni_pasaporte, curso_academico, id_reunion,
                    id_entrevista_oficial,
                    pregunta.id_pregunta_oficial)):

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

def addPlantillaOficialAReunionGrupal(request, curso_academico, fecha,
    id_entrevista_oficial):
    user = unicode(request.user)

    lista_reuniones = determinarReunionesGrupales(user, curso_academico,
        fecha)

    if lista_reuniones:
        # Por cada reunion en la reunion grupal se incluyen las
        # preguntas.
        for reunion in lista_reuniones:
            lista_preguntas_oficiales = \
                models.PreguntaOficial.objects.filter(
                id_entrevista_oficial=id_entrevista_oficial).order_by(
                'id_pregunta_oficial')

            for pregunta in lista_preguntas_oficiales:
                if not (vistasRPO.obtenerReunion_preguntaOficial(
                    reunion.dni_pasaporte, curso_academico,
                    reunion.id_reunion, id_entrevista_oficial,
                    pregunta.id_pregunta_oficial)):

                    instancia_nueva_pregunta = \
                        models.ReunionPreguntaOficial.objects.create(
                        dni_pasaporte=reunion.dni_pasaporte,
                        curso_academico=curso_academico,
                        id_reunion=reunion.id_reunion,
                        id_entrevista_oficial=id_entrevista_oficial,
                        id_pregunta_oficial=
                        pregunta.id_pregunta_oficial,
                        respuesta='-')
                    instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunionGrupal_Asesor',
            kwargs={'curso_academico': curso_academico,
            'fecha': fecha}))

def addPlantillaAsesorAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_asesor):
    user = unicode(request.user)
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(user,
        curso_academico)

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
                dni_pasaporte=user,
                id_entrevista_asesor=id_entrevista_asesor).order_by(
                'id_pregunta_asesor')

            for pregunta in lista_preguntas_asesor:
                if not (vistasRPA.obtenerReunion_preguntaAsesor(
                dni_pasaporte, curso_academico, id_reunion, user,
                id_entrevista_asesor, pregunta.id_pregunta_asesor)):

                    instancia_nueva_pregunta = \
                        models.ReunionPreguntaAsesor.objects.create(
                        dni_pasaporte_alumno=dni_pasaporte,
                        dni_pasaporte_asesor=user,
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

def addPreguntaOficialAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_oficial, id_pregunta_oficial):
    user = unicode(request.user)
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(user,
        curso_academico)

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

            if not (vistasRPO.obtenerReunion_preguntaOficial(
            dni_pasaporte, curso_academico, id_reunion,
            id_entrevista_oficial, id_pregunta_oficial)):

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

def addPreguntaOficialAReunionGrupal(request, curso_academico, fecha,
    id_entrevista_oficial, id_pregunta_oficial):
    user = unicode(request.user)

    lista_reuniones = determinarReunionesGrupales(user, curso_academico,
        fecha)

    if lista_reuniones:
        # Por cada reunion en la reunion grupal se incluyen las
        # preguntas.
        for reunion in lista_reuniones:
            instancia_pregunta_oficial = \
                vistasPreguntaOficial.obtenerPreguntaOficial(
                id_entrevista_oficial, id_pregunta_oficial)

            if instancia_pregunta_oficial:
                if not (vistasRPO.obtenerReunion_preguntaOficial(
                reunion.dni_pasaporte, curso_academico, reunion.id_reunion,
                id_entrevista_oficial, id_pregunta_oficial)):

                    instancia_nueva_pregunta = \
                        models.ReunionPreguntaOficial.objects.create(
                        dni_pasaporte=reunion.dni_pasaporte,
                        curso_academico=curso_academico,
                        id_reunion=reunion.id_reunion,
                        id_entrevista_oficial=id_entrevista_oficial,
                        id_pregunta_oficial=id_pregunta_oficial,
                        respuesta='-')
                    instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunionGrupal_Asesor',
            kwargs={'curso_academico': curso_academico,
            'fecha': fecha}))

def addPreguntaAsesorAReunion(request, curso_academico, dni_pasaporte,
    id_reunion, id_entrevista_asesor, id_pregunta_asesor):
    user = unicode(request.user)
    # Se obtiene la instancia del asesor curso academico.
    instancia_asesorCA = \
        vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(user,
        curso_academico)

    # El asesor presta asesoria durante el curso academico.
    if instancia_asesorCA:
        # Se obtiene la instancia de la reunion.
        instancia_reunion = vistasReunion.obtenerReunion(dni_pasaporte,
            curso_academico, id_reunion)

        # Si existe se buscan las preguntas.
        if instancia_reunion:
            instancia_pregunta_asesor = \
                vistasPreguntaAsesor.obtenerPreguntaAsesor(user,
                curso_academico, id_entrevista_asesor,
                id_pregunta_asesor)

            if not (vistasRPA.obtenerReunion_preguntaAsesor(
                dni_pasaporte, curso_academico, id_reunion, user,
                id_entrevista_asesor, id_pregunta_asesor)):

                instancia_nueva_pregunta = \
                    models.ReunionPreguntaAsesor.objects.create(
                        dni_pasaporte_alumno=dni_pasaporte,
                        dni_pasaporte_asesor=user,
                        curso_academico=curso_academico,
                        id_reunion=id_reunion,
                        id_entrevista_asesor=id_entrevista_asesor,
                        id_pregunta_asesor=id_pregunta_asesor,
                        respuesta='-')
                instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunion_Asesor',
            kwargs={'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'id_reunion': id_reunion}))

def addPreguntaAsesorAReunionGrupal(request, curso_academico, fecha,
    id_entrevista_asesor, id_pregunta_asesor):
    user = unicode(request.user)

    lista_reuniones = determinarReunionesGrupales(user, curso_academico,
        fecha)

    if lista_reuniones:
        # Por cada reunion en la reunion grupal se incluyen las
        # preguntas.
        for reunion in lista_reuniones:
            instancia_pregunta_asesor = \
                vistasPreguntaAsesor.obtenerPreguntaAsesor(
                user, curso_academico, id_entrevista_asesor,
                id_pregunta_asesor)

            if instancia_pregunta_asesor:
                if not (vistasRPA.obtenerReunion_preguntaAsesor(
                    reunion.dni_pasaporte, curso_academico,
                    reunion.id_reunion, user, id_entrevista_asesor,
                    id_pregunta_asesor)):

                    instancia_nueva_pregunta = \
                        models.ReunionPreguntaAsesor.objects.create(
                        dni_pasaporte_alumno=reunion.dni_pasaporte,
                        curso_academico=curso_academico,
                        dni_pasaporte_asesor=user,
                        id_reunion=reunion.id_reunion,
                        id_entrevista_asesor=id_entrevista_asesor,
                        id_pregunta_asesor=id_pregunta_asesor,
                        respuesta='-')
                    instancia_nueva_pregunta.save()

    return HttpResponseRedirect(
            reverse('showReunionGrupal_Asesor',
            kwargs={'curso_academico': curso_academico,
            'fecha': fecha}))

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

def delPreguntaOficialAReunionGrupal(request, curso_academico, fecha,
    id_entrevista_oficial, id_pregunta_oficial):
    user = unicode(request.user)

    lista_reuniones = determinarReunionesGrupales(user, curso_academico,
        fecha)

    if lista_reuniones:
        # Por cada reunion en la reunion grupal se incluyen las
        # preguntas.
        for reunion in lista_reuniones:
            instancia_reunion_pregunta_oficial = \
                models.ReunionPreguntaOficial.objects.get(
                dni_pasaporte=reunion.dni_pasaporte,
                curso_academico=curso_academico,
                id_reunion=reunion.id_reunion,
                id_entrevista_oficial=id_entrevista_oficial,
                id_pregunta_oficial=id_pregunta_oficial)
            instancia_reunion_pregunta_oficial.delete()

    return HttpResponseRedirect(
            reverse('showReunionGrupal_Asesor',
            kwargs={'curso_academico': curso_academico,
            'fecha': fecha}))

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

def delPreguntaAsesorAReunionGrupal(request, curso_academico, fecha,
    id_entrevista_asesor, id_pregunta_asesor):
    user = unicode(request.user)

    lista_reuniones = determinarReunionesGrupales(user, curso_academico,
        fecha)

    if lista_reuniones:
        # Por cada reunion en la reunion grupal se incluyen las
        # preguntas.
        for reunion in lista_reuniones:
            instancia_reunion_pregunta_asesor = \
                models.ReunionPreguntaAsesor.objects.get(
                dni_pasaporte_alumno=reunion.dni_pasaporte,
                curso_academico=curso_academico,
                dni_pasaporte_asesor=user,
                id_reunion=reunion.id_reunion,
                id_entrevista_asesor=id_entrevista_asesor,
                id_pregunta_asesor=id_pregunta_asesor)
            instancia_reunion_pregunta_asesor.delete()

    return HttpResponseRedirect(
            reverse('showReunionGrupal_Asesor',
            kwargs={'curso_academico': curso_academico,
            'fecha': fecha}))
