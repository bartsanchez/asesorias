from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import forms

PATH = 'asesorias/UsuarioAsesor/'

@login_required()
def asesor_inicio(request, curso_academico):
    return render_to_response(PATH + 'asesor_inicio.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_informacion_personal(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_informacion_personal.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_alumnos(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_alumnos.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_plantillas(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_plantillas.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def asesor_reuniones(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_reuniones.html',
        {'user': request.user, 'curso_academico': curso_academico})

@login_required()
def setCursoAcademico(request, curso_academico):
    # Se ha modificado el formulario original.
    if request.method == 'POST':
        # Se actualiza el formulario con la nueva informacion.
        form = forms.CursoAcademicoFormSelect(request.POST)
        # Si es valido se redirige.
        if form.is_valid():
            curso_academico = request.POST['curso_academico']
            return HttpResponseRedirect(reverse('asesor_inicio',
            kwargs={'curso_academico': curso_academico}))
    else:
        form = forms.CursoAcademicoFormSelect()
    return render_to_response(
        PATH + 'setCursoAcademico.html',
        {'user': request.user, 'curso_academico': curso_academico,
        'form': form})
