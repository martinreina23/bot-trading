#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-03 -- financiacion asimetrica con triple miercoles (largo y corto independientes, C-3)."""
from __future__ import annotations

import pandas as pd

from conftest import D

from configuracion import ConfigInstrumento
from motor import calcular_apuntes_swap

TS_LUNES = pd.Timestamp("2026-03-02T00:00:00", tz="UTC")     # semana de CL-1/CL-2 (mar 03/03/2026)
TS_LUNES_SIGUIENTE = pd.Timestamp("2026-03-09T00:00:00", tz="UTC")


def _cfg(swap_largo="-3.65", swap_corto="0.64") -> ConfigInstrumento:
    return ConfigInstrumento(
        instrumento="XAUUSD-PRUEBA-R03",
        spread=D("0.20"), comision=D("0.10"),
        swap_largo_anual=D(swap_largo), swap_corto_anual=D(swap_corto),
        fuente="prueba R-03 (03-motor/backtester/tests/test_r03_swap.py)",
        estado="CASO DE PRUEBA -- no es una cifra de mercado",
    )


def test_r03a_semana_completa_largo():
    """(a) Posicion larga sintetica abierta de lunes 00:00 a lunes 00:00 siguiente (semana
    completa): exactamente 5 apuntes de swap fechados (lun,mar,mie,jue,vie a las 22:00 UTC), el
    del miercoles por el triple exacto de los demas, total 7 unidades."""
    apuntes = calcular_apuntes_swap("largo", TS_LUNES, TS_LUNES_SIGUIENTE, D("3000.00"), D("1.0"),
                                     _cfg())
    assert len(apuntes) == 5

    dias_esperados = {
        pd.Timestamp("2026-03-02T22:00:00", tz="UTC"): 1,  # lunes
        pd.Timestamp("2026-03-03T22:00:00", tz="UTC"): 1,  # martes
        pd.Timestamp("2026-03-04T22:00:00", tz="UTC"): 3,  # miercoles, triple
        pd.Timestamp("2026-03-05T22:00:00", tz="UTC"): 1,  # jueves
        pd.Timestamp("2026-03-06T22:00:00", tz="UTC"): 1,  # viernes
    }
    por_ts = {a.ts: a.importe for a in apuntes}
    assert set(por_ts) == set(dias_esperados)

    importe_unitario = por_ts[pd.Timestamp("2026-03-02T22:00:00", tz="UTC")]
    for ts, mult in dias_esperados.items():
        assert por_ts[ts] == importe_unitario * mult

    total_unidades = sum(dias_esperados.values())
    assert total_unidades == 7
    assert sum(por_ts.values()) == importe_unitario * 7
    assert importe_unitario < 0  # swap largo negativo (coste), C-3


def test_r03b_semana_completa_corto_signo_contrario():
    """(b) La misma semana en corto con swap_corto positivo -> 5 abonos (signo contrario), mismas
    fechas."""
    apuntes = calcular_apuntes_swap("corto", TS_LUNES, TS_LUNES_SIGUIENTE, D("3000.00"), D("1.0"),
                                     _cfg())
    assert len(apuntes) == 5
    for a in apuntes:
        assert a.importe > 0  # swap corto positivo (credito), C-3

    fechas_esperadas = {
        pd.Timestamp("2026-03-02T22:00:00", tz="UTC"),
        pd.Timestamp("2026-03-03T22:00:00", tz="UTC"),
        pd.Timestamp("2026-03-04T22:00:00", tz="UTC"),
        pd.Timestamp("2026-03-05T22:00:00", tz="UTC"),
        pd.Timestamp("2026-03-06T22:00:00", tz="UTC"),
    }
    assert {a.ts for a in apuntes} == fechas_esperadas

    miercoles = [a for a in apuntes if a.ts == pd.Timestamp("2026-03-04T22:00:00", tz="UTC")][0]
    otro = [a for a in apuntes if a.ts == pd.Timestamp("2026-03-02T22:00:00", tz="UTC")][0]
    assert miercoles.importe == otro.importe * 3


def test_r03c_config_distinta_cambia_el_importe_sin_tocar_el_motor(tmp_path):
    """(c) Cambiar la tasa en el fichero de configuracion cambia el importe sin tocar codigo del
    motor (C-8): dos ejecuciones con dos configs (leidas de dos JSON distintos en disco) ->
    importes proporcionales a las tasas."""
    import json

    from configuracion import cargar_config_instrumento

    base = {
        "instrumento": "XAUUSD-PRUEBA-R03C",
        "spread": "0.19", "comision": "0.07",
        "swap_corto_anual": "0",
        "fuente": "prueba R-03(c)", "estado": "CASO DE PRUEBA",
    }
    ruta_x1 = tmp_path / "cfg_x1.json"
    ruta_x2 = tmp_path / "cfg_x2.json"
    ruta_x1.write_text(json.dumps({**base, "swap_largo_anual": "-3.65"}))
    ruta_x2.write_text(json.dumps({**base, "swap_largo_anual": "-7.30"}))  # exactamente el doble

    cfg1 = cargar_config_instrumento(ruta_x1)
    cfg2 = cargar_config_instrumento(ruta_x2)

    apuntes1 = calcular_apuntes_swap("largo", TS_LUNES, TS_LUNES_SIGUIENTE, D("3000.00"), D("1.0"), cfg1)
    apuntes2 = calcular_apuntes_swap("largo", TS_LUNES, TS_LUNES_SIGUIENTE, D("3000.00"), D("1.0"), cfg2)

    por_ts1 = {a.ts: a.importe for a in apuntes1}
    por_ts2 = {a.ts: a.importe for a in apuntes2}
    assert set(por_ts1) == set(por_ts2)
    for ts in por_ts1:
        assert por_ts2[ts] == por_ts1[ts] * 2  # tasa doble -> importe exactamente doble
