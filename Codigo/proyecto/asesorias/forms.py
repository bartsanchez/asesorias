from django import forms
from asesorias import models

class LoginForm(forms.Form):
	username = forms.CharField(label="Nombre", max_length=50)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

class addCentroForm(forms.ModelForm):
	class Meta:
		model = models.Centro
