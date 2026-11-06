# Taller 3 — Ejercicio 1 (procesos mixtos): SRTF y Round Robin q=3

Responsable: José Palma. Alcance: **solo SRTF y Round Robin** del ejercicio 1 (Taller 3, no el simulador/interfaz del Taller 4). FIFO y SJF del ejercicio 1 corresponden a Darío Leal y se incluyen en el Excel de esta carpeta. El ejercicio 2 se documenta en [su propia carpeta](../ejercicio2/README.md): FIFO/SJF de Nicolás Portilla corregidos; SRTF y RR q=2 de Luis Felipe pendientes de integrar.

Supuestos: una ráfaga de CPU por proceso, sin cambio de contexto, sin E/S ni prioridades, un proceso a la vez. Empates: llegó antes, luego menor ID. Espera = tiempo en cola de listos = Retorno − Ráfaga.

## Resultado resumido

| Algoritmo | Espera prom. | Retorno prom. | Respuesta prom. |
|---|---:|---:|---:|
| SRTF | 11.20 | 16.10 | 8.20 |
| Round Robin q=3 | 24.20 | 29.10 | 10.10 |
| FIFO (Darío, verificado) | 22.00 | 26.90 | 22.00 |
| SJF (Darío, verificado) | 14.40 | 19.30 | 14.40 |

SRTF: `P1 P2 P4 P8 P6 P10 P9 P7 P3 P1 P5` (única expropiación: P1 por P2 en t=1).
RR: 20 turnos, termina en t=49 (P5).

## Archivos

| Archivo | Contenido |
|---|---|
| [procesos.csv](procesos.csv) | Datos oficiales (entrada común para todos los algoritmos) |
| [srtf.md](srtf.md) / [gantt_srtf.md](gantt_srtf.md) / [metricas_srtf.csv](metricas_srtf.csv) | Decisiones, Gantt y métricas SRTF |
| [round_robin.md](round_robin.md) / [gantt_rr.md](gantt_rr.md) / [metricas_rr.csv](metricas_rr.csv) | Registro de turnos y cola, Gantt y métricas RR |
| [comparacion.md](comparacion.md) | Comparación, conclusiones y tabla para el análisis grupal |
| [validacion.md](validacion.md) | Verificaciones y estado de la integración |
| [Ejercicio_1.xlsx](Ejercicio_1.xlsx) | Hojas FIFO y SJF de Darío Leal (Gantt y métricas) |
| `referencia.py`, `generar_docs.py` | Implementación de referencia independiente y generador de los `.md`/`.csv` |
| `../../../tests/test_taller3_ejercicio1.py` | Pruebas automáticas |

Los `.md` de resultados y los `.csv` se generan con `python3 docs/taller3/ejercicio1/referencia.py`; no editarlos a mano.
