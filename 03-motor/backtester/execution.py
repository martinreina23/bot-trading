#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de backtest -- tarea 01.02.02, pieza T2 del trasplante desde gb2 (D6=B,
00-direccion/WBS.md, seccion "Trasplante desde gb2 - criterios de
aceptacion"). Construido como informacion, no como copia en bloque de
`/home/server/projects/gold-bot-2/engine/core/execution.py`: la logica de
fills se ha vuelto a escribir aqui, adaptada a los datos que este proyecto
tiene de verdad (velas open/high/low/close de una sola serie de referencia,
sin bid/ask nativo -- ver la nota de diseno en costs.py).

REGLAS DE FILL (declaradas para que quien revise no tenga que adivinarlas):

  - Entrada LARGA:  fill = open de la PRIMERA vela con timestamp posterior a
                    la senal, mas la mitad del spread (precio de COMPRA).
  - Entrada CORTA:  fill = ese mismo open, menos la mitad del spread (precio
                    de VENTA).
  - Salida por STOP (largo): dispara cuando `low - half_spread <= stop_price`
                    (el precio de VENTA de la vela toca o cruza el stop; esta
                    condicion de DISPARO no se toca al reparar el sesgo de
                    abajo). Fill = min(stop_price, open) - half_spread: se
                    toma el PEOR de (stop_price, open de esta vela) en unidad
                    de REFERENCIA, y DESPUES se resta la mitad del spread
                    (lado de venta) -- exactamente el mismo segundo paso que
                    ya se aplicaba en tiempo/eod (close - half_spread). En un
                    cruce normal intra-vela (sin gap) el open esta por encima
                    del stop, asi que min() da stop_price y el fill exacto es
                    `stop_price - half_spread`. Solo cuando la vela ABRE ya
                    por debajo del stop (gap/salto de precio) el fill es peor,
                    a `open - half_spread` de esa misma vela -- NUNCA al open
                    de una vela posterior (cero look-ahead) y NUNCA mejor que
                    `stop_price - half_spread`.
  - Salida por STOP (corto): espejo exacto -- dispara cuando
                    `high + half_spread >= stop_price`; fill =
                    max(stop_price, open) + half_spread.
  - Salida por TARGET (largo): dispara cuando `high - half_spread >=
                    target_price`; fill = target_price - half_spread (limit
                    exacto en unidad de REFERENCIA, menos el lado de venta
                    del spread; sin deslizamiento adicional).
  - Salida por TARGET (corto): dispara cuando `low + half_spread <=
                    target_price`; fill = target_price + half_spread.
  - Salida por TIEMPO: si la senal declara `exit_time`, se sale en la PRIMERA
                    vela cuyo timestamp sea >= exit_time, al precio de cierre
                    del lado correspondiente (close-half_spread en largo,
                    close+half_spread en corto). Se comprueba ANTES que stop y
                    target en cada vela (mismo orden que gb2: la salida
                    programada por el propio criterio de la senal manda sobre
                    lo que pase esa misma vela).
  - Fin de datos sin salida: se cierra al close de la ultima vela disponible
                    (razon "eod"), mismo lado que la salida por tiempo.
  - Orden en la MISMA vela cuando stop y target podrian disparar los dos:
                    se comprueba el STOP antes que el TARGET (convencion
                    pesimista deliberada: asumir que el precio adverso llego
                    primero intra-vela es mas conservador que asumir lo
                    contrario, y evita sobre-acreditar operaciones).
  - La vela de ENTRADA nunca se explora para stop/target/tiempo: el rastreo
                    de salida empieza en la vela SIGUIENTE a la de entrada.
  - Comision: descuento EXPLICITO sobre el PnL, no se mezcla con el precio de
                    fill (igual que en costs.py).
  - Swap: se acumula sobre la posicion completa entre entry_time y exit_time
                    via costs.swap_cost(); una operacion intradia que no
                    cruza rollover devuelve 0.0 exacto.

DEFECTO CORREGIDO EL 03/08/2026 (rechazo de `critico-codigo`, reproducido por
el orquestador antes de mandarlo: regla 11 de CLAUDE.md): las reglas de STOP
y TARGET de arriba devolvian el fill SIN restar/sumar half_spread --
`min(stop_price, open - half_spread)` colapsaba a `stop_price` a secas en el
caso ordinario, y `target_price` se devolvia sin ajustar. Como time/eod SI
restaban half_spread, el resultado era un sesgo sistematico A FAVOR de la
estrategia: una salida por stop pagaba medio coste de ida y vuelta en vez del
coste completo, y una salida por target no pagaba nada del lado de salida.
Como stop/target son la salida NORMAL de cualquier estrategia real (time/eod
son la excepcion), casi toda operacion se beneficiaba del sesgo. Corregido
aplicando half_spread DESPUES de resolver el peor-de-los-dos, simetrico a
time/eod en los cuatro casos. Prueba de la simetria restaurada:
`verificar_motor.py`, PRUEBA 3; regresion permanente en
`tests/test_execution.py` (`test_stop_ordinario_aplica_half_spread_simetrico`,
`test_target_ordinario_aplica_half_spread_simetrico`,
`test_coste_de_spread_identico_salga_por_donde_salga`).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from .costs import CostModel, SwapConfig, swap_cost
from .sizing import SizingConfig, calculate_position_size

REQUIRED_BAR_COLUMNS = ("open", "high", "low", "close")
REQUIRED_SIGNAL_COLUMNS = ("timestamp", "direction", "stop_price")


@dataclass
class Trade:
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: int                     # 1 = largo, -1 = corto
    entry_price: float
    exit_price: float
    stop_price: float
    target_price: Optional[float]
    position_size: float
    commission_cost: float             # comision total de la operacion (ya multiplicada por el tamano)
    pnl_gross: float                   # (exit - entry) * direction * size -- ya incluye el spread embebido
    swap_total: float                  # positivo = credito, negativo = coste
    pnl_net: float                     # gross - commission_cost + swap_total
    stop_distance: float               # abs(entry_price - stop_price)
    pnl_r: float                       # pnl_net / (stop_distance * position_size)
    exit_reason: str                   # 'stop' | 'target' | 'time' | 'eod' | 'skipped'
    was_skipped: bool = False


@dataclass
class BacktestResult:
    trades: list[Trade]
    skipped_count: int
    equity_curve: pd.Series            # indexado por exit_time
    initial_equity: float


def _validate_bars(bars: pd.DataFrame) -> None:
    """
    HUECO DECLARADO, NO REPARADO (revision de critico-codigo, 03/08/2026):
    esta funcion NO comprueba la coherencia OHLC de cada vela (que
    high >= open, close, low y que low <= open, close, high). Un dato
    corrupto llegaria a _find_exit sin lanzar ningun error aqui.
    critico-codigo comprobo que el invariante del stop (regla 25 de
    CLAUDE.md: nunca ejecuta a mejor precio del disparado) se sostiene
    igual aunque la coherencia OHLC no se valide, asi que NO es motivo de
    rechazo de T2. Queda pendiente para cuando se construya el pipeline de
    datos limpios (Fase 04): validar la coherencia OHLC pertenece a esa
    pieza, no a este motor.
    """
    faltan = [c for c in REQUIRED_BAR_COLUMNS if c not in bars.columns]
    if faltan:
        raise ValueError(f"bars no tiene las columnas obligatorias {faltan}")
    if not isinstance(bars.index, pd.DatetimeIndex):
        raise ValueError("bars debe estar indexado por un DatetimeIndex")
    if bars.index.tz is None:
        raise ValueError("el indice de bars debe ser tz-aware (UTC)")
    if not bars.index.is_monotonic_increasing:
        raise ValueError("bars debe estar ordenado ascendentemente por timestamp")


def _validate_signals(signals: pd.DataFrame) -> None:
    faltan = [c for c in REQUIRED_SIGNAL_COLUMNS if c not in signals.columns]
    if faltan:
        raise ValueError(f"signals no tiene las columnas obligatorias {faltan}")


def run_backtest(
    signals: pd.DataFrame,
    bars: pd.DataFrame,
    cost_model: CostModel,
    sizing_config: SizingConfig,
    swap_config: Optional[SwapConfig] = None,
    initial_equity: float = 10_000.0,
) -> BacktestResult:
    """
    Backtest orientado a eventos sobre velas open/high/low/close.

    Args:
        signals:  DataFrame con columnas timestamp (vela TRAS la que se
                  decide entrar), direction (1/-1), stop_price (precio
                  absoluto), target_price (opcional, NaN = sin target fijo),
                  exit_time (opcional, NaT = sin limite de tiempo).
        bars:     DataFrame indexado por Timestamp UTC tz-aware, ordenado
                  ascendente, columnas open/high/low/close.
        cost_model:    ver costs.CostModel.
        sizing_config: ver sizing.SizingConfig.
        swap_config:   ver costs.SwapConfig. None = no se cobra ni acredita
                  financiacion nocturna (0.0 siempre).
        initial_equity: capital inicial en la misma unidad que el PnL.

    Nota: este motor NO impone una sola posicion abierta a la vez -- esa
    disciplina es responsabilidad de quien genera `signals` (igual
    separacion de responsabilidades que gb2: el motor ejecuta lo que se le
    da, no decide si dos senales se solapan).
    """
    _validate_bars(bars)
    _validate_signals(signals)

    if signals.empty:
        return BacktestResult([], 0, pd.Series(dtype=float), initial_equity)

    if len(bars) == 0:
        raise ValueError("bars no puede estar vacio si hay senales que procesar")

    signals = signals.sort_values("timestamp").reset_index(drop=True)

    bar_index = bars.index
    bar_index_ns = bar_index.as_unit("ns").asi8

    open_arr = bars["open"].to_numpy(dtype=float)
    high_arr = bars["high"].to_numpy(dtype=float)
    low_arr = bars["low"].to_numpy(dtype=float)
    close_arr = bars["close"].to_numpy(dtype=float)

    half_spread = cost_model.half_spread

    equity = initial_equity
    trades: list[Trade] = []
    skipped_count = 0
    equity_points: list[tuple[pd.Timestamp, float]] = [(bar_index[0], equity)]

    for sig in signals.itertuples(index=False):
        signal_time = sig.timestamp
        direction = int(sig.direction)
        if direction not in (1, -1):
            raise ValueError(f"direction debe ser 1 o -1; recibido: {direction!r}")
        stop_price = float(sig.stop_price)

        target_price = getattr(sig, "target_price", np.nan)
        if isinstance(target_price, float) and math.isnan(target_price):
            target_price = None
        elif pd.isnull(target_price):
            target_price = None
        else:
            target_price = float(target_price)

        exit_time_limit = getattr(sig, "exit_time", pd.NaT)
        if pd.isnull(exit_time_limit):
            exit_time_limit = None

        entry_mask = bar_index > signal_time
        if not entry_mask.any():
            continue
        entry_pos = int(np.argmax(entry_mask))
        entry_time = bar_index[entry_pos]

        if direction == 1:
            entry_price = open_arr[entry_pos] + half_spread
        else:
            entry_price = open_arr[entry_pos] - half_spread

        stop_distance = abs(entry_price - stop_price)

        position_size, skipped = calculate_position_size(equity, stop_distance, sizing_config)
        if skipped:
            skipped_count += 1
            trades.append(
                Trade(
                    entry_time=entry_time, exit_time=entry_time, direction=direction,
                    entry_price=entry_price, exit_price=entry_price,
                    stop_price=stop_price, target_price=target_price,
                    position_size=0.0, commission_cost=0.0,
                    pnl_gross=0.0, swap_total=0.0, pnl_net=0.0,
                    stop_distance=stop_distance, pnl_r=0.0,
                    exit_reason="skipped", was_skipped=True,
                )
            )
            continue

        exit_price, exit_time, exit_reason = _find_exit(
            open_arr, high_arr, low_arr, close_arr,
            bar_index, bar_index_ns,
            entry_pos + 1, direction, stop_price, target_price,
            exit_time_limit, half_spread,
        )

        gross_pnl = direction * (exit_price - entry_price) * position_size
        commission_cost = cost_model.commission_total * position_size
        if swap_config is not None:
            swap_total = swap_cost(direction, entry_time, exit_time, position_size, swap_config)
        else:
            swap_total = 0.0
        net_pnl = gross_pnl - commission_cost + swap_total
        pnl_r = net_pnl / (stop_distance * position_size) if stop_distance > 0 else 0.0

        equity += net_pnl
        equity_points.append((exit_time, equity))

        trades.append(
            Trade(
                entry_time=entry_time, exit_time=exit_time, direction=direction,
                entry_price=entry_price, exit_price=exit_price,
                stop_price=stop_price, target_price=target_price,
                position_size=position_size, commission_cost=commission_cost,
                pnl_gross=gross_pnl, swap_total=swap_total, pnl_net=net_pnl,
                stop_distance=stop_distance, pnl_r=pnl_r,
                exit_reason=exit_reason, was_skipped=False,
            )
        )

    equity_series = pd.Series(dict(equity_points), name="equity")

    return BacktestResult(
        trades=trades,
        skipped_count=skipped_count,
        equity_curve=equity_series,
        initial_equity=initial_equity,
    )


def _find_exit(
    open_arr: np.ndarray,
    high_arr: np.ndarray,
    low_arr: np.ndarray,
    close_arr: np.ndarray,
    bar_index: pd.DatetimeIndex,
    bar_index_ns: np.ndarray,
    start_pos: int,
    direction: int,
    stop_price: float,
    target_price: Optional[float],
    exit_time_limit: Optional[pd.Timestamp],
    half_spread: float,
) -> tuple[float, pd.Timestamp, str]:
    """
    Recorre las velas desde start_pos buscando el evento de salida.
    Devuelve (precio_fill, timestamp_salida, motivo).

    El orden de comprobacion en cada vela es SIEMPRE: tiempo -> stop ->
    target (ver docstring del modulo, seccion "Orden en la MISMA vela").
    """
    n = len(open_arr)
    exit_limit_ns = exit_time_limit.value if exit_time_limit is not None else None

    for pos in range(start_pos, n):
        if exit_limit_ns is not None and bar_index_ns[pos] >= exit_limit_ns:
            ts = bar_index[pos]
            fill = close_arr[pos] - half_spread if direction == 1 else close_arr[pos] + half_spread
            return fill, ts, "time"

        if direction == 1:
            sell_low = low_arr[pos] - half_spread
            if sell_low <= stop_price:
                # T2: "un stop nunca ejecuta a mejor precio del disparado".
                # El peor de (stop_price, open de ESTA vela) en unidad de
                # REFERENCIA -- nunca el open de una vela posterior -- y
                # DESPUES se resta half_spread, simetrico a como se calcula
                # la salida por tiempo/eod (close - half_spread). Sin este
                # segundo paso el fill quedaba SIN el lado de venta del
                # spread: rechazado por critico-codigo el 03/08/2026 (sesgo
                # sistematico a favor de la estrategia, reproducido con
                # CostModel(spread_total=2.0): cargaba 1.0 en vez de 2.0).
                fill = min(stop_price, open_arr[pos]) - half_spread
                return fill, bar_index[pos], "stop"
            if target_price is not None:
                sell_high = high_arr[pos] - half_spread
                if sell_high >= target_price:
                    # Mismo remedio: limit exacto en unidad de REFERENCIA,
                    # menos half_spread (lado de venta), nunca "a secas".
                    return target_price - half_spread, bar_index[pos], "target"
        else:
            buy_high = high_arr[pos] + half_spread
            if buy_high >= stop_price:
                fill = max(stop_price, open_arr[pos]) + half_spread
                return fill, bar_index[pos], "stop"
            if target_price is not None:
                buy_low = low_arr[pos] + half_spread
                if buy_low <= target_price:
                    return target_price + half_spread, bar_index[pos], "target"

    last_ts = bar_index[-1]
    fill = close_arr[-1] - half_spread if direction == 1 else close_arr[-1] + half_spread
    return fill, last_ts, "eod"
