#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 01.02.02 (pieza T2 del trasplante desde gb2, D6=B, 00-direccion/WBS.md).

Dimensionado de posicion por riesgo: tamano = riesgo en $ / distancia al stop
en unidad de precio, redondeado hacia abajo al incremento minimo operable del
instrumento, con suelo en el tamano minimo operable (nunca se salta una senal
por dar un tamano pequeno: el minimo SIEMPRE se toma).

DECISION DE DISENO, declarada: `min_size` y `size_step` son OBLIGATORIOS, sin
valor por defecto propio. El tamano minimo operable (0,01 lotes en forex,
0,01 onzas en oro, distinto en cripto...) es una propiedad del INSTRUMENTO y
del BROKER, que este proyecto todavia no ha elegido (la puerta G1 sigue
pendiente en 00-direccion/WBS.md). Ponerle un numero por defecto aqui seria
adivinar un dato que la regla 6 de CLAUDE.md prohibe suponer; quien construya
la senal de una hipotesis concreta en la Fase 04 lo declara explicitamente.

`risk_pct` si tiene un valor por defecto propio, 0.01 (1%), porque ese numero
YA esta decidido y firmado en el proyecto: criterio G1-C6 de
00-direccion/WBS.md ("el instrumento debe permitir arriesgar como mucho el 1%
del capital por operacion con un stop de 1 x ATR mediana"). Sigue siendo
configurable: cada hipotesis puede pasar el suyo si su especificacion lo pide.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple

# Criterio G1-C6 (00-direccion/WBS.md): arriesgar como mucho el 1% del
# capital por operacion. Es el UNICO numero de este modulo con valor por
# defecto propio, porque es el unico que ya esta decidido en el proyecto.
RIESGO_POR_OPERACION_G1_C6 = 0.01


@dataclass(frozen=True)
class SizingConfig:
    min_size: float
    size_step: float
    risk_pct: float = RIESGO_POR_OPERACION_G1_C6
    max_risk_pct: Optional[float] = None

    def __post_init__(self) -> None:
        if self.min_size <= 0:
            raise ValueError(f"min_size debe ser positivo: {self.min_size!r}")
        if self.size_step <= 0:
            raise ValueError(f"size_step debe ser positivo: {self.size_step!r}")
        if self.risk_pct <= 0:
            raise ValueError(f"risk_pct debe ser positivo: {self.risk_pct!r}")
        if self.max_risk_pct is not None and self.max_risk_pct <= 0:
            raise ValueError(f"max_risk_pct debe ser positivo si se declara: {self.max_risk_pct!r}")


def calculate_position_size(
    equity: float,
    stop_distance: float,
    config: SizingConfig,
) -> Tuple[float, bool]:
    """
    Devuelve (position_size, was_skipped).

    was_skipped=True cuando:
      - stop_distance <= 0 (senal invalida: no hay distancia de riesgo)
      - equity <= 0 (no hay capital sobre el que dimensionar)
      - config.max_risk_pct esta declarado Y el riesgo implicito del tamano
        MINIMO (config.min_size) lo supera -- es el UNICO criterio de salto
        por riesgo excesivo, y es opcional: si max_risk_pct es None (valor
        por defecto), esta comprobacion no se hace nunca y el minimo siempre
        se toma.

    No existe un salto por dar un tamano "demasiado pequeno": el tamano se
    redondea hacia abajo al incremento config.size_step con SUELO en
    config.min_size (el minimo se toma siempre, nunca se descarta por ser
    pequeno).
    """
    if stop_distance <= 0:
        return 0.0, True
    if equity <= 0:
        return 0.0, True

    if config.max_risk_pct is not None:
        min_size_risk_pct = (config.min_size * stop_distance) / equity
        if min_size_risk_pct > config.max_risk_pct:
            return 0.0, True

    risk_amount = equity * config.risk_pct
    raw_size = risk_amount / stop_distance

    # EPSILON_REDONDEO: sin el, un tamano que matematicamente es un multiplo
    # EXACTO de size_step pierde un paso entero en ~4% de los casos por como
    # el hardware representa los decimales en coma flotante (comprobado por
    # ejecucion: 24.283 de 599.997 casos construidos a proposito para ser
    # exactos, p.ej. 0.29/0.01 se representa como 28.999999999999996 y
    # math.floor() lo trunca a 28 en vez de 29). El epsilon es 7-8 ordenes de
    # magnitud menor que cualquier paso de tamano real, asi que no cambia
    # ningun redondeo hacia abajo genuino (12.4533.../0.01 sigue dando 1245,
    # no 1246), solo repara el caso limite.
    EPSILON_REDONDEO = 1e-9
    steps = math.floor(raw_size / config.size_step + EPSILON_REDONDEO)
    position_size = steps * config.size_step
    position_size = max(position_size, config.min_size)

    return position_size, False


def implied_risk_pct(equity: float, position_size: float, stop_distance: float) -> float:
    """Riesgo real, como fraccion del capital, para un tamano de posicion dado."""
    if equity <= 0:
        return float("inf")
    return (position_size * stop_distance) / equity
