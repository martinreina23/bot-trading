#!/usr/bin/env python3
"""Contador mecanico del reparto PRODUCTO / MOTOR — tarea 03.01.18 del WBS.

Por que existe: el techo del 20% de motor (regla 8 de CLAUDE.md) era prosa y nadie lo
media. La primera vez que se midio, el 01/08/2026, el reparto real era 7 de 16 commits
(43,8%), mas del doble del techo, y el proyecto llevaba desde el arranque sin saberlo.

Dos usos:
  1. A mano:            python3 .claude/hooks/contador_producto_motor.py
     Con un rango:      python3 .claude/hooks/contador_producto_motor.py --hasta 79902cb
     Con detalle:       python3 .claude/hooks/contador_producto_motor.py --detalle
  2. Como hook SessionStart: con --hook escribe el JSON que Claude Code espera, e inyecta
     el numero en el contexto al arrancar cada tirada.

REGLA DE CLASIFICACION — depurada en tres rondas de revision el 01/08/2026 y registrada en
`01-investigacion/ecosistema/INFORME_AWESOME.md`. NO se reinventa:

  1. Commit CON codigo WBS -> manda la FASE del codigo, que es la declaracion autorizada
     de que era ese trabajo:
       02, 04, 05, 06 -> PRODUCTO      03, 07 -> MOTOR
       01.01.* -> PRODUCTO (direccion y puertas)
       01.02.* -> MOTOR, porque sus propias fichas del WBS llevan escrito
                  «Carril de motor: cuenta contra el 20%».
  2. Commit SIN codigo WBS (los que `.githooks/commit-msg` exime, y el `arranque del
     proyecto` que es anterior al hook) -> y SOLO entonces, se clasifica por RUTAS:
       toca .claude/**, .githooks/**, 05-vista-ceo/** o un fichero de configuracion de la
         raiz -> MOTOR
       toca SOLO 00-direccion/** -> PAPELEO, que se declara aparte y NO entra en el cociente
       el resto -> PRODUCTO
  3. `03-motor/**` NUNCA se usa como criterio. Esa carpeta contiene PRODUCTO: cinco de sus
     scripts son calculo de mercado. Es una colision de nombres — «motor» en CLAUDE.md es
     la fabrica de agentes; la carpeta `03-motor/` es donde vive el calculo del bot, que
     segun esa misma frase de CLAUDE.md es el producto.

PROHIBIDO contar solo los commits que llevan codigo WBS. Ese es el punto ciego que ya
falseo el numero una vez: dio 20,0% cuando el real era 43,8%, porque el trabajo de motor
es precisamente el que se cuela bajo `meta:` y `org:` (L-016 de LECCIONES.md). Este fichero
no tiene ninguna rama que filtre por codigo WBS antes de contar.

Es un INDICADOR, no una medida: un commit no es una unidad de esfuerzo y puede tocar rutas
de los dos lados. Su valor esta en que deje de ser cero.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# --- criterio 1: la fase del codigo WBS ---------------------------------------------
FASES_PRODUCTO = {"02", "04", "05", "06"}
FASES_MOTOR = {"03", "07"}
GRUPOS_FASE_01 = {"01.01": "producto", "01.02": "motor"}

# --- criterio 2: rutas, SOLO para commits sin codigo WBS ------------------------------
PREFIJOS_MOTOR = (".claude/", ".githooks/", "05-vista-ceo/")
CONFIG_RAIZ = {"CLAUDE.md", "INSTALAR.md", "README.md", "requirements.txt", ".gitignore"}
PREFIJO_PAPELEO = "00-direccion/"

RE_CODIGO = re.compile(r"^(\d{2})\.(\d{2})\.\d{2}")


def git(*args):
    return subprocess.run(
        ["git", "-C", str(RAIZ), *args], capture_output=True, text=True, check=True
    ).stdout


def clasificar_por_codigo(asunto):
    """Devuelve 'producto' | 'motor' | None segun la fase del codigo WBS del mensaje."""
    m = RE_CODIGO.match(asunto.strip())
    if not m:
        return None
    fase, grupo = m.group(1), f"{m.group(1)}.{m.group(2)}"
    if fase == "01":
        return GRUPOS_FASE_01.get(grupo, "producto")
    if fase in FASES_MOTOR:
        return "motor"
    if fase in FASES_PRODUCTO:
        return "producto"
    return "producto"


def clasificar_por_rutas(ficheros):
    """Solo para commits SIN codigo WBS. `03-motor/**` no se mira nunca."""
    utiles = [f for f in ficheros if not f.startswith("03-motor/")]
    for f in utiles:
        if f.startswith(PREFIJOS_MOTOR) or f in CONFIG_RAIZ:
            return "motor"
    if utiles and all(f.startswith(PREFIJO_PAPELEO) for f in utiles):
        return "papeleo"
    return "producto"


def clasificar(sha, asunto):
    por_codigo = clasificar_por_codigo(asunto)
    if por_codigo:
        return por_codigo, "codigo WBS"
    ficheros = [f for f in git("show", "--name-only", "--pretty=format:", sha).split("\n") if f]
    return clasificar_por_rutas(ficheros), "rutas"


def contar(desde=None, hasta="HEAD"):
    rango = f"{desde}..{hasta}" if desde else hasta
    salida = git("log", "--reverse", "--pretty=format:%h\x1f%s", rango).strip()
    filas = []
    for linea in salida.split("\n"):
        if not linea:
            continue
        sha, asunto = linea.split("\x1f", 1)
        carril, via = clasificar(sha, asunto)
        filas.append((sha, asunto, carril, via))
    return filas


def resumen(filas):
    motor = sum(1 for f in filas if f[2] == "motor")
    producto = sum(1 for f in filas if f[2] == "producto")
    papeleo = sum(1 for f in filas if f[2] == "papeleo")
    denominador = motor + producto
    pct = (motor / denominador * 100) if denominador else 0.0
    return motor, producto, papeleo, pct


def linea_contexto(filas):
    motor, producto, papeleo, pct = resumen(filas)
    techo = " — POR ENCIMA DEL TECHO DEL 20% (regla 8 de CLAUDE.md)" if pct > 20 else ""
    return (
        f"REPARTO PRODUCTO/MOTOR sobre {motor + producto + papeleo} commits: "
        f"motor {motor}, producto {producto}, papeleo {papeleo} (fuera del cociente). "
        f"MOTOR = {pct:.1f}%{techo}. "
        "Contado por 03.01.18 clasificando TODOS los commits, tambien los que no llevan "
        "codigo WBS: contar solo los que lo llevan da 20,0% cuando el real es 43,8% (L-016)."
    )


def main():
    p = argparse.ArgumentParser(description="Reparto producto/motor por commit.")
    p.add_argument("--desde", default=None, help="ref exclusiva de inicio")
    p.add_argument("--hasta", default="HEAD", help="ref inclusiva de fin (por defecto HEAD)")
    p.add_argument("--detalle", action="store_true", help="una linea por commit")
    p.add_argument("--hook", action="store_true", help="salida JSON para el hook SessionStart")
    a = p.parse_args()

    try:
        filas = contar(a.desde, a.hasta)
    except subprocess.CalledProcessError as e:
        if a.hook:
            # Un hook que revienta no puede impedir arrancar la sesion.
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"Contador producto/motor no disponible: {e.stderr.strip()[:200]}",
            }}))
            return 0
        raise

    if a.hook:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": linea_contexto(filas),
        }}))
        return 0

    motor, producto, papeleo, pct = resumen(filas)
    if a.detalle:
        for sha, asunto, carril, via in filas:
            print(f"  {sha}  {carril:9s} ({via:9s})  {asunto[:62]}")
        print()
    print(f"commits examinados : {len(filas)}")
    print(f"  MOTOR            : {motor}")
    print(f"  PRODUCTO         : {producto}")
    print(f"  PAPELEO          : {papeleo}  (declarado aparte, fuera del cociente)")
    print(f"REPARTO MOTOR      : {pct:.1f}%   (techo de la regla 8 de CLAUDE.md: 20%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
