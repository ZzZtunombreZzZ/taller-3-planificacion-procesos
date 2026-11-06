"""Genera la entrega anónima. Requiere openpyxl y python-docx."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED
import sys

from docx import Document
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'docs/taller3/ejercicio1'))
import referencia as R

CARGAS = [[10, 4, 7, 2, 9, 3, 6, 1, 5, 2],
          [12, 3, 1, 8, 2, 6, 1, 4, 2, 5]]
CONCLUSIONES = [
    'SRTF obtiene los menores promedios: espera 11,20, retorno 16,10 y respuesta '
    '8,20. SJF obtiene 14,40 / 19,30 / 14,40; FIFO 22,00 / 26,90 / 22,00; '
    'RR q=3 obtiene 24,20 / 29,10 / 10,10. RR mejora la respuesta media frente '
    'a FIFO y SJF, aunque empeora espera y retorno. Su respuesta máxima es '
    '19 frente a 36 de SRTF. P1 es expropiado por P2 en t=1 y reanuda en t=31; '
    'P5 espera hasta t=40 en SRTF. Todos terminan en t=49.',
    'SRTF obtiene los menores promedios: espera 7,90, retorno 12,30 y respuesta '
    '4,60. SJF obtiene 14,00 / 18,40 / 14,00; FIFO 18,90 / 23,30 / 18,90; '
    'RR q=2 obtiene 16,70 / 21,10 / 5,80. P1 ejecuta [0,12) en FIFO/SJF; '
    'en SRTF es expropiado en t=1, reanuda en t=33 y termina en t=44. '
    'Los procesos cortos P2, P3 y P9 tienen respuesta 0 en SRTF. P4 tiene '
    'respuesta 13 en FIFO, 33 en SJF, 22 en SRTF y 4 en RR. En RR termina '
    'en t=42: recibe CPU antes, pero su retorno es mayor que en SRTF. '
    'La respuesta máxima RR es 12 frente a 22 de SRTF. Todos terminan en t=44.'
]


def generar(destino):
    informe = Document()
    informe.core_properties.author = ''
    informe.core_properties.last_modified_by = ''
    informe.add_heading('Taller 3 — Planificación de procesos', 0)
    informe.add_paragraph('Etapa 03 · Desarrollo y comparación de dos ejercicios')
    informe.add_heading('Supuestos y métricas', 1)
    informe.add_paragraph(
        'Todos los tiempos están en unidades de tiempo. Cada proceso tiene una '
        'ráfaga de CPU; no hay E/S ni costo por cambio de contexto. Solo un '
        'proceso ejecuta a la vez. Intervalos [inicio, fin): fin es el instante '
        'de finalización. Desempates por llegada y luego identificador. En SRTF '
        'solo se interrumpe si el candidato tiene un restante estrictamente '
        'menor. En RR las llegadas al vencer el quantum entran antes del '
        'proceso reincorporado. Retorno = fin − llegada; espera = retorno − '
        'ráfaga; respuesta = primer inicio − llegada.')
    for numero, (rafagas, quantum) in enumerate(zip(CARGAS, [3, 2]), 1):
        procs = [(f'P{i+1}', i, b) for i, b in enumerate(rafagas)]
        total = sum(rafagas)
        rr, turnos = R.rr(procs, quantum)
        algoritmos = {'FIFO': R.fifo(procs), 'SJF': R.sjf(procs),
                      'SRTF': R.srtf(procs)[0], 'RR': rr}
        libro = Workbook()
        resumen = libro.active
        resumen.title = 'Resumen'
        libro.properties.creator = ''
        libro.properties.lastModifiedBy = ''
        resumen.append([f'Ejercicio {numero}', f'Quantum RR = {quantum}'])
        resumen.append(['Algoritmo', 'Espera promedio', 'Retorno promedio', 'Respuesta promedio'])
        informe.add_page_break()
        informe.add_heading(f'Ejercicio {numero} — Round Robin q={quantum}', 1)
        for nombre, gantt in algoritmos.items():
            filas = R.metricas(procs, gantt)
            medias = R.promedios(filas)
            resumen.append([nombre] + [float(medias[k]) for k in ('espera', 'retorno', 'respuesta')])
            hoja = libro.create_sheet(nombre)
            cabecera = ['Proceso', 'Llegada', 'Ráfaga', 'Inicio', 'Finalización', 'Espera', 'Retorno', 'Respuesta']
            hoja.append(cabecera)
            datos = [[f[k] for k in ('pid', 'llegada', 'rafaga', 'inicio', 'fin', 'espera', 'retorno', 'respuesta')] for f in filas]
            for fila in datos:
                hoja.append(fila)
            hoja.append(['Promedios', '', '', '', ''] + [float(medias[k]) for k in ('espera', 'retorno', 'respuesta')])
            hoja.cell(14, 1, 'Proceso / t')
            for t in range(total):
                hoja.cell(14, t+2, t)
            for i, (pid, llegada, _) in enumerate(procs, 15):
                hoja.cell(i, 1, pid)
                fin = next(f['fin'] for f in filas if f['pid'] == pid)
                for t in range(total):
                    ejecuta = any(p == pid and a <= t < b for p, a, b in gantt)
                    c = hoja.cell(i, t+2)
                    c.value = pid if ejecuta else ('E' if llegada <= t < fin else None)
                    if c.value:
                        c.fill = PatternFill('solid', fgColor='92D050' if ejecuta else 'FFF2CC')
                    c.alignment = Alignment(horizontal='center')
            hoja.cell(26, 1, f'Cada columna t representa [t,t+1). Verde: CPU. E / amarillo: espera. Fin total: {total}.')
            hoja.append([])
            hoja.cell(28, 1, 'Gantt por intervalos')
            for i, segmento in enumerate(gantt, 29):
                for j, dato in enumerate(segmento, 1):
                    hoja.cell(i, j, dato)
            hoja.freeze_panes = 'B15'
            hoja.column_dimensions['A'].width = 20
            for c in range(2, total+2):
                hoja.column_dimensions[get_column_letter(c)].width = 6
            hoja.print_area = f'A1:{get_column_letter(total+1)}26'
            hoja.page_setup.orientation = 'landscape'
            hoja.page_setup.paperSize = hoja.PAPERSIZE_A3
            hoja.sheet_properties.pageSetUpPr.fitToPage = True
            hoja.page_setup.fitToWidth = 1
            hoja.page_setup.fitToHeight = 1
            informe.add_heading(nombre, 2)
            tabla = informe.add_table(rows=1, cols=8)
            tabla.style = 'Light Shading Accent 1'
            for c, txt in zip(tabla.rows[0].cells, cabecera):
                c.text = txt
            for fila in datos:
                for c, dato in zip(tabla.add_row().cells, fila):
                    c.text = str(dato)
            informe.add_paragraph('Promedios: ' + '; '.join(f'{k} = {float(medias[k]):.2f}' for k in ('espera', 'retorno', 'respuesta')) + '.')
            informe.add_paragraph('Gantt [inicio, fin): ' + ' → '.join(f'{p} [{a},{b})' for p, a, b in gantt) + '.')
        cola = libro.create_sheet('Cola RR')
        cola.append(['Inicio', 'Proceso', 'Restante antes', 'Duración', 'Fin', 'Restante después', 'Llegadas', 'Reincorpora', 'Cola al terminar'])
        for x in turnos:
            cola.append([x['t'], x['pid'], x['antes'], x['dur'], x['fin'], x['despues'], ', '.join(x['nuevos']), 'Sí' if x['reinc'] else 'No', ', '.join(x['cola'])])
        cola.column_dimensions['G'].width = 30
        cola.column_dimensions['I'].width = 65
        for s in [resumen, cola]:
            s.freeze_panes = 'A3' if s == resumen else 'A2'
            for c in range(1, s.max_column+1):
                if s.column_dimensions[get_column_letter(c)].width < 20:
                    s.column_dimensions[get_column_letter(c)].width = 20
        for s in libro:
            for c in s[2 if s == resumen else 1]:
                c.font = Font(bold=True)
        libro.save(destino / f'Ejercicio_{numero}.xlsx')
        informe.add_heading('Conclusión comparativa y quantum', 2)
        informe.add_paragraph(CONCLUSIONES[numero-1])
        informe.add_paragraph(
            f'RR usa quantum {quantum}, con {len(turnos)} turnos y '
            f'{sum(x["reinc"] for x in turnos)} reincorporaciones, registradas '
            'en la hoja Cola RR del Excel. Las ráfagas que no superan el '
            'quantum terminan en un turno. Un quantum menor reduce la duración '
            'de cada turno y puede aumentar interrupciones; uno mayor aproxima '
            'RR a FIFO. Aquí no se cobra costo de cambio de contexto.')
        informe.add_paragraph(
            'RR reparte el acceso periódicamente y evita la inanición para '
            'esta carga. SJF y SRTF favorecen trabajos cortos y postergan '
            'largos: bajo llegadas continuas de procesos cortos hay riesgo '
            'de inanición, aunque en estos datos finitos todos terminan. '
            'FIFO respeta el orden de llegada, pero sufre efecto convoy. '
            'SRTF favorece los promedios; RR ofrece mejor peor caso de '
            'respuesta. Ninguno es superior para todos los objetivos.')
    informe.save(destino / 'Informe_Taller_3.docx')
    (destino / 'LEEME.txt').write_text(
        'TALLER 3 — PLANIFICACIÓN DE PROCESOS — ETAPA 03\n\n'
        'Informe_Taller_3.docx: desarrollo y conclusiones de ambos ejercicios.\n'
        'Ejercicio_1.xlsx: cuatro algoritmos, Gantt, métricas, promedios y cola RR q=3.\n'
        'Ejercicio_2.xlsx: cuatro algoritmos, Gantt, métricas, promedios y cola RR q=2.\n\n'
        'Abrir primero el informe; consultar los Excel para los diagramas y '
        'el registro completo de cada turno y reincorporación.\n', encoding='utf-8')


if __name__ == '__main__':
    entrega = RAIZ / 'entregas/Taller_3_Etapa_03.zip'
    entrega.parent.mkdir(exist_ok=True)
    with TemporaryDirectory() as carpeta:
        destino = Path(carpeta)
        generar(destino)
        with ZipFile(entrega, 'w', ZIP_DEFLATED) as z:
            for p in sorted(destino.iterdir()):
                z.write(p, 'Taller_3_Etapa_03/' + p.name)
    print(entrega)
