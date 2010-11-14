from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsignatura
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico, vistasCentro
from asesorias.vistas.AdministradorPrincipal import \
    vistasMatricula, vistasTitulacion
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsignaturaCursoAcademico as vistasAsignaturaCA
from asesorias.vistas.vistasAdministradorPrincipal import \
    checkAdministradorPrincipal
from asesorias.utils import vistasPDF


PATH = 'asesorias/CalificacionConvocatoria/'

# Comprueba si existe una calificacion y, de ser asi, la devuelve.
def obtenerCalificacionConvocatoria(nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte,
    convocatoria):
    try:
        # Obtiene la instancia de la asignatura para posteriormente
        # obtener los id's correspondientes.
        instancia_asignatura = vistasAsignatura.obtenerAsignatura(
            nombre_centro, nombre_titulacion, plan_estudios,
            nombre_asignatura)

        # Obtiene la instancia del alumno curso academico para
        # posteriormente obtener los id's correspondientes.
        instancia_alumnoCA = \
            vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
            dni_pasaporte, curso_academico)

        # Obtiene la instancia de calificacion.
        resultado = models.CalificacionConvocatoria.objects.get(
            id_centro=instancia_asignatura.id_centro,
            id_titulacion=instancia_asignatura.id_titulacion,
            id_asignatura=instancia_asignatura.id_asignatura,
            curso_academico=instancia_alumnoCA.curso_academico,
            dni_pasaporte=
            unicode(instancia_alumnoCA.dni_pasaporte_alumno),
            convocatoria=convocatoria)
    except:
        resultado = False
    return resultado

@checkAdministradorPrincipal
@login_required
def addCalificacionConvocatoria(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte):

    # Se obtiene la posible matricula.
    instancia_matricula = \
        vistasMatricula.obtenerMatricula(nombre_centro,
        nombre_titulacion, plan_estudios, nombre_asignatura,
        curso_academico, dni_pasaporte)

    # Se comprueba que exista la matricula.
    if not instancia_matricula:
        return HttpResponseRedirect(
            reverse('selectCentro_CalificacionConvocatoria',
            kwargs={'tipo': 'add'}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        #Se extraen los valores pasados por el metodo POST.
        convocatoria = request.POST['convocatoria']
        nota = request.POST['nota']
        comentario = request.POST['comentario']

        # Se determina los campos heredados para la calificacion
        # convocatoria.
        id_centro = instancia_matricula.id_centro
        id_titulacion = instancia_matricula.id_titulacion
        id_asignatura = instancia_matricula.id_asignatura

        # Datos necesarios para crear la nueva calificacion.
        datos_calificacion = {'id_centro': id_centro,
            'id_titulacion': id_titulacion,
            'id_asignatura': id_asignatura,
            'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'convocatoria': convocatoria,
            'nota': nota,
            'comentario': comentario}

        # Se obtienen los valores y se valida.
        form = forms.CalificacionConvocatoriaForm(datos_calificacion)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar matriculas.
            return HttpResponseRedirect(
                reverse('listCalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'curso_academico': curso_academico,
                'dni_pasaporte': dni_pasaporte,
                'orden': 'convocatoria'}))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.CalificacionConvocatoriaForm()
    return render_to_response(PATH + 'addCalificacionConvocatoria.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'dni_pasaporte': dni_pasaporte})

@checkAdministradorPrincipal
@login_required
def editCalificacionConvocatoria(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte, convocatoria):
    # Se obtiene la instancia de la calificacion convocatoria.
    instancia_calificacion = obtenerCalificacionConvocatoria(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico, dni_pasaporte, convocatoria)
    # Si existe se edita.
    if instancia_calificacion:
        # Se carga el formulario para la calificacion existente.
        form = forms.CalificacionConvocatoriaForm(
            instance=instancia_calificacion)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            #Se extraen los valores pasados por el metodo POST.
            convocatoria = request.POST['convocatoria']
            nota = request.POST['nota']
            comentario = request.POST['comentario']

            # Datos necesarios para crear la nueva calificacion.
            datos_calificacion = {'id_centro':
                instancia_calificacion.id_centro,
                'id_titulacion':
                instancia_calificacion.id_titulacion,
                'id_asignatura':
                instancia_calificacion.id_asignatura,
                'curso_academico': curso_academico,
                'dni_pasaporte': dni_pasaporte,
                'convocatoria': convocatoria,
                'nota': nota,
                'comentario': comentario}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.CalificacionConvocatoriaForm(
                datos_calificacion, instance=instancia_calificacion)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar calificaciones.
                return HttpResponseRedirect(
                    reverse('listCalificacionConvocatoria',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico,
                    'dni_pasaporte': dni_pasaporte,
                    'orden': 'convocatoria'}))
    # La calificacion no existe.
    else:
        form = False
    return render_to_response(PATH +
        'editCalificacionConvocatoria.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'dni_pasaporte': dni_pasaporte})

@checkAdministradorPrincipal
@login_required
def delCalificacionConvocatoria(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte, convocatoria):
    # Se obtiene la instancia de la calificacion convocatoria.
    instancia_calificacion = obtenerCalificacionConvocatoria(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico, dni_pasaporte, convocatoria)

    # Si existe se elimina.
    if instancia_calificacion:
        instancia_calificacion.delete()
        # Redirige a la pagina de listar calificaciones.
        return HttpResponseRedirect(
            reverse('listCalificacionConvocatoria',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico,
                    'dni_pasaporte': dni_pasaporte,
                    'orden': 'convocatoria'}))
    # La calificacion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delCalificacionConvocatoria.html',
       {'user': request.user, 'error': error})

@checkAdministradorPrincipal
@login_required
def selectCentro(request, tipo):
    # Se ha introducido un centro.
    if request.method == 'POST':

        # Se obtiene el centro y se valida.
        form = forms.CentroFormSelect(request.POST)

        # Si es valido se redirige a listar centros.
        if form.is_valid():
            centro = request.POST['centro']

            # Se crea una instancia del centro para pasar el nombre de
            # centro por argumento.
            instancia_centro = models.Centro.objects.get(pk=centro)

            return HttpResponseRedirect(
                reverse('selectTitulacion_CalificacionConvocatoria',
                kwargs={'nombre_centro': instancia_centro.nombre_centro,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectCentro_CalificacionConvocatoria',
                kwargs={'tipo': tipo}))

    else:
        form = forms.CentroFormSelect()

    return render_to_response(PATH + 'selectCentro.html',
        {'user': request.user, 'form': form, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectTitulacion(request, nombre_centro, tipo):
    # Se obtiene el posible centro.
    instancia_centro = vistasCentro.obtenerCentro(nombre_centro)

    # Se comprueba que exista el centro.
    if not instancia_centro:
        return HttpResponseRedirect(
            reverse('selectCentro_CalificacionConvocatoria',
            kwargs={'tipo': tipo}))
    else:
        id_centro = instancia_centro.id_centro

    # Se ha introducido una titulacion.
    if request.method == 'POST':

        # Se obtiene la titulacion y se valida.
        form = forms.TitulacionFormSelect(id_centro, request.POST)

        # Si es valido se redirige a listar asignaturas.
        if form.is_valid():
            titulacion = request.POST['titulacion']

            # Se crea una instancia de la titulacion para pasar los
            # argumentos.
            instancia_titulacion = models.Titulacion.objects.get(
                pk=titulacion)

            return HttpResponseRedirect(
                reverse('selectAsignatura_CalificacionConvocatoria',
                kwargs={'nombre_centro':
                instancia_titulacion.determinarNombreCentro(),
                'nombre_titulacion':
                instancia_titulacion.nombre_titulacion,
                'plan_estudios': instancia_titulacion.plan_estudios,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectTitulacion_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro, 'tipo': tipo}))

    else:
        form = forms.TitulacionFormSelect(id_centro=id_centro)

    return render_to_response(PATH + 'selectTitulacion.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectAsignatura(request, nombre_centro, nombre_titulacion,
    plan_estudios, tipo):
    # Se obtiene la posible titulacion.
    instancia_titulacion = vistasTitulacion.obtenerTitulacion(
        nombre_centro, nombre_titulacion, plan_estudios)

    # Se comprueba que exista la titulacion.
    if not instancia_titulacion:
        return HttpResponseRedirect(
            reverse('selectTitulacion_CalificacionConvocatoria',
            kwargs={'nombre_centro': nombre_centro, 'tipo': tipo}))
    else:
        id_centro = instancia_titulacion.id_centro_id
        id_titulacion = instancia_titulacion.id_titulacion

    # Se ha introducido una titulacion.
    if request.method == 'POST':

        # Se obtiene la titulacion y se valida.
        form = forms.AsignaturaFormSelect(id_centro, id_titulacion,
            request.POST)

        # Si es valido se redirige a listar asignaturas curso academico.
        if form.is_valid():
            asignatura = request.POST['asignatura']

            # Se crea una instancia de la asignatura para pasar los
            # argumentos.
            instancia_asignatura = models.Asignatura.objects.get(
                pk=asignatura)

            return HttpResponseRedirect(
                reverse('selectAsignaturaCA_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': instancia_titulacion.plan_estudios,
                'nombre_asignatura':
                instancia_asignatura.nombre_asignatura,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsignatura_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios, 'tipo': tipo}))

    else:
        form = forms.AsignaturaFormSelect(id_centro=id_centro,
            id_titulacion=id_titulacion)

    return render_to_response(PATH + 'selectAsignatura.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios, 'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectAsignaturaCursoAcademico(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura, tipo):
    # Se obtiene la posible asignatura.
    instancia_asignatura = vistasAsignatura.obtenerAsignatura(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura)

    # Se comprueba que exista la asignatura.
    if not instancia_asignatura:
        return HttpResponseRedirect(
            reverse('selectAsignatura_CalificacionConvocatoria',
            kwargs={'nombre_centro': nombre_centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios, 'tipo': tipo}))
    else:
        id_centro = instancia_asignatura.id_centro
        id_titulacion = instancia_asignatura.id_titulacion
        id_asignatura = instancia_asignatura.id_asignatura

    # Se ha introducido una titulacion.
    if request.method == 'POST':

        # Se obtiene la titulacion y se valida.
        form = forms.AsignaturaCursoAcademicoFormSelect(
            id_centro, id_titulacion, id_asignatura, request.POST)

        # Si es valido se redirige a listar asignaturas curso academico.
        if form.is_valid():
            asignatura_curso_academico = \
                request.POST['asignatura_curso_academico']

            # Se crea una instancia de la asignatura curso academico
            # para pasar los argumentos.
            instancia_asignatura_curso_academico = \
                models.AsignaturaCursoAcademico.objects.get(
                pk=asignatura_curso_academico)

            curso_academico = \
                instancia_asignatura_curso_academico.curso_academico

            return HttpResponseRedirect(
                reverse('selectAlumno_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'curso_academico': curso_academico,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsignaturaCA_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'tipo': tipo}))

    else:
        form = forms.AsignaturaCursoAcademicoFormSelect(
            id_centro=id_centro, id_titulacion=id_titulacion,
            id_asignatura=id_asignatura)

    return render_to_response(PATH +
        'selectAsignaturaCursoAcademico.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def selectAlumno(request, nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, tipo):
    # Se obtiene la posible asignatura curso academico.
    instancia_asignatura_curso_academico = \
        vistasAsignaturaCA.obtenerAsignaturaCursoAcademico(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico)

    # Se comprueba que exista la asignatura.
    if not instancia_asignatura_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsignaturaCA_CalificacionConvocatoria',
            kwargs={'nombre_centro': nombre_centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'nombre_asignatura': nombre_asignatura,
            'tipo': tipo}))
    else:
        id_centro = instancia_asignatura_curso_academico.id_centro
        id_titulacion = \
            instancia_asignatura_curso_academico.id_titulacion
        id_asignatura = \
            instancia_asignatura_curso_academico.id_asignatura

    # Se ha introducido una titulacion.
    if request.method == 'POST':

        # Se obtiene la titulacion y se valida.
        form = forms.AlumnoCursoAcademicoFormSelect(
            curso_academico, request.POST)

        # Si es valido se redirige a listar asignaturas curso academico.
        if form.is_valid():
            alumno_curso_academico = request.POST['alumno']

            # Se crea una instancia del alumno curso academico para
            # pasar los argumentos.
            instancia_alumnoCA = \
                models.AlumnoCursoAcademico.objects.get(
                pk=alumno_curso_academico)

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse('addCalificacionConvocatoria',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico,
                    'dni_pasaporte':
                    instancia_alumnoCA.dni_pasaporte_alumno}))

            else:
                return HttpResponseRedirect(
                    reverse('listCalificacionConvocatoria',
                    kwargs={'nombre_centro': nombre_centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico,
                    'dni_pasaporte':
                    instancia_alumnoCA.dni_pasaporte_alumno,
                    'orden': 'convocatoria'}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumno_CalificacionConvocatoria',
                kwargs={'nombre_centro': nombre_centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'curso_academico': curso_academico,
                'tipo': tipo}))

    else:
        form = forms.AlumnoCursoAcademicoFormSelect(
            curso_academico=curso_academico)

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'tipo': tipo})

@checkAdministradorPrincipal
@login_required
def listCalificacionConvocatoria(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte, orden):
    # Se obtiene la posible matricula.
    instancia_matricula = \
        vistasMatricula.obtenerMatricula(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico, dni_pasaporte)

    # Se comprueba que exista la matricula.
    if not instancia_matricula:
        return HttpResponseRedirect(reverse(
            'selectAlumno_CalificacionConvocatoria',
            kwargs={'nombre_centro': nombre_centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'nombre_asignatura': nombre_asignatura,
            'curso_academico': curso_academico,
            'tipo': 'list'}))
    else:
        id_centro = instancia_matricula.id_centro
        id_titulacion = \
            instancia_matricula.id_titulacion
        id_asignatura = \
            instancia_matricula.id_asignatura

    # Se obtiene una lista con todos las calificaciones.
    lista_calificaciones = \
        models.CalificacionConvocatoria.objects.filter(
        id_centro=id_centro, id_titulacion=id_titulacion,
        id_asignatura=id_asignatura,
        curso_academico=curso_academico,
        dni_pasaporte=dni_pasaporte).all()

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
            for calificacion in lista_calificaciones:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(calificacion.convocatoria)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(calificacion)

            # La lista final a devolver sera la lista auxiliar.
            lista_calificaciones = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        # Si el orden es descendente se invierte la lista.
        if (orden == '_convocatoria'):
            lista_calificaciones = reversed(lista_calificaciones)

    return render_to_response(PATH +
        'listCalificacionConvocatoria.html',
        {'user': request.user, 'form': form,
        'lista_calificaciones': lista_calificaciones,
        'busqueda': busqueda,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'dni_pasaporte': dni_pasaporte,
        'orden': orden})

@checkAdministradorPrincipal
@login_required
def generarPDFListaCalificacionesConvocatoria(request, nombre_centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte, busqueda):
    # Se obtiene la posible matricula.
    instancia_matricula = \
        vistasMatricula.obtenerMatricula(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico, dni_pasaporte)

    # Se comprueba que exista la matricula.
    if not instancia_matricula:
        return HttpResponseRedirect(reverse(
            'selectAlumno_CalificacionConvocatoria',
            kwargs={'nombre_centro': nombre_centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'nombre_asignatura': nombre_asignatura,
            'curso_academico': curso_academico,
            'tipo': 'list'}))
    else:
        id_centro = instancia_matricula.id_centro
        id_titulacion = \
            instancia_matricula.id_titulacion
        id_asignatura = \
            instancia_matricula.id_asignatura

    # Se obtiene una lista con todos las calificaciones.
    lista_calificaciones = \
        models.CalificacionConvocatoria.objects.filter(
        id_centro=id_centro, id_titulacion=id_titulacion,
        id_asignatura=id_asignatura,
        curso_academico=curso_academico,
        dni_pasaporte=dni_pasaporte).all()

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de
            # la busqueda.
            lista_aux = []

            # Se recorren los elementos determinando si coinciden con
            # la busqueda.
            for calificacion in lista_calificaciones:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(calificacion.convocatoria)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(calificacion)

            # La lista final a devolver sera la lista auxiliar.
            lista_calificaciones = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_calificaciones,
        'name': 'calificaciones convocatoria',})
