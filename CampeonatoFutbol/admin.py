from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Equipo, Jugador, Arbitro, Partido, Resultado, Inscripcion, EstadisticaEquipo, EstadisticaJugador, Campeonato, TablaPosiciones, ResultadoCampeonato])

