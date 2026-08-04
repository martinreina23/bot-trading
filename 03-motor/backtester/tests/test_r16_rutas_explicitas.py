#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-16 -- el motor no busca datos por su cuenta: solo lee las rutas que recibe como parametro
explicito. Sin ruta de datos, falla con error claro. Nunca lleva una ruta cableada al cajon
reservado."""
from __future__ import annotations

import inspect
import subprocess
from pathlib import Path

import pytest

from datos import cargar_1m, cargar_velas_4h

RAIZ_BACKTESTER = Path(__file__).resolve().parents[1]


def test_r16a_sin_parametro_de_datos_falla_explicito():
    """(a) Invocar el motor sin parametro de datos -> error explicito, no exploracion de
    directorios. `cargar_1m` y `cargar_velas_4h` exigen `ruta` como argumento posicional: llamarlas
    sin el produce un `TypeError` de Python en la propia firma, nunca una busqueda silenciosa."""
    with pytest.raises(TypeError):
        cargar_1m()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        cargar_velas_4h()  # type: ignore[call-arg]

    # Con una ruta que no existe: error explicito y propio (FormatoDatosError), no una exploracion.
    from datos import FormatoDatosError
    with pytest.raises(FormatoDatosError):
        cargar_1m(Path("/ruta/que/no/existe/en/ningun/sitio.csv.gz"))


def test_r16a_ninguna_funcion_del_motor_tiene_ruta_por_defecto():
    """Ninguna funcion publica de `datos.py` o `motor.py` que reciba una ruta de datos tiene un
    valor por defecto: siempre hay que pasarla."""
    for nombre_funcion in ("cargar_1m", "construir_velas_4h", "cargar_velas_4h"):
        import datos
        firma = inspect.signature(getattr(datos, nombre_funcion))
        primer_parametro = next(iter(firma.parameters.values()))
        assert primer_parametro.default is inspect.Parameter.empty, (
            f"{nombre_funcion} tiene un valor por defecto para su ruta de datos"
        )


def test_r16b_ninguna_mencion_a_reservado_fuera_de_comentarios():
    """(b) `grep -rn "reservado" <dir_motor>` -> 0 apariciones fuera de comentarios."""
    proc = subprocess.run(
        ["grep", "-rn", "reservado", str(RAIZ_BACKTESTER), "--include=*.py",
         "--exclude=test_r16_rutas_explicitas.py"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, f"'reservado' aparece en el motor:\n{proc.stdout}"
