# Entrega del Brief B (correlaciones e historicos)

# Medición documental: correlaciones y datos históricos de 8 instrumentos (EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD, BTCUSD, ETHUSD)

*Rol: analista de datos. Este informe SOLO mide y documenta. No recomienda instrumentos, no los agrupa por preferencia y no saca conclusiones sobre cuáles "combinan bien". Donde un dato no es fiable u homogéneo, se marca como tal y se explica por qué.*

## TL;DR
- **No existe ninguna fuente pública con una matriz 8×8 homogénea** (mismo periodo y mismo método para las 28 parejas) que combine forex, oro y cripto; la matriz de la Entrega 1 se compone POR BLOQUES con periodos y métodos distintos, y muchas celdas quedan marcadas "sin dato fiable homogéneo".
- Los datos históricos para descargar HOY son abundantes y en su mayoría gratuitos: **Dukascopy** (tick desde 2003 en forex y oro spot; cripto desde 2017), **HistData** (1-min gratis), **TrueFX** (tick desde mayo 2009, sin oro) y, en cripto, **data.binance.vision** y **CryptoDataDownload/Kraken** (1-min gratis).
- Las correlaciones que sí se publican son **inestables**: la misma pareja cambia mucho según ventana y fuente (ej. EURUSD-AUDUSD aparece como 0,33 en una tabla ilustrativa y 0,64 en PortfoliosLab a 12 meses; BTC-ETH 0,85 a 1 año vs 0,66 histórico; la correlación BTC-oro llegó a -0,88 en marzo 2026).

## Key Findings
1. **La matriz homogénea no existe en fuentes públicas.** Las herramientas de forex (Mataf, Myfxbook, Investing.com) no incluyen BTC/ETH; las de cripto (PortfoliosLab, Sharpe.ai) sí mezclan clases pero usan tickers de Yahoo con convenciones distintas (p. ej. yen y franco invertidos). Por eso se entrega por bloques.
2. **Las correlaciones "mecánicas" entre pares con USD común se confirman como hecho medido**, no como opinión: EURUSD-USDCHF es fuertemente negativa y EURUSD-GBPUSD fuertemente positiva en la tabla clásica de referencia.
3. **Inestabilidad temporal grande** en BTC-oro y en USDJPY frente al resto; también las correlaciones forex cambian según la ventana.
4. **Datos históricos: cobertura profunda y gratuita** para los 8 instrumentos, con dos o más fuentes cada uno.
5. **Oro: hay que distinguir spot (XAUUSD) de futuros (GC).** Son instrumentos distintos aunque muy correlacionados (0,82 a 12 meses según PortfoliosLab, con rendimientos diarios).

---

## Cómo está organizado esto (criterio MECE)
Divido en dos entregas independientes que no se solapan:
- **Entrega 1 — Correlaciones**: qué relación de movimiento hay entre los instrumentos.
- **Entrega 2 — Datos históricos**: de dónde bajar los precios para calcularlas o para backtesting.

Dentro de la Entrega 1, parto la matriz en **cinco bloques** según qué clase de activo se cruza, porque cada bloque tiene fuente y periodo distintos (ese es el hueco estructural que la pregunta pedía señalar): (A) forex-forex; (B) forex-oro; (C) forex-cripto; (D) oro-cripto; (E) cripto-cripto. Hay solapamiento inevitable en el oro, que funciona a la vez como "casi divisa" y como materia prima; lo señalo donde aplica.

### Glosario rápido (términos en palabras llanas)
- **Correlación de Pearson**: número entre -1 y +1 que mide si dos cosas suben y bajan a la vez. +1 = se mueven idéntico; -1 = espejo (uno sube, otro baja); 0 = sin relación lineal.
- **Rendimientos diarios**: el cambio porcentual de precio de un día al siguiente. Lo correcto es correlacionar rendimientos, NO precios directos (correlacionar precios infla artificialmente el número, porque dos cosas que suben con el tiempo parecen "correlacionadas" aunque no compartan movimientos diarios).
- **Tick data**: cada cambio de precio individual, uno a uno; el nivel de detalle más fino posible.
- **Bid / ask / mid**: bid = precio al que puedes vender; ask = al que puedes comprar; la diferencia es el *spread*; mid = punto medio entre ambos. Muchos históricos dan solo mid u ocultan el spread.
- **Spot vs futuros**: spot (XAUUSD) es el precio de compra inmediata; futuros (GC) es un contrato con fecha de vencimiento en un mercado organizado (COMEX, 100 onzas por contrato). No son el mismo precio.

---

## ENTREGA 1 — Tabla 1: Matriz de correlaciones 8×8 (POR BLOQUES, NO HOMOGÉNEA)

Orden de filas/columnas: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD, BTCUSD, ETHUSD. Diagonal = 1,00. Cada celda lleva una etiqueta de fuente. Las celdas sin dato fiable homogéneo se marcan "s/d".

| | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| **EURUSD** | 1,00 | 0,91 [M] / 0,59 [P] | 0,82 [M] | 0,33 [M] / 0,64 [P] | -0,97 [M] | s/d | 0,20 [P] | s/d |
| **GBPUSD** | | 1,00 | 0,69 [M] | 0,41 [M] / 0,69 [P] | -0,89 [M] | s/d | s/d | s/d |
| **USDJPY** | | | 1,00 | 0,21 [M] | -0,83 [M] | s/d (inestable) | s/d | s/d |
| **AUDUSD** | | | | 1,00 | -0,29 [M] | s/d | s/d | s/d |
| **USDCHF** | | | | | 1,00 | s/d | s/d | s/d |
| **XAUUSD** | | | | | | 1,00 | ~0,30 [S] (muy inestable) | s/d |
| **BTCUSD** | | | | | | | 1,00 | 0,85 [P] |
| **ETHUSD** | | | | | | | | 1,00 |

**Etiquetas de fuente y su metodología (léase con cuidado; NO son comparables entre sí):**

- **[M] = tabla clásica tipo Mataf/ForexUseful.** Valores: EURUSD-GBPUSD +0,91; EURUSD-USDCHF -0,97; EURUSD-USDJPY +0,82; EURUSD-AUDUSD +0,33; GBPUSD-USDJPY +0,69; GBPUSD-AUDUSD +0,41; GBPUSD-USDCHF -0,89; USDJPY-AUDUSD +0,21; USDJPY-USDCHF -0,83; AUDUSD-USDCHF -0,29. **Método**: correlación sobre movimientos de pares de divisas. **Periodo: NO especificado** en la fuente (es una tabla ilustrativa/instantánea). Herramientas como Mataf y Myfxbook permiten elegir ventana (1 semana, 1 mes, 3 meses, 1 año) y timeframe (H1, D1…), pero publican el número "en vivo", sin fijar un bienio. **Por eso [M] sirve para mostrar el PATRÓN estructural (signos y magnitudes aproximadas), no como medida de un periodo concreto.**
- **[P] = PortfoliosLab.** Método declarado textualmente: **Pearson sobre rendimientos diarios de los últimos 12 meses** ("These values are calculated using daily returns over the previous 12 months"), con precios de Yahoo Finance. Valores confirmados (consulta 30 jul 2026): BTC-ETH **0,85** (1 año; 3 años 0,80; 5 años 0,83; histórico total 0,66 desde ago 2015); EURUSD-BTC **0,20** (1 año; histórico 0,06); EURUSD-AUDUSD **0,64**; GBPUSD-AUDUSD **0,69**; EURUSD-GBPUSD **~0,59** (dato de caché, posiblemente desactualizado). **Ventana = 12 meses, NO 2 años.**
- **[S] = literatura/gestoras sobre BTC-oro.** BTC-oro: media móvil de 90 días a 5 años **~+0,30** (cifra atribuida a Phemex y citada por Spark, spark.money). Extremo negativo documentado: según CryptoQuant (recogido por MEXC/BitcoinWorld, 18 mar 2026), "the Bitcoin-gold correlation plunged to -0.88… the most extreme negative relationship between these assets since November 2022". Otro dato puntual: CoinDesk citó 0,70 en abril 2025. State Street (SSGA, sept 2025) sitúa la correlación estática de largo plazo del oro frente a renta variable en ~0,01 (S&P 500) y ~0,10 (bonos), y la de BTC bastante más alta (0,22-0,35 frente a distintos índices de acciones) — contexto útil pero no son parejas de la matriz. **Método**: rolling 90 días sobre rendimientos; periodos variables. Extremadamente inestable.

**Por qué tantas "s/d" (sin dato fiable homogéneo):**
- **Oro-forex** (XAUUSD contra las 5 divisas): no encontré una fuente que publique estas parejas concretas con Pearson sobre rendimientos diarios y periodo declarado de ~2 años. Lo que existe es la correlación **oro contra el índice dólar DXY**, que el World Gold Council (citado por GoldSilver, jul 2026, con datos de ICE Benchmark Administration para el DXY) describe como que "typically ranged between -0.5 and -0.8 depending on the time period measured"; PortfoliosLab da ^DXY vs oro **-0,42** a 12 meses. Pero DXY no es ninguna de las 5 divisas individuales, así que no relleno esas celdas.
- **Oro-ETH y forex-cripto (casi todas)**: PortfoliosLab tiene páginas por pareja pero no pude recuperar de forma fiable XAUUSD-BTC, XAUUSD-ETH ni la mayoría de forex-cripto; además usa tickers invertidos para yen y franco (JPYUSD=X, CHFUSD=X), lo que **cambia el signo** frente a la convención USDJPY/USDCHF. No mezclo signos.
- **Cripto-forex individuales** más allá de EURUSD-BTC: no hallé medidas fiables homogéneas.

---

## ENTREGA 1 — Discrepancias por ventana y parejas inestables (lo que la pregunta pedía marcar)

1. **EURUSD-AUDUSD**: 0,33 [M, instantánea] vs 0,64 [P, 12 meses]. Casi el doble. Ejemplo claro de cómo cambia según ventana/fuente.
2. **EURUSD-GBPUSD**: 0,91 [M] vs ~0,59 [P, 12 meses]. Diferencia enorme; probablemente por la ventana y por diferencias de feed (Yahoo vs feed de broker) y de hora de corte del "día".
3. **BTC-ETH**: 0,85 (12 meses) vs 0,66 (histórico total) [P]. Sube en el régimen reciente. (La propia página inversa de PortfoliosLab mostraba 0,65 el mismo día por caché, prueba de lo volátil que es incluso el dato publicado.)
4. **BTC-oro**: de ~+0,30 de media a un extremo de **-0,88** en marzo 2026 [S]. La pareja más inestable de todas; cualquier número único es una foto, no una constante.
5. **EURUSD-BTC**: 0,20 (12 meses) vs 0,06 (histórico) [P]. Baja pero creciente en el régimen reciente.
6. **USDJPY frente al resto**: las herramientas forex muestran que el yen cambia de "bando" según el régimen (a veces sigue al riesgo, a veces actúa de refugio); por eso lo marco como inestable aunque [M] dé +0,82 con EURUSD.

## ENTREGA 1 — Nota estructural (hecho medido, no conclusión)
La tabla [M] confirma que varias correlaciones forex son **casi mecánicas por compartir el USD**: EURUSD y USDCHF salen en -0,97 (el USD está "abajo" en un par y "arriba" en el otro, así que se mueven en espejo), y EURUSD-GBPUSD en +0,91 (ambos llevan USD como moneda cotizada, así que un dólar fuerte los baja a los dos). Esto es aritmética de cómo se construye cada par, medida y documentada, no una recomendación.

---

## ENTREGA 2 — Tabla 2: Datos históricos disponibles HOY

Criterio de partición: una fila por (instrumento × fuente), mínimo dos fuentes por instrumento. Columnas: profundidad, vela mínima, coste, calidad/limitaciones. Las fechas de inicio del feed de Dukascopy proceden del listado oficial recogido por Tickstory (cada movimiento de precio queda registrado como tick).

### Forex (EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF) y oro spot (XAUUSD)

| Instrumento | Fuente (URL) | Profundidad | Vela mínima / tick | Coste | Calidad y limitaciones |
|---|---|---|---|---|---|
| EURUSD | Dukascopy (dukascopy.com/swiss/english/marketwatch/historical/) | desde 2003-05-04 | Tick (bid/ask) y barras | Gratis, requiere cuenta demo/JForex o herramienta de exportación | Datos del pool ECN de Dukascopy (un solo agregador suizo), buena calidad, incluye bid y ask. Descarga tick lenta y voluminosa |
| EURUSD | HistData (histdata.com) | ~20+ años atrás | 1-min y tick (resolución 1 seg) | Gratis, sin cuenta (descarga web o FTP/Google Drive) | Feed retail agregado; formato zip por par/año/mes; huecos mínimos declarados; da un solo precio (no bid/ask separado en M1) |
| EURUSD | TrueFX (truefx.com) | desde mayo 2009 | Tick (bid/ask) | Gratis con registro | Agregado de bancos market-makers, top-of-book, marcas de tiempo en milisegundos GMT; algún día ausente y ticks erróneos; la web nueva limita el histórico gratuito |
| GBPUSD | Dukascopy | desde 2003-05-05 | Tick (bid/ask) | Gratis con cuenta | Igual que EURUSD |
| GBPUSD | HistData / TrueFX | ~20 años / desde 2009 | 1-min / tick | Gratis | Igual que arriba; TrueFX incluye GBPUSD entre sus ~15 pares |
| USDJPY | Dukascopy | desde 2003-05-05 | Tick (bid/ask) | Gratis con cuenta | Igual |
| USDJPY | HistData / TrueFX | ~20 años / desde 2009 | 1-min / tick | Gratis | Igual |
| AUDUSD | Dukascopy | desde 2003-08-03 | Tick (bid/ask) | Gratis con cuenta | Igual |
| AUDUSD | HistData / TrueFX | ~20 años / desde 2009 | 1-min / tick | Gratis | Igual |
| USDCHF | Dukascopy | desde 2003-05-05 | Tick (bid/ask) | Gratis con cuenta | Igual |
| USDCHF | HistData / TrueFX | ~20 años / desde 2009 | 1-min / tick | Gratis | Igual |
| XAUUSD (oro SPOT) | Dukascopy | desde 2003-05-04 | Tick (bid/ask) | Gratis con cuenta | **Oro SPOT contra USD (CFD/OTC), NO futuros.** Incluye bid/ask |
| XAUUSD (oro SPOT) | HistData | años atrás | 1-min y tick | Gratis | Incluye el par XAU/USD; feed retail agregado |

**Fuentes API/adicionales para forex y oro (todos los pares anteriores):**
- **Alpha Vantage** (alphavantage.co): FX y oro vía API, diario e intradía; **gratis con clave hasta 25 peticiones/día y 5/min** (verbatim en su web de soporte: "up to 25 requests per day"); el plan de pago más barato son **49,99 USD/mes por 75 peticiones/min**. No da tick.
- **Twelve Data** (twelvedata.com): FX + cripto; plan gratuito **"8 API calls per minute, 800 per day"** (verbatim en su página de precios); plan Grow desde **29 USD/mes**. Intradía y diario.
- **Yahoo Finance** vía yfinance (EURUSD=X, etc.): diario hasta origen gratis; **1-min solo últimos 7 días, cualquier intradía solo últimos 60 días** (hourly hasta 730 días); API no oficial que puede romperse.
- **Stooq**: diario gratis.

### Cripto (BTCUSD, ETHUSD)

| Instrumento | Fuente (URL) | Profundidad | Vela mínima / tick | Coste | Calidad y limitaciones |
|---|---|---|---|---|---|
| BTCUSD | Binance data.binance.vision | BTCUSDT desde ago 2017 | 1-min (klines) y trades tick | Gratis, sin cuenta | **Es BTCUSDT (contra Tether), no USD puro**; zips mensuales/diarios con checksums; mercado 24/7 sin huecos de fin de semana |
| BTCUSD | CryptoDataDownload (cryptodatadownload.com) | desde 2017 | 1-min, 1h, diario | Gratis (CSV); versión "zero-gap" es de pago Plus+ | CSV por exchange (Binance, Kraken, Coinbase); los gratis llevan los huecos del exchange "tal cual" |
| BTCUSD | Kraken (support.kraken.com) | desde inicio del mercado | OHLCVT 1-min y superiores | Gratis (CSV descargable + API) | BTC/USD real (no USDT); API con límites de volumen/velocidad |
| BTCUSD | Dukascopy | BTC/USD desde 2017-05-23 | Tick (bid/ask) | Gratis con cuenta | CFD de Dukascopy, no exchange spot |
| ETHUSD | Binance data.binance.vision | ETHUSDT desde ago 2017 | 1-min y trades tick | Gratis | Igual que BTC; es ETHUSDT |
| ETHUSD | CryptoDataDownload / Kraken | desde 2017 / inicio mercado | 1-min | Gratis (CSV) | Igual que BTC |
| ETHUSD | Dukascopy | ETH/USD desde 2017-12-11 | Tick (bid/ask) | Gratis con cuenta | CFD, no exchange |

**Oro spot vs futuros (aviso para XAUUSD):** Dukascopy y HistData dan **oro SPOT contra USD** (XAUUSD, OTC/CFD). Yahoo `GC=F` y COMEX dan **futuros** (contrato de 100 onzas, con vencimiento y rollover). No son el mismo precio; su correlación diaria es alta pero no perfecta — PortfoliosLab: "The correlation between XAUUSD=X and GC=F is 0.82… calculated using daily returns over the previous 12 months". Si el bot va a operar spot, usar históricos spot, no futuros.

---

## Lista de advertencias sobre calidad y limitaciones
1. **La matriz NO es homogénea.** Mezcla una tabla forex sin periodo declarado [M], PortfoliosLab a 12 meses [P] y literatura BTC-oro con ventanas móviles [S]. No se deben comparar celdas de bloques distintos como si fueran la misma medida.
2. **Ventanas distintas dan números muy distintos** (ejemplos numéricos arriba: EURUSD-AUDUSD 0,33 vs 0,64; BTC-ETH 0,85 vs 0,66; BTC-oro de +0,30 medio a -0,88 puntual).
3. **Forex es un mercado descentralizado**: cada broker/agregador publica precios algo distintos. Para correlación diaria importa poco; para backtesting intradía importa mucho.
4. **Convención de signos**: PortfoliosLab usa yen y franco invertidos (JPYUSD, CHFUSD); el signo sale al revés que en USDJPY/USDCHF. No mezclar sin corregir.
5. **Oro spot ≠ futuros** (ver arriba).
6. **Cripto en USDT ≠ USD**: los klines de Binance son contra Tether; hay una diferencia pequeña frente al dólar real. Kraken y Dukascopy sí dan contra USD.
7. **Datos MT4/MT5** vía broker: calidad variable y huecos según el broker; el History Center de MetaTrader baja datos de MetaQuotes, no de tu broker, con menor calidad de modelado.
8. **Yahoo intradía**: 1-min solo 7 días, intradía 60 días; inútil para 2 años de velas de 1-min.
9. **Alpha Vantage**: límite estricto de 25 peticiones/día en el plan gratuito.
10. **Cifras de terceros no verificadas en primaria**: el rango "-0,5 a -0,8 oro-DXY" (World Gold Council/ICE vía GoldSilver), el "0,70 BTC-oro abril 2025" (CoinDesk) y el "-0,88 marzo 2026" (CryptoQuant vía medios cripto) proceden de fuentes secundarias.

## Recommendations (pasos para quien decida, sin opinar sobre instrumentos)
1. **Si se quiere una matriz 8×8 realmente comparable, hay que calcularla uno mismo.** Ninguna fuente la da homogénea. Ruta recomendada: bajar 1-min de las mismas fechas (~mediados 2024 a mediados 2026) de Dukascopy (forex+oro spot) y Binance/Kraken (cripto), agregar a diario con la MISMA hora de corte, calcular rendimientos diarios y Pearson. Umbral que cambiaría el plan: si se acepta una matriz solo indicativa, basta [M]+[P]; si se va a usar para dimensionar riesgo real, hay que calcularla.
2. **Fijar la hora de corte del "día"** antes de calcular (ver puntos ciegos abajo): afecta sobre todo a las correlaciones con cripto.
3. **Decidir spot o futuros en oro** y bajar el histórico correspondiente; no mezclar.
4. **Recalcular en varias ventanas** (3 meses, 1 año, 2 años) para ver la inestabilidad, no un solo número.
5. **Benchmark de calidad**: si al comparar dos feeds (p. ej. Dukascopy vs HistData) los rendimientos diarios difieren más de una fracción mínima, revisar huecos y hora de cierre antes de fiarse.

## Lo que un experto vería
- **Correlación diaria ≠ correlación intradía.** Un bot de 15m o 1h vive en una escala donde las correlaciones son distintas (y suelen ser más bajas y más ruidosas) que las de rendimientos diarios que publican estas fuentes.
- **Una matriz de 2 años es una foto, no una constante.** Las correlaciones cambian con el régimen de mercado; BTC-oro es el caso extremo (de +0,30 medio a -0,88 en marzo 2026).
- **Parte de la correlación forex es aritmética**, no información de mercado: compartir el USD ya fuerza signos (EURUSD-USDCHF negativo, EURUSD-GBPUSD positivo).
- **Horarios desalineados sesgan la correlación.** Forex opera 24/5, cripto 24/7, el oro spot tiene pausas. Si el "día" se corta a horas distintas para cada uno, los rendimientos diarios no coinciden y la correlación medida se distorsiona, sobre todo forex/oro (que paran el fin de semana) contra cripto (que no para).
- **La fuente del precio forex importa poco para la correlación diaria pero mucho para el backtest intradía**: el spread y los pequeños desajustes entre brokers cambian los resultados a 15m/1h, no tanto la correlación de cierres diarios.
- **Puntos ciegos de la propia pregunta**: (a) no se especifica a qué hora se corta el "día" para los rendimientos, y eso cambia sobre todo las correlaciones con cripto; (b) no se dice si el bot operará varios instrumentos a la vez, que es precisamente el caso para el que sirve una matriz de correlaciones (si opera uno solo cada vez, la matriz es informativa pero no operativa).

## Lista de fuentes (con enlaces y fecha de consulta: 30 julio 2026)
- Mataf, Forex Correlation — mataf.net/en/forex/tools/correlation
- Myfxbook, Forex Correlation — myfxbook.com/forex-market/correlation
- Investing.com, Correlation Calculator — investing.com/tools/correlation-calculator
- ForexUseful (tabla clásica de correlación) — slideshare.net/ForexUseful/forex-currency-correlation
- PortfoliosLab (comparadores por pareja) — portfolioslab.com/tools/stock-comparison/…
- Sharpe.ai, Crypto Correlation Matrix — sharpe.ai/learn/crypto-correlation-matrix
- Spark, Bitcoin Correlation Calculator — spark.money/tools/bitcoin-correlation-calculator
- State Street (SSGA), "Can Bitcoin and gold co-exist in a portfolio?" sept 2025 — ssga.com (PDF)
- CoinDesk, BTC-oro 0,70 (abril 2025) — coindesk.com
- World Gold Council / ICE (rango oro-DXY) citado por GoldSilver — goldsilver.com
- CryptoQuant (BTC-oro -0,88 marzo 2026) vía MEXC/BitcoinWorld — mexc.com
- Dukascopy, Historical Data Export — dukascopy.com/swiss/english/marketwatch/historical/
- Tickstory, rangos de fechas Dukascopy — tickstory.com/dukascopy-historical-data-available-date-ranges/
- HistData — histdata.com
- TrueFX — truefx.com
- Binance public data — github.com/binance/binance-public-data y data.binance.vision
- CryptoDataDownload — cryptodatadownload.com
- Kraken, OHLCVT descargable — support.kraken.com
- Alpha Vantage (soporte y precios) — alphavantage.co / alphavantage.co/premium
- Twelve Data (precios) — twelvedata.com/pricing
- Yahoo Finance / yfinance (límites intradía) — varias guías técnicas (dev.to, algotrading101)
- StoneX / Bitget / MEXC (spot vs futuros oro) — futures.stonex.com, bitget.com, mexc.com
- CME Group, "Gold and the U.S. Dollar" 2025 — cmegroup.com