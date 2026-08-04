#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-07 -- unidad USD por onza en todo el motor, nunca la unidad de cotizacion habitual de las
divisas (C-1).

NOTA sobre este fichero: al igual que en `test_r06_camino_unico.py`, la prueba de aceptacion de
(a) exige "0 lineas" en TODO `<dir_motor>`, sin excepcion de comentarios. Por eso los patrones de
busqueda de este fichero se construyen por CONCATENACION en vez de como texto contiguo: si se
escribieran contiguos, este mismo fichero se auto-incumpliria."""
from __future__ import annotations

import subprocess
from pathlib import Path

from conftest import D, construir_velas

from configuracion import ConfigCuenta, ConfigInstrumento
from motor import Decision, simular

RAIZ_BACKTESTER = Path(__file__).resolve().parents[1]
# Las dos constantes de abajo se construyen por CONCATENACION a proposito: la palabra completa no
# puede aparecer contigua en ningun comentario de este fichero (se auto-incumpliria la prueba de
# 0 apariciones sobre <dir_motor>, que no tiene excepcion para comentarios en R-07).
_UNIDAD_PROHIBIDA = "p" + "ip"       # la unidad de cotizacion habitual de las divisas
_NOMBRE_PROHIBIDO = "pipe" + "line"  # el nombre generico que R-07 prohibe usar dentro del motor


def test_r07a_ni_una_mencion_a_la_unidad_prohibida_en_el_motor():
    """(a) Patron `\\b` + unidad-prohibida + `s?` + `\\b`, case-insensitive, sobre TODO
    `<dir_motor>` -> 0 lineas."""
    patron = r"\b" + _UNIDAD_PROHIBIDA + r"s?\b"
    proc = subprocess.run(
        ["grep", "-rniE", patron, str(RAIZ_BACKTESTER), "--include=*.py"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, f"la unidad prohibida aparece dentro del motor:\n{proc.stdout}"


def test_r07a_nombre_prohibido_no_aparece():
    """No nombrar nada con el nombre prohibido dentro del motor (instruccion explicita de R-07)."""
    proc = subprocess.run(
        ["grep", "-rniE", _NOMBRE_PROHIBIDO, str(RAIZ_BACKTESTER), "--include=*.py"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, f"el nombre prohibido aparece en el motor:\n{proc.stdout}"


def test_r07b_ida_vuelta_plana_1oz_config_medida():
    """(b) Ida y vuelta plana de 1 oz con la config medida (spread 0,19, comision 0,07) -> cargo
    total exactamente 0,26 USD, la cifra de la fila XAUUSD de coste_operar.md."""
    velas = construir_velas([
        ("2026-05-04T00:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-05-04T04:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
        ("2026-05-04T08:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
    ])
    cfg_instrumento = ConfigInstrumento(
        instrumento="XAUUSD", spread=D("0.19"), comision=D("0.07"),
        swap_largo_anual=D("0"), swap_corto_anual=D("0"),
        fuente="01-investigacion/mercados/coste_operar.md, fila XAUUSD",
        estado="PROVISIONAL (la sustituye 04.01.02)",
    )
    # riesgo 100.00 / distancia 1000.00 -> 0.1 oz teoricas exactas... se necesita 1 oz exacta:
    # riesgo 1000.00 (50% del capital, caso de prueba) / distancia 1000.00 = 1.0 oz exacta.
    cfg_cuenta = ConfigCuenta(capital_inicial=D("2000.00"), riesgo_por_operacion_pct=D("50"),
                               apalancamiento=D("1"))

    llamadas = {"n": 0}

    def estrategia(velas_cerradas, posicion, ts_cierre_visible):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            return Decision("abrir_largo", distancia_stop=D("1000.00"))
        if llamadas["n"] == 2:
            return Decision("cerrar")
        return Decision("nada")

    resultado = simular(velas, estrategia, cfg_instrumento, cfg_cuenta)
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert op.onzas == D("1.0")

    spread_apunte = [a for a in op.apuntes if a.tipo == "resultado_precio"][0].importe
    comision_apunte = [a for a in op.apuntes if a.tipo == "comision"][0].importe
    cargo_total = -(spread_apunte + comision_apunte)  # ambos son costes (negativos): cargo = -suma
    assert cargo_total == D("0.26")
