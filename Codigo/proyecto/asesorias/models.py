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