#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from asesorias import models

CHOICES = [('administradorPrincipal', 'Administrador principal'),
    ('administradorCentro','Administrador de centro'),
    ('asesor','Asesor'), ('alumno','Alumno')]

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre", max_length=50)
    password = forms.CharField(label="Contraseña",
        widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=CHOICES)

class CentroForm(forms.ModelForm):
    class Meta:
        model = models.Centro

class CentroFormSelect(forms.Form):
    centro = forms.ModelChoiceField(models.Centro.objects.order_by(
        'nombre_centro'))

class AdministradorCentroForm(forms.ModelForm):
    class Meta:
        model = models.AdministradorCentro

class TitulacionForm(forms.ModelForm):
    class Meta:
        model = models.Titulacion

class TitulacionFormSelect(forms.Form):
    titulacion = forms.ModelChoiceField(
        queryset=models.Titulacion.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento id_centro.
    def __init__(self, id_centro, *args, **kwargs):
        super(TitulacionFormSelect, self).__init__(*args, **kwargs)
        self.fields['titulacion'].queryset = \
            models.Titulacion.objects.filter(
            id_centro=id_centro).order_by('nombre_titulacion')

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = models.Asignatura

class AsignaturaFormSelect(forms.Form):
    asignatura = forms.ModelChoiceField(
        queryset=models.Asignatura.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves de los argumentos id_centro e id_titulacion.
    def __init__(self, id_centro, id_titulacion, *args, **kwargs):
        super(AsignaturaFormSelect, self).__init__(*args, **kwargs)
        self.fields['asignatura'].queryset = \
            models.Asignatura.objects.filter(
            id_centro=id_centro, id_titulacion=id_titulacion).order_by(
            'nombre_asignatura')

class AsignaturaCursoAcademicoForm(forms.ModelForm):
    class Meta:
        model = models.AsignaturaCursoAcademico

class AsignaturaCursoAcademicoFormSelect(forms.Form):
    asignatura_curso_academico = forms.ModelChoiceField(
        queryset=models.AsignaturaCursoAcademico.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves de los argumentos id_centro e id_titulacion e
    # id_asignatura.
    def __init__(self, id_centro, id_titulacion, id_asignatura,
        *args, **kwargs):
        super(AsignaturaCursoAcademicoFormSelect,
            self).__init__(*args, **kwargs)
        self.fields['asignatura_curso_academico'].queryset = \
            models.AsignaturaCursoAcademico.objects.filter(
            id_centro=id_centro, id_titulacion=id_titulacion,
            id_asignatura=id_asignatura).order_by('curso_academico')

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = models.Departamento

class DepartamentoFormSelect(forms.Form):
    departamento = forms.ModelChoiceField(
        models.Departamento.objects.order_by('nombre_departamento'))

class AsesorForm(forms.ModelForm):
    class Meta:
        model = models.Asesor

class AsesorFormSelect(forms.Form):
    asesor = forms.ModelChoiceField(models.Asesor.objects.order_by(
        'dni_pasaporte'))

class AsesorCursoAcademicoForm(forms.ModelForm):
    class Meta:
        model = models.AsesorCursoAcademico

class AsesorCursoAcademicoFormSelect(forms.Form):
    asesor_curso_academico = forms.ModelChoiceField(
        queryset=models.AsesorCursoAcademico.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento dni_pasaporte.
    def __init__(self, dni_pasaporte, *args, **kwargs):
        super(AsesorCursoAcademicoFormSelect,
            self).__init__(*args, **kwargs)
        self.fields['asesor_curso_academico'].queryset = \
            models.AsesorCursoAcademico.objects.filter(
            dni_pasaporte=dni_pasaporte).order_by('curso_academico')

class PlantillaEntrevistaAsesorForm(forms.ModelForm):
    class Meta:
        model = models.PlantillaEntrevistaAsesor

class PlantillaEntrevistaAsesorFormSelect(forms.Form):
    entrevista_asesor = forms.ModelChoiceField(
        models.PlantillaEntrevistaAsesor.objects.order_by(
        'descripcion'))

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves de los argumentos id_centro e id_titulacion.
    def __init__(self, dni_pasaporte, curso_academico, *args, **kwargs):
        super(PlantillaEntrevistaAsesorFormSelect, self).__init__(
            *args, **kwargs)
        self.fields['entrevista_asesor'].queryset = \
            models.PlantillaEntrevistaAsesor.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico).order_by(
            'descripcion')

class PreguntaAsesorForm(forms.ModelForm):
    class Meta:
        model = models.PreguntaAsesor

class PreguntaAsesorFormSelect(forms.Form):
    pregunta_asesor = forms.ModelChoiceField(
        queryset=models.PreguntaAsesor.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves de los argumentos dni_pasaporte, curso_academico e
    # id_entrevista_asesor.
    def __init__(self, dni_pasaporte, curso_academico,
        id_entrevista_asesor, *args, **kwargs):
        super(PreguntaAsesorFormSelect,
            self).__init__(*args, **kwargs)
        self.fields['pregunta_asesor'].queryset = \
            models.PreguntaAsesor.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico,
            id_entrevista_asesor=id_entrevista_asesor).order_by(
            'enunciado')

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = models.Alumno

class AlumnoFormSelect(forms.Form):
    alumno = forms.ModelChoiceField(models.Alumno.objects.order_by(
        'dni_pasaporte'))

class AlumnosDeAsesorForm(forms.Form):
    alumno = forms.ModelChoiceField(
        models.AlumnoCursoAcademico.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento codigo_asesorCursoAcademico.
    def __init__(self, codigo_asesorCursoAcademico, curso_academico,
        *args, **kwargs):
        super(AlumnosDeAsesorForm,
            self).__init__(*args, **kwargs)
        self.fields['alumno'].queryset = \
            models.AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico=
            codigo_asesorCursoAcademico,
            curso_academico=curso_academico).order_by(
            'dni_pasaporte_alumno')

class AlumnoCursoAcademicoForm(forms.ModelForm):
    class Meta:
        model = models.AlumnoCursoAcademico

class AlumnoCursoAcademicoFormSelect(forms.Form):
    alumno = forms.ModelChoiceField(
        queryset=models.AlumnoCursoAcademico.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento curso_academico.
    def __init__(self, curso_academico, *args, **kwargs):
        super(AlumnoCursoAcademicoFormSelect,
            self).__init__(*args, **kwargs)
        self.fields['alumno'].queryset = \
            models.AlumnoCursoAcademico.objects.filter(
            curso_academico=curso_academico).order_by(
            'dni_pasaporte_alumno')

class AlumnoCursoAcademico2FormSelect(forms.Form):
    alumno_curso_academico = forms.ModelChoiceField(
        queryset=models.AlumnoCursoAcademico.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento dni_pasaporte.
    def __init__(self, dni_pasaporte, *args, **kwargs):
        super(AlumnoCursoAcademico2FormSelect,
            self).__init__(*args, **kwargs)
        self.fields['alumno_curso_academico'].queryset = \
            models.AlumnoCursoAcademico.objects.filter(
            dni_pasaporte_alumno=dni_pasaporte).order_by(
            'curso_academico')

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = models.Matricula

class CalificacionConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = models.CalificacionConvocatoria

class PlantillaEntrevistaOficialForm(forms.ModelForm):
    class Meta:
        model = models.PlantillaEntrevistaOficial

class PlantillaEntrevistaOficialFormSelect(forms.Form):
    entrevista_oficial = forms.ModelChoiceField(
        models.PlantillaEntrevistaOficial.objects.order_by(
        'descripcion'))

class PreguntaOficialForm(forms.ModelForm):
    class Meta:
        model = models.PreguntaOficial

class ReunionForm(forms.ModelForm):
    class Meta:
        model = models.Reunion

class ReunionFormSelect(forms.Form):
    reunion = forms.ModelChoiceField(
        queryset=models.Reunion.objects.all())

    # Necesario para actualizar el queryset en tiempo de ejecucion, a
    # traves del argumento dni_pasaporte.
    def __init__(self, dni_pasaporte, curso_academico, *args, **kwargs):
        super(ReunionFormSelect,
            self).__init__(*args, **kwargs)
        self.fields['reunion'].queryset = \
            models.Reunion.objects.filter(
            dni_pasaporte=dni_pasaporte,
            curso_academico=curso_academico).order_by('fecha')

class Centro_AdministradorCentroForm(forms.ModelForm):
    class Meta:
        model = models.CentroAdministradorCentro

class Reunion_PreguntaAsesorForm(forms.ModelForm):
    class Meta:
        model = models.ReunionPreguntaAsesor

class SearchForm(forms.Form):
    busqueda = forms.CharField(label="Busqueda", max_length=50)

class ModificarClaveForm(forms.Form):
    old_password = forms.CharField(label="Antigua contraseña",
        widget=forms.PasswordInput)
    new_password = forms.CharField(label="Nueva contraseña",
        widget=forms.PasswordInput)
