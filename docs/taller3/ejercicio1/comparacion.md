# Comparación SRTF vs Round Robin (q=3) — Ejercicio 1

| Métrica | SRTF | Round Robin q=3 | Mejor |
|---|---:|---:|---|
| Espera promedio | 11.20 | 24.20 | SRTF |
| Retorno promedio | 16.10 | 29.10 | SRTF |
| Respuesta promedio | 8.20 | 10.10 | SRTF |
| Espera máxima | 36 (P5) | 36 (P1) | Empate numérico (36) |
| Respuesta máxima | 36 (P5) | 19 (P10) | Round Robin |
| Cambios de CPU (segmentos) | 11 | 20 | SRTF |
| Finalización total | 49 | 49 | Igual (mismo trabajo, sin ocio) |

## Por proceso (espera)

| Proceso | Ráfaga | Espera SRTF | Espera RR | Respuesta SRTF | Respuesta RR |
|---|---:|---:|---:|---:|---:|
| P1 | 10 | 30 | 36 | 0 | 0 |
| P2 | 4 | 0 | 19 | 0 | 2 |
| P3 | 7 | 22 | 36 | 22 | 4 |
| P4 | 2 | 2 | 6 | 2 | 6 |
| P5 | 9 | 36 | 36 | 36 | 10 |
| P6 | 3 | 3 | 12 | 3 | 12 |
| P7 | 6 | 12 | 30 | 12 | 14 |
| P8 | 1 | 0 | 17 | 0 | 17 |
| P9 | 5 | 5 | 31 | 5 | 17 |
| P10 | 2 | 2 | 19 | 2 | 19 |

## Análisis

**Espera y retorno promedio.** SRTF es claramente mejor (11.20 vs 24.20 y 16.10 vs 29.10). Como no hay E/S, retorno = espera + ráfaga y la suma de ráfagas es la misma (49), por lo que la diferencia de retorno es exactamente la de espera (13.0). SRTF minimiza la espera promedio porque deja pasar primero a los trabajos cortos (P8, P4, P10, P6 esperan entre 0 y 3 u.).

**Respuesta.** Para estos datos SRTF también obtiene mejor promedio (8.20 vs 10.10), pero esto no es una propiedad general: se debe a que los procesos cortos llegan pronto y son despachados casi de inmediato. Su respuesta máxima es peor (36 u. para P5, que no recibe CPU hasta t=40). RR acota la respuesta máxima a 19 u. (P10) porque todo proceso recibe CPU en cuanto le llega su turno en la cola; es la mejor garantía de peor caso.

**Equidad e inanición.** RR reparte la CPU en turnos de 3 u.: nadie espera más de (n−1)·q por turno, y ningún proceso puede sufrir inanición. SRTF es injusto con los largos: P1 (ráfaga 10) es expropiado en t=1 y no vuelve hasta t=31; P5 (9) espera 36 u. y corre al final. Con estos datos todos terminan porque la carga es finita, pero si siguieran llegando procesos cortos, P1/P5/P3 podrían postergarse indefinidamente (riesgo de inanición propio de SRTF). En RR los largos pagan en cambio retornos altos (P1 46, P3 43, P5 45) por compartir la CPU, y P1 termina más tarde que con SRTF (46 vs 40).

**Efecto del quantum 3.** Con q=3, las ráfagas ≤3 (P4, P6, P8, P10) terminan en un solo turno, pero esperan detrás de los procesos de la cola (P8 espera 17 u. para una ráfaga de 1). Un quantum mayor se acercaría a FIFO (menos cambios, peor respuesta); uno menor mejoraría la respuesta a costa de más cambios de contexto (aquí sin costo por supuesto del enunciado, pero RR hace 20 turnos contra 11 segmentos de SRTF).

**Apropiación por restante vs. reparto por turnos.** SRTF decide según el trabajo pendiente (requiere conocer o estimar la ráfaga) y solo interrumpe cuando aparece un trabajo más corto (1 apropiación en este ejercicio). RR no necesita conocer ráfagas y interrumpe por tiempo (10 reincorporaciones) independientemente de cuánto falte.

**Conclusión.** Para los datos oficiales SRTF gana en espera promedio, retorno promedio, respuesta promedio y número de cambios; RR gana en peor caso de respuesta y en equidad/ausencia de inanición. Ninguno es superior en general: depende de si se prioriza el promedio (SRTF) o la previsibilidad para todos los procesos (RR).

## Estructura para la comparación grupal (FIFO y SJF: Darío Leal)

| Algoritmo | Espera prom. | Retorno prom. | Respuesta prom. | Responsable | Estado |
|---|---:|---:|---:|---|---|
| FIFO | 22.00 | 26.90 | 22.00 | Darío Leal | Valores de su Excel, verificados |
| SJF | 14.40 | 19.30 | 14.40 | Darío Leal | Valores de su Excel, verificados |
| SRTF | 11.20 | 16.10 | 8.20 | José Palma | Resuelto |
| Round Robin q=3 | 24.20 | 29.10 | 10.10 | José Palma | Resuelto |

Los gráficos y tablas de FIFO y SJF son de Darío Leal (`Ejercicio_1.xlsx`); aquí solo se recalcularon sus promedios con `referencia.py` para comprobar que coinciden.

### Lectura conjunta

- **Espera y retorno:** SRTF (11.20/16.10) < SJF (14.40/19.30) < FIFO (22.00/26.90) < RR (24.20/29.10). SRTF mejora a SJF porque puede expropiar a P1 (10 u.) en t=1 en vez de obligar a los cortos a esperarlo.
- **Respuesta:** SRTF (8.20) < RR (10.10) < SJF (14.40) < FIFO (22.00). RR supera a SJF y FIFO en respuesta aunque pierda en espera: reparte el primer acceso a la CPU.
- **FIFO y SJF** son no apropiativos: espera = respuesta, no hay reanudaciones. FIFO sufre el efecto convoy (los cortos esperan tras P1 y P3); SJF posterga a los largos (P5 espera 36).
- Todos terminan en t=49 (mismo trabajo, sin ocio): el algoritmo cambia el reparto de la espera, no el total ejecutado.
- RR queda último en promedios con este quantum, pero es el único con garantía de acceso periódico a la CPU.
