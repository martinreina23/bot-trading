#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 02.02.03 (WBS) — matriz de correlaciones 8x8 sobre RENDIMIENTOS
LOGARITMICOS (nunca sobre precios: correlacionar precios da correlaciones
espurias), en 3 ventanas (3 meses / 1 año / 2 años) y en las TRES velas
(15min / 1h / 4h), mas la diaria (1d) como comprobacion. Corte 22:00 UTC
unico para todos los instrumentos.

Reutiliza SIN DUPLICAR (leccion T2 de CLAUDE.md: en el proyecto anterior la
logica de remuestreo vivia en dos sitios y divergio) las funciones ya
reparadas y verificadas por recalculo independiente en la tarea 02.02.01:
`remuestrear` de 03-motor/scripts/precios_mercado.py. La unica capacidad
nueva que se añadio a ESE fichero (no aqui) es la vela "1d" anclada al corte
de 22:00 UTC (offset=22h sobre resample("24h", ...)); 15min/1h/4h no
cambiaron ni un bit.

Este script NO descarga nada nuevo: lee los precios YA descargados por
02.02.01 en 02-datos/bruto/ (cache 1-minuto para EURUSD/GBPUSD/USDJPY/
AUDUSD/USDCHF/XAUUSD; velas nativas 15min/1h/4h de Kraken para BTCUSD/
ETHUSD, sin 1-minuto disponible para cripto — ver comentario de
`precios_mercado.procesar_cripto`).

FUENTES (idénticas a 02.02.01, no se cambian aquí):
  - EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF -> HistData.com, ASCII M1, BID
  - XAUUSD  -> Dukascopy, oro AL CONTADO (spot/OTC, bid), NUNCA el futuro GC=F
  - BTCUSD, ETHUSD -> Kraken, PAR REAL CONTRA USD (XBTUSD, ETHUSD), NUNCA USDT

CORTE UNICO 22:00 UTC: fija el ANCLA de la vela diaria (1d) y el borde
superior/inferior de cada ventana (3 meses/1 año/2 años) sobre la serie de
retornos ya calculada; el remuestreo intradia (15min/1h/4h) es reloj UTC
puro como en 02.02.01 (ese corte SI coincide con la rejilla de 15min/1h; en
4h no coincide y el arreglo de bin de borde de `remuestrear` ya lo cubre).

HUECO CONOCIDO, DECLARADO Y NO RELLENADO (regla 14 CLAUDE.md): BTCUSD y
ETHUSD solo tienen 720 velas cerradas por instrumento en cache (Kraken,
ventana deslizante — 7,4 dias en 15min, 30 en 1h, 120 en 4h). Las ventanas
de 1 año y 2 años NO EXISTEN para ellas en ninguna vela: se marcan hueco con
su motivo, nunca se estiman ni se extrapolan. La vela diaria (1d) tambien
queda hueco para cripto: no hay 1-minuto de Kraken para remuestrear con el
corte 22:00 UTC exacto, y agregar desde las velas 4h nativas (rejilla
0/4/8/12/16/20 UTC, NO anclada a 22:00) rompería el corte unico exigido; no
se descarga una granularidad nueva (1440min) de Kraken para rellenar esto:
excede el alcance de "los datos ya estan descargados, no se vuelve a
descargar salvo que falte algo" y contradice explicitamente "no cambies de
fuente" del encargo.

Toda celda que involucre BTCUSD o ETHUSD lleva "reproducible": false, igual
que en 02.02.01, porque la ventana de Kraken se desliza en cada ejecucion.

USO:
    .venv/bin/python 03-motor/scripts/correlaciones_mercado.py

SALIDA:
    04-resultados/correlaciones_8x8.json
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "03-motor" / "scripts"))
import precios_mercado as pm  # noqa: E402  (reutiliza remuestrear, no se duplica)

BRUTO = pm.BRUTO
RESULTADOS = pm.RESULTADOS
guardia_no_reservado = pm.guardia_no_reservado

# ---------------------------------------------------------------------------
# Constantes del encargo
# ---------------------------------------------------------------------------
INSTRUMENTOS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "XAUUSD", "BTCUSD", "ETHUSD"]
INSTRUMENTOS_FOREX_ORO = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF", "XAUUSD"]
INSTRUMENTOS_CRIPTO = ["BTCUSD", "ETHUSD"]
VELAS = ["15min", "1h", "4h", "1d"]
VENTANAS_DIAS = {"3_meses": 90, "1_anio": 365, "2_anios": 730}
UMBRAL_MIN_OBS = 20  # mismo umbral que 02.02.01 usa para declarar hueco (< 20 velas)
UMBRAL_CORRELACION_G1 = 0.7  # criterio 4 de G1 (en valor absoluto)

FUENTES = {
    "EURUSD": "HistData.com (ASCII M1, precio BID, forex minorista agregado)",
    "GBPUSD": "HistData.com (ASCII M1, precio BID, forex minorista agregado)",
    "USDJPY": "HistData.com (ASCII M1, precio BID, forex minorista agregado)",
    "AUDUSD": "HistData.com (ASCII M1, precio BID, forex minorista agregado)",
    "USDCHF": "HistData.com (ASCII M1, precio BID, forex minorista agregado)",
    "XAUUSD": "Dukascopy (oro AL CONTADO / spot OTC, lado BID; NUNCA futuro GC=F)",
    "BTCUSD": "Kraken (par REAL contra USD, XBTUSD; NUNCA USDT/Tether)",
    "ETHUSD": "Kraken (par REAL contra USD, ETHUSD; NUNCA USDT/Tether)",
}

MOTIVO_HUECO_CRIPTO_1D = (
    "No hay serie 1-minuto de Kraken para remuestrear a diaria con el corte "
    "22:00 UTC exacto (Kraken no entrega 1-min con profundidad suficiente, "
    "ver precios_mercado.procesar_cripto). Agregar desde las velas 4h "
    "nativas de Kraken usaria su rejilla propia (0/4/8/12/16/20 UTC), NO "
    "anclada al corte 22:00: los bordes de la vela diaria resultante no "
    "coincidirian con los de forex/oro, y los rendimientos dejarian de ser "
    "contemporaneos entre instrumentos. No se descarga una granularidad "
    "diaria nueva de Kraken (excede 'no cambies de fuente' del encargo "
    "02.02.03)."
)


def _motivo_hueco_ventana_cripto(instrumento: str, vela: str, meta: dict, dias_ventana: int) -> str:
    if meta["n_total"] == 0:
        return (
            f"{instrumento} sin historial en la vela {vela}: 0 velas en cache "
            f"(hueco heredado de 02.02.01)."
        )
    return (
        f"{instrumento}/{vela}: cache cubre solo {meta['n_total']} velas desde "
        f"{meta['desde_real_utc']} hasta {meta['hasta_real_utc']} "
        f"(~{meta['dias_cubiertos']:.1f} dias); no alcanza para una ventana de "
        f"{dias_ventana} dias. Ventana deslizante de Kraken (endpoint publico "
        f"/OHLC, ~720 velas cerradas mas recientes, sin profundidad de 1 año/2 "
        f"años); no se estima ni se cambia de fuente."
    )


# ---------------------------------------------------------------------------
# Carga de datos (solo lectura de 02-datos/bruto/, ya descargado por 02.02.01)
# ---------------------------------------------------------------------------
def cargar_1m(instrumento: str) -> pd.DataFrame:
    ruta = BRUTO / instrumento / "1m.csv.gz"
    df = pd.read_csv(ruta, compression="gzip")
    df.index = pd.to_datetime(df["ts_utc"], utc=True)
    df.index.name = "ts_utc"
    return df[["open", "high", "low", "close"]]


def cargar_cripto_vela(instrumento: str, vela: str) -> pd.DataFrame:
    ruta = BRUTO / instrumento / f"{vela}.csv.gz"
    df = pd.read_csv(ruta, compression="gzip")
    df.index = pd.to_datetime(df["ts_utc"], utc=True)
    df.index.name = "ts_utc"
    return df[["open", "high", "low", "close"]]


# ---------------------------------------------------------------------------
# Rendimientos logaritmicos por instrumento y vela
# ---------------------------------------------------------------------------
def retornos_forex_oro(instrumento: str, vela: str) -> tuple[pd.Series, dict]:
    df1m = cargar_1m(instrumento)
    inicio = df1m.index.min()
    fin = df1m.index.max() + pd.Timedelta(minutes=1)  # borde superior exclusivo real
    r = pm.remuestrear(df1m, vela, inicio, fin)
    if len(r) < 2:
        return pd.Series(dtype=float), {
            "fuente": FUENTES[instrumento], "hueco": True,
            "motivo": "menos de 2 velas tras remuestrear: no hay retorno calculable",
            "n_total": int(len(r)),
        }
    log_ret = np.log(r["close"] / r["close"].shift(1)).dropna()
    ancho = pd.Timedelta(pm.REGLA_PANDAS[vela])
    meta = {
        "fuente": FUENTES[instrumento],
        "hueco": False,
        "n_total": int(len(log_ret)),
        "desde_real_utc": log_ret.index[0].isoformat(),
        "hasta_real_utc": (log_ret.index[-1] + ancho).isoformat(),
        "dias_cubiertos": (log_ret.index[-1] - log_ret.index[0]).total_seconds() / 86400,
    }
    return log_ret, meta


def retornos_cripto(instrumento: str, vela: str) -> tuple[pd.Series, dict]:
    if vela == "1d":
        return pd.Series(dtype=float), {
            "fuente": FUENTES[instrumento], "hueco": True,
            "motivo": MOTIVO_HUECO_CRIPTO_1D, "n_total": 0,
        }
    df = cargar_cripto_vela(instrumento, vela)
    if len(df) < 2:
        return pd.Series(dtype=float), {
            "fuente": FUENTES[instrumento], "hueco": True,
            "motivo": "menos de 2 velas en cache: no hay retorno calculable",
            "n_total": int(len(df)),
        }
    log_ret = np.log(df["close"] / df["close"].shift(1)).dropna()
    meta = {
        "fuente": FUENTES[instrumento],
        "hueco": False,
        "n_total": int(len(log_ret)),
        "desde_real_utc": log_ret.index[0].isoformat(),
        "hasta_real_utc": df.index[-1].isoformat(),
        "dias_cubiertos": (df.index[-1] - df.index[0]).total_seconds() / 86400,
    }
    return log_ret, meta


def construir_retornos(instrumento: str, vela: str) -> tuple[pd.Series, dict]:
    if instrumento in INSTRUMENTOS_CRIPTO:
        return retornos_cripto(instrumento, vela)
    return retornos_forex_oro(instrumento, vela)


# ---------------------------------------------------------------------------
# Matriz de correlaciones por vela x ventana
# ---------------------------------------------------------------------------
def matriz_para_ventana(
    retornos_por_instrumento: dict[str, pd.Series],
    metas: dict[str, dict],
    vela: str,
    nombre_ventana: str,
    dias_ventana: int,
) -> dict:
    # ancla de la ventana: la ultima fecha COMUN disponible entre los 6
    # instrumentos forex+oro (nunca cripto: su cache siempre es mas reciente
    # y desplazaria la ventana en cada ejecucion). Esto es lo que hace la
    # ventana reproducible para los 15 pares no-cripto.
    candidatos_fin = [
        retornos_por_instrumento[i].index[-1]
        for i in INSTRUMENTOS_FOREX_ORO
        if len(retornos_por_instrumento[i])
    ]
    if not candidatos_fin:
        raise RuntimeError(f"Sin datos forex/oro para anclar la ventana en vela {vela}")
    fin_comun = min(candidatos_fin)
    inicio_ventana = fin_comun - pd.Timedelta(days=dias_ventana)

    series_win: dict[str, pd.Series] = {}
    cobertura: dict[str, dict] = {}
    for inst in INSTRUMENTOS:
        s = retornos_por_instrumento[inst]
        if len(s) == 0:
            series_win[inst] = pd.Series(dtype=float)
            cobertura[inst] = {"n_en_ventana": 0, "n_total_disponible": 0}
            continue
        s_win = s[(s.index > inicio_ventana) & (s.index <= fin_comun)]
        series_win[inst] = s_win
        cobertura[inst] = {
            "n_en_ventana": int(len(s_win)),
            "n_total_disponible": int(len(s)),
        }

    df_win = pd.concat(series_win, axis=1, sort=True)  # outer join por indice de tiempo, cronologico
    corr = df_win.corr(method="pearson")

    # PROFUNDIDAD INSUFICIENTE (no solo solapamiento): si el historial TOTAL
    # de un instrumento cripto (dias_cubiertos, medido de punta a punta de su
    # cache) es menor que la ventana nominal pedida, esa ventana NO EXISTE
    # para el, por mucho que las pocas observaciones que tiene "quepan"
    # dentro del rango de fechas de la ventana (que es enorme comparado con
    # su historial real). Sin este chequeo, un BTCUSD con 120 dias de cache
    # colaria como si tuviera correlacion "de 1 año" o "de 2 años" solo
    # porque 120 dias < 365/730 dias de la ventana nominal. Esto es lo que
    # el encargo 02.02.03 exige declarar como hueco, no rellenar.
    motivo_insuficiente: dict[str, str | None] = {}
    for inst in INSTRUMENTOS_CRIPTO:
        meta = metas[inst]
        if meta.get("hueco"):
            motivo_insuficiente[inst] = meta["motivo"]
        elif meta.get("dias_cubiertos", 0) < dias_ventana:
            motivo_insuficiente[inst] = _motivo_hueco_ventana_cripto(inst, vela, {
                "n_total": meta["n_total"],
                "desde_real_utc": meta["desde_real_utc"],
                "hasta_real_utc": meta["hasta_real_utc"],
                "dias_cubiertos": meta["dias_cubiertos"],
            }, dias_ventana)
        else:
            motivo_insuficiente[inst] = None

    correlaciones: dict[str, dict] = {}
    n_observaciones: dict[str, dict] = {}
    reproducible: dict[str, dict] = {}
    huecos: list[dict] = []

    for a in INSTRUMENTOS:
        correlaciones[a] = {}
        n_observaciones[a] = {}
        reproducible[a] = {}
        for b in INSTRUMENTOS:
            n = int(df_win[[a, b]].dropna().shape[0])
            n_observaciones[a][b] = n
            es_reproducible = not (a in INSTRUMENTOS_CRIPTO or b in INSTRUMENTOS_CRIPTO)
            reproducible[a][b] = es_reproducible
            if a == b:
                correlaciones[a][b] = 1.0 if n > 0 else None
                continue

            motivo_profundidad = None
            for inst in (a, b):
                if inst in INSTRUMENTOS_CRIPTO and motivo_insuficiente[inst] is not None:
                    motivo_profundidad = motivo_insuficiente[inst]
                    break

            if motivo_profundidad is not None or n < UMBRAL_MIN_OBS:
                correlaciones[a][b] = None
                if a < b:  # una sola entrada por par no ordenado
                    motivo = motivo_profundidad or (
                        f"solapamiento insuficiente: {n} observaciones (< {UMBRAL_MIN_OBS})"
                    )
                    huecos.append({"par": [a, b], "n_observaciones": n, "motivo": motivo})
            else:
                val = corr.loc[a, b]
                correlaciones[a][b] = None if pd.isna(val) else float(val)

    return {
        "fin_comun_utc": fin_comun.isoformat(),
        "inicio_ventana_utc": inicio_ventana.isoformat(),
        "dias_ventana_objetivo": dias_ventana,
        "cobertura_por_instrumento": cobertura,
        "correlaciones": correlaciones,
        "n_observaciones": n_observaciones,
        "reproducible": reproducible,
        "huecos": huecos,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    generado_utc = datetime.now(timezone.utc)

    print("=== 02.02.03 — matriz de correlaciones 8x8 (rendimientos logaritmicos) ===")
    print("Cargando y remuestreando retornos por instrumento x vela...\n")

    retornos: dict[str, dict[str, pd.Series]] = {}
    metas: dict[str, dict[str, dict]] = {}
    for vela in VELAS:
        retornos[vela] = {}
        metas[vela] = {}
        for inst in INSTRUMENTOS:
            s, meta = construir_retornos(inst, vela)
            retornos[vela][inst] = s
            metas[vela][inst] = meta
            estado = "HUECO: " + meta.get("motivo", "") if meta.get("hueco") else f"n={meta['n_total']}"
            print(f"  {inst:<8}{vela:<8}{estado}")
    print()

    matrices: dict[str, dict] = {}
    for vela in VELAS:
        matrices[vela] = {}
        for nombre_ventana, dias in VENTANAS_DIAS.items():
            matrices[vela][nombre_ventana] = matriz_para_ventana(
                retornos[vela], metas[vela], vela, nombre_ventana, dias
            )

    # -------------------------------------------------------------
    # PRUEBA DE CORDURA OBLIGATORIA: EURUSD/USDCHF fuertemente NEGATIVO
    # -------------------------------------------------------------
    print("=" * 90)
    print("PRUEBA DE CORDURA: EURUSD/USDCHF (esperado: fuertemente NEGATIVO, brief ~-0.97)")
    print("=" * 90)
    cordura_ok = True
    cordura_detalle = {}
    for vela in VELAS:
        cordura_detalle[vela] = {}
        for nombre_ventana in VENTANAS_DIAS:
            val = matrices[vela][nombre_ventana]["correlaciones"]["EURUSD"]["USDCHF"]
            cordura_detalle[vela][nombre_ventana] = val
            estado = "N/D (hueco)" if val is None else f"{val:.4f}"
            marca = ""
            if val is not None:
                if val >= 0:
                    cordura_ok = False
                    marca = "  <<< FALLO: NO ES NEGATIVO"
                elif val > -0.5:
                    marca = "  (negativo pero mas debil de lo esperado, revisar)"
            print(f"  {vela:<8}{nombre_ventana:<12}{estado:<14}{marca}")
    print()
    if not cordura_ok:
        print("[CORDURA FALLIDA] EURUSD/USDCHF salio positivo en al menos una celda.", file=sys.stderr)
        print("PARANDO: posible error de signo o convencion (L-006). No se maquilla.", file=sys.stderr)

    # -------------------------------------------------------------
    # Resumen: pares que superan 0.7 en valor absoluto en ALGUNA ventana
    # -------------------------------------------------------------
    pares_sobre_umbral: list[dict] = []
    for vela in VELAS:
        for nombre_ventana in VENTANAS_DIAS:
            m = matrices[vela][nombre_ventana]
            for i, a in enumerate(INSTRUMENTOS):
                for b in INSTRUMENTOS[i + 1:]:
                    val = m["correlaciones"][a][b]
                    if val is not None and abs(val) > UMBRAL_CORRELACION_G1:
                        pares_sobre_umbral.append({
                            "par": [a, b], "vela": vela, "ventana": nombre_ventana,
                            "correlacion": val, "n_observaciones": m["n_observaciones"][a][b],
                            "reproducible": m["reproducible"][a][b],
                        })

    print("=" * 90)
    print(f"PARES CON |correlacion| > {UMBRAL_CORRELACION_G1} (criterio 4 de G1)")
    print("=" * 90)
    for p in sorted(pares_sobre_umbral, key=lambda x: (-abs(x["correlacion"]))):
        rep = "reproducible" if p["reproducible"] else "NO reproducible (cripto)"
        print(f"  {p['par'][0]}/{p['par'][1]:<8} {p['vela']:<6}{p['ventana']:<10}"
              f"{p['correlacion']:>8.4f}  n={p['n_observaciones']:<7} {rep}")
    print()

    salida = {
        "generado_utc": generado_utc.isoformat(),
        "corte_utc_hora": pm.CORTE_UTC_HORA,
        "metodo": (
            "correlacion de Pearson sobre rendimientos logaritmicos "
            "ln(close_t/close_t-1) de precios de cierre por vela; pares "
            "calculados solo sobre observaciones donde ambos instrumentos "
            "tienen dato real y simultaneo en la ventana (sin relleno, sin "
            "interpolacion)."
        ),
        "ventanas_dias": VENTANAS_DIAS,
        "umbral_min_observaciones_para_no_ser_hueco": UMBRAL_MIN_OBS,
        "umbral_correlacion_g1": UMBRAL_CORRELACION_G1,
        "instrumentos": INSTRUMENTOS,
        "fuentes": FUENTES,
        "prueba_cordura_eurusd_usdchf": {
            "ok": cordura_ok,
            "detalle_por_vela_ventana": cordura_detalle,
        },
        "pares_sobre_umbral_g1": pares_sobre_umbral,
        "metadatos_retornos": metas,
        "matrices": matrices,
    }

    destino = RESULTADOS / "correlaciones_8x8.json"
    destino.write_text(json.dumps(salida, indent=2, ensure_ascii=False))
    print(f"Guardado: {destino}")

    if not cordura_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
