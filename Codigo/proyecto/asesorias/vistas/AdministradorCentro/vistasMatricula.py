from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.vistas.AdministradorPrincipal import vistasAsignatura
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsignaturaCursoAcademico as vistasAsignaturaCA
from asesorias.vistas.AdministradorPrincipal import vistasAlumno
from asesorias.vistas.AdministradorPrincipal import \
    vistasAlumnoCursoAcademico, vistasCentro
from asesorias.vistas.AdministradorPrincipal import vistasTitulacion
from asesorias.utils import vistasPDF

PATH = 'asesorias/UsuarioAdministradorCentro/Matricula/'

# Comprueba si existe una matricula y, de ser asi, la devuelve.
def obtenerMatricula(nombre_centro, nombre_titulacion, plan_estudios,
    nombre_asignatura, curso_academico, dni_pasaporte):
    try:
        # Obtiene la instancia de la asignatura para posteriormente
        # obtener los id's correspondientes.
        instancia_asignatura = vistasAsignatura.obtenerAsignatura(
            nombre_centro, nombre_titulacion, plan_estudios,
            nombre_asignatura)

        # Obtiene la instancia del alumno curso academico para
        # posteriormente obtener los id's correspondientes.
        instancia_alumno_curso_academico = \
            vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
            dni_pasaporte, curso_academico)

        # Obtiene la instancia de matricula.
        resultado = models.Matricula.objects.get(
            id_centro=instancia_asignatura.id_centro,
            id_titulacion=instancia_asignatura.id_titulacion,
            id_asignatura=instancia_asignatura.id_asignatura,
            curso_academico=
            instancia_alumno_curso_academico.curso_academico,
            dni_pasaporte=
            unicode(
            instancia_alumno_curso_academico.dni_pasaporte_alumno))
    except:
        resultado = False
    return resultado

def addMatricula(request, centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
    # Se obtiene la posible asignatura curso academico.
    instancia_asignaturaCA = \
        vistasAsignaturaCA.obtenerAsignaturaCursoAcademico(
        centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico)

    # Se comprueba que exista la asignatura.
    if not instancia_asignaturaCA:
        return HttpResponseRedirect(
            reverse('selectAsignaturaCursoAcademico_Matricula' +
            '_administradorCentro',
            kwargs={'centro': centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'nombre_asignatura': nombre_asignatura,
            'tipo': 'add'}))

    # Se obtiene el posible alumno curso academico.
    instancia_alumnoCA =  \
        vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
            dni_pasaporte, curso_academico)

    # Se comprueba que exista el alumno curso academico.
    if not instancia_alumnoCA:
        return HttpResponseRedirect(
            reverse('administradorCentro_inicio',
            kwargs={'centro': centro}))

    # Se ha rellenado el formulario.
    if request.method == 'POST':
        #Se extraen los valores pasados por el metodo POST.
        comentario = request.POST['comentario']

        # Se determina id_centro, id_titulacion e id_asignatura para esa
        # asignatura curso academico.
        id_centro = instancia_asignaturaCA.id_centro
        id_titulacion = instancia_asignaturaCA.id_titulacion
        id_asignatura = instancia_asignaturaCA.id_asignatura

        # Datos necesarios para crear la nueva asignatura
        datos_matricula = {'id_centro': id_centro,
            'id_titulacion': id_titulacion,
            'id_asignatura': id_asignatura,
            'curso_academico': curso_academico,
            'dni_pasaporte': dni_pasaporte,
            'comentario': comentario}

        # Se obtienen los valores y se valida.
        form = forms.MatriculaForm(datos_matricula)
        if form.is_valid():
            # Se guarda la informacion del formulario en el sistema.
            form.save()
            # Redirige a la pagina de listar matriculas.
            return HttpResponseRedirect(
                reverse('listMatricula_administradorCentro',
                kwargs={'centro':
                instancia_asignaturaCA.determinarNombreCentro(),
                'nombre_titulacion':
                instancia_asignaturaCA.determinarNombreTitulacion(),
                'plan_estudios':
                instancia_asignaturaCA.determinarPlanEstudios(),
                'nombre_asignatura':
                instancia_asignaturaCA.determinarNombreAsignatura(),
                'curso_academico': curso_academico,
                'orden': 'curso_academico'}) )
    # Si aun no se ha rellenado el formulario, se genera uno en blanco.
    else:
        form = forms.MatriculaForm()
    return render_to_response(PATH + 'addMatricula.html',
        {'user': request.user, 'form': form,
        'centro': centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'dni_pasaporte': dni_pasaporte})

def editMatricula(request, nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
    # Se obtiene la instancia de la matricula.
    instancia_matricula = obtenerMatricula(nombre_centro,
        nombre_titulacion, plan_estudios, nombre_asignatura,
        curso_academico, dni_pasaporte)
    # Si existe se edita.
    if instancia_matricula:
        # Se carga el formulario para la matricula existente.
        form = forms.MatriculaForm(instance=instancia_matricula)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se obtienen el resto de valores necesarios a traves de
            # POST.
            comentario = request.POST['comentario']

            # Datos necesarios para crear la nueva asignatura
            datos_matricula = {'id_centro':
                instancia_matricula.id_centro,
                'id_titulacion': instancia_matricula.id_titulacion,
                'id_asignatura': instancia_matricula.id_asignatura,
                'curso_academico': curso_academico,
                'dni_pasaporte': dni_pasaporte,
                'comentario': comentario}

            # Se actualiza el formulario con la nueva informacion.
            form = forms.MatriculaForm(datos_matricula,
                instance=instancia_matricula)

            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar matriculas.
                return HttpResponseRedirect(reverse('listMatricula',
                kwargs={'nombre_centro':
                instancia_matricula.determinarNombreCentro(),
                'nombre_titulacion':
                instancia_matricula.determinarNombreTitulacion(),
                'plan_estudios':
                instancia_matricula.determinarPlanEstudios(),
                'nombre_asignatura':
                instancia_matricula.determinarNombreAsignatura(),
                'curso_academico': curso_academico,
                'orden': 'curso_academico'}))
    # La matricula no existe
    else:
        form = False
    return render_to_response(PATH + 'editMatricula.html',
        {'user': request.user, 'form': form,
        'nombre_centro': nombre_centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'dni_pasaporte': dni_pasaporte})

def delMatricula(request, centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, dni_pasaporte):
    # Se obtiene la instancia de la matricula.
    instancia_matricula = obtenerMatricula(centro,
    nombre_titulacion, plan_estudios, nombre_asignatura,
    curso_academico, dni_pasaporte)

    # Si existe se elimina.
    if instancia_matricula:
        instancia_matricula.borrar()
        # Redirige a la pagina de listar matriculas.
        return HttpResponseRedirect(
            reverse('listMatricula_administradorCentro',
                kwargs={'centro':
                instancia_matricula.determinarNombreCentro(),
                'nombre_titulacion':
                instancia_matricula.determinarNombreTitulacion(),
                'plan_estudios':
                instancia_matricula.determinarPlanEstudios(),
                'nombre_asignatura':
                instancia_matricula.determinarNombreAsignatura(),
                'curso_academico': curso_academico,
                'orden': 'curso_academico'}))
    # La matricula no existe.
    else:
        error = True
    return render_to_response(PATH + 'delMatricula.html',
        {'user': request.user, 'error': error, 'centro': centro})

def selectTitulacion(request, centro, tipo):
    # Se obtiene el posible centro.
    instancia_centro = vistasCentro.obtenerCentro(centro)

    # Se comprueba que exista el centro.
    if not instancia_centro:
        return HttpResponseRedirect(
            reverse('administradorCentro_inicio',
            kwargs={'centro': centro}))
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
                reverse(
                'selectAsignatura_Matricula_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion':
                instancia_titulacion.nombre_titulacion,
                'plan_estudios': instancia_titulacion.plan_estudios,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse(
                'selectTitulacion_Matricula_administradorCentro',
                kwargs={'centro': centro, 'tipo': tipo}))

    else:
        form = forms.TitulacionFormSelect(id_centro=id_centro)

    return render_to_response(PATH + 'selectTitulacion.html',
        {'user': request.user, 'form': form,
        'centro': centro, 'tipo': tipo})

def selectAsignatura(request, centro, nombre_titulacion,
    plan_estudios, tipo):
    # Se obtiene la posible titulacion.
    instancia_titulacion = vistasTitulacion.obtenerTitulacion(
        centro, nombre_titulacion, plan_estudios)

    # Se comprueba que exista la titulacion.
    if not instancia_titulacion:
        return HttpResponseRedirect(
            reverse(
                'selectTitulacion_Matricula_administradorCentro',
                kwargs={'centro': centro, 'tipo': tipo}))
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
                reverse('selectAsignaturaCursoAcademico_Matricula' +
                '_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': instancia_titulacion.plan_estudios,
                'nombre_asignatura':
                instancia_asignatura.nombre_asignatura,
                'tipo': tipo}))

        else:
            return HttpResponseRedirect(
                reverse(
                'selectAsignatura_Matricula_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios, 'tipo': tipo}))

    else:
        form = forms.AsignaturaFormSelect(id_centro=id_centro,
            id_titulacion=id_titulacion)

    return render_to_response(PATH + 'selectAsignatura.html',
        {'user': request.user, 'form': form,
        'centro': centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios, 'tipo': tipo})

def selectAsignaturaCursoAcademico(request, centro,
    nombre_titulacion, plan_estudios, nombre_asignatura, tipo):
    # Se obtiene la posible asignatura.
    instancia_asignatura = vistasAsignatura.obtenerAsignatura(
        centro, nombre_titulacion, plan_estudios,
        nombre_asignatura)

    # Se comprueba que exista la asignatura.
    if not instancia_asignatura:
        return HttpResponseRedirect(
            reverse('selectAsignatura_Matricula_administradorCentro',
            kwargs={'centro': centro,
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

            if tipo == 'add':
                return HttpResponseRedirect(
                    reverse(
                    'selectAlumno_Matricula_administradorCentro',
                    kwargs={'centro': centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico}))

            else:
                return HttpResponseRedirect(
                    reverse('listMatricula_administradorCentro',
                    kwargs={'centro': centro,
                    'nombre_titulacion': nombre_titulacion,
                    'plan_estudios': plan_estudios,
                    'nombre_asignatura': nombre_asignatura,
                    'curso_academico': curso_academico,
                    'orden': 'curso_academico'}))

        else:
            return HttpResponseRedirect(
                reverse('selectAsignaturaCursoAcademico_Matricula' +
                '_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'tipo': tipo}))

    else:
        form = forms.AsignaturaCursoAcademicoFormSelect(
            id_centro=id_centro, id_titulacion=id_titulacion,
            id_asignatura=id_asignatura)

    return render_to_response(PATH +
        'selectAsignaturaCursoAcademico.html',
        {'user': request.user, 'form': form,
        'centro': centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'tipo': tipo})

def selectAlumno(request, centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico):
    # Se obtiene la posible asignatura curso academico.
    instancia_asignatura_curso_academico = \
        vistasAsignaturaCA.obtenerAsignaturaCursoAcademico(
        centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico)

    # Se comprueba que exista la asignatura.
    if not instancia_asignatura_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsignaturaCursoAcademico_Matricula' +
            '_administradorCentro',
            kwargs={'centro': centro,
            'nombre_titulacion': nombre_titulacion,
            'plan_estudios': plan_estudios,
            'nombre_asignatura': nombre_asignatura,
            'tipo': 'list'}))
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
            instancia_alumno_curso_academico = \
                models.AlumnoCursoAcademico.objects.get(
                pk=alumno_curso_academico)

            return HttpResponseRedirect(
                reverse('addMatricula_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'curso_academico': curso_academico,
                'dni_pasaporte':
                instancia_alumno_curso_academico.dni_pasaporte_alumno}))

        else:
            return HttpResponseRedirect(
                reverse('selectAlumno_Matricula_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'curso_academico': curso_academico}))

    else:
        form = forms.AlumnoCursoAcademicoFormSelect(
            curso_academico=curso_academico)

    return render_to_response(PATH + 'selectAlumno.html',
        {'user': request.user, 'form': form,
        'centro': centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico})

def listMatricula(request, centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, orden):
    # Se obtiene la posible asignatura_curso_academico.
    instancia_asignatura_curso_academico = \
        vistasAsignaturaCA.obtenerAsignaturaCursoAcademico(
        centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico)

    # Se comprueba que exista la asignatura curso academico.
    if not instancia_asignatura_curso_academico:
        reverse('selectAsignaturaCursoAcademico_Matricula' +
                '_administradorCentro',
                kwargs={'centro': centro,
                'nombre_titulacion': nombre_titulacion,
                'plan_estudios': plan_estudios,
                'nombre_asignatura': nombre_asignatura,
                'tipo': tipo})
    else:
        id_centro = instancia_asignatura_curso_academico.id_centro
        id_titulacion = \
            instancia_asignatura_curso_academico.id_titulacion
        id_asignatura = \
            instancia_asignatura_curso_academico.id_asignatura

    # Se obtiene una lista con todos las matriculas.
    lista_matriculas = models.Matricula.objects.filter(
        id_centro=id_centro, id_titulacion=id_titulacion,
        id_asignatura=id_asignatura,
        curso_academico=curso_academico).all()

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
            for matricula in lista_matriculas:
                # Se crea una cadena auxiliar para examinar si se
                # encuentra el resultado de la busqueda.
                cadena = unicode(matricula.dni_pasaporte)

                # Si se encuentra la busqueda el elemento se incluye en
                # la lista auxiliar.
                if cadena.find(busqueda) >= 0:
                    lista_aux.append(matricula)

            # La lista final a devolver sera la lista auxiliar.
            lista_matriculas = lista_aux

        else:
            busqueda = False
    # No se ha realizado busqueda.
    else:
        # Formulario para una posible busqueda.
        form = forms.SearchForm()
        busqueda = False

        # Si el orden es descendente se invierte la lista.
        if (orden == '_curso_academico'):
            lista_matriculas = reversed(lista_matriculas)

    return render_to_response(PATH + 'listMatricula.html',
        {'user': request.user, 'form': form,
        'lista_matriculas': lista_matriculas,
        'busqueda': busqueda,
        'centro': centro,
        'nombre_titulacion': nombre_titulacion,
        'plan_estudios': plan_estudios,
        'nombre_asignatura': nombre_asignatura,
        'curso_academico': curso_academico,
        'orden': orden})

def generarPDFListaMatriculas(request, nombre_centro, nombre_titulacion,
    plan_estudios, nombre_asignatura, curso_academico, busqueda):
    # Se obtiene la posible asignatura curso academico.
    instancia_asignatura_curso_academico = \
        vistasAsignaturaCA.obtenerAsignaturaCursoAcademico(
        nombre_centro, nombre_titulacion, plan_estudios,
        nombre_asignatura, curso_academico)

    # Se comprueba que exista la asignatura curso academico.
    if not instancia_asignatura_curso_academico:
        return HttpResponseRedirect(
            reverse('selectAsignaturaOAlumnoCursoAcademico'))
    else:
        id_centro = instancia_asignatura_curso_academico.id_centro
        id_titulacion = \
            instancia_asignatura_curso_academico.id_titulacion
        id_asignatura = \
            instancia_asignatura_curso_academico.id_asignatura

    # Se obtiene una lista con todas las matriculas.
    lista_matriculas = models.Matricula.objects.filter(
        id_centro=id_centro, id_titulacion=id_titulacion,
        id_asignatura=id_asignatura,
        curso_academico=curso_academico).order_by('dni_pasaporte')

    # Se ha realizado una busqueda.
    if busqueda != 'False':
        # Se crea una lista auxiliar que albergara el resultado de la
        # busqueda.
        lista_aux = []

        # Se recorren los elementos determinando si coinciden con la
        # busqueda.
        for matricula in lista_matriculas:
            # Se crea una cadena auxiliar para examinar si se encuentra
            # el resultado de la busqueda.
            cadena = unicode(matricula.dni_pasaporte)

            # Si se encuentra la busqueda el elemento se incluye en la
            # lista auxiliar.
            if cadena.find(busqueda) >= 0:
                lista_aux.append(matricula)

        # La lista final a devolver sera la lista auxiliar.
        lista_matriculas = lista_aux

    return vistasPDF.render_to_pdf('asesorias/plantilla_pdf.html',
        {'mylist': lista_matriculas, 'name': 'matriculas',})
