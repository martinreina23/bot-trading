#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-06 -- la logica vive en un solo sitio.

(a) El remuestreo a 4h se hace importando `remuestrear` de `precios_mercado.py`; el motor no
    reimplementa el metodo de remuestreo de pandas en ningun otro sitio.
(b) Serie 1m sintetica procesada por el motor y por `remuestrear` directamente -> velas 4h
    identicas bit a bit.
(c) Camino unico probado por sabotaje (no por ojo): `test_camino_unico`, ejecutado con
    `pytest -q <dir_motor> -k camino_unico`.

NOTA sobre este fichero: la prueba de aceptacion de (a) exige "0 apariciones" del patron de
remuestreo directo de pandas EN TODO `<dir_motor>`, sin excepcion de comentarios (a diferencia de
R-16b, que si la tiene). Por eso el patron de busqueda se construye aqui por CONCATENACION (nunca
como una cadena contigua): si se escribiera contiguo, este mismo fichero se auto-incumpliria.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pandas as pd

from conftest import (D, VELAS_CL1, VELAS_CL2, VELAS_CL2B, cfg_cuenta_casos_lapiz,
                       cfg_instrumento_casos_lapiz, construir_velas, estrategia_sonda)

import motor
from motor import Decision, simular

RAIZ_BACKTESTER = Path(__file__).resolve().parents[1]
RAIZ = Path(__file__).resolve().parents[3]


# --------------------------------------------------------------------------------------------
# (a) ningun remuestreo directo de pandas en el motor -- el unico del proyecto sigue en
#     precios_mercado.py. Patron construido por concatenacion, ver NOTA del docstring del modulo.
# --------------------------------------------------------------------------------------------
def test_r06a_ningun_resample_en_el_motor():
    patron = "\\" + "." + "resample" + "("
    proc = subprocess.run(
        ["grep", "-rn", patron, str(RAIZ_BACKTESTER), "--include=*.py"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, f"patron de remuestreo directo encontrado dentro del motor:\n{proc.stdout}"


# --------------------------------------------------------------------------------------------
# (b) motor.datos.construir_velas_4h y remuestrear() directo dan velas identicas.
# --------------------------------------------------------------------------------------------
def test_r06b_velas_4h_identicas_a_remuestrear_directo():
    sys.path.insert(0, str(RAIZ / "03-motor" / "scripts"))
    import precios_mercado as pm

    from datos import construir_velas_4h

    inicio_dt = datetime(2026, 2, 2, 0, 0, tzinfo=timezone.utc)
    n = 60 * 24 * 3  # 3 dias de 1 minuto
    idx = pd.DatetimeIndex([inicio_dt + timedelta(minutes=i) for i in range(n)], name="ts_utc")
    df1m = pd.DataFrame({
        "open": [3000.0 + (i % 97) * 0.01 for i in range(n)],
        "high": [3000.5 + (i % 97) * 0.01 for i in range(n)],
        "low": [2999.5 + (i % 97) * 0.01 for i in range(n)],
        "close": [3000.1 + (i % 97) * 0.01 for i in range(n)],
    }, index=idx)

    velas_motor = construir_velas_4h(df1m, inicio_dt, inicio_dt + timedelta(minutes=n))
    velas_directas = pm.remuestrear(df1m, "4h", inicio_dt, inicio_dt + timedelta(minutes=n))
    assert velas_motor.equals(velas_directas)


# --------------------------------------------------------------------------------------------
# (c) test_camino_unico -- sabotaje por monkeypatch de los dos simbolos declarados en el README.
# --------------------------------------------------------------------------------------------
def _estrategia_abre_una_vez(accion: str, distancia: Decimal):
    """Abre en la primera llamada, no vuelve a decidir nada mas (deja el stop hacer su trabajo)."""
    llamadas = {"n": 0}

    def f(velas_cerradas, posicion, ts_cierre_visible):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            return Decision(accion, distancia_stop=distancia)
        return Decision("nada")

    return f


def _estrategia_abre_y_cierra_siguiente(accion: str, distancia: Decimal):
    """Abre en la primera llamada, cierra por señal en la segunda (posicion ya abierta)."""
    llamadas = {"n": 0}

    def f(velas_cerradas, posicion, ts_cierre_visible):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            return Decision(accion, distancia_stop=distancia)
        if llamadas["n"] == 2:
            return Decision("cerrar")
        return Decision("nada")

    return f


def _construir_escenarios():
    """Los 6 casos que exige R-06(c): CL-1, CL-2, CL-2b y R-02(d), R-02(e), R-03(a)-(b) -- largos
    y cortos; stop por hueco, dentro de vela y en la vela de entrada; apuntes de swap en las dos
    direcciones. Cada tupla es (nombre, velas, estrategia, cfg_instrumento, cfg_cuenta), lista para
    pasarse literalmente a `motor.simular`."""
    escenarios = []

    escenarios.append(("CL-1", construir_velas(VELAS_CL1), estrategia_sonda(D("55.00")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))
    escenarios.append(("CL-2", construir_velas(VELAS_CL2), estrategia_sonda(D("100.00")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))
    escenarios.append(("CL-2b", construir_velas(VELAS_CL2B), estrategia_sonda(D("100.00")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    # R-02(d): largo, stop dentro de la propia vela de entrada.
    velas_r02d = construir_velas([
        ("2026-04-06T08:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-04-06T12:00:00", 3000.00, 3010.00, 2940.00, 2999.00),
    ])
    escenarios.append(("R-02d", velas_r02d, _estrategia_abre_una_vez("abrir_largo", D("55.00")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    # R-02(e): corto, tres sub-casos (no dispara / dispara en nivel / dispara en apertura).
    # nivel = open_bid_entrada + distancia + spread = 3000.00 + 9.80 + 0.20 = 3010.00
    velas_r02e_no_dispara = construir_velas([
        ("2026-04-06T00:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-04-06T04:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
        ("2026-04-06T08:00:00", 3000.00, 3009.79, 2995.00, 3000.00),
    ])
    escenarios.append(("R-02e-no-dispara", velas_r02e_no_dispara,
                        _estrategia_abre_una_vez("abrir_corto", D("9.80")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    velas_r02e_dispara_nivel = construir_velas([
        ("2026-04-06T00:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-04-06T04:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
        ("2026-04-06T08:00:00", 3000.00, 3009.80, 2995.00, 3000.00),
    ])
    escenarios.append(("R-02e-dispara-nivel", velas_r02e_dispara_nivel,
                        _estrategia_abre_una_vez("abrir_corto", D("9.80")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    velas_r02e_dispara_apertura = construir_velas([
        ("2026-04-06T00:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-04-06T04:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
        ("2026-04-06T08:00:00", 3050.00, 3055.00, 3045.00, 3050.00),
    ])
    escenarios.append(("R-02e-dispara-apertura", velas_r02e_dispara_apertura,
                        _estrategia_abre_una_vez("abrir_corto", D("9.80")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    # R-03(a)/(b): semana completa lunes 00:00 a lunes 00:00 siguiente, largo y corto.
    velas_r03a = construir_velas([
        ("2026-03-01T20:00:00", 3000.00, 3000.00, 3000.00, 3000.00),  # domingo, señal
        ("2026-03-02T00:00:00", 3000.00, 3005.00, 2990.00, 3000.00),  # lunes 00:00, entrada
        ("2026-03-09T00:00:00", 3000.00, 3005.00, 2995.00, 3000.00),  # lunes 00:00 siguiente, salida
    ])
    escenarios.append(("R-03a", velas_r03a,
                        _estrategia_abre_y_cierra_siguiente("abrir_largo", D("50.00")),
                        cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz()))

    velas_r03b = construir_velas([
        ("2026-03-01T20:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-03-02T00:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
        ("2026-03-09T00:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
    ])
    escenarios.append(("R-03b", velas_r03b,
                        _estrategia_abre_y_cierra_siguiente("abrir_corto", D("50.00")),
                        cfg_instrumento_casos_lapiz(swap_corto_anual=D("0.64")), cfg_cuenta_casos_lapiz()))

    return escenarios


def _ejecutar_y_recolectar(escenarios):
    """Reejecuta `motor.simular` sobre los 6 escenarios y devuelve (fills, swaps): cada precio de
    fill de stop realizado y cada importe de apunte de swap, en orden estable."""
    fills = []
    swaps = []
    for _nombre, velas, estrategia, cfg_instrumento, cfg_cuenta in escenarios:
        resultado = simular(velas, estrategia, cfg_instrumento, cfg_cuenta)
        for op in resultado.operaciones:
            if op.motivo_salida == "stop":
                fills.append(op.precio_salida)
            for apunte in op.apuntes:
                if apunte.tipo == "swap":
                    swaps.append(apunte.importe)
    return fills, swaps


def test_camino_unico(monkeypatch, capsys):
    """R-06(c): sabotea por monkeypatch, por nombre de simbolo, `resolver_fill_stop` y
    `calcular_apuntes_swap` -- los dos simbolos declarados en `03-motor/backtester/README.md`.
    Pasa si `fills_intactos == 0` y `apuntes_intactos == 0`.

    Los escenarios se RECONSTRUYEN de cero para cada uno de los tres pases (base, sabotaje de
    fill, sabotaje de swap): algunas estrategias de prueba son estado-con-memoria (cuentan
    llamadas para decidir cuando abrir), y reutilizar el mismo objeto de estrategia entre pases
    arrastraria su contador de una ejecucion a la siguiente -- no es lo que hace `simular()` en
    produccion (cada llamada real parte de una estrategia fresca) y falsearia la comparacion."""
    # --- Paso 1: linea base, sin sabotaje. ---
    fills_base, swaps_base = _ejecutar_y_recolectar(_construir_escenarios())
    assert len(fills_base) >= 1, "el paquete de escenarios no produjo ningun fill de stop"
    assert len(swaps_base) >= 1, "el paquete de escenarios no produjo ningun apunte de swap"

    # --- Paso 2: sabotea resolver_fill_stop (+1.00 USD a todo precio de fill que devuelve). ---
    fill_original = motor.resolver_fill_stop

    def fill_envoltura(*args, **kwargs):
        r = fill_original(*args, **kwargs)
        return r if r is None else r + Decimal("1.00")

    monkeypatch.setattr(motor, "resolver_fill_stop", fill_envoltura)
    fills_saboteados, _swaps_ignorar = _ejecutar_y_recolectar(_construir_escenarios())
    monkeypatch.undo()

    assert len(fills_saboteados) == len(fills_base)
    fills_intactos = sum(1 for original, saboteado in zip(fills_base, fills_saboteados)
                          if original == saboteado)

    # --- Paso 3: restaura, sabotea calcular_apuntes_swap (+1.00 USD a cada apunte). ---
    swap_original = motor.calcular_apuntes_swap

    def swap_envoltura(*args, **kwargs):
        apuntes = swap_original(*args, **kwargs)
        return [motor.Apunte(ts=a.ts, tipo=a.tipo, importe=a.importe + Decimal("1.00"))
                for a in apuntes]

    monkeypatch.setattr(motor, "calcular_apuntes_swap", swap_envoltura)
    _fills_ignorar, swaps_saboteados = _ejecutar_y_recolectar(_construir_escenarios())
    monkeypatch.undo()

    assert len(swaps_saboteados) == len(swaps_base)
    apuntes_intactos = sum(1 for original, saboteado in zip(swaps_base, swaps_saboteados)
                            if original == saboteado)

    with capsys.disabled():
        print(f"\n[R-06c] fills_intactos={fills_intactos} (de {len(fills_base)} fills capturados)")
        print(f"[R-06c] apuntes_intactos={apuntes_intactos} (de {len(swaps_base)} apuntes capturados)")

    assert fills_intactos == 0
    assert apuntes_intactos == 0
