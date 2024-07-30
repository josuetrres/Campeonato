from django.db import models

class Persona (models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=10)
    correo = models.EmailField()
    class Meta:
        abstract = True

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    jugadorList = models.ManyToManyField('Jugador', blank=True)
    inscripcionList = models.ManyToManyField('Inscripcion', blank=True)
    estadistica = models.ForeignKey('EstadisticaEquipo', on_delete=models.CASCADE, blank=True, null=True)


class Jugador(Persona):
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    posicion = models.CharField(max_length=100)
    peso = models.FloatField()
    genero = models.CharField(max_length=100)
    estadistica = models.ForeignKey('EstadisticaJugador', on_delete=models.CASCADE, blank=True, null=True)

class Arbitro(Persona):
    partidoList = models.ManyToManyField('Partido', blank=True)


class Partido(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    equipoLocal = models.ForeignKey('Inscripcion', on_delete=models.DO_NOTHING, related_name='partidosComoLocal')
    equipoVisitante = models.ForeignKey('Inscripcion', on_delete=models.DO_NOTHING, related_name='partidosComoVisitante')
    arbitroList = models.ManyToManyField(Arbitro, blank=True)
    resultado = models.ForeignKey('Resultado', on_delete=models.CASCADE, blank=True, null=True)

class Resultado(models.Model):
    ganador = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    perdedor = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    esEmpate = models.BooleanField()
    golesLocal = models.IntegerField()
    golesVisitante = models.IntegerField()
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE)
    

class Inscripcion(models.Model):
    fecha = models.DateField()
    equipoInscrito = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    cuota = models.FloatField()
    estado = models.CharField(max_length=100)

class Estadistica(models.Model):
    fecha = models.DateField()
    campeonato = models.CharField(max_length=100)
    partidosJugados = models.IntegerField()
    goles = models.IntegerField()
    tarjetasAmarillas = models.IntegerField()
    tarjetasRojas = models.IntegerField()
    asistencias = models.IntegerField()
    faltas = models.IntegerField()
    recuperaciones = models.IntegerField()
    class Meta:
        abstract = True
    

class EstadisticaJugador(Estadistica):
    jugador = models.ForeignKey(Jugador, on_delete=models.DO_NOTHING)
    mvpPartidos = models.IntegerField()
    mvpCampeonatos = models.IntegerField()

class EstadisticaEquipo(Estadistica):
    puntos = models.IntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)


class TipoCampeonato(models.TextChoices):
    LIGA = 'LIGA', 'Liga'
    COPA = 'COPA', 'Copa'
    TORNEO = 'TORNEO', 'Torneo'
    GRUPOS = 'GRUPOS', 'Grupos'

class Campeonato(models.Model):
    tipo = models.CharField(max_length=100, choices=TipoCampeonato.choices) 
    nombre = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    periodo = models.CharField(max_length=100)
    inscripcionesList = models.ManyToManyField(Inscripcion, blank=True)
    partidoList = models.ManyToManyField(Partido, blank=True)

class TablaPosiciones(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.DO_NOTHING)
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING)
    puntos = models.IntegerField()
    partidosJugados = models.IntegerField()
    partidosGanados = models.IntegerField()
    partidosEmpatados = models.IntegerField()
    partidosPerdidos = models.IntegerField()
    golesFavor = models.IntegerField()
    golesContra = models.IntegerField()
    estadistica = models.ForeignKey(EstadisticaEquipo, on_delete=models.CASCADE)
   