#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-11 -- hueco de fin de semana: el motor no ejecuta nada dentro de un hueco; un stop saltado
por el hueco ejecuta al primer precio real, con la perdida del hueco, no la del stop."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, estrategia_sonda

from motor import simular


def test_r11a_cl2_hueco_5_05x():
    """(a) CL-2, construido con un hueco de exactamente 5,05x la distancia de stop: fill en
    2.395,00 y caja final 1.878,88."""
    from conftest import VELAS_CL2, construir_velas
    resultado = simular(construir_velas(VELAS_CL2), estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    op = resultado.operaciones[0]
    assert op.precio_salida == D("2395.00")
    assert resultado.caja_final == D("1878.88")

    distancia_stop = D("100.00")
    hueco_mas_alla_del_stop = op.nivel_stop - op.precio_salida
    assert hueco_mas_alla_del_stop == D("505.00")
    assert hueco_mas_alla_del_stop / distancia_stop == D("5.05")


def test_r11b_todo_fill_lleva_timestamp_de_una_vela_existente(velas_cl1, velas_cl2, velas_cl2b):
    """(b) Aserción global: todo fill (entrada, salida, stop) lleva el timestamp de una vela
    EXISTENTE en la serie de entrada; ningun apunte de fill tiene un timestamp dentro de un tramo
    sin velas."""
    casos = (
        (velas_cl1, D("55.00")),
        (velas_cl2, D("100.00")),
        (velas_cl2b, D("100.00")),
    )
    for velas, distancia in casos:
        resultado = simular(velas, estrategia_sonda(distancia),
                             cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
        indice = set(velas.index)
        for op in resultado.operaciones:
            assert op.ts_entrada in indice
            assert op.ts_salida in indice
