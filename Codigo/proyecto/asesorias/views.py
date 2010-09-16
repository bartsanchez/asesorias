from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias.vistas.AdministradorPrincipal import vistasAlumno

@login_required()
def alumno(request):
    # Obtiene una instancia del alumno en el sistema.
    alumno = vistasAlumno.obtenerAlumno( unicode(request.user) )

    return render_to_response('asesorias/alumnos.html', {'alumno': alumno})
