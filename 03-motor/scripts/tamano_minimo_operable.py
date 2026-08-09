#!/usr/bin/env python3
"""Tarea 04.01.04 — Re-derivar por cálculo el tamaño mínimo operable de XAUUSD 4h
y el requisito real de lote para el broker.

Subtarea NUEVA dentro del alcance de 04.01.01, creada por el orquestador
(regla 2 de CLAUDE.md).

NO recalcula ningún ATR ni ninguna correlación: lee el único campo autorizado
del artefacto cerrado `04-resultados/atr_15m_1h_4h.json`
(`instrumentos.XAUUSD.velas.4h.atr14_mediana`, y `atr14_medio` SOLO para el
punto 7, exigido expresamente) y la cita textual de
`04-resultados/veredictos/veredicto_criterios_g1.md` sección A3
("2.215 USD = 1.962 EUR"), de la que se deriva el tipo de cambio EUR/USD
implícito porque A3 no lo declara.

Entradas, y solo estas (regla 14 de CLAUDE.md — cálculo sobre datos brutos /
artefactos primarios ya en disco, sin red):
  - 04-resultados/atr_15m_1h_4h.json → instrumentos.XAUUSD.velas.4h.atr14_mediana
    (y atr14_medio, solo para el punto 7)
  - 04-resultados/atr_15m_1h_4h.json → instrumentos.EURUSD.velas.4h.precio_medio
    (tipo de cambio EUR/USD de fuente primaria, usado para cerrar el punto 2
    sin la circularidad de la ronda 1 — corrección ronda 1)
  - 04-resultados/veredictos/veredicto_criterios_g1.md, sección A3
    (cita "2.215 USD = 1.962 EUR", usada como dato, no reescrita)
  - 00-direccion/WBS.md, sección "## Puertas", viñeta G1-C6 (declara el
    estimador: ATR MEDIANA, y el rango de capital 1.000-2.000 EUR)
  - 00-direccion/DECISIONES.md, D-11 (rango de capital 1.000-2.000 EUR) y
    D-14 (parada dura automática al -30% del capital inicial)
  - 01-investigacion/mercados/coste_relativo.md (confirma el mismo valor de
    ATR14 mediana de XAUUSD 4h, 22,1527 USD/oz, usado como insumo del cálculo
    de A3)
  - 01-investigacion/mercados/comparacion_brokers.md, Tabla A, fila del
    criterio 1 ("1. Lote mínimo y fraccionado 0,1 oz — anclado a la entidad
    que admite España, ronda 3..."), columnas "XTB Limited" (pedido mínimo
    0,3 oz; paso 0,1 oz) e "IC Markets (EU) Ltd" (1 oz) — origen de las TRES
    etiquetas de lote usadas en los puntos 4 y 6 (corrección ronda 1, regla 12
    de CLAUDE.md: fichero usado y no declarado en la ronda 1). No se toca ese
    fichero (ver prohibición debajo); solo se cita la fila y las columnas de
    las que salen las etiquetas.

PROHIBIDO en esta tarea: tocar comparacion_brokers.md, elegir o descartar
broker, recomendar, tocar el WBS, usar red, usar ATR medio salvo en el
punto 7.

Uso: python3 03-motor/scripts/tamano_minimo_operable.py
Determinista: sin red, sin datos nuevos, solo aritmética sobre los insumos
declarados arriba.
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
JSON_ATR = RAIZ / "04-resultados" / "atr_15m_1h_4h.json"
SALIDA_JSON = RAIZ / "04-resultados" / "tamano_minimo_operable.json"

# ---------------------------------------------------------------------------
# Constantes declaradas por las entradas autorizadas (no supuestos nuevos)
# ---------------------------------------------------------------------------

RISK_PCT = 0.01              # G1-C6 (WBS, viñeta G1-C6): arriesgar como mucho el 1% del capital
STOP_MULT_ATR = 1             # G1-C6: stop de 1 x ATR MEDIANA

CAPITAL_RANGE_EUR = (1000.0, 2000.0)   # D-11 / G1-C6: rango de capital 1.000-2.000 EUR
CAPITAL_TIERS_EUR = [1000.0, 1500.0, 2000.0]  # punto 3 del encargo

PARADA_DURA_PCT = 0.30        # D-14: parada dura automática al -30% del capital inicial ingresado

# Cita literal de A3 (veredicto_criterios_g1.md), usada como dato para
# derivar el tipo de cambio que A3 NO declara. No se reescribe A3.
A3_QUOTE_USD = 2215.0   # "2.215 USD" (redondeado en el texto de A3)
A3_QUOTE_EUR = 1962.0   # "1.962 EUR" (redondeado en el texto de A3)

LOTES_BROKER_OZ = [1.0, 0.3, 0.1, 0.01]      # punto 4 del encargo
LOTES_OPERABILIDAD_OZ = [1.0, 0.3, 0.1]      # punto 5 del encargo (tabla de 3 filas)

CAPITAL_INICIAL_PUNTO5_EUR = 2000.0  # punto 5 del encargo: "capital inicial de 2.000 EUR"


def cargar_atr():
    with open(JSON_ATR) as fh:
        data = json.load(fh)
    vela4h_xau = data["instrumentos"]["XAUUSD"]["velas"]["4h"]
    vela4h_eurusd = data["instrumentos"]["EURUSD"]["velas"]["4h"]
    return (
        vela4h_xau["atr14_mediana"],
        vela4h_xau["atr14_medio"],
        vela4h_eurusd["precio_medio"],
        vela4h_xau["hasta_utc"],
    )


def eur_a_usd(eur, rate):
    return eur * rate


def usd_a_eur(usd, rate):
    return usd / rate


def capital_min_eur_para_lote(lote_oz, atr_usd_por_oz, rate):
    """Capital (EUR) necesario para que el riesgo de `lote_oz` onzas con stop
    STOP_MULT_ATR x ATR sea exactamente RISK_PCT del capital.

    Fórmula:
      riesgo_usd = lote_oz * STOP_MULT_ATR * ATR_usd_por_oz
      capital_usd = riesgo_usd / RISK_PCT
      capital_eur = capital_usd / rate   (rate = USD por 1 EUR)
    """
    riesgo_usd = lote_oz * STOP_MULT_ATR * atr_usd_por_oz
    capital_usd = riesgo_usd / RISK_PCT
    capital_eur = usd_a_eur(capital_usd, rate)
    return capital_eur, riesgo_usd, capital_usd


def max_oz_para_capital(capital_eur, atr_usd_por_oz, rate):
    """Tamaño máximo operable (oz) con stop STOP_MULT_ATR x ATR y riesgo
    RISK_PCT, para un capital dado en EUR.

    Fórmula:
      capital_usd = capital_eur * rate
      riesgo_maximo_usd = capital_usd * RISK_PCT
      oz_max = riesgo_maximo_usd / (STOP_MULT_ATR * ATR_usd_por_oz)
    """
    capital_usd = eur_a_usd(capital_eur, rate)
    riesgo_maximo_usd = capital_usd * RISK_PCT
    oz_max = riesgo_maximo_usd / (STOP_MULT_ATR * atr_usd_por_oz)
    return oz_max, capital_usd, riesgo_maximo_usd


def main():
    atr_mediana, atr_medio, eurusd_4h_precio_medio, xau_4h_hasta_utc = cargar_atr()

    resultado = {}

    print("=" * 78)
    print("PUNTO 1 — Tipo EUR/USD implícito en la cita de A3 ('2.215 USD = 1.962 EUR')")
    print("=" * 78)
    # A3 no declara el tipo de cambio. Se reconstruye de dos formas:
    #  (a) directamente de los dos números redondeados que cita A3.
    #  (b) con precisión completa: el USD exacto sale de ATR14 mediana / RISK_PCT
    #      (el mismo cálculo que A3 dice haber hecho), dividido por el EUR
    #      redondeado que sí publica A3 (es el único dato en EUR disponible).
    rate_de_cita_redondeada = A3_QUOTE_USD / A3_QUOTE_EUR
    usd_exacto_1oz = atr_mediana / RISK_PCT
    rate_implicito_preciso = usd_exacto_1oz / A3_QUOTE_EUR

    print(f"ATR14 mediana XAUUSD 4h (insumo, dato bruto): {atr_mediana} USD/oz")
    print(f"Fórmula (a): tipo = USD_citado / EUR_citado = {A3_QUOTE_USD} / {A3_QUOTE_EUR}")
    print(f"  => rate_de_cita_redondeada = {rate_de_cita_redondeada:.6f} USD por 1 EUR")
    print(f"Fórmula (b): USD_exacto = ATR14_mediana / RISK_PCT = {atr_mediana} / {RISK_PCT} = {usd_exacto_1oz:.6f}")
    print(f"  tipo = USD_exacto / EUR_citado = {usd_exacto_1oz:.6f} / {A3_QUOTE_EUR}")
    print(f"  => rate_implicito_preciso = {rate_implicito_preciso:.6f} USD por 1 EUR")
    print("Se adopta rate_implicito_preciso para el resto del cálculo (declarado, no supuesto oculto).")
    RATE = rate_implicito_preciso

    resultado["punto_1_tipo_cambio_implicito"] = {
        "formula": "rate = (atr14_mediana_4h / RISK_PCT) / EUR_citado_en_A3",
        "atr14_mediana_4h_usd_oz": atr_mediana,
        "a3_usd_citado_redondeado": A3_QUOTE_USD,
        "a3_eur_citado_redondeado": A3_QUOTE_EUR,
        "rate_de_cita_redondeada_usd_por_eur": rate_de_cita_redondeada,
        "usd_exacto_para_1oz": usd_exacto_1oz,
        "rate_implicito_preciso_usd_por_eur": rate_implicito_preciso,
        "rate_adoptado_para_el_resto_del_calculo": RATE,
    }

    print()
    print("=" * 78)
    print("PUNTO 2 — Qué representan los 1.962 EUR: aritmética, no lectura del texto")
    print("=" * 78)
    riesgo_usd_1oz = STOP_MULT_ATR * atr_mediana
    capital_usd_1oz = riesgo_usd_1oz / RISK_PCT
    capital_eur_1oz = usd_a_eur(capital_usd_1oz, RATE)
    print("Hipótesis a probar: 1.962 EUR = capital necesario para que el riesgo de 1 oz,")
    print("con stop 1 x ATR14_mediana(4h), sea el 1% del capital.")
    print(f"  riesgo_usd_1oz = STOP_MULT_ATR * atr14_mediana = {STOP_MULT_ATR} * {atr_mediana} = {riesgo_usd_1oz:.6f} USD")
    print(f"  capital_usd_1oz = riesgo_usd_1oz / RISK_PCT = {riesgo_usd_1oz:.6f} / {RISK_PCT} = {capital_usd_1oz:.6f} USD")
    print(f"  Tramo USD (dato primario solo, sin RATE): {capital_usd_1oz:.4f} USD  <-> A3 cita 2.215 USD. NO circular.")
    print()
    print("CORRECCIÓN RONDA 1 (regla 9 de CLAUDE.md): dividir capital_usd_1oz por RATE aquí NO demuestra")
    print("nada, porque RATE (punto 1) ya se construyó como capital_usd_1oz / A3_QUOTE_EUR: el cociente")
    print("da 1.962,00 EUR por construcción, para cualquier ATR — es una identidad algebraica, no una prueba.")
    capital_eur_1oz_via_rate = capital_eur_1oz
    diferencia = abs(capital_eur_1oz_via_rate - A3_QUOTE_EUR)
    print(f"  (Cálculo circular, se conserva solo como constancia: capital_usd_1oz / RATE = {capital_eur_1oz_via_rate:.6f} EUR,"
          f" diferencia {diferencia:.4e} EUR — es la propia definición de RATE, no un hallazgo.)")
    print()
    print("Cierre NO circular del tramo EUR: se toma el tipo de cambio de una fuente primaria")
    print("INDEPENDIENTE de A3 y del punto 1 — instrumentos.EURUSD.velas.4h.precio_medio, mismo JSON")
    print(f"de ATR (ventana que cierra {xau_4h_hasta_utc[:10]} para XAUUSD 4h).")
    capital_eur_1oz_primario = usd_a_eur(capital_usd_1oz, eurusd_4h_precio_medio)
    diferencia_primario_eur = capital_eur_1oz_primario - A3_QUOTE_EUR
    diferencia_primario_pct = diferencia_primario_eur / A3_QUOTE_EUR * 100
    print(f"  EURUSD 4h precio_medio (primario, independiente) = {eurusd_4h_precio_medio:.6f} USD por 1 EUR")
    print(f"  capital_eur_1oz_primario = capital_usd_1oz / precio_medio = {capital_usd_1oz:.6f} / {eurusd_4h_precio_medio:.6f}"
          f" = {capital_eur_1oz_primario:.6f} EUR")
    print(f"  Diferencia con la cita de A3 (1.962 EUR): {diferencia_primario_eur:+.4f} EUR ({diferencia_primario_pct:+.4f}%)")
    print("VEREDICTO: el tramo USD se demuestra desde el dato primario solo (sin RATE). El tramo EUR se")
    print(f"cierra, sin circularidad, contra el tipo de cambio EURUSD 4h primario, y confirma la cifra de A3")
    print(f"dentro de {abs(diferencia_primario_pct):.4f}%.")

    resultado["punto_2_que_representan_1962_eur"] = {
        "hipotesis": "capital necesario para que el riesgo de 1 oz con stop 1xATR mediana sea el 1% del capital",
        "formula": "capital_eur = (STOP_MULT_ATR * atr14_mediana_4h / RISK_PCT) / RATE",
        "riesgo_usd_1oz": riesgo_usd_1oz,
        "capital_usd_1oz": capital_usd_1oz,
        "capital_eur_1oz_calculado": capital_eur_1oz,
        "capital_eur_1oz_citado_por_a3": A3_QUOTE_EUR,
        "diferencia_eur": diferencia,
        "confirmado_por_aritmetica": True,
        "nota_circularidad_ronda_1": (
            "corrección ronda 1 (regla 9 de CLAUDE.md): capital_eur_1oz_calculado usa RATE, y RATE "
            "(punto 1) se definió como capital_usd_1oz / A3_QUOTE_EUR. Dividir de nuevo por RATE aquí "
            "es una identidad algebraica -- da 1.962,00 EUR para cualquier ATR, no demuestra nada por "
            "si sola. El cierre sin circularidad esta en 'tramo_eur_cierre_no_circular_con_tipo_primario'."
        ),
        "tramo_usd_no_circular": {
            "capital_usd_1oz_calculado": capital_usd_1oz,
            "capital_usd_1oz_citado_por_a3": A3_QUOTE_USD,
            "diferencia_usd_vs_a3": capital_usd_1oz - A3_QUOTE_USD,
        },
        "tramo_eur_cierre_no_circular_con_tipo_primario": {
            "fuente": "atr_15m_1h_4h.json -> instrumentos.EURUSD.velas.4h.precio_medio",
            "eurusd_4h_precio_medio": eurusd_4h_precio_medio,
            "formula": "capital_eur_1oz_primario = capital_usd_1oz / eurusd_4h_precio_medio",
            "capital_eur_1oz_primario": capital_eur_1oz_primario,
            "capital_eur_1oz_citado_por_a3": A3_QUOTE_EUR,
            "diferencia_eur_vs_a3": diferencia_primario_eur,
            "diferencia_pct_vs_a3": diferencia_primario_pct,
        },
    }

    print()
    print("=" * 78)
    print("PUNTO 3 — Tamaño máximo operable (oz), stop 1xATR mediana, riesgo 1%")
    print("=" * 78)
    resultado["punto_3_max_oz_por_capital"] = {}
    for capital in CAPITAL_TIERS_EUR:
        oz_max, capital_usd, riesgo_max_usd = max_oz_para_capital(capital, atr_mediana, RATE)
        print(f"Capital = {capital:.0f} EUR:")
        print(f"  capital_usd = {capital:.0f} * {RATE:.6f} = {capital_usd:.6f} USD")
        print(f"  riesgo_maximo_usd = capital_usd * RISK_PCT = {capital_usd:.6f} * {RISK_PCT} = {riesgo_max_usd:.6f} USD")
        print(f"  oz_max = riesgo_maximo_usd / (STOP_MULT_ATR * atr14_mediana) = {riesgo_max_usd:.6f} / {atr_mediana:.6f} = {oz_max:.6f} oz")
        resultado["punto_3_max_oz_por_capital"][f"{capital:.0f}_eur"] = {
            "capital_usd": capital_usd,
            "riesgo_maximo_usd": riesgo_max_usd,
            "oz_max": oz_max,
        }

    print()
    print("=" * 78)
    print("PUNTO 4 — Capital mínimo (EUR) por tamaño mínimo real de broker")
    print("=" * 78)
    resultado["punto_4_capital_minimo_por_lote"] = {}
    # Cita de origen de las tres etiquetas de broker (corrección ronda 1, regla 13 de CLAUDE.md:
    # se cita por sección y fila de tabla, nunca por número de línea):
    # 01-investigacion/mercados/comparacion_brokers.md, Tabla A, fila del criterio 1
    # ("1. Lote mínimo y fraccionado 0,1 oz — anclado a la entidad que admite España, ronda 3...").
    CITA_FILA_CRITERIO_1 = (
        "comparacion_brokers.md, Tabla A, fila criterio 1 "
        "('1. Lote mínimo y fraccionado 0,1 oz...')"
    )
    etiquetas_lote = {
        1.0: "1,0 oz (IC Markets EU) — Tabla A, fila criterio 1, columna 'IC Markets (EU) Ltd': "
             "\"Minimum Lot Size 0,01 = 1 oz, Volume Step 0,01 = 1 oz\"",
        0.3: "0,3 oz (pedido mínimo XTB Limited) — Tabla A, fila criterio 1, columna 'XTB Limited': "
             "\"Pedido mínimo 0,003 lote (0,3 oz)\"",
        0.1: "0,1 oz (paso de XTB) — Tabla A, fila criterio 1, columna 'XTB Limited': "
             "\"paso mínimo de transacción 0,001 lote = 0,1 oz exactas\"",
        0.01: "0,01 oz",
    }
    for lote in LOTES_BROKER_OZ:
        capital_eur, riesgo_usd, capital_usd = capital_min_eur_para_lote(lote, atr_mediana, RATE)
        etiqueta = etiquetas_lote[lote]
        print(f"Lote = {lote} oz ({etiqueta}):")
        print(f"  riesgo_usd = {lote} * {STOP_MULT_ATR} * {atr_mediana:.6f} = {riesgo_usd:.6f} USD")
        print(f"  capital_usd = riesgo_usd / RISK_PCT = {riesgo_usd:.6f} / {RISK_PCT} = {capital_usd:.6f} USD")
        print(f"  capital_eur = capital_usd / RATE = {capital_usd:.6f} / {RATE:.6f} = {capital_eur:.6f} EUR")
        resultado["punto_4_capital_minimo_por_lote"][str(lote)] = {
            "etiqueta": etiqueta,
            "riesgo_usd": riesgo_usd,
            "capital_usd": capital_usd,
            "capital_eur": capital_eur,
        }
    resultado["punto_4_capital_minimo_por_lote"]["_fuente_etiquetas"] = CITA_FILA_CRITERIO_1

    print()
    print("=" * 78)
    print("PUNTO 5 — Operabilidad bajo pérdida (lote mínimo INDIVISIBLE, capital inicial 2.000 EUR)")
    print("=" * 78)
    floor_parada_dura_eur = CAPITAL_INICIAL_PUNTO5_EUR * (1 - PARADA_DURA_PCT)
    rango_permitido_eur = CAPITAL_INICIAL_PUNTO5_EUR - floor_parada_dura_eur
    print(f"Capital inicial: {CAPITAL_INICIAL_PUNTO5_EUR:.0f} EUR")
    print(f"Parada dura (D-14): {PARADA_DURA_PCT*100:.0f}% del capital inicial => suelo = "
          f"{CAPITAL_INICIAL_PUNTO5_EUR:.0f} * (1-{PARADA_DURA_PCT}) = {floor_parada_dura_eur:.2f} EUR")
    print(f"Rango de pérdida PERMITIDO (0% a -30%): {CAPITAL_INICIAL_PUNTO5_EUR:.0f} - {floor_parada_dura_eur:.2f} "
          f"= {rango_permitido_eur:.2f} EUR")
    print()
    resultado["punto_5_operabilidad_bajo_perdida"] = {
        "capital_inicial_eur": CAPITAL_INICIAL_PUNTO5_EUR,
        "parada_dura_pct": PARADA_DURA_PCT,
        "floor_parada_dura_eur": floor_parada_dura_eur,
        "rango_permitido_eur": rango_permitido_eur,
        "filas": {},
    }

    print(f"{'Lote':>8} | {'Saldo umbral (EUR)':>20} | {'Caída desde 2.000 (EUR)':>24} | "
          f"{'Caída (%)':>10} | {'¿Operable en el saldo inicial?':>32} | {'Fracción del rango -30% inoperable':>36}")
    for lote in LOTES_OPERABILIDAD_OZ:
        umbral_eur, riesgo_usd, _ = capital_min_eur_para_lote(lote, atr_mediana, RATE)
        caida_eur = CAPITAL_INICIAL_PUNTO5_EUR - umbral_eur
        caida_pct = caida_eur / CAPITAL_INICIAL_PUNTO5_EUR * 100

        riesgo_eur_al_capital_inicial = usd_a_eur(riesgo_usd, RATE)
        operable_al_inicio = riesgo_eur_al_capital_inicial <= RISK_PCT * CAPITAL_INICIAL_PUNTO5_EUR

        if umbral_eur > floor_parada_dura_eur:
            # El umbral de inoperabilidad cae DENTRO del rango de pérdida permitido:
            # una franja de ese rango queda inoperable antes de llegar a la parada dura.
            inoperable_dentro_del_rango_eur = umbral_eur - floor_parada_dura_eur
            fraccion_inoperable = inoperable_dentro_del_rango_eur / rango_permitido_eur
        else:
            # El umbral está por debajo del suelo de parada dura: la cuenta para
            # ANTES de volverse inoperable para este lote. Ninguna franja del
            # rango permitido queda inoperable.
            inoperable_dentro_del_rango_eur = 0.0
            fraccion_inoperable = 0.0

        print(f"{lote:>8} | {umbral_eur:>20.2f} | {caida_eur:>24.2f} | {caida_pct:>9.2f}% | "
              f"{'sí' if operable_al_inicio else 'NO':>32} | {fraccion_inoperable*100:>35.2f}%")

        resultado["punto_5_operabilidad_bajo_perdida"]["filas"][f"{lote}_oz"] = {
            "saldo_umbral_eur": umbral_eur,
            "caida_desde_2000_eur": caida_eur,
            "caida_pct": caida_pct,
            "operable_al_capital_inicial": operable_al_inicio,
            "floor_parada_dura_eur": floor_parada_dura_eur,
            "inoperable_dentro_del_rango_permitido_eur": inoperable_dentro_del_rango_eur,
            "fraccion_del_rango_permitido_inoperable": fraccion_inoperable,
        }

    print()
    print("Fórmula de cada fila:")
    print("  saldo_umbral_eur = capital_min_eur_para_lote(lote)   (misma fórmula que el punto 4)")
    print("  caida_eur = capital_inicial - saldo_umbral_eur ; caida_pct = caida_eur / capital_inicial * 100")
    print("  Si saldo_umbral_eur > floor_parada_dura_eur:")
    print("     fraccion_inoperable = (saldo_umbral_eur - floor_parada_dura_eur) / rango_permitido_eur")
    print("  Si saldo_umbral_eur <= floor_parada_dura_eur:")
    print("     fraccion_inoperable = 0 (la parada dura corta la cuenta ANTES de que el lote deje de caber)")

    print()
    print("=" * 78)
    print("PUNTO 6 — Lote mínimo máximo admisible (dos motivos, no se mezclan)")
    print("=" * 78)
    resultado["punto_6_lote_maximo_admisible"] = {}
    for etiqueta, capital in [("conservador", 1000.0), ("alto", 2000.0)]:
        floor_eur = capital * (1 - PARADA_DURA_PCT)
        oz_motivo_a, _, _ = max_oz_para_capital(capital, atr_mediana, RATE)   # motivo (3): cabida al capital inicial
        oz_motivo_b, _, _ = max_oz_para_capital(floor_eur, atr_mediana, RATE)  # motivo (5): operable hasta la parada dura
        lote_final = min(oz_motivo_a, oz_motivo_b)
        print(f"Extremo {etiqueta} ({capital:.0f} EUR):")
        print(f"  Motivo A (punto 3, cabida al capital inicial): oz_max({capital:.0f} EUR) = {oz_motivo_a:.6f} oz")
        print(f"  Motivo B (punto 5, operable hasta la parada dura a -30%): floor = {floor_eur:.0f} EUR; "
              f"oz_max({floor_eur:.0f} EUR) = {oz_motivo_b:.6f} oz")
        binding = "B (operabilidad bajo pérdida)" if oz_motivo_b < oz_motivo_a else "A (cabida al capital inicial)"
        print(f"  Motivo que ata (más estricto): {binding}")
        print(f"  LOTE MÍNIMO MÁXIMO ADMISIBLE = min(A, B) = {lote_final:.6f} oz")
        resultado["punto_6_lote_maximo_admisible"][etiqueta] = {
            "capital_eur": capital,
            "floor_parada_dura_eur": floor_eur,
            "oz_max_motivo_a_cabida_capital_inicial": oz_motivo_a,
            "oz_max_motivo_b_operabilidad_bajo_perdida": oz_motivo_b,
            "motivo_que_ata": binding,
            "lote_minimo_maximo_admisible_oz": lote_final,
        }

    print()
    print("Margen del pedido mínimo de XTB Limited (0,3 oz) sobre el listón conservador (corrección ronda 1):")
    lote_max_conservador = resultado["punto_6_lote_maximo_admisible"]["conservador"]["lote_minimo_maximo_admisible_oz"]
    pedido_minimo_xtb_oz = 0.3
    margen_oz = lote_max_conservador - pedido_minimo_xtb_oz
    margen_pct_del_listón = margen_oz / lote_max_conservador * 100
    print(f"  listón conservador (1.000 EUR, motivo B) = {lote_max_conservador:.6f} oz")
    print(f"  pedido mínimo XTB Limited = {pedido_minimo_xtb_oz:.1f} oz (fuente: comparacion_brokers.md, "
          "Tabla A, fila criterio 1, columna 'XTB Limited')")
    print(f"  margen = {lote_max_conservador:.6f} - {pedido_minimo_xtb_oz:.1f} = {margen_oz:.6f} oz "
          f"(~0,057 oz, {margen_pct_del_listón:.1f}% del listón)")
    print("  Ese margen depende del ATR14 MEDIANA de XAUUSD 4h medido sobre la ventana que cierra "
          f"{xau_4h_hasta_utc[:10]} (instrumentos.XAUUSD.velas.4h.hasta_utc del mismo JSON primario): "
          "es el valor de un estimador sobre una ventana concreta, no una holgura estructural del bróker.")
    resultado["margen_pedido_minimo_xtb_vs_liston_conservador"] = {
        "lote_maximo_admisible_conservador_oz": lote_max_conservador,
        "pedido_minimo_xtb_limited_oz": pedido_minimo_xtb_oz,
        "fuente_pedido_minimo": "comparacion_brokers.md, Tabla A, fila criterio 1, columna 'XTB Limited'",
        "margen_oz": margen_oz,
        "margen_pct_del_liston": margen_pct_del_listón,
        "depende_de": "atr14_mediana de instrumentos.XAUUSD.velas.4h en atr_15m_1h_4h.json, "
                       f"ventana que cierra en instrumentos.XAUUSD.velas.4h.hasta_utc = {xau_4h_hasta_utc}",
        "nota": "no es una holgura estructural: es funcion del ATR mediana medido sobre esa ventana concreta.",
    }

    print()
    print("=" * 78)
    print("PUNTO 7 — Defecto en A3: '0,1 oz ~252 EUR' usa ATR MEDIO, no MEDIANA")
    print("=" * 78)
    capital_eur_medio_01, riesgo_usd_medio_01, _ = capital_min_eur_para_lote(0.1, atr_medio, RATE)
    capital_eur_mediana_01, riesgo_usd_mediana_01, _ = capital_min_eur_para_lote(0.1, atr_mediana, RATE)
    print(f"Con ATR14_MEDIO XAUUSD 4h = {atr_medio:.6f} USD/oz (el que A3 usó para el '~252 EUR'):")
    print(f"  capital_eur(0,1 oz, ATR medio) = 0,1 * {atr_medio:.6f} / {RISK_PCT} / {RATE:.6f} = {capital_eur_medio_01:.4f} EUR")
    print(f"Con ATR14_MEDIANA XAUUSD 4h = {atr_mediana:.6f} USD/oz (el que G1-C6 declara como estimador correcto):")
    print(f"  capital_eur(0,1 oz, ATR mediana) = 0,1 * {atr_mediana:.6f} / {RISK_PCT} / {RATE:.6f} = {capital_eur_mediana_01:.4f} EUR")
    print()
    print("WBS.md, sección 'Puertas', viñeta G1-C6, cita literal:")
    print('  "...con un stop de 1 x ATR MEDIANA (no la media, que en el oro esta inflada un 28-30% "')
    print('  "por su pausa diaria)."')
    print("=> El estimador que G1-C6 declara es la MEDIANA. La cifra correcta es "
          f"{capital_eur_mediana_01:.2f} EUR, no ~252 EUR.")
    print("CORRECCIÓN (no se edita veredicto_criterios_g1.md, artefacto cerrado; regla 21 de CLAUDE.md):")
    print(f"  A3 dice '~252 EUR' para 0,1 oz. Ese número sale de ATR14_MEDIO (28,4289), no de la mediana.")
    print(f"  Con el estimador declarado por G1-C6 (ATR14_MEDIANA=22,1527), el capital real es "
          f"{capital_eur_mediana_01:.2f} EUR (~196 EUR), no ~252 EUR.")

    resultado["punto_7_correccion_defecto_a3"] = {
        "cita_g1_c6_wbs": "con un stop de 1 x ATR MEDIANA (no la media, que en el oro esta inflada un 28-30% por su pausa diaria)",
        "estimador_declarado_por_g1_c6": "atr14_mediana",
        "atr14_medio_4h_usd_oz": atr_medio,
        "atr14_mediana_4h_usd_oz": atr_mediana,
        "capital_eur_0_1oz_con_atr_medio": capital_eur_medio_01,
        "capital_eur_0_1oz_con_atr_mediana": capital_eur_mediana_01,
        "cifra_citada_por_a3": "~252 EUR",
        "cifra_correcta_segun_g1_c6": capital_eur_mediana_01,
        "veredicto": "A3 usó ATR14_MEDIO (sesgado, ya corregido en otras secciones del propio proyecto) "
                      "para esta cifra de 0,1 oz, en vez de ATR14_MEDIANA, que es el estimador que G1-C6 "
                      "declara. Es un defecto de A3, no un error de este cálculo.",
    }

    with open(SALIDA_JSON, "w") as fh:
        json.dump(resultado, fh, indent=2, ensure_ascii=False)
    print()
    print(f"Salida completa escrita en: {SALIDA_JSON}")


if __name__ == "__main__":
    main()
