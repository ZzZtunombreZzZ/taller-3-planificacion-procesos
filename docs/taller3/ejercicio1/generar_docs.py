"""Genera los .md de resultados a partir de referencia.py (no editar a mano los .md de datos)."""
import os
import referencia as R

AQUI = R.AQUI


def w(nombre, txt):
    with open(os.path.join(AQUI, nombre), "w", encoding="utf-8", newline="\n") as f:
        f.write(txt.rstrip() + "\n")


def f2(x):
    return f"{float(x):.2f}"


def todo(P, gs, dec, gr, turnos, ms, mr):
    ps, pr = R.promedios(ms), R.promedios(mr)
    pf, pj = R.promedios(R.metricas(P, R.fifo(P))), R.promedios(R.metricas(P, R.sjf(P)))
    w("gantt_srtf.md", "# Gantt SRTF — Ejercicio 1\n\n" + R.gantt_md(gs, "SRTF"))
    w("gantt_rr.md", "# Gantt Round Robin (q=3) — Ejercicio 1\n\n" + R.gantt_md(gr, "Round Robin q=3"))

    s = ["# SRTF — Ejercicio 1", "",
         "Shortest Remaining Time First (apropiativo). Criterio: en cada instante de decisión "
         "(llegada o terminación) corre el proceso listo con menor tiempo **restante**; "
         "empate: llegó antes, luego menor ID. Solo se expropia si el candidato tiene un restante "
         "**estrictamente menor** que el del proceso en CPU (un empate no expropia).", "",
         "## Decisiones de planificación", "",
         "| t | Evento | Listos (restante) | Elegido | Motivo |", "|---:|---|---|---|---|"]
    for t, ev, pid, listos in dec:
        lt = ", ".join(f"{p}={v}" for p, v in sorted(listos.items(), key=lambda kv: R.nat(kv[0])))
        mot = ("menor restante" if sorted(v for v in listos.values()).count(listos[pid]) == 1
               else "empate en restante: gana el que llegó antes / menor ID")
        s.append(f"| {t} | {ev} | {lt} | {pid} | {mot} |")
    s += ["", "## Llegadas que NO expropian (verificación explícita)", "",
          "| t | Llega | Restante del proceso en CPU | Restante del que llega | ¿Expropia? |",
          "|---:|---|---:|---:|---|"]
    corriendo = {}
    for p, a, b in gs:
        for t in range(a, b):
            corriendo[t] = p
    rem = {}
    cum = {p: 0 for p, _, _ in P}
    for t in range(49):
        rem[t] = {p: r - cum[p] for p, _, r in P}
        cum[corriendo[t]] += 1
    for p, a, r in P:
        if a == 0:
            continue
        cur = corriendo[a - 1]
        if rem[a][cur] == 0:
            s.append(f"| {a} | {p} | {cur} terminó en t={a} | {r} | No hay proceso en CPU |")
            continue
        exp = "Sí" if r < rem[a][cur] else "No"
        extra = " (empate: no expropia)" if r == rem[a][cur] else ""
        s.append(f"| {a} | {p} | {cur}={rem[a][cur]} | {r} | {exp}{extra} |")
    s += ["", "## Interrupciones y reanudaciones", "",
          "- **t=1: P1 es expropiado** (restante 9) por P2 (ráfaga 4 < 9). Es la única apropiación del ejercicio.",
          "- **t=31: P1 se reanuda** (restante 9) y termina en t=40. P5 (restante 9) llegó en t=4, P1 en t=0: "
          "empate de restante=9 y gana P1 por haber llegado antes.",
          "- t=3: P4 (2) llega mientras P2 tiene restante 2: **empate, no expropia** (P2 llegó antes).",
          "- t=7: P8 (1) llega justo cuando P4 termina: se despacha de inmediato.",
          "- Ningún otro proceso se interrumpe: cada uno corre hasta terminar.", "",
          "## Resultados", "", R.tabla_md(ms), "",
          f"Espera promedio = {sum(x['espera'] for x in ms)}/10 = **{f2(ps['espera'])}**; "
          f"retorno promedio = {sum(x['retorno'] for x in ms)}/10 = **{f2(ps['retorno'])}**; "
          f"respuesta promedio = {sum(x['respuesta'] for x in ms)}/10 = **{f2(ps['respuesta'])}**.", "",
          "Gantt: ver [gantt_srtf.md](gantt_srtf.md). Datos: [metricas_srtf.csv](metricas_srtf.csv)."]
    w("srtf.md", "\n".join(s))

    s = ["# Round Robin (quantum = 3) — Ejercicio 1", "",
         "Cola FIFO de listos. Cada turno dura `min(3, restante)`. Si el proceso no termina, "
         "vuelve al **final** de la cola. Sin costo de cambio de contexto.", "",
         "## Regla: llegada simultánea con el vencimiento del quantum", "",
         "Si un proceso llega en el instante exacto en que vence el quantum de otro, **primero entra "
         "el recién llegado a la cola y después se reincorpora el proceso interrumpido**. "
         "Ocurre en este ejercicio en **t=3** (P4 llega y P1 vence: cola `[P2, P3, P4, P1]`), "
         "**t=6** (P7 antes que P2) y **t=9** (P10 antes que P3). "
         "Un proceso que llega *durante* el turno entra en su instante de llegada, también antes del interrumpido.", "",
         "## Registro de turnos", "",
         "| # | t inicial | Proceso | Restante antes | Duración | Restante después | Incorporados en (t_ini, t_fin] | Reincorporación | Cola al terminar el turno |",
         "|---:|---:|---|---:|---:|---:|---|---|---|"]
    for i, x in enumerate(turnos, 1):
        nuevos = ", ".join(x["nuevos"]) or "—"
        if x["reinc"]:
            re_ = f"{x['pid']} vuelve al final (agotó quantum)"
        else:
            re_ = f"{x['pid']} finaliza en t={x['fin']}"
        s.append(f"| {i} | {x['t']} | {x['pid']} | {x['antes']} | {x['dur']} | {x['despues']} | "
                 f"{nuevos} | {re_} | {R.cola_txt(x['cola'])} |")
    s += ["", "Finalizaciones anticipadas (turno más corto que el quantum): P4 (2 u.), P2 (1 u.), P8 (1 u.), "
          "P10 (2 u.), P9 (2 u.), P3 (1 u.) y P1 (1 u.). P6, P7 y P5 terminan justo al agotar el quantum "
          "(3 u.). Total: 20 turnos, 10 finalizaciones y 10 reincorporaciones.", "",
          "## Transiciones entre procesos (cambios de turno)", "",
          "`" + " → ".join(f"{p}[{a}-{b}]" for p, a, b in gr) + "`", "",
          "## Resultados", "", R.tabla_md(mr), "",
          f"Espera promedio = {sum(x['espera'] for x in mr)}/10 = **{f2(pr['espera'])}**; "
          f"retorno promedio = {sum(x['retorno'] for x in mr)}/10 = **{f2(pr['retorno'])}**; "
          f"respuesta promedio = {sum(x['respuesta'] for x in mr)}/10 = **{f2(pr['respuesta'])}**.", "",
          "Gantt: ver [gantt_rr.md](gantt_rr.md). Datos: [metricas_rr.csv](metricas_rr.csv)."]
    w("round_robin.md", "\n".join(s))

    mxe = lambda m, k: max(m, key=lambda x: x[k])
    s = ["# Comparación SRTF vs Round Robin (q=3) — Ejercicio 1", "",
         "| Métrica | SRTF | Round Robin q=3 | Mejor |", "|---|---:|---:|---|",
         f"| Espera promedio | {f2(ps['espera'])} | {f2(pr['espera'])} | SRTF |",
         f"| Retorno promedio | {f2(ps['retorno'])} | {f2(pr['retorno'])} | SRTF |",
         f"| Respuesta promedio | {f2(ps['respuesta'])} | {f2(pr['respuesta'])} | "
         f"{'SRTF' if ps['respuesta'] < pr['respuesta'] else 'Round Robin'} |",
         f"| Espera máxima | {mxe(ms,'espera')['espera']} ({mxe(ms,'espera')['pid']}) | "
         f"{mxe(mr,'espera')['espera']} ({mxe(mr,'espera')['pid']}) | Empate numérico (36) |",
         f"| Respuesta máxima | {mxe(ms,'respuesta')['respuesta']} ({mxe(ms,'respuesta')['pid']}) | "
         f"{mxe(mr,'respuesta')['respuesta']} ({mxe(mr,'respuesta')['pid']}) | Round Robin |",
         f"| Cambios de CPU (segmentos) | {len(gs)} | {len(gr)} | SRTF |",
         "| Finalización total | 49 | 49 | Igual (mismo trabajo, sin ocio) |", "",
         "## Por proceso (espera)", "", "| Proceso | Ráfaga | Espera SRTF | Espera RR | Respuesta SRTF | Respuesta RR |",
         "|---|---:|---:|---:|---:|---:|"]
    for a, b in zip(ms, mr):
        s.append(f"| {a['pid']} | {a['rafaga']} | {a['espera']} | {b['espera']} | {a['respuesta']} | {b['respuesta']} |")
    s += ["", "## Análisis", "",
          "**Espera y retorno promedio.** SRTF es claramente mejor (11.20 vs 24.20 y 16.10 vs 29.10). "
          "Como no hay E/S, retorno = espera + ráfaga y la suma de ráfagas es la misma (49), "
          "por lo que la diferencia de retorno es exactamente la de espera (13.0). "
          "SRTF minimiza la espera promedio porque deja pasar primero a los trabajos cortos "
          "(P8, P4, P10, P6 esperan entre 0 y 3 u.).", "",
          "**Respuesta.** Para estos datos SRTF también obtiene mejor promedio (8.20 vs 10.10), "
          "pero esto no es una propiedad general: se debe a que los procesos cortos llegan pronto y "
          "son despachados casi de inmediato. Su respuesta máxima es peor (36 u. para P5, que no recibe CPU hasta t=40). "
          "RR acota la respuesta máxima a 19 u. (P10) porque todo proceso recibe CPU en cuanto "
          "le llega su turno en la cola; es la mejor garantía de peor caso.", "",
          "**Equidad e inanición.** RR reparte la CPU en turnos de 3 u.: nadie espera más de "
          "(n−1)·q por turno, y ningún proceso puede sufrir inanición. SRTF es injusto con los largos: "
          "P1 (ráfaga 10) es expropiado en t=1 y no vuelve hasta t=31; P5 (9) espera 36 u. y corre al final. "
          "Con estos datos todos terminan porque la carga es finita, pero si siguieran llegando "
          "procesos cortos, P1/P5/P3 podrían postergarse indefinidamente (riesgo de inanición propio de SRTF). "
          "En RR los largos pagan en cambio retornos altos (P1 46, P3 43, P5 45) por compartir la CPU, "
          "y P1 termina más tarde que con SRTF (46 vs 40).", "",
          "**Efecto del quantum 3.** Con q=3, las ráfagas ≤3 (P4, P6, P8, P10) terminan en un solo turno, "
          "pero esperan detrás de los procesos de la cola (P8 espera 17 u. para una ráfaga de 1). "
          "Un quantum mayor se acercaría a FIFO (menos cambios, peor respuesta); uno menor mejoraría la respuesta "
          "a costa de más cambios de contexto (aquí sin costo por supuesto del enunciado, pero RR hace 20 turnos contra 11 segmentos de SRTF).", "",
          "**Apropiación por restante vs. reparto por turnos.** SRTF decide según el trabajo pendiente "
          "(requiere conocer o estimar la ráfaga) y solo interrumpe cuando aparece un trabajo más corto "
          "(1 apropiación en este ejercicio). RR no necesita conocer ráfagas y interrumpe por tiempo (10 reincorporaciones) "
          "independientemente de cuánto falte.", "",
          "**Conclusión.** Para los datos oficiales SRTF gana en espera promedio, retorno promedio, "
          "respuesta promedio y número de cambios; RR gana en peor caso de respuesta y en equidad/ausencia de "
          "inanición. Ninguno es superior en general: depende de si se prioriza el promedio (SRTF) o la "
          "previsibilidad para todos los procesos (RR).", "",
          "## Estructura para la comparación grupal (FIFO y SJF: Darío Leal)", "",
          "| Algoritmo | Espera prom. | Retorno prom. | Respuesta prom. | Responsable | Estado |",
          "|---|---:|---:|---:|---|---|",
          f"| FIFO | {f2(pf['espera'])} | {f2(pf['retorno'])} | {f2(pf['respuesta'])} | Darío Leal | Valores de su Excel, verificados |",
          f"| SJF | {f2(pj['espera'])} | {f2(pj['retorno'])} | {f2(pj['respuesta'])} | Darío Leal | Valores de su Excel, verificados |",
          f"| SRTF | {f2(ps['espera'])} | {f2(ps['retorno'])} | {f2(ps['respuesta'])} | José Palma | Resuelto |",
          f"| Round Robin q=3 | {f2(pr['espera'])} | {f2(pr['retorno'])} | {f2(pr['respuesta'])} | José Palma | Resuelto |", "",
          "Los gráficos y tablas de FIFO y SJF son de Darío Leal (`Ejercicio_1.xlsx`); aquí solo se "
          "recalcularon sus promedios con `referencia.py` para comprobar que coinciden.", "",
          "### Lectura conjunta", "",
          "- **Espera y retorno:** SRTF (11.20/16.10) < SJF (14.40/19.30) < FIFO (22.00/26.90) < RR (24.20/29.10). "
          "SRTF mejora a SJF porque puede expropiar a P1 (10 u.) en t=1 en vez de obligar a los cortos a esperarlo.",
          "- **Respuesta:** SRTF (8.20) < RR (10.10) < SJF (14.40) < FIFO (22.00). RR supera a SJF y FIFO "
          "en respuesta aunque pierda en espera: reparte el primer acceso a la CPU.",
          "- **FIFO y SJF** son no apropiativos: espera = respuesta, no hay reanudaciones. "
          "FIFO sufre el efecto convoy (los cortos esperan tras P1 y P3); SJF posterga a los largos (P5 espera 36).",
          "- Todos terminan en t=49 (mismo trabajo, sin ocio): el algoritmo cambia el reparto de la espera, no el total ejecutado.",
          "- RR queda último en promedios con este quantum, pero es el único con garantía de acceso periódico a la CPU."]
    w("comparacion.md", "\n".join(s))
