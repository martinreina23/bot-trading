#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 01.02.02 (pieza T2). Las DOS pruebas ejecutadas que exige el criterio
de HECHO de T2 (00-direccion/WBS.md, seccion "Trasplante desde gb2"):

  PRUEBA 1 -- Reproduccion a mano: un caso calculado con lapiz y papel (los
  numeros esperados se derivan aqui mismo, por escrito, ANTES de llamar al
  motor) se compara digito a digito con la salida real de run_backtest().

  PRUEBA 2 -- Inyeccion del stop: se inyectan velas con salto de precio
  (gap) en ambas direcciones y se comprueba, por ejecucion, que el fill de
  un stop nunca es mejor que el precio disparado -- ni en el caso ordinario
  (cruce intra-vela) ni en el caso de gap. Se contrasta explicitamente
  contra lo que produciria una implementacion ingenua que ignorase el gap.

Uso: .venv/bin/python 03-motor/backtester/verificar_motor.py
Codigo de salida 1 si cualquier prueba falla.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd

from backtester.costs import CostModel, SwapConfig
from backtester.sizing import SizingConfig
from backtester.execution import run_backtest, _find_exit

FALLOS = []


def prueba(nombre, cond, detalle=""):
    estado = "PASA" if cond else "FALLA"
    print(f"  [{estado}] {nombre}" + (f" -- {detalle}" if detalle else ""))
    if not cond:
        FALLOS.append(nombre)


def bar(o, h, l, c):
    return {"open": o, "high": h, "low": l, "close": c}


print("=" * 78)
print("PRUEBA 1 -- REPRODUCCION A MANO")
print("=" * 78)
print("""
Caso (calculado ANTES de ejecutar el motor):

  Velas diarias, corte 22:00 UTC, enero de 2024 (sin transicion de horario
  de verano en EEUU: 17:00 America/New_York = 22:00 UTC exacto todos los
  dias del caso).

    2024-01-08 22:00 UTC (lunes)     -- vela de la SENAL (no se opera en ella)
    2024-01-09 22:00 UTC (martes)    -- vela de ENTRADA: open=100.00 high=102.00 low=99.00  close=101.00
    2024-01-10 22:00 UTC (miercoles) --                  open=101.00 high=103.00 low=100.00 close=102.00
    2024-01-11 22:00 UTC (jueves)    --                  open=102.00 high=104.00 low=101.00 close=103.00
    2024-01-12 22:00 UTC (viernes)   -- vela de SALIDA por tiempo: open=103.00 high=105.00 low=102.00 close=104.00

  Senal: LARGO, stop_price=90.50, sin target, exit_time=2024-01-12 22:00 UTC.

  CostModel: spread_total=1.00 (half_spread=0.50), commission_total=0.10.
  SizingConfig: min_size=0.01, size_step=0.01, risk_pct=0.01 (G1-C6), sin max_risk_pct.
  SwapConfig: largo -0.05 /noche, corto +0.02 /noche, rollover 17:00 America/New_York,
              miercoles triple (triple_weekday=2), fin de semana peso 0.
  Equity inicial: 10 000.00.

  CALCULO A MANO:
    entry_price   = open(martes) + half_spread   = 100.00 + 0.50           = 100.50
    stop_distance = |entry_price - stop_price|   = |100.50 - 90.50|        = 10.00
    riesgo_$      = equity * risk_pct            = 10 000.00 * 0.01        = 100.00
    tamano_bruto  = riesgo_$ / stop_distance      = 100.00 / 10.00          = 10.00   (exacto, sin redondeo)
    exit_price    = close(viernes) - half_spread  = 104.00 - 0.50          = 103.50   (sale por TIEMPO)
    pnl_gross     = (exit-entry) * 1 * tamano      = (103.50-100.50)*10.00  = 30.00
    comision      = commission_total * tamano      = 0.10 * 10.00          = 1.00
    noches swap   = miercoles(peso 3) + jueves(peso 1) entre martes y viernes = 4
                    (martes = entrada, no cuenta; viernes = salida, no cuenta)
    swap_total    = 4 * (-0.05) * tamano            = 4 * -0.05 * 10.00     = -2.00
    pnl_net       = 30.00 - 1.00 + (-2.00)                                  = 27.00
    pnl_r         = pnl_net / (stop_distance*tamano) = 27.00 / 100.00       = 0.27
""")

bars = pd.DataFrame(
    [
        bar(100.00, 100.00, 100.00, 100.00),  # lunes, solo referencia de la senal (no se opera en ella)
        bar(100.00, 102.00, 99.00, 101.00),   # martes, entrada
        bar(101.00, 103.00, 100.00, 102.00),  # miercoles
        bar(102.00, 104.00, 101.00, 103.00),  # jueves
        bar(103.00, 105.00, 102.00, 104.00),  # viernes, salida por tiempo
    ],
    index=pd.to_datetime(
        [
            "2024-01-08 22:00:00",
            "2024-01-09 22:00:00",
            "2024-01-10 22:00:00",
            "2024-01-11 22:00:00",
            "2024-01-12 22:00:00",
        ],
        utc=True,
    ),
)

signals = pd.DataFrame(
    [
        {
            "timestamp": pd.Timestamp("2024-01-08 22:00:00", tz="UTC"),
            "direction": 1,
            "stop_price": 90.50,
            "target_price": float("nan"),
            "exit_time": pd.Timestamp("2024-01-12 22:00:00", tz="UTC"),
        }
    ]
)

cost_model = CostModel(spread_total=1.00, commission_total=0.10)
sizing_config = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01, max_risk_pct=None)
swap_config = SwapConfig(
    long_rate_per_night=-0.05,
    short_rate_per_night=0.02,
    rollover_hour=17,
    rollover_tz="America/New_York",
    triple_weekday=2,
    zero_weight_weekdays=(5, 6),
)

resultado = run_backtest(
    signals, bars, cost_model, sizing_config, swap_config=swap_config, initial_equity=10_000.0
)

print("SALIDA REAL DEL MOTOR:")
t = resultado.trades[0]
print(f"  entry_time    = {t.entry_time}")
print(f"  entry_price   = {t.entry_price}")
print(f"  exit_time     = {t.exit_time}")
print(f"  exit_price    = {t.exit_price}")
print(f"  exit_reason   = {t.exit_reason}")
print(f"  stop_distance = {t.stop_distance}")
print(f"  position_size = {t.position_size}")
print(f"  pnl_gross     = {t.pnl_gross}")
print(f"  commission    = {t.commission_cost}")
print(f"  swap_total    = {t.swap_total}")
print(f"  pnl_net       = {t.pnl_net}")
print(f"  pnl_r         = {t.pnl_r}")
print()

prueba("1 sola operacion, no saltada", len(resultado.trades) == 1 and not t.was_skipped)
prueba("entry_price == 100.50", abs(t.entry_price - 100.50) < 1e-9, f"real={t.entry_price}")
prueba("exit_reason == 'time'", t.exit_reason == "time", f"real={t.exit_reason}")
prueba("exit_price == 103.50", abs(t.exit_price - 103.50) < 1e-9, f"real={t.exit_price}")
prueba("stop_distance == 10.00", abs(t.stop_distance - 10.00) < 1e-9, f"real={t.stop_distance}")
prueba("position_size == 10.00", abs(t.position_size - 10.00) < 1e-9, f"real={t.position_size}")
prueba("pnl_gross == 30.00", abs(t.pnl_gross - 30.00) < 1e-9, f"real={t.pnl_gross}")
prueba("commission_cost == 1.00", abs(t.commission_cost - 1.00) < 1e-9, f"real={t.commission_cost}")
prueba("swap_total == -2.00 (4 noches ponderadas: miercoles x3 + jueves x1)",
       abs(t.swap_total - (-2.00)) < 1e-9, f"real={t.swap_total}")
prueba("pnl_net == 27.00", abs(t.pnl_net - 27.00) < 1e-9, f"real={t.pnl_net}")
prueba("pnl_r == 0.27", abs(t.pnl_r - 0.27) < 1e-9, f"real={t.pnl_r}")

print()
print("=" * 78)
print("PRUEBA 2 -- INYECCION DEL STOP (un stop nunca ejecuta a mejor precio del disparado)")
print("=" * 78)


def escanea_una_vela(direction, stop_price, target_price, o, h, l, c, half_spread=0.0):
    """Monta UNA vela y llama directamente a _find_exit para aislar la logica de fill."""
    idx = pd.to_datetime(["2024-02-01 00:00:00", "2024-02-01 01:00:00"], utc=True)
    open_arr = [o, o]
    high_arr = [h, h]
    low_arr = [l, l]
    close_arr = [c, c]
    import numpy as np
    idx_ns = idx.as_unit("ns").asi8
    fill, ts, motivo = _find_exit(
        np.array(open_arr), np.array(high_arr), np.array(low_arr), np.array(close_arr),
        idx, idx_ns, 1, direction, stop_price, target_price, None, half_spread,
    )
    return fill, motivo


def fill_ingenuo_que_ignora_el_gap(direction, stop_price):
    """Lo que produciria una implementacion INCORRECTA que siempre rellena
    exactamente al precio de stop, ignorando si la vela abrio ya mas alla
    (el bug de look-ahead / mejora de precio que la prueba debe descartar)."""
    return stop_price


print()
print("Caso A -- LARGO, cruce ORDINARIO intra-vela (la vela abre por encima del stop):")
print("  stop=100.00, vela: open=101.00 high=101.50 low=98.00 close=99.00 (spread=0)")
fill_a, motivo_a = escanea_una_vela(1, 100.00, None, 101.00, 101.50, 98.00, 99.00, half_spread=0.0)
print(f"  -> fill={fill_a}, motivo={motivo_a}")
prueba("Caso A: fill == stop_price exacto (cruce normal, sin gap)", abs(fill_a - 100.00) < 1e-9, f"real={fill_a}")
prueba("Caso A: fill NO es mejor que el stop (<=100.00 para un largo que vende)", fill_a <= 100.00)

print()
print("Caso B -- LARGO, GAP en contra (la vela abre YA por debajo del stop):")
print("  stop=100.00, vela: open=95.00 high=96.00 low=90.00 close=91.00 (spread=0)")
fill_b, motivo_b = escanea_una_vela(1, 100.00, None, 95.00, 96.00, 90.00, 91.00, half_spread=0.0)
fill_ingenuo_b = fill_ingenuo_que_ignora_el_gap(1, 100.00)
print(f"  -> fill REAL del motor = {fill_b}, motivo={motivo_b}")
print(f"  -> fill de una implementacion INGENUA que ignorase el gap = {fill_ingenuo_b} (PROHIBIDO)")
prueba("Caso B: el motor rellena AL OPEN gapeado (95.00), no al stop", abs(fill_b - 95.00) < 1e-9, f"real={fill_b}")
prueba("Caso B: fill NO es mejor que el stop (95.00 <= 100.00)", fill_b <= 100.00)
prueba(
    "Caso B: el motor NO produce el fill ingenuo (prohibido) que ignora el gap",
    abs(fill_b - fill_ingenuo_b) > 1e-9,
    f"motor={fill_b} vs ingenuo(prohibido)={fill_ingenuo_b}",
)

print()
print("Caso C -- CORTO, cruce ORDINARIO intra-vela (la vela abre por debajo del stop):")
print("  stop=100.00, vela: open=99.00 high=103.00 low=98.50 close=102.00 (spread=0)")
fill_c, motivo_c = escanea_una_vela(-1, 100.00, None, 99.00, 103.00, 98.50, 102.00, half_spread=0.0)
print(f"  -> fill={fill_c}, motivo={motivo_c}")
prueba("Caso C: fill == stop_price exacto (cruce normal, sin gap)", abs(fill_c - 100.00) < 1e-9, f"real={fill_c}")
prueba("Caso C: fill NO es mejor que el stop (>=100.00 para un corto que compra)", fill_c >= 100.00)

print()
print("Caso D -- CORTO, GAP en contra (la vela abre YA por encima del stop):")
print("  stop=100.00, vela: open=105.00 high=110.00 low=104.00 close=108.00 (spread=0)")
fill_d, motivo_d = escanea_una_vela(-1, 100.00, None, 105.00, 110.00, 104.00, 108.00, half_spread=0.0)
fill_ingenuo_d = fill_ingenuo_que_ignora_el_gap(-1, 100.00)
print(f"  -> fill REAL del motor = {fill_d}, motivo={motivo_d}")
print(f"  -> fill de una implementacion INGENUA que ignorase el gap = {fill_ingenuo_d} (PROHIBIDO)")
prueba("Caso D: el motor rellena AL OPEN gapeado (105.00), no al stop", abs(fill_d - 105.00) < 1e-9, f"real={fill_d}")
prueba("Caso D: fill NO es mejor que el stop (105.00 >= 100.00)", fill_d >= 100.00)
prueba(
    "Caso D: el motor NO produce el fill ingenuo (prohibido) que ignora el gap",
    abs(fill_d - fill_ingenuo_d) > 1e-9,
    f"motor={fill_d} vs ingenuo(prohibido)={fill_ingenuo_d}",
)

print()
print("Bateria aleatoria -- 2000 gaps al azar, largo y corto, CON spread no nulo:")
print("(invariante ESTRICTO: fill <= stop-half_spread en largo, fill >= stop+half_spread")
print(" en corto -- el invariante laxo 'fill <= stop' NO habria pillado el sesgo del")
print(" 03/08/2026, porque el fill roto (stop_price a secas) tambien lo cumplia)")
import random

random.seed(20260803)
n_bateria = 2000
peor_nunca_mejor_largo = True
peor_nunca_mejor_corto = True
for _ in range(n_bateria):
    stop = random.uniform(50.0, 150.0)
    half_spread = random.uniform(0.01, 2.0)  # NUNCA cero: si no, el invariante estricto colapsa al laxo
    gap = random.uniform(-20.0, 20.0)  # negativo = gap en contra para el largo
    o = stop + gap
    h = o + random.uniform(0, 5)
    l = o - random.uniform(0, 5)
    c = (h + l) / 2

    # LARGO: forzamos que dispare (low - half_spread <= stop) ajustando low si hace falta
    l_largo = min(l, stop + half_spread - 0.01)
    fill_l, _ = escanea_una_vela(1, stop, None, o, h, l_largo, c, half_spread=half_spread)
    if fill_l > (stop - half_spread) + 1e-9:
        peor_nunca_mejor_largo = False

    # CORTO: forzamos que dispare (high + half_spread >= stop) ajustando high si hace falta
    h_corto = max(h, stop - half_spread + 0.01)
    fill_s, _ = escanea_una_vela(-1, stop, None, o, h_corto, l, c, half_spread=half_spread)
    if fill_s < (stop + half_spread) - 1e-9:
        peor_nunca_mejor_corto = False

prueba(
    f"En {n_bateria} escenarios largos con gap/spread al azar, ningun fill mejora stop-half_spread",
    peor_nunca_mejor_largo,
)
prueba(
    f"En {n_bateria} escenarios cortos con gap/spread al azar, ningun fill mejora stop+half_spread",
    peor_nunca_mejor_corto,
)

print()
print("=" * 78)
print("PRUEBA 3 -- SIMETRIA DEL COSTE RESTAURADA (rechazo de critico-codigo, 03/08/2026)")
print("=" * 78)
print("""
Defecto reproducido y reparado: el fill de STOP (caso ordinario, sin gap) y el
de TARGET devolvian el precio "a secas", sin restar/sumar half_spread, mientras
que TIEMPO/EOD si lo hacian. Efecto: una operacion que sale por stop u objetivo
(la salida NORMAL) pagaba solo MEDIO coste de ida y vuelta -- sesgo A FAVOR de
la estrategia. Casos a mano, SIN comision ni swap para aislar solo el spread.
""")

cost_model_3 = CostModel(spread_total=1.00, commission_total=0.0)

print("Caso STOP (largo, cruce ORDINARIO -- open=96.00 > stop=95.00, sin gap):")
print("""
  CALCULO A MANO:
    entry_price = open(entrada=100.00) + half_spread(0.50)        = 100.50
    stop_distance = |100.50 - 95.00|                              = 5.50
    riesgo_$ = equity(5500.00) * risk_pct(0.01)                    = 55.00
    tamano = 55.00 / 5.50                                          = 10.00 (exacto)
    exit_price CORREGIDO = min(stop=95.00, open=96.00) - 0.50      = 94.50
    pnl_gross CORREGIDO  = (94.50-100.50)*10.00                    = -60.00
    coste de spread embebido = 0.50(entrada)+0.50(salida) por unidad, x10 = 10.00
                             = spread_total(1.00) * tamano(10.00)  -- CUADRA

    (para memoria, el valor ANTES de reparar habria sido:
     exit_price ROTO = stop_price a secas                          = 95.00
     pnl_gross ROTO  = (95.00-100.50)*10.00                        = -55.00
     coste de spread embebido ROTO = solo 5.00 (la mitad) -- ESTE ERA EL SESGO)
""")

bars_stop = pd.DataFrame(
    [
        bar(100.00, 100.00, 100.00, 100.00),
        bar(100.00, 101.00, 99.50, 100.50),   # entrada
        bar(96.00, 96.50, 94.00, 94.50),      # salida por stop, SIN gap (open=96 > stop=95)
    ],
    index=pd.to_datetime(
        ["2024-02-05 22:00:00", "2024-02-06 22:00:00", "2024-02-07 22:00:00"], utc=True
    ),
)
signals_stop = pd.DataFrame([{
    "timestamp": bars_stop.index[0], "direction": 1, "stop_price": 95.00,
    "target_price": float("nan"), "exit_time": pd.NaT,
}])
sizing_3 = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
r_stop = run_backtest(signals_stop, bars_stop, cost_model_3, sizing_3, initial_equity=5500.00)
t_stop = r_stop.trades[0]
print(f"  SALIDA REAL: entry_price={t_stop.entry_price} exit_price={t_stop.exit_price} "
      f"exit_reason={t_stop.exit_reason} pnl_gross={t_stop.pnl_gross}")
prueba("STOP: entry_price == 100.50", abs(t_stop.entry_price - 100.50) < 1e-9, f"real={t_stop.entry_price}")
prueba("STOP: exit_reason == 'stop' (ordinario, sin gap)", t_stop.exit_reason == "stop", f"real={t_stop.exit_reason}")
prueba("STOP: exit_price == 94.50 (CORREGIDO, ya no 95.00)", abs(t_stop.exit_price - 94.50) < 1e-9, f"real={t_stop.exit_price}")
prueba("STOP: pnl_gross == -60.00 (CORREGIDO, ya no -55.00)", abs(t_stop.pnl_gross - (-60.00)) < 1e-9, f"real={t_stop.pnl_gross}")

print()
print("Caso TARGET (corto, cruce ORDINARIO -- open=91.00 > target=90.00, sin gap):")
print("""
  CALCULO A MANO:
    entry_price = open(entrada=100.00) - half_spread(0.50)         = 99.50
    stop_distance = |99.50 - 110.00|                                = 10.50
    riesgo_$ = equity(5250.00) * risk_pct(0.01)                     = 52.50
    tamano = 52.50 / 10.50                                          = 5.00 (exacto)
    exit_price CORREGIDO = target(90.00) + half_spread(0.50)        = 90.50
    pnl_gross CORREGIDO  = -1*(90.50-99.50)*5.00                    = 45.00
    coste de spread embebido = 0.50(entrada)+0.50(salida) por unidad, x5 = 5.00
                             = spread_total(1.00) * tamano(5.00)   -- CUADRA

    (para memoria, el valor ANTES de reparar habria sido:
     exit_price ROTO = target_price a secas                         = 90.00
     pnl_gross ROTO  = -1*(90.00-99.50)*5.00                        = 47.50
     coste de spread embebido ROTO = solo 2.50 (la mitad) -- ESTE ERA EL SESGO)
""")

bars_target = pd.DataFrame(
    [
        bar(100.00, 100.00, 100.00, 100.00),
        bar(100.00, 101.00, 99.50, 100.50),   # entrada
        bar(91.00, 92.00, 89.00, 89.50),      # salida por target, SIN gap (open=91 > target=90)
    ],
    index=pd.to_datetime(
        ["2024-02-05 22:00:00", "2024-02-06 22:00:00", "2024-02-07 22:00:00"], utc=True
    ),
)
signals_target = pd.DataFrame([{
    "timestamp": bars_target.index[0], "direction": -1, "stop_price": 110.00,
    "target_price": 90.00, "exit_time": pd.NaT,
}])
sizing_3b = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
r_target = run_backtest(signals_target, bars_target, cost_model_3, sizing_3b, initial_equity=5250.00)
t_target = r_target.trades[0]
print(f"  SALIDA REAL: entry_price={t_target.entry_price} exit_price={t_target.exit_price} "
      f"exit_reason={t_target.exit_reason} pnl_gross={t_target.pnl_gross}")
prueba("TARGET: entry_price == 99.50", abs(t_target.entry_price - 99.50) < 1e-9, f"real={t_target.entry_price}")
prueba("TARGET: exit_reason == 'target' (ordinario, sin gap)", t_target.exit_reason == "target", f"real={t_target.exit_reason}")
prueba("TARGET: exit_price == 90.50 (CORREGIDO, ya no 90.00)", abs(t_target.exit_price - 90.50) < 1e-9, f"real={t_target.exit_price}")
prueba("TARGET: pnl_gross == 45.00 (CORREGIDO, ya no 47.50)", abs(t_target.pnl_gross - 45.00) < 1e-9, f"real={t_target.pnl_gross}")

print()
if FALLOS:
    print(f"RESULTADO: {len(FALLOS)} PRUEBA(S) FALLIDA(S): {FALLOS}")
    sys.exit(1)
else:
    print("RESULTADO: TODAS LAS PRUEBAS PASAN")
    sys.exit(0)
