#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 02.02.01 (WBS) — descargar precios REALES de los 8 instrumentos y
CALCULAR el ATR(14) en velas de 15 minutos, 1 hora y 4 horas.

No estima nada por la regla raiz-del-tiempo: si un dato no se puede calcular
sobre precios reales, se declara hueco (regla 7 de la ficha 02.02.01, regla 14
de CLAUDE.md).

Diseñado para servir tambien a la tarea 02.02.03 (matriz de correlaciones en
ventanas de 3 meses / 1 año / 2 años, corte 22:00 UTC): las funciones de
descarga, limpieza y remuestreo (`construir_1m_histdata`, `construir_1m_dukascopy`,
`kraken_ohlc`, `limpiar`, `remuestrear`) son independientes del calculo de ATR
y estan pensadas para reutilizarse sin duplicar logica (leccion T2: en el
proyecto anterior la logica duplicada divergio). Este script NO implementa la
matriz de correlaciones: esa es otra tarea del WBS y no se inventa aqui
(regla 2 de CLAUDE.md).

FUENTES FIJADAS (no se cambian sin pasar por el WBS/CEO):
  - EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF -> HistData.com, ASCII M1, precio BID
  - XAUUSD  -> Dukascopy, oro AL CONTADO (spot/OTC, bid), NUNCA el futuro GC=F
  - BTCUSD, ETHUSD -> Kraken, PAR REAL CONTRA USD (XBTUSD, ETHUSD), NUNCA USDT

Yahoo/yfinance queda jubilado (lo usaba `atr_local.py`, que no se reutiliza).

CORTE UNICO: se usa 22:00 UTC para fijar el fin/inicio de la ventana de 2 años
de cada instrumento (mismo criterio para los 8). El remuestreo intradia en si
(15m/1h/4h) es en reloj UTC puro; el corte de 22:00 solo fija los bordes de la
ventana, de forma identica para todos.

USO:
    .venv/bin/python 03-motor/scripts/precios_mercado.py

SALIDA:
    02-datos/bruto/<INSTRUMENTO>/...   cache de descargas + serie 1-min limpia
    04-resultados/atr_15m_1h_4h.json   resultado: ATR por instrumento y vela
"""
from __future__ import annotations

import json
import lzma
import re
import struct
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Rutas y guardia del cajon reservado (regla 22 de CLAUDE.md: no se abre nunca)
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[2]
BRUTO = RAIZ / "02-datos" / "bruto"
RESERVADO = (RAIZ / "02-datos" / "reservado").resolve()
RESULTADOS = RAIZ / "04-resultados"


def guardia_no_reservado(path: Path) -> None:
    """Defensa en profundidad: este script no debe escribir ni leer nunca
    dentro de 02-datos/reservado. Se verifica por ejecucion cada vez que se
    construye una ruta de escritura (regla 25 de CLAUDE.md: una barrera se
    verifica ejecutandola, no se da por buena por estar en el codigo)."""
    if RESERVADO == path.resolve() or RESERVADO in path.resolve().parents:
        raise PermissionError(
            f"BLOQUEADO: {path} cae dentro de 02-datos/reservado. "
            "Esa carpeta esta prohibida para todos los agentes salvo el CEO."
        )


CORTE_UTC_HORA = 22          # hora de corte unica, para los 8 instrumentos
VENTANA_DIAS = 730           # ~2 años
HOY_UTC = datetime.now(timezone.utc)

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (bot-trading/02.02.01 data-fetch)"}
SESSION = requests.Session()
SESSION.headers.update(HTTP_HEADERS)


def _get(url: str, **kw) -> requests.Response:
    for intento in range(3):
        try:
            r = SESSION.get(url, timeout=30, **kw)
            return r
        except requests.RequestException:
            if intento == 2:
                raise
            time.sleep(1.5 * (intento + 1))
    raise RuntimeError("inalcanzable")  # pragma: no cover


def _post(url: str, **kw) -> requests.Response:
    for intento in range(3):
        try:
            r = SESSION.post(url, timeout=30, **kw)
            return r
        except requests.RequestException:
            if intento == 2:
                raise
            time.sleep(1.5 * (intento + 1))
    raise RuntimeError("inalcanzable")  # pragma: no cover


def redondear_corte(dt_utc: datetime) -> datetime:
    """Redondea hacia abajo al ultimo corte de 22:00 UTC (<= dt_utc)."""
    dt_utc = dt_utc.astimezone(timezone.utc)
    corte = dt_utc.replace(hour=CORTE_UTC_HORA, minute=0, second=0, microsecond=0)
    if corte > dt_utc:
        corte -= timedelta(days=1)
    return corte


# ---------------------------------------------------------------------------
# 1) HistData.com — EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF (M1 ASCII, BID)
#    Documentado: "timezone of all data is: Eastern Standard Time (EST) time-
#    zone WITHOUT Day Light Savings adjustments" (histdata.com/f-a-q/). EST
#    sin DST = UTC-5 todo el año -> se convierte sumando 5 horas siempre.
# ---------------------------------------------------------------------------
HISTDATA_TZ_OFFSET_H = 5

_TK_RE = re.compile(r'name="tk"\s+id="tk"\s+value="([0-9a-f]*)"')


def _histdata_pagina_url(par: str, year: int, month: int | None) -> str:
    base = f"https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{par.lower()}/{year}"
    return base if month is None else f"{base}/{month}"


def _histdata_tk(par: str, year: int, month: int | None) -> str | None:
    url = _histdata_pagina_url(par, year, month)
    r = _get(url)
    if r.status_code != 200:
        return None
    m = _TK_RE.search(r.text)
    if not m or not m.group(1):
        return None
    return m.group(1)


def histdata_descargar(par: str, year: int, month: int | None) -> Path | None:
    """Descarga el zip de un par/mes (month=None -> año completo) con cache
    en disco. Devuelve la ruta del zip cacheado o None si no hay datos."""
    destino_dir = BRUTO / par / "histdata_cache"
    guardia_no_reservado(destino_dir)
    destino_dir.mkdir(parents=True, exist_ok=True)
    etiqueta = f"{year}" if month is None else f"{year}{month:02d}"
    destino = destino_dir / f"{par}_M1_{etiqueta}.zip"
    if destino.exists() and destino.stat().st_size > 0:
        return destino
    if destino.exists():
        destino.unlink()  # residuo vacio de un intento previo sin datos

    pagina_url = _histdata_pagina_url(par, year, month)
    tk = _histdata_tk(par, year, month)
    if tk is None:
        return None  # ese mes/año no esta publicado todavia

    datemonth = f"{year}" if month is None else f"{year}{month:02d}"
    data = {
        "tk": tk,
        "date": str(year),
        "datemonth": datemonth,
        "platform": "ASCII",
        "timeframe": "M1",
        "fxpair": par.upper(),
    }
    r = _post(
        "https://www.histdata.com/get.php",
        data=data,
        headers={"Referer": pagina_url},
    )
    if r.status_code != 200 or len(r.content) < 1000:
        return None
    destino.write_bytes(r.content)
    return destino


def histdata_a_dataframe(zip_path: Path) -> pd.DataFrame:
    import zipfile

    with zipfile.ZipFile(zip_path) as zf:
        nombre_csv = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(nombre_csv) as f:
            df = pd.read_csv(
                f,
                sep=";",
                header=None,
                names=["ts", "open", "high", "low", "close", "vol"],
                dtype={"ts": str},
            )
    ts = pd.to_datetime(df["ts"], format="%Y%m%d %H%M%S", utc=False)
    ts_utc = ts + pd.Timedelta(hours=HISTDATA_TZ_OFFSET_H)
    out = df[["open", "high", "low", "close"]].astype(float)
    out.index = pd.DatetimeIndex(ts_utc, tz="UTC")
    out.index.name = "ts_utc"
    return out


def construir_1m_histdata(par: str, inicio: datetime, fin: datetime) -> pd.DataFrame:
    """Descarga y concatena todos los meses/años necesarios para cubrir
    [inicio, fin] y devuelve una serie 1-min en UTC, ordenada, sin duplicados."""
    meses = []
    cursor = inicio.replace(day=1)
    while cursor <= fin:
        meses.append((cursor.year, cursor.month))
        cursor = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)

    por_anio: dict[int, list[int]] = {}
    for y, m in meses:
        por_anio.setdefault(y, []).append(m)

    partes = []
    for anio, lista_meses in sorted(por_anio.items()):
        es_anio_pasado = anio < HOY_UTC.year
        # PROBADO POR EJECUCION (31/07/2026): histdata.com solo publica token
        # de descarga MENSUAL para el año en curso; para años ya cerrados
        # (aqui: 2024 y anteriores) el mes individual devuelve tk="" y solo
        # funciona el zip de AÑO COMPLETO. 2025 (año cerrado pero reciente)
        # sí tenia tk mensual, pero se pide igualmente el año completo si se
        # necesitan los 12 meses, por eficiencia (1 descarga en vez de 12).
        if es_anio_pasado:
            zp = histdata_descargar(par, anio, None)
            if zp is not None:
                partes.append(histdata_a_dataframe(zp))
                continue
            # el año completo no estuviera disponible (no deberia pasar para
            # un año ya cerrado): cae a mensual como ultimo recurso
        for mes in lista_meses:
            zp = histdata_descargar(par, anio, mes)
            if zp is not None:
                partes.append(histdata_a_dataframe(zp))

    if not partes:
        return pd.DataFrame(columns=["open", "high", "low", "close"])
    df = pd.concat(partes)
    df = df[~df.index.duplicated(keep="first")].sort_index()
    # Borde superior EXCLUSIVO: `fin` es exactamente un corte de 22:00 UTC.
    # Si se incluye ese instante (<=) y la fuente publica hasta ahi (caso
    # Dukascopy), el minuto de las 22:00:00 queda solo, en su propio minuto,
    # y el resample(closed="left", label="left") lo cuenta como una vela
    # nueva con un solo minuto de datos (vela fantasma). Con "<" ese minuto
    # queda fuera y el ultimo dato real pasa a ser el de las 21:59.
    df = df.loc[(df.index >= pd.Timestamp(inicio)) & (df.index < pd.Timestamp(fin))]
    return df


# ---------------------------------------------------------------------------
# 2) Dukascopy — XAUUSD (oro AL CONTADO, bid, min_1, un fichero por dia)
#    Formato del registro (24 bytes, big-endian): uint32 t_seg_desde_00utc,
#    uint32 open, uint32 close, uint32 low, uint32 high, float32 volumen.
#    Precio real = entero / divisor. divisor=1000 para XAUUSD (3 decimales).
#    NO se afirma aqui un cierre historico concreto como prueba: la ventana
#    descargada (~2 anios hacia atras desde hoy) no incluye 2024-01-01, asi
#    que esa cifra no seria reproducible desde la cache de este script. El
#    divisor se verifica de forma reproducible con `prueba_cordura()` sobre
#    el precio medio REALMENTE descargado (ver RANGO_CORDURA y el campo
#    "prueba_cordura_detalle" del JSON de salida: el oro debe caer en
#    cientos/miles de USD/oz, nunca en decenas).
# ---------------------------------------------------------------------------
DUKASCOPY_DIVISOR = {"XAUUSD": 1000.0}
DUKASCOPY_CONCURRENCIA = 12


def _dukascopy_url(symbol: str, fecha: datetime, lado: str = "BID") -> str:
    return (
        f"https://datafeed.dukascopy.com/datafeed/{symbol}/"
        f"{fecha.year}/{fecha.month - 1:02d}/{fecha.day:02d}/"
        f"{lado}_candles_min_1.bi5"
    )


def dukascopy_dia(symbol: str, fecha: datetime, lado: str = "BID") -> pd.DataFrame | None:
    cache_dir = BRUTO / symbol / "dukascopy_cache"
    guardia_no_reservado(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{lado}_{fecha:%Y%m%d}.bi5"

    if cache_file.exists():
        raw = cache_file.read_bytes()
        if len(raw) == 0:
            return None  # dia sin datos, ya comprobado antes
    else:
        r = _get(_dukascopy_url(symbol, fecha, lado))
        if r.status_code != 200 or len(r.content) == 0:
            cache_file.write_bytes(b"")  # cachea el "no hay dato" tambien
            return None
        raw = r.content
        cache_file.write_bytes(raw)

    try:
        dec = lzma.decompress(raw, format=lzma.FORMAT_ALONE)
    except lzma.LZMAError:
        return None
    n = len(dec) // 24
    if n == 0:
        return None
    divisor = DUKASCOPY_DIVISOR[symbol]
    registros = struct.unpack(f">{'IIIIIf' * n}", dec)
    # unpack en bloques de 6
    t = registros[0::6]
    o = registros[1::6]
    c = registros[2::6]
    lo = registros[3::6]
    hi = registros[4::6]
    v = registros[5::6]
    base = datetime(fecha.year, fecha.month, fecha.day, tzinfo=timezone.utc)
    idx = [base + timedelta(seconds=s) for s in t]
    df = pd.DataFrame(
        {
            "open": [x / divisor for x in o],
            "high": [x / divisor for x in hi],
            "low": [x / divisor for x in lo],
            "close": [x / divisor for x in c],
            "vol": v,
        },
        index=pd.DatetimeIndex(idx, tz="UTC"),
    )
    df.index.name = "ts_utc"
    # descarta las velas de relleno (sin volumen y sin movimiento: mercado
    # cerrado), no son datos reales de operacion.
    sin_movimiento = (df["vol"] == 0) & (df["open"] == df["high"]) & (df["open"] == df["low"]) & (df["open"] == df["close"])
    df = df.loc[~sin_movimiento, ["open", "high", "low", "close"]]
    return df if len(df) else None


def construir_1m_dukascopy(symbol: str, inicio: datetime, fin: datetime, lado: str = "BID") -> pd.DataFrame:
    dias = []
    cursor = inicio.date()
    fin_d = fin.date()
    while cursor <= fin_d:
        dias.append(cursor)
        cursor += timedelta(days=1)

    partes: list[pd.DataFrame] = []
    with ThreadPoolExecutor(max_workers=DUKASCOPY_CONCURRENCIA) as ex:
        futs = {
            ex.submit(dukascopy_dia, symbol, datetime(d.year, d.month, d.day, tzinfo=timezone.utc), lado): d
            for d in dias
        }
        for fut in as_completed(futs):
            r = fut.result()
            if r is not None:
                partes.append(r)

    if not partes:
        return pd.DataFrame(columns=["open", "high", "low", "close"])
    df = pd.concat(partes)
    df = df[~df.index.duplicated(keep="first")].sort_index()
    # Mismo borde superior exclusivo que en construir_1m_histdata: ver el
    # comentario de esa funcion. Aqui es donde el defecto se manifestaba de
    # verdad (Dukascopy SI publica hasta el instante exacto del corte).
    df = df.loc[(df.index >= pd.Timestamp(inicio)) & (df.index < pd.Timestamp(fin))]
    return df


# ---------------------------------------------------------------------------
# 3) Kraken — BTCUSD, ETHUSD (par REAL contra USD, no USDT)
#    LIMITE VERIFICADO POR EJECUCION: el endpoint publico /OHLC solo conserva
#    las ultimas ~720 velas de cada intervalo, sin importar el parametro
#    "since" (probado con since=0): 15m -> ~7,5 dias; 1h -> ~30 dias;
#    4h -> ~120 dias. No hay ventana de 2 años accesible por este endpoint.
#    Ver informe para la traza de esa prueba y las alternativas descartadas.
# ---------------------------------------------------------------------------
KRAKEN_PAR = {"BTCUSD": "XBTUSD", "ETHUSD": "ETHUSD"}
KRAKEN_INTERVALO_MIN = {"15min": 15, "1h": 60, "4h": 240}


def kraken_ohlc(instrumento: str, vela: str) -> pd.DataFrame:
    par = KRAKEN_PAR[instrumento]
    interval = KRAKEN_INTERVALO_MIN[vela]
    cache_dir = BRUTO / instrumento / "kraken_cache"
    guardia_no_reservado(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"ohlc_{vela}.json"

    r = _get(
        "https://api.kraken.com/0/public/OHLC",
        params={"pair": par, "interval": interval},
    )
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(f"Kraken devolvio error para {instrumento}/{vela}: {data['error']}")
    cache_file.write_text(json.dumps(data))

    clave = next(k for k in data["result"] if k != "last")
    filas = data["result"][clave]
    df = pd.DataFrame(
        filas,
        columns=["ts", "open", "high", "low", "close", "vwap", "volume", "count"],
    )
    # Descarta la VELA EN FORMACION: Kraken devuelve 721 filas = 720 velas
    # CERRADAS + 1 todavia abierta, cuyo High/Low se actualiza en vivo
    # mientras el intervalo no termina (PROBADO por el critico con dos
    # llamadas reales separadas 11 minutos, mismo `hasta_utc`, ATR distinto:
    # 123.91751412429375 -> 123.92354721549634). Es el mismo defecto que el
    # bin de borde incompleto ya arreglado en `remuestrear` para forex/oro,
    # solo que aqui entra por la API en vez de por el filtro de ventana; se
    # descarta por coherencia con ese criterio.
    #
    # El propio endpoint documenta `data["result"]["last"]` como el
    # timestamp de apertura de la ULTIMA VELA CERRADA (cursor para "since"
    # en la siguiente llamada). Se filtra contra ese campo -no contra una
    # posicion fija como "quitar la ultima fila"- para no depender de que
    # Kraken siga devolviendo exactamente 721 filas en el futuro.
    ultimo_cerrado_ts = data["result"]["last"]
    df = df[df["ts"] <= ultimo_cerrado_ts]
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
    df.index = pd.to_datetime(df["ts"], unit="s", utc=True)
    df.index.name = "ts_utc"
    return df[["open", "high", "low", "close"]]


# ---------------------------------------------------------------------------
# Limpieza, remuestreo y ATR — comun a todos los instrumentos
# ---------------------------------------------------------------------------
@dataclass
class InformeLimpieza:
    filas_entrada: int = 0
    duplicados_eliminados: int = 0
    velas_invalidas_eliminadas: int = 0  # high<low, o algun valor <=0 / NaN


def limpiar(df: pd.DataFrame) -> tuple[pd.DataFrame, InformeLimpieza]:
    info = InformeLimpieza(filas_entrada=len(df))
    antes = len(df)
    df = df[~df.index.duplicated(keep="first")].sort_index()
    info.duplicados_eliminados = antes - len(df)

    validas = (
        (df["high"] >= df["low"])
        & (df[["open", "high", "low", "close"]] > 0).all(axis=1)
        & df[["open", "high", "low", "close"]].notna().all(axis=1)
    )
    info.velas_invalidas_eliminadas = int((~validas).sum())
    df = df.loc[validas]
    return df, info


REGLA_PANDAS = {"15min": "15min", "1h": "1h", "4h": "4h"}


def remuestrear(
    df1m: pd.DataFrame,
    vela: str,
    inicio: datetime | None = None,
    fin: datetime | None = None,
) -> pd.DataFrame:
    """Remuestrea 1-min a la vela pedida, reloj UTC puro, label='left',
    closed='left'.

    El borde superior exclusivo en `construir_1m_histdata`/`construir_1m_dukascopy`
    arregla la VELA FANTASMA (un unico minuto en su propio bin), pero no cura
    la VELA TRUNCADA: en 4h la rejilla es 0/4/8/12/16/20 UTC y el corte de
    22:00 UTC no coincide con esa rejilla, asi que el primer y/o el ultimo
    bin de la serie puede caer solo PARCIALMENTE dentro de [inicio, fin) sin
    dejar de agregarse como si fuera una vela completa (en 15min/1h el corte
    de 22:00 SI coincide con la rejilla, asi que ahi esto no aplica nunca).

    Si se pasan `inicio`/`fin` (los limites reales de la ventana ya aplicados
    a `df1m`), se descarta:
      - el primer bin si empieza ANTES de `inicio` (le falta la parte inicial
        porque la ventana no llega hasta ahi, no porque el mercado estuviera
        cerrado);
      - el ultimo bin si su fin nominal (inicio_del_bin + ancho_de_vela) cae
        DESPUES de `fin` (le falta la parte final por el mismo motivo).

    Esto NO toca huecos naturales de mercado (fin de semana, dato aun no
    publicado) que caigan en medio de la serie: esos bins conservan los
    minutos reales que tengan, como siempre. Solo se recorta el bin cuyo
    limite nominal se sale de la ventana pedida.
    """
    regla = REGLA_PANDAS[vela]
    r = df1m.resample(regla, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}
    ).dropna()

    if len(r) == 0:
        return r

    ancho = pd.Timedelta(regla)
    if inicio is not None and len(r):
        inicio_ts = pd.Timestamp(inicio)
        if r.index[0] < inicio_ts:
            r = r.iloc[1:]
    if fin is not None and len(r):
        fin_ts = pd.Timestamp(fin)
        if (r.index[-1] + ancho) > fin_ts:
            r = r.iloc[:-1]

    return r


def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df["close"].shift(1)
    a = df["high"] - df["low"]
    b = (df["high"] - prev_close).abs()
    c = (df["low"] - prev_close).abs()
    return pd.concat([a, b, c], axis=1).max(axis=1)


def atr14(df: pd.DataFrame) -> pd.Series:
    """ATR(14) = media movil simple (SMA) del True Range sobre 14 velas.
    Formula explicita y reproducible (no Wilder-smoothing) para que cualquiera
    pueda recalcularla leyendo esta funcion."""
    return true_range(df).rolling(14).mean()


# ---------------------------------------------------------------------------
# Prueba de cordura de precio (obligatoria, regla 6 de la ficha 02.02.01)
# ---------------------------------------------------------------------------
RANGO_CORDURA = {
    "EURUSD": (0.5, 2.0),
    "GBPUSD": (0.5, 2.5),
    "USDJPY": (50, 300),
    "AUDUSD": (0.3, 1.5),
    "USDCHF": (0.5, 1.5),
    "XAUUSD": (500, 6000),      # oro en cientos/miles de USD/oz, NO decenas
    "BTCUSD": (1000, 500000),
    "ETHUSD": (50, 50000),
}


def prueba_cordura(instrumento: str, precio_medio: float) -> tuple[bool, str]:
    lo, hi = RANGO_CORDURA[instrumento]
    ok = lo <= precio_medio <= hi
    msg = f"{instrumento}: precio medio {precio_medio:.4f} vs rango esperado [{lo}, {hi}]"
    return ok, msg


# ---------------------------------------------------------------------------
# Cobertura (aproximada): forex/oro cierran fin de semana (~5/7 del calendario
# abierto), cripto opera 24/7.
# ---------------------------------------------------------------------------
def cobertura_pct(vela: str, n_velas: int, inicio: pd.Timestamp, fin: pd.Timestamp, abierto_247: bool) -> float:
    minutos_vela = {"15min": 15, "1h": 60, "4h": 240}[vela]
    span_min = (fin - inicio).total_seconds() / 60
    fraccion_abierta = 1.0 if abierto_247 else 5 / 7
    esperado = max(span_min / minutos_vela * fraccion_abierta, 1)
    return 100.0 * n_velas / esperado


# ---------------------------------------------------------------------------
# Orquestacion por instrumento
# ---------------------------------------------------------------------------
INSTRUMENTOS_FOREX = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]
INSTRUMENTOS_CRIPTO = ["BTCUSD", "ETHUSD"]
TODOS = INSTRUMENTOS_FOREX + ["XAUUSD"] + INSTRUMENTOS_CRIPTO


def guardar_serie(instrumento: str, nombre: str, df: pd.DataFrame) -> Path:
    destino = BRUTO / instrumento / f"{nombre}.csv.gz"
    guardia_no_reservado(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destino, compression="gzip")
    return destino


def procesar_forex_o_oro(instrumento: str) -> dict:
    fin = redondear_corte(HOY_UTC - timedelta(days=1))  # ayer, para no pedir un dia sin publicar
    inicio = fin - timedelta(days=VENTANA_DIAS)

    if instrumento == "XAUUSD":
        fuente = "Dukascopy (oro al contado / spot OTC, lado BID)"
        # Dukascopy publica con menos retraso que HistData: se prueba el dia
        # de ayer y, si no esta listo, se retrocede.
        cursor = fin
        while dukascopy_dia("XAUUSD", cursor) is None and cursor > inicio:
            cursor -= timedelta(days=1)
        fin = redondear_corte(cursor)
        inicio = fin - timedelta(days=VENTANA_DIAS)
        df1m = construir_1m_dukascopy("XAUUSD", inicio, fin, lado="BID")
    else:
        fuente = "HistData.com (ASCII M1, precio BID, forex minorista agregado)"
        df1m = construir_1m_histdata(instrumento, inicio, fin)

    df1m, info_limpieza = limpiar(df1m)
    guardar_serie(instrumento, "1m", df1m)
    return ensamblar_resultado(
        instrumento, fuente, df1m, info_limpieza, abierto_247=False,
        inicio=inicio, fin=fin,
    )


def procesar_cripto(instrumento: str) -> dict:
    # Kraken no entrega 1-minuto con 2 años de profundidad (ver limite
    # verificado mas arriba): cada vela (15min/1h/4h) se pide YA construida
    # como candela nativa de Kraken, no se remuestrea desde 1-min. Se guarda
    # cada vela por separado (no existe un "1m.csv.gz" real para cripto aqui).
    fuente = "Kraken (par real contra USD, no USDT/Tether)"
    resultado_por_vela = {}
    ultima_info_limpieza = None
    for vela in ["15min", "1h", "4h"]:
        df = kraken_ohlc(instrumento, vela)
        df, info_limpieza = limpiar(df)
        ultima_info_limpieza = info_limpieza
        guardar_serie(instrumento, vela, df)
        resultado_por_vela[vela] = df
    return ensamblar_resultado(
        instrumento, fuente, None, ultima_info_limpieza, abierto_247=True,
        velas_precalculadas=resultado_por_vela,
    )


MOTIVO_NO_REPRODUCIBLE_CRIPTO = (
    "Kraken (endpoint publico /OHLC) solo sirve las ~720 velas CERRADAS mas "
    "recientes de cada intervalo, sin profundidad de 2 anios; la ventana se "
    "desplaza hacia adelante en cada ejecucion (mismo n_velas=720, pero "
    "desde_utc/hasta_utc distintos). Reejecuciones separadas por minutos "
    "cambian poco; reejecuciones separadas por mas que el ancho de la "
    "ventana (7,4 dias en 15m, 30 dias en 1h, 120 dias en 4h) no comparten "
    "ni una sola vela con la ejecucion anterior, y el ATR resultante puede "
    "no parecerse. No usar estas 6 celdas como entrada de un testbed de "
    "invarianza (03.01.10) sin congelar antes los datos (fijar la serie "
    "descargada en disco y leer siempre de ahi, no repetir la llamada a Kraken)."
)


def _marca_reproducibilidad(instrumento: str) -> dict:
    """Declara si la celda es reproducible entre ejecuciones (regla 14/20 de
    CLAUDE.md: quien consuma el JSON -p.ej. el testbed de invarianza de
    03.01.10- no puede adivinarlo). Forex y oro: ventana fija por fecha,
    reproducible mientras no pase un dia. Cripto: ventana deslizante de
    Kraken, NUNCA reproducible entre ejecuciones separadas en el tiempo."""
    if instrumento in INSTRUMENTOS_CRIPTO:
        return {"reproducible": False, "motivo_no_reproducible": MOTIVO_NO_REPRODUCIBLE_CRIPTO}
    return {"reproducible": True}


def ensamblar_resultado(
    instrumento: str,
    fuente: str,
    df1m: pd.DataFrame | None,
    info_limpieza: InformeLimpieza,
    abierto_247: bool,
    velas_precalculadas: dict[str, pd.DataFrame] | None = None,
    inicio: datetime | None = None,
    fin: datetime | None = None,
) -> dict:
    salida: dict = {
        "instrumento": instrumento,
        "fuente": fuente,
        "duplicados_eliminados": info_limpieza.duplicados_eliminados if info_limpieza else None,
        "velas_invalidas_eliminadas": info_limpieza.velas_invalidas_eliminadas if info_limpieza else None,
        "velas": {},
    }

    precios_medios = []
    for vela in ["15min", "1h", "4h"]:
        if velas_precalculadas is not None:
            r = velas_precalculadas[vela]
        else:
            r = remuestrear(df1m, vela, inicio, fin) if df1m is not None and len(df1m) else pd.DataFrame()

        if len(r) < 20:
            salida["velas"][vela] = {
                "hueco": True,
                "motivo": "menos de 20 velas validas tras limpieza: no se calcula ATR sobre una muestra insuficiente",
                "n_velas_disponibles": int(len(r)),
            }
            salida["velas"][vela].update(_marca_reproducibilidad(instrumento))
            continue

        a = atr14(r).dropna()
        precio_medio = float(r["close"].mean())
        precios_medios.append(precio_medio)
        cobertura = cobertura_pct(vela, len(r), r.index[0], r.index[-1], abierto_247)
        salida["velas"][vela] = {
            "hueco": False,
            "atr14_medio": float(a.mean()),
            "atr14_mediana": float(a.median()),
            "atr14_p10": float(a.quantile(0.10)),
            "atr14_p90": float(a.quantile(0.90)),
            "precio_medio": precio_medio,
            "n_velas": int(len(r)),
            "n_atr_validos": int(len(a)),
            "desde_utc": r.index[0].isoformat(),
            "hasta_utc": r.index[-1].isoformat(),
            "cobertura_pct_aprox": round(cobertura, 1),
        }
        salida["velas"][vela].update(_marca_reproducibilidad(instrumento))

    if precios_medios:
        ok, msg = prueba_cordura(instrumento, sum(precios_medios) / len(precios_medios))
        salida["prueba_cordura_ok"] = ok
        salida["prueba_cordura_detalle"] = msg
        if not ok:
            print(f"[CORDURA FALLIDA] {msg}", file=sys.stderr)
    else:
        salida["prueba_cordura_ok"] = None
        salida["prueba_cordura_detalle"] = "sin velas suficientes para evaluar"

    return salida


def main() -> None:
    guardia_no_reservado(BRUTO)  # verificacion explicita al arrancar
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    BRUTO.mkdir(parents=True, exist_ok=True)

    resultados: dict[str, dict] = {}
    for instrumento in INSTRUMENTOS_FOREX + ["XAUUSD"]:
        print(f"--- descargando y calculando {instrumento} ---", flush=True)
        resultados[instrumento] = procesar_forex_o_oro(instrumento)

    for instrumento in INSTRUMENTOS_CRIPTO:
        print(f"--- descargando y calculando {instrumento} ---", flush=True)
        resultados[instrumento] = procesar_cripto(instrumento)

    salida_json = {
        "generado_utc": HOY_UTC.isoformat(),
        "corte_utc_hora": CORTE_UTC_HORA,
        "ventana_dias_objetivo": VENTANA_DIAS,
        "formula_atr": "SMA(14) del True Range = max(H-L, |H-C_prev|, |L-C_prev|)",
        "instrumentos": resultados,
    }
    destino = RESULTADOS / "atr_15m_1h_4h.json"
    destino.write_text(json.dumps(salida_json, indent=2, ensure_ascii=False))
    print(f"\nGuardado: {destino}")

    # tabla resumen por pantalla
    print("\n" + "=" * 100)
    print(f"{'Instrumento':<10}{'vela':<8}{'ATR14 medio':>14}{'precio medio':>14}{'n velas':>10}{'periodo':>28}")
    print("=" * 100)
    for instrumento in TODOS:
        for vela in ["15min", "1h", "4h"]:
            v = resultados[instrumento]["velas"][vela]
            if v.get("hueco"):
                print(f"{instrumento:<10}{vela:<8}{'HUECO':>14}  ({v['motivo']})")
                continue
            periodo = f"{v['desde_utc'][:10]} -> {v['hasta_utc'][:10]}"
            print(
                f"{instrumento:<10}{vela:<8}{v['atr14_medio']:>14.5f}{v['precio_medio']:>14.4f}"
                f"{v['n_velas']:>10}{periodo:>28}"
            )
    print("=" * 100)


if __name__ == "__main__":
    main()
