# ATR(14) real, 15m / 1h / 4h — 8 instrumentos (Tarea 02.02.01)

**Agente:** `constructor-datos` (`claude-sonnet-5`). **Fecha de ejecución:** 2026-07-31 (ronda 1,
entrega original) — **CORREGIDO 2026-07-31 (reparación, ronda 1)** tras rechazo de `critico-codigo`,
fallo reproducido de forma independiente por el orquestador — **CORREGIDO OTRA VEZ 2026-07-31 (ronda
2, hallazgo nuevo y distinto)** tras un segundo hallazgo del `critico-codigo`, probado con dos
llamadas reales a Kraken separadas 11 minutos. Ver secciones "Corrección ronda 1" y "Corrección ronda
2" al final: la ronda 2 es la que manda para las 6 celdas de BTCUSD/ETHUSD; el resto del documento
(forex y oro) no cambió en la ronda 2.
**Script:** `03-motor/scripts/precios_mercado.py` (ejecutado entero tras cada reparación, salida
completa leída antes de cada entrega — regla 15 de CLAUDE.md).
**Resultado en bruto:** `04-resultados/atr_15m_1h_4h.json`.
**Datos descargados (NO en git, verificado):** `02-datos/bruto/<INSTRUMENTO>/` — `git status
--porcelain 02-datos/` devuelve vacío tras la descarga completa.

Todo número de esta tabla se calculó sobre precios reales descargados, nunca estimado por la regla
raíz-del-tiempo (regla 7 de la ficha 02.02.01). Donde no fue posible calcular sobre datos reales, se
declara como hueco explícito; no hay ninguno en esta entrega, pero sí ventanas más cortas de lo
pedido en cripto (ver sección de huecos).

**Fórmula exacta de ATR:** `SMA(14)` del *True Range* = `max(H-L, |H-C_prev|, |L-C_prev|)`, sobre las
velas OHLC de cada timeframe. Es una media móvil simple de 14 periodos, no el suavizado de Wilder;
se documenta así para que sea reproducible leyendo la función `atr14` del script.

**Corte único:** 22:00 UTC, usado para fijar el borde de la ventana de ~2 años en cada instrumento.
El remuestreo intradía en sí es en reloj UTC puro (`resample(..., label="left", closed="left")`); el
corte de 22:00 solo fija dónde empieza y termina la ventana de descarga — y, como se explica abajo,
por eso mismo pudo producir velas defectuosas justo en los bordes de esa ventana.

---

## Tabla — 8 instrumentos × 3 velas (recalculada tras la corrección)

Divisas en **pips** (EURUSD/GBPUSD/AUDUSD/USDCHF: 1 pip = 0,0001; USDJPY: 1 pip = 0,01) y valor nativo
entre paréntesis. Oro y cripto en USD directamente.

| Instrumento | Vela | ATR(14) medio | Fuente | Periodo cubierto (UTC) | N.º velas |
|---|---|---|---|---|---|
| **EURUSD** | 15m | 6,86 pips (0,000686) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 47.545 |
| **EURUSD** | 1h  | 14,07 pips (0,001407) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 11.888 |
| **EURUSD** | 4h  | 28,50 pips (0,002850) | HistData.com (M1 ASCII, BID) | 2024-07-30 → 2026-06-26 | 3.077 |
| **GBPUSD** | 15m | 8,28 pips (0,000828) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 47.519 |
| **GBPUSD** | 1h  | 16,95 pips (0,001695) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 11.882 |
| **GBPUSD** | 4h  | 34,14 pips (0,003414) | HistData.com (M1 ASCII, BID) | 2024-07-30 → 2026-06-26 | 3.076 |
| **USDJPY** | 15m | 12,03 pips (0,1203) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 47.485 |
| **USDJPY** | 1h  | 24,86 pips (0,2486) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 11.872 |
| **USDJPY** | 4h  | 50,73 pips (0,5073) | HistData.com (M1 ASCII, BID) | 2024-07-30 → 2026-06-26 | 3.073 |
| **AUDUSD** | 15m | 5,59 pips (0,000559) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 47.486 |
| **AUDUSD** | 1h  | 11,48 pips (0,001148) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 11.873 |
| **AUDUSD** | 4h  | 23,24 pips (0,002324) | HistData.com (M1 ASCII, BID) | 2024-07-30 → 2026-06-26 | 3.074 |
| **USDCHF** | 15m | 5,72 pips (0,000572) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 47.550 |
| **USDCHF** | 1h  | 11,74 pips (0,001174) | HistData.com (M1 ASCII, BID) | 2024-07-29 → 2026-06-26 | 11.890 |
| **USDCHF** | 4h  | 23,88 pips (0,002388) | HistData.com (M1 ASCII, BID) | 2024-07-30 → 2026-06-26 | 3.077 |
| **XAUUSD** | 15m | **7,06 USD/oz** | Dukascopy (oro **al contado**, spot/OTC, BID) | 2024-07-29 → 2026-07-29 | 47.267 |
| **XAUUSD** | 1h  | **14,46 USD/oz** | Dukascopy (oro **al contado**, spot/OTC, BID) | 2024-07-29 → 2026-07-29 | 11.824 |
| **XAUUSD** | 4h  | **28,43 USD/oz** | Dukascopy (oro **al contado**, spot/OTC, BID) | 2024-07-30 → 2026-07-29 | 3.196 |
| **BTCUSD** | 15m | 123,93 USD | Kraken (**XBT/USD real**, no USDT) | 2026-07-24 → 2026-07-31 (**7,4 días, NO 2 años**) | 720 |
| **BTCUSD** | 1h  | 298,69 USD | Kraken (**XBT/USD real**, no USDT) | 2026-07-01 → 2026-07-31 (**30 días, NO 2 años**) | 720 |
| **BTCUSD** | 4h  | 809,13 USD | Kraken (**XBT/USD real**, no USDT) | 2026-04-02 → 2026-07-31 (**120 días, NO 2 años**) | 720 |
| **ETHUSD** | 15m | 5,45 USD | Kraken (**ETH/USD real**, no USDT) | 2026-07-24 → 2026-07-31 (**7,4 días, NO 2 años**) | 720 |
| **ETHUSD** | 1h  | 12,25 USD | Kraken (**ETH/USD real**, no USDT) | 2026-07-01 → 2026-07-31 (**30 días, NO 2 años**) | 720 |
| **ETHUSD** | 4h  | 30,97 USD | Kraken (**ETH/USD real**, no USDT) | 2026-04-02 → 2026-07-31 (**120 días, NO 2 años**) | 720 |

*(Nota — CORREGIDA en la ronda 2, ver esa sección: BTCUSD/ETHUSD son precios de mercado en vivo, y su
reproducibilidad tiene DOS problemas distintos, no uno:*

1. *Re-ejecuciones separadas por MINUTOS cambian poco: Kraken sirve siempre las ~720 velas CERRADAS
   más recientes, así que la ventana se desliza hacia adelante un poco en cada llamada (`desde_utc`/
   `hasta_utc` se desplazan), pero el solape entre dos llamadas próximas en el tiempo es casi total.*
2. *Re-ejecuciones separadas por MÁS que el ancho de la ventana (7,4 días en 15m, 30 días en 1h, 120
   días en 4h) NO COMPARTEN NI UNA SOLA VELA con la ejecución anterior: es una ventana completamente
   distinta, y el ATR resultante puede no parecerse en absoluto al de esta tabla. "Ligeramente" solo
   es cierto dentro de la misma sesión de trabajo; no lo es de un día para otro.*

*BTCUSD/ETHUSD no pasan por `remuestrear` (usan velas nativas de Kraken), así que la corrección de la
ronda 1 (bin de borde) no los tocó. Los 5 pares de forex y el oro sí son deterministas: misma
ventana, mismo número exacto de velas en cualquier re-ejecución mientras no pase un día más.)*

24 de 24 celdas tienen ATR calculado sobre precios reales descargados. Cero celdas estimadas por
raíz-del-tiempo. Cero celdas "sin dato fiable".

**El hueco real no está en las celdas sino en la profundidad histórica de BTCUSD/ETHUSD**: 6 de las 24
celdas (las de cripto) cubren un periodo mucho más corto que los ~2 años del resto. Se explica abajo,
con la prueba ejecutada que lo demuestra.

---

## Qué es EXACTAMENTE cada instrumento (regla 5 del rol, lección L-007)

- **EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF** — precio **BID** de forex minorista agregado de
  HistData.com (1 minuto, ASCII). No es el feed de un broker concreto; sirve para medir movimiento,
  no spread (para spread hace falta otra fuente — tarea 02.02.02).
- **XAUUSD** — oro **al contado (spot/OTC)** de Dukascopy, lado BID. **No es el futuro GC=F de
  COMEX** (lección L-007: en el proyecto anterior se midió el futuro creyendo medir el contado).
- **BTCUSD, ETHUSD** — Bitcoin y Ethereum **contra dólar real** en Kraken (pares `XBTUSD` y `ETHUSD`,
  liquidados en `ZUSD`). **No son USDT/Tether** (lección L-007, mismo error que con el oro pero con
  cripto).

## Prueba de cordura del precio (obligatoria)

| Instrumento | Precio medio en la ventana | Rango esperado | Resultado |
|---|---|---|---|
| EURUSD | 1,1291 | 0,5 – 2,0 | OK |
| GBPUSD | 1,3196 | 0,5 – 2,5 | OK |
| USDJPY | 151,71 | 50 – 300 | OK |
| AUDUSD | 0,6629 | 0,3 – 1,5 | OK |
| USDCHF | 0,8276 | 0,5 – 1,5 | OK |
| **XAUUSD** | **3.596,64 USD/oz** | 500 – 6.000 | **OK — el oro sale en miles, no en decenas** |
| BTCUSD | 65.917,28 USD | 1.000 – 500.000 | OK |
| ETHUSD | 1.908,62 USD | 50 – 50.000 | OK |

Verificación reproducible del divisor de Dukascopy (1000, es decir 3 decimales): la función
`prueba_cordura()` del script comprueba, en cada ejecución, que el precio medio REALMENTE descargado
cae en el rango [500, 6.000] USD/oz — el resultado (`prueba_cordura_ok`, `prueba_cordura_detalle`)
queda en `04-resultados/atr_15m_1h_4h.json` para cada instrumento, así que es un dato recalculable a
partir del artefacto, no una afirmación suelta.

**Corrección (rechazo del crítico, ronda 1):** la entrega anterior de este informe afirmaba que el
divisor se había verificado además contra "el cierre del oro del 2024-01-01 (~2.062,7 USD/oz)". Esa
fecha **no está en la ventana descargada** (la caché de Dukascopy en `02-datos/bruto/XAUUSD/dukascopy_cache/`
empieza en `BID_20240729.bi5`, no en enero de 2024), así que esa cifra no era reproducible desde los
artefactos de este proyecto (regla 20 de CLAUDE.md: ninguna cita entra sin verificación documental).
Se retira esa afirmación; la única prueba de cordura del oro que queda es la de la tabla de arriba,
que sí se recalcula sobre datos realmente descargados.

## Comprobaciones obligatorias del rol

1. **Cobertura** (aprox., asume forex/oro cerrados fin de semana ≈5/7 del calendario, cripto 24/7):
   94–103% en todos los instrumentos y velas (detalle completo en el JSON, campo
   `cobertura_pct_aprox`). Los valores por encima de 100% en velas de 4h son un artefacto de la
   fórmula aproximada de "esperado" cerca de los bordes de la ventana, no datos duplicados (ver
   punto 2).
2. **Duplicados:** cero en los 8 instrumentos (`duplicados_eliminados: 0` en las 8 entradas del
   JSON, verificado por `df.index.duplicated()` tras cada descarga).
3. **Spreads negativos:** no aplica a este entregable. Ninguna de las tres fuentes fijadas entrega
   aquí una serie bid+ask combinada: HistData da solo BID, Dukascopy se usó solo en BID (el ATR mide
   rango de una única serie de precio, no un spread), y Kraken da velas basadas en operaciones
   ejecutadas (ni bid ni ask). El spread bid/ask real es el objeto de la tarea 02.02.02, que sí
   necesita descargar el lado ASK y no se adelanta aquí para no invadir esa tarea (regla 2:
   no se inventan tareas).
4. **Velas inválidas** (High<Low o algún valor ≤0/NaN): cero en los 8 instrumentos
   (`velas_invalidas_eliminadas: 0`).
5. **Reproducibilidad, marcada explícitamente por celda (nuevo, ronda 2):** cada una de las 24 celdas
   del JSON lleva ahora el campo `"reproducible"`. Las 18 celdas de EURUSD/GBPUSD/USDJPY/AUDUSD/
   USDCHF/XAUUSD llevan `"reproducible": true`. Las 6 celdas de BTCUSD/ETHUSD llevan
   `"reproducible": false` más un campo `"motivo_no_reproducible"` con el texto completo (ver sección
   "Corrección ronda 2"). Así, quien consuma el JSON sin leer este informe no puede confundir "no hay
   campo" con "es estable": la ausencia de dato queda descartada como interpretación posible.

**LÍNEA EXPLÍCITA PARA 03.01.10 (testbed de invarianza):** las 6 celdas de BTCUSD/ETHUSD (15m/1h/4h)
**NO pueden formar parte del testbed sintético de invarianza de la tarea 03.01.10 tal como están.**
Ese testbed necesita un resultado de referencia FIJO que se reproduzca tras cualquier cambio del
motor; estas 6 celdas cambian aunque el motor no cambie, porque Kraken no sirve una ventana fija (ver
"Corrección ronda 2"). Para usarlas ahí haría falta congelar antes los datos de entrada: descargar una
vez, guardar esa serie en disco (`02-datos/bruto/BTCUSD/kraken_cache/`, `.../ETHUSD/...`) y hacer que
el testbed lea siempre de ese fichero congelado, nunca repita la llamada en vivo a Kraken. Eso no se
ha hecho aquí porque no es el alcance de esta tarea (regla 2 de CLAUDE.md: no se inventan tareas).

---

## Corrección ronda 1 (rechazo del crítico, fallo reproducido por el orquestador)

**Qué estaba mal.** `construir_1m_histdata`/`construir_1m_dukascopy` filtraban la ventana con
`df.index <= fin`, y `fin` es exactamente un corte de 22:00 UTC. Combinado con
`resample(..., label="left", closed="left")` eso producía dos defectos, ambos en las funciones
COMPARTIDAS que también reutilizará 02.02.03 (no en un sitio de llamada suelto):

- **(a) Vela fantasma:** cuando la fuente publica datos hasta el instante exacto del corte
  (Dukascopy sí llega ahí; HistData hoy no, por su retraso de publicación), el minuto de las
  22:00:00 quedaba solo, abriendo un bin nuevo de 15min/1h con un único minuto de datos, contado
  como vela completa.
- **(b) Vela truncada:** en 4h la rejilla es 0/4/8/12/16/20 UTC, que no coincide con el corte de
  22:00 UTC. El bin que contiene el corte se queda con solo 2 de sus 4 horas nominales y aun así se
  contaba como vela completa. El borde exclusivo por sí solo NO curaba esto: aunque los datos
  reales acaben a las 21:59, el bin de las 20:00 sigue teniendo solo 2 horas de 4.

**Arreglo aplicado (en las tres funciones compartidas, no en el sitio de llamada):**

1. `construir_1m_histdata` y `construir_1m_dukascopy`: el filtro de la ventana pasó de
   `df.index <= fin` a `df.index < fin` (borde superior exclusivo) — cura (a).
2. `remuestrear` ahora acepta `inicio`/`fin` opcionales y, tras el resample, descarta el primer bin
   si empieza antes de `inicio` y/o el último bin si su fin nominal (`inicio_del_bin + ancho_de_vela`)
   cae después de `fin` — cura (b). Esto NO toca huecos naturales de mercado en medio de la serie
   (fines de semana, la pausa diaria de settlement del oro hacia las 21:00–22:00 UTC): esos bins
   conservan los minutos reales que tengan, igual que antes. Solo se recorta el bin de borde cuya
   incompletitud viene de la ventana pedida, no del mercado.
3. **Hallazgo simétrico no pedido explícitamente pero de la misma causa:** `inicio` es también un
   corte de 22:00 UTC, así que el PRIMER bin de 4h de TODOS los instrumentos (no solo XAUUSD) estaba
   igual de truncado (2 de 4 horas) y se contaba como completo. Se corrigió con el mismo mecanismo
   simétrico del punto 2. Por eso el `n_velas` de 4h baja en 1 también en los pares de forex (p.ej.
   EURUSD 4h: 3.078 → 3.077), no solo en XAUUSD.

**Prueba ejecutada de que el arreglo es correcto:** el recálculo independiente del crítico para
XAUUSD 1h dio `n_velas=11824, atr14_medio=14.464676282400184`. Tras el arreglo, el script (ejecutado
entero, sin parches en el sitio de llamada) produce exactamente `n_velas=11824,
atr14_medio=14.464676282400184` — coincide dígito a dígito.

**Comparativa ANTES (entrega rechazada) / DESPUÉS (esta corrección):**

| Instrumento | Vela | ANTES n_velas | DESPUÉS n_velas | ANTES atr14_medio | DESPUÉS atr14_medio | ANTES hasta_utc | DESPUÉS hasta_utc |
|---|---|---|---|---|---|---|---|
| XAUUSD | 15min | 47.268 | 47.267 | ≈7,06 USD/oz (redondeado; el JSON exacto de la ronda rechazada quedó sobreescrito por esta ejecución, no se cita un decimal que no se puede volver a verificar) | 7,064494481192823 | 2026-07-29T22:00:00 (vela fantasma) | 2026-07-29T20:45:00 |
| XAUUSD | 1h | 11.825 | **11.824** | 14,465474469062938 (cifra dada en la orden de reparación, verificada contra la salida que produjo esta entrega antes de corregirse) | **14,464676282400184** | 2026-07-29T22:00:00 (vela fantasma) | 2026-07-29T20:00:00 |
| XAUUSD | 4h | 3.198 | 3.196 | ≈28,43 USD/oz (redondeado; mismo motivo que el 15min de arriba) | 28,42890772406983 | 2026-07-29T20:00:00 (bin truncado, 2h de 4) | 2026-07-29T16:00:00 |
| EURUSD | 15min | 47.545 | **47.545 (sin cambio)** | 0,000686... (sin cambio en los decimales mostrados) | 0,0006864200358254897 (sin cambio) | 2026-06-26T21:45:00 | 2026-06-26T21:45:00 (sin cambio) |

EURUSD 15min queda exactamente igual (mismo `n_velas`, mismo `hasta_utc`, mismo `atr14_medio` hasta
el último dígito guardado en el JSON): confirma que el arreglo no recorta de más cuando la fuente no
llega al corte (criterio explícito de la reparación). El único cambio no trivial en EURUSD es el 4h
(3.078 → 3.077), por el hallazgo simétrico del borde de `inicio` explicado arriba — mismo mecanismo,
no un efecto colateral distinto.

**Nota de trazabilidad:** los valores "ANTES" de `n_velas` y `hasta_utc` de esta tabla se leyeron
directamente del JSON de la ronda rechazada antes de sobreescribirlo con la ejecución corregida. El
`atr14_medio` exacto de esa ronda solo se conserva para XAUUSD 1h porque es la cifra que cita
explícitamente la orden de reparación (verificada por ejecución: reproducida dígito a dígito por la
entrega corregida); para XAUUSD 15min y 4h solo queda el valor redondeado a 2 decimales que constaba
en la versión anterior de este mismo informe, no el JSON completo (regla 12 de CLAUDE.md: no se cita
una precisión que no se puede volver a verificar).

---

## Corrección ronda 2 (hallazgo nuevo del crítico, no una ronda 2 del bin de borde)

**Qué se probó.** El crítico hizo dos llamadas reales al endpoint `GET /0/public/OHLC` de Kraken para
BTCUSD/15min, separadas 11 minutos, y encontró DOS causas distintas de no-reproducibilidad, no una:

- **(a) Ventana deslizante:** dos ejecuciones separadas ~15 minutos dieron `desde_utc`/`hasta_utc`
  desplazados 15 minutos, con `n_velas` constante en 721. Esto es consecuencia directa del límite ya
  documentado en la ronda 1 (Kraken solo sirve las ~720 velas más recientes) y **no tiene arreglo
  posible contra el endpoint público**: no hay parámetro que fije una ventana histórica estable.
- **(b) Vela en formación:** sin cruzar ningún límite de vela, el ATR de la ÚLTIMA fila cambió solo,
  con el mismo `hasta_utc`: `123.91751412429375 -> 123.92354721549634` en 11 minutos. La causa: Kraken
  devuelve **721 filas exactas** en los 6 casos de cripto (720 velas cerradas + 1 vela todavía
  abierta, cuyo High/Low se sigue actualizando en vivo mientras dura el intervalo en curso). Es
  **el mismo defecto que el bin de borde incompleto contado como completo** que se arregló en la
  ronda 1 para forex/oro (`remuestrear`) — aquí entra por la API en lugar de por el filtro de
  ventana, pero el criterio a aplicar es el mismo: un bin que no ha terminado de acumular datos no
  cuenta como vela.

**Arreglo aplicado (solo a `kraken_ohlc`, nada más se tocó):** se descarta la última fila cuando su
timestamp de apertura es posterior al timestamp `data["result"]["last"]` que el propio endpoint
documenta como el cursor de la última vela CERRADA (usado para paginar con `since`). No se recorta
"la última fila" por posición fija, sino contra ese campo, para no depender de que Kraken siga
devolviendo siempre exactamente 721 filas.

**Prueba ejecutada de que el arreglo funciona (causa (b)):**

| | ANTES (n_velas) | DESPUÉS (n_velas) |
|---|---|---|
| BTCUSD 15min | 721 | **720** |
| BTCUSD 1h | 721 | **720** |
| BTCUSD 4h | 721 | **720** |
| ETHUSD 15min | 721 | **720** |
| ETHUSD 1h | 721 | **720** |
| ETHUSD 4h | 721 | **720** |

Las 6 celdas de cripto pasan de 721 a 720 velas, verificado ejecutando `kraken_ohlc` de forma aislada
y el script entero (`main()`), y leyendo el JSON resultante. Nuevos ATR14 medios (calculados sobre las
720 velas cerradas, sin la vela en formación):

| Instrumento | Vela | ATR14 medio (720 velas, corregido) |
|---|---|---|
| BTCUSD | 15m | 123,92806627601533 |
| BTCUSD | 1h | 298,6939785815318 |
| BTCUSD | 4h | 809,1331380076782 |
| ETHUSD | 15m | 5,452330773893716 |
| ETHUSD | 1h | 12,247821782178214 |
| ETHUSD | 4h | 30,967611638714885 |

**Causa (a) NO tiene arreglo y no se ha intentado arreglar.** Descartar la vela en formación cura (b)
pero no (a): la ventana de ~720 velas cerradas sigue desplazándose hacia adelante en cada llamada, sin
foto fija posible contra el endpoint público (mismo límite ya probado y documentado en la ronda 1, ver
más abajo). Es la razón de fondo por la que estas 6 celdas quedan marcadas `"reproducible": false` en
el JSON en lugar de intentar "arreglarlas" del todo.

**Confirmación de que las 18 celdas no-cripto NO se movieron (forex + oro, regla de no tocar lo ya
aceptado):** se comparó, dígito a dígito, el `n_velas` y el `atr14_medio` de las 18 celdas antes y
después de este cambio. Las 18 son idénticas: mismo `n_velas`, mismo `atr14_medio` hasta el último
dígito guardado en el JSON (p. ej. EURUSD 15min: `n_velas=47545`,
`atr14_medio=0.0006864200358254897`, sin cambio; XAUUSD 1h: `n_velas=11824`,
`atr14_medio=14.464676282400184`, sin cambio). Es el resultado esperado: el cambio de esta ronda solo
toca `kraken_ohlc`, que no interviene en ningún instrumento de forex ni en XAUUSD.

---

## Qué fuentes funcionaron y con qué limitación real (probada por ejecución)

### HistData — funcionó, con una restricción de la propia web (no del script)
Verificado por ejecución (`curl` directo, 31/07/2026): **histdata.com solo publica el token de
descarga por mes para el año en curso** (2026); para años ya cerrados (2024, 2023, …) el mes
individual devuelve `tk=""` y **solo funciona el ZIP de año completo**. 2025 (año cerrado pero
reciente) sí tenía token mensual, y aun así se pidió como año completo por eficiencia (1 descarga en
vez de 12). El script detecta esto y usa año completo para cualquier año ya cerrado, cayendo a mensual
solo como último recurso. Por eso el rango de forex llega hasta **2026-06-26**: julio de 2026 (mes en
curso) todavía no tiene ZIP mensual publicado en HistData — se comprobó con el mismo método (`tk`
vacío) y no se sustituyó por otra fuente.

### Dukascopy — funcionó igual de bien, con menos retraso de publicación que HistData
El oro cubre hasta **2026-07-29** (un día completo antes de "hoy"), porque Dukascopy publica el
fichero binario diario (`BID_candles_min_1.bi5`) con mucho menos retraso que el ZIP mensual de
HistData. Formato decodificado: registros de 24 bytes big-endian (tiempo, open, close, low, high,
volumen), precio real = entero/1000 para XAUUSD. Se observó además, al revisar el minuto a minuto
para esta corrección, que el oro al contado tiene una pausa diaria real sin operaciones hacia las
21:00–22:00 UTC (settlement/rollover): eso NO se toca por esta corrección, es un hueco de mercado
real, no un artefacto del script.

### Kraken — funcionó, pero con una profundidad histórica intradía muy inferior a 2 años (PROBADO, no un fallo silencioso)
Esto es el hallazgo más importante de esta tarea y hay que escalarlo:

**Prueba ejecutada (31/07/2026):** el endpoint público `GET /0/public/OHLC` de Kraken devuelve como
máximo **~720 velas** del intervalo pedido, sin importar el parámetro `since`. Se probó explícitamente
con `since=0` (el origen de los tiempos) en el intervalo de 4h y devolvió exactamente las mismas 721
velas que sin `since`: la API **no tiene más histórico que ofrecer** en ese endpoint para intervalos
intradía, no es un problema de paginación.

Profundidad real medida por intervalo:
- 15 min → ~7,4 días (721 velas devueltas por la API)
- 1 hora → ~30 días (721 velas devueltas por la API)
- 4 horas → ~120 días (721 velas devueltas por la API)
- (solo el diario, 1440 min, sí llega a los ~2 años — pero el diario no es una de las 3 velas pedidas)

*(Actualizado en la ronda 2: la API sigue devolviendo 721 filas — eso no cambió y no tiene arreglo —,
pero desde la ronda 2 el script descarta la última porque es la vela EN FORMACIÓN, no cerrada. Por
eso el `n_velas` que queda en el JSON y en la tabla de arriba es 720, no 721: ver sección "Corrección
ronda 2".)*

**Alternativas consideradas y descartadas, con la prueba que las descarta:**
- **`GET /0/public/Trades` (tick a tick) para reconstruir velas propias:** probado — 1.000 trades de
  BTC/USD cubrieron solo ~23 minutos de mercado al ritmo actual. Cubrir 2 años exigiría del orden de
  45.000 llamadas paginadas, inviable en el tiempo de esta tarea y agresivo contra el límite de tasa
  público de Kraken. Descartado por prueba de tiempo/volumen, no por suposición.
- **Volcado histórico masivo de Kraken (`OHLCVT`, todos los pares e intervalos)**: existe, pero se
  distribuye como ZIPs multi-GB con TODOS los pares mezclados en una carpeta de Google Drive
  (enlazada desde `support.kraken.com`), sin URL directa por par/intervalo y sin API — no es
  "descargar con script" en el sentido de la regla 27, sino una descarga manual de varios gigabytes.
  No se ha usado.
- **No se sustituyó por Binance/USDT ni por ningún otro exchange.** La ficha fija Kraken contra
  dólar real (lección L-007) y la regla 8 prohíbe sustituir una fuente en silencio.

**Conclusión sobre este punto, para escalar:** BTCUSD y ETHUSD en 15m/1h/4h están calculados con
datos 100% reales de Kraken (no estimados), pero la ventana histórica es de días/semanas, no de 2
años. Alcanzar 2 años de intradía en cripto por esta vía requeriría autorización para una descarga
manual del volcado `OHLCVT` de Kraken (varios GB) o aceptar la profundidad actual. **Esto no se ha
decidido unilateralmente**: se deja constancia aquí para que el orquestador/CEO decida si se
autoriza esa descarga o si se acepta la ventana corta para G1.

### Yahoo/yfinance
No se ha usado en ningún punto de este script (jubilado, tal como ordena la ficha). El fichero
`03-motor/scripts/atr_local.py` que lo usaba queda intacto pero no se ha reutilizado ni un import; lo
retira el orquestador aparte.

---

## Modelo/respaldo usado

`claude-sonnet-5` (el asignado a `constructor-datos`), sin necesidad de respaldo, también en esta
segunda reparación (ronda 2).
