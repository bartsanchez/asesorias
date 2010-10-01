#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Centro(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre_centro = models.CharField("Centro", max_length=25,
        unique=True)

    class Meta:
        db_table = "Centros"

    def borrar(self):
        # Se obtienen todas las titulaciones del centro para
        # borrarlas.
        titulaciones = Titulacion.objects.filter(
            id_centro=self.id_centro)

        # Si el centro tenia titulaciones se borran.
        if (titulaciones):
            for titulacion in titulaciones:
                titulacion.borrar()

        # Se borra el asesor.
        self.delete()
        return

    def __unicode__(self):
        return self.nombre_centro

class AdministradorCentro(models.Model):
    id_adm_centro = models.AutoField(primary_key=True)
    nombre_adm_centro = models.CharField(
        "Nombre administrador de centro", max_length=25, unique=True)

    class Meta:
        db_table = "AdministradoresCentro"

    def __unicode__(self):
        return self.nombre_adm_centro

class Titulacion(models.Model):
    codigo_titulacion = models.AutoField(primary_key=True)
    id_centro = models.ForeignKey('Centro', db_column='id_centro',
        verbose_name="Centro")
    id_titulacion = models.IntegerField()
    nombre_titulacion = models.CharField("Titulación", max_length=100)
    plan_estudios = models.IntegerField("Plan de estudios")

    class Meta:
        db_table = "Titulaciones"
        unique_together = (("id_centro", "id_titulacion"),
            ("id_centro", "nombre_titulacion", "plan_estudios"))

    def editar(self, id_centro_antigua, id_titulacion_antigua):
        # Se obtienen todas las asignaturas de la titulacion para
        # editarlas.
        asignaturas = Asignatura.objects.filter(
            id_centro=id_centro_antigua,
            id_titulacion=id_titulacion_antigua).update(
            id_centro=self.id_centro_id,
            id_titulacion=self.id_titulacion)

        # Se obtienen todas las asignaturasCA de la titulacion para
        # editarlas.
        asignaturasCA = AsignaturaCursoAcademico.objects.filter(
            id_centro=id_centro_antigua,
            id_titulacion=id_titulacion_antigua).update(
            id_centro=self.id_centro_id,
            id_titulacion=self.id_titulacion)

        # Se obtienen todas las matriculas de la titulacion para
        # editarlas.
        matriculas = Matricula.objects.filter(
            id_centro=id_centro_antigua,
            id_titulacion=id_titulacion_antigua).update(
            id_centro=self.id_centro_id,
            id_titulacion=self.id_titulacion)

        # Se obtienen todas las calificaciones de la titulacion para
        # editarlas.
        calificaciones = CalificacionConvocatoria.objects.filter(
            id_centro=id_centro_antigua,
            id_titulacion=id_titulacion_antigua).update(
            id_centro=self.id_centro_id,
            id_titulacion=self.id_titulacion)

        return

    def borrar(self):
        # Se obtienen todas las asignaturas de la titulacion para
        # borrarlas.
        asignaturas = Asignatura.objects.filter(
            id_centro=self.id_centro_id,
            id_titulacion=self.id_titulacion)

        # Si la titulacion tenia asignaturas curso academico se borran.
        if (asignaturas):
            for asignatura in asignaturas:
                asignatura.borrar()

        # Se borra el asesor.
        self.delete()
        return

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
    nombre_asignatura = models.CharField("Asignatura", max_length=50)
    curso = models.IntegerField()
    tipo = models.CharField(max_length=3, choices=TIPOS_ASIGNATURAS)
    nCreditosTeoricos = models.FloatField("Nº de créditos teóricos")
    nCreditosPracticos = models.FloatField("Nº de créditos prácticos")

    class Meta:
        db_table = "Asignaturas"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura")

    def editar(self, id_asignatura_antiguo):
        # Se obtienen todas las asignaturas curso academico de la
        # asignatura para editarlas.
        asignaturas = AsignaturaCursoAcademico.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=id_asignatura_antiguo).update(
            id_asignatura=self.id_asignatura)

        # Se obtienen todas las matriculas de la asignatura para
        # editarlas.
        matriculas = Matricula.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=id_asignatura_antiguo).update(
            id_asignatura=self.id_asignatura)

        # Se obtienen todas las calificaciones de la asignatura para
        # editarlas.
        calificaciones = CalificacionConvocatoria.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=id_asignatura_antiguo).update(
            id_asignatura=self.id_asignatura)

        return

    def borrar(self):
        # Se obtienen todas las asignaturas curso academico de la
        # asignatura para borrarlas.
        asignaturas = AsignaturaCursoAcademico.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura)

        # Si la asignatura tenia asignaturas curso academico se borran.
        if (asignaturas):
            for asignatura in asignaturas:
                asignatura.borrar()

        # Se borra el asesor.
        self.delete()
        return

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
    curso_academico = models.IntegerField("Curso académico")

    class Meta:
        db_table = "AsignaturasCursoAcademico"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura", "curso_academico")

    def editar(self, curso_academico_antiguo):
        # Se obtienen todas las matriculas de la asignatura para
        # editarlas.
        matriculas = Matricula.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura,
            curso_academico=curso_academico_antiguo).update(
            curso_academico=self.curso_academico)

        # Se obtienen todas las calificaciones de la asignatura para
        # editarlas.
        calificaciones = CalificacionConvocatoria.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura,
            curso_academico=curso_academico_antiguo).update(
            curso_academico=self.curso_academico)

        return

    def borrar(self):
        # Se obtienen todas las matriculas de la asignatura para
        # borrarlas.
        matriculas = Matricula.objects.filter(
            id_centro=self.id_centro,
            id_titulacion=self.id_titulacion,
            id_asignatura=self.id_asignatura,
            curso_academico=self.curso_academico)

        # Si la asignatura tenia matriculas se borran.
        if (matriculas):
            for matricula in matriculas:
                matricula.borrar()

        # Se borra el asesor.
        self.delete()
        return

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
    nombre_departamento = models.CharField("Departamento",
        max_length=25, unique=True)
    telefono = models.IntegerField("Teléfono")

    class Meta:
        db_table = "Departamentos"

    def __unicode__(self):
        return self.nombre_departamento

class Asesor(models.Model):
    dni_pasaporte = models.CharField("DNI/Pasaporte", primary_key=True,
        max_length=9)
    correo_electronico = models.EmailField("Correo electrónico",
        unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    telefono = models.IntegerField("Teléfono")

    class Meta:
        db_table = "Asesores"

    def borrar(self):
        # Se obtienen todos los asesores curso academico para borrarlos.
        asesores = AsesorCursoAcademico.objects.filter(
            dni_pasaporte=self.dni_pasaporte)

        # Si el asesor estaba matriculado se borra.
        if (asesores):
            for asesor in asesores:
                asesor.borrar()

        # Se borra el asesor.
        self.delete()
        return

    def __unicode__(self):
        return self.dni_pasaporte

class AsesorCursoAcademico(models.Model):
    codigo_asesorCursoAcademico = models.AutoField(primary_key=True)
    dni_pasaporte = models.ForeignKey('Asesor',
        db_column='dni_pasaporte', verbose_name="DNI/Pasaporte")
    curso_academico = models.IntegerField("Curso académico")
    observaciones = models.CharField(max_length=100)
    id_departamento = models.ForeignKey('Departamento',
        db_column='id_departamento', verbose_name="Departamento")

    class Meta:
        db_table = "AsesoresCursoAcademico"
        unique_together = ("dni_pasaporte", "curso_academico")

    def editar(self, dni_pasaporte_antiguo, curso_academico_antiguo):
        # Se obtienen todas las plantillas de asesor curso academico.
        plantillas_asesor = PlantillaEntrevistaAsesor.objects.filter(
            dni_pasaporte=dni_pasaporte_antiguo,
            curso_academico=curso_academico_antiguo).update(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico)

        # Se obtienen todas las preguntas de asesor curso academico.
        preguntas_asesor = PreguntaAsesor.objects.filter(
            dni_pasaporte=dni_pasaporte_antiguo,
            curso_academico=curso_academico_antiguo).update(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico)

        return

    def borrar(self):
        # Se obtienen todas las plantillas del asesor para borrarlas.
        plantillas_asesor = PlantillaEntrevistaAsesor.objects.filter(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico)

        # Si el asesor tenia plantillas se borran.
        if (plantillas_asesor):
            for plantilla in plantillas_asesor:
                plantilla.borrar()

        # Se obtienen todos los alumnos curso academico del asesor para
        # borrarlos.
        alumnos_curso_academico = AlumnoCursoAcademico.objects.filter(
            codigo_asesorCursoAcademico=
            self.codigo_asesorCursoAcademico,
            curso_academico=self.curso_academico)

        # Si el asesor tenia alumnos curso academico se borran.
        if (alumnos_curso_academico):
            for alumno in alumnos_curso_academico:
                alumno.borrar()

        # Se borra el asesor.
        self.delete()
        return

    def __unicode__(self):
        return (unicode(self.curso_academico) +
            " (" + unicode(self.id_departamento) + ")")

class PlantillaEntrevistaAsesor(models.Model):
    codigo_plantillaEntrevistaAsesor = \
        models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
    curso_academico = models.IntegerField("Curso académico")
    id_entrevista_asesor = models.IntegerField("Entrevista asesor")
    descripcion = models.CharField("Descripción", max_length=100)
    ultima_modificacion = models.DateField("Última modificación",
        auto_now=True)

    class Meta:
        db_table = "PlantillasEntrevistaAsesor"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_entrevista_asesor")

    def editar(self, id_entrevista_asesor_antigua):
        # Se obtienen todas las preguntas de asesor de esta plantilla.
        preguntas_de_plantilla = PreguntaAsesor.objects.filter(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico,
            id_entrevista_asesor=id_entrevista_asesor_antigua).update(
            id_entrevista_asesor=self.id_entrevista_asesor)

        return

    def borrar(self):
        # Se borran todas las preguntas de asesor de esta plantilla.
        preguntas_de_plantilla = PreguntaAsesor.objects.filter(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico,
            id_entrevista_asesor=self.id_entrevista_asesor).delete()

        # Se borra la plantilla.
        self.delete()
        return

    def __unicode__(self):
        return unicode(self.descripcion)

class PreguntaAsesor(models.Model):
    codigo_preguntaAsesor = models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
    curso_academico = models.IntegerField("Curso académico")
    id_entrevista_asesor = models.IntegerField("Entrevista asesor")
    id_pregunta_asesor = models.IntegerField("Pregunta asesor")
    enunciado = models.CharField(max_length=150)
    ultima_modificacion = models.DateField("Última modificación",
        auto_now=True)

    class Meta:
        db_table = "PreguntasAsesores"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_entrevista_asesor", "id_pregunta_asesor")

    def __unicode__(self):
        return unicode(self.enunciado)

class Alumno(models.Model):
    dni_pasaporte = models.CharField("DNI/Pasaporte", primary_key=True,
        max_length=9)
    correo_electronico = models.EmailField("Correo electrónico",
        unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    direccion_cordoba = models.CharField("Dirección en Córdoba",
        max_length=100)
    localidad_familiar = models.CharField(max_length=50)
    provincia_familiar = models.CharField(max_length=50)
    codigo_postal = models.CharField("Código postal", max_length=7)
    telefono_familiar = models.IntegerField("Teléfono familiar")
    ingreso = models.IntegerField()
    otros_estudios_universitarios = models.CharField(max_length=50)
    modalidad_acceso_universidad = models.CharField(
        "Modalidad de acceso a la universidad", max_length=50)
    calificacion_acceso = models.FloatField("Calificación de acceso")

    class Meta:
        db_table = "Alumnos"

    def borrar(self):
        # Se obtienen todos los alumnos curso academico para borrarlos.
        alumnos = AlumnoCursoAcademico.objects.filter(
            dni_pasaporte_alumno=self.dni_pasaporte)

        # Si el alumno estaba matriculado se borra.
        if (alumnos):
            for alumno in alumnos:
                alumno.borrar()

        # Se borra el asesor.
        self.delete()
        return

    def __unicode__(self):
        return self.dni_pasaporte

class AlumnoCursoAcademico(models.Model):
    codigo_alumnoCursoAcademico = models.AutoField(primary_key=True)
    dni_pasaporte_alumno = models.ForeignKey('Alumno',
        db_column='dni_pasaporte', verbose_name="DNI/Pasaporte")
    curso_academico = models.IntegerField("Curso académico")
    observaciones = models.CharField(max_length=100)
    codigo_asesorCursoAcademico = models.ForeignKey(
        'AsesorCursoAcademico', db_column='dni_pasaporte_asesor',
        verbose_name="DNI/Pasaporte Asesor")

    class Meta:
        db_table = "AlumnosCursoAcademico"
        unique_together = ("dni_pasaporte_alumno", "curso_academico")

    def borrar(self):
        # Se obtienen todas las reuniones del alumno para borrarlas.
        reuniones = Reunion.objects.filter(
            dni_pasaporte=self.dni_pasaporte_alumno,
            curso_academico=self.curso_academico)

        # Si el alumno tenia reuniones se borran.
        if (reuniones):
            for reunion in reuniones:
                reunion.borrar()

        # Se obtienen todas las matriculas del alumno para borrarlas.
        matriculas = Matricula.objects.filter(
            dni_pasaporte=self.dni_pasaporte_alumno,
            curso_academico=self.curso_academico)

        # Si el alumno tenia matriculas se borran.
        if (matriculas):
            for matricula in matriculas:
                matricula.borrar()

        # Se borra el asesor.
        self.delete()
        return

    def nombre(self):
        return (unicode(self.dni_pasaporte_alumno.nombre))

    def apellidos(self):
        return (unicode(self.dni_pasaporte_alumno.apellidos))

    def __unicode__(self):
        return (unicode(self.dni_pasaporte_alumno) + ' (' +
            unicode(self.curso_academico)) + ') '

class Matricula(models.Model):
    codigo_matricula = models.AutoField(primary_key=True)
    id_centro = models.IntegerField()
    id_titulacion = models.IntegerField()
    id_asignatura = models.IntegerField()
    curso_academico = models.IntegerField("Curso académico")
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
    comentario = models.CharField(max_length=100)

    class Meta:
        db_table = "Matriculas"
        unique_together = ("id_centro", "id_titulacion",
            "id_asignatura", "curso_academico", "dni_pasaporte")

    def borrar(self):
        # Se obtienen todas las calificaciones para borrarlas.
        calificaciones = CalificacionConvocatoria.objects.filter(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico).delete()

        # Se borra el asesor.
        self.delete()
        return

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
    curso_academico = models.IntegerField("Curso académico")
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
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
    descripcion = models.CharField("Descripción", max_length=100)
    ultima_modificacion = models.DateField("Última modificación",
        auto_now=True)

    class Meta:
        db_table = "PlantillasEntrevistaOficial"

    def __unicode__(self):
        return unicode(self.descripcion)

class PreguntaOficial(models.Model):
    codigo_pregunta_oficial = models.AutoField(primary_key=True)
    id_entrevista_oficial = \
        models.ForeignKey('PlantillaEntrevistaOficial',
        db_column='id_entrevista_oficial',
        verbose_name="Entrevista oficial")
    id_pregunta_oficial = models.IntegerField("Pregunta oficial")
    enunciado = models.CharField(max_length=150)
    ultima_modificacion = models.DateField("Última modificación",
        auto_now=True)

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
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
    curso_academico = models.IntegerField("Curso académico")
    id_reunion = models.IntegerField()
    fecha = models.DateField()
    tipo = models.CharField(max_length=3, choices=TIPOS_REUNION)
    comentario_asesor = models.CharField(max_length=100)
    comentario_alumno = models.CharField(max_length=100)

    class Meta:
        db_table = "Reuniones"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_reunion")

    def borrar(self):
        # Se obtienen todas las reuniones del alumno para borrarlas.
        reuniones = ReunionPreguntaAsesor.objects.filter(
            dni_pasaporte_alumno=self.dni_pasaporte,
            curso_academico=self.curso_academico).delete()

        reuniones = ReunionPreguntaOficial.objects.filter(
            dni_pasaporte=self.dni_pasaporte,
            curso_academico=self.curso_academico).delete()

        # Se borra el asesor.
        self.delete()
        return

    def __unicode__(self):
        return unicode(self.fecha)

class CentroAdministradorCentro(models.Model):
    codigo_centro_administradorCentro = \
        models.AutoField(primary_key=True)
    id_centro = models.ForeignKey('Centro', db_column='id_centro',
        verbose_name="Centro")
    id_adm_centro = models.ForeignKey('AdministradorCentro',
        db_column='id_adm_centro',
        verbose_name="Administrador de centro")

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
    dni_pasaporte_alumno = models.CharField("DNI/Pasaporte Alumno",
        max_length=9)
    curso_academico = models.IntegerField("Curso académico")
    id_reunion = models.IntegerField()
    dni_pasaporte_asesor = models.CharField("DNI/Pasaporte Asesor",
        max_length=9)
    id_entrevista_asesor = models.IntegerField("Entrevista asesor")
    id_pregunta_asesor = models.IntegerField("Pregunta asesor")
    respuesta = models.CharField(max_length=150)

    class Meta:
        db_table = "ReunionPreguntaAsesor"
        unique_together = ("dni_pasaporte_alumno", "curso_academico",
            "id_reunion", "dni_pasaporte_asesor",
            "id_entrevista_asesor", "id_pregunta_asesor")

    def __unicode__(self):
        return unicode(self.id_pregunta_asesor)

class ReunionPreguntaOficial(models.Model):
    codigo_reunion_preguntasOficiales = \
        models.AutoField(primary_key=True)
    dni_pasaporte = models.CharField("DNI/Pasaporte", max_length=9)
    curso_academico = models.IntegerField("Curso académico")
    id_reunion = models.IntegerField()
    id_entrevista_oficial = models.IntegerField("Entrevista oficial")
    id_pregunta_oficial = models.IntegerField("Pregunta oficial")
    respuesta = models.CharField(max_length=150)

    class Meta:
        db_table = "ReunionPreguntaOficial"
        unique_together = ("dni_pasaporte", "curso_academico",
            "id_reunion", "id_entrevista_oficial",
            "id_pregunta_oficial")

    def __unicode__(self):
        return unicode(self.id_pregunta_oficial)
