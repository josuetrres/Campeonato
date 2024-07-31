from django.db import models

class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ci = models.CharField(max_length=10)
    correo = models.EmailField()
    class Meta:
        abstract = True

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    jugadorList = models.ManyToManyField('Jugador', blank=True, related_name='equipos')
    inscripcionList = models.ManyToManyField('Inscripcion', blank=True, related_name='equipos_inscripciones')
    estadistica = models.ForeignKey('EstadisticaEquipo', on_delete=models.CASCADE, blank=True, null=True, related_name='equipos')
    def __str__(self):
        return self.nombre

class Jugador(Persona):
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='jugadores')
    posicion = models.CharField(max_length=100)
    peso = models.FloatField()
    genero = models.CharField(max_length=100)
    estadistica = models.ForeignKey('EstadisticaJugador', on_delete=models.CASCADE, blank=True, null=True, related_name='jugadores')
    def __str__(self):
        return self.nombres + ' ' + self.apellidos  

class Arbitro(Persona):
    partidoList = models.ManyToManyField('Partido', blank=True, related_name='arbitros')

class Partido(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    equipoLocal = models.ForeignKey('Inscripcion', on_delete=models.DO_NOTHING, related_name='partidos_local')
    equipoVisitante = models.ForeignKey('Inscripcion', on_delete=models.DO_NOTHING, related_name='partidos_visitante')
    resultado = models.ForeignKey('Resultado', on_delete=models.CASCADE, blank=True, null=True, related_name='partidos_asociados')

class Resultado(models.Model):
    ganador = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='ganador_resultados')
    perdedor = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='perdedor_resultados')
    esEmpate = models.BooleanField()
    golesLocal = models.IntegerField()
    golesVisitante = models.IntegerField()
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE, related_name='resultado_partido')


class Inscripcion(models.Model):
    fecha = models.DateField()
    equipoInscrito = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='inscripciones')
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
    jugador = models.ForeignKey(Jugador, on_delete=models.DO_NOTHING, related_name='estadisticas')
    mvpPartidos = models.IntegerField()
    mvpCampeonatos = models.IntegerField()

class EstadisticaEquipo(Estadistica):
    puntos = models.IntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='estadisticas')

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
    inscripcionesList = models.ManyToManyField(Inscripcion, blank=True, related_name='campeonatos')
    partidoList = models.ManyToManyField(Partido, blank=True, related_name='campeonatos')
    def __str__(self):
        return self.nombre
    
class TablaPosiciones(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.DO_NOTHING, related_name='tabla_posiciones')
    equipo = models.ForeignKey(Equipo, on_delete=models.DO_NOTHING, related_name='posiciones')
    puntos = models.IntegerField()
    partidosJugados = models.IntegerField()
    partidosGanados = models.IntegerField()
    partidosEmpatados = models.IntegerField()
    partidosPerdidos = models.IntegerField()
    golesFavor = models.IntegerField()
    golesContra = models.IntegerField()
    estadistica = models.ForeignKey(EstadisticaEquipo, on_delete=models.CASCADE, related_name='posiciones')
