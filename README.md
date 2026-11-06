# Equipo A — Taller 3: planificación de procesos

Entrega de la etapa 03: comparación de FIFO/FCFS, SJF, SRTF y Round Robin para dos cargas de trabajo. Cada ejercicio reúne diagramas de Gantt, métricas y una conclusión comparativa.

## Ejercicios

| Ejercicio | Desarrollo y comparación | Archivos de entrega |
|---|---|---|
| 1 · Procesos mixtos · RR q=3 | [Ver ejercicio 1](docs/taller3/ejercicio1/README.md) | [Excel FIFO/SJF](docs/taller3/ejercicio1/Ejercicio_1.xlsx), [SRTF](docs/taller3/ejercicio1/srtf.md), [RR y cola](docs/taller3/ejercicio1/round_robin.md), [conclusión conjunta](docs/taller3/ejercicio1/comparacion.md) |
| 2 · Llegadas continuas · RR q=2 | [Ver ejercicio 2](docs/taller3/ejercicio2/README.md) | [Excel de los cuatro algoritmos](docs/taller3/ejercicio2/Ejercicio_2.xlsx), [conclusión conjunta](docs/taller3/ejercicio2/Conclusion_Ejercicio_2.docx) |

## Integrantes y aportes

| Integrante | Desarrollo principal | Integración |
|---|---|---|
| José Palma | Ejercicio 1: SRTF y RR q=3; decisiones y reincorporaciones | Revisión con las tablas de Darío |
| Darío Leal | Ejercicio 1: FIFO y SJF, métricas y promedios | Comparación de los cuatro con José |
| Luis Felipe | Ejercicio 2: SRTF y RR q=2; procesos cortos frente a largos y quantum | Revisión con las tablas de Nicolás |
| Nicolás Portilla | Ejercicio 2: FIFO y SJF, métricas y borrador de conclusión | Comparación de los cuatro con Luis |

La presentación común reúne los resultados sin borrar las responsabilidades. Los [aportes recibidos del ejercicio 2](docs/taller3/ejercicio2/README.md#aportes-y-revisión) se conservan separados de su entrega integrada; esta última incorpora las correcciones de revisión.

## Criterios de cálculo

Una ráfaga de CPU por proceso, sin E/S ni costo de cambio de contexto. Un proceso ejecuta a la vez. Intervalos [inicio, fin); desempates por llegada y luego identificador. En RR, las llegadas al vencer el quantum se encolan antes del proceso reincorporado.

Retorno = finalización − llegada; espera = retorno − ráfaga; respuesta = primer inicio − llegada. El análisis considera promedios, equidad, postergación e inanición.

## Verificación

Las pruebas usan Python 3 y solo biblioteca estándar:

```sh
python3 -m unittest discover -s tests -v
```

Incluyen comparación de SRTF y RR con simulaciones por unidad de tiempo y comprobación de los CSV. Los documentos Office se consultan directamente; no se necesitan para ejecutar las pruebas.

El [simulador del Taller 4](https://github.com/bgonzalezc/Planificador-de-procesos) es una entrega independiente.
