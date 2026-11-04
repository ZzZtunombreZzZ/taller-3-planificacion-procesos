# SRTF — Ejercicio 1

Shortest Remaining Time First (apropiativo). Criterio: en cada instante de decisión (llegada o terminación) corre el proceso listo con menor tiempo **restante**; empate: llegó antes, luego menor ID. Solo se expropia si el candidato tiene un restante **estrictamente menor** que el del proceso en CPU (un empate no expropia).

## Decisiones de planificación

| t | Evento | Listos (restante) | Elegido | Motivo |
|---:|---|---|---|---|
| 0 | despacho | P1=10 | P1 | menor restante |
| 1 | expropia a P1 | P1=9, P2=4 | P2 | menor restante |
| 5 | despacho | P1=9, P3=7, P4=2, P5=9, P6=3 | P4 | menor restante |
| 7 | despacho | P1=9, P3=7, P5=9, P6=3, P7=6, P8=1 | P8 | menor restante |
| 8 | despacho | P1=9, P3=7, P5=9, P6=3, P7=6, P9=5 | P6 | menor restante |
| 11 | despacho | P1=9, P3=7, P5=9, P7=6, P9=5, P10=2 | P10 | menor restante |
| 13 | despacho | P1=9, P3=7, P5=9, P7=6, P9=5 | P9 | menor restante |
| 18 | despacho | P1=9, P3=7, P5=9, P7=6 | P7 | menor restante |
| 24 | despacho | P1=9, P3=7, P5=9 | P3 | menor restante |
| 31 | despacho | P1=9, P5=9 | P1 | empate en restante: gana el que llegó antes / menor ID |
| 40 | despacho | P5=9 | P5 | menor restante |

## Llegadas que NO expropian (verificación explícita)

| t | Llega | Restante del proceso en CPU | Restante del que llega | ¿Expropia? |
|---:|---|---:|---:|---|
| 1 | P2 | P1=9 | 4 | Sí |
| 2 | P3 | P2=3 | 7 | No |
| 3 | P4 | P2=2 | 2 | No (empate: no expropia) |
| 4 | P5 | P2=1 | 9 | No |
| 5 | P6 | P2 terminó en t=5 | 3 | No hay proceso en CPU |
| 6 | P7 | P4=1 | 6 | No |
| 7 | P8 | P4 terminó en t=7 | 1 | No hay proceso en CPU |
| 8 | P9 | P8 terminó en t=8 | 5 | No hay proceso en CPU |
| 9 | P10 | P6=2 | 2 | No (empate: no expropia) |

## Interrupciones y reanudaciones

- **t=1: P1 es expropiado** (restante 9) por P2 (ráfaga 4 < 9). Es la única apropiación del ejercicio.
- **t=31: P1 se reanuda** (restante 9) y termina en t=40. P5 (restante 9) llegó en t=4, P1 en t=0: empate de restante=9 y gana P1 por haber llegado antes.
- t=3: P4 (2) llega mientras P2 tiene restante 2: **empate, no expropia** (P2 llegó antes).
- t=7: P8 (1) llega justo cuando P4 termina: se despacha de inmediato.
- Ningún otro proceso se interrumpe: cada uno corre hasta terminar.

## Resultados

| Proceso | Llegada | Ráfaga | Inicio | Finalización | Espera | Retorno | Respuesta |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 10 | 0 | 40 | 30 | 40 | 0 |
| P2 | 1 | 4 | 1 | 5 | 0 | 4 | 0 |
| P3 | 2 | 7 | 24 | 31 | 22 | 29 | 22 |
| P4 | 3 | 2 | 5 | 7 | 2 | 4 | 2 |
| P5 | 4 | 9 | 40 | 49 | 36 | 45 | 36 |
| P6 | 5 | 3 | 8 | 11 | 3 | 6 | 3 |
| P7 | 6 | 6 | 18 | 24 | 12 | 18 | 12 |
| P8 | 7 | 1 | 7 | 8 | 0 | 1 | 0 |
| P9 | 8 | 5 | 13 | 18 | 5 | 10 | 5 |
| P10 | 9 | 2 | 11 | 13 | 2 | 4 | 2 |
| **Promedio** | | | | | **11.20** | **16.10** | **8.20** |

Espera promedio = 112/10 = **11.20**; retorno promedio = 161/10 = **16.10**; respuesta promedio = 82/10 = **8.20**.

Gantt: ver [gantt_srtf.md](gantt_srtf.md). Datos: [metricas_srtf.csv](metricas_srtf.csv).
