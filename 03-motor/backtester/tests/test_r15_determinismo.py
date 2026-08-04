#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-15 -- determinismo y registro que cuadra: misma entrada y misma config -> salida
bit-identica."""
from __future__ import annotations

import hashlib
import json
from decimal import Decimal

from conftest import D, cfg_cuenta_casos_lapiz, cfg_instrumento_casos_lapiz, estrategia_sonda

from motor import simular


def _serializar_resultado(resultado) -> str:
    """Serializacion determinista y completa del registro de salida (operaciones + serie de caja)
    para poder comparar por hash."""
    def _apunte(a):
        return {"ts": a.ts.isoformat(), "tipo": a.tipo, "importe": str(a.importe)}

    def _operacion(op):
        return {
            "direccion": op.direccion,
            "ts_senal": op.ts_senal.isoformat(),
            "ts_entrada": op.ts_entrada.isoformat(),
            "precio_entrada": str(op.precio_entrada),
            "onzas": str(op.onzas),
            "riesgo_nominal": str(op.riesgo_nominal),
            "nivel_stop": str(op.nivel_stop),
            "ts_salida": op.ts_salida.isoformat(),
            "precio_salida": str(op.precio_salida),
            "motivo_salida": op.motivo_salida,
            "apuntes": [_apunte(a) for a in op.apuntes],
        }

    payload = {
        "caja_inicial": str(resultado.caja_inicial),
        "caja_final": str(resultado.caja_final),
        "operaciones": [_operacion(op) for op in resultado.operaciones],
        "rechazadas": [
            {"ts_senal": r.ts_senal.isoformat() if r.ts_senal is not None else None,
             "direccion": r.direccion, "motivo": r.motivo}
            for r in resultado.rechazadas
        ],
        "serie_caja": [(ts.isoformat(), str(caja)) for ts, caja in resultado.serie_caja],
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def test_r15_dos_ejecuciones_de_cl1_hash_identico(velas_cl1):
    """Ejecutar dos veces CL-1 con la misma entrada y la misma config -> los dos ficheros de
    salida tienen hash identico (sha256sum)."""
    r1 = simular(velas_cl1, estrategia_sonda(D("55.00")),
                 cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
    r2 = simular(velas_cl1.copy(deep=True), estrategia_sonda(D("55.00")),
                 cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())

    s1 = _serializar_resultado(r1)
    s2 = _serializar_resultado(r2)

    h1 = hashlib.sha256(s1.encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(s2.encode("utf-8")).hexdigest()

    assert h1 == h2
    assert r1.caja_final == r2.caja_final == D("2014.55")


def test_r15_cuadre_es_r01c(velas_cl1, velas_cl2, velas_cl2b):
    """La asercion de cuadre es la R-01(c): caja_final - caja_inicial == suma de todos los
    apuntes de todas las operaciones, sin residuo."""
    for velas, distancia in ((velas_cl1, D("55.00")), (velas_cl2, D("100.00")), (velas_cl2b, D("100.00"))):
        resultado = simular(velas, estrategia_sonda(distancia),
                             cfg_instrumento_casos_lapiz(), cfg_cuenta_casos_lapiz())
        suma_apuntes = Decimal("0")
        for op in resultado.operaciones:
            for apunte in op.apuntes:
                suma_apuntes += apunte.importe
        assert resultado.caja_final - resultado.caja_inicial == suma_apuntes
