from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from asesorias import models
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import \
    vistasAsesorCursoAcademico
from asesorias import forms

PATH = 'asesorias/UsuarioAsesor/'

# Funcion decoradora para comprobar el asesor.
def checkAsesor(funcion):
    def inner(request, curso_academico, *args, **kwargs):
        try:
            models.Asesor.objects.get(
                dni_pasaporte=unicode(request.user))
        except:
            return HttpResponseRedirect(reverse('logout'))
        return funcion(request, curso_academico, *args, **kwargs)
    return inner

@checkAsesor
@login_required()
def asesor_inicio(request, curso_academico):
    return render_to_response(PATH + 'asesor_inicio.html',
        {'user': request.user, 'curso_academico': curso_academico})

@checkAsesor
@login_required()
def asesor_informacion_personal(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_informacion_personal.html',
        {'user': request.user, 'curso_academico': curso_academico})

@checkAsesor
@login_required()
def asesor_alumnos(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_alumnos.html',
        {'user': request.user, 'curso_academico': curso_academico})

@checkAsesor
@login_required()
def asesor_plantillas(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_plantillas.html',
        {'user': request.user, 'curso_academico': curso_academico})

@checkAsesor
@login_required()
def asesor_reuniones(request, curso_academico):
    return render_to_response(
        PATH + 'asesor_reuniones.html',
        {'user': request.user, 'curso_academico': curso_academico})

@checkAsesor
@login_required()
def setCursoAcademico(request, curso_academico):
    # Se ha modificado el formulario original.
    if request.method == 'POST':
        # Se actualiza el formulario con la nueva informacion.
        form = forms.CursoAcademicoFormSelect(request.POST)
        # Si es valido se redirige.
        if form.is_valid():
            curso_academico_nuevo = request.POST['curso_academico']

            # Se comprueba que exista el asesor curso academico.
            if vistasAsesorCursoAcademico.obtenerAsesorCursoAcademico(
                unicode(request.user), curso_academico_nuevo):
                return HttpResponseRedirect(reverse('asesor_inicio',
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
