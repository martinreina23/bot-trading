#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 04.03.07 (WBS) -- carga de datos y remuestreo a 4h del motor de backtest.

R-12: el motor lee EXACTAMENTE el formato que escribe `guardar_serie` en
`03-motor/scripts/precios_mercado.py` -- CSV comprimido gzip, cabecera literal
`ts_utc,open,high,low,close`, timestamps ISO-8601 UTC, precios float USD/oz, lado BID. Un formato
distinto no se adapta en silencio: se rechaza con error explicito.

R-06(a)/R-08: el remuestreo a 4h se hace importando `remuestrear` (y `limpiar`) de
`precios_mercado.py`, nunca reimplementado aqui. Mismo patron de import que ya usa
`03-motor/scripts/correlaciones_mercado.py` (sys.path + `import precios_mercado as pm`): no se
inventa un segundo mecanismo de import para el mismo modulo.

R-16: este fichero NUNCA construye una ruta por su cuenta ni explora directorios. Toda ruta de
datos llega como parametro explicito de quien llama.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "03-motor" / "scripts"))
import precios_mercado as pm  # noqa: E402  (R-06a: reutiliza remuestrear/limpiar, no se duplica)

CABECERA_ESPERADA = ["ts_utc", "open", "high", "low", "close"]


class FormatoDatosError(Exception):
    """R-12: el fichero de entrada no tiene el formato exacto que escribe `guardar_serie`."""


def cargar_1m(ruta: Path) -> pd.DataFrame:
    """R-12: carga un CSV.gz con cabecera EXACTA `ts_utc,open,high,low,close`.

    No hay ruta por defecto (R-16): `ruta` es siempre un parametro explicito de quien llama. Si el
    fichero no existe o la cabecera no coincide letra por letra, falla con `FormatoDatosError` --
    nunca intenta adivinar ni renombrar columnas.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FormatoDatosError(f"No existe el fichero de datos: {ruta}")

    cabecera = list(pd.read_csv(ruta, compression="infer", nrows=0).columns)
    if cabecera != CABECERA_ESPERADA:
        raise FormatoDatosError(
            f"Formato de datos no reconocido en {ruta}: cabecera {cabecera!r}, "
            f"se esperaba exactamente {CABECERA_ESPERADA!r} (formato de `guardar_serie` en "
            "precios_mercado.py). El motor no adapta formatos distintos en silencio (R-12)."
        )

    df = pd.read_csv(ruta, compression="infer", parse_dates=["ts_utc"])
    df = df.set_index("ts_utc")
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")
    df.index.name = "ts_utc"

    df, _info_limpieza = pm.limpiar(df)  # R-06a: limpieza reutilizada, no reimplementada
    return df


def construir_velas_4h(
    df1m: pd.DataFrame,
    inicio: datetime | None = None,
    fin: datetime | None = None,
) -> pd.DataFrame:
    """R-06(a)/R-08: vela de 4h idéntica a la de 02.02.01/02.02.03 -- llama directamente a
    `remuestrear(df, "4h", inicio, fin)` de `precios_mercado.py`. El motor no reimplementa el
    metodo de remuestreo de pandas en ningun otro sitio (prueba R-06a)."""
    return pm.remuestrear(df1m, "4h", inicio, fin)


def cargar_velas_4h(
    ruta_1m: Path,
    inicio: datetime | None = None,
    fin: datetime | None = None,
) -> pd.DataFrame:
    """Atajo: carga el 1m crudo (R-12) y lo remuestrea a 4h (R-06a/R-08) en un solo paso."""
    df1m = cargar_1m(ruta_1m)
    return construir_velas_4h(df1m, inicio, fin)
