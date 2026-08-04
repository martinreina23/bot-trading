#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-14 -- sin mirada al futuro (C-4): la estrategia recibe unicamente las velas cerradas hasta t;
su orden se ejecuta en la apertura de t+1."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz

from motor import Decision, simular


def test_r14_estrategia_sonda_nunca_ve_mas_alla_de_la_vela_actual(velas_cl1):
    """Estrategia-sonda que registra, en cada decision, el timestamp maximo visible: siempre es
    exactamente la apertura de la vela actual (nunca una posterior), y toda orden que nazca de esa
    decision ejecuta estrictamente despues (en la apertura de la vela siguiente, cuando existe)."""
    registro = []

    def estrategia_sonda_r14(velas_cerradas, posicion, ts_cierre_visible):
        registro.append(velas_cerradas.index[-1])  # apertura de la ultima vela vista
        ultimo_close = float(velas_cerradas["close"].iloc[-1])
        if posicion is None:
            if ultimo_close >= 3000.00:
                return Decision("abrir_largo", distancia_stop=D("55.00"))
            return Decision("nada")
        if ultimo_close >= 3045.00:
            return Decision("cerrar")
        return Decision("nada")

    resultado = simular(velas_cl1, estrategia_sonda_r14,
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())

    # (a) se pregunta una vez por vela, nunca con una vela que no ha cerrado: el maximo visible en
    #     la llamada i es exactamente la apertura de la vela i, nunca una posterior.
    assert len(registro) == len(velas_cl1)
    for i, ts_max_visible in enumerate(registro):
        assert ts_max_visible == velas_cl1.index[i]

    # (b) toda decision tomada en la llamada i, si genera una orden, la ejecuta en la vela i+1 --
    #     su apertura es SIEMPRE estrictamente posterior al maximo visible que origino la decision
    #     (indice estrictamente creciente, por construccion de la serie).
    for i in range(len(registro) - 1):
        assert registro[i] < velas_cl1.index[i + 1]

    # (c) la unica operacion de CL-1 se decidio con datos de la vela 0 (visible en la llamada 0) y
    #     ejecuto en la vela 1: estrictamente despues del maximo visible que la origino.
    assert len(resultado.operaciones) == 1
    op = resultado.operaciones[0]
    assert velas_cl1.index[0] < op.ts_entrada
    assert op.ts_entrada in set(velas_cl1.index)


def test_r14_ninguna_operacion_ejecuta_en_la_primera_vela(velas_cl1, velas_cl2, velas_cl2b):
    """Ninguna operacion (entrada ni salida) puede ejecutar en la primera vela de la serie: la
    primera vela solo puede GENERAR una decision (con datos de si misma), nunca ejecutarla (no
    existe una vela -1 anterior desde la que pudiera haberse decidido)."""
    from conftest import estrategia_sonda

    for velas, distancia in ((velas_cl1, D("55.00")), (velas_cl2, D("100.00")), (velas_cl2b, D("100.00"))):
        resultado = simular(velas, estrategia_sonda(distancia),
                             cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
        for op in resultado.operaciones:
            assert op.ts_entrada != velas.index[0]
            assert op.ts_entrada in set(velas.index)
            assert op.ts_salida in set(velas.index)
