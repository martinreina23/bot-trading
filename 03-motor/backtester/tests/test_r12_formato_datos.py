#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-12 -- lectura del formato que produce `precios_mercado.py`: CSV comprimido gzip, cabecera
`ts_utc,open,high,low,close`, timestamps ISO-8601 UTC, precios float USD/oz, lado BID. El motor no
adapta en silencio formatos distintos: los rechaza con error."""
from __future__ import annotations

import gzip
from pathlib import Path

import pytest

from datos import FormatoDatosError, cargar_1m

RAIZ = Path(__file__).resolve().parents[3]
DATOS_XAUUSD_1M = RAIZ / "02-datos" / "bruto" / "XAUUSD" / "1m.csv.gz"


def _escribir_csv_gz(ruta: Path, contenido: str) -> None:
    with gzip.open(ruta, "wt", encoding="utf-8") as f:
        f.write(contenido)


def test_r12a_formato_sintetico_exacto(tmp_path):
    """(a) Fichero sintetico con el formato exacto; el motor lo carga y reproduce n de filas,
    primer y ultimo ts_utc."""
    ruta = tmp_path / "sintetico_1m.csv.gz"
    _escribir_csv_gz(ruta, (
        "ts_utc,open,high,low,close\n"
        "2026-01-05T00:00:00+00:00,3000.00,3001.00,2999.00,3000.50\n"
        "2026-01-05T00:01:00+00:00,3000.50,3002.00,3000.00,3001.00\n"
        "2026-01-05T00:02:00+00:00,3001.00,3003.00,3000.50,3002.00\n"
    ))

    df = cargar_1m(ruta)
    assert len(df) == 3
    assert str(df.index[0]) == "2026-01-05 00:00:00+00:00"
    assert str(df.index[-1]) == "2026-01-05 00:02:00+00:00"


def test_r12b_cabecera_distinta_falla_explicito(tmp_path):
    """(b) El mismo fichero con la cabecera `timestamp,...` en vez de `ts_utc` -> el motor falla
    con error explicito de formato, no carga."""
    ruta = tmp_path / "cabecera_mala.csv.gz"
    _escribir_csv_gz(ruta, (
        "timestamp,open,high,low,close\n"
        "2026-01-05T00:00:00+00:00,3000.00,3001.00,2999.00,3000.50\n"
    ))
    with pytest.raises(FormatoDatosError):
        cargar_1m(ruta)


def test_r12c_fichero_real_carga_y_pasa_cordura():
    """(c) Sobre el fichero real 02-datos/bruto/XAUUSD/1m.csv.gz: carga sin error y todos los
    precios caen en el rango de cordura del oro (500-6000 USD/oz), el mismo RANGO_CORDURA de
    precios_mercado.py."""
    if not DATOS_XAUUSD_1M.exists():
        pytest.skip(f"no existe {DATOS_XAUUSD_1M} en este entorno")

    import sys
    sys.path.insert(0, str(RAIZ / "03-motor" / "scripts"))
    import precios_mercado as pm

    df = cargar_1m(DATOS_XAUUSD_1M)
    assert len(df) > 0
    lo, hi = pm.RANGO_CORDURA["XAUUSD"]
    for col in ("open", "high", "low", "close"):
        assert df[col].min() >= lo
        assert df[col].max() <= hi
