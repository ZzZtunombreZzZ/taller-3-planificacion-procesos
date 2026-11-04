"""Taller 3, ejercicio 1 (José Palma): verificación de SRTF y Round Robin q=3.

Capas:
  1. Referencia (docs/taller3/ejercicio1/referencia.py) contra un ORÁCULO
     tick a tick escrito aquí, independiente de la referencia.
  2. Resultados esperados fijos del ejercicio 1 (calculados a mano/oráculo).
  3. Verificación de los promedios de FIFO y SJF del Excel de Darío Leal.
Independiente del simulador: este repo (main) no tiene paquete `simulador`.
"""
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "docs", "taller3", "ejercicio1"))

import referencia as R                                        # noqa: E402

EJ1 = [("P1", 0, 10), ("P2", 1, 4), ("P3", 2, 7), ("P4", 3, 2), ("P5", 4, 9),
       ("P6", 5, 3), ("P7", 6, 6), ("P8", 7, 1), ("P9", 8, 5), ("P10", 9, 2)]

# (inicio, fin, espera, retorno, respuesta) por proceso
ESP_SRTF = {"P1": (0, 40, 30, 40, 0), "P2": (1, 5, 0, 4, 0), "P3": (24, 31, 22, 29, 22),
            "P4": (5, 7, 2, 4, 2), "P5": (40, 49, 36, 45, 36), "P6": (8, 11, 3, 6, 3),
            "P7": (18, 24, 12, 18, 12), "P8": (7, 8, 0, 1, 0), "P9": (13, 18, 5, 10, 5),
            "P10": (11, 13, 2, 4, 2)}
ESP_RR = {"P1": (0, 46, 36, 46, 0), "P2": (3, 24, 19, 23, 2), "P3": (6, 45, 36, 43, 4),
          "P4": (9, 11, 6, 8, 6), "P5": (14, 49, 36, 45, 10), "P6": (17, 20, 12, 15, 12),
          "P7": (20, 42, 30, 36, 14), "P8": (24, 25, 17, 18, 17), "P9": (25, 44, 31, 36, 17),
          "P10": (28, 30, 19, 21, 19)}
GANTT_SRTF = [("P1", 0, 1), ("P2", 1, 5), ("P4", 5, 7), ("P8", 7, 8), ("P6", 8, 11),
              ("P10", 11, 13), ("P9", 13, 18), ("P7", 18, 24), ("P3", 24, 31),
              ("P1", 31, 40), ("P5", 40, 49)]
GANTT_RR = [("P1", 0, 3), ("P2", 3, 6), ("P3", 6, 9), ("P4", 9, 11), ("P1", 11, 14),
            ("P5", 14, 17), ("P6", 17, 20), ("P7", 20, 23), ("P2", 23, 24), ("P8", 24, 25),
            ("P9", 25, 28), ("P10", 28, 30), ("P3", 30, 33), ("P1", 33, 36), ("P5", 36, 39),
            ("P7", 39, 42), ("P9", 42, 44), ("P3", 44, 45), ("P1", 45, 46), ("P5", 46, 49)]


def num(p):
    return int(p[1:])


def oraculo_srtf(procs):
    """Tick a tick: en cada unidad corre min (restante, llegada, id) entre los
    llegados; el que ya está en CPU conserva la CPU salvo restante estrictamente menor."""
    rest = {p: r for p, _, r in procs}
    lleg = {p: a for p, a, _ in procs}
    linea, cur, t = [], None, 0
    while any(rest.values()):
        lis = [p for p in rest if rest[p] > 0 and lleg[p] <= t]
        if lis:
            m = min(lis, key=lambda p: (rest[p], lleg[p], num(p)))
            if cur is None or rest[cur] == 0 or rest[m] < rest[cur]:
                cur = m
            rest[cur] -= 1
            linea.append(cur)
        else:
            linea.append(None)
        t += 1
    return linea


def oraculo_rr(procs, q):
    """Tick a tick con cola explícita; llegada en t entra antes que el interrumpido en t."""
    rest = {p: r for p, _, r in procs}
    cola, cur, uso, linea, t = [], None, 0, [], 0
    while any(rest.values()):
        for p, a, _ in sorted(procs, key=lambda x: (x[1], num(x[0]))):
            if a == t:
                cola.append(p)
        if cur is not None and (rest[cur] == 0 or uso == q):
            if rest[cur] > 0:
                cola.append(cur)
            cur = None
        if cur is None and cola:
            cur, uso = cola.pop(0), 0
        if cur is None:
            linea.append(None)
        else:
            rest[cur] -= 1
            uso += 1
            linea.append(cur)
        t += 1
    return linea


def a_linea(segs):
    out = []
    for p, a, b in segs:
        assert len(out) == a, "hueco o solape en el Gantt"
        out += [p] * (b - a)
    return out


def _a_segs(linea):
    segs = []
    for t, p in enumerate(linea):
        if segs and segs[-1][0] == p and segs[-1][2] == t:
            segs[-1] = (p, segs[-1][1], t + 1)
        else:
            segs.append((p, t, t + 1))
    return segs


class RefSRTF(unittest.TestCase):
    def test_gantt_completo_ejercicio1(self):
        segs, _ = R.srtf(EJ1)
        self.assertEqual(segs, GANTT_SRTF)

    def test_referencia_coincide_con_oraculo_tick_a_tick(self):
        segs, _ = R.srtf(EJ1)
        self.assertEqual(a_linea(segs), oraculo_srtf(EJ1))

    def test_unica_expropiacion_p1_por_p2_en_t1(self):
        segs, dec = R.srtf(EJ1)
        self.assertEqual([d for d in dec if d[1].startswith("expropia")],
                         [(1, "expropia a P1", "P2", {"P1": 9, "P2": 4})])
        self.assertEqual([s for s in segs if s[0] == "P1"], [("P1", 0, 1), ("P1", 31, 40)])

    def test_p1_reanuda_con_restante_9_y_desempata_con_p5(self):
        segs, dec = R.srtf(EJ1)
        t31 = [d for d in dec if d[0] == 31][0]
        self.assertEqual((t31[2], t31[3]), ("P1", {"P1": 9, "P5": 9}))

    def test_empate_de_restante_no_expropia(self):
        # P1 (rest 2) en CPU; llega P2 con 2: no expropia (mismo restante)
        segs, _ = R.srtf([("P1", 0, 4), ("P2", 2, 2)])
        self.assertEqual(segs, [("P1", 0, 4), ("P2", 4, 6)])

    def test_desempate_por_llegada_y_luego_id(self):
        segs, _ = R.srtf([("P1", 0, 3), ("P3", 1, 2), ("P2", 1, 2)])
        self.assertEqual([s[0] for s in segs], ["P1", "P2", "P3"])   # mismo restante+llegada: menor id
        segs, _ = R.srtf([("P1", 0, 5), ("P2", 1, 4), ("P3", 2, 3), ("P4", 3, 2)])
        self.assertEqual([s[0] for s in segs], ["P1", "P4", "P3", "P2"])   # todos empatan: nadie expropia
        segs, _ = R.srtf([("P1", 0, 8), ("P2", 1, 4), ("P3", 2, 3), ("P4", 3, 1)])
        self.assertEqual([s[0] for s in segs], ["P1", "P2", "P4", "P2", "P3", "P1"])

    def test_srtf_con_otros_datos_coincide_con_oraculo(self):
        casos = [[("P1", 0, 7), ("P2", 2, 4), ("P3", 4, 1), ("P4", 5, 4)],
                 [("P1", 3, 2), ("P2", 10, 1)],                       # CPU ociosa inicial y central
                 [("P1", 0, 6), ("P2", 0, 6), ("P3", 0, 2)]]
        for c in casos:
            with self.subTest(c=c):
                lin, t = [], 0
                for p, ini, fin in R.srtf(c)[0]:
                    lin += [None] * (ini - t) + [p] * (fin - ini)
                    t = fin
                self.assertEqual(lin, oraculo_srtf(c))


class RefRR(unittest.TestCase):
    def test_gantt_completo_ejercicio1(self):
        segs, _ = R.rr(EJ1)
        self.assertEqual(segs, GANTT_RR)

    def test_referencia_coincide_con_oraculo_tick_a_tick(self):
        segs, _ = R.rr(EJ1)
        self.assertEqual(a_linea(segs), oraculo_rr(EJ1, 3))

    def test_ningun_turno_supera_el_quantum_ni_la_rafaga(self):
        _, turnos = R.rr(EJ1)
        cons = {p: 0 for p, _, _ in EJ1}
        for x in turnos:
            self.assertLessEqual(x["dur"], 3)
            self.assertEqual(x["dur"], min(3, x["antes"]))
            self.assertEqual(x["despues"], x["antes"] - x["dur"])
            self.assertGreaterEqual(x["despues"], 0)
            cons[x["pid"]] += x["dur"]
        self.assertEqual(cons, {p: r for p, _, r in EJ1})
        self.assertEqual(len(turnos), 20)

    def test_orden_fifo_y_cola_tras_cada_turno(self):
        _, turnos = R.rr(EJ1)
        self.assertEqual(turnos[0]["cola"], ["P2", "P3", "P4", "P1"])
        self.assertEqual(turnos[1]["cola"], ["P3", "P4", "P1", "P5", "P6", "P7", "P2"])
        self.assertEqual(turnos[2]["cola"], ["P4", "P1", "P5", "P6", "P7", "P2", "P8", "P9", "P10", "P3"])
        self.assertEqual(turnos[-1]["cola"], [])

    def test_llegada_en_el_vencimiento_del_quantum_entra_antes(self):
        _, turnos = R.rr(EJ1)
        for idx, nuevo in ((0, "P4"), (1, "P7"), (2, "P10")):      # t=3, 6, 9
            c = turnos[idx]["cola"]
            self.assertLess(c.index(nuevo), c.index(turnos[idx]["pid"]))
        self.assertEqual(turnos[0]["nuevos"], ["P2", "P3", "P4"])

    def test_llegadas_durante_la_ejecucion(self):
        _, turnos = R.rr(EJ1)
        self.assertEqual([x["nuevos"] for x in turnos[:3]],
                         [["P2", "P3", "P4"], ["P5", "P6", "P7"], ["P8", "P9", "P10"]])

    def test_reincorporaciones_y_finalizacion_anticipada(self):
        _, turnos = R.rr(EJ1)
        self.assertEqual(sum(x["reinc"] for x in turnos), 10)
        anticipados = [x["pid"] for x in turnos if x["despues"] == 0 and x["dur"] < 3]
        self.assertEqual(anticipados, ["P4", "P2", "P8", "P10", "P9", "P3", "P1"])

    def test_rr_otros_datos_coincide_con_oraculo(self):
        casos = [[("P1", 0, 5), ("P2", 1, 3), ("P3", 3, 2)],
                 [("P1", 0, 4), ("P2", 0, 4), ("P3", 0, 1)],
                 [("P1", 0, 3), ("P2", 3, 3)]]                      # llega justo al terminar P1
        for c in casos:
            with self.subTest(c=c):
                self.assertEqual(a_linea(R.rr(c)[0]), oraculo_rr(c, 3))

    def test_llegada_exacta_al_agotar_quantum_caso_minimo(self):
        # P1 vence en t=3 y P2 llega en t=3: P2 debe ir antes que P1 reincorporado
        segs, turnos = R.rr([("P1", 0, 5), ("P2", 3, 1), ("P3", 1, 4)])
        self.assertEqual([s[0] for s in segs[:4]], ["P1", "P3", "P2", "P1"])


class Metricas(unittest.TestCase):
    def comprobar(self, segs, esperado):
        filas = {f["pid"]: f for f in R.metricas(EJ1, segs)}
        for p, (ini, fin, esp, ret, res) in esperado.items():
            f = filas[p]
            self.assertEqual((f["inicio"], f["fin"], f["espera"], f["retorno"], f["respuesta"]),
                             (ini, fin, esp, ret, res), p)
            self.assertEqual(f["retorno"], f["fin"] - f["llegada"])
            self.assertEqual(f["espera"], f["retorno"] - f["rafaga"])
            self.assertEqual(f["respuesta"], f["inicio"] - f["llegada"])
        return filas

    def test_srtf_metricas_individuales_y_promedios(self):
        pr = R.promedios(self.comprobar(R.srtf(EJ1)[0], ESP_SRTF).values())
        self.assertEqual((float(pr["espera"]), float(pr["retorno"]), float(pr["respuesta"])),
                         (11.2, 16.1, 8.2))

    def test_rr_metricas_individuales_y_promedios(self):
        pr = R.promedios(self.comprobar(R.rr(EJ1)[0], ESP_RR).values())
        self.assertEqual((float(pr["espera"]), float(pr["retorno"]), float(pr["respuesta"])),
                         (24.2, 29.1, 10.1))

    def test_invariantes_comunes(self):
        for segs in (R.srtf(EJ1)[0], R.rr(EJ1)[0]):
            lin = a_linea(segs)                                  # falla si hay hueco/solape
            self.assertEqual(len(lin), 49)
            self.assertEqual(segs[-1][2], 49)
            llegada = {p: a for p, a, _ in EJ1}
            for p, a, b in segs:
                self.assertGreaterEqual(a, llegada[p])
                self.assertLess(a, b)
            for p, _, r in EJ1:
                self.assertEqual(lin.count(p), r)

    def test_csv_generados_coinciden_con_referencia(self):
        import csv
        for nombre, segs in (("metricas_srtf.csv", R.srtf(EJ1)[0]), ("metricas_rr.csv", R.rr(EJ1)[0])):
            with open(os.path.join(R.AQUI, nombre), newline="") as f:
                filas = list(csv.DictReader(f))
            self.assertEqual(len(filas), 11)                     # 10 procesos + promedio
            for fila, m in zip(filas, R.metricas(EJ1, segs)):
                self.assertEqual((fila["Proceso"], int(fila["Inicio"]), int(fila["Finalizacion"]),
                                  int(fila["Espera"]), int(fila["Retorno"]), int(fila["Respuesta"])),
                                 (m["pid"], m["inicio"], m["fin"], m["espera"], m["retorno"], m["respuesta"]))

    def test_procesos_csv_son_los_datos_oficiales(self):
        self.assertEqual(R.cargar(), EJ1)
        self.assertEqual(sum(r for _, _, r in EJ1), 49)


class VerificacionExcelDario(unittest.TestCase):
    """Comprueba los promedios del Excel de Darío Leal (FIFO y SJF); no es trabajo de José Palma."""

    def test_promedios_fifo_y_sjf(self):
        for f, esp in ((R.fifo, (22.0, 26.9, 22.0)), (R.sjf, (14.4, 19.3, 14.4))):
            pr = R.promedios(R.metricas(EJ1, f(EJ1)))
            self.assertEqual((float(pr["espera"]), float(pr["retorno"]), float(pr["respuesta"])), esp)

    def test_secuencia_sjf(self):
        self.assertEqual([s[0] for s in R.sjf(EJ1)],
                         ["P1", "P8", "P4", "P10", "P6", "P2", "P9", "P7", "P3", "P5"])


if __name__ == "__main__":
    unittest.main()
