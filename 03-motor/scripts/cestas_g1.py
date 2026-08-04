#!/usr/bin/env python3
"""Tarea 02.03.02 — enumeración de cestas admisibles bajo G1-C5 (D-11).

NO recalcula ninguna correlación: lee el artefacto cerrado
`04-resultados/correlaciones_8x8.json` (tarea 02.02.03, hecha y verificada) y
comprueba, por par de instrumentos, si |correlación| <= 0,7 en LAS TRES ventanas
(3 meses, 1 año, 2 años) de la vela dada, que es lo que exige el criterio
G1-C5 aprobado en D-11 (`00-direccion/DECISIONES.md`, sección D-11; forma
operativa en `00-direccion/WBS.md`, sección "## Puertas", viñeta G1-C5).

Cripto queda fuera de la enumeración principal porque el criterio aprobado ya
la deja "FUERA de la cesta por defecto" (solo 1 de las 3 ventanas existe:
regla 26 de CLAUDE.md, los guardias bloquean por defecto). Un par con hueco en
alguna ventana se trata como INVERIFICABLE, no como aprobado.

Uso: python3 03-motor/scripts/cestas_g1.py
Determinista: sin red, sin datos nuevos. Insumo: el JSON cerrado.
"""

import itertools
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
JSON_CORRELACIONES = RAIZ / "04-resultados" / "correlaciones_8x8.json"

UMBRAL = 0.7  # G1-C5 (D-11)
VENTANAS = ["3_meses", "1_anio", "2_anios"]
NO_CRIPTO = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "XAUUSD"]


def cargar():
    with open(JSON_CORRELACIONES) as fh:
        return json.load(fh)


def correlacion(mats, vela, ventana, a, b):
    celdas = mats[vela][ventana]["correlaciones"]
    if a in celdas and b in celdas[a]:
        return celdas[a][b]
    return None


def par_admisible(mats, vela, a, b):
    """(True/False/None, valores). None = alguna ventana es hueco (inverificable)."""
    valores = []
    for ventana in VENTANAS:
        v = correlacion(mats, vela, ventana, a, b)
        if v is None:
            return None, valores
        valores.append(v)
    return all(abs(v) <= UMBRAL for v in valores), valores


def enumerar(vela, mats):
    print(f"=== VELA {vela} — pares no-cripto contra G1-C5 (|corr|<=0,7 en las 3 ventanas) ===")
    pasan, fallan = [], []
    for a, b in itertools.combinations(NO_CRIPTO, 2):
        ok, valores = par_admisible(mats, vela, a, b)
        maximo = max(abs(v) for v in valores)
        (pasan if ok else fallan).append((a, b, maximo, valores))
    print(f"PASAN ({len(pasan)}):")
    for a, b, mx, vs in sorted(pasan, key=lambda t: -t[2]):
        print(f"  {a}/{b}: max|corr|={mx:.4f}  ({', '.join(f'{v:+.3f}' for v in vs)})")
    print(f"FALLAN ({len(fallan)}):")
    for a, b, mx, vs in sorted(fallan, key=lambda t: -t[2]):
        print(f"  {a}/{b}: max|corr|={mx:.4f}  ({', '.join(f'{v:+.3f}' for v in vs)})")

    for tamano in (5, 4, 3):
        cestas = []
        for combo in itertools.combinations(NO_CRIPTO, tamano):
            oks = [par_admisible(mats, vela, a, b)[0]
                   for a, b in itertools.combinations(combo, 2)]
            if all(o is True for o in oks):
                mx = max(max(abs(v) for v in par_admisible(mats, vela, a, b)[1])
                         for a, b in itertools.combinations(combo, 2))
                cestas.append((combo, mx))
        etiqueta = f"cestas de {tamano} instrumentos no-cripto totalmente admisibles"
        if cestas:
            print(f"{etiqueta}: {len(cestas)}")
            for combo, mx in sorted(cestas, key=lambda t: t[1]):
                print(f"  {' + '.join(combo)}  (max|corr| de la cesta: {mx:.4f})")
        else:
            print(f"{etiqueta}: NINGUNA")
    print()


def cripto(mats):
    print("=== Cripto a 4h: ventanas con dato real (las demás son hueco declarado) ===")
    for ventana in VENTANAS:
        con_dato = [b for b in NO_CRIPTO + ["ETHUSD"]
                    if correlacion(mats, "4h", ventana, "BTCUSD", b) is not None]
        print(f"  BTCUSD {ventana}: {con_dato if con_dato else 'NADIE (hueco)'}")


def main():
    datos = cargar()
    mats = datos["matrices"]
    assert datos["umbral_correlacion_g1"] == UMBRAL, "umbral del JSON distinto del aprobado"
    for vela in ("4h", "1h"):
        enumerar(vela, mats)
    cripto(mats)


if __name__ == "__main__":
    main()
