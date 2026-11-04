"""Referencia independiente (Taller 3, ejercicio 1) para SRTF y Round Robin.

Independiente de cualquier simulador (solo biblioteca estándar).
SRTF avanza por eventos (llegadas / terminaciones); RR por turnos.
Uso:  python3 docs/taller3/ejercicio1/referencia.py   (regenera CSV y .md)
"""
import csv
import os
import re
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
QUANTUM = 3


def cargar(ruta=None):
    with open(ruta or os.path.join(AQUI, "procesos.csv"), newline="") as f:
        return [(r["Proceso"], int(r["Llegada"]), int(r["Rafaga"]))
                for r in csv.DictReader(f)]


def nat(pid):
    return int(re.sub(r"\D", "", pid))


def srtf(procs):
    """Devuelve (segmentos, decisiones). segmento=(pid, ini, fin);
    decision=(t, evento, pid, restantes_listos). Empate: restante, llegada, ID.
    Solo se expropia si el restante del candidato es ESTRICTAMENTE menor."""
    rest = {p: r for p, _, r in procs}
    lleg = {p: a for p, a, _ in procs}
    t, act, segs, dec = 0, None, [], []
    llegadas = sorted({a for _, a, _ in procs})
    hecho = set()
    while len(hecho) < len(procs):
        listos = [p for p in rest if lleg[p] <= t and p not in hecho]
        if not listos:
            t = min(a for a in llegadas if a > t)
            continue
        mejor = min(listos, key=lambda p: (rest[p], lleg[p], nat(p)))
        if act is None:
            ev = "despacho"
            act = mejor
        elif rest[mejor] < rest[act]:
            ev = f"expropia a {act}"
            act = mejor
        else:
            ev = None
        if ev:
            dec.append((t, ev, act, {p: rest[p] for p in listos}))
        sig = [a for a in llegadas if a > t]
        t_fin = t + rest[act]
        t_next = min([t_fin] + sig)
        if segs and segs[-1][0] == act and segs[-1][2] == t:
            segs[-1] = (act, segs[-1][1], t_next)
        else:
            segs.append((act, t, t_next))
        rest[act] -= t_next - t
        t = t_next
        if rest[act] == 0:
            hecho.add(act)
            act = None
    return segs, dec


def fifo(procs):
    """Solo verificacion del Excel de Dario Leal (su trabajo): FIFO sin apropiacion."""
    t, segs = 0, []
    for p, a, r in sorted(procs, key=lambda x: (x[1], nat(x[0]))):
        t = max(t, a)
        segs.append((p, t, t + r))
        t += r
    return segs


def sjf(procs):
    """Solo verificacion del Excel de Dario Leal: SJF no apropiativo (rafaga, llegada, ID)."""
    pend, t, segs = list(procs), 0, []
    while pend:
        lis = [x for x in pend if x[1] <= t] or [min(pend, key=lambda x: x[1])]
        x = min(lis, key=lambda x: (x[2], x[1], nat(x[0])))
        t = max(t, x[1])
        segs.append((x[0], t, t + x[2]))
        t += x[2]
        pend.remove(x)
    return segs


def rr(procs, q=QUANTUM):
    """Devuelve (segmentos, turnos). Una llegada en el instante exacto en que
    vence el quantum entra a la cola ANTES que el proceso interrumpido."""
    rest = {p: r for p, _, r in procs}
    pend = sorted(procs, key=lambda x: (x[1], nat(x[0])))
    cola, t, segs, turnos = [], 0, [], []

    def admitir(hasta):
        nuevos = []
        while pend and pend[0][1] <= hasta:
            p = pend.pop(0)[0]
            cola.append(p)
            nuevos.append(p)
        return nuevos

    admitir(0)
    while cola or pend:
        if not cola:
            t = pend[0][1]
            admitir(t)
            continue
        p = cola.pop(0)
        antes = rest[p]
        d = min(q, antes)
        rest[p] -= d
        t_fin = t + d
        nuevos = admitir(t_fin)
        reinc = rest[p] > 0
        if reinc:
            cola.append(p)
        if segs and segs[-1][0] == p and segs[-1][2] == t:
            segs[-1] = (p, segs[-1][1], t_fin)
        else:
            segs.append((p, t, t_fin))
        turnos.append(dict(t=t, pid=p, antes=antes, dur=d, despues=rest[p],
                           nuevos=nuevos, reinc=reinc, cola=list(cola), fin=t_fin))
        t = t_fin
    return segs, turnos


def metricas(procs, segs):
    ini, fin = {}, {}
    for p, a, b in segs:
        ini.setdefault(p, a)
        fin[p] = b
    filas = []
    for p, ll, r in procs:
        ret = fin[p] - ll
        filas.append(dict(pid=p, llegada=ll, rafaga=r, inicio=ini[p], fin=fin[p],
                          espera=ret - r, retorno=ret, respuesta=ini[p] - ll))
    return filas


def promedios(filas):
    n = len(filas)
    return {k: Fraction(sum(f[k] for f in filas), n)
            for k in ("espera", "retorno", "respuesta")}


def cola_txt(c):
    return "[" + ", ".join(c) + "]" if c else "[]"


def escribir_csv(nombre, filas):
    with open(os.path.join(AQUI, nombre), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Proceso", "Llegada", "Rafaga", "Inicio", "Finalizacion",
                    "Espera", "Retorno", "Respuesta"])
        for x in filas:
            w.writerow([x["pid"], x["llegada"], x["rafaga"], x["inicio"], x["fin"],
                        x["espera"], x["retorno"], x["respuesta"]])
        pr = promedios(filas)
        w.writerow(["Promedio", "", "", "", "", f"{float(pr['espera']):.2f}",
                    f"{float(pr['retorno']):.2f}", f"{float(pr['respuesta']):.2f}"])


def tabla_md(filas):
    s = ["| Proceso | Llegada | Ráfaga | Inicio | Finalización | Espera | Retorno | Respuesta |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for x in filas:
        s.append(f"| {x['pid']} | {x['llegada']} | {x['rafaga']} | {x['inicio']} | "
                 f"{x['fin']} | {x['espera']} | {x['retorno']} | {x['respuesta']} |")
    pr = promedios(filas)
    s.append(f"| **Promedio** | | | | | **{float(pr['espera']):.2f}** | "
             f"**{float(pr['retorno']):.2f}** | **{float(pr['respuesta']):.2f}** |")
    return "\n".join(s)


def gantt_md(segs, titulo):
    l = [f"## Diagrama de Gantt {titulo}", "", "```mermaid", "gantt",
         "    dateFormat X", "    axisFormat %s", f"    title Gantt {titulo} (eje = unidades de tiempo)"]
    orden = []
    for p, _, _ in segs:
        if p not in orden:
            orden.append(p)
    for p in sorted(orden, key=nat):
        l.append(f"    section {p}")
        for q, a, b in segs:
            if q == p:
                l.append(f"    {p} t{a}-{b} :{a}, {b}")
    l += ["```", "", "Secuencia: `" + " ".join(p for p, _, _ in segs) + "`", "",
          "| # | Proceso | Inicio | Fin | Duración |", "|---:|---|---:|---:|---:|"]
    for i, (p, a, b) in enumerate(segs, 1):
        l.append(f"| {i} | {p} | {a} | {b} | {b - a} |")
    tiempos = []
    for p, a, b in segs:
        tiempos += [p] * (b - a)
    l += ["", "Línea de tiempo (una columna por unidad; la columna `t` es el instante inicial):", "", "```",
          "t  : " + " ".join(f"{i:>3}" for i in range(len(tiempos))),
          "CPU: " + " ".join(f"{p:>3}" for p in tiempos),
          f"fin: t={len(tiempos)}", "```"]
    return "\n".join(l)


if __name__ == "__main__":
    P = cargar()
    gs, dec = srtf(P)
    gr, turnos = rr(P)
    ms, mr = metricas(P, gs), metricas(P, gr)
    escribir_csv("metricas_srtf.csv", ms)
    escribir_csv("metricas_rr.csv", mr)
    import generar_docs
    generar_docs.todo(P, gs, dec, gr, turnos, ms, mr)
