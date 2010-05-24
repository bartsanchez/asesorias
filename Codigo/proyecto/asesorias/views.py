from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from asesorias.vistas import vistasAsesor, vistasAlumno

@login_required()
def administrador_inicio(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_inicio.html', {'administrador': request.user})

@login_required()
def administrador_org_institucional(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_org_institucional.html', {'administrador': request.user})

@login_required()
def administrador_org_docente(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_org_docente.html', {'administrador': request.user})

@login_required()
def administrador_alumnos(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_alumnos.html', {'administrador': request.user})

@login_required()
def administrador_reuniones(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_reuniones.html', {'administrador': request.user})

@login_required()
def administrador_plantillas(request):
	return render_to_response('asesorias/AdministradorPrincipal/administrador_plantillas.html', {'administrador': request.user})

@login_required()
def asesor(request):
	# Obtiene una instancia del asesor en el sistema.
	asesor = vistasAsesor.obtenerAsesor( unicode(request.user) )

	return render_to_response('asesorias/asesores.html', {'asesor': asesor})

@login_required()
def alumno(request):
	# Obtiene una instancia del alumno en el sistema.
	alumno = vistasAlumno.obtenerAlumno( unicode(request.user) )

	return render_to_response('asesorias/alumnos.html', {'alumno': alumno})
