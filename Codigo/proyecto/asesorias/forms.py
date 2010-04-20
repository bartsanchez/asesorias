from django import forms
from asesorias import models

class LoginForm(forms.Form):
	username = forms.CharField(label="Nombre", max_length=50)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

class CentroForm(forms.ModelForm):
	class Meta:
		model = models.Centro

class AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.AdministradorCentro

class TitulacionForm(forms.ModelForm):
	class Meta:
		model = models.Titulacion

class AsignaturaForm(forms.ModelForm):
	TITULACIONES = [(titulacion.codigo_titulacion, unicode(titulacion.id_centro) + ': ' + unicode(titulacion.nombre_titulacion) + ' (' + unicode(titulacion.plan_estudios) + ')' ) for titulacion in models.Titulacion.objects.all()]

	titulacion = forms.ChoiceField(choices=TITULACIONES)

	class Meta:
		model = models.Asignatura

class Centro_AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.CentroAdministradorCentro
