#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculo de apoyo dentro del alcance de la tarea 01.01.02 del WBS (aprobar los
criterios de la puerta G1). NO es una tarea nueva del WBS.

Convierte el coste relativo (tarea 02.02.02, ya cerrado) en:
  1) velas disponibles al año, contadas sobre los datos realmente descargados;
  2) arrastre de coste anual sobre el capital, con un modelo de parametros
     EXPLICITOS (riesgo por operacion, stop en ATR, tasa de actividad);
  3) borde bruto minimo que tiene que capturar la estrategia por operacion
     solo para cubrir el coste de entrar y salir;
  4) a partir de cuantos dias de posicion mantenida el coste de mantener
     (swap) supera al coste de entrar y salir, por broker y direccion;
  5) sensibilidad del arrastre anual a un deslizamiento no medido (1.25x,
     1.5x, 2x del coste), declarado como analisis, no como dato.

INSUMOS, YA CERRADOS Y VERIFICADOS. NO SE RECALCULAN, SOLO SE LEEN:
  - 04-resultados/coste_relativo_15m_1h_4h.json  (tarea 02.02.02)
  - 04-resultados/atr_15m_1h_4h.json              (tarea 02.02.01)
  - 01-investigacion/mercados/coste_operar.md     (tarea 02.01.02)
  - 01-investigacion/mercados/coste_swap.md       (tarea 02.02.05)

Este script SOLO divide y multiplica sobre esos cuatro insumos (mas la fecha
de hoy, irrelevante para el calculo). No descarga nada, no toca
02-datos/reservado (no lo lee, no lo lista, no lo referencia).

Reutiliza sin duplicar: no reimplementa el calculo de ATR ni el de coste
relativo; los lee tal cual de sus JSON de salida (regla 14 de CLAUDE.md: el
dato numerico de origen ya esta calculado sobre datos brutos en 02.02.01 y
02.02.02; este script hace aritmetica de segundo piso sobre esos numeros
cerrados, declarada como tal).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ATR_JSON = RAIZ / "04-resultados" / "atr_15m_1h_4h.json"
COSTE_RELATIVO_JSON = RAIZ / "04-resultados" / "coste_relativo_15m_1h_4h.json"
SALIDA_JSON = RAIZ / "04-resultados" / "arrastre_coste_anual.json"

VELAS = ["15min", "1h", "4h"]
ANCHO_MIN = {"15min": 15, "1h": 60, "4h": 240}
INSTRUMENTOS_CRIPTO = ("BTCUSD", "ETHUSD")
VELA_ESCENARIO_A_CLAVE = {"media": "ratios", "mediana": "ratios_mediana", "p10": "ratios_p10", "p90": "ratios_p90"}

# ---------------------------------------------------------------------------
# Parametros del modelo — EXPLICITOS, ninguno escondido (punto 2 del encargo)
# ---------------------------------------------------------------------------
RIESGOS_POR_OPERACION = [0.005, 0.01, 0.02]          # fraccion del capital
STOPS_EN_ATR = [0.5, 1.0, 2.0]                        # distancia del stop en ATR14
TASAS_ACTIVIDAD = [0.02, 0.05, 0.10]                  # fraccion de velas con operacion
ESCENARIO_CENTRAL = {"riesgo_por_operacion": 0.01, "stop_en_atr": 1.0, "tasa_actividad": 0.05, "vela_escenario": "mediana"}
FACTOR_ANUALIZACION_DIAS = 365
MULTIPLICADORES_DESLIZAMIENTO = [1.0, 1.25, 1.5, 2.0]  # NINGUNO tiene fuente: declarado

MOTIVO_HUECO_VELAS_ANO_CRIPTO = (
    "Kraken (endpoint publico /OHLC, ver 04-resultados/atr_15m_1h_4h.json campo "
    "'motivo_no_reproducible') solo entrega una ventana deslizante de ~720 velas "
    "CERRADAS por intervalo (7,4 dias en 15m, 30 dias en 1h, 120 dias en 4h), muy "
    "por debajo de un año y marcada reproducible=false. Extrapolar esa ventana a "
    "un año multiplicaria por un factor grande (~49x en 15m, ~12x en 1h, ~3x en 4h) "
    "una muestra en la que ademas el activo cotiza 24/7 sin cierres: el ritmo "
    "observado en la ventana corta coincide por construccion con la aritmetica "
    "teorica 24x365 que el encargo prohibe usar como estimacion (no distingue "
    "cobertura real de aritmetica de calendario). Se declara HUECO, no se rellena "
    "(instruccion explicita del encargo). Todo lo que dependa de velas/año para "
    "BTCUSD/ETHUSD (arrastre anual, sensibilidad al deslizamiento) hereda este hueco."
)

# ---------------------------------------------------------------------------
# Tabla de coste de mantener (swap), transcrita literalmente de
# 01-investigacion/mercados/coste_swap.md, seccion "Tabla — 8 instrumentos x 3
# brokers x (largo/corto)" (tarea 02.02.05, cerrada). Unidad: % anual publicado
# por cada broker o calculado por el propio informe (XTB, %diario x 365,
# metodo declarado en su seccion "Metodo"). NO se recalcula aqui: se copia.
# None  = "sin dato fiable" (hueco declarado en el propio 02.02.05).
# "no_aplica_spot" = instrumento distinto (spot, no CFD), no comparable.
# ---------------------------------------------------------------------------
SWAP_PCT_ANUAL = {
    "EURUSD": {
        "OANDA": {"largo": -2.41, "corto": 0.44},
        "XTB": {"largo": -3.01, "corto": -0.04},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "GBPUSD": {
        "OANDA": {"largo": -0.88, "corto": -1.05},
        "XTB": {"largo": -1.48, "corto": -1.54},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "USDJPY": {
        "OANDA": {"largo": 1.61, "corto": -3.52},
        "XTB": {"largo": 0.68, "corto": -4.73},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "AUDUSD": {
        "OANDA": {"largo": -0.28, "corto": -1.63},
        "XTB": {"largo": -1.34, "corto": -2.68},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "USDCHF": {
        "OANDA": {"largo": 2.60, "corto": -4.50},
        "XTB": {"largo": 2.22, "corto": -5.26},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "XAUUSD": {
        "OANDA": {"largo": -6.64, "corto": 0.64},
        "XTB": {"largo": -8.16, "corto": -0.76},
        "Pepperstone": {"largo": None, "corto": None},
    },
    "BTCUSD": {
        "OANDA": {"largo": -33.64, "corto": -26.36},
        "XTB": {"largo": "no_aplica_spot", "corto": "no_aplica_spot"},
        "Pepperstone": {"largo": -22.5, "corto": 7.5},
    },
    "ETHUSD": {
        "OANDA": {"largo": -33.64, "corto": -26.36},
        "XTB": {"largo": "no_aplica_spot", "corto": "no_aplica_spot"},
        "Pepperstone": {"largo": None, "corto": None},
    },
}

# ---------------------------------------------------------------------------
# Convencion de "lote" y valor de pip en USD, transcrita literalmente de
# 01-investigacion/mercados/coste_operar.md (tarea 02.01.02). Necesaria SOLO
# para el punto 4 (comparar contra el nocional de 100.000 USD que usa
# coste_swap.md). Los valores 10 / 6,667 / 12,50 USD-por-pip-por-lote estan
# YA CALCULADOS y citados en coste_operar.md (division comision/pips ya hecha
# por ese documento); aqui solo se reutilizan, no se recalculan.
#   - EURUSD, GBPUSD, AUDUSD: pip valor 10 USD/lote (coste_operar.md, filas
#     EURUSD/GBPUSD/AUDUSD, "0,7 pip - mismo calculo que EURUSD").
#   - USDJPY: pip valor ~6,667 USD/lote (comision 7 USD / 1,05 pips).
#   - USDCHF: pip valor ~12,50 USD/lote (comision 7 USD / 0,56 pips).
#   - XAUUSD: 1 lote = 100 oz (coste_operar.md, "comision 7 USD por lote de
#     100 oz").
#   - BTCUSD, ETHUSD: coste_operar.md da el coste YA en USD de precio directo
#     (mismo criterio que usa coste_relativo.py, funcion coste_en_unidad_atr:
#     "xauusd/cripto: ya esta en USD de precio, misma unidad que el ATR crudo
#     del JSON"). Para poner ese coste en base 100.000 USD nocional (la base
#     que usa coste_swap.md) se declara aqui, como SUPUESTO EXPLICITO propio
#     de este calculo (no de un insumo cerrado): "1 lote = 1 unidad del
#     activo" (analogo a como XAUUSD usa 1 oz como unidad de precio). Sin
#     esta convencion no se puede comparar swap (dado en % nocional) contra
#     spread (dado por unidad de precio) en ninguna base comun.
# ---------------------------------------------------------------------------
PIP_VALUE_USD_POR_LOTE = {"EURUSD": 10.0, "GBPUSD": 10.0, "AUDUSD": 10.0, "USDJPY": 7.0 / 1.05, "USDCHF": 7.0 / 0.56}
LOTE_BASE_USD_DIRECTO = {"USDJPY", "USDCHF"}  # base=USD: 1 lote = 100.000 USD nocional exacto, sin precio
UNIDADES_POR_LOTE_XAUUSD = 100.0  # 100 oz por lote (coste_operar.md)

# Coste total ida y vuelta, transcrito literalmente de coste_operar.md,
# columna "COSTE TOTAL ida y vuelta" (identico a COSTES de coste_relativo.py,
# se repite aqui para no importar un script de otra tarea y no crear
# acoplamiento; los valores son los mismos, verificables por grep cruzado).
COSTE_TOTAL_IDA_VUELTA = {
    "EURUSD": {"unico": 0.8},
    "GBPUSD": {"unico": 0.82},
    "USDJPY": {"unico": 1.16},
    "AUDUSD": {"unico": 0.85},
    "USDCHF": {"unico": 0.73},
    "XAUUSD": {"unico": 0.26},
    "BTCUSD": {"feb-2025": 20.22, "abr-2026": 36.90},
    "ETHUSD": {"feb-2025": 3.01, "abr-2026": 7.04},
}


def cargar_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1) VELAS DISPONIBLES AL AÑO — contadas sobre datos realmente descargados
# ---------------------------------------------------------------------------
def calcular_velas_disponibles_ano(atr_data: dict) -> dict:
    resultado = {}
    for instr, datos in atr_data["instrumentos"].items():
        resultado[instr] = {}
        for vela in VELAS:
            v = datos["velas"][vela]
            if instr in INSTRUMENTOS_CRIPTO:
                resultado[instr][vela] = {
                    "hueco": True,
                    "motivo": MOTIVO_HUECO_VELAS_ANO_CRIPTO,
                    "n_velas_ventana_real": v["n_velas"],
                    "desde_utc_ventana_real": v["desde_utc"],
                    "hasta_utc_ventana_real": v["hasta_utc"],
                    "reproducible": v.get("reproducible", False),
                }
                continue
            desde = datetime.fromisoformat(v["desde_utc"])
            hasta = datetime.fromisoformat(v["hasta_utc"])
            ancho = timedelta(minutes=ANCHO_MIN[vela])
            span_dias = (hasta + ancho - desde).total_seconds() / 86400.0
            velas_dia = v["n_velas"] / span_dias
            velas_ano = velas_dia * FACTOR_ANUALIZACION_DIAS
            resultado[instr][vela] = {
                "hueco": False,
                "n_velas_ventana_real": v["n_velas"],
                "desde_utc": v["desde_utc"],
                "hasta_utc": v["hasta_utc"],
                "span_dias_ventana_real": round(span_dias, 3),
                "cobertura_ventana_mayor_o_igual_365_dias": span_dias >= 365,
                "velas_por_dia_real": velas_dia,
                "factor_anualizacion_dias": FACTOR_ANUALIZACION_DIAS,
                "velas_ano": velas_ano,
                "reproducible": v.get("reproducible", True),
            }
    return resultado


# ---------------------------------------------------------------------------
# 2) ARRASTRE DE COSTE ANUAL
# ---------------------------------------------------------------------------
def extraer_costes_relativos(coste_rel_data: dict, instr: str, vela: str, vela_escenario: str) -> dict:
    """Devuelve {fuente: coste_relativo_pct} para el instr/vela/escenario dado."""
    clave = VELA_ESCENARIO_A_CLAVE[vela_escenario]
    bloque = coste_rel_data["instrumentos"][instr]["velas"][vela][clave]
    return {fuente: datos["coste_relativo_pct"] for fuente, datos in bloque.items()}


def coste_por_operacion_frac_capital(costo_atr_frac: float, riesgo: float, stop_en_atr: float) -> float:
    return riesgo * (costo_atr_frac / stop_en_atr)


def arrastre_anual_aditivo(velas_ano: float, tasa_actividad: float, coste_op_frac: float) -> tuple[float, float]:
    operaciones_ano = velas_ano * tasa_actividad
    arrastre_frac = operaciones_ano * coste_op_frac
    return operaciones_ano, arrastre_frac


def arrastre_anual_compuesto(operaciones_ano: float, coste_op_frac: float) -> float:
    """OBJECION del constructor (declarada en el informe, no aplicada por
    defecto): la formula pedida por el encargo suma el coste de cada
    operacion sobre una base fija (aditiva), lo que SOBREESTIMA el arrastre
    real si el coste se paga sobre capital que ya se redujo por costes
    previos (base decreciente, interes compuesto de una perdida). La formula
    compuesta es arrastre = 1 - (1 - coste_por_operacion)^operaciones_año.
    Con coste_por_operacion >= 1 (mas del 100% del capital en una operacion,
    posible en escenarios extremos de esta malla) se satura en 100%."""
    c = min(max(coste_op_frac, 0.0), 1.0)
    return 1.0 - (1.0 - c) ** operaciones_ano


def calcular_arrastre_anual(coste_rel_data: dict, velas_ano_data: dict) -> dict:
    resultado = {}
    for instr in COSTE_TOTAL_IDA_VUELTA:
        resultado[instr] = {}
        for vela in VELAS:
            va = velas_ano_data[instr][vela]
            resultado[instr][vela] = {}
            if va["hueco"]:
                resultado[instr][vela]["hueco"] = True
                resultado[instr][vela]["motivo"] = MOTIVO_HUECO_VELAS_ANO_CRIPTO
                continue
            resultado[instr][vela]["hueco"] = False
            resultado[instr][vela]["reproducible"] = va["reproducible"]
            resultado[instr][vela]["escenarios_vela"] = {}
            for vela_escenario in VELA_ESCENARIO_A_CLAVE:
                costes_por_fuente = extraer_costes_relativos(coste_rel_data, instr, vela, vela_escenario)
                resultado[instr][vela]["escenarios_vela"][vela_escenario] = {}
                for fuente, coste_relativo_pct in costes_por_fuente.items():
                    costo_atr_frac = coste_relativo_pct / 100.0
                    malla = {}
                    for riesgo in RIESGOS_POR_OPERACION:
                        for stop in STOPS_EN_ATR:
                            coste_op_frac = coste_por_operacion_frac_capital(costo_atr_frac, riesgo, stop)
                            for actividad in TASAS_ACTIVIDAD:
                                operaciones_ano, arrastre_frac = arrastre_anual_aditivo(
                                    va["velas_ano"], actividad, coste_op_frac
                                )
                                arrastre_compuesto_frac = arrastre_anual_compuesto(operaciones_ano, coste_op_frac)
                                clave = f"riesgo_{riesgo}__stop_{stop}__actividad_{actividad}"
                                malla[clave] = {
                                    "riesgo_por_operacion": riesgo,
                                    "stop_en_atr": stop,
                                    "tasa_actividad": actividad,
                                    "operaciones_ano": operaciones_ano,
                                    "coste_por_operacion_pct_capital": coste_op_frac * 100.0,
                                    "arrastre_anual_pct_aditivo": arrastre_frac * 100.0,
                                    "arrastre_anual_pct_compuesto_objecion": arrastre_compuesto_frac * 100.0,
                                }
                    resultado[instr][vela]["escenarios_vela"][vela_escenario][fuente] = {
                        "coste_relativo_pct": coste_relativo_pct,
                        "malla_riesgo_stop_actividad": malla,
                    }
    return resultado


# ---------------------------------------------------------------------------
# 3) BORDE BRUTO MINIMO POR OPERACION — relectura directa del coste relativo
# ---------------------------------------------------------------------------
def calcular_borde_bruto_minimo(coste_rel_data: dict) -> dict:
    resultado = {}
    for instr in COSTE_TOTAL_IDA_VUELTA:
        resultado[instr] = {}
        for vela in VELAS:
            resultado[instr][vela] = {}
            for vela_escenario in VELA_ESCENARIO_A_CLAVE:
                costes_por_fuente = extraer_costes_relativos(coste_rel_data, instr, vela, vela_escenario)
                resultado[instr][vela][vela_escenario] = {
                    fuente: {
                        "coste_relativo_pct": pct,
                        "borde_bruto_minimo_pct_del_atr": pct,
                        "frase": (
                            f"Para cubrir solo el coste de entrar y salir, la estrategia debe "
                            f"capturar al menos el {pct:.2f}% del ATR14 de la vela {vela} de "
                            f"{instr} en cada operacion (escenario de vela: {vela_escenario}, "
                            f"fuente de coste: {fuente})."
                        ),
                    }
                    for fuente, pct in costes_por_fuente.items()
                }
    return resultado


# ---------------------------------------------------------------------------
# 4) CUANDO EL SWAP SUPERA AL SPREAD — por broker, largo y corto
# ---------------------------------------------------------------------------
def notional_por_lote_usd(instr: str, precio_medio_15m: float) -> float:
    if instr in LOTE_BASE_USD_DIRECTO:
        return 100_000.0
    if instr == "XAUUSD":
        return UNIDADES_POR_LOTE_XAUUSD * precio_medio_15m
    if instr in INSTRUMENTOS_CRIPTO:
        return 1.0 * precio_medio_15m  # 1 lote = 1 unidad, supuesto declarado
    # EURUSD, GBPUSD, AUDUSD: lote = 100.000 unidades de la divisa BASE (no USD)
    return 100_000.0 * precio_medio_15m


def coste_usd_por_lote(instr: str, fuente: str) -> float:
    coste_original = COSTE_TOTAL_IDA_VUELTA[instr][fuente]
    if instr in PIP_VALUE_USD_POR_LOTE:
        return coste_original * PIP_VALUE_USD_POR_LOTE[instr]
    if instr == "XAUUSD":
        return coste_original * UNIDADES_POR_LOTE_XAUUSD
    # BTCUSD, ETHUSD: coste_original ya esta en USD directos (1 lote = 1 unidad)
    return coste_original


def calcular_swap_vs_spread(atr_data: dict) -> dict:
    resultado = {}
    for instr in COSTE_TOTAL_IDA_VUELTA:
        precio_medio_15m = atr_data["instrumentos"][instr]["velas"]["15min"]["precio_medio"]
        notional = notional_por_lote_usd(instr, precio_medio_15m)
        resultado[instr] = {
            "precio_referencia_usado": precio_medio_15m,
            "fuente_precio_referencia": "04-resultados/atr_15m_1h_4h.json, instrumentos." + instr + ".velas.15min.precio_medio",
            "notional_por_lote_usd": notional,
            "brokers": {},
        }
        if instr in INSTRUMENTOS_CRIPTO:
            resultado[instr]["aviso_precio_referencia"] = (
                "Para BTCUSD/ETHUSD este precio procede de la ventana Kraken NO reproducible "
                "(reproducible=false en atr_15m_1h_4h.json) y ademas no coincide temporalmente "
                "con ninguna de las dos fechas del coste (feb-2025, abr-2026): es una limitacion "
                "heredada, ya presente en coste_relativo_15m_1h_4h.json, que aqui se propaga "
                "explicitamente en vez de disimularse."
            )
        for fuente, coste_original in COSTE_TOTAL_IDA_VUELTA[instr].items():
            coste_usd = coste_usd_por_lote(instr, fuente)
            coste_pct_notional = coste_usd / notional * 100.0
            resultado[instr]["brokers"].setdefault(fuente, {})
            for broker, direcciones in SWAP_PCT_ANUAL[instr].items():
                fila_broker = resultado[instr]["brokers"][fuente].setdefault(broker, {})
                for direccion, swap_pct_anual in direcciones.items():
                    if swap_pct_anual is None:
                        fila_broker[direccion] = {"estado": "sin_dato_fiable", "motivo": "coste_swap.md declara este broker/instrumento sin dato fiable"}
                        continue
                    if swap_pct_anual == "no_aplica_spot":
                        fila_broker[direccion] = {"estado": "no_aplica", "motivo": "coste_swap.md: este broker ofrece el instrumento como spot, no como CFD; no tiene swap y no es comparable"}
                        continue
                    swap_pct_dia = swap_pct_anual / 365.0
                    if swap_pct_dia >= 0:
                        fila_broker[direccion] = {
                            "estado": "credito",
                            "swap_pct_anual": swap_pct_anual,
                            "swap_pct_dia": swap_pct_dia,
                            "motivo": "swap positivo = credito para el cliente; nunca 'supera' un coste porque no es un coste",
                        }
                        continue
                    dias_breakeven = coste_pct_notional / abs(swap_pct_dia)
                    fila_broker[direccion] = {
                        "estado": "coste",
                        "swap_pct_anual": swap_pct_anual,
                        "swap_pct_dia": swap_pct_dia,
                        "coste_entrada_salida_pct_notional": coste_pct_notional,
                        "dias_hasta_que_swap_supera_spread": dias_breakeven,
                    }
    return resultado


# ---------------------------------------------------------------------------
# 5) SENSIBILIDAD AL DESLIZAMIENTO — escenario central de riesgo/stop/actividad
# ---------------------------------------------------------------------------
def calcular_sensibilidad_deslizamiento(coste_rel_data: dict, velas_ano_data: dict) -> dict:
    resultado = {}
    riesgo = ESCENARIO_CENTRAL["riesgo_por_operacion"]
    stop = ESCENARIO_CENTRAL["stop_en_atr"]
    actividad = ESCENARIO_CENTRAL["tasa_actividad"]
    for instr in COSTE_TOTAL_IDA_VUELTA:
        resultado[instr] = {}
        for vela in VELAS:
            va = velas_ano_data[instr][vela]
            resultado[instr][vela] = {}
            if va["hueco"]:
                resultado[instr][vela]["hueco"] = True
                resultado[instr][vela]["motivo"] = MOTIVO_HUECO_VELAS_ANO_CRIPTO
                continue
            resultado[instr][vela]["hueco"] = False
            resultado[instr][vela]["escenarios_vela"] = {}
            for vela_escenario in VELA_ESCENARIO_A_CLAVE:
                costes_por_fuente = extraer_costes_relativos(coste_rel_data, instr, vela, vela_escenario)
                resultado[instr][vela]["escenarios_vela"][vela_escenario] = {}
                for fuente, coste_relativo_pct in costes_por_fuente.items():
                    por_multiplicador = {}
                    for mult in MULTIPLICADORES_DESLIZAMIENTO:
                        costo_atr_frac = (coste_relativo_pct * mult) / 100.0
                        coste_op_frac = coste_por_operacion_frac_capital(costo_atr_frac, riesgo, stop)
                        operaciones_ano, arrastre_frac = arrastre_anual_aditivo(va["velas_ano"], actividad, coste_op_frac)
                        por_multiplicador[str(mult)] = {
                            "coste_relativo_pct_ajustado": coste_relativo_pct * mult,
                            "arrastre_anual_pct_aditivo": arrastre_frac * 100.0,
                        }
                    resultado[instr][vela]["escenarios_vela"][vela_escenario][fuente] = {
                        "coste_relativo_pct_base": coste_relativo_pct,
                        "por_multiplicador": por_multiplicador,
                        "aviso": "ninguno de los multiplicadores (1.25x, 1.5x, 2x) tiene fuente: es un analisis de sensibilidad declarado, no un dato medido",
                    }
    return resultado


# ---------------------------------------------------------------------------
# PRUEBA DE CORDURA OBLIGATORIA: a igual instrumento y tasa_actividad, el
# arrastre anual a 15m debe ser VARIAS VECES mayor que a 4h (mas velas y
# mayor coste relativo). Umbral: al menos 3x (declarado aqui, es el criterio
# de "varias veces" del encargo).
# ---------------------------------------------------------------------------
UMBRAL_CORDURA_MULTIPLICADOR = 3.0


def prueba_cordura_15m_vs_4h(arrastre_data: dict) -> dict:
    filas = []
    errores = []
    for instr, por_vela in arrastre_data.items():
        if por_vela["15min"].get("hueco") or por_vela["4h"].get("hueco"):
            filas.append({"instrumento": instr, "estado": "excluido_por_hueco"})
            continue
        vela_escenario = ESCENARIO_CENTRAL["vela_escenario"]
        clave_malla = (
            f"riesgo_{ESCENARIO_CENTRAL['riesgo_por_operacion']}__"
            f"stop_{ESCENARIO_CENTRAL['stop_en_atr']}__"
            f"actividad_{ESCENARIO_CENTRAL['tasa_actividad']}"
        )
        fuentes_15m = por_vela["15min"]["escenarios_vela"][vela_escenario]
        fuentes_4h = por_vela["4h"]["escenarios_vela"][vela_escenario]
        for fuente in fuentes_15m:
            a15 = fuentes_15m[fuente]["malla_riesgo_stop_actividad"][clave_malla]["arrastre_anual_pct_aditivo"]
            a4h = fuentes_4h[fuente]["malla_riesgo_stop_actividad"][clave_malla]["arrastre_anual_pct_aditivo"]
            multiplicador = a15 / a4h if a4h > 0 else float("inf")
            ok = multiplicador >= UMBRAL_CORDURA_MULTIPLICADOR
            filas.append({
                "instrumento": instr, "fuente_coste": fuente,
                "arrastre_15m_pct": a15, "arrastre_4h_pct": a4h,
                "multiplicador_15m_vs_4h": multiplicador, "ok": ok,
            })
            if not ok:
                errores.append(f"{instr} ({fuente}): 15m={a15:.4f}% vs 4h={a4h:.4f}% -> x{multiplicador:.2f} < umbral x{UMBRAL_CORDURA_MULTIPLICADOR}")
    return {"umbral_multiplicador": UMBRAL_CORDURA_MULTIPLICADOR, "filas": filas, "ok": len(errores) == 0, "errores": errores}


def main() -> None:
    atr_data = cargar_json(ATR_JSON)
    coste_rel_data = cargar_json(COSTE_RELATIVO_JSON)

    velas_ano_data = calcular_velas_disponibles_ano(atr_data)
    arrastre_data = calcular_arrastre_anual(coste_rel_data, velas_ano_data)
    borde_minimo_data = calcular_borde_bruto_minimo(coste_rel_data)
    swap_vs_spread_data = calcular_swap_vs_spread(atr_data)
    sensibilidad_data = calcular_sensibilidad_deslizamiento(coste_rel_data, velas_ano_data)
    cordura = prueba_cordura_15m_vs_4h(arrastre_data)

    resultado = {
        "generado_desde": {
            "coste_relativo": "04-resultados/coste_relativo_15m_1h_4h.json (02.02.02, NO recalculado)",
            "atr": "04-resultados/atr_15m_1h_4h.json (02.02.01, NO recalculado)",
            "coste_operar": "01-investigacion/mercados/coste_operar.md (02.01.02, NO recalculado)",
            "coste_swap": "01-investigacion/mercados/coste_swap.md (02.02.05, NO recalculado)",
        },
        "contexto_wbs": "Calculo de apoyo dentro del alcance de 01.01.02 (Aprobar criterios de la puerta G1). No es una tarea nueva del WBS.",
        "supuestos_declarados": {
            "riesgo_por_operacion_frac_capital": RIESGOS_POR_OPERACION,
            "stop_en_atr": STOPS_EN_ATR,
            "tasa_actividad_frac_velas": TASAS_ACTIVIDAD,
            "escenario_central": ESCENARIO_CENTRAL,
            "factor_anualizacion_dias": FACTOR_ANUALIZACION_DIAS,
            "multiplicadores_deslizamiento_sin_fuente": MULTIPLICADORES_DESLIZAMIENTO,
            "formula_arrastre_anual_pedida": (
                "coste_por_operacion_pct_capital = riesgo_por_operacion x (coste_relativo/100 / stop_en_ATR); "
                "operaciones_año = velas_año x tasa_actividad; "
                "arrastre_anual_pct = operaciones_año x coste_por_operacion_pct_capital"
            ),
            "objecion_formula": (
                "La formula pedida es ADITIVA: suma el coste de cada operacion sobre una base de "
                "capital fija. Si el coste se paga sobre capital que ya se redujo por costes previos "
                "(igual que en un interes compuesto de perdidas), el arrastre real compuesto es "
                "1 - (1 - coste_por_operacion)^operaciones_año, que es MENOR que la suma aditiva para "
                "cualquier coste_por_operacion > 0 (la perdida compuesta sobre una base decreciente es "
                "siempre menor que la misma tasa aplicada n veces sobre una base fija). Se calculan "
                "las dos, la aditiva (pedida) y la compuesta (objecion), en cada celda de la malla de "
                "arrastre anual, marcada como 'arrastre_anual_pct_compuesto_objecion'. No se sustituye "
                "la formula pedida en ningun sitio: se añade la alternativa al lado."
            ),
            "convencion_lote_para_calculo_4": {
                "EURUSD_GBPUSD_AUDUSD": "1 lote = 100.000 unidades de la divisa BASE (no USD); notional_usd = 100.000 x precio_medio_15m",
                "USDJPY_USDCHF": "1 lote = 100.000 USD (base=USD); notional_usd = 100.000 exacto, sin precio",
                "XAUUSD": "1 lote = 100 oz (coste_operar.md); notional_usd = 100 x precio_medio_15m",
                "BTCUSD_ETHUSD": "SUPUESTO PROPIO de este calculo (no de un insumo cerrado): 1 lote = 1 unidad del activo; notional_usd = 1 x precio_medio_15m",
                "precio_referencia": "precio_medio de la vela 15min en 04-resultados/atr_15m_1h_4h.json (ventana mas reciente disponible para cada instrumento)",
            },
        },
        "1_velas_disponibles_ano": velas_ano_data,
        "2_arrastre_coste_anual": arrastre_data,
        "3_borde_bruto_minimo_por_operacion": borde_minimo_data,
        "4_swap_supera_spread": swap_vs_spread_data,
        "5_sensibilidad_deslizamiento": sensibilidad_data,
        "prueba_cordura_15m_vs_4h": cordura,
    }

    SALIDA_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    # -----------------------------------------------------------------
    # Impresion en consola COMPLETA para lectura antes de entregar (regla 15)
    # -----------------------------------------------------------------
    print("=" * 100)
    print("1) VELAS DISPONIBLES AL AÑO (contadas sobre datos reales)")
    print("=" * 100)
    for instr, por_vela in velas_ano_data.items():
        for vela in VELAS:
            d = por_vela[vela]
            if d["hueco"]:
                print(f"  {instr:8s} {vela:6s} HUECO (ver motivo en JSON)")
            else:
                print(f"  {instr:8s} {vela:6s} velas_ano={d['velas_ano']:10.1f}  "
                      f"(n_real={d['n_velas_ventana_real']}, span_dias={d['span_dias_ventana_real']:.1f}, "
                      f"velas/dia={d['velas_por_dia_real']:.3f})")

    print("\n" + "=" * 100)
    print(f"2) ARRASTRE ANUAL — ESCENARIO CENTRAL {ESCENARIO_CENTRAL}")
    print("=" * 100)
    clave_central = (
        f"riesgo_{ESCENARIO_CENTRAL['riesgo_por_operacion']}__"
        f"stop_{ESCENARIO_CENTRAL['stop_en_atr']}__"
        f"actividad_{ESCENARIO_CENTRAL['tasa_actividad']}"
    )
    for instr, por_vela in arrastre_data.items():
        for vela in VELAS:
            d = por_vela[vela]
            if d["hueco"]:
                print(f"  {instr:8s} {vela:6s} HUECO")
                continue
            bloque = d["escenarios_vela"][ESCENARIO_CENTRAL["vela_escenario"]]
            for fuente, datos in bloque.items():
                celda = datos["malla_riesgo_stop_actividad"][clave_central]
                print(f"  {instr:8s} {vela:6s} [{fuente:9s}] coste_rel={datos['coste_relativo_pct']:7.3f}%  "
                      f"op/año={celda['operaciones_ano']:8.1f}  "
                      f"arrastre_aditivo={celda['arrastre_anual_pct_aditivo']:8.4f}%  "
                      f"arrastre_compuesto={celda['arrastre_anual_pct_compuesto_objecion']:8.4f}%")

    print("\n" + "=" * 100)
    print("3) BORDE BRUTO MINIMO POR OPERACION (vela mediana, muestra)")
    print("=" * 100)
    for instr, por_vela in borde_minimo_data.items():
        for vela in VELAS:
            bloque = por_vela[vela]["mediana"]
            for fuente, datos in bloque.items():
                print(f"  {instr:8s} {vela:6s} [{fuente:9s}] borde_minimo={datos['borde_bruto_minimo_pct_del_atr']:7.3f}% del ATR")

    print("\n" + "=" * 100)
    print("4) CUANDO EL SWAP SUPERA AL SPREAD (dias, por broker/direccion)")
    print("=" * 100)
    for instr, datos in swap_vs_spread_data.items():
        print(f"  --- {instr} (precio_ref={datos['precio_referencia_usado']:.4f}, notional/lote=${datos['notional_por_lote_usd']:.2f}) ---")
        for fuente, brokers in datos["brokers"].items():
            for broker, direcciones in brokers.items():
                for direccion, fila in direcciones.items():
                    estado = fila["estado"]
                    if estado == "coste":
                        print(f"    [{fuente:9s}] {broker:12s} {direccion:6s} swap={fila['swap_pct_anual']:+7.2f}%/año  "
                              f"dias_hasta_superar_spread={fila['dias_hasta_que_swap_supera_spread']:.2f}")
                    else:
                        print(f"    [{fuente:9s}] {broker:12s} {direccion:6s} estado={estado}")

    print("\n" + "=" * 100)
    print("5) SENSIBILIDAD AL DESLIZAMIENTO (escenario central riesgo/stop/actividad)")
    print("=" * 100)
    for instr, por_vela in sensibilidad_data.items():
        for vela in VELAS:
            d = por_vela[vela]
            if d["hueco"]:
                print(f"  {instr:8s} {vela:6s} HUECO")
                continue
            bloque = d["escenarios_vela"]["mediana"]
            for fuente, datos in bloque.items():
                cifras = " | ".join(
                    f"x{m}={datos['por_multiplicador'][m]['arrastre_anual_pct_aditivo']:.4f}%"
                    for m in [str(x) for x in MULTIPLICADORES_DESLIZAMIENTO]
                )
                print(f"  {instr:8s} {vela:6s} [{fuente:9s}] {cifras}")

    print("\n" + "=" * 100)
    print(f"PRUEBA DE CORDURA — arrastre 15m debe ser >= {UMBRAL_CORDURA_MULTIPLICADOR}x el de 4h (mismo instrumento, misma actividad)")
    print("=" * 100)
    for fila in cordura["filas"]:
        if fila.get("estado") == "excluido_por_hueco":
            print(f"  {fila['instrumento']:8s} EXCLUIDO (hueco, cripto)")
            continue
        marca = "OK" if fila["ok"] else "FALLO"
        print(f"  {fila['instrumento']:8s} [{fila['fuente_coste']:9s}] 15m={fila['arrastre_15m_pct']:.4f}%  "
              f"4h={fila['arrastre_4h_pct']:.4f}%  x{fila['multiplicador_15m_vs_4h']:.2f}  {marca}")
    print(f"\nRESULTADO GLOBAL PRUEBA DE CORDURA: {'OK' if cordura['ok'] else 'FALLO'}")
    if cordura["errores"]:
        for e in cordura["errores"]:
            print(f"  FALLO: {e}")

    print(f"\nEscrito: {SALIDA_JSON}")


if __name__ == "__main__":
    main()
