from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import \
        vistasAlumnoCursoAcademico
from asesorias import forms

PATH = 'asesorias/UsuarioAlumno/'

@login_required()
def alumno_inicio(request, curso_academico):
    return render_to_response(PATH + 'alumno_inicio.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def alumno_informacion_personal(request, curso_academico):
    return render_to_response(
        PATH + 'alumno_informacion_personal.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def alumno_matriculas(request, curso_academico):
    return render_to_response(
        PATH + 'alumno_matriculas.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def alumno_reuniones(request, curso_academico):
    return render_to_response(
        PATH + 'alumno_reuniones.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def setCursoAcademico(request, curso_academico):
    # Se ha modificado el formulario original.
    if request.method == 'POST':
        # Se actualiza el formulario con la nueva informacion.
        form = forms.CursoAcademicoFormSelect(request.POST)
        # Si es valido se redirige.
        if form.is_valid():
            curso_academico_nuevo = request.POST['curso_academico']

            # Se comprueba que exista el alumno curso academico.
            if vistasAlumnoCursoAcademico.obtenerAlumnoCursoAcademico(
                unicode(request.user), curso_academico_nuevo):
                return HttpResponseRedirect(reverse('alumno_inicio',
                    kwargs={'curso_academico': curso_academico_nuevo}))
            else:
                return render_to_response(
                    PATH + 'NoCursoAcademico.html',
                    {'user': request.user,
                    'curso_academico': curso_academico})
    else:
        form = forms.CursoAcademicoFormSelect()
    return render_to_response(
        PATH + 'setCursoAcademico.html',
        {'user': request.user, 'curso_academico': curso_academico,
        'form': form})
