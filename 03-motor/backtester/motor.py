#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tarea 04.03.07 (WBS) -- motor de backtest, construido desde cero contra
`03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`.

Este fichero contiene los DOS nombres de simbolo que exige R-06(c) de la especificacion (y que el
README del motor declara para que la prueba de sabotaje se pueda ejecutar):

  - `resolver_fill_stop`  -- la funcion de fill de un stop de proteccion (R-02).
  - `calcular_apuntes_swap` -- la funcion de cargo de swap (R-03/C-7).

Las dos son funciones de MODULO (no metodos, no lambdas, no closures locales) y `simular()` las
llama SIEMPRE por su nombre de modulo, nunca via un alias local capturado antes del bucle: es lo
que hace posible interceptarlas con `monkeypatch.setattr(motor, "resolver_fill_stop", ...)` en el
test de sabotaje `test_r06_camino_unico.py` (R-06c).

Convenciones de la especificacion que este fichero da por sentadas (ver el documento para el
detalle): C-1 a C-8 en la seccion 2, R-01 a R-16 en las secciones 3-6.

Todo el dinero se mueve en `decimal.Decimal`, nunca en `float`: los tres casos a lapiz (R-05) piden
la caja final exacta al centimo, sin tolerancia, y un `float` no lo garantiza por construccion
binaria. Los valores que llegan de una fila de pandas (numpy.float64) se convierten SIEMPRE via
`Decimal(str(float(x)))`, nunca `Decimal(float(x))` directo (que arrastraria el ruido binario).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from typing import Callable, Optional

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from configuracion import ConfigCuenta, ConfigInstrumento  # noqa: E402

# ---------------------------------------------------------------------------------------------
# Constantes de mecanica (C-7): NINGUNA cifra de MERCADO vive aqui (C-8) -- esto es estructura del
# calendario (que dia es miercoles, a que hora UTC corta el swap), no un precio ni una tasa.
# ---------------------------------------------------------------------------------------------
DIA_MIERCOLES = 2                    # datetime.weekday(): lunes=0 ... domingo=6
DIAS_CARGO_SWAP = frozenset({0, 1, 2, 3, 4})   # lunes a viernes (C-7)
HORA_CORTE_SWAP_UTC = 22             # C-7: r_D = D 22:00:00 UTC


def _dec(x) -> Decimal:
    """Convierte un valor numerico (incluido numpy.float64 de una fila de pandas) a Decimal via
    su representacion decimal mas corta y exacta -- nunca `Decimal(float(x))` directo."""
    if isinstance(x, Decimal):
        return x
    return Decimal(str(float(x)))


# ---------------------------------------------------------------------------------------------
# Estructuras del registro de salida (R-15: registro por operacion + serie de caja)
# ---------------------------------------------------------------------------------------------
@dataclass
class Apunte:
    ts: pd.Timestamp
    tipo: str          # "resultado_precio" | "comision" | "swap"
    importe: Decimal    # signo C-3: negativo = coste, positivo = credito


@dataclass
class Operacion:
    direccion: str            # "largo" | "corto"
    ts_senal: pd.Timestamp
    ts_entrada: pd.Timestamp
    precio_entrada: Decimal
    bid_entrada: Decimal      # C-7: base del swap = nocional al BID de entrada, no al precio pagado
    onzas: Decimal
    riesgo_nominal: Decimal
    nivel_stop: Decimal
    ts_salida: Optional[pd.Timestamp] = None
    precio_salida: Optional[Decimal] = None
    motivo_salida: Optional[str] = None   # "señal" | "stop"
    apuntes: list = field(default_factory=list)

    @property
    def resultado_neto(self) -> Decimal:
        """R-01(c): suma de TODOS los apuntes de la operacion (resultado de precio, comision,
        swap). `caja_final - caja_inicial` es exactamente la suma de esto sobre todas las
        operaciones, sin residuo -- no hay ningun cargo que mueva la caja sin ser un Apunte."""
        total = Decimal("0")
        for a in self.apuntes:
            total += a.importe
        return total


@dataclass
class OperacionRechazada:
    ts_senal: pd.Timestamp
    direccion: str
    motivo: str


@dataclass
class Decision:
    """Lo que devuelve una estrategia en cada vela cerrada (R-14)."""
    accion: str                                  # "abrir_largo" | "abrir_corto" | "cerrar" | "nada"
    distancia_stop: Optional[Decimal] = None      # obligatorio si accion es "abrir_*"


@dataclass
class SimulacionResultado:
    caja_inicial: Decimal
    caja_final: Decimal
    operaciones: list       # list[Operacion], cerradas
    rechazadas: list        # list[OperacionRechazada]
    serie_caja: list        # list[tuple[pd.Timestamp, Decimal]]


# Contrato de estrategia (R-14): recibe SOLO velas cerradas hasta t, la posicion abierta (o None)
# y el timestamp de cierre de la ultima vela visible; devuelve una Decision que se ejecuta en la
# apertura de t+1. No se le pasa nunca una vela que no haya cerrado.
Estrategia = Callable[[pd.DataFrame, Optional[Operacion], pd.Timestamp], Decision]


# ---------------------------------------------------------------------------------------------
# R-02 -- la funcion de fill de un stop de proteccion. UN SOLO camino para largo y corto (R-06):
# la direccion es un parametro, no una rama duplicada en otro fichero ni otro metodo.
# ---------------------------------------------------------------------------------------------
def resolver_fill_stop(
    direccion: str,
    nivel: Decimal,
    o_bid: Decimal,
    h_bid: Decimal,
    l_bid: Decimal,
    spread: Decimal,
    es_vela_entrada: bool,
) -> Optional[Decimal]:
    """R-02/C-5/C-6: precio de fill de un stop de proteccion dentro de una vela, o None si no
    dispara. Nunca ejecuta a mejor precio que el nivel disparado.

    Largo (protege una compra, sale vendiendo al bid -- C-6): el stop se evalua contra el bid.
      - Si la vela abre ya por debajo del nivel (hueco), ejecuta en la apertura (peor que el
        nivel). Excepcion: en la propia vela de entrada NO se comprueba el hueco de apertura,
        porque esa apertura ya se ha usado para la entrada (C-5: "el stop se evalua desde la
        propia vela de entrada, tras la apertura").
      - Si no hay hueco pero el low toca o cruza el nivel, ejecuta EXACTAMENTE en el nivel.
      - Si no, no dispara.

    Corto (protege una venta, sale recomprando al ask sintetico = bid + spread -- C-2/C-6):
    exactamente simetrico, evaluado contra el ask sintetico en vez del bid.
    """
    if direccion == "largo":
        if not es_vela_entrada and o_bid <= nivel:
            return o_bid
        if l_bid <= nivel:
            return nivel
        return None
    if direccion == "corto":
        ask_o = o_bid + spread
        ask_h = h_bid + spread
        if not es_vela_entrada and ask_o >= nivel:
            return ask_o
        if ask_h >= nivel:
            return nivel
        return None
    raise ValueError(f"direccion desconocida: {direccion!r}")


# ---------------------------------------------------------------------------------------------
# R-03/C-7 -- la funcion de cargo de swap. UN SOLO camino para largo y corto (R-06).
# ---------------------------------------------------------------------------------------------
def calcular_apuntes_swap(
    direccion: str,
    ts_entrada: pd.Timestamp,
    ts_cierre_atribuido: pd.Timestamp,
    bid_entrada: Decimal,
    onzas: Decimal,
    cfg: ConfigInstrumento,
) -> list:
    """R-03/C-7: un `Apunte` de swap por cada corte `r_D` (D de lunes a viernes, r_D = D 22:00:00
    UTC) que la posicion cruza abierta -- `ts_entrada < r_D < ts_cierre_atribuido`, estrictamente
    en los dos lados (si la posicion abre o cierra EXACTAMENTE en el corte, ese corte no se
    carga: no hay noche completa cruzada). El miercoles carga el triple (`mult=3`); el resto,
    `mult=1`. Sabado y domingo nunca generan corte (no estan en `DIAS_CARGO_SWAP`).

    Base del calculo (PROVISIONAL, hueco H-1 de la especificacion): nocional al BID de entrada
    (`bid_entrada * onzas`), no al precio pagado (que en el largo ya incluye el spread).

    Tasa: `cfg.swap_largo_anual` o `cfg.swap_corto_anual` segun `direccion` (R-03: direcciones
    independientes, con signo C-3), convertida a tasa por noche con `% anual / 365` (conversion
    lineal, el metodo declarado de `coste_swap.md`).
    """
    tasa_anual = cfg.swap_largo_anual if direccion == "largo" else cfg.swap_corto_anual
    tasa_noche_pct = tasa_anual / Decimal(365)
    base = bid_entrada * onzas

    apuntes: list = []
    dia = pd.Timestamp(ts_entrada).normalize()
    ultimo_dia = pd.Timestamp(ts_cierre_atribuido).normalize()
    un_dia = pd.Timedelta(days=1)
    while dia <= ultimo_dia:
        if dia.weekday() in DIAS_CARGO_SWAP:
            r_d = dia + pd.Timedelta(hours=HORA_CORTE_SWAP_UTC)
            if ts_entrada < r_d < ts_cierre_atribuido:
                mult = 3 if dia.weekday() == DIA_MIERCOLES else 1
                importe = Decimal(mult) * (tasa_noche_pct / Decimal(100)) * base
                apuntes.append(Apunte(ts=r_d, tipo="swap", importe=importe))
        dia += un_dia
    return apuntes


# ---------------------------------------------------------------------------------------------
# R-04/R-10 -- dimensionado por riesgo, redondeo a la baja al paso de lote.
# ---------------------------------------------------------------------------------------------
def dimensionar(riesgo_usd: Decimal, distancia_stop: Decimal, paso_lote: Decimal) -> tuple:
    """R-04: onzas = riesgo_por_operacion / distancia_de_stop_por_onza, redondeado A LA BAJA al
    paso de lote (R-10). Si el tamaño calculado queda por debajo del paso de lote, no abre:
    devuelve `(Decimal("0"), Decimal("0"))`. El riesgo nominal registrado es el del tamaño
    REALMENTE abierto (onzas * distancia), no el teorico."""
    if distancia_stop <= 0:
        raise ValueError("distancia_stop debe ser > 0")
    onzas_teoricas = riesgo_usd / distancia_stop
    pasos = (onzas_teoricas / paso_lote).to_integral_value(rounding=ROUND_FLOOR)
    onzas = pasos * paso_lote
    if onzas < paso_lote:
        return Decimal("0"), Decimal("0")
    riesgo_nominal = onzas * distancia_stop
    return onzas, riesgo_nominal


# ---------------------------------------------------------------------------------------------
# C-6 -- precio de entrada/salida a mercado (sin stop). Un solo lugar, parametrizado por direccion.
# ---------------------------------------------------------------------------------------------
def _precio_entrada_mercado(direccion: str, open_bid: Decimal, spread: Decimal) -> Decimal:
    """C-6: largo compra al ask (bid+spread); corto vende al bid."""
    return open_bid + spread if direccion == "largo" else open_bid


def _precio_salida_mercado(direccion: str, open_bid: Decimal, spread: Decimal) -> Decimal:
    """C-6: largo vende al bid; corto recompra al ask (bid+spread)."""
    return open_bid if direccion == "largo" else open_bid + spread


def _nivel_stop_desde_distancia(
    direccion: str, open_bid_entrada: Decimal, distancia: Decimal, spread: Decimal
) -> Decimal:
    """Decision de diseño DECLARADA (04.03.07, no viene de un caso a lapiz con corto: CL-1/CL-2/
    CL-2b son los tres largos -- R-02(e) da el nivel de un corto directamente, nunca derivado de
    una distancia). Para el largo si esta fijada sin ambiguedad por los tres casos a lapiz:
    `nivel = open_bid_entrada - distancia`, en BID puro, SIN sumar el spread -- confirmado por
    CL-2b, cuya nota dice explicitamente que la perdida realizada excede el riesgo nominal en el
    spread precisamente porque el nivel no lo incluye.

    Para el corto se aplica la misma convencion por simetria (distancia medida en BID-equivalente
    desde el bid de la vela de entrada) y se traduce a ask sintetico sumando el spread, porque
    `resolver_fill_stop` compara el corto contra ask (R-02): `nivel = open_bid_entrada + distancia
    + spread`. Ningun requisito de la especificacion fija esta cifra con un caso a lapiz corto, asi
    que queda documentada aqui en vez de adivinada en silencio (regla 6 de CLAUDE.md)."""
    if direccion == "largo":
        return open_bid_entrada - distancia
    return open_bid_entrada + distancia + spread


def _cerrar_posicion(pos: Operacion, ts_cierre: pd.Timestamp, precio: Decimal, motivo: str,
                      cfg: ConfigInstrumento) -> None:
    """Cierra `pos` in-place: registra el precio y motivo de salida y los tres apuntes fechados
    (R-01) -- resultado de precio, comision (ida y vuelta, cargada al cierre) y swap (R-03/C-7,
    via `calcular_apuntes_swap`, el unico camino). Un solo lugar para largo y corto (R-06): el
    signo del resultado de precio es el unico punto que depende de la direccion."""
    pos.ts_salida = ts_cierre
    pos.precio_salida = precio
    pos.motivo_salida = motivo

    signo = Decimal(1) if pos.direccion == "largo" else Decimal(-1)
    resultado_precio = signo * (precio - pos.precio_entrada) * pos.onzas
    pos.apuntes.append(Apunte(ts=ts_cierre, tipo="resultado_precio", importe=resultado_precio))

    comision = -(cfg.comision * pos.onzas)
    pos.apuntes.append(Apunte(ts=ts_cierre, tipo="comision", importe=comision))

    pos.apuntes.extend(
        calcular_apuntes_swap(pos.direccion, pos.ts_entrada, ts_cierre, pos.bid_entrada,
                               pos.onzas, cfg)
    )


# ---------------------------------------------------------------------------------------------
# El bucle principal.
# ---------------------------------------------------------------------------------------------
def simular(
    velas: pd.DataFrame,
    estrategia: Estrategia,
    cfg_instrumento: ConfigInstrumento,
    cfg_cuenta: ConfigCuenta,
    ancho_vela: pd.Timedelta = pd.Timedelta(hours=4),
) -> SimulacionResultado:
    """Motor de simulacion (R-01 a R-16). `velas` es un DataFrame con indice = apertura de cada
    vela (UTC) y columnas open/high/low/close en BID (C-2), ya en la granularidad que se quiera
    simular -- normalmente el resultado de `datos.construir_velas_4h` (R-06a/R-08), pero los
    casos a lapiz de la seccion 7 de la especificacion se construyen directamente en 4h porque las
    tablas YA vienen en esa vela.

    Orden por vela (C-4, C-5, R-14), sin excepcion:
      1. Ejecuta en la APERTURA de esta vela la decision tomada al CIERRE de la anterior (si hay
         una orden pendiente de "abrir" y la cuenta esta plana, o de "cerrar" y hay posicion).
      2. Si sigue habiendo posicion abierta (la que ya estaba, o la que se acaba de abrir en el
         paso 1), comprueba el stop DENTRO de esta vela (R-02), con la regla especial de la vela
         de entrada (C-5).
      3. Pregunta a la estrategia, que SOLO ve velas cerradas hasta esta (R-14); su decision queda
         pendiente para ejecutarse en la apertura de la vela siguiente.
    """
    if len(velas) == 0:
        raise ValueError("simular() necesita al menos una vela")

    spread = cfg_instrumento.spread
    riesgo_usd = cfg_cuenta.riesgo_por_operacion_usd
    paso_lote = cfg_cuenta.paso_lote

    caja = cfg_cuenta.capital_inicial
    posicion: Optional[Operacion] = None
    entrada_idx: Optional[int] = None
    operaciones: list = []
    rechazadas: list = []
    serie_caja: list = [(velas.index[0], caja)]
    pendiente: Optional[Decision] = None
    ts_senal_pendiente: Optional[pd.Timestamp] = None

    for i in range(len(velas)):
        fila = velas.iloc[i]
        ts_open = velas.index[i]
        o_bid = _dec(fila["open"])
        h_bid = _dec(fila["high"])
        l_bid = _dec(fila["low"])

        # 1) Ejecuta en la apertura la decision del cierre anterior (C-4: sin mirada al futuro).
        if pendiente is not None and pendiente.accion in ("abrir_largo", "abrir_corto") and posicion is None:
            if pendiente.distancia_stop is None:
                raise ValueError("una decision de apertura necesita distancia_stop")
            direccion = "largo" if pendiente.accion == "abrir_largo" else "corto"
            precio_entrada = _precio_entrada_mercado(direccion, o_bid, spread)
            onzas, riesgo_nominal = dimensionar(riesgo_usd, pendiente.distancia_stop, paso_lote)
            if onzas <= 0:
                rechazadas.append(OperacionRechazada(
                    ts_senal=ts_senal_pendiente, direccion=direccion,
                    motivo="tamaño calculado inferior al lote mínimo de 0,1 oz",
                ))
            else:
                nivel_stop = _nivel_stop_desde_distancia(direccion, o_bid, pendiente.distancia_stop, spread)
                posicion = Operacion(
                    direccion=direccion, ts_senal=ts_senal_pendiente, ts_entrada=ts_open,
                    precio_entrada=precio_entrada, bid_entrada=o_bid, onzas=onzas,
                    riesgo_nominal=riesgo_nominal, nivel_stop=nivel_stop,
                )
                entrada_idx = i
        elif pendiente is not None and pendiente.accion == "cerrar" and posicion is not None:
            precio_salida = _precio_salida_mercado(posicion.direccion, o_bid, spread)
            _cerrar_posicion(posicion, ts_open, precio_salida, "señal", cfg_instrumento)
            caja += posicion.resultado_neto
            serie_caja.append((ts_open, caja))
            operaciones.append(posicion)
            posicion = None
            entrada_idx = None
        pendiente = None
        ts_senal_pendiente = None

        # 2) Comprueba el stop DENTRO de esta vela (R-02/C-5), si hay posicion abierta.
        if posicion is not None:
            es_entrada = (i == entrada_idx)
            fill = resolver_fill_stop(
                posicion.direccion, posicion.nivel_stop, o_bid, h_bid, l_bid, spread, es_entrada,
            )
            if fill is not None:
                _cerrar_posicion(posicion, ts_open, fill, "stop", cfg_instrumento)
                caja += posicion.resultado_neto
                serie_caja.append((ts_open, caja))
                operaciones.append(posicion)
                posicion = None
                entrada_idx = None

        # 3) Pregunta a la estrategia (R-14: solo ve velas cerradas hasta i).
        ts_cierre_visible = ts_open + ancho_vela
        decision = estrategia(velas.iloc[: i + 1], posicion, ts_cierre_visible)
        if decision.accion == "nada":
            continue
        if decision.accion in ("abrir_largo", "abrir_corto") and posicion is not None:
            continue
        if decision.accion == "cerrar" and posicion is None:
            continue
        pendiente = decision
        ts_senal_pendiente = ts_cierre_visible

    return SimulacionResultado(
        caja_inicial=cfg_cuenta.capital_inicial,
        caja_final=caja,
        operaciones=operaciones,
        rechazadas=rechazadas,
        serie_caja=serie_caja,
    )
