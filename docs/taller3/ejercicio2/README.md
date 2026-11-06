# Ejercicio 2 — FIFO y SJF

Responsable: Nicolás Portilla. SRTF y Round Robin q=2, a cargo de Luis Felipe, pendientes de integrar.

Una ráfaga por proceso, sin E/S ni costo por cambio de contexto. Empates por llegada y luego identificador. Intervalos [inicio, fin): fin es el instante de finalización.

## FIFO

| Proceso | Llegada | Ráfaga | Inicio | Finalización | Espera | Retorno | Respuesta |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 12 | 0 | 12 | 0 | 12 | 0 |
| P2 | 1 | 3 | 12 | 15 | 11 | 14 | 11 |
| P3 | 2 | 1 | 15 | 16 | 13 | 14 | 13 |
| P4 | 3 | 8 | 16 | 24 | 13 | 21 | 13 |
| P5 | 4 | 2 | 24 | 26 | 20 | 22 | 20 |
| P6 | 5 | 6 | 26 | 32 | 21 | 27 | 21 |
| P7 | 6 | 1 | 32 | 33 | 26 | 27 | 26 |
| P8 | 7 | 4 | 33 | 37 | 26 | 30 | 26 |
| P9 | 8 | 2 | 37 | 39 | 29 | 31 | 29 |
| P10 | 9 | 5 | 39 | 44 | 30 | 35 | 30 |
| **Promedio** | | | | | **18.90** | **23.30** | **18.90** |

### Gantt por intervalos

| Proceso | Inicio | Fin |
|---|---:|---:|
| P1 | 0 | 12 |
| P2 | 12 | 15 |
| P3 | 15 | 16 |
| P4 | 16 | 24 |
| P5 | 24 | 26 |
| P6 | 26 | 32 |
| P7 | 32 | 33 |
| P8 | 33 | 37 |
| P9 | 37 | 39 |
| P10 | 39 | 44 |

## SJF

| Proceso | Llegada | Ráfaga | Inicio | Finalización | Espera | Retorno | Respuesta |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 12 | 0 | 12 | 0 | 12 | 0 |
| P2 | 1 | 3 | 18 | 21 | 17 | 20 | 17 |
| P3 | 2 | 1 | 12 | 13 | 10 | 11 | 10 |
| P4 | 3 | 8 | 36 | 44 | 33 | 41 | 33 |
| P5 | 4 | 2 | 14 | 16 | 10 | 12 | 10 |
| P6 | 5 | 6 | 30 | 36 | 25 | 31 | 25 |
| P7 | 6 | 1 | 13 | 14 | 7 | 8 | 7 |
| P8 | 7 | 4 | 21 | 25 | 14 | 18 | 14 |
| P9 | 8 | 2 | 16 | 18 | 8 | 10 | 8 |
| P10 | 9 | 5 | 25 | 30 | 16 | 21 | 16 |
| **Promedio** | | | | | **14.00** | **18.40** | **14.00** |

### Gantt por intervalos

| Proceso | Inicio | Fin |
|---|---:|---:|
| P1 | 0 | 12 |
| P3 | 12 | 13 |
| P7 | 13 | 14 |
| P5 | 14 | 16 |
| P9 | 16 | 18 |
| P2 | 18 | 21 |
| P8 | 21 | 25 |
| P10 | 25 | 30 |
| P6 | 30 | 36 |
| P4 | 36 | 44 |

## Conclusión

FIFO obtiene retorno promedio 23,30, espera 18,90 y respuesta 18,90. SJF obtiene retorno 18,40, espera 14,00 y respuesta 14,00. SJF reduce la espera y la respuesta promedio en 4,90 unidades. Ambos terminan en t=44, la suma de las ráfagas. En estos algoritmos no apropiativos y sin E/S, espera y respuesta coinciden.

P4 llega en t=3. En FIFO ejecuta [16,24), con espera y respuesta de 13 unidades y retorno de 21. En SJF ejecuta [36,44), con espera y respuesta de 33 y retorno de 41. SJF lo posterga para atender ráfagas más cortas. P4 sí termina en esta carga finita: hay postergación, no inanición efectiva; un flujo continuo de trabajos cortos podría provocar inanición.

SJF mejora los promedios frente a FIFO para estos datos, a costa de retrasar procesos largos como P4. FIFO respeta el orden de llegada y evita esa postergación por tamaño, pero los trabajos cortos sufren el efecto convoy. La comparación con SRTF y Round Robin q=2, el registro de reincorporaciones y el análisis del quantum quedan pendientes de integrar con la parte de Luis Felipe. Cada columna del Gantt representa [t,t+1): el instante de finalización es el extremo final, no la etiqueta de la última casilla.
