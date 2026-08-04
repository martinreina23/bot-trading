#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-05 -- el caso hecho a mano es la prueba maestra: los tres casos de la seccion 7 (CL-1, CL-2,
CL-2b), pruebas automatizadas permanentes. Cajas finales exactas a 2 decimales, sin tolerancia."""
from __future__ import annotations

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, estrategia_sonda

from motor import simular


def test_r05_cl1_2014_55(velas_cl1):
    resultado = simular(velas_cl1, estrategia_sonda(D("55.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert resultado.caja_final == D("2014.55")


def test_r05_cl2_1878_88(velas_cl2):
    resultado = simular(velas_cl2, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert resultado.caja_final == D("1878.88")


def test_r05_cl2b_1979_88(velas_cl2b):
    resultado = simular(velas_cl2b, estrategia_sonda(D("100.00")),
                         cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    assert resultado.caja_final == D("1979.88")
