#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-02 -- un stop nunca ejecuta a mejor precio que el disparado."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, construir_velas, estrategia_sonda

from motor import Decision, resolver_fill_stop, simular


def test_r02a_intra_vela_cl2b(velas_cl2b):
    """(a) Intra-vela: CL-2b -> fill exactamente 2.900,00, caja final 1.979,88 USD."""
    resultado = simular(velas_cl2b, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert op.motivo_salida == "stop"
    assert op.precio_salida == D("2900.00")
    assert resultado.caja_final == D("1979.88")


def test_r02b_hueco_cl2(velas_cl2):
    """(b) Hueco: CL-2 -> fill exactamente 2.395,00, nunca 2.900,00."""
    resultado = simular(velas_cl2, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert op.motivo_salida == "stop"
    assert op.precio_salida == D("2395.00")
    assert op.precio_salida != D("2900.00")


def test_r02c_toque_exacto():
    """(c) Toque exacto: vela con L = nivel del stop -> dispara y ejecuta en el nivel."""
    fill = resolver_fill_stop("largo", D("2900.00"), D("2950.00"), D("2955.00"), D("2900.00"),
                               D("0.20"), es_vela_entrada=False)
    assert fill == D("2900.00")


def test_r02d_misma_vela_de_entrada_unitario():
    """(d) Directo: entrada en O bid 3.000,00 (ask 3.000,20), stop 2.945,00, esa misma vela con
    L 2.940,00 -> salida por stop en esa vela a 2.945,00. El open-gap NO se comprueba en la vela de
    entrada (C-5): si se comprobara, 3.000,00 no dispara nada por si solo -- lo que dispara es el
    low, que aqui SI se comprueba incluso en la vela de entrada."""
    fill = resolver_fill_stop("largo", D("2945.00"), D("3000.00"), D("3010.00"), D("2940.00"),
                               D("0.20"), es_vela_entrada=True)
    assert fill == D("2945.00")


def test_r02d_misma_vela_de_entrada_via_motor():
    """(d) A traves del motor completo: 2 velas, señal en la primera, entrada+stop en la segunda."""
    velas = construir_velas([
        ("2026-04-06T08:00:00", 3000.00, 3000.00, 3000.00, 3000.00),   # señal (precio arbitrario)
        ("2026-04-06T12:00:00", 3000.00, 3010.00, 2940.00, 2999.00),   # entrada Y stop, misma vela
    ])

    llamadas = {"n": 0}

    def estrategia(velas_cerradas, posicion, ts_cierre_visible):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            return Decision("abrir_largo", distancia_stop=D("55.00"))
        return Decision("nada")

    resultado = simular(velas, estrategia, cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert op.ts_entrada == op.ts_salida  # misma vela
    assert op.nivel_stop == D("2945.00")
    assert op.motivo_salida == "stop"
    assert op.precio_salida == D("2945.00")


def test_r02e_corto_asimetrico():
    """(e) Corto con spread 0,20 y stop de recompra en ask 3.010,00: H bid 3.009,79 -> NO dispara;
    H bid 3.009,80 -> dispara y ejecuta en 3.010,00; apertura bid 3.050,00 -> ejecuta en ask
    3.050,20."""
    nivel = D("3010.00")
    spread = D("0.20")

    no_dispara = resolver_fill_stop("corto", nivel, D("3000.00"), D("3009.79"), D("2995.00"),
                                     spread, es_vela_entrada=False)
    assert no_dispara is None

    dispara_en_nivel = resolver_fill_stop("corto", nivel, D("3000.00"), D("3009.80"), D("2995.00"),
                                           spread, es_vela_entrada=False)
    assert dispara_en_nivel == D("3010.00")

    dispara_en_apertura = resolver_fill_stop("corto", nivel, D("3050.00"), D("3055.00"), D("3045.00"),
                                              spread, es_vela_entrada=False)
    assert dispara_en_apertura == D("3050.20")


def test_r02f_asercion_global_largo_y_corto(velas_cl2, velas_cl2b):
    """(f) Asercion global: para todo stop de largo, precio_fill <= nivel; para todo stop de
    corto, precio_fill >= nivel."""
    casos_largo = [
        (D("2900.00"), D("2950.00"), D("2960.00"), D("2890.00"), False),  # CL-2b
        (D("2900.00"), D("2395.00"), D("2420.00"), D("2390.00"), False),  # CL-2 (hueco)
        (D("2945.00"), D("3000.00"), D("3010.00"), D("2940.00"), True),   # R-02(d)
        (D("2900.00"), D("2900.00"), D("2905.00"), D("2895.00"), False),  # toque exacto
    ]
    for nivel, o, h, l, es_entrada in casos_largo:
        fill = resolver_fill_stop("largo", nivel, o, h, l, D("0.20"), es_entrada)
        if fill is not None:
            assert fill <= nivel

    casos_corto = [
        (D("3010.00"), D("3000.00"), D("3009.80"), D("2995.00"), False),
        (D("3010.00"), D("3050.00"), D("3055.00"), D("3045.00"), False),
        (D("3010.00"), D("3000.00"), D("3009.79"), D("2995.00"), False),
    ]
    for nivel, o, h, l, es_entrada in casos_corto:
        fill = resolver_fill_stop("corto", nivel, o, h, l, D("0.20"), es_entrada)
        if fill is not None:
            assert fill >= nivel

    # Y sobre las ejecuciones completas de CL-2 y CL-2b (via motor.simular):
    for velas, distancia in ((velas_cl2, D("100.00")), (velas_cl2b, D("100.00"))):
        resultado = simular(velas, estrategia_sonda(distancia),
                             cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
        for op in resultado.operaciones:
            if op.motivo_salida == "stop":
                assert op.precio_salida <= op.nivel_stop
