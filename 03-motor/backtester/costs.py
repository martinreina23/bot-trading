#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 01.02.02 (pieza T2 del trasplante desde gb2, D6=B, 00-direccion/WBS.md,
seccion "Trasplante desde gb2 - criterios de aceptacion").

Coste de spread/comision y financiacion nocturna (swap), nativos del motor de
backtest -- no un descuento a posteriori sobre el resultado.

DECISION DE DISENO (no es un supuesto adivinado, es una eleccion de interfaz,
declarada aqui para que quien la revise no tenga que deducirla): este proyecto
NO tiene hoy, para ningun instrumento, velas con columnas bid/ask separadas
(comprobado por ejecucion: 02-datos/bruto/EURUSD/1m.csv.gz solo trae
open/high/low/close). gb2 si tenia tick bid/ask real de Dukascopy. Aqui el
coste de spread se APLICA sobre una unica serie de referencia (open/high/low/
close), partiendo el coste total ida y vuelta en dos mitades: la mitad se suma
al comprar y la mitad se resta al vender -- el mismo resultado economico que
"entrar al precio de compra, salir al precio de venta" (T2), reconstruido a
partir del numero que ya calcula 01-investigacion/mercados/coste_operar.md
(columna "COSTE TOTAL ida y vuelta"), sin que este modulo aplique NINGUN
divisor de pip: ese fue exactamente el fallo de la pieza T1 ("un divisor mal
puesto puso el oro a 17 $/onza", WBS.md, fila T1). Quien llama a este modulo
convierte pips/USD-por-onza a la unidad de precio de la serie ANTES de
construir el CostModel; este modulo no lo hace por su cuenta.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterator, Tuple

import pandas as pd
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class CostModel:
    """
    spread_total:      coste de spread, IDA Y VUELTA, en la unidad de precio
                        nativa del instrumento (USD/oz para oro, precio de
                        cotizacion para divisas ya con el divisor de pip
                        aplicado por quien llama, USD para cripto...).
    commission_total:   comision, IDA Y VUELTA, misma unidad. Se descuenta de
                        forma EXPLICITA del PnL; nunca se mezcla con el precio
                        de fill (igual separacion que costes_operar.md hace
                        entre "spread medio" y "comision convertida").
    """
    spread_total: float
    commission_total: float = 0.0

    def __post_init__(self) -> None:
        if self.spread_total < 0:
            raise ValueError(f"spread_total no puede ser negativo: {self.spread_total!r}")
        if self.commission_total < 0:
            raise ValueError(f"commission_total no puede ser negativo: {self.commission_total!r}")

    @property
    def half_spread(self) -> float:
        """Mitad del spread total: lo que se suma al comprar y se resta al vender."""
        return self.spread_total / 2.0

    @property
    def total_explicit_rt(self) -> float:
        """Spread + comision, ida y vuelta. Solo para informes/cordura, no se usa en el fill."""
        return self.spread_total + self.commission_total


@dataclass(frozen=True)
class SwapConfig:
    """
    Financiacion nocturna (swap / rollover), asimetrica entre largo y corto,
    con un dia de la semana que pesa TRIPLE para compensar el fin de semana
    sin mercado (convencion estandar de FX/CFD, verificada documentalmente en
    01-investigacion/mercados/coste_swap.md, advertencia 7: "miercoles...
    cobran tres veces la tarifa diaria" -- el mismo informe registra que XTB
    usa JUEVES para USDTRY, asi que el dia triple es CONFIGURABLE por
    instrumento/broker, nunca fijo para todos).

    long_rate_per_night / short_rate_per_night: unidad de precio por unidad
    de tamano de posicion, por noche. El signo ya codifica coste (negativo) o
    credito (positivo); swap_cost() no lo invierte.

    rollover_hour / rollover_tz: instante local del rollover. Por defecto
    17:00 America/New_York (la misma ancla horaria, DST-real via zoneinfo,
    que usa el corte de sesion de mercado ya fijado en el proyecto: nunca un
    offset UTC fijo, porque el offset NY<->UTC cambia con el horario de
    verano).

    triple_weekday: lunes=0 ... domingo=6 (convencion datetime.weekday()).
    Por defecto 2 = miercoles.

    zero_weight_weekdays: dias cuyo rollover no genera noche cobrada (por
    defecto sabado y domingo, sin mercado).
    """
    long_rate_per_night: float
    short_rate_per_night: float
    rollover_hour: int = 17
    rollover_tz: str = "America/New_York"
    triple_weekday: int = 2
    zero_weight_weekdays: Tuple[int, ...] = (5, 6)

    def __post_init__(self) -> None:
        if not (0 <= self.rollover_hour <= 23):
            raise ValueError(f"rollover_hour fuera de rango 0-23: {self.rollover_hour!r}")
        if not (0 <= self.triple_weekday <= 6):
            raise ValueError(f"triple_weekday fuera de rango 0-6: {self.triple_weekday!r}")


def _ensure_utc(ts) -> pd.Timestamp:
    """Normaliza a Timestamp tz-aware UTC. Un timestamp sin zona se asume UTC
    (misma convencion que el resto del proyecto: 02.02.01 corta a las 22:00
    UTC unico para todos los instrumentos)."""
    ts = pd.Timestamp(ts)
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def _weekday_weight(weekday: int, config: SwapConfig) -> int:
    if weekday in config.zero_weight_weekdays:
        return 0
    if weekday == config.triple_weekday:
        return 3
    return 1


def _rollovers_between(
    entry_time: pd.Timestamp, exit_time: pd.Timestamp, config: SwapConfig
) -> Iterator[int]:
    """
    Genera el peso de cada instante de rollover (config.rollover_hour en
    config.rollover_tz) que cae ESTRICTAMENTE entre entry_time y exit_time.
    Ninguno de los dos extremos cuenta: entrar o salir justo en el instante
    del rollover no carga ni acredita esa noche (no se "sostuvo" la posicion
    a traves de ella).

    La fecha calendario usada para el peso semanal es la fecha LOCAL (en
    rollover_tz) del propio instante de rollover, nunca derivada de un offset
    UTC fijo (zoneinfo aplica DST real).
    """
    if exit_time <= entry_time:
        return

    tz = ZoneInfo(config.rollover_tz)
    start_local_date = (entry_time.tz_convert(tz) - pd.Timedelta(days=1)).date()
    end_local_date = (exit_time.tz_convert(tz) + pd.Timedelta(days=1)).date()

    d = start_local_date
    while d <= end_local_date:
        rollover_local = datetime(
            d.year, d.month, d.day, config.rollover_hour, 0, 0, tzinfo=tz
        )
        rollover_utc = pd.Timestamp(rollover_local).tz_convert("UTC")
        if entry_time < rollover_utc < exit_time:
            yield _weekday_weight(d.weekday(), config)
        d += timedelta(days=1)


def swap_cost(
    direction: int,
    entry_time,
    exit_time,
    position_size: float,
    config: SwapConfig,
) -> float:
    """
    Coste (negativo) o credito (positivo) TOTAL de financiacion nocturna para
    una posicion, ya multiplicado por position_size, en unidad de precio.

    direction: 1 = largo, -1 = corto.
    Una posicion intradia que no cruza ningun rollover devuelve 0.0 exacto.
    """
    if direction == 1:
        rate = config.long_rate_per_night
    elif direction == -1:
        rate = config.short_rate_per_night
    else:
        raise ValueError(f"direction debe ser 1 (largo) o -1 (corto); recibido: {direction!r}")

    entry_time = _ensure_utc(entry_time)
    exit_time = _ensure_utc(exit_time)

    weighted_nights = sum(_rollovers_between(entry_time, exit_time, config))
    return weighted_nights * rate * position_size
