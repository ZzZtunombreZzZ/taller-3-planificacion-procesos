# Round Robin (quantum = 3) — Ejercicio 1

Cola FIFO de listos. Cada turno dura `min(3, restante)`. Si el proceso no termina, vuelve al **final** de la cola. Sin costo de cambio de contexto.

## Regla: llegada simultánea con el vencimiento del quantum

Si un proceso llega en el instante exacto en que vence el quantum de otro, **primero entra el recién llegado a la cola y después se reincorpora el proceso interrumpido**. Ocurre en este ejercicio en **t=3** (P4 llega y P1 vence: cola `[P2, P3, P4, P1]`), **t=6** (P7 antes que P2) y **t=9** (P10 antes que P3). Un proceso que llega *durante* el turno entra en su instante de llegada, también antes del interrumpido.

## Registro de turnos

| # | t inicial | Proceso | Restante antes | Duración | Restante después | Incorporados en (t_ini, t_fin] | Reincorporación | Cola al terminar el turno |
|---:|---:|---|---:|---:|---:|---|---|---|
| 1 | 0 | P1 | 10 | 3 | 7 | P2, P3, P4 | P1 vuelve al final (agotó quantum) | [P2, P3, P4, P1] |
| 2 | 3 | P2 | 4 | 3 | 1 | P5, P6, P7 | P2 vuelve al final (agotó quantum) | [P3, P4, P1, P5, P6, P7, P2] |
| 3 | 6 | P3 | 7 | 3 | 4 | P8, P9, P10 | P3 vuelve al final (agotó quantum) | [P4, P1, P5, P6, P7, P2, P8, P9, P10, P3] |
| 4 | 9 | P4 | 2 | 2 | 0 | — | P4 finaliza en t=11 | [P1, P5, P6, P7, P2, P8, P9, P10, P3] |
| 5 | 11 | P1 | 7 | 3 | 4 | — | P1 vuelve al final (agotó quantum) | [P5, P6, P7, P2, P8, P9, P10, P3, P1] |
| 6 | 14 | P5 | 9 | 3 | 6 | — | P5 vuelve al final (agotó quantum) | [P6, P7, P2, P8, P9, P10, P3, P1, P5] |
| 7 | 17 | P6 | 3 | 3 | 0 | — | P6 finaliza en t=20 | [P7, P2, P8, P9, P10, P3, P1, P5] |
| 8 | 20 | P7 | 6 | 3 | 3 | — | P7 vuelve al final (agotó quantum) | [P2, P8, P9, P10, P3, P1, P5, P7] |
| 9 | 23 | P2 | 1 | 1 | 0 | — | P2 finaliza en t=24 | [P8, P9, P10, P3, P1, P5, P7] |
| 10 | 24 | P8 | 1 | 1 | 0 | — | P8 finaliza en t=25 | [P9, P10, P3, P1, P5, P7] |
| 11 | 25 | P9 | 5 | 3 | 2 | — | P9 vuelve al final (agotó quantum) | [P10, P3, P1, P5, P7, P9] |
| 12 | 28 | P10 | 2 | 2 | 0 | — | P10 finaliza en t=30 | [P3, P1, P5, P7, P9] |
| 13 | 30 | P3 | 4 | 3 | 1 | — | P3 vuelve al final (agotó quantum) | [P1, P5, P7, P9, P3] |
| 14 | 33 | P1 | 4 | 3 | 1 | — | P1 vuelve al final (agotó quantum) | [P5, P7, P9, P3, P1] |
| 15 | 36 | P5 | 6 | 3 | 3 | — | P5 vuelve al final (agotó quantum) | [P7, P9, P3, P1, P5] |
| 16 | 39 | P7 | 3 | 3 | 0 | — | P7 finaliza en t=42 | [P9, P3, P1, P5] |
| 17 | 42 | P9 | 2 | 2 | 0 | — | P9 finaliza en t=44 | [P3, P1, P5] |
| 18 | 44 | P3 | 1 | 1 | 0 | — | P3 finaliza en t=45 | [P1, P5] |
| 19 | 45 | P1 | 1 | 1 | 0 | — | P1 finaliza en t=46 | [P5] |
| 20 | 46 | P5 | 3 | 3 | 0 | — | P5 finaliza en t=49 | [] |

Finalizaciones anticipadas (turno más corto que el quantum): P4 (2 u.), P2 (1 u.), P8 (1 u.), P10 (2 u.), P9 (2 u.), P3 (1 u.) y P1 (1 u.). P6, P7 y P5 terminan justo al agotar el quantum (3 u.). Total: 20 turnos, 10 finalizaciones y 10 reincorporaciones.

## Transiciones entre procesos (cambios de turno)

`P1[0-3] → P2[3-6] → P3[6-9] → P4[9-11] → P1[11-14] → P5[14-17] → P6[17-20] → P7[20-23] → P2[23-24] → P8[24-25] → P9[25-28] → P10[28-30] → P3[30-33] → P1[33-36] → P5[36-39] → P7[39-42] → P9[42-44] → P3[44-45] → P1[45-46] → P5[46-49]`

## Resultados

| Proceso | Llegada | Ráfaga | Inicio | Finalización | Espera | Retorno | Respuesta |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 10 | 0 | 46 | 36 | 46 | 0 |
| P2 | 1 | 4 | 3 | 24 | 19 | 23 | 2 |
| P3 | 2 | 7 | 6 | 45 | 36 | 43 | 4 |
| P4 | 3 | 2 | 9 | 11 | 6 | 8 | 6 |
| P5 | 4 | 9 | 14 | 49 | 36 | 45 | 10 |
| P6 | 5 | 3 | 17 | 20 | 12 | 15 | 12 |
| P7 | 6 | 6 | 20 | 42 | 30 | 36 | 14 |
| P8 | 7 | 1 | 24 | 25 | 17 | 18 | 17 |
| P9 | 8 | 5 | 25 | 44 | 31 | 36 | 17 |
| P10 | 9 | 2 | 28 | 30 | 19 | 21 | 19 |
| **Promedio** | | | | | **24.20** | **29.10** | **10.10** |

Espera promedio = 242/10 = **24.20**; retorno promedio = 291/10 = **29.10**; respuesta promedio = 101/10 = **10.10**.

Gantt: ver [gantt_rr.md](gantt_rr.md). Datos: [metricas_rr.csv](metricas_rr.csv).
