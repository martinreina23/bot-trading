#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 02.03.01 (segunda pasada, 02/08/2026) — aritmetica del motivo 3 del veredicto de la
Fase 02 (`04-resultados/veredictos/veredicto_fase_02.md`): el coste del oro medido en feb-2025
(0,26 USD/oz, Pepperstone Razor) se divide contra ATR de jul-2026. Sin segunda fuente primaria
de coste del oro >=2026 en los entregables, se aplica como COTA SUPERIOR la deriva medida en los
dos instrumentos que SI tienen dos fechas en `coste_operar.md` (BTC +82%, ETH +134% entre
feb-2025 y abr-2026) y se comprueba si algun veredicto de G1 cambia bajo esa cota.

Insumos (NO se recalcula nada desde cero, prohibido por la ficha; se leen valores ya cerrados):
  - 04-resultados/atr_15m_1h_4h.json           (tarea 02.02.01, cerrada y verificada)
  - 01-investigacion/mercados/coste_operar.md  (tarea 02.01.02): coste XAUUSD 0,26 USD/oz
    ida y vuelta (fila XAUUSD, Tabla FINAL) y las dos parejas de fechas de BTCUSD (36,90/20,22)
    y ETHUSD (7,04/3,01) de las que salen los factores de deriva.
  - 01-investigacion/mercados/arrastre_coste.md, tabla del escenario central: 79,9 ops/año
    (riesgo 1%, stop 1xATR, actividad 5%).
  - D-11 (00-direccion/DECISIONES.md) / veredicto_criterios_g1.md, ataque A4: swap XAUUSD largo
    OANDA jul-2026, +2,36% anual con 1 noche/operacion.

Este script NO descarga nada, NO toca 02-datos/ (y jamas 02-datos/reservado/), NO escribe
ningun fichero: imprime la aritmetica para que un tercero la reproduzca ejecutandolo
(regla 9 de CLAUDE.md, nivel 1).
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ATR_JSON = RAIZ / "04-resultados" / "atr_15m_1h_4h.json"

atr = json.load(open(ATR_JSON))
velas = atr['instrumentos']['XAUUSD']['velas']
print("claves de velas:", list(velas.keys()))
for v, c in velas.items():
    print(v, {k: c.get(k) for k in ('atr14_medio','atr14_mediana','atr14_p10','atr14_p90')})

# --- Motivo 3: aplicar factores de deriva (cota superior) al coste del oro de feb-2025 ---
COSTE = 0.26            # USD/oz ida y vuelta, coste_operar.md fila XAUUSD (Pepperstone feb-2025)
F82, F134 = 1.82, 2.34  # deriva medida en BTC (+82%) y ETH (+134%) entre feb-2025 y abr-2026

# Verificacion de los factores contra los propios documentos (coste_operar.md, filas BTCUSD/ETHUSD):
print("\nfactor BTC 36,90/20,22 =", round(36.90/20.22, 4), "-> +%.1f%%" % ((36.90/20.22-1)*100))
print("factor ETH 7,04/3,01  =", round(7.04/3.01, 4), "-> +%.1f%%" % ((7.04/3.01-1)*100))

print("\n--- G1-C2 (coste ida y vuelta / ATR p10 <= 10%) XAUUSD ---")
for v, c in velas.items():
    p10 = c['atr14_p10']
    base = COSTE/p10*100
    print(f"{v}: base {base:.2f}%  | x1,82 -> {COSTE*F82/p10*100:.2f}%  | x2,34 -> {COSTE*F134/p10*100:.2f}%")

print("\n--- G1-C1 XAUUSD 4h (coste relativo mediana -> arrastre y tope de operaciones/ano) ---")
med4h = velas['4h']['atr14_mediana']
cr = COSTE/med4h*100
OPS_CENTRAL = 79.9      # arrastre_coste.md, tabla escenario central (riesgo 1%, stop 1xATR, actividad 5%)
for nombre, f in (("base", 1.0), ("x1,82", F82), ("x2,34", F134)):
    cr_f = cr*f
    coste_op_pct_capital = 0.01*cr_f          # riesgo 1% x (cr/100) / stop 1  -> en % del capital
    arrastre = OPS_CENTRAL*coste_op_pct_capital
    tope = 5.0/coste_op_pct_capital
    print(f"{nombre}: cr mediana {cr_f:.4f}% | arrastre central {arrastre:.2f}% (umbral 5%) | tope ops/ano {tope:.0f}")

print("\n--- Reproduccion del tope publicado 126-426 (D-11/WBS, 4h) con costes SIN deriva ---")
# XAUUSD (extremo alto) y AUDUSD (extremo bajo), coste_relativo.md tabla mediana
aud = json.load(open(ATR_JSON))['instrumentos']['AUDUSD']['velas']['4h']['atr14_mediana']
cr_aud = (0.85*0.0001)/aud*100
print(f"XAUUSD 4h: 5% / (1% x {cr:.5f}%) = {5.0/(0.01*cr):.1f}  (publicado: 426)")
print(f"AUDUSD 4h: 5% / (1% x {cr_aud:.5f}%) = {5.0/(0.01*cr_aud):.1f}  (publicado: 126)")

print("\n--- G1-C3 dentro de G1-C1, XAUUSD 4h largo (swap OANDA jul-2026, SIN deriva: dato vigente) ---")
SWAP_1N = 2.36  # % anual añadido con 1 noche/op, dato de D-11/G1-C3 y veredicto_criterios_g1.md A4
for nombre, f in (("base", 1.0), ("x1,82", F82), ("x2,34", F134)):
    arr = OPS_CENTRAL*0.01*cr*f
    print(f"{nombre}: entrada/salida {arr:.2f}% + 1 noche {SWAP_1N}% = {arr+SWAP_1N:.2f}% | + 2 noches = {arr+2*SWAP_1N:.2f}% (umbral 5%)")
