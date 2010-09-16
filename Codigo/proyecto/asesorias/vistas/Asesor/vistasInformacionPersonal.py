from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias.vistas.AdministradorPrincipal import vistasAsesor
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

def showInfo(request):
    # Se obtiene la instancia del asesor.
    instancia_asesor = vistasAsesor.obtenerAsesor(request.user)
    # Si existe se edita.
    if instancia_asesor:
        # Se carga el formulario para el asesor existente.
        form = forms.AsesorForm(instance=instancia_asesor)
        # Se ha modificado el formulario original.
        if request.method == 'POST':
            # Se actualiza el formulario con la nueva informacion.
            form = forms.AsesorForm(request.POST,
                instance=instancia_asesor)
            # Si es valido se guarda.
            if form.is_valid():
                form.save()
                # Redirige a la pagina de listar asesores.
                return HttpResponseRedirect(
                    reverse('asesor_informacion_personal'))
    # El asesor no existe.
    else:
        form = False
    return render_to_response(PATH + 'showInfo.html',
        {'user': request.user, 'form': form})
