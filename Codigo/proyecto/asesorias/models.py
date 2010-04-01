from django.db import models

# Create your models here.
class Centro(models.Model):
	id_centro = models.AutoField(primary_key=True)
	nombre_centro = models.CharField(max_length=25, unique=True)

	def __unicode__(self):
		return self.nombre_centro

class AdministradorCentro(models.Model):
	id_adm_centro = models.AutoField(primary_key=True)
	nombre_adm_centro = models.CharField(max_length=25, unique=True)

	def __unicode__(self):
		return self.nombre_adm_centro

class Titulacion(models.Model):
	id_centro = models.ForeignKey('Centro', db_column='id_centro')
	id_titulacion = models.AutoField(primary_key=True)
	nombre_titulacion = models.CharField(max_length=100)
	plan_estudios = models.IntegerField()

	class Meta:
		unique_together = (("id_centro", "id_titulacion"), ("nombre_titulacion", "plan_estudios"))

	def __unicode__(self):
		return self.nombre_titulacion

class Asignatura(models.Model):
	TIPOS_ASIGNATURAS = (
		('TRO', 'Troncal'),
		('OBL', 'Obligatoria'),
		('OPT', 'Optativa'),
		('LCN', 'Libre configuracion'),
	)

	id_centro = models.ForeignKey('Centro', db_column='id_centro')
	id_titulacion = models.ForeignKey('Titulacion', db_column='id_titulacion')
	id_asignatura = models.AutoField(primary_key=True)
	nombre_asignatura = models.CharField(max_length=50)
	curso = models.IntegerField()
	tipo = models.CharField(max_length=3, choices=TIPOS_ASIGNATURAS)
	nCreditosTeoricos = models.FloatField()
	nCreditosPracticos = models.FloatField()

	class Meta:
		unique_together = ("id_centro", "id_titulacion", "id_asignatura")

	def __unicode__(self):
		return self.nombre_asignatura

class AsignaturaCursoAcademico(models.Model):
	id_centro = models.ForeignKey('Centro', db_column='id_centro')
	id_titulacion = models.ForeignKey('Titulacion', db_column='id_titulacion')
	id_asignatura = models.ForeignKey('Asignatura', db_column='id_asignatura')
	curso_academico = models.IntegerField()

	class Meta:
		unique_together = ("id_centro", "id_titulacion", "id_asignatura", "curso_academico")

	def __unicode__(self):
		return self.curso_academico

class Departamento(models.Model):
	id_departamento = models.AutoField(primary_key=True)
	nombre_departamento = models.CharField(max_length=25)
	telefono = models.IntegerField()

	def __unicode__(self):
		return self.nombre_departamento

class Asesor(models.Model):
	dni_pasaporte = models.CharField(primary_key=True, max_length=9)
	correo_electronico = models.CharField(max_length=50)
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=100)
	telefono = models.IntegerField()

	def __unicode__(self):
		return self.correo_electronico

class AsesorCursoAcademico(models.Model):
	dni_pasaporte = models.ForeignKey('Asesor', db_column='dni_pasaporte')
	curso_academico = models.IntegerField()
	observaciones = models.CharField(max_length=100)
	id_departamento = models.ForeignKey('Departamento', db_column='id_departamento')

	class Meta:
		unique_together = ("dni_pasaporte", "curso_academico")

	def __unicode__(self):
		return self.dni_pasaporte

class PlantillaEntrevistaAsesor(models.Model):
	dni_pasaporte = models.ForeignKey('Asesor', db_column='dni_pasaporte')
	curso_academico = models.IntegerField()
	id_entrevista_asesor = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100)
	ultima_modificacion = models.DateField()

	class Meta:
		unique_together = ("dni_pasaporte", "curso_academico", "id_entrevista_asesor")

	def __unicode__(self):
		return self.id_entrevista_asesor
