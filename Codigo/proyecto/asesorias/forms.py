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

class Centro_AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.CentroAdministradorCentro

class TitulacionForm(forms.ModelForm):
	class Meta:
		model = models.Titulacion
