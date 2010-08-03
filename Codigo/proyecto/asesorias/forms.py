from django import forms
from asesorias import models

class LoginForm(forms.Form):
	username = forms.CharField(label="Nombre", max_length=50)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)

class CentroForm(forms.ModelForm):
	class Meta:
		model = models.Centro

class CentroFormSelect(forms.Form):
	centro = forms.ModelChoiceField(models.Centro.objects.order_by('nombre_centro'))

class AdministradorCentroForm(forms.ModelForm):
	class Meta:
		model = models.AdministradorCentro

class TitulacionForm(forms.ModelForm):
	class Meta:
		model = models.Titulacion

class TitulacionFormSelect(forms.Form):
	titulacion = forms.ModelChoiceField(queryset=models.Titulacion.objects.all())

	# Necesario para actualizar el queryset en tiempo de ejecucion, a traves del argumento id_centro.
	def __init__(self, id_centro, *args, **kwargs):
		super(TitulacionFormSelect, self).__init__(*args, **kwargs)
		self.fields['titulacion'].queryset = models.Titulacion.objects.filter(id_centro=id_centro).order_by('nombre_titulacion')

class AsignaturaForm(forms.ModelForm):
	class Meta:
		model = models.Asignatura

class AsignaturaFormSelect(forms.Form):
	asignatura = forms.ModelChoiceField(queryset=models.Asignatura.objects.all())

	# Necesario para actualizar el queryset en tiempo de ejecucion, a traves de los argumentos id_centro e id_titulacion.
	def __init__(self, id_centro, id_titulacion, *args, **kwargs):
		super(AsignaturaFormSelect, self).__init__(*args, **kwargs)
		self.fields['asignatura'].queryset = models.Asignatura.objects.filter(id_centro=id_centro, id_titulacion=id_titulacion).order_by('nombre_asignatura')

class AsignaturaCursoAcademicoForm(forms.ModelForm):
	class Meta:
		model = models.AsignaturaCursoAcademico

class AsignaturaCursoAcademicoFormSelect(forms.Form):
	asignatura_curso_academico = forms.ModelChoiceField(queryset=models.AsignaturaCursoAcademico.objects.all())

	# Necesario para actualizar el queryset en tiempo de ejecucion, a traves de los argumentos id_centro e id_titulacion e id_asignatura.
	def __init__(self, id_centro, id_titulacion, id_asignatura, *args, **kwargs):
		super(AsignaturaCursoAcademicoFormSelect, self).__init__(*args, **kwargs)
		self.fields['asignatura_curso_academico'].queryset = models.AsignaturaCursoAcademico.objects.filter(id_centro=id_centro, id_titulacion=id_titulacion, id_asignatura=id_asignatura).order_by('curso_academico')

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = models.Departamento

class DepartamentoFormSelect(forms.Form):
	departamento = forms.ModelChoiceField(models.Departamento.objects.order_by('nombre_departamento'))

class AsesorForm(forms.ModelForm):
	class Meta:
		model = models.Asesor

class AsesorFormSelect(forms.Form):
	asesor = forms.ModelChoiceField(models.Asesor.objects.order_by('dni_pasaporte'))

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

class AlumnoFormSelect(forms.Form):
	alumno = forms.ModelChoiceField(models.Alumno.objects.order_by('dni_pasaporte'))

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
