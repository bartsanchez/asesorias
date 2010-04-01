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

	id_titulacion = models.ForeignKey('Titulacion', db_column='id_titulacion')
	id_centro = models.ForeignKey('Centro', db_column='id_centro')
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