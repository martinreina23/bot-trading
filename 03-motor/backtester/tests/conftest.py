#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixtures comunes para las pruebas de aceptacion de 04.03.07 (WBS) contra
`03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`.

Los tres casos a lapiz (seccion 7 de la especificacion, R-05) se declaran UNA vez aqui y se
reutilizan desde varios ficheros de prueba (R-01, R-02, R-05, R-06, R-11, R-14, R-15): son datos
del enunciado, transcritos letra por letra de las tablas de la especificacion, no inventados.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

RAIZ_BACKTESTER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_BACKTESTER))

from configuracion import ConfigCuenta, ConfigInstrumento  # noqa: E402
from motor import Decision, _dec  # noqa: E402

D = Decimal


def construir_velas(filas) -> pd.DataFrame:
    """`filas`: lista de (ts_iso_utc, open, high, low, close). Devuelve un DataFrame indexado por
    la apertura de cada vela (UTC), tal como lo espera `motor.simular` (C-2: precios BID)."""
    idx = pd.DatetimeIndex([pd.Timestamp(ts, tz="UTC") for ts, *_ in filas], name="ts_utc")
    datos = {
        "open": [f[1] for f in filas],
        "high": [f[2] for f in filas],
        "low": [f[3] for f in filas],
        "close": [f[4] for f in filas],
    }
    return pd.DataFrame(datos, index=idx)


# --------------------------------------------------------------------------------------------
# CL-1 -- largo con swap (triple miercoles incluido) y salida por señal
# --------------------------------------------------------------------------------------------
VELAS_CL1 = [
    ("2026-03-03T12:00:00", 2990.00, 3001.00, 2989.00, 3000.00),
    ("2026-03-03T16:00:00", 3000.00, 3010.00, 2995.00, 3005.00),
    ("2026-03-03T20:00:00", 3005.00, 3012.00, 3000.00, 3010.00),
    ("2026-03-04T00:00:00", 3010.00, 3015.00, 3002.00, 3008.00),
    ("2026-03-04T04:00:00", 3008.00, 3020.00, 3006.00, 3018.00),
    ("2026-03-04T08:00:00", 3018.00, 3030.00, 3015.00, 3025.00),
    ("2026-03-04T12:00:00", 3025.00, 3035.00, 3020.00, 3030.00),
    ("2026-03-04T16:00:00", 3030.00, 3040.00, 3028.00, 3038.00),
    ("2026-03-04T20:00:00", 3038.00, 3044.00, 3030.00, 3040.00),
    ("2026-03-05T00:00:00", 3040.00, 3052.00, 3038.00, 3049.00),
    ("2026-03-05T04:00:00", 3050.00, 3055.00, 3045.00, 3052.00),
]

# --------------------------------------------------------------------------------------------
# CL-2 -- stop saltado por hueco de fin de semana de 5,05x
# --------------------------------------------------------------------------------------------
VELAS_CL2 = [
    ("2026-03-06T00:00:00", 2995.00, 3002.00, 2990.00, 3000.00),
    ("2026-03-06T04:00:00", 3000.00, 3008.00, 2996.00, 3004.00),
    ("2026-03-06T08:00:00", 3004.00, 3010.00, 2998.00, 3005.00),
    ("2026-03-06T12:00:00", 3005.00, 3009.00, 2999.00, 3002.00),
    ("2026-03-06T16:00:00", 3002.00, 3006.00, 2996.00, 3001.00),
    ("2026-03-09T00:00:00", 2395.00, 2420.00, 2390.00, 2410.00),
]

# --------------------------------------------------------------------------------------------
# CL-2b -- mismo caso, stop dentro de vela (sin hueco)
# --------------------------------------------------------------------------------------------
VELAS_CL2B = VELAS_CL2[:-1] + [
    ("2026-03-09T00:00:00", 2950.00, 2960.00, 2890.00, 2920.00),
]


def cfg_instrumento_casos_lapiz(swap_corto_anual: Decimal = D("0")) -> ConfigInstrumento:
    """Config comun de los tres casos a lapiz (seccion 7 de la especificacion): spread 0,20,
    comision 0,10 ida y vuelta, swap largo -3,65% anual. Los tres casos son largos; `swap_corto_anual`
    no participa en ninguno -- se declara explicitamente (por defecto 0), nunca se adivina un valor
    de mercado para una direccion que el enunciado no ejercita."""
    return ConfigInstrumento(
        instrumento="XAUUSD-CASO-LAPIZ",
        spread=D("0.20"),
        comision=D("0.10"),
        swap_largo_anual=D("-3.65"),
        swap_corto_anual=swap_corto_anual,
        fuente="03-motor/ESPECIFICACION_MOTOR_BACKTEST.md, seccion 7 (config comun de CL-1/CL-2/CL-2b)",
        estado="CASO A LAPIZ -- no es una cifra de mercado, es el dato del enunciado",
    )


def cfg_cuenta_casos_lapiz() -> ConfigCuenta:
    """Capital 2.000,00 USD, riesgo 1% del capital inicial = 20,00 USD (seccion 7)."""
    return ConfigCuenta(
        capital_inicial=D("2000.00"),
        riesgo_por_operacion_pct=D("1"),
        apalancamiento=D("1"),  # H-2: ningun caso a lapiz depende del margen; valor de prueba propio
    )


def estrategia_sonda(distancia_stop: Decimal, umbral_entrada: Decimal = D("3000.00"),
                      umbral_salida: Decimal = D("3045.00")):
    """La estrategia-sonda de la seccion 7: 'compra cuando cierra >= umbral_entrada estando plana;
    cierra por señal cuando cierra >= umbral_salida'."""

    def _estrategia(velas_cerradas: pd.DataFrame, posicion, ts_cierre_visible: pd.Timestamp) -> Decision:
        ultimo_close = _dec(velas_cerradas["close"].iloc[-1])
        if posicion is None:
            if ultimo_close >= umbral_entrada:
                return Decision("abrir_largo", distancia_stop=distancia_stop)
            return Decision("nada")
        if ultimo_close >= umbral_salida:
            return Decision("cerrar")
        return Decision("nada")

    return _estrategia


@pytest.fixture
def velas_cl1() -> pd.DataFrame:
    return construir_velas(VELAS_CL1)


@pytest.fixture
def velas_cl2() -> pd.DataFrame:
    return construir_velas(VELAS_CL2)


@pytest.fixture
def velas_cl2b() -> pd.DataFrame:
    return construir_velas(VELAS_CL2B)


@pytest.fixture
def cfg_instrumento_lapiz() -> ConfigInstrumento:
    return cfg_instrumento_casos_lapiz()


@pytest.fixture
def cfg_cuenta_lapiz() -> ConfigCuenta:
    return cfg_cuenta_casos_lapiz()
