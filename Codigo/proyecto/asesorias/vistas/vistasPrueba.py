from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms
from asesorias.utils import vistasPDF

def show_info(request):
    form = forms.AlumnoForm()
    return render_to_response('asesorias/Alumno/addAlumno.html',
        {'user': request.user, 'form': form})
