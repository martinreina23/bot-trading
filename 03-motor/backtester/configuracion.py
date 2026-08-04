#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 04.03.07 (WBS) -- configuracion versionada del motor de backtest.

C-8 de la especificacion (`03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`): "Toda cifra de mercado
vive en configuracion versionada, nunca cableada en el codigo del motor (spread, comision, swaps,
apalancamiento)." Este fichero NO contiene ningun numero de mercado: solo define la forma de la
configuracion (dataclasses) y la funcion que la lee de `config_datos/*.json`, que si esta
versionado en git y es lo que cambia cuando 04.01.02 traiga precios reales de broker.

R-09/R-13: los campos `fuente` y `estado` son obligatorios en la config de instrumento -- de donde
sale cada cifra y si es PROVISIONAL, no una constante muda.

H-2 (especificacion, seccion 9): el apalancamiento no tiene valor por defecto -- sin broker no hay
cifra fiable. `ConfigCuenta.apalancamiento` es un campo obligatorio (sin default): quien construye
la config tiene que declararlo explicitamente, los tests le pasan un valor propio del test.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

RAIZ_MOTOR = Path(__file__).resolve().parent
CONFIG_DATOS = RAIZ_MOTOR / "config_datos"


class ConfigInvalidaError(Exception):
    """La config no trae los campos que exige R-09/R-13 (fuente, estado, rango medido)."""


def _a_decimal(valor) -> Decimal:
    """Convierte a Decimal via str() SIEMPRE (nunca Decimal(float) directo): evita arrastrar el
    ruido binario de un float ya parseado por json. Regla 14 de CLAUDE.md: el dato numerico se
    calcula sobre el valor bruto, no sobre una representacion ya deformada."""
    return Decimal(str(valor))


@dataclass(frozen=True)
class ConfigInstrumento:
    """Costes nativos de un instrumento (R-01, R-07, R-09, R-13). Todo en USD por onza."""

    instrumento: str
    spread: Decimal              # USD/oz, se paga una vez por ida y vuelta (C-6)
    comision: Decimal            # USD/oz, ida y vuelta, cargada al cierre
    swap_largo_anual: Decimal    # % anual, con signo (C-3): negativo = coste
    swap_corto_anual: Decimal    # % anual, con signo (C-3)
    fuente: str
    estado: str


@dataclass(frozen=True)
class ConfigCuenta:
    """Parametros de cuenta y dimensionado (R-04, R-10, D-19)."""

    capital_inicial: Decimal
    riesgo_por_operacion_pct: Decimal   # fraccion del capital INICIAL (D-19: "1% del capital inicial")
    apalancamiento: Decimal             # H-2: obligatorio, SIN valor por defecto en esta clase
    paso_lote: Decimal = Decimal("0.1")     # R-10
    lote_minimo: Decimal = Decimal("0.1")   # R-10

    @property
    def riesgo_por_operacion_usd(self) -> Decimal:
        return self.capital_inicial * self.riesgo_por_operacion_pct / Decimal("100")


def cargar_config_instrumento(ruta: Path) -> ConfigInstrumento:
    """Lee un fichero JSON versionado (`config_datos/*.json`) y construye la config. Cualquier
    numero de mercado sale de aqui, nunca de una constante en `motor.py` (C-8)."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ConfigInvalidaError(f"No existe el fichero de config: {ruta}")
    datos = json.loads(ruta.read_text(encoding="utf-8"))

    faltan = [c for c in ("instrumento", "spread", "comision", "swap_largo_anual",
                           "swap_corto_anual", "fuente", "estado") if c not in datos]
    if faltan:
        raise ConfigInvalidaError(
            f"Config incompleta en {ruta}: faltan los campos {faltan} "
            "(R-09/R-13 exigen fuente y estado declarados, no solo los numeros)."
        )

    return ConfigInstrumento(
        instrumento=str(datos["instrumento"]),
        spread=_a_decimal(datos["spread"]),
        comision=_a_decimal(datos["comision"]),
        swap_largo_anual=_a_decimal(datos["swap_largo_anual"]),
        swap_corto_anual=_a_decimal(datos["swap_corto_anual"]),
        fuente=str(datos["fuente"]),
        estado=str(datos["estado"]),
    )


def config_xauusd_defecto() -> ConfigInstrumento:
    """Config PROVISIONAL de XAUUSD (R-13): `config_datos/xauusd.json`, versionado en git."""
    return cargar_config_instrumento(CONFIG_DATOS / "xauusd.json")
