"""Verifica los resultados publicados del ejercicio 2, incluidos los de Luis."""
import csv
from pathlib import Path
import unittest

from test_taller3_ejercicio1 import oraculo_rr, oraculo_srtf


DATOS = [(f"P{i + 1}", i, b)
         for i, b in enumerate([12, 3, 1, 8, 2, 6, 1, 4, 2, 5])]
CARPETA = Path(__file__).resolve().parents[1] / "docs/taller3/ejercicio2"


class Ejercicio2(unittest.TestCase):
    def test_csv_coinciden_con_planificacion_independiente(self):
        fifo = [p for p, _, b in DATOS for _ in range(b)]
        orden_sjf = ["P1", "P3", "P7", "P5", "P9", "P2", "P8", "P10", "P6", "P4"]
        rafagas = {p: b for p, _, b in DATOS}
        sjf = [p for p in orden_sjf for _ in range(rafagas[p])]
        lineas = {"fifo": fifo, "sjf": sjf,
                  "srtf": oraculo_srtf(DATOS), "rr": oraculo_rr(DATOS, 2)}
        for algoritmo, linea in lineas.items():
            with self.subTest(algoritmo=algoritmo):
                self.assertEqual(len(linea), 44)
                with (CARPETA / f"metricas_{algoritmo}.csv").open(newline="") as f:
                    filas = list(csv.DictReader(f))
                self.assertEqual([f["Proceso"] for f in filas], [p for p, _, _ in DATOS])
                for fila, (pid, llegada, rafaga) in zip(filas, DATOS):
                    inicio = linea.index(pid)
                    fin = len(linea) - linea[::-1].index(pid)
                    esperado = [llegada, rafaga, inicio, fin,
                                fin - llegada - rafaga, fin - llegada, inicio - llegada]
                    columnas = ["Llegada", "Rafaga", "Inicio", "Finalizacion",
                                "Espera", "Retorno", "Respuesta"]
                    self.assertEqual([int(fila[k]) for k in columnas], esperado, pid)
                    self.assertEqual(linea.count(pid), rafaga)

    def test_promedios_publicados(self):
        esperados = {"fifo": (18.9, 23.3, 18.9), "sjf": (14.0, 18.4, 14.0),
                     "srtf": (7.9, 12.3, 4.6), "rr": (16.7, 21.1, 5.8)}
        for algoritmo, esperado in esperados.items():
            with self.subTest(algoritmo=algoritmo):
                with (CARPETA / f"metricas_{algoritmo}.csv").open(newline="") as f:
                    filas = list(csv.DictReader(f))
                actual = tuple(sum(int(f[k]) for f in filas) / len(filas)
                               for k in ("Espera", "Retorno", "Respuesta"))
                self.assertEqual(actual, esperado)


if __name__ == "__main__":
    unittest.main()
