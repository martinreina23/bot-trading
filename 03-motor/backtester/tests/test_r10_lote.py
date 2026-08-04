#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-10 -- lote fraccionado de 0,1 onzas: paso 0,1, minimo 0,1, redondeo siempre a la baja; por
debajo del minimo no se abre y se registra el motivo."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz

from motor import Decision, dimensionar, simular


def test_r10_casos_de_dimensionado():
    """0,3636 -> 0,3 · 0,25 -> 0,2 · 0,19 -> 0,1 · 0,09 -> no se abre."""
    onzas, _ = dimensionar(D("0.3636"), D("1"), D("0.1"))
    assert onzas == D("0.3")

    onzas, _ = dimensionar(D("0.25"), D("1"), D("0.1"))
    assert onzas == D("0.2")

    onzas, _ = dimensionar(D("0.19"), D("1"), D("0.1"))
    assert onzas == D("0.1")

    onzas, riesgo_nominal = dimensionar(D("0.09"), D("1"), D("0.1"))
    assert onzas == D("0")
    assert riesgo_nominal == D("0")


def test_r10_operacion_rechazada_queda_en_el_registro():
    """Si el tamaño calculado < 0,1 oz, no se abre la operacion y el registro contiene una entrada
    de operacion rechazada con el motivo exacto."""
    from conftest import construir_velas

    velas = construir_velas([
        ("2026-04-06T08:00:00", 3000.00, 3000.00, 3000.00, 3000.00),
        ("2026-04-06T12:00:00", 3000.00, 3005.00, 2995.00, 3000.00),
    ])

    def estrategia(velas_cerradas, posicion, ts_cierre_visible):
        # riesgo=20.00 (1% de 2000), distancia=250.00 -> 0.08 oz teoricas -> por debajo de 0.1
        return Decision("abrir_largo", distancia_stop=D("250.00")) if posicion is None else Decision("nada")

    resultado = simular(velas, estrategia, cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())

    assert len(resultado.operaciones) == 0
    assert len(resultado.rechazadas) == 1
    assert resultado.rechazadas[0].motivo == "tamaño calculado inferior al lote mínimo de 0,1 oz"
    assert resultado.caja_final == resultado.caja_inicial  # ninguna operacion abierta, caja intacta


def test_r10_asercion_global_ningun_tamano_por_debajo_del_minimo_ni_con_resto(velas_cl1, velas_cl2):
    from conftest import estrategia_sonda

    for velas, distancia in ((velas_cl1, D("55.00")), (velas_cl2, D("100.00"))):
        resultado = simular(velas, estrategia_sonda(distancia),
                             cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
        for op in resultado.operaciones:
            assert op.onzas >= D("0.1")
            resto = op.onzas % D("0.1")
            assert resto == D("0") or abs(resto) < D("1e-9")
