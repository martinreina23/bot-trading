#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-13 -- la configuracion por defecto de XAUUSD son los valores medidos, marcados
PROVISIONALES: spread 0,19 USD/oz y comision 0,07 USD/oz de ida y vuelta."""
from __future__ import annotations

from decimal import Decimal

from conftest import D

from configuracion import config_xauusd_defecto


def test_r13a_valores_por_defecto_y_campos_obligatorios():
    """(a) Test que lee la config por defecto y aserta 0,19 / 0,07 y los campos fuente y estado."""
    cfg = config_xauusd_defecto()
    assert cfg.spread == D("0.19")
    assert cfg.comision == D("0.07")
    assert cfg.fuente
    assert cfg.estado
    assert "PROVISIONAL" in cfg.estado


def test_r13b_coste_relativo_contra_atr_mediana_4h():
    """(b) Contraste con coste_relativo.md, seccion "CORRECCION (31/07) -- sesgo del ATR medio en
    XAUUSD", tabla "coste relativo contra ATR MEDIANA", fila XAUUSD 4h: el cargo de ida y vuelta
    del motor (0,26) dividido por el ATR14 mediana 4h del oro que publica esa fila (22,1527
    USD/oz) x 100 = 1,17% (+-0,01 punto). Cifra citada tal cual de la fila de esa tabla (no de
    04-resultados/atr_15m_1h_4h.json, que no fue leido para esta ficha -- correccion declarada en
    la seccion 5 de la especificacion)."""
    cfg = config_xauusd_defecto()
    cargo_ida_y_vuelta = cfg.spread + cfg.comision
    assert cargo_ida_y_vuelta == D("0.26")

    atr14_mediana_4h_oro = Decimal("22.1527")  # coste_relativo.md, tabla ATR MEDIANA, fila XAUUSD 4h
    coste_relativo_pct = cargo_ida_y_vuelta / atr14_mediana_4h_oro * 100

    esperado = Decimal("1.17")
    assert abs(coste_relativo_pct - esperado) <= Decimal("0.01")
