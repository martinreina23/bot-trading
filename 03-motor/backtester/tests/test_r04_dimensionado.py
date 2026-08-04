#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-04 -- dimensionado por riesgo: onzas = riesgo_por_operacion / distancia_de_stop, redondeado a
la baja al paso de lote (R-10); el riesgo nominal registrado es el del tamaño realmente abierto."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, estrategia_sonda

from motor import dimensionar, simular


def test_r04_cl1_riesgo_20_distancia_55():
    """riesgo 20,00 USD, distancia 55,00 USD/oz -> 0,3636... -> tamaño abierto 0,3 oz, riesgo
    nominal registrado 16,50 USD."""
    onzas, riesgo_nominal = dimensionar(D("20.00"), D("55.00"), D("0.1"))
    assert onzas == D("0.3")
    assert riesgo_nominal == D("16.50")


def test_r04_sin_redondeo_distancia_100():
    """distancia 100,00 y riesgo 20,00 -> exactamente 0,2 oz (sin redondeo)."""
    onzas, riesgo_nominal = dimensionar(D("20.00"), D("100.00"), D("0.1"))
    assert onzas == D("0.2")
    assert riesgo_nominal == D("20.00")


def test_r04_riesgo_nominal_registrado_es_del_tamano_abierto(velas_cl1):
    """El riesgo nominal registrado en una operacion real es el del tamaño REALMENTE abierto
    (0,3 oz x 55,00 = 16,50), no el riesgo teorico configurado (20,00)."""
    resultado = simular(velas_cl1, estrategia_sonda(D("55.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    op = resultado.operaciones[0]
    assert op.onzas == D("0.3")
    assert op.riesgo_nominal == D("16.50")
    assert op.riesgo_nominal != D("20.00")
