from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas import vistasAsignatura
from asesorias.vistas import vistasAlumnoCursoAcademico, vistasMatricula

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
            dni_pasaporte=unicode(instancia_alumnoCA.dni_pasaporte),
            convocatoria=convocatoria)
    except:
        resultado = False
    return resultado

def addCalificacionConvocatoria(request):
    # Se ha rellenado el formulario.
    if request.method == 'POST':
        #Se extraen los valores pasados por el metodo POST.
        codigo_matricula = request.POST['matricula']
        convocatoria = request.POST['convocatoria']
        nota = request.POST['nota']
        comentario = request.POST['comentario']

        # Se obtiene una instancia de la matricula a traves de su id.
        instancia_matricula = models.Matricula.objects.get(
            pk=codigo_matricula)

        # Se determina los campos heredados para la calificacion
        # convocatoria.
        id_centro = instancia_matricula.id_centro
        id_titulacion = instancia_matricula.id_titulacion
        id_asignatura = instancia_matricula.id_asignatura
        curso_academico = instancia_matricula.curso_academico
        dni_pasaporte = instancia_matricula.dni_pasaporte

        # Datos necesarios para crear la nueva calificacion.
        datos_calificacion = {'id_centro': id_centro,
            'id_titulacion': id_titulacion,
            'id_asignatura': id_asignatura,
            'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'convocatoria': convocatoria,
            'nota': nota,
            'comentario': comentario,
            'matricula': codigo_matricula}

        # Se obtienen los valores y se valida.
        form = forms.CalificacionConvocatoriaForm(datos_calificacion)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar matriculas.
            return HttpResponseRedirect(
                reverse('listCalificacionConvocatoria'))
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.CalificacionConvocatoriaForm()
    return render_to_response(PATH + 'addCalificacionConvocatoria.html',
        {'form': form})

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
            instance=instancia_calificacion,
            initial={'matricula':
            vistasMatricula.obtenerMatricula(
            nombre_centro, nombre_titulacion, plan_estudios,
            nombre_asignatura, curso_academico,
            dni_pasaporte).codigo_matricula})
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            #Se extraen los valores pasados por el metodo POST.
            codigo_matricula = request.POST['matricula']
            convocatoria = request.POST['convocatoria']
            nota = request.POST['nota']
            comentario = request.POST['comentario']

            # Se obtiene una instancia de la matricula a traves de
            # su id.
            instancia_matricula = models.Matricula.objects.get(
                pk=codigo_matricula)

            # Se determina los campos heredados para la calificacion
            # convocatoria.
            id_centro = instancia_matricula.id_centro
            id_titulacion = instancia_matricula.id_titulacion
            id_asignatura = instancia_matricula.id_asignatura
            curso_academico = instancia_matricula.curso_academico
            dni_pasaporte = instancia_matricula.dni_pasaporte

            # Datos necesarios para crear la nueva calificacion.
            datos_calificacion = {'id_centro': id_centro,
                'id_titulacion': id_titulacion,
                'id_asignatura': id_asignatura,
                'curso_academico': curso_academico,
                'dni_pasaporte': dni_pasaporte,
                'convocatoria': convocatoria,
                'nota': nota,
                'comentario': comentario,
                'matricula': codigo_matricula}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.CalificacionConvocatoriaForm(
                datos_calificacion, instance=instancia_calificacion)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar calificaciones.
                return HttpResponseRedirect(
                    reverse('listCalificacionConvocatoria'))
    # La calificacion no existe.
    else:
        form = False
    return render_to_response(PATH +
        'editCalificacionConvocatoria.html', {'form': form})

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
            reverse('listCalificacionConvocatoria'))
    # La calificacion no existe.
    else:
        error = True
    return render_to_response(PATH + 'delCalificacionConvocatoria.html',
        {'error': error})

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

def listCalificacionConvocatoria(request):
    # Se obtiene una lista con todas las calificaciones por
    # convocatoria.
    lista_calificaciones = models.CalificacionConvocatoria.objects.all()
    return render_to_response(PATH +
        'listCalificacionConvocatoria.html',
        {'lista_calificaciones': lista_calificaciones})
