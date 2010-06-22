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

class AlumnoForm(forms.ModelForm):
	class Meta:
		model = models.Alumno

class AlumnoCursoAcademicoForm(forms.ModelForm):
	class Meta:
		model = models.AlumnoCursoAcademico

class MatriculaForm(forms.ModelForm):
	alumno_curso_academico = forms.ModelChoiceField(models.AlumnoCursoAcademico.objects.all())
	asignatura_curso_academico = forms.ModelChoiceField(models.AsignaturaCursoAcademico.objects.all())

	class Meta:
		model = models.Matricula

class CalificacionConvocatoriaForm(forms.ModelForm):
	matricula = forms.ModelChoiceField(models.Matricula.objects.all())

	class Meta:
		model = models.CalificacionConvocatoria

class PlantillaEntrevistaOficialForm(forms.ModelForm):
	class Meta:
		model = models.PlantillaEntrevistaOficial

class PreguntaOficialForm(forms.ModelForm):
	plantilla_entrevista_oficial = forms.ModelChoiceField(models.PlantillaEntrevistaOficial.objects.all())

	class Meta:
		model = models.PreguntaOficial

class ReunionForm(forms.ModelForm):
	alumno_curso_academico = forms.ModelChoiceField(models.AlumnoCursoAcademico.objects.all())

	class Meta:
		model = models.Reunion

class Centro_AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.CentroAdministradorCentro

class Reunion_PreguntaAsesorForm(forms.ModelForm):
	reunion = forms.ModelChoiceField(models.Reunion.objects.all())
	pregunta_asesor = forms.ModelChoiceField(models.PreguntaAsesor.objects.all())

	class Meta:
		model = models.ReunionPreguntaAsesor

class SearchForm(forms.Form):
	busqueda = forms.CharField(label="Busqueda", max_length=50)
