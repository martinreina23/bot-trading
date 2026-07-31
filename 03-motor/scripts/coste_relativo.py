"""
Tarea 02.02.02 — Coste relativo = coste ida y vuelta / ATR de la vela x 100.

Insumos (NO se recalculan, se leen tal cual):
  - 01-investigacion/mercados/coste_operar.md  (tarea 02.01.02, cerrada y verificada)
  - 04-resultados/atr_15m_1h_4h.json            (tarea 02.02.01, cerrada y verificada)

Regla critica: el ATR del JSON esta en unidad CRUDA de precio. El coste (en coste_operar.md)
esta en pips para las 6 divisas, en USD/oz para XAUUSD y en USD para BTCUSD/ETHUSD.
Antes de dividir, coste y ATR se ponen en LA MISMA unidad:
  - Divisas: coste_pips * divisor_pip = coste en unidad de precio cruda (misma que el ATR del JSON).
    divisor_pip = 0.0001 para EURUSD, GBPUSD, AUDUSD, USDCHF.
    divisor_pip = 0.01   para USDJPY (cien veces mayor).
  - XAUUSD, BTCUSD, ETHUSD: no hay pip. Coste y ATR ya estan ambos en USD de precio: se dividen
    directamente, sin conversion.

AMPLIACION (31/07, ficha ampliada): el coste relativo contra el ATR MEDIO oculta la cola de las
velas tranquilas (aviso del revisor del Brief A + leccion L-008: un umbral sobre una magnitud
inestable necesita mas de una ventana/percentil, no una sola). El JSON de 02.02.01 ya trae
`atr14_p10` (vela tranquila, percentil 10 del ATR) y `atr14_p90` (vela agitada, percentil 90).
Se añaden dos escenarios mas por fila, con la MISMA metodologia y los MISMOS divisores de pip:
  - "ratios_p10": coste / atr14_p10 x 100 — caso TIPICO-MALO (una vela tranquila de cada diez).
  - "ratios_p90": coste / atr14_p90 x 100 — caso FAVORABLE (una vela agitada de cada diez), NO
    el caso tipico; se presenta solo como referencia del mejor extremo.
  - "multiplicador_vs_media" en cada uno: coste_relativo_pct(escenario) / coste_relativo_pct(media).
    Mide cuanto EMPEORA (p10) o MEJORA (p90) el coste relativo frente al numero de la vela media.
Los valores ya calculados de "ratios" (contra atr14_medio) NO se tocan: se leen y escriben
exactamente igual que antes de esta ampliacion.

Este script NO toca 03-motor/scripts/precios_mercado.py ni 04-resultados/atr_15m_1h_4h.json
(otro agente trabaja con ellos en 02.02.03 en paralelo). Escribe en ficheros nuevos.

CORRECCION (31/07, rechazo de critico-codigo sobre 02.02.02): el ATR MEDIO de XAUUSD esta inflado
respecto a su mediana mas que el de cualquier otro instrumento (ratio medio/mediana ~1,28-1,30 en
XAUUSD frente a 0,985-1,144 en los otros 7), por la pausa diaria real del oro al contado (~21:00-
22:00 UTC, documentada en 02.02.01) que genera un salto de rango una vez al dia -- infla la media,
no la mediana. Se añade "ratios_mediana" (coste / atr14_mediana x 100) para las 18 celdas de
divisas+oro y, donde el dato lo permite, cripto, usando el campo `atr14_mediana` que YA estaba en
el JSON de 02.02.01 (no se recalcula el ATR, solo se divide con otro estadistico de la misma serie).
No se toca ningun valor de "ratios", "ratios_p10" ni "ratios_p90" ya escritos.
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ATR_JSON = RAIZ / "04-resultados" / "atr_15m_1h_4h.json"
SALIDA_JSON = RAIZ / "04-resultados" / "coste_relativo_15m_1h_4h.json"

# Costes de ida y vuelta, copiados literalmente de 01-investigacion/mercados/coste_operar.md
# (tabla "Tabla FINAL — coste de entrar y salir", columna "COSTE TOTAL ida y vuelta").
# unidad: "pip" (requiere divisor_pip) o "usd" (ya en la misma unidad cruda que el ATR del JSON).
COSTES = {
    "EURUSD": {"tipo_cuenta": "Raw/ECN", "unidad": "pip", "divisor_pip": 0.0001, "valores": {"unico": 0.8}},
    "GBPUSD": {"tipo_cuenta": "Raw/ECN", "unidad": "pip", "divisor_pip": 0.0001, "valores": {"unico": 0.82}},
    "USDJPY": {"tipo_cuenta": "Raw/ECN", "unidad": "pip", "divisor_pip": 0.01, "valores": {"unico": 1.16}},
    "AUDUSD": {"tipo_cuenta": "Raw/ECN", "unidad": "pip", "divisor_pip": 0.0001, "valores": {"unico": 0.85}},
    "USDCHF": {"tipo_cuenta": "Raw/ECN", "unidad": "pip", "divisor_pip": 0.0001, "valores": {"unico": 0.73}},
    "XAUUSD": {"tipo_cuenta": "Raw/ECN", "unidad": "usd", "divisor_pip": None, "valores": {"unico": 0.26}},
    "BTCUSD": {
        "tipo_cuenta": "CFD spread-only",
        "unidad": "usd",
        "divisor_pip": None,
        "valores": {"feb-2025": 20.22, "abr-2026": 36.90},
    },
    "ETHUSD": {
        "tipo_cuenta": "CFD spread-only",
        "unidad": "usd",
        "divisor_pip": None,
        "valores": {"feb-2025": 3.01, "abr-2026": 7.04},
    },
}

VELAS = ["15min", "1h", "4h"]
UMBRAL_G1_MIN = 10.0
UMBRAL_G1_MAX = 15.0


def cargar_atr():
    with open(ATR_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def coste_en_unidad_atr(cfg, valor_coste):
    """Convierte el coste a la misma unidad cruda de precio que usa el ATR del JSON."""
    if cfg["unidad"] == "pip":
        return valor_coste * cfg["divisor_pip"]
    # xauusd/cripto: ya esta en USD de precio, misma unidad que el ATR crudo del JSON
    return valor_coste


def main():
    atr_data = cargar_atr()
    instrumentos = atr_data["instrumentos"]

    resultado = {
        "generado_desde": {
            "costes": "01-investigacion/mercados/coste_operar.md (02.01.02, NO recalculado)",
            "atr": "04-resultados/atr_15m_1h_4h.json (02.02.01, NO recalculado)",
        },
        "formula": "coste_relativo_pct = (coste_ida_y_vuelta_en_unidad_atr / atr14_medio) x 100",
        "formula_ampliacion_p10_p90": (
            "ratios_p10 = coste / atr14_p10 x 100 (vela tranquila, caso desfavorable); "
            "ratios_p90 = coste / atr14_p90 x 100 (vela agitada, mejor caso, NO tipico); "
            "multiplicador_vs_media = coste_relativo_pct(escenario) / coste_relativo_pct(media)"
        ),
        "umbral_g1_pct": [UMBRAL_G1_MIN, UMBRAL_G1_MAX],
        "instrumentos": {},
    }

    errores_cordura = []

    for instr, cfg in COSTES.items():
        atr_instr = instrumentos[instr]
        fila = {
            "unidad_coste_original": cfg["unidad"],
            "divisor_pip_aplicado": cfg["divisor_pip"],
            "tipo_cuenta_coste": cfg["tipo_cuenta"],
            "fuente_atr": atr_instr["fuente"],
            "velas": {},
        }
        for vela in VELAS:
            atr_vela = atr_instr["velas"][vela]
            atr_medio = atr_vela["atr14_medio"]
            atr_mediana = atr_vela["atr14_mediana"]
            atr_p10 = atr_vela["atr14_p10"]
            atr_p90 = atr_vela["atr14_p90"]
            reproducible = atr_vela.get("reproducible", True)
            ratios = {}
            for etiqueta, valor_coste in cfg["valores"].items():
                coste_conv = coste_en_unidad_atr(cfg, valor_coste)
                ratio_pct = (coste_conv / atr_medio) * 100.0
                ratios[etiqueta] = {
                    "coste_original": valor_coste,
                    "coste_convertido_unidad_atr": coste_conv,
                    "atr14_medio_crudo": atr_medio,
                    "coste_relativo_pct": ratio_pct,
                    "pasa_g1_10pct": ratio_pct <= UMBRAL_G1_MIN,
                    "pasa_g1_15pct": ratio_pct <= UMBRAL_G1_MAX,
                }
                # Prueba de cordura: ningun coste relativo de DIVISA (no oro, no cripto) > 100%
                if instr in ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF") and ratio_pct > 100.0:
                    errores_cordura.append(f"{instr} {vela} {etiqueta}: {ratio_pct:.2f}% > 100%")

            # --- AMPLIACION: mismos divisores de pip, mismo coste, denominador = atr14_p10 / atr14_p90 ---
            ratios_p10 = {}
            ratios_p90 = {}
            for etiqueta, valor_coste in cfg["valores"].items():
                coste_conv = coste_en_unidad_atr(cfg, valor_coste)
                ratio_medio_pct = ratios[etiqueta]["coste_relativo_pct"]

                ratio_p10_pct = (coste_conv / atr_p10) * 100.0
                ratios_p10[etiqueta] = {
                    "coste_original": valor_coste,
                    "coste_convertido_unidad_atr": coste_conv,
                    "atr14_p10_crudo": atr_p10,
                    "coste_relativo_pct": ratio_p10_pct,
                    "pasa_g1_10pct": ratio_p10_pct <= UMBRAL_G1_MIN,
                    "pasa_g1_15pct": ratio_p10_pct <= UMBRAL_G1_MAX,
                    "multiplicador_vs_media": ratio_p10_pct / ratio_medio_pct,
                }

                ratio_p90_pct = (coste_conv / atr_p90) * 100.0
                ratios_p90[etiqueta] = {
                    "coste_original": valor_coste,
                    "coste_convertido_unidad_atr": coste_conv,
                    "atr14_p90_crudo": atr_p90,
                    "coste_relativo_pct": ratio_p90_pct,
                    "pasa_g1_10pct": ratio_p90_pct <= UMBRAL_G1_MIN,
                    "pasa_g1_15pct": ratio_p90_pct <= UMBRAL_G1_MAX,
                    "multiplicador_vs_media": ratio_p90_pct / ratio_medio_pct,
                }

            # --- CORRECCION 31/07: mismos divisores de pip, mismo coste, denominador = atr14_mediana ---
            ratios_mediana = {}
            for etiqueta, valor_coste in cfg["valores"].items():
                coste_conv = coste_en_unidad_atr(cfg, valor_coste)
                ratio_medio_pct = ratios[etiqueta]["coste_relativo_pct"]

                ratio_mediana_pct = (coste_conv / atr_mediana) * 100.0
                ratios_mediana[etiqueta] = {
                    "coste_original": valor_coste,
                    "coste_convertido_unidad_atr": coste_conv,
                    "atr14_mediana_crudo": atr_mediana,
                    "coste_relativo_pct": ratio_mediana_pct,
                    "pasa_g1_10pct": ratio_mediana_pct <= UMBRAL_G1_MIN,
                    "pasa_g1_15pct": ratio_mediana_pct <= UMBRAL_G1_MAX,
                    "multiplicador_vs_media": ratio_mediana_pct / ratio_medio_pct,
                }

            fila["velas"][vela] = {
                "atr14_medio_crudo": atr_medio,
                "atr14_mediana_crudo": atr_mediana,
                "ratio_medio_vs_mediana_atr": atr_medio / atr_mediana,
                "atr14_p10_crudo": atr_p10,
                "atr14_p90_crudo": atr_p90,
                "reproducible": reproducible,
                "ratios": ratios,
                "ratios_p10": ratios_p10,
                "ratios_p90": ratios_p90,
                "ratios_mediana": ratios_mediana,
            }
        resultado["instrumentos"][instr] = fila

    resultado["prueba_cordura"] = {
        "regla": "ningun coste relativo de DIVISA (EUR/GBP/USD/AUD/CHF) puede superar 100%",
        "ok": len(errores_cordura) == 0,
        "errores": errores_cordura,
    }

    with open(SALIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    # --- Impresion en consola para lectura completa antes de entregar (regla 15/regla del encargo) ---
    print("=" * 100)
    print("COMPROBACION MANUAL — dos cifras de control dadas por el encargo")
    print("=" * 100)
    eur15 = instrumentos["EURUSD"]["velas"]["15min"]["atr14_medio"]
    jpy15 = instrumentos["USDJPY"]["velas"]["15min"]["atr14_medio"]
    print(f"EURUSD 15m crudo {eur15:.8f} / 0.0001 = {eur15/0.0001:.2f} pips (esperado ~6.86)")
    print(f"USDJPY 15m crudo {jpy15:.8f} / 0.01   = {jpy15/0.01:.2f} pips (esperado ~12.03)")
    print()

    print("=" * 100)
    print("TABLA COSTE RELATIVO (%) = coste ida y vuelta / ATR x 100 -- tres escenarios")
    print("=" * 100)
    for instr, fila in resultado["instrumentos"].items():
        print(f"\n--- {instr} ({fila['tipo_cuenta_coste']}, unidad coste original: {fila['unidad_coste_original']}"
              + (f", divisor_pip={fila['divisor_pip_aplicado']}" if fila['divisor_pip_aplicado'] else "") + ") ---")
        for vela in VELAS:
            v = fila["velas"][vela]
            repro = "reproducible" if v["reproducible"] else "NO reproducible (heredado del ATR)"
            for etiqueta, r in v["ratios"].items():
                marca = "PASA<=10%" if r["pasa_g1_10pct"] else ("PASA<=15%" if r["pasa_g1_15pct"] else "NO PASA")
                print(f"  {vela:6s} [{etiqueta:9s}] MEDIA  ATR={r['atr14_medio_crudo']:.8f}  coste={r['coste_original']}"
                      f"  coste_conv={r['coste_convertido_unidad_atr']:.8f}  ratio={r['coste_relativo_pct']:.3f}%"
                      f"  {marca}  [{repro}]")
            for etiqueta, r in v["ratios_p10"].items():
                marca = "PASA<=10%" if r["pasa_g1_10pct"] else ("PASA<=15%" if r["pasa_g1_15pct"] else "NO PASA")
                print(f"  {vela:6s} [{etiqueta:9s}] P10    ATR={r['atr14_p10_crudo']:.8f}  coste={r['coste_original']}"
                      f"  coste_conv={r['coste_convertido_unidad_atr']:.8f}  ratio={r['coste_relativo_pct']:.3f}%"
                      f"  {marca}  mult_vs_media={r['multiplicador_vs_media']:.2f}x  [{repro}]")
            for etiqueta, r in v["ratios_p90"].items():
                marca = "PASA<=10%" if r["pasa_g1_10pct"] else ("PASA<=15%" if r["pasa_g1_15pct"] else "NO PASA")
                print(f"  {vela:6s} [{etiqueta:9s}] P90    ATR={r['atr14_p90_crudo']:.8f}  coste={r['coste_original']}"
                      f"  coste_conv={r['coste_convertido_unidad_atr']:.8f}  ratio={r['coste_relativo_pct']:.3f}%"
                      f"  {marca}  mult_vs_media={r['multiplicador_vs_media']:.2f}x  [{repro}]")
            for etiqueta, r in v["ratios_mediana"].items():
                marca = "PASA<=10%" if r["pasa_g1_10pct"] else ("PASA<=15%" if r["pasa_g1_15pct"] else "NO PASA")
                print(f"  {vela:6s} [{etiqueta:9s}] MEDIANA ATR={r['atr14_mediana_crudo']:.8f}  coste={r['coste_original']}"
                      f"  coste_conv={r['coste_convertido_unidad_atr']:.8f}  ratio={r['coste_relativo_pct']:.3f}%"
                      f"  {marca}  mult_vs_media={r['multiplicador_vs_media']:.2f}x  [{repro}]")

    print("\n" + "=" * 100)
    print("CORRECCION: RATIO ATR_MEDIO / ATR_MEDIANA por instrumento (sesgo de la pausa diaria del oro)")
    print("=" * 100)
    for instr, fila in resultado["instrumentos"].items():
        cifras = [f"{fila['velas'][v]['ratio_medio_vs_mediana_atr']:.3f}" for v in VELAS]
        print(f"  {instr:7s} 15m/1h/4h = {' / '.join(cifras)}")

    print("\n" + "=" * 100)
    print("PRUEBA DE CORDURA (ningun coste relativo de divisa > 100%)")
    print("=" * 100)
    print(f"OK: {resultado['prueba_cordura']['ok']}")
    if errores_cordura:
        for e in errores_cordura:
            print(f"  FALLO: {e}")

    print(f"\nEscrito: {SALIDA_JSON}")


if __name__ == "__main__":
    main()
