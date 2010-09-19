from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from asesorias import models, forms

PATH = 'asesorias/UsuarioAsesor/'

def showAlumnos(request):
    return render_to_response(PATH + 'showAlumnos.html',
        {'user': request.user, 'form': form})
