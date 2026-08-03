#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas de sizing.py (tarea 01.02.02, pieza T2). Ejecutar:
    .venv/bin/python 03-motor/backtester/tests/test_sizing.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backtester.sizing import SizingConfig, calculate_position_size, implied_risk_pct


def test_tamano_exacto_sin_redondeo():
    cfg = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
    size, skipped = calculate_position_size(equity=10_000.0, stop_distance=10.0, config=cfg)
    assert not skipped
    assert abs(size - 10.0) < 1e-12, size


def test_tamano_se_redondea_hacia_abajo():
    cfg = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
    # riesgo=100.00, stop=8.0 -> bruto=12.5 -> floor a step 0.01 = 12.50 exacto
    size, skipped = calculate_position_size(equity=10_000.0, stop_distance=8.0, config=cfg)
    assert not skipped
    assert abs(size - 12.5) < 1e-12, size

    # Ahora con un stop que fuerza un resto no exacto: riesgo=100.00, stop=8.03
    # -> bruto=12.4533... -> floor a step 0.01 = 12.45
    size2, skipped2 = calculate_position_size(equity=10_000.0, stop_distance=8.03, config=cfg)
    assert not skipped2
    assert abs(size2 - 12.45) < 1e-9, size2


def test_minimo_siempre_se_toma_sin_max_risk_pct():
    """Sin max_risk_pct declarado (None, valor por defecto), el tamano minimo
    se toma SIEMPRE, por pequeno que sea el resultado bruto."""
    cfg = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=0.0001)
    # riesgo = 10000*0.0001 = 1.0; stop_distance=1000 -> bruto=0.001, muy por debajo del minimo
    size, skipped = calculate_position_size(equity=10_000.0, stop_distance=1000.0, config=cfg)
    assert not skipped
    assert size == 1.0, size


def test_salta_por_stop_distance_no_positivo():
    cfg = SizingConfig(min_size=0.01, size_step=0.01)
    size, skipped = calculate_position_size(equity=10_000.0, stop_distance=0.0, config=cfg)
    assert skipped and size == 0.0
    size2, skipped2 = calculate_position_size(equity=10_000.0, stop_distance=-5.0, config=cfg)
    assert skipped2 and size2 == 0.0


def test_salta_por_equity_no_positivo():
    cfg = SizingConfig(min_size=0.01, size_step=0.01)
    size, skipped = calculate_position_size(equity=0.0, stop_distance=10.0, config=cfg)
    assert skipped and size == 0.0
    size2, skipped2 = calculate_position_size(equity=-100.0, stop_distance=10.0, config=cfg)
    assert skipped2 and size2 == 0.0


def test_salta_por_max_risk_pct_cuando_esta_declarado():
    # tamano minimo = 1.0, stop_distance=50 -> riesgo implicito del minimo = 50/1000=5%
    # max_risk_pct=0.025 (2.5%) -> se supera -> salta
    cfg = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=0.01, max_risk_pct=0.025)
    size, skipped = calculate_position_size(equity=1000.0, stop_distance=50.0, config=cfg)
    assert skipped and size == 0.0


def test_no_salta_por_max_risk_pct_si_no_se_supera():
    cfg = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01, max_risk_pct=0.025)
    size, skipped = calculate_position_size(equity=10_000.0, stop_distance=10.0, config=cfg)
    assert not skipped
    assert abs(size - 10.0) < 1e-12


def test_sin_max_risk_pct_nunca_salta_por_riesgo_del_minimo():
    """Diferencia deliberada frente a gb2: aqui max_risk_pct es OPCIONAL y por
    defecto None -- si no se declara, NUNCA se salta por este motivo, aunque
    el riesgo implicito del minimo sea enorme."""
    cfg = SizingConfig(min_size=100.0, size_step=1.0, risk_pct=0.01, max_risk_pct=None)
    size, skipped = calculate_position_size(equity=100.0, stop_distance=1000.0, config=cfg)
    assert not skipped
    assert size == 100.0  # el minimo, aunque su riesgo implicito sea 1000x el capital


def test_precision_flotante_no_pierde_un_paso_exacto():
    """Regresion: sin el epsilon de sizing.py, un tamano que matematicamente
    es un multiplo EXACTO de size_step pierde un paso entero por como el
    hardware representa los decimales (0.29/0.01 se representa como
    27.999999999999996 y math.floor() lo trunca a 28, no 29). Encontrado por
    ejecucion (200000 casos aleatorios NO lo mostraron; 599997 casos
    construidos para ser multiplos exactos si, en 24283 de ellos)."""
    cfg = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=1.0)
    size, skipped = calculate_position_size(equity=0.29, stop_distance=1.0, config=cfg)
    assert not skipped
    assert abs(size - 0.29) < 1e-12, size

    # Bateria de multiplos exactos conocidos por ser problematicos en coma
    # flotante (comprobados directamente, sin pasar por equity/stop_distance).
    import math
    for step in (0.01, 0.001, 0.1):
        for k in (29, 58, 59, 116, 205, 401):
            raw = k * step
            cfg2 = SizingConfig(min_size=step, size_step=step, risk_pct=1.0)
            size2, _ = calculate_position_size(equity=raw, stop_distance=1.0, config=cfg2)
            esperado = k * step
            assert abs(size2 - esperado) < 1e-9, f"step={step} k={k}: size={size2} esperado={esperado}"


def test_sizingconfig_valida_parametros():
    for kwargs, motivo in [
        (dict(min_size=0.0, size_step=0.01), "min_size debe ser positivo"),
        (dict(min_size=0.01, size_step=0.0), "size_step debe ser positivo"),
        (dict(min_size=0.01, size_step=0.01, risk_pct=0.0), "risk_pct debe ser positivo"),
        (dict(min_size=0.01, size_step=0.01, max_risk_pct=0.0), "max_risk_pct debe ser positivo"),
    ]:
        try:
            SizingConfig(**kwargs)
            assert False, f"debia lanzar ValueError ({motivo})"
        except ValueError:
            pass


def test_implied_risk_pct():
    assert abs(implied_risk_pct(10_000.0, 10.0, 10.0) - 0.01) < 1e-12
    assert implied_risk_pct(0.0, 10.0, 10.0) == float("inf")
    assert implied_risk_pct(-5.0, 10.0, 10.0) == float("inf")


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
    print(f"\ntest_sizing.py: {ok} pasadas, {fail} fallidas de {len(tests)}")
    return fail == 0


if __name__ == "__main__":
    ok = _run_all()
    sys.exit(0 if ok else 1)
