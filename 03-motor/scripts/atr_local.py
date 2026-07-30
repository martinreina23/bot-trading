#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 02.02.01 / 02.02.02 — Medición REAL de ATR y coste relativo.

Sustituye a la búsqueda de ATR intradía publicado (que no existe de forma fiable).
En vez de buscar el dato, lo calcula sobre precios reales.

USO:  pip install yfinance pandas
      python3 atr_local.py

SALIDA: atr_real.json  +  tablas por pantalla.

LIMITACIONES QUE HAY QUE DECLARAR EN EL INFORME:
- Yahoo Finance limita: velas de 1h hasta 730 días, velas de 15m hasta 60 días.
  Las de 4h se construyen agrupando las de 1h (correcto).
- Los precios de divisas de Yahoo son indicativos, no de un broker concreto: sirven
  para medir movimiento, NO para medir spread.
- El oro se mide con el futuro GC=F como aproximación del contado XAUUSD (hay una
  pequeña diferencia de base entre ambos). Declararlo.
- Cripto: precios de mercado al contado, no de CFD.
"""
import warnings, json, math
warnings.filterwarnings("ignore")
import yfinance as yf
import pandas as pd

INSTR = [
    ("EURUSD=X", "EURUSD", 0.0001, "pips"),
    ("GBPUSD=X", "GBPUSD", 0.0001, "pips"),
    ("JPY=X",    "USDJPY", 0.01,   "pips"),
    ("AUDUSD=X", "AUDUSD", 0.0001, "pips"),
    ("CHF=X",    "USDCHF", 0.0001, "pips"),
    ("GC=F",     "XAUUSD", 1.0,    "USD/oz"),
    ("BTC-USD",  "BTCUSD", 1.0,    "USD"),
    ("ETH-USD",  "ETHUSD", 1.0,    "USD"),
]

# Coste representativo por operación completa (abrir+cerrar), cuenta raw/ECN.
# CORREGIDO respecto al informe del analista: la comisión de 7 USD/lote NO son
# 0,7 pips en USDJPY ni en USDCHF, porque el valor del pip no es 10 USD.
COSTE = {
    "EURUSD": 0.80,   # 0,1 spread + 0,70 comisión
    "GBPUSD": 0.82,   # 0,12 + 0,70
    "USDJPY": 1.16,   # 0,11 + 1,05  <-- corregido (el analista usó 0,90)
    "AUDUSD": 0.85,   # 0,15 + 0,70
    "USDCHF": 0.73,   # 0,17 + 0,56  <-- corregido (el analista usó 0,80)
    "XAUUSD": 0.26,   # 0,19 USD/oz + 0,07 comisión
    "BTCUSD": 28.0,   # spread medio CFD (rango 20-37)
    "ETHUSD": 4.5,    # spread medio CFD (rango 3-7)
}


def atr(df, n=14):
    h, l, c = df["High"], df["Low"], df["Close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def fetch(ticker, interval, period):
    df = yf.download(ticker, interval=interval, period=period,
                     progress=False, auto_adjust=False)
    if df is None or len(df) == 0:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna(subset=["High", "Low", "Close"])


def stats(df, unidad):
    a = atr(df).dropna()
    if len(a) < 50:
        return None
    return {
        "atr_medio": float(a.mean() / unidad),
        "atr_mediana": float(a.median() / unidad),
        "p10": float(a.quantile(0.10) / unidad),
        "p90": float(a.quantile(0.90) / unidad),
        "velas": int(len(df)),
        "desde": str(df.index[0].date()),
        "hasta": str(df.index[-1].date()),
        "precio_medio": float(df["Close"].mean()),
    }


res = {}
for tk, nombre, unidad, ulab in INSTR:
    print(f"descargando {nombre} ...", flush=True)
    r = {"ticker": tk, "unidad": ulab}
    d1h = fetch(tk, "1h", "730d")
    d15 = fetch(tk, "15m", "60d")
    r["1h"] = stats(d1h, unidad) if d1h is not None else None
    r["15m"] = stats(d15, unidad) if d15 is not None else None
    if d1h is not None and len(d1h) > 200:
        d4 = (d1h.resample("4h")
                 .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"})
                 .dropna())
        r["4h"] = stats(d4, unidad)
    else:
        r["4h"] = None
    res[nombre] = r

json.dump(res, open("atr_real.json", "w"), indent=1)

print("\n" + "=" * 96)
print("TABLA 2 — ATR MEDIO REAL (medido, no estimado)")
print("=" * 96)
print(f"{'Instrumento':<10}{'unidad':<9}{'15m':>10}{'1h':>10}{'4h':>10}   {'periodo (velas de 1h)'}")
for _, n, _, _ in INSTR:
    r = res[n]
    g = lambda k: f"{r[k]['atr_medio']:10.2f}" if r.get(k) else "       n/d"
    per = f"{r['1h']['desde']} → {r['1h']['hasta']}  ({r['1h']['velas']} velas)" if r.get("1h") else "sin datos"
    print(f"{n:<10}{r['unidad']:<9}{g('15m')}{g('1h')}{g('4h')}   {per}")

print("\n" + "=" * 96)
print("TABLA 3 — COSTE RELATIVO REAL (%) = coste de operar ÷ ATR medio de la vela")
print("Umbral orientativo: por debajo del 10% hay margen; por encima del 15% es muy difícil ganar")
print("=" * 96)
print(f"{'Instrumento':<10}{'coste':>9}{'15m':>10}{'1h':>10}{'4h':>10}")
for _, n, _, _ in INSTR:
    r = res[n]
    c = COSTE[n]
    def cr(k):
        if not r.get(k):
            return "       n/d"
        return f"{c / r[k]['atr_medio'] * 100:9.1f}%"
    print(f"{n:<10}{c:>9.2f}{cr('15m')}{cr('1h')}{cr('4h')}")

print("\n" + "=" * 96)
print("TABLA 4 — DISPERSIÓN: coste relativo en velas tranquilas (p10) vs. agitadas (p90), en 1h")
print("Importa porque el bot no opera en la media: opera en todos los regímenes")
print("=" * 96)
print(f"{'Instrumento':<10}{'tranquila(p10)':>16}{'media':>10}{'agitada(p90)':>14}")
for _, n, _, _ in INSTR:
    r = res[n].get("1h")
    if not r:
        print(f"{n:<10}{'n/d':>16}"); continue
    c = COSTE[n]
    print(f"{n:<10}{c/r['p10']*100:15.1f}%{c/r['atr_medio']*100:9.1f}%{c/r['p90']*100:13.1f}%")

print("\nGuardado: atr_real.json")
