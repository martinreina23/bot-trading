#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica por EJECUCION que el Excel del CEO dice la verdad sobre WBS.md.

Uso:  .venv/bin/python 05-vista-ceo/verificar_excel.py
Sale con codigo 1 si algo FALLA. Los AVISOS no tumban la ejecucion pero se leen.

Por que existe: el 31/07/2026 el formato del WBS cambio (la ficha pasó a ir DELANTE
del estado, dentro de la misma celda) y el generador siguió leyendo solo el principio
de la celda. Resultado: 4 tareas hechas salieron como pendientes en la vista del CEO,
sin que nada avisara. Regla 25: lo que no se prueba por ejecucion, no esta verificado.

Este fichero NO comparte codigo con generar_excel.py a proposito: vuelve a leer WBS.md
con su propio analizador. Si los dos coinciden, es que el dato es bueno; si un unico
analizador se equivoca, la comprobacion no valdria nada.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# Rutas por argumento SOLO para la prueba de inyeccion (regla 25: se comprueba que el
# verificador muerde metiendole un WBS roto). En uso normal no se pasan argumentos.
WBS = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "00-direccion" / "WBS.md"
XLSX = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "05-vista-ceo" / "WBS_Bot_Trading_v0.9.xlsx"

FALLOS, AVISOS = [], []
ESTADOS = ("pendiente", "en_curso", "hecha", "bloqueada")
ETIQUETA = {"pendiente": "Pendiente", "en_curso": "En curso", "hecha": "Hecha", "bloqueada": "Bloqueada"}


def fallo(prueba, detalle):
    FALLOS.append((prueba, detalle))
    print(f"  FALLO  {prueba}: {detalle}")


def aviso(prueba, detalle):
    AVISOS.append((prueba, detalle))
    print(f"  AVISO  {prueba}: {detalle}")


def ok(prueba, detalle=""):
    print(f"  OK     {prueba}{': ' + detalle if detalle else ''}")


# ---------------------------------------------------------------- lectura independiente
def leer_wbs():
    """Recorre el fichero entero buscando filas de tarea, sin fiarse de las secciones."""
    tareas = {}
    for linea in WBS.read_text(encoding="utf-8").splitlines():
        s = linea.strip()
        if not s.startswith("|"):
            continue
        celdas = [c.strip() for c in s.strip("|").split("|")]
        if len(celdas) < 5:
            continue
        codigo = celdas[0].strip("*` ")
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", codigo):
            continue
        if codigo in tareas:
            fallo("codigos unicos", f"{codigo} aparece dos veces en WBS.md")
        tareas[codigo] = {
            "codigo": codigo,
            "tarea": celdas[1],
            "responsable": celdas[2],
            "depende": celdas[3],
            "celda_estado": celdas[4],
        }
    return tareas


def estado_de(celda, codigo):
    """Estado declarado. Nunca lo adivina: si no hay marca, es un FALLO."""
    apertura = re.match(r"\*{0,2}(pendiente|en_curso|hecha|bloqueada)\*{0,2}\b", celda, flags=re.I)
    if apertura:
        return apertura.group(1).lower()
    negritas = re.findall(r"\*\*(pendiente|en_curso|hecha|bloqueada)\*\*", celda, flags=re.I)
    if negritas:
        if len(negritas) > 1:
            aviso("estado declarado", f"{codigo}: {len(negritas)} marcas en negrita {negritas}; vale la ultima")
        return negritas[-1].lower()
    fallo("estado declarado", f"{codigo}: su celda ESTADO no declara ningun estado -> "
                             f"el generador lo daria por 'pendiente' sin saberlo. Celda: {celda[:80]}...")
    return None


def dependencias(t, todos):
    salida = []
    for trozo in re.split(r"[,;]", t["depende"].replace("—", "").replace("–", "")):
        d = trozo.strip().strip("*` ") if not trozo.strip().endswith("*") else trozo.strip()
        if not d:
            continue
        if d.endswith("*"):
            pref = d.rstrip("*").rstrip(".")
            hijos = [c for c in todos if c.startswith(pref + ".") and c != t["codigo"]]
            if not hijos:
                fallo("dependencias existen", f"{t['codigo']} depende de '{d}' y no encaja con ninguna tarea")
            salida += hijos
        elif re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", d):
            if d not in todos:
                fallo("dependencias existen", f"{t['codigo']} depende de {d}, que no existe en el WBS")
            else:
                salida.append(d)
    return sorted(set(salida))


print(f"VERIFICACION DE LA VISTA DEL CEO\n  WBS  : {WBS}\n  Excel: {XLSX}\n")

if not XLSX.exists():
    sys.exit("FALLO: no existe el Excel. Ejecuta antes generar_excel.py")

try:
    import openpyxl
except ImportError:
    sys.exit("FALLO: falta openpyxl. Instala con: .venv/bin/pip install openpyxl")

WBS_TAREAS = leer_wbs()
for t in WBS_TAREAS.values():
    t["estado"] = estado_de(t["celda_estado"], t["codigo"])
    t["deps"] = dependencias(t, WBS_TAREAS)

wb = openpyxl.load_workbook(XLSX)
hoja = wb["TAREAS"]
EXCEL = {}
for r in range(1, hoja.max_row + 1):
    cod, est = hoja.cell(r, 1).value, hoja.cell(r, 5).value
    if isinstance(cod, str) and re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", cod):
        if cod in EXCEL:
            fallo("filas unicas", f"{cod} aparece dos veces en la hoja TAREAS")
        EXCEL[cod] = est

print("\n1. El Excel es posterior al WBS")
if XLSX.stat().st_mtime < WBS.stat().st_mtime:
    fallo("Excel al dia", "el WBS se ha tocado despues de generar el Excel: regeneralo")
else:
    ok("Excel al dia")

print("\n2. Censo de tareas: ni una perdida, ni una inventada")
faltan = sorted(set(WBS_TAREAS) - set(EXCEL))
sobran = sorted(set(EXCEL) - set(WBS_TAREAS))
if faltan:
    fallo("censo", f"en el WBS pero NO en el Excel: {faltan}")
if sobran:
    fallo("censo", f"en el Excel pero NO en el WBS: {sobran}")
if not faltan and not sobran:
    ok("censo", f"{len(WBS_TAREAS)} tareas en los dos sitios")

print("\n3. Estado de cada tarea, leido dos veces con analizadores distintos")
discrepa = []
for cod, t in sorted(WBS_TAREAS.items()):
    if t["estado"] is None:
        continue
    esperado = ETIQUETA[t["estado"]]
    if EXCEL.get(cod) != esperado:
        discrepa.append(f"{cod}: Excel dice '{EXCEL.get(cod)}' y el WBS dice '{esperado}'")
if discrepa:
    for d in discrepa:
        fallo("estados", d)
else:
    ok("estados", f"{len(WBS_TAREAS)} coinciden")

print("\n4. Ciclos de dependencias")
ciclo = None
for inicio in WBS_TAREAS:
    pila, vistos = [(inicio, [inicio])], set()
    while pila and not ciclo:
        nodo, camino = pila.pop()
        for d in WBS_TAREAS[nodo]["deps"]:
            if d == inicio:
                ciclo = " -> ".join(camino + [d])
                break
            if d not in vistos:
                vistos.add(d)
                pila.append((d, camino + [d]))
    if ciclo:
        break
if ciclo:
    fallo("ciclos", f"dependencia circular: {ciclo}")
else:
    ok("ciclos", "ninguno")

print("\n5. La cola de SIGUIENTE respeta sus propias reglas")
sig = wb["SIGUIENTE"]
grupo, cola, esperando = None, [], []
for r in range(1, sig.max_row + 1):
    a, b = sig.cell(r, 1).value, sig.cell(r, 2).value
    if isinstance(a, str) and a.startswith("SE PUEDE TRABAJAR YA"):
        grupo = "cola"
    elif isinstance(a, str) and a.startswith("ESPERANDO"):
        grupo = "esperando"
    elif isinstance(b, str) and re.fullmatch(r"\d{2}\.\d{2}\.\d{2}", b):
        (cola if grupo == "cola" else esperando).append(b)

vivas = {c for c, t in WBS_TAREAS.items() if t["estado"] != "hecha"}
if set(cola) | set(esperando) != vivas:
    fallo("cola completa", f"faltan o sobran tareas vivas: "
                           f"{sorted(vivas ^ (set(cola) | set(esperando)))}")
else:
    ok("cola completa", f"{len(vivas)} tareas vivas repartidas en cola({len(cola)}) y espera({len(esperando)})")
if set(cola) & set(esperando):
    fallo("cola sin duplicados", f"aparecen en los dos grupos: {sorted(set(cola) & set(esperando))}")
for c in cola:
    pendientes = [d for d in WBS_TAREAS[c]["deps"] if WBS_TAREAS[d]["estado"] != "hecha"]
    if pendientes:
        fallo("cola trabajable", f"{c} esta en 'se puede trabajar ya' pero espera a {pendientes}")
for c in esperando:
    pendientes = [d for d in WBS_TAREAS[c]["deps"] if WBS_TAREAS[d]["estado"] != "hecha"]
    if not pendientes:
        fallo("espera justificada", f"{c} esta en 'esperando' y no le falta ninguna dependencia")
if not FALLOS or all(p[0] not in ("cola trabajable", "espera justificada") for p in FALLOS):
    ok("orden de la cola", "cada tarea esta en el grupo que le toca")

print("\n6. Las cuentas del PANEL (formulas evaluadas de verdad)")
try:
    import formulas  # opcional: pesado, pero es la unica prueba real de las formulas
    modelo = formulas.ExcelModel().loads(str(XLSX)).finish()
    sol = modelo.calculate()
    def celda(ref):
        v = sol.get(f"'[{XLSX.name}]PANEL'!{ref}")
        try:
            return v.value[0, 0]
        except Exception:
            return v
    total = celda("B11")
    hechas = celda("C11")
    hechas_wbs = sum(1 for t in WBS_TAREAS.values() if t["estado"] == "hecha")
    if int(total) != len(WBS_TAREAS):
        fallo("panel", f"el panel suma {total} tareas y el WBS tiene {len(WBS_TAREAS)}")
    elif int(hechas) != hechas_wbs:
        fallo("panel", f"el panel cuenta {hechas} hechas y el WBS tiene {hechas_wbs}")
    else:
        ok("panel", f"total {int(total)} · hechas {int(hechas)}, cuadra con el WBS")
except ImportError:
    aviso("panel", "sin el paquete 'formulas' no se pueden evaluar los COUNTIFS: NO VERIFICADO")

print("\n7. Las tareas hechas tienen su entregable en disco")
sin_artefacto = []
for cod, t in sorted(WBS_TAREAS.items()):
    if t["estado"] != "hecha":
        continue
    corte = re.search(r"\*\*hecha\*\*|^hecha", t["celda_estado"], flags=re.I)
    cola_celda = t["celda_estado"][corte.end():] if corte else t["celda_estado"]
    for nombre in set(re.findall(r"`([\w./-]+\.(?:md|py|json|csv|txt|xlsx))`", cola_celda)):
        base = Path(nombre).name
        if not list(RAIZ.rglob(base)):
            sin_artefacto.append(f"{cod} dice haber entregado {nombre} y no esta en el repositorio")
if sin_artefacto:
    for s in sin_artefacto:
        aviso("entregables", s)
else:
    ok("entregables", "todos los ficheros citados por las tareas hechas existen")

print("\n8. Regla 24: los datos siguen fuera de git")
try:
    salida = subprocess.run(["git", "status", "--porcelain", "02-datos/"], cwd=RAIZ,
                            capture_output=True, text=True, timeout=30).stdout.strip()
    if salida:
        fallo("regla 24", f"git ve ficheros dentro de 02-datos/:\n{salida[:400]}")
    else:
        ok("regla 24", "git no ve nada dentro de 02-datos/")
except Exception as e:  # noqa: BLE001
    aviso("regla 24", f"no se pudo comprobar: {e}")

print("\n" + "=" * 70)
if FALLOS:
    print(f"RESULTADO: {len(FALLOS)} FALLOS y {len(AVISOS)} avisos. El Excel NO es de fiar.")
    for p, d in FALLOS:
        print(f"  - [{p}] {d}")
    sys.exit(1)
print(f"RESULTADO: sin fallos. {len(AVISOS)} avisos." if AVISOS else "RESULTADO: sin fallos ni avisos.")
for p, d in AVISOS:
    print(f"  - [{p}] {d}")
sys.exit(0)
