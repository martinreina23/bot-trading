#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WBS v0.7 — Bot de trading. Panel de un vistazo + equipo de agentes con modelo por rol."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

ARIAL = "Arial"
F_TITLE = Font(name=ARIAL, size=14, bold=True, color="FFFFFF")
F_HDR = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
F_FASE = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
F_PKG = Font(name=ARIAL, size=10, bold=True)
F_TXT = Font(name=ARIAL, size=10)
F_SMALL = Font(name=ARIAL, size=9, italic=True)
FILL_TITLE = PatternFill("solid", fgColor="1F3864")
FILL_HDR = PatternFill("solid", fgColor="2F5496")
FILL_FASE = PatternFill("solid", fgColor="4472C4")
FILL_PKG = PatternFill("solid", fgColor="D9E2F2")
FILL_LEG = PatternFill("solid", fgColor="FFF2CC")
FILL_HECHA = PatternFill("solid", fgColor="C6EFCE")
FILL_CURSO = PatternFill("solid", fgColor="FFEB9C")
FILL_BLOQ = PatternFill("solid", fgColor="FFC7CE")
THIN = Border(*[Side(style="thin", color="B0B0B0")]*4)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

wb = openpyxl.Workbook()

# ============ PLAN DE ACCION ============
plan = wb.active
plan.title = "PLAN DE ACCION"

# (codigo, tipo, que se hace, que se entrega, responsable, depende de, duracion, estado, notas)
ROWS = [
("01","Fase","ARRANQUE","Plan aprobado, limites fijados y herencia de gb2 analizada","CEO + Orquestador","—","1 semana","",""),
("01.01","Paquete","Plan y reglas","","","","","",""),
("01.01.01","Tarea","Aprobar este plan y las reglas de trabajo","Plan v0.7 aprobado","CEO","—","1 dia","En curso",""),
("01.01.02","Tarea","Aprobar los criterios para elegir mercado (hoja PUERTAS, G1)","Criterios aprobados","CEO","01.01.01","1 dia","Pendiente",""),
("01.01.03","Tarea","Fijar limites: fecha tope, horas del CEO por semana y perdida maxima futura","Limites en numeros","CEO","01.01.01","1 dia","Pendiente","Solo puede decidirlo el CEO"),
("01.02","Paquete","Herencia de gb2 (informacion, no copia)","","","","","",""),
("01.02.01","Tarea","Analizar gb2: que funciono, que no, que modelo usaba cada agente y por que, errores a no repetir. NO se copia codigo","Informe de herencia + lecciones iniciales","Critico de codigo","01.01.01","2-3 dias","Pendiente","Necesita acceso a los archivos de gb2; sus conclusiones alimentan 03.01.02 y la hoja EQUIPO. Paralela a la Fase 02"),
("02","Fase","ELEGIR MERCADO Y TAMAÑO DE VELA (puerta G1)","3-5 mercados y 1-2 tamaños de vela, decididos con numeros","Orquestador + Investigador","01.01","2-3 semanas","",""),
("02.01","Paquete","Preparar la comparacion","","","","","",""),
("02.01.01","Tarea","Confirmar lista de 8 candidatos: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, oro (XAUUSD), BTC y ETH","Lista cerrada","CEO + Orquestador","01.01.02","1 dia","Pendiente","Si se añade uno, se quita otro"),
("02.01.02","Tarea","Recopilar cuanto cuesta operar en cada mercado (comisiones y horquillas tipicas de brokers grandes)","Tabla de costes con fuentes","Investigador","02.01.01","1-2 dias","Pendiente","PROVISIONAL: se recalcula con el broker real en 04.01.02"),
("02.02","Paquete","Medir los mercados (paralelas entre si)","","","","","",""),
("02.02.01","Tarea","Medir cuanto se mueve cada mercado de media en velas de 15 min, 1 h y 4 h (ultimos 2 años)","Tabla 8 mercados x 3 velas","Investigador","02.01.01","1-2 dias","Pendiente",""),
("02.02.02","Tarea","Calcular que parte del movimiento se la come el coste de operar, en %","Tabla 8x3 en %","Investigador","02.01.02, 02.02.01","1 dia","Pendiente","El numero mas importante de la fase"),
("02.02.03","Tarea","Medir que mercados se mueven a la vez (correlacion), para no repetir la misma apuesta","Matriz de correlaciones","Investigador","02.01.01","1-2 dias","Pendiente",""),
("02.02.04","Tarea","Averiguar que historial de precios existe, donde conseguirlo y cuanto cuesta","Tabla: años, fuente, precio","Investigador","02.01.01","1-2 dias","Pendiente","Minimo deseado: 5 años"),
("02.03","Paquete","Validar y decidir","","","","","",""),
("02.03.01","Tarea","Revision independiente: metodo, fuentes y numeros del investigador","Informe de revision","Orquestador","02.02.01 a 02.02.04","1-2 dias","Pendiente","Quien produce no se valida a si mismo"),
("02.03.02","Tarea","Informe de decision: propuesta de 3-5 mercados poco correlacionados y 1-2 velas, con los porques en llano","Informe G1","Orquestador","02.03.01","1 dia","Pendiente",""),
("02.03.03","Tarea","PUERTA G1: el CEO elige","Decision escrita","CEO","02.03.02","1 dia","Pendiente",""),
("03","Fase","MONTAR LA CASA (Claude Code) — EN PARALELO con la Fase 02","Repositorio con carpetas, reglas y agentes funcionando, cada uno con su modelo","Claude Code","01.01","1 semana","",""),
("03.01","Paquete","Puesta en marcha tecnica","","","","","",""),
("03.01.01","Tarea","Crear el repositorio: carpetas, este WBS (version texto), reglas (CLAUDE.md), DECISIONES.md y LECCIONES.md","Repositorio funcionando","Constructores","01.01.01","1-2 dias","Pendiente","Aqui se vuelca todo lo aprendido en estos chats"),
("03.01.02","Tarea","Crear los agentes de la hoja EQUIPO, cada uno con su modelo asignado y descripcion sin ambiguedad; prueba de activacion de TODOS","Todos los agentes activándose y anunciando tarea por codigo WBS","Constructores","03.01.01, 01.02.01","1-2 dias","Pendiente","Ningun agente fantasma: si no se activa en la prueba, se arregla antes de seguir"),
("03.01.03","Tarea","Ejecucion desatendida en el ordenador de casa: arranques programados, permisos AMPLIOS por defecto (con git como red de seguridad) y topes de gasto","Sistema corriendo solo con red de seguridad","Constructores","03.01.02","1-2 dias","Pendiente","Regla anti-gb2: se empieza permisivo; las restricciones se añaden solo tras un incidente real"),
("03.01.04","Tarea","Plan de respaldo de modelos: si un modelo no esta disponible o rechaza una peticion, el agente continua con el modelo de respaldo de la hoja EQUIPO y lo deja anotado","Respaldo probado y funcionando","Constructores","03.01.02","1 dia","Pendiente","Fable 5 puede rechazar peticiones y ya estuvo suspendido en junio de 2026; el motor no puede depender de un solo modelo"),
("03.01.05","Tarea","PRUEBA REAL DEL MOTOR: un dia entero de trabajo desatendido de verdad antes de dar la fase por buena. Lo que falle se arregla ahora, no en el papel","Informe de la prueba de un dia","Orquestador","03.01.03, 03.01.04","1-2 dias","Pendiente","Evita el error de gb2: motor perfecto en papel que no aguanta la realidad"),
("03.01.06","Tarea","Plantilla y automatismo de fichas de decision: el secretario prepara cada decision del CEO en el formato obligatorio y la adjunta al informe semanal","Fichas generadas solas","Secretario","03.01.02","1 dia","Pendiente","Si una ficha obliga al CEO a redactar, buscar o calcular, vuelve atras"),
("03.01.07","Tarea","Cola de aprobacion del CEO: una tabla donde el equipo deja lo que necesita visto bueno, cada linea con desplegable Aprobado / Saltar / Corregir y una columna para escribir la correccion. Lo aprobado se ejecuta solo; lo corregido se rehace Y la correccion se guarda en LECCIONES.md","Cola de aprobacion funcionando","Secretario","03.01.06","1 dia","Pendiente","Idea tomada de un video de TikTok (29/07). El valor no es aprobar: es que cada correccion tuya quede escrita y no haya que repetirla"),
("04","Fase","HIPOTESIS Y VALIDACION (puerta G2)","Estrategias que sobreviven a todos los filtros; si ninguna sobrevive, el bucle se repite","Claude Code","03","4-8 semanas","",""),
("04.01","Paquete","Broker y cajones de datos","","","","","",""),
("04.01.01","Tarea","Comparar 3-4 brokers del mercado elegido (costes reales, regulacion, cuenta demo) y elegir uno","Broker elegido + demo abierta","CEO + Orquestador","02.03.03","3-4 dias","Pendiente","El CEO firma"),
("04.01.02","Tarea","Recalcular los costes con los precios reales del broker (sustituye los provisionales de 02.01.02)","Tabla de costes definitiva","Constructor de datos","04.01.01","1 dia","Pendiente",""),
("04.01.03","Tarea","Conseguir y limpiar el historico; partirlo en 3 cajones: construir (train), ajustar (validacion) y RESERVADO bajo llave (OOS), que solo se abre una vez por variante","3 cajones de datos separados y protegidos","Constructor de datos","04.01.01","3-5 dias","Pendiente","Ningun agente puede tocar el cajon reservado"),
("04.02","Paquete","Investigacion de hipotesis (el analisis grande)","","","","","",""),
("04.02.01","Tarea","Barrido de fuentes: papers, libros, foros especializados, GitHub y X/Twitter. Regla: cada idea necesita minimo 2 fuentes independientes y verificables","Lista larga de ideas con sus fuentes","Investigador","03.01.02","1-2 semanas","Pendiente","Descartar humo: vendedores de cursos y señales no son fuente"),
("04.02.02","Tarea","Ficha por hipotesis: por que existiria la ventaja (la logica), reglas de entrada y salida, mercado y vela donde aplica","Fichas completas","Investigador","04.02.01","3-5 dias","Pendiente","Hipotesis sin logica de por que gana = no entra. Nada de probar por probar"),
("04.02.03","Tarea","Filtro de sentido: el validador puntua las fichas y se eligen las 3-5 mejores","Lista corta de 3-5 hipotesis","Validador","04.02.02","2-3 dias","Pendiente","El investigador no elige sus propias fichas"),
("04.02.04","Tarea","Pre-registro de variantes: ANTES de probar nada, cada hipotesis deja escritas sus variantes a probar (maximo 5-7 por hipotesis)","Registro de variantes cerrado","Validador","04.02.03","1-2 dias","Pendiente","Lo que no este pre-registrado no se prueba. Es la proteccion contra engañarnos"),
("04.03","Paquete","Laboratorio de pruebas (por hipotesis y variante)","","","","","",""),
("04.03.01","Tarea","Backtest de cada variante con costes reales sobre el cajon de construir (train)","Resultados de train por variante","Constructores","04.01.03, 04.02.04","1-2 semanas","Pendiente",""),
("04.03.02","Tarea","Ajustar parametros SOLO con el cajon de ajuste (validacion); lo que no aguanta, muere aqui","Variantes supervivientes","Constructores","04.03.01","3-5 dias","Pendiente",""),
("04.03.03","Tarea","Prueba de fuego: cada superviviente se prueba UNA sola vez sobre el cajon reservado (OOS)","Resultados OOS","Validador","04.03.02","2-3 dias","Pendiente","Una sola bala por variante; repetir seria hacerse trampa"),
("04.03.04","Tarea","Robustez: Monte Carlo (barajar el orden de las operaciones y meter pequeños cambios miles de veces para ver si el beneficio aguanta o era suerte) y walk-forward (repetir el ajuste avanzando en el tiempo)","Informe de robustez por variante","Validador","04.03.03","3-5 dias","Pendiente",""),
("04.03.05","Tarea","Veredicto pasa / no pasa por variante, emitido por el validador con los criterios de la puerta G2","Veredictos escritos","Validador","04.03.04","1-2 dias","Pendiente","Quien construyo la variante no vota"),
("04.04","Paquete","Decision y bucle","","","","","",""),
("04.04.01","Tarea","Informe final de la vuelta: que paso el filtro, que murio y por que. Registro de TODAS las pruebas, tambien las fallidas","Informe de vuelta + registro completo","Secretario","04.03.05","1-2 dias","Pendiente","Las pruebas fallidas tambien se guardan: son informacion"),
("04.04.02","Tarea","Si ninguna variante pasa: volver a 04.02 con las lecciones aprendidas (vuelta 2, 3...). Al acabar la vuelta 3 sin exito, revision completa del planteamiento con el CEO","Decision de bucle registrada","Orquestador","04.04.01","—","Pendiente","El bucle es normal; infinito, no"),
("04.04.03","Tarea","PUERTA G2: el CEO decide que estrategias pasan a demo","Decision escrita","CEO","04.04.01","1 dia","Pendiente",""),
("05","Fase","DEMO (puerta G3)","Bot operando con dinero de mentira en mercado real 8-12 semanas","Claude Code","04","8-12 semanas","",""),
("05.01","Paquete","Se detalla al cerrar la puerta G2","","","","","",""),
("05.01.01","Tarea","Poner el bot a operar en demo, solo y con los guardias automaticos puestos","Bot en demo","Constructores","04.04.03","2-3 dias","Pendiente",""),
("05.01.02","Tarea","Seguimiento semanal: comparar lo que hace el bot con lo que prometian las pruebas","Informe semanal","Secretario","05.01.01","8-12 semanas","Pendiente","El reloj de mercado no se puede acelerar"),
("05.01.03","Tarea","PUERTA G3: el CEO decide si entra dinero real, cuanto y con que perdida maxima","Decision escrita","CEO","05.01.02","1 dia","Pendiente",""),
("06","Fase","REAL (puerta G4)","Dinero de verdad, pequeño y con limites escritos","Claude Code + CEO","05","continua","",""),
("06.01","Paquete","Se detalla al cerrar la puerta G3","","","","","",""),
("06.01.01","Tarea","Operar con dinero pequeño respetando los limites de 01.01.03","Bot en real","Constructores","05.01.03","continua","Pendiente",""),
("06.01.02","Tarea","PUERTA G4 (mensual): seguir, ampliar o parar","Decision mensual","CEO","06.01.01","continua","Pendiente","Si pierde mas de lo escrito, se para sin discusion"),
("07","Fase","MOTOR Y ORDEN (paralela, max. 20% del esfuerzo semanal)","Motor y carpetas en orden sin comerse el proyecto","Claude Code","03","continua","",""),
("07.01","Paquete","Trabajo continuo","","","","","",""),
("07.01.01","Tarea","Carpetas, documentos y reglas en orden: una sola fuente de verdad por tema; lo sustituido se borra","Repositorio limpio","Constructores","03.01.01","continua","Pendiente",""),
("07.01.02","Tarea","Mejoras del motor: SOLO tareas aprobadas en la revision semanal del CEO","Mejoras con codigo WBS","Constructores","03.01.02","continua","Pendiente","Regla anti-deriva: el motor no manda"),
]

HDRS = ["CODIGO","TIPO","QUE SE HACE","QUE SE ENTREGA","RESPONSABLE","DEPENDE DE","DURACION EST.","ESTADO","FECHA CIERRE","NOTAS"]
plan["A1"] = "PLAN DE ACCION — BOT DE TRADING (WBS v0.7)"
plan["A1"].font = Font(name=ARIAL, size=13, bold=True, color="FFFFFF")
plan.merge_cells("A1:J1")
for c in range(1, 11):
    plan.cell(row=1, column=c).fill = FILL_TITLE
plan["A2"] = "Rellenar solo: ESTADO (desplegable), FECHA CIERRE y NOTAS. Ejemplo: 01.01.01 esta 'En curso'. Los codigos no cambian una vez la tarea empieza."
plan["A2"].font = F_SMALL
plan.merge_cells("A2:J2")
plan["A2"].fill = FILL_LEG

hdr_row = 3
for j, h in enumerate(HDRS, start=1):
    c = plan.cell(row=hdr_row, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

r = hdr_row
for cod, tipo, hace, entrega, resp, dep, dur, estado, notas in ROWS:
    r += 1
    vals = [cod, tipo, hace, entrega, resp, dep, dur, estado, "", notas]
    for j, v in enumerate(vals, start=1):
        c = plan.cell(row=r, column=j, value=v)
        c.border = THIN; c.alignment = WRAP; c.font = F_TXT
        if j == 1:
            c.number_format = "@"
    if tipo == "Fase":
        for j in range(1, 11):
            cc = plan.cell(row=r, column=j); cc.fill = FILL_FASE; cc.font = F_FASE
    elif tipo == "Paquete":
        for j in range(1, 11):
            cc = plan.cell(row=r, column=j); cc.fill = FILL_PKG; cc.font = F_PKG
last_row = r

dv = DataValidation(type="list", formula1='"Pendiente,En curso,Hecha,Bloqueada"', allow_blank=True)
plan.add_data_validation(dv)
dv.add(f"H{hdr_row+1}:H{last_row}")
rng = f"H{hdr_row+1}:H{last_row}"
plan.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Hecha"'], fill=FILL_HECHA))
plan.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"En curso"'], fill=FILL_CURSO))
plan.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Bloqueada"'], fill=FILL_BLOQ))
for j, w in enumerate([10, 9, 55, 27, 18, 15, 12, 11, 12, 32], start=1):
    plan.column_dimensions[get_column_letter(j)].width = w
plan.freeze_panes = "A4"

# ============ PANEL (primera hoja, vista de un vistazo) ============
panel = wb.create_sheet("PANEL", 0)
panel["A1"] = "PANEL — BOT DE TRADING · evaluacion del mes: 1 de septiembre de 2026"
panel["A1"].font = F_TITLE
panel.merge_cells("A1:G1")
for c in range(1, 8):
    panel.cell(row=1, column=c).fill = FILL_TITLE

hdrs = ["FASE","TAREAS","HECHAS","EN CURSO","PENDIENTES","BLOQUEADAS","% AVANCE"]
for j, h in enumerate(hdrs, start=1):
    c = panel.cell(row=3, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

fases = [
    ("01","01. Arranque"),
    ("02","02. Elegir mercado y vela"),
    ("03","03. Montar la casa (Claude Code)"),
    ("04","04. Hipotesis y validacion"),
    ("05","05. Demo"),
    ("06","06. Real"),
    ("07","07. Motor y orden (paralela)"),
]
A = f"'PLAN DE ACCION'!$A${hdr_row+1}:$A${last_row}"
B = f"'PLAN DE ACCION'!$B${hdr_row+1}:$B${last_row}"
H = f"'PLAN DE ACCION'!$H${hdr_row+1}:$H${last_row}"
row = 3
for pref, nombre in fases:
    row += 1
    panel.cell(row=row, column=1, value=nombre).font = F_TXT
    panel.cell(row=row, column=2, value=f'=COUNTIFS({B},"Tarea",{A},"{pref}.*")')
    panel.cell(row=row, column=3, value=f'=COUNTIFS({B},"Tarea",{A},"{pref}.*",{H},"Hecha")')
    panel.cell(row=row, column=4, value=f'=COUNTIFS({B},"Tarea",{A},"{pref}.*",{H},"En curso")')
    panel.cell(row=row, column=5, value=f'=COUNTIFS({B},"Tarea",{A},"{pref}.*",{H},"Pendiente")')
    panel.cell(row=row, column=6, value=f'=COUNTIFS({B},"Tarea",{A},"{pref}.*",{H},"Bloqueada")')
    panel.cell(row=row, column=7, value=f'=IFERROR(C{row}/B{row},0)')
    for j in range(1, 8):
        cc = panel.cell(row=row, column=j); cc.border = THIN
        if j > 1: cc.font = F_TXT; cc.alignment = CENTER
    panel.cell(row=row, column=7).number_format = "0%"
first_fase_row = 4
row += 1
panel.cell(row=row, column=1, value="TOTAL PROYECTO").font = Font(name=ARIAL, size=10, bold=True)
for j, col in zip(range(2, 7), "BCDEF"):
    panel.cell(row=row, column=j, value=f"=SUM({col}{first_fase_row}:{col}{row-1})").font = Font(name=ARIAL, size=10, bold=True)
panel.cell(row=row, column=7, value=f"=IFERROR(C{row}/B{row},0)")
panel.cell(row=row, column=7).number_format = "0%"
panel.cell(row=row, column=7).font = Font(name=ARIAL, size=10, bold=True)
for j in range(1, 8):
    panel.cell(row=row, column=j).border = THIN
    panel.cell(row=row, column=j).fill = FILL_PKG
total_row = row

# barras visuales en % avance
panel.conditional_formatting.add(
    f"G{first_fase_row}:G{total_row}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="4472C4", showValue=True)
)

panel[f"A{total_row+2}"] = "PROXIMA PUERTA:"
panel[f"A{total_row+2}"].font = Font(name=ARIAL, size=10, bold=True)
panel[f"B{total_row+2}"] = "G1 — elegir mercado y tamaño de vela · lunes 3 de agosto de 2026"
panel[f"B{total_row+2}"].font = F_TXT
panel[f"A{total_row+3}"] = "EN MARCHA AHORA:"
panel[f"A{total_row+3}"].font = Font(name=ARIAL, size=10, bold=True)
panel[f"B{total_row+3}"] = "Fase 02 (medir mercados) + 01.02.01 (analisis gb2) + 03.01.01 (repositorio), en paralelo"
panel[f"B{total_row+3}"].font = F_TXT

leg = total_row + 5
panel[f"A{leg}"] = "LEYENDA:"
panel[f"A{leg}"].font = Font(name=ARIAL, size=10, bold=True)
for i, (txt, fill) in enumerate([("Hecha", FILL_HECHA), ("En curso", FILL_CURSO), ("Pendiente", None), ("Bloqueada", FILL_BLOQ)]):
    c = panel.cell(row=leg + 1 + i, column=1, value=txt)
    c.font = F_TXT; c.border = THIN
    if fill: c.fill = fill
for j, w in enumerate([34, 9, 9, 10, 12, 12, 14], start=1):
    panel.column_dimensions[get_column_letter(j)].width = w

# ============ EQUIPO (agentes + modelo por rol) ============
eq = wb.create_sheet("EQUIPO")
eq["A1"] = "EQUIPO DE AGENTES — cada uno con su modelo segun su tarea"
eq["A1"].font = F_TITLE
eq.merge_cells("A1:E1")
for c in range(1, 6):
    eq.cell(row=1, column=c).fill = FILL_TITLE
eq["A2"] = ("Propuesta inicial: se confirma con el analisis de gb2 (01.02.01) y la prueba de agentes (03.01.02). "
            "Mientras trabajemos en chats: el chat director hace de Orquestador + Validador, y el chat analista de Investigador.")
eq["A2"].font = F_SMALL
eq.merge_cells("A2:E2")
eq["A2"].fill = FILL_LEG

hdrs = ["AGENTE","QUE HACE","QUE NO PUEDE HACER","MODELO","RESPALDO SI FALLA","POR QUE ESE MODELO"]
for j, h in enumerate(hdrs, start=1):
    c = eq.cell(row=4, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

equipo = [
("Orquestador (jefe de proyecto)","Reparte tareas por codigo WBS, cierra tareas contra su criterio de hecho, decide la siguiente, escala excepciones al CEO","Ejecutar tareas de construccion; validar su propio reparto","Opus 5","Sonnet 5","Decidir y planificar sin humano detras es lo mas dificil del sistema. Opus 5 esta descrito por Anthropic para trabajo agentico complejo, a la mitad de precio que Fable"),
("Investigador","Barre fuentes (papers, libros, foros, GitHub, X), redacta fichas de hipotesis con fuentes","Elegir sus propias fichas; tocar codigo o datos","Sonnet 5","Haiku 4.5","Mucho volumen de lectura y sintesis; el listo-y-rapido de la casa. Precio de salida 5 veces menor que Opus"),
("Constructor de datos","Descarga y limpia historicos, mantiene los 3 cajones de datos, calcula costes reales","Abrir el cajon reservado (OOS)","Sonnet 5","Haiku 4.5","Trabajo de codigo y datos estandar"),
("Constructor de motor y bot","Backtester, bot, ejecucion desatendida","Validar sus propios backtests; tocar el cajon reservado","Sonnet 5","Opus 5 si se atasca 2 veces","Codigo intensivo y repetitivo; escalar solo cuando falla"),
("Critico de codigo","Revisa el codigo de los constructores e informa de fallos; analiza gb2 (01.02.01)","Revisar codigo escrito por el mismo","Sonnet 5 (Opus 5 en el codigo que toca dinero real)","Sonnet 5","Revision constante en Sonnet; se sube el liston donde un fallo cuesta dinero"),
("Validador de estrategias","Intenta tumbar cada hipotesis: filtro de sentido, prueba de fuego OOS, Monte Carlo, veredictos pasa / no pasa","Construir estrategias; suavizar veredictos","FABLE 5","Opus 5","Es el que evita perder dinero: el puesto donde mas se nota el mejor razonamiento. Ojo: es el modelo mas caro (50 $ por millon de palabras de salida) y puede rechazar peticiones, por eso lleva respaldo"),
("Arquitecto (solo en momentos clave)","Diseña el motor al arrancar la Fase 03 y revisa el planteamiento si el bucle de hipotesis falla 3 veces","Trabajo del dia a dia","FABLE 5","Opus 5","Uso puntual y caro: solo donde una decision de diseño condiciona meses de trabajo"),
("Secretario","Informe diario y semanal, actualiza WBS, DECISIONES.md y LECCIONES.md, registro de todas las pruebas","Tomar decisiones de proyecto","Haiku 4.5","Sonnet 5","Trabajo mecanico y muy frecuente: el mas rapido y barato"),
]
r = 4
for row_data in equipo:
    r += 1
    for j, v in enumerate(row_data, start=1):
        c = eq.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
r += 2
eq.cell(row=r, column=1, value="PRECIOS OFICIALES (por millon de tokens; 1 token = mas o menos 3/4 de palabra) — fuente: platform.claude.com, consultado 29/07/2026").font = Font(name=ARIAL, size=10, bold=True)
r += 1
for j, h in enumerate(["MODELO","ID TECNICO","ENTRADA","SALIDA","MEMORIA (CONTEXTO)"], start=1):
    c = eq.cell(row=r, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN
precios = [
("Claude Fable 5","claude-fable-5","10 $","50 $","1.000.000 tokens"),
("Claude Opus 5","claude-opus-5","5 $","25 $","1.000.000 tokens"),
("Claude Sonnet 5","claude-sonnet-5","3 $ (2 $ hasta 31/08/2026)","15 $ (10 $ hasta 31/08/2026)","1.000.000 tokens"),
("Claude Haiku 4.5","claude-haiku-4-5-20251001","1 $","5 $","200.000 tokens"),
]
for p in precios:
    r += 1
    for j, v in enumerate(p, start=1):
        c = eq.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
r += 2
eq.cell(row=r, column=1, value="AVISO SOBRE FABLE 5: en junio de 2026 estuvo suspendido por controles de exportacion y volvio el 1 de julio. Ademas puede rechazar peticiones por sus filtros de seguridad. Por eso todo agente con Fable lleva respaldo obligatorio (tarea 03.01.04). Comprobar en la cuenta si su uso consume creditos aparte del plan Max.").font = F_SMALL
eq.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
eq.cell(row=r, column=1).fill = FILL_LEG
eq.cell(row=r, column=1).alignment = WRAP
for j, w in enumerate([22, 42, 28, 16, 18, 42], start=1):
    eq.column_dimensions[get_column_letter(j)].width = w

# ============ RESPONSABILIDADES (RACI con agentes) ============
raci = wb.create_sheet("RESPONSABILIDADES")
raci["A1"] = "MATRIZ DE RESPONSABILIDADES (por paquete de trabajo)"
raci["A1"].font = F_TITLE
raci.merge_cells("A1:I1")
for c in range(1, 10):
    raci.cell(row=1, column=c).fill = FILL_TITLE
raci["A2"] = "A = Aprueba (ultima palabra) · R = Realiza · C = Consultado (opina antes) · I = Informado (se entera despues) · — = no participa"
raci["A2"].font = F_SMALL
raci.merge_cells("A2:I2")
raci["A2"].fill = FILL_LEG

hdrs = ["CODIGO","PAQUETE","CEO","ORQUESTADOR","INVESTIGADOR","CONSTRUCTORES","CRITICO","VALIDADOR","SECRETARIO"]
for j, h in enumerate(hdrs, start=1):
    c = raci.cell(row=4, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

raci_rows = [
("01.01","Plan y reglas","A","R","I","I","I","I","I"),
("01.02","Herencia de gb2","C","A","—","—","R","—","I"),
("02.01","Preparar la comparacion de mercados","A","R","R","—","—","—","I"),
("02.02","Medir los mercados","I","A","R","—","—","—","I"),
("02.03","Validar y decidir (puerta G1)","A","R","C","—","—","—","I"),
("03.01","Montar la casa en Claude Code","A","C","—","R","C","—","I"),
("04.01","Broker y cajones de datos","A","R","C","R","—","—","I"),
("04.02","Investigacion de hipotesis","I","A","R","—","—","C","I"),
("04.03","Laboratorio de pruebas","I","C","—","R","C","A","I"),
("04.04","Decision y bucle (puerta G2)","A","R","—","—","—","C","R"),
("05.01","Demo (puerta G3)","A","C","—","R","—","C","R"),
("06.01","Real (puerta G4)","A","C","—","R","—","C","R"),
("07.01","Motor y orden","I","A","—","R","C","—","I"),
]
r = 4
for row_data in raci_rows:
    r += 1
    for j, v in enumerate(row_data, start=1):
        c = raci.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT
        c.alignment = CENTER if j >= 3 else WRAP
        if j == 1: c.number_format = "@"
for j, w in enumerate([9, 34, 8, 14, 14, 15, 10, 11, 12], start=1):
    raci.column_dimensions[get_column_letter(j)].width = w

# ============ DECISIONES DEL CEO ============
dc = wb.create_sheet("DECISIONES CEO")
dc["A1"] = "DECISIONES DEL CEO — formato obligatorio y decisiones abiertas"
dc["A1"].font = F_TITLE
dc.merge_cells("A1:F1")
for c in range(1, 7):
    dc.cell(row=1, column=c).fill = FILL_TITLE

dc["A2"] = ("REGLA: nada llega al CEO en formato 'opina sobre esto'. Toda decision llega como FICHA: 1 linea de que se decide · 2-4 opciones cerradas · la recomendada marcada con su motivo · "
            "que pasa con cada opcion · y se responde con una letra o un numero. Si no cabe en media pantalla de movil, el equipo no ha terminado su trabajo y la ficha vuelve atras. "
            "Ninguna ficha puede pedir al CEO que redacte, busque o calcule nada.")
dc["A2"].font = F_SMALL
dc.merge_cells("A2:F2")
dc["A2"].fill = FILL_LEG
dc["A2"].alignment = WRAP
dc.row_dimensions[2].height = 45

dc["A4"] = "DECISIONES ABIERTAS AHORA (puerta G0) — rellenar solo la columna TU RESPUESTA"
dc["A4"].font = Font(name=ARIAL, size=11, bold=True)
dc.merge_cells("A4:F4")

for j, h in enumerate(["#","QUE SE DECIDE","OPCIONES","RECOMENDADA Y POR QUE","QUE PASA SI ELIGES OTRA","TU RESPUESTA"], start=1):
    c = dc.cell(row=5, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

fichas = [
("D1","Aprobar el plan y los criterios de la puerta G1 (01.01.01 y 01.01.02)",
 "A) Apruebo todo\nB) Apruebo el plan, repasemos criterios\nC) Quiero cambios",
 "RESUELTA 29/07: se separa QUE se mide (fijado ahora, igual para los 8 candidatos) de DONDE se pone el corte (los umbrales se calibran en G1 con los numeros delante)",
 "El CEO tenia razon en no fijar umbrales a ciegas; y hacia falta fijar la vara de medir antes, o cada mercado se mide distinto y la comparacion no vale","A (con umbrales orientativos)"),
("D2","Horizonte de trabajo y fecha de evaluacion",
 "A) 5 meses\nB) 4 meses\nC) 8 meses",
 "RESPONDIDA 29/07: el CEO fija 1 MES. Evaluacion el 1 de septiembre de 2026 (puerta GM)",
 "AVISO: en 1 mes no hay bot en demo. El objetivo del mes es tener VEREDICTO sobre si existe una estrategia que merezca ir a demo","1 mes (GM el 01/09/2026)"),
("D3","Tiempo del CEO a la semana",
 "A) 1 hora dia fijo\nB) 2-3 horas\nC) 30 minutos",
 "RESPONDIDA 29/07: opcion A. Dia propuesto: LUNES (se cambia con una palabra)",
 "Lunes de agosto: 3, 10, 17, 24 y 31","A — lunes"),
("D5","Confirmar los limites de dinero. El CEO dio: 1.000-2.000 €, caida de cuenta 50-60%, perdida maxima 25%. Esas dos ultimas cifras se contradicen: no se puede parar en -25% y a la vez tolerar -60%",
 "A) Capital 1.000 € · parada dura en -25% (750 €)\nB) Capital 1.000 € · parada dura en -50% (500 €)\nC) Capital 2.000 € · parada dura en -25% (1.500 €)\nD) Otra combinacion que me digas",
 "A — de una caida del 25% se vuelve subiendo un 33%; de una del 50% hay que subir un 100% y de una del 60%, un 150%. Cuanto mas hondo el agujero, mas dificil salir",
 "B o C: mismo criterio, mas dinero expuesto\nD: dime capital y % de parada y queda escrito",""),
]
r = 5
for f in fichas:
    r += 1
    for j, v in enumerate(f, start=1):
        c = dc.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
    dc.cell(row=r, column=6).fill = FILL_CURSO
    dc.row_dimensions[r].height = 78
r += 2
dc.cell(row=r, column=1, value="ABIERTAS AHORA: D1 (confirmar tras leer los criterios) y D5 (limites de dinero). Se responde en una linea: D1=A · D5=A").font = Font(name=ARIAL, size=10, bold=True)
dc.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
for j, w in enumerate([6, 38, 30, 40, 42, 16], start=1):
    dc.column_dimensions[get_column_letter(j)].width = w

# ============ CALENDARIO ============
cal = wb.create_sheet("CALENDARIO")
cal["A1"] = "CALENDARIO DEL MES — del 29 de julio al 1 de septiembre de 2026"
cal["A1"].font = F_TITLE
cal.merge_cells("A1:E1")
for c in range(1, 6):
    cal.cell(row=1, column=c).fill = FILL_TITLE
cal["A2"] = ("OBJETIVO DEL MES: NO es tener el bot operando en demo. Es llegar al 1 de septiembre con una respuesta clara a la pregunta "
             "'¿existe alguna estrategia que merezca pasar a demo?'. Puede ser que si (y arrancamos demo) o que no (y sabemos por que).")
cal["A2"].font = F_SMALL
cal.merge_cells("A2:E2")
cal["A2"].fill = FILL_LEG
cal["A2"].alignment = WRAP
cal.row_dimensions[2].height = 32

for j, h in enumerate(["SEMANA","FECHAS","QUE SE HACE (codigos WBS)","QUE TIENE QUE ESTAR HECHO AL FINAL","TU LUNES (1 h)"], start=1):
    c = cal.cell(row=4, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

semanas = [
("S1","29 jul - 4 ago","Fase 02 completa (02.01 a 02.03): medir los 8 mercados x 3 velas, costes, correlaciones y datos disponibles.\nEN PARALELO: 01.02.01 analisis de gb2 y 03.01.01 montar el repositorio","Mercado(s) y tamaño de vela ELEGIDOS (puerta G1)","Lun 3 ago: leer informe G1 y elegir"),
("S2","5 - 11 ago","03.01.02 a 03.01.06: agentes con su modelo, ejecucion desatendida, respaldo de modelos, fichas automaticas y PRUEBA REAL de un dia.\n04.01.01 elegir broker y abrir demo","Motor funcionando solo 24 h sin caerse + broker elegido","Lun 10 ago: firmar broker (ficha)"),
("S3","12 - 18 ago","04.01.02 y 04.01.03 (costes reales y los 3 cajones de datos) + 04.02.01 a 04.02.04: barrido de fuentes, fichas de hipotesis, filtro de sentido y pre-registro de variantes","3-5 hipotesis con sus variantes pre-registradas","Lun 17 ago: ver las hipotesis elegidas"),
("S4","19 - 25 ago","04.03.01 y 04.03.02: backtests con costes reales sobre el cajon de construir y ajuste sobre el cajon de validacion","Variantes supervivientes tras el ajuste","Lun 24 ago: ver cuantas siguen vivas"),
("S5","26 ago - 1 sept","04.03.03 a 04.03.05: prueba de fuego OOS (una bala por variante), Monte Carlo, walk-forward y veredictos.\n04.04.01 informe de la vuelta","Veredicto pasa / no pasa de cada variante","Lun 31 ago: preparar la evaluacion"),
("GM","1 septiembre","PUERTA DEL MES: evaluacion completa contigo","Decision: arrancar demo, dar otra vuelta al bucle, o replantear","Mar 1 sept: la reunion de verdad"),
]
r = 4
for sm in semanas:
    r += 1
    for j, v in enumerate(sm, start=1):
        c = cal.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
    cal.row_dimensions[r].height = 66
    if sm[0] == "GM":
        for j in range(1, 6):
            cal.cell(row=r, column=j).fill = FILL_CURSO
r += 2
cal.cell(row=r, column=1, value="LO QUE NO CABE EN ESTE MES (y hay que saberlo desde hoy)").font = Font(name=ARIAL, size=11, bold=True)
r += 1
cal.cell(row=r, column=1, value=("1) La DEMO: necesita 8-12 semanas de mercado real y ese reloj no se puede acelerar con agentes. Si el 1 de septiembre hay una estrategia buena, la demo arranca ese dia y termina en noviembre.\n"
                                 "2) Las 3 vueltas del bucle de hipotesis: en un mes cabe UNA vuelta completa y quiza media segunda.\n"
                                 "3) El dinero real: imposible antes de terminar la demo.\n"
                                 "Lo que SI cabe: saber si el planteamiento tiene futuro o no. Eso es mucho, y es la pregunta que te interesa."))
cal.cell(row=r, column=1).font = F_TXT
cal.cell(row=r, column=1).alignment = WRAP
cal.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
cal.row_dimensions[r].height = 82
for j, w in enumerate([9, 16, 62, 42, 26], start=1):
    cal.column_dimensions[get_column_letter(j)].width = w

# ============ AUTONOMIA ============
au = wb.create_sheet("AUTONOMIA")
au["A1"] = "AUTONOMIA — que llega al CEO y que no"
au["A1"].font = F_TITLE
au.merge_cells("A1:C1")
for c in range(1, 4):
    au.cell(row=1, column=c).fill = FILL_TITLE
au["A2"] = "Regla general: el CEO decide en las puertas y en las excepciones. Todo lo demas lo cierra el Orquestador. Ninguna tarea normal necesita firma del CEO."
au["A2"].font = F_SMALL
au.merge_cells("A2:C2")
au["A2"].fill = FILL_LEG

for j, h in enumerate(["SITUACION","QUIEN DECIDE","COMO"], start=1):
    c = au.cell(row=4, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

auto = [
("Cerrar una tarea que cumple su criterio de hecho","Orquestador","Sin consultar. Queda en el informe diario"),
("Elegir en que orden se hacen tareas ya aprobadas","Orquestador","Sin consultar"),
("Crear subtareas dentro de una tarea existente (1.4.1, 1.4.2)","Orquestador","Sin consultar. Se anotan en el WBS"),
("Descartar una hipotesis o variante que no pasa el filtro","Validador","Sin consultar. Queda en el registro de pruebas"),
("Reescribir una tarea ambigua","Orquestador","Sin consultar. Se anota el cambio"),
("Corregir, mover o borrar archivos para mantener el orden","Constructores","Sin consultar. Git permite deshacer"),
("Mejora del motor no prevista","CEO","Se propone en el informe semanal. Sin aprobacion, no se hace"),
("Añadir una tarea nueva de primer nivel al WBS","CEO","Revision semanal"),
("Cambiar de mercado, de vela o de planteamiento","CEO","Solo en una puerta"),
("Gasto nuevo (datos de pago, VPS, broker, creditos extra)","CEO","Excepcion inmediata: se avisa y se para hasta respuesta"),
("Cualquier cosa con dinero real","CEO","Excepcion inmediata"),
("Bloqueo que impide avanzar mas de 24 h","CEO","Excepcion inmediata en el informe diario, marcada en rojo"),
("3 vueltas del bucle de hipotesis sin exito","CEO","Revision completa del planteamiento"),
]
r = 4
for a in auto:
    r += 1
    for j, v in enumerate(a, start=1):
        c = au.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
        if v == "CEO":
            c.fill = FILL_CURSO
r += 2
au.cell(row=r, column=1, value="PRINCIPIO DE RESTRICCION JUSTIFICADA (leccion de gb2)").font = Font(name=ARIAL, size=11, bold=True)
r += 1
au.cell(row=r, column=1, value=("MATIZ IMPORTANTE (29/07): el principio se aplica SOLO al trabajo reversible (archivos, carpetas, codigo, pruebas), porque git lo deshace todo. "
                                "Las barreras sobre lo IRREVERSIBLE se ponen ANTES de soltar nada y no se negocian: dinero real, ordenes al broker, borrar el cajon de datos reservado, gastar dinero nuevo. "
                                "Dicho corto: manga ancha con lo que se puede deshacer, cero manga con lo que no.\n\n"
                                "En gb2 se pusieron muchas restricciones por adelantado, sobre el papel, y luego hubo que ir quitandolas. Aqui se hace al reves: "
                                "se empieza con permisos AMPLIOS y una red de seguridad (git: todo se puede deshacer). Una restriccion nueva solo se añade si ha ocurrido un incidente real, "
                                "y se apunta junto al incidente que la origino. Cada mes se revisan: la restriccion que ya no tenga un incidente vivo detras, se quita."))
au.cell(row=r, column=1).font = F_TXT
au.cell(row=r, column=1).alignment = WRAP
au.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
au.row_dimensions[r].height = 110
for j, w in enumerate([56, 18, 52], start=1):
    au.column_dimensions[get_column_letter(j)].width = w

# ============ PUERTAS Y DECISIONES ============
pd_ = wb.create_sheet("PUERTAS Y DECISIONES")
pd_["A1"] = "PUERTAS DEL PROYECTO"
pd_["A1"].font = F_TITLE
pd_.merge_cells("A1:E1")
for c in range(1, 6):
    pd_.cell(row=1, column=c).fill = FILL_TITLE

hdrs = ["PUERTA","QUE SE DECIDE","CRITERIOS PARA PASAR (en llano)","ESTADO","FECHA"]
for j, h in enumerate(hdrs, start=1):
    c = pd_.cell(row=3, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN

gates = [
("G0","Aprobar plan, criterios y limites","El CEO ha leido el plan y ha puesto por escrito: fecha tope, horas semanales y perdida maxima futura","En curso",""),
("G1","Elegir mercados y tamaño de vela","1) El coste no se come mas del 10-15% del movimiento medio de vela · 2) El conjunto puede generar cientos de operaciones · 3) Minimo 5 años de historial · 4) Correlacion menor de 0,7 entre elegidos · 5) Operable sin nadie delante","Pendiente",""),
("G2","Que estrategias pasan a demo","Solo pasan variantes que: ganan despues de costes en la prueba de fuego (OOS) · aguantan el Monte Carlo · y estaban pre-registradas. Todo veredicto lo firma el validador, no quien la construyo","Pendiente",""),
("G3","Si entra dinero real","La demo (8-12 semanas) se parece a lo que prometian las pruebas; el CEO fija cuanto dinero y que perdida maxima","Pendiente",""),
("G4","Seguir, ampliar o parar (mensual)","El bot respeta sus limites; si pierde mas de lo escrito en 01.01.03, se para sin discusion","Pendiente",""),
]
r = 3
for g in gates:
    r += 1
    for j, v in enumerate(g, start=1):
        c = pd_.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP

r += 2
pd_.cell(row=r, column=1, value="LOS 5 CRITERIOS DE G1, EXPLICADOS CON UN EJEMPLO").font = Font(name=ARIAL, size=12, bold=True)
r += 1
for j, h in enumerate(["CRITERIO","QUE MIDE, EN LLANO","EJEMPLO CON NUMEROS","POR QUE ESE UMBRAL"], start=1):
    c = pd_.cell(row=r, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN
crit = [
("1. Coste relativo (10-15% max)","De cada movimiento tipico de una vela, que parte se lleva el broker antes de que ganes nada","Si el EURUSD se mueve de media 10 pips en una vela de 1 h y el broker cobra 1 pip por operar, el coste es el 10% del movimiento","Con un coste del 30%, el bot tiene que acertar muchisimo solo para empatar. Por debajo del 10% queda margen para que la estrategia gane"),
("2. Cientos de operaciones","Que la estrategia genere suficientes operaciones para saber si gana por habilidad o por suerte","Con 20 operaciones ganadoras no sabes nada: es como decir que sabes jugar a los dados por acertar 20 veces. Con 300 ya se puede juzgar","Menos de 100 operaciones no permite distinguir habilidad de casualidad. Por eso 4h en un solo mercado da problemas: pocas señales"),
("3. Cinco años de datos minimo","Que la estrategia haya visto epocas distintas: subidas, bajadas, crisis y calma","5 años incluyen mercados tranquilos y sacudidas. Una estrategia probada solo en 2024 puede fallar en cuanto cambie el clima","Una estrategia que solo ha visto un tipo de mercado se rompe cuando el mercado cambia, y el mercado siempre cambia"),
("4. Correlacion menor de 0,7","Que los mercados elegidos NO suban y bajen a la vez","EURUSD y GBPUSD suelen moverse casi igual: elegir los dos es hacer la misma apuesta dos veces. Si una pierde, pierden las dos","Diversificar de verdad exige mercados que no se muevan juntos. Por encima de 0,7 la diversificacion es un espejismo"),
("5. Operable sin nadie delante","Que el bot pueda funcionar solo: horarios compatibles, el broker permite bots y no hace falta decidir a mano","Cripto opera 24/7 (bien para desatendido) pero se mueve mucho de noche; forex cierra el fin de semana y abre con saltos de precio","Todo el proyecto se basa en que no estes tu delante. Un mercado que exija vigilancia manual rompe la premisa"),
]
for cr in crit:
    r += 1
    for j, v in enumerate(cr, start=1):
        c = pd_.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
    pd_.row_dimensions[r].height = 62

r += 2
pd_.cell(row=r, column=1, value="REGISTRO DE DECISIONES").font = Font(name=ARIAL, size=12, bold=True)
r += 1
for j, h in enumerate(["FECHA","DECISION","MOTIVO"], start=1):
    c = pd_.cell(row=r, column=j, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = CENTER; c.border = THIN
decisions = [
("2026-07-29","Producto antes que motor; motor en paralelo con maximo el 20% del esfuerzo","Evitar la deriva que hubo en gb2"),
("2026-07-29","Portafolio de 3-5 mercados poco correlacionados, no un solo par","Repartir riesgo y ganar muestra de operaciones"),
("2026-07-29","Mercado y tamaño de vela se deciden en la puerta G1 con datos","Evitar corazonadas"),
("2026-07-29","Revision del CEO: semanal + puertas; nada de firmar tareas sueltas","Direccion por excepcion"),
("2026-07-29","Broker DESPUES de G1; costes provisionales de referencia mientras","Buscar broker ya enfocado al mercado"),
("2026-07-29","Fuente de verdad del WBS: archivo de texto; el Excel es la vista del CEO","Los agentes trabajan mejor con texto"),
("2026-07-29","Cada agente con su modelo segun su tarea (hoja EQUIPO); se confirma con el analisis de gb2","Replicar lo que funcionaba en gb2, con criterio"),
("2026-07-29","gb2 se analiza como informacion, no como copia (tarea 01.02.01)","Aprovechar lecciones sin contaminar el proyecto nuevo"),
("2026-07-29","Validacion en 3 cajones (train/validacion/OOS) + Monte Carlo + walk-forward, con pre-registro de variantes (max. 5-7 por hipotesis)","Cuantas mas variantes se prueban, mas facil que una salga bien por suerte; el pre-registro y el registro de fallidas lo controlan"),
("2026-07-29","Si ninguna variante pasa el filtro: bucle de vuelta a investigacion; a la 3a vuelta sin exito, revision del planteamiento con el CEO","El bucle es sano; infinito, no"),
("2026-07-29","Regla de no-ambiguedad: toda tarea debe poder ejecutarse sin adivinar nada; si un agente tiene que suponer, la tarea vuelve al orquestador","Lo ambiguo fue una causa del caos de gb2"),
("2026-07-29","Principio de restriccion justificada: se empieza con permisos amplios + git como red de seguridad; una restriccion solo se añade tras un incidente real y se revisa cada mes","En gb2 se restringio de mas sobre el papel y hubo que ir quitando restricciones"),
("2026-07-29","Modelos asignados por puesto (hoja EQUIPO): Fable 5 en validacion y arquitectura, Opus 5 en orquestacion, Sonnet 5 en construccion e investigacion, Haiku 4.5 en secretaria","Consultado en platform.claude.com el 29/07/2026; se paga el modelo caro solo donde un error cuesta dinero"),
("2026-07-29","Todo agente con Fable 5 lleva modelo de respaldo obligatorio","Fable 5 estuvo suspendido en junio de 2026 y puede rechazar peticiones por sus filtros; el motor no puede depender de un solo modelo"),
("2026-07-29","La Fase 03 no se da por buena hasta pasar un dia entero de trabajo desatendido real (03.01.05)","Evitar el error de gb2: motor perfecto en papel que no aguanta la realidad"),
("2026-07-29","Escalado definido en la hoja AUTONOMIA: el CEO solo interviene en puertas y excepciones","El CEO no firma tareas"),
("2026-07-29","D2 del CEO: horizonte de 1 mes con evaluacion el 1 de septiembre de 2026 (puerta GM). NO es fecha de demo: en 1 mes el objetivo es tener veredicto sobre si existe una estrategia que merezca ir a demo","Decision del CEO el 29/07/2026"),
("2026-07-29","D3 del CEO: 1 hora semanal, lunes, dia fijo","Decision del CEO el 29/07/2026"),
("2026-07-29","Fase 03 (montar la casa) pasa a ejecutarse EN PARALELO con la Fase 02: el motor no depende del mercado elegido","Ganar 1 semana dentro del mes; lo forzo el plazo del CEO"),
("2026-07-29","D1 resuelta: se fija AHORA que se mide (misma vara para los 8 candidatos) y se calibran los umbrales en G1 con los numeros delante","El CEO no quiere poner cortes a ciegas; sin vara comun, cada mercado se mediria distinto y la comparacion no valdria"),
("2026-07-29","Los guardarrailes se separan en dos: lo reversible empieza permisivo (git deshace); lo irreversible (dinero, ordenes al broker, borrar datos reservados) lleva barrera desde el minuto uno","Matiz aportado por un video de TikTok analizado el 29/07"),
("2026-07-29","Se añade cola de aprobacion del CEO con Aprobado / Saltar / Corregir, y toda correccion escrita va a LECCIONES.md","Idea del mismo video: el valor esta en que la correccion quede guardada, no en aprobar"),
("2026-07-29","Formato obligatorio de ficha de decision del CEO (hoja DECISIONES CEO): opciones cerradas, recomendacion con motivo, consecuencias y respuesta de una letra","Reducir al minimo el tiempo del CEO: ni redactar, ni buscar, ni calcular"),
]
for d in decisions:
    r += 1
    for j, v in enumerate(d, start=1):
        c = pd_.cell(row=r, column=j, value=v)
        c.border = THIN; c.font = F_TXT; c.alignment = WRAP
for j, w in enumerate([9, 42, 62, 11, 11], start=1):
    pd_.column_dimensions[get_column_letter(j)].width = w

wb.save("WBS_Bot_Trading_v0.7.xlsx")
print("OK filas plan:", last_row)
