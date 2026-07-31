#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla 25: una barrera no verificada por ejecucion NO es una barrera.

Inyecta cada caso prohibido y comprueba que se bloquea. En el proyecto anterior una capa entera de
seguridad estuvo documentada como activa durante meses sin funcionar nunca; esto existe para que no
vuelva a pasar.

Uso:  python3 03-motor/scripts/verificar_barreras.py
Salida: informe por pantalla + codigo de salida 1 si alguna barrera NO esta verificada.
"""
import os, subprocess, sys, tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
res = []

def prueba(nombre, regla, fn):
    try:
        bloqueado, detalle = fn()
    except Exception as e:
        bloqueado, detalle = False, f"la prueba fallo: {e}"
    res.append((nombre, regla, bloqueado, detalle))

def sh(cmd):
    p = subprocess.run(cmd, shell=True, cwd=RAIZ, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()

# 1 — hooks instalados
def t_hooks():
    cod, out = sh("git config core.hooksPath")
    ok = out.strip() == ".githooks"
    return ok, f"core.hooksPath = '{out.strip() or 'sin configurar'}' (debe ser .githooks)"

# 2 — el pre-commit bloquea datos
def t_datos_git():
    ruta = os.path.join(RAIZ, "02-datos", "bruto", "_PRUEBA_BARRERA.csv")
    open(ruta, "w").write("prueba,1\n")
    try:
        cod, out = sh("git add -f 02-datos/bruto/_PRUEBA_BARRERA.csv && git commit -m '02.02.01: prueba de barrera' --no-edit")
        bloqueado = cod != 0
        sh("git reset HEAD 02-datos/bruto/_PRUEBA_BARRERA.csv")
        if not bloqueado:
            sh("git reset --soft HEAD~1")
        return bloqueado, "el commit fue rechazado" if bloqueado else "EL COMMIT PASO: los datos entrarian en git"
    finally:
        if os.path.exists(ruta): os.remove(ruta)

# 3 — .gitignore ignora datos de verdad
def t_gitignore():
    ruta = os.path.join(RAIZ, "02-datos", "limpio", "_PRUEBA.csv")
    open(ruta, "w").write("x\n")
    try:
        cod, out = sh("git status --porcelain 02-datos/")
        return out.strip() == "", f"git status 02-datos/ devolvio: '{out.strip() or 'vacio'}'"
    finally:
        if os.path.exists(ruta): os.remove(ruta)

# 4 — el cajon reservado es legible por terminal (limitacion conocida)
def t_reservado_shell():
    d = os.path.join(RAIZ, "02-datos", "reservado")
    legible = os.access(d, os.R_OK)
    return (not legible), ("el sistema de ficheros permite leer el cajon reservado: la barrera es "
                           "SOLO de permisos de Claude Code, no del sistema operativo. "
                           "Un script de Python lanzado por un agente PODRIA leerlo." if legible
                           else "no legible desde el sistema de ficheros")

# 5 — el commit-msg exige codigo WBS
def t_mensaje():
    cod, out = sh("echo 'arreglado el tema ese' > /tmp/_msg && .githooks/commit-msg /tmp/_msg")
    return cod != 0, "mensaje sin codigo WBS rechazado" if cod != 0 else "PASO un mensaje sin codigo WBS"

prueba("Hooks de git instalados",            "—",  t_hooks)
prueba("Los datos no entran en git",         "27", t_datos_git)
prueba(".gitignore ignora 02-datos",         "27", t_gitignore)
prueba("Cajon reservado fuera de alcance",   "22", t_reservado_shell)
prueba("El mensaje exige codigo WBS",        "1",  t_mensaje)

print("\n" + "=" * 78)
print("VERIFICACION DE BARRERAS (regla 25)")
print("=" * 78)
fallos = 0
for nombre, regla, ok, det in res:
    estado = "VERIFICADA    " if ok else "NO VERIFICADA "
    if not ok: fallos += 1
    print(f"[{estado}] (regla {regla:>2}) {nombre}\n{'':17}{det}")
print("=" * 78)
if fallos:
    print(f"\n{fallos} barrera(s) NO VERIFICADA(S).")
    print("Regla 25: se documentan como 'no verificadas', NUNCA como muro.")
    print("Escalar al CEO como excepcion inmediata.")
else:
    print("\nTodas verificadas por ejecucion.")
print("\nLO QUE ESTA PRUEBA NO PUEDE DEMOSTRAR:")
print("  · Que cada agente corra en el modelo de su ficha (se comprueba por gasto: tarea 03.01.04).")
print("  · Que las reglas de prosa de CLAUDE.md se cumplan. Esas no tienen muro mecanico.")
sys.exit(1 if fallos else 0)
