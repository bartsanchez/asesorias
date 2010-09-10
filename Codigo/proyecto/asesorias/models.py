from django.db import models

# Create your models here.
class Centro(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre_centro = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = "Centros"

    def __unicode__(self):
        return self.nombre_centro

class AdministradorCentro(models.Model):
    id_adm_centro = models.AutoField(primary_key=True)
    nombre_adm_centro = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = "AdministradoresCentro"

    def __unicode__(self):
        return self.nombre_adm_centro

class Titulacion(models.Model):
    codigo_titulacion = models.AutoField(primary_key=True)
    id_centro = models.ForeignKey('Centro', db_column='id_centro')
    id_titulacion = models.IntegerField()
    nombre_titulacion = models.CharField(max_length=100)
    plan_estudios = models.IntegerField()

    class Meta:
        db_table = "Titulaciones"
        unique_together = (("id_centro", "id_titulacion"),
            ("id_centro", "nombre_titulacion", "plan_estudios"))

    def determinarNombreCentro(self):
        centro = Centro.objects.get(id_centro=self.id_centro_id)

        return unicode(centro.nombre_centro)

    def __unicode__(self):
        return (unicode(self.nombre_titulacion) +
            " (" + unicode(self.plan_estudios) + ")")

class Asignatura(models.Model):
    TIPOS_ASIGNATURAS = (
        ('TRO', 'Troncal'),
        ('OBL', 'Obligatoria'),
        ('OPT', 'Optativa'),
        ('LCN', 'Libre configuracion'),
    )

    codigo_asignatura = models.AutoField(primary_key=True)
    id_centro = models.IntegerField()
    id_titulacion = models.IntegerField()
    id_asignatura = models.IntegerField()
    nombre_asignatura = models.CharField(max_length=50)
    curso = models.IntegerField()
    tipo = models.CharField(max_length=3, choices=TIPOS_ASIGNATURAS)
    nCreditosTeoricos = models.FloatField()
    nCreditosPracticos = models.FloatField()

    class Meta:
        db_table = "Asignaturas"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura")

    def determinarNombreCentro(self):
        titulacion = Titulacion.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion)

        return unicode(titulacion.id_centro)

    def determinarNombreTitulacion(self):
        titulacion = Titulacion.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion)

        return unicode(titulacion.nombre_titulacion)

    def determinarPlanEstudios(self):
        titulacion = Titulacion.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion)

        return unicode(titulacion.plan_estudios)

    def __unicode__(self):
        return unicode(self.nombre_asignatura)

class AsignaturaCursoAcademico(models.Model):
    codigo_asignaturaCursoAcademico = models.AutoField(primary_key=True)
    id_centro = models.IntegerField()
    id_titulacion = models.IntegerField()
    id_asignatura = models.IntegerField()
    curso_academico = models.IntegerField()

    class Meta:
        db_table = "AsignaturasCursoAcademico"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura", "curso_academico")

    def determinarNombreCentro(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreCentro())

    def determinarNombreTitulacion(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreTitulacion())

    def determinarPlanEstudios(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarPlanEstudios())

    def determinarNombreAsignatura(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.nombre_asignatura)

    def __unicode__(self):
        return unicode(self.curso_academico)

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=25, unique=True)
    telefono = models.IntegerField()

    class Meta:
        db_table = "Departamentos"

    def __unicode__(self):
        return self.nombre_departamento

class Asesor(models.Model):
    dni_pasaporte = models.CharField(primary_key=True, max_length=9)
    correo_electronico = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    telefono = models.IntegerField()

    class Meta:
        db_table = "Asesores"

    def __unicode__(self):
        return self.dni_pasaporte

class AsesorCursoAcademico(models.Model):
    codigo_asesorCursoAcademico = models.AutoField(primary_key=True)
    dni_pasaporte = models.ForeignKey('Asesor',
        db_column='dni_pasaporte')
    curso_academico = models.IntegerField()
    observaciones = models.CharField(max_length=100)
    id_departamento = models.ForeignKey('Departamento',
        db_column='id_departamento')

    class Meta:
        db_table = "AsesoresCursoAcademico"
        unique_together = ("dni_pasaporte", "curso_academico")

    def __unicode__(self):
        return (unicode(self.curso_academico) +
            " (" + unicode(self.id_departamento) + ")")

class PlantillaEntrevistaAsesor(models.Model):
    codigo_plantillaEntrevistaAsesor = \
        models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField(max_length=9)
    curso_academico = models.IntegerField()
    id_entrevista_asesor = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    ultima_modificacion = models.DateField(auto_now=True)

    class Meta:
        db_table = "PlantillasEntrevistaAsesor"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_entrevista_asesor")

    def __unicode__(self):
        return unicode(self.descripcion)

class PreguntaAsesor(models.Model):
    codigo_preguntaAsesor = models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField(max_length=9)
    curso_academico = models.IntegerField()
    id_entrevista_asesor = models.IntegerField()
    id_pregunta_asesor = models.IntegerField()
    enunciado = models.CharField(max_length=150)
    ultima_modificacion = models.DateField(auto_now=True)

    class Meta:
        db_table = "PreguntasAsesores"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_entrevista_asesor", "id_pregunta_asesor")

    def __unicode__(self):
        return unicode(self.enunciado)

class Alumno(models.Model):
    dni_pasaporte = models.CharField(primary_key=True, max_length=9)
    correo_electronico = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion_cordoba = models.CharField(max_length=100)
    localidad_familiar = models.CharField(max_length=50)
    provincia_familiar = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=7)
    telefono_familiar = models.IntegerField()
    ingreso = models.IntegerField()
    otros_estudios_universitarios = models.CharField(max_length=50)
    modalidad_acceso_universidad = models.CharField(max_length=50)
    calificacion_acceso = models.FloatField()

    class Meta:
        db_table = "Alumnos"

    def __unicode__(self):
        return self.dni_pasaporte

class AlumnoCursoAcademico(models.Model):
    codigo_alumnoCursoAcademico = models.AutoField(primary_key=True)
    dni_pasaporte_alumno = models.ForeignKey('Alumno',
        db_column='dni_pasaporte')
    curso_academico = models.IntegerField()
    observaciones = models.CharField(max_length=100)
    codigo_asesorCursoAcademico = models.ForeignKey(
        'AsesorCursoAcademico', db_column='dni_pasaporte_asesor')

    class Meta:
        db_table = "AlumnosCursoAcademico"
        unique_together = ("dni_pasaporte_alumno", "curso_academico")

    def __unicode__(self):
        return (unicode(self.dni_pasaporte_alumno) + ' (' +
            unicode(self.curso_academico)) + ') '

class Matricula(models.Model):
    codigo_matricula = models.AutoField(primary_key=True)
    id_centro = models.IntegerField()
    id_titulacion = models.IntegerField()
    id_asignatura = models.IntegerField()
    curso_academico = models.IntegerField()
    dni_pasaporte = models.CharField(max_length=9)
    comentario = models.CharField(max_length=100)

    class Meta:
        db_table = "Matriculas"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura", "curso_academico", "dni_pasaporte")

    def determinarNombreCentro(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreCentro())

    def determinarNombreTitulacion(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreTitulacion())

    def determinarPlanEstudios(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarPlanEstudios())

    def determinarNombreAsignatura(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.nombre_asignatura)

    def __unicode__(self):
        return unicode(self.dni_pasaporte)

class CalificacionConvocatoria(models.Model):
    codigo_calificacionConvocatoria = models.AutoField(primary_key=True)
    id_centro = models.IntegerField()
    id_titulacion = models.IntegerField()
    id_asignatura = models.IntegerField()
    curso_academico = models.IntegerField()
    dni_pasaporte = models.CharField(max_length=9)
    convocatoria = models.CharField(max_length=15)
    nota = models.FloatField()
    comentario = models.CharField(max_length=100)

    class Meta:
        db_table = "CalificacionesConvocatoria"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura", "curso_academico", "dni_pasaporte",
            "convocatoria")

    def determinarNombreCentro(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreCentro())

    def determinarNombreTitulacion(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarNombreTitulacion())

    def determinarPlanEstudios(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.determinarPlanEstudios())

    def determinarNombreAsignatura(self):
        asignatura = Asignatura.objects.get(id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        return unicode(asignatura.nombre_asignatura)

    def __unicode__(self):
        return unicode(self.convocatoria)

class PlantillaEntrevistaOficial(models.Model):
    id_entrevista_oficial = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    ultima_modificacion = models.DateField(auto_now=True)

    class Meta:
        db_table = "PlantillasEntrevistaOficial"

    def __unicode__(self):
        return unicode(self.descripcion)

class PreguntaOficial(models.Model):
    codigo_pregunta_oficial = models.AutoField(primary_key=True)
    id_entrevista_oficial = \
        models.ForeignKey('PlantillaEntrevistaOficial',
        db_column='id_entrevista_oficial')
    id_pregunta_oficial = models.IntegerField()
    enunciado = models.CharField(max_length=150)
    ultima_modificacion = models.DateField(auto_now=True)

    class Meta:
        db_table = "PreguntasOficiales"
        unique_together = ("id_entrevista_oficial",
            "id_pregunta_oficial")

    def __unicode__(self):
        return unicode(self.enunciado)

class Reunion(models.Model):
    TIPOS_REUNION = (
        ('GRU', 'Grupal'),
        ('IND', 'Individual'),
    )

    codigo_reunion = models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField(max_length=9)
    curso_academico = models.IntegerField()
    id_reunion = models.IntegerField()
    fecha = models.DateField()
    tipo = models.CharField(max_length=3, choices=TIPOS_REUNION)
    comentario_asesor = models.CharField(max_length=100)
    comentario_alumno = models.CharField(max_length=100)

    class Meta:
        db_table = "Reuniones"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_reunion")

    def __unicode__(self):
        return unicode(self.fecha)

class CentroAdministradorCentro(models.Model):
    codigo_centro_administradorCentro = \
        models.AutoField(primary_key=True)
    id_centro = models.ForeignKey('Centro', db_column='id_centro')
    id_adm_centro = models.ForeignKey('AdministradorCentro',
        db_column='id_adm_centro')

    class Meta:
        db_table = "CentroAdministradorCentro"
        unique_together = ("id_centro", "id_adm_centro")

    def determinarNombreCentro(self):
        centro = Centro.objects.get(id_centro=self.id_centro_id)
        return unicode(centro.nombre_centro)

    def determinarNombreAdministradorCentro(self):
        administrador_centro = AdministradorCentro.objects.get(
            id_adm_centro=self.id_adm_centro_id)
        return unicode(administrador_centro.nombre_adm_centro)

    def __unicode__(self):
        return (unicode(self.id_centro) + " : " +
            unicode(self.id_adm_centro))

class ReunionPreguntaAsesor(models.Model):
    codigo_reunion_preguntasAsesores = \
        models.AutoField(primary_key=True)
    dni_pasaporte_alumno = models.CharField(max_length=9)
    curso_academico = models.IntegerField()
    id_reunion = models.IntegerField()
    dni_pasaporte_asesor = models.CharField(max_length=9)
    id_entrevista_asesor = models.IntegerField()
    id_pregunta_asesor = models.IntegerField()
    respuesta = models.CharField(max_length=150)

    class Meta:
        db_table = "ReunionPreguntaAsesor"
        unique_together = ("dni_pasaporte_alumno", "curso_academico",
            "id_reunion", "dni_pasaporte_asesor",
            "id_entrevista_asesor", "id_pregunta_asesor")

    def __unicode__(self):
        return (unicode(self.dni_pasaporte_alumno) + " : " +
            unicode(self.curso_academico) + " : " +
            unicode(self.id_reunion) + " : " +
            unicode(self.dni_pasaporte_asesor)  + " : " +
            unicode(self.id_entrevista_asesor) + " : " +
            unicode(self.id_pregunta_asesor))
