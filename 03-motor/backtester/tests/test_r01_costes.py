#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-01 -- costes nativos dentro de la simulacion (spread embebido en el precio, comision y swap
como apuntes fechados dentro del registro, nunca un descuento porcentual aplicado despues)."""
from __future__ import annotations

from decimal import Decimal

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, estrategia_sonda

from motor import Decision, simular


def test_r01a_cl1_caja_final_y_apuntes(velas_cl1):
    """(a) CL-1: caja final 2.014,55 USD exactos, con los apuntes fechados de comision y swap."""
    resultado = simular(velas_cl1, estrategia_sonda(D("55.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())

    assert resultado.caja_final == D("2014.55")
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]

    comisiones = [a for a in op.apuntes if a.tipo == "comision"]
    assert len(comisiones) == 1
    assert comisiones[0].importe == D("-0.03")
    assert comisiones[0].ts == op.ts_salida

    swaps = {a.ts: a.importe for a in op.apuntes if a.tipo == "swap"}
    ts_mar_2200 = op.ts_entrada.normalize() + __import__("pandas").Timedelta(hours=22)
    ts_mie_2200 = ts_mar_2200 + __import__("pandas").Timedelta(days=1)
    assert swaps[ts_mar_2200] == D("-0.09")
    assert swaps[ts_mie_2200] == D("-0.27")


def test_r01b_ida_vuelta_plana_corto():
    """(b) Ida y vuelta sobre precio plano: corto de 0,1 oz abierto al bid 3.000,00 y recomprado al
    ask 3.000,20, comision 0,10 USD/oz -> variacion de caja exactamente -0,03 USD (-0,02 de spread,
    -0,01 de comision)."""
    from conftest import construir_velas

    velas = construir_velas([
        ("2026-06-01T00:00:00", 3000.00, 3000.00, 3000.00, 3000.00),  # bar de señal
        ("2026-06-01T04:00:00", 3000.00, 3005.00, 2995.00, 3000.00),  # entrada: bid 3.000,00
        ("2026-06-01T08:00:00", 3000.00, 3005.00, 2995.00, 3000.00),  # salida: ask 3.000,20
    ])

    llamadas = {"n": 0}

    def estrategia(velas_cerradas, posicion, ts_cierre_visible):
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            return Decision("abrir_corto", distancia_stop=D("200.00"))
        if llamadas["n"] == 2:
            return Decision("cerrar")
        return Decision("nada")

    cfg_instrumento = cfg_instrumento_casos_lapiz()
    cfg_cuenta = cfg_cuenta_casos_lapiz()  # capital 2000, riesgo 1% = 20.00; 20.00/200.00 = 0.1 oz exacto

    resultado = simular(velas, estrategia, cfg_instrumento, cfg_cuenta)

    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert op.direccion == "corto"
    assert op.onzas == D("0.1")
    assert op.precio_entrada == D("3000.00")
    assert op.precio_salida == D("3000.20")

    spread_apunte = [a for a in op.apuntes if a.tipo == "resultado_precio"][0].importe
    comision_apunte = [a for a in op.apuntes if a.tipo == "comision"][0].importe
    assert spread_apunte == D("-0.02")
    assert comision_apunte == D("-0.01")
    assert op.resultado_neto == D("-0.03")
    assert resultado.caja_final - resultado.caja_inicial == D("-0.03")


def _asercion_caja_cuadra(resultado) -> None:
    """R-01(c): caja_final - caja_inicial == suma de TODOS los apuntes de TODAS las operaciones,
    sin residuo."""
    suma_apuntes = Decimal("0")
    for op in resultado.operaciones:
        for apunte in op.apuntes:
            suma_apuntes += apunte.importe
    assert resultado.caja_final - resultado.caja_inicial == suma_apuntes


def test_r01c_asercion_global_cl1(velas_cl1):
    resultado = simular(velas_cl1, estrategia_sonda(D("55.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    _asercion_caja_cuadra(resultado)


def test_r01c_asercion_global_cl2(velas_cl2):
    resultado = simular(velas_cl2, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    _asercion_caja_cuadra(resultado)


def test_r01c_asercion_global_cl2b(velas_cl2b):
    resultado = simular(velas_cl2b, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    _asercion_caja_cuadra(resultado)
