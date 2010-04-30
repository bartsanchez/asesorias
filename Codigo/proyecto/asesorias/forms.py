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
	titulacion = forms.ModelChoiceField(models.Titulacion.objects.all())

	class Meta:
		model = models.Asignatura

class AsignaturaCursoAcademicoForm(forms.ModelForm):
	asignatura = forms.ModelChoiceField(models.Asignatura.objects.all())

	class Meta:
		model = models.AsignaturaCursoAcademico

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = models.Departamento

class AsesorForm(forms.ModelForm):
	class Meta:
		model = models.Asesor

class AsesorCursoAcademicoForm(forms.ModelForm):
	class Meta:
		model = models.AsesorCursoAcademico

class PlantillaEntrevistaAsesorForm(forms.ModelForm):
	asesor_curso_academico = forms.ModelChoiceField(models.AsesorCursoAcademico.objects.all())

	class Meta:
		model = models.PlantillaEntrevistaAsesor

class PreguntaAsesorForm(forms.ModelForm):
	plantilla_entrevista_asesor = forms.ModelChoiceField(models.PlantillaEntrevistaAsesor.objects.all())

	class Meta:
		model = models.PreguntaAsesor

class Centro_AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.CentroAdministradorCentro
