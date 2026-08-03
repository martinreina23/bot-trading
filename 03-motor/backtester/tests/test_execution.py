#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas de execution.py (tarea 01.02.02, pieza T2). Ejecutar:
    .venv/bin/python 03-motor/backtester/tests/test_execution.py

Cubre ramas que el caso a mano de verificar_motor.py NO toca: salida por
target, salida por fin de datos (eod), señal saltada por dimensionado,
varias operaciones seguidas actualizando el equity, señal sin vela posterior
(no genera operación), swap_config=None, y las validaciones de entrada.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pandas as pd

from backtester.costs import CostModel, SwapConfig
from backtester.sizing import SizingConfig
from backtester.execution import run_backtest


def _bars(rows, start="2024-01-08 22:00:00", freq="D"):
    idx = pd.date_range(start=start, periods=len(rows), freq=freq, tz="UTC")
    return pd.DataFrame(rows, index=idx, columns=["open", "high", "low", "close"])


def test_entrada_larga_y_corta_embeben_el_spread():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],   # señal
        [100.0, 105.0, 95.0, 100.0],    # entrada
        [100.0, 200.0, 0.0, 100.0],     # sale seguro (target/stop lejanos, o EOD)
    ])
    cm = CostModel(spread_total=2.0, commission_total=0.0)  # half_spread=1.0
    sizing = SizingConfig(min_size=1.0, size_step=1.0)

    sig_largo = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 1.0, "target_price": 199.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig_largo, bars, cm, sizing, initial_equity=100_000.0)
    assert abs(r.trades[0].entry_price - 101.0) < 1e-9, r.trades[0].entry_price  # 100 + half_spread

    sig_corto = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": -1,
        "stop_price": 199.0, "target_price": 1.0, "exit_time": pd.NaT,
    }])
    r2 = run_backtest(sig_corto, bars, cm, sizing, initial_equity=100_000.0)
    assert abs(r2.trades[0].entry_price - 99.0) < 1e-9, r2.trades[0].entry_price  # 100 - half_spread


def test_salida_por_target_fill_exacto():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],   # señal
        [100.0, 102.0, 98.0, 101.0],    # entrada, open=100
        [101.0, 115.0, 100.0, 110.0],   # el target (110) se alcanza aqui
        [110.0, 120.0, 105.0, 118.0],   # no deberia llegar aqui
    ])
    cm = CostModel(spread_total=0.0)  # sin spread, para verificar el precio EXACTO del target
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 50.0, "target_price": 110.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=10_000.0)
    t = r.trades[0]
    assert t.exit_reason == "target", t.exit_reason
    assert abs(t.exit_price - 110.0) < 1e-9, t.exit_price
    assert t.exit_time == bars.index[2]


def test_salida_por_fin_de_datos_eod():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
        [100.0, 101.0, 99.0, 100.5],   # ultima vela: ni stop ni target se disparan
    ])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 1.0, "target_price": 999.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=10_000.0)
    t = r.trades[0]
    assert t.exit_reason == "eod", t.exit_reason
    assert abs(t.exit_price - 100.5) < 1e-9, t.exit_price  # close de la ultima vela
    assert t.exit_time == bars.index[-1]


def test_stop_antes_que_target_en_la_misma_vela():
    """Si stop y target podrian dispararse los dos en la misma vela, el motor
    comprueba el stop PRIMERO (convencion pesimista deliberada, ver
    execution.py, seccion 'Orden en la MISMA vela')."""
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 110.0, 90.0, 100.0],   # entrada
        [100.0, 120.0, 80.0, 100.0],   # esta vela toca tanto el stop (85) como el target (115)
    ])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 85.0, "target_price": 115.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=10_000.0)
    assert r.trades[0].exit_reason == "stop", r.trades[0].exit_reason


def test_stop_ordinario_aplica_half_spread_simetrico():
    """Regresion del rechazo de critico-codigo (03/08/2026): el fill de un
    stop ORDINARIO (sin gap) tiene que pagar el half_spread de salida, igual
    que time/eod. Antes de la reparacion este exit_price salia en 95.0 (el
    stop_price a secas); el correcto es 95.0 - half_spread."""
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],   # entrada, open=100
        [96.0, 96.5, 94.0, 94.5],      # stop ORDINARIO: open=96 > stop=95, sin gap
    ])
    cm = CostModel(spread_total=1.0)  # half_spread=0.5
    sizing = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 95.0, "target_price": float("nan"), "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=5_500.0)
    t = r.trades[0]
    assert t.exit_reason == "stop", t.exit_reason
    assert abs(t.exit_price - 94.5) < 1e-9, t.exit_price  # 95.0 - 0.5, NO 95.0


def test_target_ordinario_aplica_half_spread_simetrico():
    """Mismo defecto, rama TARGET: antes de la reparacion salia en 90.0 (el
    target_price a secas); el correcto es 90.0 + half_spread (corto)."""
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],   # entrada, open=100
        [91.0, 92.0, 89.0, 89.5],      # target ORDINARIO: open=91 > target=90, sin gap
    ])
    cm = CostModel(spread_total=1.0)  # half_spread=0.5
    sizing = SizingConfig(min_size=0.01, size_step=0.01, risk_pct=0.01)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": -1,
        "stop_price": 110.0, "target_price": 90.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=5_250.0)
    t = r.trades[0]
    assert t.exit_reason == "target", t.exit_reason
    assert abs(t.exit_price - 90.5) < 1e-9, t.exit_price  # 90.0 + 0.5, NO 90.0


def test_coste_de_spread_identico_salga_por_donde_salga():
    """La prueba de fondo del rechazo: el coste de spread embebido (medido
    como spread_total * position_size) debe ser IDENTICO para una operacion
    que sale por TIEMPO y para una que sale por STOP ordinario, dado el
    MISMO movimiento de precio de referencia. Antes de la reparacion, la
    salida por stop salia con la mitad del coste."""
    cm = CostModel(spread_total=1.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=1.0)

    # Sale por TIEMPO, exit al MISMO nivel de referencia (95.0) que el stop de
    # abajo, y con el MISMO stop_price (95.0) para que el tamaño de posicion
    # (que depende de stop_distance) salga IDENTICO en los dos casos. El
    # tiempo se comprueba ANTES que el stop en la misma vela (ver docstring
    # de _find_exit), asi que aunque el low de esta vela tambien toque 95.0,
    # la salida real es por tiempo, no por stop.
    bars_tiempo = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],
        [96.0, 96.5, 94.0, 95.0],  # close=95.0
    ])
    sig_tiempo = pd.DataFrame([{
        "timestamp": bars_tiempo.index[0], "direction": 1, "stop_price": 95.0,
        "target_price": float("nan"), "exit_time": bars_tiempo.index[-1],
    }])
    r_tiempo = run_backtest(sig_tiempo, bars_tiempo, cm, sizing, initial_equity=100.0)
    t_tiempo = r_tiempo.trades[0]

    # Sale por STOP ordinario al mismo nivel de referencia (95.0).
    bars_stop = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],
        [96.0, 96.5, 94.0, 94.5],
    ])
    sig_stop = pd.DataFrame([{
        "timestamp": bars_stop.index[0], "direction": 1, "stop_price": 95.0,
        "target_price": float("nan"), "exit_time": pd.NaT,
    }])
    r_stop = run_backtest(sig_stop, bars_stop, cm, sizing, initial_equity=100.0)
    t_stop = r_stop.trades[0]

    # Mismo entry_price, mismo stop_price (95.0) -> mismo tamaño de posicion
    # en los dos casos (18.0, ver comentario de sizing arriba). Mismo
    # movimiento de referencia (100 -> 95) en ambos: el pnl_gross de los dos
    # debe coincidir dígito a dígito.
    assert abs(t_tiempo.position_size - t_stop.position_size) < 1e-9, (
        f"tamaños distintos: tiempo={t_tiempo.position_size} stop={t_stop.position_size}"
    )
    assert abs(t_tiempo.pnl_gross - t_stop.pnl_gross) < 1e-9, (
        f"tiempo={t_tiempo.pnl_gross} stop={t_stop.pnl_gross} -- deberian ser IGUALES"
    )
    # entry=100.5, exit=94.5 (95.0-half_spread) en los dos, tamaño=18.0:
    # (94.5-100.5)*18.0 = -108.0
    assert abs(t_tiempo.pnl_gross - (-108.0)) < 1e-9, t_tiempo.pnl_gross


def test_gap_contra_stop_largo_via_run_backtest():
    """El hueco que 'critico-codigo' señaló como NO cubierto por esta
    bateria: un GAP en contra del stop, en LARGO, pasando por el run_backtest
    COMPLETO (no solo por _find_exit aislado). Si se desactivase la
    proteccion de hueco (min(stop, open)), este test debe caer -- demostrado
    por ejecucion en la entrega, no solo declarado."""
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],   # entrada, open=100
        [90.0, 91.0, 89.0, 89.5],      # GAP: open=90 YA por debajo del stop=95
    ])
    cm = CostModel(spread_total=1.0)  # half_spread=0.5
    sizing = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 95.0, "target_price": float("nan"), "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=1_000.0)
    t = r.trades[0]
    assert t.exit_reason == "stop", t.exit_reason
    # Fill correcto: min(95.0, 90.0) - 0.5 = 89.5. Sin la proteccion de hueco
    # (naive fill = stop_price - half_spread = 94.5) este assert cae.
    assert abs(t.exit_price - 89.5) < 1e-9, t.exit_price


def test_gap_contra_stop_corto_via_run_backtest():
    """Espejo del anterior, en CORTO: GAP hacia arriba, en contra del stop."""
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.5, 100.5],
        [110.0, 112.0, 109.0, 111.0],   # GAP: open=110 YA por encima del stop=105
    ])
    cm = CostModel(spread_total=1.0)  # half_spread=0.5
    sizing = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": -1,
        "stop_price": 105.0, "target_price": float("nan"), "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=1_000.0)
    t = r.trades[0]
    assert t.exit_reason == "stop", t.exit_reason
    # Fill correcto: max(105.0, 110.0) + 0.5 = 110.5. Sin la proteccion de
    # hueco (naive fill = stop_price + half_spread = 105.5) este assert cae.
    assert abs(t.exit_price - 110.5) < 1e-9, t.exit_price


def test_senal_saltada_por_dimensionado_se_registra():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
    ])
    cm = CostModel(spread_total=0.0)
    # max_risk_pct muy bajo: el minimo (1.0) con stop_distance grande supera el techo -> salta
    sizing = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=0.01, max_risk_pct=0.001)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 1.0, "target_price": 999.0, "exit_time": pd.NaT,  # stop_distance ~ 99
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=1_000.0)
    assert r.skipped_count == 1
    assert len(r.trades) == 1
    assert r.trades[0].was_skipped
    assert r.trades[0].exit_reason == "skipped"
    assert r.trades[0].position_size == 0.0


def test_senal_sin_vela_posterior_no_genera_operacion():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
    ])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    # la señal cae en la ULTIMA vela: no hay ninguna vela posterior donde entrar
    sig = pd.DataFrame([{
        "timestamp": bars.index[-1], "direction": 1,
        "stop_price": 1.0, "target_price": 999.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=10_000.0)
    assert len(r.trades) == 0
    assert r.skipped_count == 0


def test_varias_operaciones_actualizan_el_equity_secuencialmente():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 110.0, 99.0, 110.0],    # entrada op.1, sube y sale por target
        [110.0, 111.0, 109.0, 110.0],   # señal op.2
        [110.0, 130.0, 109.0, 120.0],   # entrada op.2, sube y sale por target
        [120.0, 121.0, 119.0, 120.0],
    ])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0, risk_pct=1.0)  # 100% para tamaño=equity/stop_distance
    sig = pd.DataFrame([
        {"timestamp": bars.index[0], "direction": 1, "stop_price": 90.0, "target_price": 110.0, "exit_time": pd.NaT},
        {"timestamp": bars.index[2], "direction": 1, "stop_price": 100.0, "target_price": 130.0, "exit_time": pd.NaT},
    ])
    r = run_backtest(sig, bars, cm, sizing, initial_equity=1_000.0)
    assert len(r.trades) == 2
    assert not r.trades[0].was_skipped and not r.trades[1].was_skipped
    equity_tras_op1 = 1_000.0 + r.trades[0].pnl_net
    assert len(r.equity_curve) == 3  # inicial + 2 operaciones
    assert abs(r.equity_curve.iloc[1] - equity_tras_op1) < 1e-6


def test_swap_config_none_no_cobra_nunca():
    bars = _bars([
        [100.0, 100.0, 100.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
        [100.0, 101.0, 99.0, 100.0],
        [100.0, 101.0, 99.0, 105.0],
    ])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{
        "timestamp": bars.index[0], "direction": 1,
        "stop_price": 1.0, "target_price": 999.0, "exit_time": pd.NaT,
    }])
    r = run_backtest(sig, bars, cm, sizing, swap_config=None, initial_equity=10_000.0)
    assert r.trades[0].swap_total == 0.0


def test_senales_vacias():
    bars = _bars([[100.0, 100.0, 100.0, 100.0]])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig_vacio = pd.DataFrame(columns=["timestamp", "direction", "stop_price", "target_price", "exit_time"])
    r = run_backtest(sig_vacio, bars, cm, sizing, initial_equity=5_000.0)
    assert r.trades == []
    assert r.skipped_count == 0
    assert r.initial_equity == 5_000.0


def test_bars_vacio_con_senales_lanza_error_claro():
    """Regresion: bars vacio + señales NO vacias lanzaba un IndexError crudo
    ('index 0 is out of bounds') en vez de un ValueError explicativo. Se
    exige el error claro; el caso degenerado bars vacio + señales vacias
    (sin nada que procesar) NO debe lanzar nada."""
    bars_vacio = pd.DataFrame(
        {"open": [], "high": [], "low": [], "close": []},
        index=pd.DatetimeIndex([], tz="UTC"),
    )
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{
        "timestamp": pd.Timestamp("2024-01-01", tz="UTC"), "direction": 1, "stop_price": 1.0,
    }])
    try:
        run_backtest(sig, bars_vacio, cm, sizing)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass

    sig_vacio = pd.DataFrame(columns=["timestamp", "direction", "stop_price"])
    r = run_backtest(sig_vacio, bars_vacio, cm, sizing, initial_equity=500.0)
    assert r.trades == [] and r.skipped_count == 0 and r.initial_equity == 500.0


def test_valida_columnas_de_bars():
    bars_mal = pd.DataFrame(
        {"open": [1.0], "high": [1.0], "low": [1.0]},  # falta 'close'
        index=pd.date_range("2024-01-01", periods=1, tz="UTC"),
    )
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{"timestamp": bars_mal.index[0], "direction": 1, "stop_price": 1.0}])
    try:
        run_backtest(sig, bars_mal, cm, sizing)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_valida_indice_tz_aware():
    bars_naive = pd.DataFrame(
        {"open": [1.0, 1.0], "high": [1.0, 1.0], "low": [1.0, 1.0], "close": [1.0, 1.0]},
        index=pd.date_range("2024-01-01", periods=2),  # SIN tz
    )
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{"timestamp": bars_naive.index[0], "direction": 1, "stop_price": 1.0}])
    try:
        run_backtest(sig, bars_naive, cm, sizing)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_valida_indice_ordenado():
    idx = pd.to_datetime(["2024-01-02", "2024-01-01"], utc=True)  # invertido
    bars_desordenadas = pd.DataFrame(
        {"open": [1.0, 1.0], "high": [1.0, 1.0], "low": [1.0, 1.0], "close": [1.0, 1.0]},
        index=idx,
    )
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{"timestamp": idx[0], "direction": 1, "stop_price": 1.0}])
    try:
        run_backtest(sig, bars_desordenadas, cm, sizing)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_valida_columnas_de_signals():
    bars = _bars([[100.0, 100.0, 100.0, 100.0], [100.0, 100.0, 100.0, 100.0]])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig_mal = pd.DataFrame([{"timestamp": bars.index[0], "direction": 1}])  # falta stop_price
    try:
        run_backtest(sig_mal, bars, cm, sizing)
        assert False, "debia lanzar ValueError"
    except ValueError:
        pass


def test_direccion_invalida_lanza():
    bars = _bars([[100.0, 100.0, 100.0, 100.0], [100.0, 100.0, 100.0, 100.0]])
    cm = CostModel(spread_total=0.0)
    sizing = SizingConfig(min_size=1.0, size_step=1.0)
    sig = pd.DataFrame([{"timestamp": bars.index[0], "direction": 0, "stop_price": 1.0}])
    try:
        run_backtest(sig, bars, cm, sizing)
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
        except Exception as e:
            print(f"  [FALLA] {t.__name__} -- excepcion inesperada: {type(e).__name__}: {e}")
            fail += 1
    print(f"\ntest_execution.py: {ok} pasadas, {fail} fallidas de {len(tests)}")
    return fail == 0


if __name__ == "__main__":
    ok = _run_all()
    sys.exit(0 if ok else 1)
