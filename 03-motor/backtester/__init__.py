"""
Motor de backtest -- tarea 01.02.02, pieza T2 del trasplante desde gb2
(D6=B, 00-direccion/WBS.md).

Solo T2: costes reales nativos (spread + comision), stops sin mejora de
precio, financiacion asimetrica con dia triple configurable, dimensionado
por riesgo. NO incluye metricas, Monte Carlo ni walk-forward: son piezas
distintas con su propia puerta (T3 en adelante, ver la tabla de la seccion
"Trasplante desde gb2" del WBS).
"""
from .costs import CostModel, SwapConfig, swap_cost
from .sizing import SizingConfig, calculate_position_size, implied_risk_pct
from .execution import Trade, BacktestResult, run_backtest

__all__ = [
    "CostModel",
    "SwapConfig",
    "swap_cost",
    "SizingConfig",
    "calculate_position_size",
    "implied_risk_pct",
    "Trade",
    "BacktestResult",
    "run_backtest",
]
