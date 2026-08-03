#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas de costs.py (tarea 01.02.02, pieza T2). Sin pytest (no esta instalado
en .venv, comprobado por ejecucion): funciones `test_*` con `assert`, mismo
estilo que 03-motor/scripts/verificar_barreras.py. Ejecutar:
    .venv/bin/python 03-motor/backtester/tests/test_costs.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pandas as pd

from backtester.costs import CostModel, SwapConfig, swap_cost


def test_cost_model_half_spread():
    cm = CostModel(spread_total=1.20, commission_total=0.05)
    assert abs(cm.half_spread - 0.60) < 1e-12
    assert abs(cm.total_explicit_rt - 1.25) < 1e-12


def test_cost_model_rechaza_spread_negativo():
    try:
        CostModel(spread_total=-0.1)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_cost_model_rechaza_comision_negativa():
    try:
        CostModel(spread_total=0.1, commission_total=-0.01)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_swap_intradia_es_cero():
    cfg = SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=0.5)
    t0 = pd.Timestamp("2024-01-09 10:00:00", tz="UTC")
    t1 = pd.Timestamp("2024-01-09 12:00:00", tz="UTC")  # mismo dia, sin rollover de por medio
    assert swap_cost(1, t0, t1, 5.0, cfg) == 0.0
    assert swap_cost(-1, t0, t1, 5.0, cfg) == 0.0


def test_swap_una_noche_ordinaria_largo_paga():
    # Lunes a martes, saliendo ANTES del rollover del martes: cruza solo el
    # rollover del lunes (22:00 UTC = 17:00 NY en enero) -> 1 noche, peso 1.
    cfg = SwapConfig(long_rate_per_night=-0.10, short_rate_per_night=0.03)
    entrada = pd.Timestamp("2024-01-08 20:00:00", tz="UTC")  # lunes, antes de su rollover
    salida = pd.Timestamp("2024-01-09 20:00:00", tz="UTC")   # martes, antes de SU rollover
    resultado = swap_cost(1, entrada, salida, 2.0, cfg)
    esperado = 1 * (-0.10) * 2.0  # 1 noche (lunes, peso 1) x tarifa x tamano
    assert abs(resultado - esperado) < 1e-12, f"{resultado} != {esperado}"


def test_swap_corto_cobra_signo_contrario():
    cfg = SwapConfig(long_rate_per_night=-0.10, short_rate_per_night=0.03)
    entrada = pd.Timestamp("2024-01-08 20:00:00", tz="UTC")
    salida = pd.Timestamp("2024-01-09 20:00:00", tz="UTC")
    resultado = swap_cost(-1, entrada, salida, 2.0, cfg)
    esperado = 1 * 0.03 * 2.0
    assert abs(resultado - esperado) < 1e-12, f"{resultado} != {esperado}"


def test_swap_miercoles_pesa_triple():
    """Los EXTREMOS nunca cuentan (test_swap_extremos_no_cuentan): para aislar
    UN solo rollover hay que entrar ANTES de el y salir DESPUES de el pero
    ANTES del siguiente."""
    cfg = SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0, triple_weekday=2)
    # martes 20:00 UTC -> miercoles 20:00 UTC: cruza SOLO el rollover del martes (peso 1).
    entrada = pd.Timestamp("2024-01-09 20:00:00", tz="UTC")
    salida = pd.Timestamp("2024-01-10 20:00:00", tz="UTC")
    assert abs(swap_cost(1, entrada, salida, 1.0, cfg) - (-1.0)) < 1e-12
    # miercoles 20:00 UTC -> jueves 20:00 UTC: cruza SOLO el rollover del miercoles (peso 3).
    entrada2 = pd.Timestamp("2024-01-10 20:00:00", tz="UTC")
    salida2 = pd.Timestamp("2024-01-11 20:00:00", tz="UTC")
    assert abs(swap_cost(1, entrada2, salida2, 1.0, cfg) - (-3.0)) < 1e-12


def test_swap_fin_de_semana_no_anade_noches():
    # Viernes 20:00 UTC (antes de su rollover) -> lunes 20:00 UTC (antes del
    # suyo): cruza rollover de viernes (peso 1), sabado (peso 0) y domingo
    # (peso 0) = 1 noche neta, no 3.
    cfg = SwapConfig(long_rate_per_night=-2.0, short_rate_per_night=2.0)
    entrada = pd.Timestamp("2024-01-12 20:00:00", tz="UTC")  # viernes
    salida = pd.Timestamp("2024-01-15 20:00:00", tz="UTC")   # lunes siguiente
    resultado = swap_cost(1, entrada, salida, 1.0, cfg)
    assert abs(resultado - (-2.0)) < 1e-12, f"{resultado} (esperado 1 noche x -2.0)"


def test_swap_extremos_no_cuentan():
    """Entrar o salir EXACTAMENTE en el instante del rollover no lo cuenta
    (regla ESTRICTA: ni entry_time ni exit_time cuentan como rollover)."""
    cfg = SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0)
    entrada = pd.Timestamp("2024-01-09 22:00:00", tz="UTC")  # exactamente un rollover (martes)
    salida = pd.Timestamp("2024-01-09 22:00:01", tz="UTC")   # 1 segundo despues, mismo rollover
    # Al entrar justo en el rollover, ese instante no cuenta como "cruzado" para
    # ESTA posicion (se entro en el, no se sostuvo a traves de el).
    resultado = swap_cost(1, entrada, salida, 1.0, cfg)
    assert resultado == 0.0, f"{resultado} (no deberia cruzar ningun rollover)"


def test_swap_direccion_invalida_lanza():
    cfg = SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0)
    try:
        swap_cost(0, pd.Timestamp.now(tz="UTC"), pd.Timestamp.now(tz="UTC") + pd.Timedelta(days=1), 1.0, cfg)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_swap_naive_se_asume_utc():
    cfg = SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0)
    entrada = pd.Timestamp("2024-01-08 20:00:00")  # sin tz
    salida = pd.Timestamp("2024-01-09 20:00:00")   # sin tz, antes del rollover del martes
    resultado = swap_cost(1, entrada, salida, 1.0, cfg)
    assert abs(resultado - (-1.0)) < 1e-12


def test_swapconfig_rechaza_hora_fuera_de_rango():
    try:
        SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0, rollover_hour=24)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_swapconfig_rechaza_triple_weekday_fuera_de_rango():
    try:
        SwapConfig(long_rate_per_night=-1.0, short_rate_per_night=1.0, triple_weekday=7)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def _run_all():
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    ok, fail = 0, 0
    for t in tests:
        try:
            t()
            print(f"  [PASA] {t.__name__}")
            ok += 1
        except AssertionError as e:
            print(f"  [FALLA] {t.__name__} -- {e}")
            fail += 1
    print(f"\ntest_costs.py: {ok} pasadas, {fail} fallidas de {len(tests)}")
    return fail == 0


if __name__ == "__main__":
    ok = _run_all()
    sys.exit(0 if ok else 1)
