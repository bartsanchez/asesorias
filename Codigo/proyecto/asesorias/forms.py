from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="Nombre", max_length=50)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

