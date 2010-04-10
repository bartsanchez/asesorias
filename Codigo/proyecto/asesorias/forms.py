from django import forms

class LoginForm(forms.Form):
	nombre = forms.CharField(label='Nombre')
	password = forms.CharField(label='Password')
