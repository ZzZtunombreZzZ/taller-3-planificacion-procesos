# Validación — Ejercicio 1 (SRTF y Round Robin q=3)

Los resultados no se aceptaron por coincidir con una sola salida: se contrastaron **cuatro fuentes independientes**.

| Fuente | Qué es | SRTF | RR q=3 |
|---|---|:---:|:---:|
| `referencia.py` | Implementación por eventos (SRTF) y por turnos (RR) | Gantt y métricas | Gantt y métricas |
| Oráculo tick a tick (`tests/test_taller3_ejercicio1.py`) | Simula cada unidad de tiempo con reglas escritas por separado | Coincide | Coincide |
| Resolución manual de [srtf.md](srtf.md) y [round_robin.md](round_robin.md) | Decisiones por instante | Coincide | Coincide |

## Lista de comprobación (cada punto está cubierto por una prueba automática)

| # | Comprobación | SRTF | RR |
|---|---|:---:|:---:|
| 1 | Los 10 procesos aparecen en el Gantt | OK | OK |
| 2 | Ningún proceso ejecuta antes de su llegada | OK | OK |
| 3 | Cada proceso ejecuta exactamente su ráfaga | OK | OK |
| 4 | Un solo proceso en CPU por instante (sin solapes ni huecos) | OK | OK |
| 5 | Total ejecutado = 49 u. (ráfagas 10+4+7+2+9+3+6+1+5+2) | OK | OK |
| 6 | Sin tiempos restantes negativos | OK | OK (`despues ≥ 0` en los 20 turnos) |
| 7 | Último proceso finaliza en t=49 (P5 en ambos) | OK | OK |
| 8 | Retorno = Fin − Llegada; Espera = Retorno − Ráfaga; Respuesta = Inicio − Llegada | OK | OK |
| 9 | Promedios sobre los 10 procesos | OK | OK |
| 10 | Desempates (restante → llegada → ID) | OK | n/a (FIFO) |
| 11 | Ningún turno supera el quantum 3 | n/a | OK |
| 12 | Orden FIFO de la cola y regla de llegada en el vencimiento (t=3, 6, 9) | n/a | OK |

Comprobación aritmética adicional: Σ espera = 112 (SRTF) y 242 (RR); Σ retorno = Σ espera + 49 → 161 y 291 ✔; Σ respuesta = 82 y 101.

## Resultados validados

| Algoritmo | Espera prom. | Retorno prom. | Respuesta prom. | Segmentos Gantt |
|---|---:|---:|---:|---:|
| SRTF | 11.20 | 16.10 | 8.20 | 11 |
| Round Robin q=3 | 24.20 | 29.10 | 10.10 | 20 |

## Alcance

Este trabajo es el **Taller 3** (resolución manual y documentada del ejercicio 1) y es independiente del simulador del Taller 4 (PR #1). No se contrastó con ese simulador porque no forma parte de `main`. Cuando se integre, se puede reutilizar `tests/test_taller3_ejercicio1.py` como resultado esperado (Gantt y métricas de `referencia.py`).

## Reproducción

```
python3 -m unittest tests.test_taller3_ejercicio1 -v        # pruebas del ejercicio 1
python3 docs/taller3/ejercicio1/referencia.py               # regenera CSV y .md de resultados
```
