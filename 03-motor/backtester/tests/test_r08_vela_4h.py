#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-08 -- vela de 4h identica a la de 02.02.01/02.02.03: rejilla UTC pura 0/4/8/12/16/20,
label="left", closed="left"; bordes de ventana en cortes de 22:00 UTC; velas truncadas
descartadas exactamente como `remuestrear` con inicio/fin."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "03-motor" / "scripts"))
import precios_mercado as pm  # noqa: E402

from datos import cargar_1m, construir_velas_4h  # noqa: E402

DATOS_XAUUSD_1M = RAIZ / "02-datos" / "bruto" / "XAUUSD" / "1m.csv.gz"


def _serie_1m_sintetica_con_borde_22utc() -> pd.DataFrame:
    """1 minuto por fila, de 2026-01-05 20:00 UTC a 2026-01-07 02:00 UTC (cruza un corte de 22:00
    UTC y varios bordes de la rejilla 4h)."""
    inicio = datetime(2026, 1, 5, 20, 0, tzinfo=timezone.utc)
    fin = datetime(2026, 1, 7, 2, 0, tzinfo=timezone.utc)
    n = int((fin - inicio).total_seconds() // 60)
    idx = pd.DatetimeIndex([inicio + timedelta(minutes=i) for i in range(n)], name="ts_utc")
    precio_base = 3000.0
    datos = {
        "open": [precio_base + i * 0.01 for i in range(n)],
        "high": [precio_base + i * 0.01 + 0.05 for i in range(n)],
        "low": [precio_base + i * 0.01 - 0.05 for i in range(n)],
        "close": [precio_base + i * 0.01 + 0.02 for i in range(n)],
    }
    return pd.DataFrame(datos, index=idx)


def test_r08a_motor_y_remuestrear_directo_coinciden_incluidos_descartes():
    """(a) Sobre una serie con un borde de ventana a las 22:00 UTC: primera y ultima vela del
    motor coinciden con las de `remuestrear`, incluidos los descartes de bins truncados."""
    df1m = _serie_1m_sintetica_con_borde_22utc()
    inicio = datetime(2026, 1, 5, 22, 0, tzinfo=timezone.utc)
    fin = datetime(2026, 1, 7, 0, 0, tzinfo=timezone.utc)

    velas_motor = construir_velas_4h(df1m, inicio, fin)
    velas_directas = pm.remuestrear(df1m, "4h", inicio, fin)

    assert velas_motor.equals(velas_directas)
    assert list(velas_motor.index) == list(velas_directas.index)
    # cordura: las horas de apertura caen en la rejilla 0/4/8/12/16/20
    assert all(h in (0, 4, 8, 12, 16, 20) for h in velas_motor.index.hour)


def test_r08b_tramo_real_todas_las_aperturas_en_la_rejilla():
    """(b) Sobre un tramo real de 02-datos/bruto/XAUUSD/1m.csv.gz: todas las aperturas de las
    velas 4h del motor tienen hora en {0,4,8,12,16,20} UTC."""
    if not DATOS_XAUUSD_1M.exists():
        import pytest
        pytest.skip(f"no existe {DATOS_XAUUSD_1M} en este entorno")

    df1m = cargar_1m(DATOS_XAUUSD_1M)
    tramo = df1m.iloc[: 60 * 24 * 10]  # primeros ~10 dias, de sobra para varias velas 4h
    velas_4h = construir_velas_4h(tramo)

    assert len(velas_4h) > 0
    horas = set(velas_4h.index.hour)
    assert horas.issubset({0, 4, 8, 12, 16, 20})
