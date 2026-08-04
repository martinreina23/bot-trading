#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-09 -- asimetria del swap del oro, calibrada de la medicion (coste_swap.md)."""
from __future__ import annotations

import pandas as pd

from conftest import D

from configuracion import config_xauusd_defecto
from motor import calcular_apuntes_swap


def test_r09a_config_dentro_del_rango_medido():
    """(a) -8,16 <= swap_largo_anual <= -6,64 · -0,76 <= swap_corto_anual <= +0,64 · existen los
    campos fuente y estado."""
    cfg = config_xauusd_defecto()
    assert D("-8.16") <= cfg.swap_largo_anual <= D("-6.64")
    assert D("-0.76") <= cfg.swap_corto_anual <= D("0.64")
    assert cfg.fuente
    assert cfg.estado


def test_r09b_asimetria_al_menos_8x():
    """(b) Con esa config, una noche normal de largo produce un cargo (negativo) y la misma noche
    en corto produce un apunte de magnitud al menos 8 veces menor en valor absoluto."""
    cfg = config_xauusd_defecto()
    ts_entrada = pd.Timestamp("2026-04-06T00:00:00", tz="UTC")   # lunes
    ts_cierre = pd.Timestamp("2026-04-07T00:00:00", tz="UTC")    # martes (una noche, martes NO es
    # miercoles: no hay triple de por medio, es "una noche normal")

    apuntes_largo = calcular_apuntes_swap("largo", ts_entrada, ts_cierre, D("3000.00"), D("1.0"), cfg)
    apuntes_corto = calcular_apuntes_swap("corto", ts_entrada, ts_cierre, D("3000.00"), D("1.0"), cfg)

    assert len(apuntes_largo) == 1
    assert len(apuntes_corto) == 1
    importe_largo = apuntes_largo[0].importe
    importe_corto = apuntes_corto[0].importe

    assert importe_largo < 0  # cargo, C-3

    magnitud_largo = abs(importe_largo)
    magnitud_corto = abs(importe_corto)
    assert magnitud_corto * 8 <= magnitud_largo
