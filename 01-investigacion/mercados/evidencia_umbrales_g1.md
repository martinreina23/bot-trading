# Evidencia externa para los umbrales de la puerta G1

**Agente:** `investigador` (`claude-sonnet-5`). No fue necesario el respaldo (`claude-haiku-4-5-20251001`): el modelo principal
respondió sin rechazos.
**Fecha de la investigación:** 31/07/2026. **Apoya a:** 01.01.02 ("Aprobar criterios de la puerta G1"). **No elige mercado ni
vela** — eso es de G1 con el CEO. Este documento entrega números, método y fuentes externas, más el contraste con lo ya
calculado dentro del proyecto (`coste_relativo.md`, `coste_operar.md`, `coste_swap.md`, `correlaciones_8x8.md`, leídos
enteros antes de empezar, para no repetir trabajo).

**Regla de fuentes aplicada:** cada afirmación numérica lleva fuente primaria con fecha, o se declara hueco. Cuando dos
fuentes se contradicen se dan las dos, sin promediar. Se distingue siempre **PUBLICADO** (fuente primaria con autor/fecha
identificable) de **PRÁCTICA COMÚN SIN RESPALDO** (lo que dicen blogs/foros de forma repetida pero sin un estudio o libro
citable detrás). Un dato de foro (Elite Trader, Forex Factory, blogs educativos genéricos) nunca cuenta como una de las
2 fuentes independientes exigidas; se usa como máximo como ilustración de orden de magnitud, marcado como tal.

**Verificación documental de fuentes primarias (regla 9, nivel 2):** los tres PDF citados como fuente primaria en este
informe (Bailey & López de Prado 2014; especificación de commodities de IC Markets; especificación de criptomonedas de IC
Markets) se leyeron **completos**, con la herramienta de lectura de PDF, no a través del resumen de un modelo pequeño de
`WebFetch`. Esto importa: un primer intento de `WebFetch` sobre el PDF de Bailey/López de Prado devolvió una cifra
("300 operaciones independientes requeridas al 95%") que **no aparece en ningún lugar del paper real** — se descarta
explícitamente en la sección 2 y se documenta el hallazgo como aviso metodológico para el resto del proyecto.

---

## 1. Umbral de coste: ¿qué relación coste/volatilidad o coste/borde se considera el límite de lo operable?

**Hallazgo central: no se encontró ninguna fuente externa (académica, de broker o de trading sistemático) que exprese el
umbral literalmente como "el coste no debe superar el X% del movimiento medio de la vela (ATR)".** Es la forma exacta que
usa este proyecto en `coste_relativo.md` (criterio 1 de G1, ≤10-15% del ATR), pero las fuentes externas localizadas miden
el coste **contra el retorno/borde esperado de la estrategia**, no contra la volatilidad bruta del instrumento. Son
magnitudes distintas: un mismo coste absoluto puede ser el 5% del ATR y el 200% del borde esperado de una estrategia con
poca ventaja, o al revés.

### Las dos anclas externas encontradas (coste vs. RETORNO esperado, no vs. ATR)

1. **Robert Carver — regla del "límite de velocidad" (Sharpe Ratio).** Cita textual verificada por lectura de la fuente
   primaria: *"SPEED LIMIT: DO NOT SPEND MORE THAN ONE THIRD OF YOUR EXPECTED PRE-COST RETURNS ON COSTS"*, con la
   fórmula operativa *"Max cost per year = Expected SR / 3"*. **Fuente:** Robert Carver, "How fast should we trade?",
   blog personal `qoppac.blogspot.com`, publicado 02/04/2020: https://qoppac.blogspot.com/2020/04/how-fast-should-we-trade.html
   (leído 31/07/2026).
2. **Robert Carver — techo absoluto en su libro.** Una segunda fuente (resumen del libro, no el libro mismo) afirma que en
   *Systematic Trading* (2015), capítulo 12 ("Speed and Size"), Carver fija un techo de **0,13 unidades de Sharpe Ratio al
   año** de coste como límite operativo, lo que a una volatilidad objetivo del 25% equivale a ~3,35% anual de coste sobre
   capital. **Fuente (secundaria, no verificada por lectura directa del libro esta sesión):** "Systematic Trading 5 —
   Speed", the7circles.uk: https://the7circles.uk/systematic-trading-5-speed/ (consultado 31/07/2026). Se cita con esta
   reserva explícita.
3. **Ernest Chan — coste vs. borde esperado, con un ejemplo verificable.** En su blog sobre reversión a la media,
   confirmado por lectura directa: sin costes la estrategia tenía Sharpe 4,8; **"even after subtracting 10 b.p. round-trip
   transaction cost, it is still at 3.5"**. **Fuente:** Ernest P. Chan, "The enduring profitability of mean-reversion
   strategies", `epchan.blogspot.com`, dic-2008: https://epchan.blogspot.com/2008/12/enduring-profitability-of-mean.html
   (leído 31/07/2026). **Aviso:** una cita muy repetida en resúmenes de terceros ("edge 5bps, cost 4bps = hobby, not a
   strategy") **no aparece en esta entrada del blog** ni se pudo localizar en ninguna fuente primaria durante esta sesión;
   se descarta explícitamente, no se cita.

### Regla de foro (orden de magnitud, no fuente primaria)

Varios hilos de Elite Trader y sitios educativos genéricos repiten que la expectativa neta debe ser ≥1,5-2× el coste medio
por operación para considerarse un sistema "sano". Es **PRÁCTICA COMÚN SIN RESPALDO**: ningún hilo cita un estudio, y no
cuenta como fuente independiente verificable.

### Conclusión de la pregunta 1

El criterio interno del proyecto (coste ≤10-15% del ATR) **no tiene un precedente externo directo encontrado**. Los dos
anclajes externos más sólidos (Carver: coste ≤1/3 del retorno esperado en SR; Chan: coste debe dejar un Sharpe positivo
claro tras restarlo) miden coste **relativo al retorno/edge**, no a la volatilidad. Esto es información útil para quien
decida en G1: el criterio 1 de este proyecto mide algo distinto de lo que mide la literatura citada aquí, y las dos
magnitudes no son intercambiables sin conocer el borde esperado de la estrategia (que aún no existe, porque el bot no
está construido). **Hueco declarado:** no hay una fuente externa de "coste ≤ X% del ATR" con ese nombre exacto.

---

## 2. Tamaño de muestra: ¿cuántas operaciones necesita un backtest?

**Hallazgo central, y una corrección importante de un dato ya circulante:** el Deflated Sharpe Ratio (DSR) de Bailey y
López de Prado **no da una cifra de "número mínimo de operaciones"**. Su variable N es el **número de ensayos
independientes** (variantes de estrategia probadas), no el número de operaciones dentro de un solo backtest. Confundir
las dos cosas es un error que circula en resúmenes de terceros.

### Lo que sí dice el paper (leído completo, PDF primario)

**Fuente:** Bailey, D.H. & López de Prado, M., "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest
Overfitting and Non-Normality", *Journal of Portfolio Management* (2014), versión del 31/07/2014:
https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf (leído completo, 31/07/2026).

- **Ejemplo numérico del propio paper (sección "A Numerical Example"):** un investigador prueba N=100 variantes
  independientes (`N`), con varianza entre esas variantes `V=1/2`, sobre una muestra de `T=1250` observaciones diarias
  (5 años), sesgo `γ₃=-3`, curtosis `γ₄=10`, y obtiene una variante ganadora con Sharpe anualizado 2,5. El umbral de
  rechazo por el número de ensayos sale `SR₀≈0,1132` (no anualizado); el **DSR calculado = 0,9004 < 0,95** → la
  estrategia **se rechaza** al nivel de confianza del 95%.
- **Sensibilidad al número de ensayos (mismo ejemplo, mismo paper):** si el investigador hubiese probado solo **N=46**
  variantes (no 100), el DSR habría subido a **0,9505**, justo por encima del umbral de aceptación del 95%.
- **Relevancia directa para este proyecto:** la regla 19 de `CLAUDE.md` fija un pre-registro de **máximo 5-7 variantes por
  hipótesis**. Con N=5-7 (muy por debajo del N=46 del ejemplo del paper), el umbral de rechazo por selección múltiple es
  bastante más bajo que con N=100 — es decir, la regla de pre-registro del proyecto no es solo disciplina anti-pesca de
  datos: también es lo que mantiene bajo el listón estadístico exigido por el propio DSR. Esto es una relación matemática
  directa del paper, no una recomendación mía.
- El paper **no define ningún número mínimo de trades para que un Sharpe individual sea fiable**; solo corrige el sesgo
  de haber probado muchas variantes y de que los retornos no sean normales.

### Lo que dice White / Sullivan-Timmermann-White (sobre número de REGLAS probadas, no de operaciones)

**Fuente:** Sullivan, R., Timmermann, A., White, H., "Data-Snooping, Technical Trading Rule Performance, and the
Bootstrap", *Journal of Finance* 54(5), 1999, pp. 1647-1691 (citado consistentemente en múltiples fuentes secundarias
académicas — ResearchGate, Semantic Scholar, ideas.repec.org — no se leyó el PDF completo del artículo de 1999 esta
sesión, solo resúmenes/abstracts). El estudio probó **7.846 reglas técnicas de trading** contra 100 años de datos diarios
del Dow Jones para cuantificar el sesgo de "data snooping" con el bootstrap de White (2000, *Econometrica* 68(5),
1097-1126). Es la misma lógica del DSR: el número que importa es cuántas **variantes** se prueban, no cuántas
**operaciones** genera cada una.

### Reglas de "número de trades" que circulan (PRÁCTICA COMÚN SIN RESPALDO ACADÉMICO VERIFICABLE)

Múltiples sitios (Medium, backtestbase.com, darwintiq.com, tradezella.com) repiten cifras de "30 trades mínimo (CLT)",
"100+ para fiabilidad" y "200-500 como estándar institucional". **Una de estas fuentes atribuye explícitamente "200-500
trades" a López de Prado** — esta atribución **no se pudo verificar**: no aparece en el paper del DSR leído completo esta
sesión, ni se localizó en ningún otro texto primario suyo durante la búsqueda. Se marca como **posible error de
atribución de una fuente secundaria**, no se usa. El rango "30 a algunos cientos" se declara como **práctica común, sin
fuente académica primaria verificada** que fije ese número exacto.

### Conclusión de la pregunta 2

- **PUBLICADO, con cifra concreta:** el marco DSR de Bailey/López de Prado (2014) — pero su cifra clave es el número de
  **variantes/ensayos** probados (N), no de operaciones. El propio paper muestra, en su ejemplo, que N=46 pasa el umbral
  del 95% y N=100 no, para el mismo Sharpe realizado.
- **PUBLICADO, sobre número de reglas (no de operaciones):** Sullivan-Timmermann-White probaron 7.846 reglas (fuente
  secundaria consistente, no leída en PDF completo esta sesión).
- **Hueco declarado:** ninguna fuente primaria verificada da un número mínimo de *operaciones dentro de un solo backtest*
  para que su Sharpe realizado sea estadísticamente significativo, más allá del marco general (más operaciones y más años
  reducen el error de estimación, sin una cifra de corte única publicada y verificada por mí).

---

## 3. Tamaño de vela: ¿sobrevive un sistema de 15 minutos a los costes en forex minorista?

**Se buscaron las dos direcciones, tal como pedía el encargo. Solo se encontró evidencia externa creíble en una
dirección (no viable); no se encontró evidencia externa publicada y creíble de sistemas de 15 minutos que sí funcionen
tras costes en forex minorista. Se declara explícitamente, como pide el encargo.**

### Dirección "NO viable" (encontrada, con fuente académica)

**Fuente:** estudio sobre trading técnico intradía en el mercado de divisas (Neely et al., *Journal of International
Money and Finance*, versión de working paper: Warwick Economics WP99-02,
https://wrap.warwick.ac.uk/id/eprint/1846/1/WRAP_Neely_fwp99-02.pdf; versión publicada indexada en ScienceDirect:
https://www.sciencedirect.com/science/article/abs/pii/S0261560602001018). **Aviso de nivel de lectura:** se consultó el
resumen/abstract vía búsqueda, no el PDF completo, esta sesión — se cita con esa reserva. Hallazgo del resumen: **"when
realistic transaction costs and trading hours are taken into account, [the study finds] no evidence of excess returns to
intraday technical trading rules"**.

### Dirección "SÍ viable" — hueco declarado explícitamente

Se hicieron búsquedas específicas ("published systematic 15-minute forex strategy profitable after transaction costs",
"intraday forex trading strategy survives transaction costs 2020-2022", CTA/hedge fund minimum holding period). **No se
encontró ningún ejemplo publicado y verificable** (paper académico, libro de un gestor sistemático con track record
citable, o documento regulado) de una estrategia de 15 minutos en forex minorista que sea rentable tras costes reales.
Lo único encontrado en esta dirección son sitios educativos genéricos sin datos verificables ("XS", "OpoFinance",
"mondfx"), que no cuentan como fuente. **Se declara hueco en la dirección "sí funciona": no hay evidencia externa
creíble de que exista, no que se haya demostrado que no exista.**

### Contraste con lo ya calculado dentro de este proyecto (no es una fuente externa nueva, es coherencia interna)

`coste_relativo.md` (tarea 02.02.02, ya cerrada) ya muestra, con datos brutos propios del proyecto y sin necesidad de
buscar fuera: en la vela de 15 minutos, contra el ATR **medio**, pasan 5 de 6 instrumentos de forex+oro el criterio
≤15%; contra el ATR de la vela **tranquila (p10)** —el escenario que ocurre una vela de cada diez—, **solo el oro sigue
pasando**, y solo por el extremo laxo. Este patrón (viable en el caso típico, frágil en el caso tranquilo) es coherente
con lo que dice Neely et al. sobre que la rentabilidad intradía desaparece al aplicar condiciones realistas y
restringir a horas de actividad alta. No se trata de una segunda fuente externa: es la misma pregunta mirada con datos
propios ya calculados, y coincide en la dirección del hallazgo.

### Conclusión de la pregunta 3

- **PUBLICADO (una dirección, con reserva de "solo resumen leído"):** no hay evidencia de rentabilidad intradía en forex
  tras costes reales (Neely et al.).
- **Hueco explícito, declarado tal como pide el encargo:** no se encontró evidencia externa publicada en la dirección
  contraria.

---

## 4. Umbral de correlación: ¿de dónde sale el 0,7 y qué hay que correlacionar de verdad?

### El origen del 0,7

**No se encontró ninguna fuente académica primaria que establezca 0,7 como el umbral correcto o validado** para decidir
que dos activos son "apuestas distintas". Es una cifra que se repite en múltiples blogs y sitios de gestión de carteras
retail (alphaexcapital.com, guardfolio.ai, morningstar.com, litovskymanagement.com) de forma inconsistente entre sí:
algunas fuentes usan 0,7 como corte, otras 0,5, otras 0,85. **Se declara PRÁCTICA COMÚN SIN RESPALDO ACADÉMICO
IDENTIFICADO** para el valor exacto 0,7. Dentro de este mismo proyecto, `correlaciones_8x8.md` usa 0,7 como "criterio 4
de G1" sin remitir a una fuente externa (`01-investigacion/mercados/BRIEFS_FASE_02.md` tampoco cita de dónde sale el
número: solo pide "calibrar los umbrales" en la tarea 02.03.02) — es decir, dentro del proyecto 0,7 parece ser un valor
de trabajo adoptado para calibrar, no un número traído de la literatura.

### ¿Correlación de activos o de rendimientos de la estrategia? — dos fuentes convergen: importa la segunda

1. **Grinold & Kahn — Ley Fundamental de la Gestión Activa.** `IR = IC × √Breadth`, donde `Breadth` es el número de
   **apuestas activas independientes** (previsiones no correlacionadas), no el número de activos. Lo que reduce el
   riesgo de verdad es que las **previsiones/apuestas** sean independientes entre sí, no que los activos subyacentes lo
   sean. **Fuentes (múltiples, convergentes, consultadas 31/07/2026):** CFA Institute / AnalystPrep, notas de estudio
   sobre "Fundamental Law of Active Portfolio Management"; Robeco, "Fundamental Law of Active Management shows way to
   higher information ratio" (robeco.com/en-int/insights/2018/04/); ScienceDirect, "The fundamental law of active
   management: Redux" (sciencedirect.com/science/article/pii/S0927539817300543).
2. **Ray Dalio / Bridgewater — "el Santo Grial de la inversión".** Con 15-20 flujos de retorno **buenos y no
   correlacionados**, el riesgo de cartera puede bajar ~80% sin sacrificar el retorno esperado. Cita explícita
   encontrada: *"individual assets within an asset class are usually about 60% correlated with each other, so even if
   you think you're diversified, you're not"* — el foco está en la **correlación de los rendimientos**, no en la
   clase de activo. **Fuentes (múltiples, convergentes, consultadas 31/07/2026):** Benzinga, "Ray Dalio's 'Holy Grail'
   Investment Strategy: Why 10-15 Diversified Investments Could Make You a Fortune" (benzinga.com, feb-2026);
   financhill.com/blog/investing/ray-dalio-holy-grail-explained; Forbes Marketplace, "Holy Grail of Investing"
   (forbes.com/sites/forbesmarketplace/2019/03/27/).

### Conclusión de la pregunta 4, y su relevancia directa para lo ya medido en el proyecto

Las dos fuentes (Grinold-Kahn, académica de gestión de carteras; Dalio, práctica de un gestor con track record público)
**coinciden en que lo que importa es la correlación de los RENDIMIENTOS de las apuestas/estrategias, no la correlación
de los precios de los activos subyacentes**. `correlaciones_8x8.md` (tarea 02.02.03, ya cerrada) mide exactamente lo
segundo: correlación de rendimientos logarítmicos de **precio** entre los 8 instrumentos, no de los rendimientos de una
estrategia aplicada sobre cada uno (porque el bot aún no existe). Es una limitación que el propio documento no oculta,
pero que aquí queda respaldada por dos fuentes externas: la matriz 8×8 responde "¿se mueven los precios juntos?", que es
una proxy razonable y barata cuando no hay estrategia que probar todavía, pero **no** responde "¿producirían dos
estrategias corriendo sobre esos activos resultados correlacionados?", que es la pregunta que de verdad decide si 5
pares de forex son o no 5 apuestas distintas.

- **Hueco declarado:** no hay fuente para el valor exacto 0,7 como el corte correcto.
- **PUBLICADO, con dos fuentes convergentes:** lo que hay que medir para diversificar de verdad es la correlación de
  rendimientos de estrategia/apuesta, no la de activos — pregunta distinta a la que responde `correlaciones_8x8.md`.

---

## 5. Deslizamiento: ¿qué hace la práctica profesional sin broker elegido todavía?

### La convención más citada: media del spread bid-ask en el momento de entrada

Robert Carver publica y mantiene una estimación de deslizamiento basada en **"half the bid/ask spread at the point when
a trade was entered"** como uno de los componentes de su medida de coste de ejecución, ponderado junto con el
deslizamiento real incurrido. **Fuente (resumen de su metodología, no su repositorio original leído directamente esta
sesión):** hallado vía búsqueda que cita su blog `qoppac.blogspot.com` y una entrada suya en el foro Elite Trader;
**nivel de confianza: medio** — la cifra de "mitad del spread" es coherente entre varias fuentes que la citan, pero no se
leyó el repositorio/post original con el número exacto esta sesión. Se cita con esta reserva.

Esta misma convención ("fill price = midprice futuro + mitad del spread + impacto de mercado + ruido") aparece descrita
como el estándar profesional en documentación de plataformas/brokers: QuantConnect (`quantconnect.com/docs/v2/writing-
algorithms/reality-modeling/slippage/key-concepts`) e Interactive Brokers Campus, "Slippage in Model Backtesting"
(`interactivebrokers.com/campus/ibkr-quant-news/slippage-in-model-backtesting/`), ambas consultadas 31/07/2026. Son
fuentes de plataforma/broker, no papers académicos, pero son dos fuentes independientes que convergen en la misma
convención.

### El modelo más sofisticado: impacto de mercado en raíz cuadrada, no un porcentaje fijo

Varias fuentes de plataformas quant (quantmedia.io, entre otras) describen el **"square-root impact model"**, que
calibra el coste de ejecución en función de la volatilidad y de la tasa de participación en el volumen, en vez de un
porcentaje fijo. Es un concepto bien establecido en la literatura de microestructura de mercado (línea Almgren-Chriss),
pero **no se leyó el paper original de Almgren-Chriss esta sesión** — se cita el concepto, no el paper, y se recomienda
que quien implemente esto en `03-motor` verifique la fuente primaria antes de usarlo como base numérica.

### Factores publicados por clase de activo, tamaño de vela u hora del día

**Hueco declarado, explícitamente, tal como permite el encargo: no se encontró ningún factor de deslizamiento publicado
por una fuente autorizada (broker, regulador o paper) desglosado por clase de activo (forex/oro/cripto), por tamaño de
vela, o por hora del día.** Lo único encontrado fue una cifra genérica de un sitio educativo ("el deslizamiento puede ser
tan bajo como 0,1% en mercados líquidos, o superior al 1% cuando la liquidez se reduce") de `luxalgo.com` — se marca
explícitamente como **PRÁCTICA COMÚN, orden de magnitud ilustrativo, no un factor validado**, y no se usa como número de
referencia.

### Conclusión de la pregunta 5

- **PUBLICADO (convención, no cifra exacta con broker o vela):** deslizamiento estimado como la mitad del spread
  bid-ask en el momento de entrada, más un componente de impacto de mercado — convención repetida en tres fuentes
  independientes (Carver, QuantConnect, Interactive Brokers), aunque ninguna da el número exacto verificado por lectura
  directa esta sesión.
- **Hueco declarado:** ningún factor numérico publicado por clase de activo, vela u hora del día.

---

## 6. Tamaño mínimo operable con 1.000-2.000 euros — la pregunta que nadie había mirado

### Método (cálculo, no estimación — sobre datos ya verificados del proyecto + specs de broker leídas en PDF completo)

`riesgo_monetario = posición_mínima × ATR(vela) ÷ precio_de_conversión_si_aplica`
`capital_necesario_para_1%_riesgo = riesgo_monetario ÷ 0,01`

- ATR y precio medio: `04-resultados/atr_15m_1h_4h.json` (tarea 02.02.01, cerrada y verificada por dos revisiones —
  **no recalculado aquí, solo reutilizado**), fecha de generación 2026-07-31T19:52:51 UTC.
- Tamaños mínimos de posición: leídos **directamente y completos** en los PDF oficiales de **IC Markets** (única fuente
  con las tres hojas de especificación —divisas, metales, cripto— leídas íntegras esta sesión, no resumidas por un
  modelo intermedio): `Cryptocurrency-CFD-Specification-Sheet.pdf` (icmarkets.com.au) y `Commodity-Specification-
  Sheet.pdf` (icmarkets.eu), ambas consultadas 31/07/2026.
- Conversión EUR: se usa el precio medio EURUSD del propio JSON (≈1,1291, media de ~700 días, **no** un tipo de cambio
  al contado del día) solo para dar una cifra de referencia en euros; se declara explícitamente que no es un tipo de
  cambio spot verificado y es solo orientativo.
- Para USDJPY y USDCHF, el riesgo en la divisa de cotización (JPY, CHF) se convierte a USD dividiendo por el precio
  medio de ese par (151,70 y 0,82757 respectivamente, misma fuente).

### Tamaño mínimo de posición por instrumento (fuente primaria: IC Markets, PDF leído completo)

| Instrumento | Tamaño de 1 lote | Lote mínimo | **Posición mínima real** | Fuente exacta |
|---|---|---|---|---|
| EURUSD/GBPUSD/AUDUSD/USDJPY/USDCHF | 100.000 unidades de divisa base | 0,01 lote (estándar del sector; confirmado para XTB: *"minimum transaction volume of 0.01 lot"*, xtb.com/int/education/minimum-transaction-size, leído 31/07/2026) | **1.000 unidades** | XTB (primaria, leída); tamaño de lote estándar confirmado también en OANDA TMS Brokers S.A., "Financial Instruments Specification CFDs", vigente 2026-06-26 (PDF leído completo: "Nominal value of 1 lot = 100 000 [divisa]" para los 5 pares, sección 1) |
| XAUUSD (oro) | 100 oz por lote | **0,01 lote** | **1 onza** | IC Markets, `Commodity-Specification-Sheet.pdf`: fila XAUUSD, "Contract size (Platform Volume 1.00) = 100", "Minimum Lot Size = 0,01" (leído completo, PDF primario) |
| BTCUSD | 1 BTC por lote | **0,01 lote** | **0,01 BTC** | IC Markets, `Cryptocurrency-CFD-Specification-Sheet.pdf`: fila BTCUSD, "1 BTC" por lote, "Min Volume 0,01" (leído completo, PDF primario) |
| ETHUSD | 1 ETH por lote | **0,01 lote** | **0,01 ETH** | IC Markets, `Cryptocurrency-CFD-Specification-Sheet.pdf`: fila ETHUSD, "1 ETH" por lote, "Min Volume 0,01" (leído completo, PDF primario) |

**Contraste con OANDA (segunda fuente, con reserva de nivel de lectura).** El documento oficial de OANDA TMS Brokers
S.A. (leído completo, PDF primario) da el "Nominal value of 1 lot" para todos los instrumentos (incluidos GOLD.pro,
BTCUSD, ETHUSD) pero **no incluye una columna de "lote mínimo"** — consistente con que OANDA opera con tamaños
fraccionarios/por unidad en su plataforma nativa, no por lotes. Una página de ayuda separada de OANDA (no la entidad TMS
Brokers S.A., posiblemente otra entidad del grupo; consultada solo vía resumen de `WebFetch`, no leída completa, por lo
que el nivel de confianza es menor) afirma tamaños mínimos de: forex 1 unidad, oro 0,1 unidad, BTCUSD 0,001 unidad,
otras cripto 0,01 unidad — **si estas cifras son correctas, el mínimo de OANDA es igual o más pequeño que el de IC
Markets en todos los casos**, por lo que no cambiaría ninguna de las conclusiones de la tabla siguiente, solo las
reforzaría. Se cita con la reserva explícita de menor verificación.

**Huecos declarados explícitamente:**
- **Pepperstone:** no se encontró una hoja de especificación de contrato leída de forma primaria con el lote mínimo
  exacto para XAUUSD/BTCUSD/ETHUSD esta sesión (solo referencias genéricas de reseñas de terceros a "0,01 lote"). Se
  declara hueco para Pepperstone específicamente en oro y cripto.
- **XTB:** confirma 0,01 lote como mínimo universal (fuente primaria leída), pero **XTB no ofrece BTCUSD/ETHUSD como CFD
  apalancado** — los ofrece como cripto **al contado** (hallazgo ya establecido en `coste_swap.md`, no repetido aquí);
  el tamaño mínimo de compra al contado en XTB no se recuperó esta sesión. Hueco declarado.
- **Interactive Brokers:** forex al contado vía IdealPro tiene un mínimo estándar de **20.000 unidades** de la divisa
  base (con órdenes sueltas ("odd lot") desde 1.000 unidades a comisión más alta); CFD de forex vía Smart routing,
  mínimo **1.000 unidades**. Oro al contado: desde **1 onza**. **Cripto al contado: no disponible para clientes de la
  entidad europea (IBIE) — solo ETP/ETN/futuros de cripto**, según la propia página de IBKR (el servicio al contado vía
  Paxos, con mínimo de 1,75 USD por orden, solo está disponible para EE.UU. y Reino Unido, no para la entidad europea
  que atendería a un cliente español). **Fuentes:** `interactivebrokers.com/en/trading/forexOrderSize.php` y
  `interactivebrokers.com/en/trading/products-cryptocurrencies.php` (ambas consultadas vía `WebFetch`, 31/07/2026).
  **Conclusión operativa: IBKR no es una vía directa a BTCUSD/ETHUSD al contado para un cliente en España** — solo a
  través de instrumentos derivados (ETP/ETN/futuros), que no son el mismo instrumento que mide este proyecto (rendimiento
  BID de contado, según `correlaciones_8x8.md`).

### Tabla — capital necesario para arriesgar el 1% con un stop de 1×ATR y la posición mínima de IC Markets

Fórmula aplicada celda a celda: `capital_necesario = posición_mínima × ATR(vela) [convertido a USD si hace falta] ÷ 0,01`.
Los ATR son los de `04-resultados/atr_15m_1h_4h.json`, `atr14_medio`, no recalculados.

| Instrumento | Vela | ATR (unidad cruda) | Riesgo con posición mínima | **Capital necesario (USD)** | **≈ EUR** (orientativo, EURUSD≈1,1291) | ¿Cabe en 1.500 €? | ¿Cabe en 2.000 €? |
|---|---|---|---|---|---|---|---|
| EURUSD | 15m/1h/4h | 0,000686 / 0,001407 / 0,002850 | 0,69 / 1,41 / 2,85 USD | 68,6 / 140,7 / 285,0 | 60,8 / 124,7 / 252,5 | **Sí** (las 3 velas) | **Sí** |
| GBPUSD | 15m/1h/4h | 0,000828 / 0,001695 / 0,003414 | 0,83 / 1,69 / 3,41 USD | 82,8 / 169,5 / 341,4 | 73,3 / 150,1 / 302,4 | **Sí** | **Sí** |
| USDJPY | 15m/1h/4h | 0,1203 / 0,2486 / 0,5073 JPY | 0,79 / 1,64 / 3,34 USD (÷151,70) | 79,3 / 163,9 / 334,4 | 70,2 / 145,2 / 296,3 | **Sí** | **Sí** |
| AUDUSD | 15m/1h/4h | 0,000559 / 0,001148 / 0,002324 | 0,56 / 1,15 / 2,32 USD | 55,9 / 114,8 / 232,4 | 49,5 / 101,7 / 205,9 | **Sí** | **Sí** |
| USDCHF | 15m/1h/4h | 0,000572 / 0,001174 / 0,002388 CHF | 0,69 / 1,42 / 2,89 USD (÷0,82757) | 69,1 / 141,8 / 288,5 | 61,2 / 125,6 / 255,6 | **Sí** | **Sí** |
| **XAUUSD** | 15m | 7,0645 USD/oz | 7,06 USD (×1 oz) | **706,5** | 625,9 | **Sí** | **Sí** |
| **XAUUSD** | 1h | 14,4647 USD/oz | 14,46 USD | **1.446,5** | 1.281,4 | **Sí, apurado** (~85% del capital) | **Sí** |
| **XAUUSD** | 4h | 28,4289 USD/oz | 28,43 USD | **2.842,9** | **2.517,6** | **NO** | **NO** (supera el techo de 2.000 €) |
| BTCUSD | 15m/1h/4h | 123,93 / 298,69 / 809,13 USD | 1,24 / 2,99 / 8,09 USD (×0,01 BTC) | 123,9 / 298,7 / 809,1 | 109,8 / 264,6 / 716,9 | **Sí** | **Sí** |
| ETHUSD | 15m/1h/4h | 5,45 / 12,25 / 30,97 USD | 0,05 / 0,12 / 0,31 USD (×0,01 ETH) | 5,5 / 12,2 / 31,0 | 4,8 / 10,9 / 27,4 | **Sí** | **Sí** |

### Respuesta directa a "con 1.500 euros, ¿en cuáles de los 8 se puede arriesgar el 1% sin que el mínimo obligue a arriesgar
más?"

**Con las posiciones mínimas de IC Markets (0,01 lote en todo), los 8 instrumentos lo permiten en 15m y en 1h.** La
única celda que **no** lo permite es **XAUUSD en vela de 4 horas**: el 1×ATR de la vela de 4h en oro (28,43 USD/oz)
sobre la posición mínima de 1 onza obliga a un capital de ~2.518 € solo para que esa pérdida máxima sea el 1% — por
encima incluso del techo alto (2.000 €) del rango de capital declarado en el encargo. En XAUUSD 1h, con 1.500 €
justos, la cifra necesaria (~1.281 €) cabe pero consume ~85% del capital — deja poco margen si se quisiera un stop
más ancho que exactamente 1×ATR, o abrir más de una posición a la vez. **El sospechoso confirmado es el oro, no el
bitcoin**: con el mínimo de IC Markets, BTCUSD y ETHUSD no imponen ninguna restricción real en ninguna de las tres
velas — la fricción de cripto que ya documentó este proyecto (`coste_relativo.md`, `coste_swap.md`) está en el
**spread/swap**, no en el tamaño mínimo de posición.

**Aclaración de método (para que no se confunda con margen):** esta tabla mide el capital necesario para que la
**pérdida** de un stop de 1×ATR sea el 1% del capital, no el margen necesario para **abrir** la posición mínima (que es
siempre mucho menor, dado el apalancamiento típico: p. ej. margen inicial del 5% en oro según IC Markets implicaría
solo ~180 USD de margen para abrir 1 onza — la restricción real es el riesgo potencial de la posición mínima, no el
margen de apertura).

---

## 7. Horario y liquidez: ¿en qué horas se concentra el coste alto?

### Forex

- **Mejor liquidez / menor coste:** solapamiento Londres-Nueva York, aproximadamente 13:00-17:00 UTC (múltiples fuentes
  educativas/de broker convergentes: tmgm.com, mondfx.com — **PRÁCTICA COMÚN, sin cifra publicada por un regulador o
  paper académico esta sesión**).
- **Peor liquidez / mayor coste — el "rollover" de las 17:00 hora de Nueva York (~21:00-22:00 UTC).** Varias fuentes de
  broker/foro coinciden en que los spreads se ensanchan alrededor del cierre/rollover diario, con una cifra ilustrativa
  citada de picos "de hasta 20 pips incluso en pares principales" — **fuente secundaria de tipo educativo (mondfx.com),
  no verificada de forma independiente, se marca como orden de magnitud, no como cifra fiable**.
- **Coincidencia directa con el propio corte de datos del proyecto.** El pipeline de este proyecto (`atr_15m_1h_4h.json`,
  `correlaciones_8x8.md`) usa un **corte único de 22:00 UTC** para anclar el día/las ventanas — justo dentro o al borde
  de la ventana de baja liquidez descrita arriba. No es una fuente externa nueva: es una observación de coherencia entre
  lo que dice la práctica de mercado y una decisión de método ya tomada en 02.02.01/02.02.03.

### Oro al contado

`coste_relativo.md` (sección "CORRECCIÓN (31/07)", ya cerrada en este proyecto, **no recalculada aquí**) ya documentó y
verificó, con datos brutos propios, que el oro al contado tiene una **pausa diaria real hacia las 21:00-22:00 UTC**, que
infla la media del ATR frente a la mediana (ratio medio/mediana de 1,28-1,30, muy por encima de los demás instrumentos).
Es el mismo fenómeno horario que describe la sección anterior para forex (ventana de baja actividad a esa hora), pero
para el oro tiene un efecto medible y ya cuantificado dentro del proyecto: la elección de la vela de 4h de este
instrumento cruza justo esa pausa.

### Cripto

- **Fin de semana, con una cifra concreta y con fuente (Kaiko, datos de mercado cripto):** el volumen de operaciones de
  bitcoin en fin de semana ha caído del 24% del total (2018) al 17% (2023) y al 13% (2024) — **fuente:** datos de Kaiko
  citados en Decrypt, "Nobody Trades Bitcoin on Weekends Anymore—Here's Why Liquidity Is Dwindling", abril-2026:
  https://decrypt.co/219288/bitcoin-crypto-weekend-trading-liquidity-kaiko (consultado 31/07/2026).
- **Coste en fin de semana:** el mismo artículo cita un aumento de ~11% en el coste de trading en fin de semana,
  atribuido a datos de "BridgePort" — **esta cifra es de una sola fuente (no las 2 independientes que exige la regla del
  proyecto), se marca como no fiable como cifra aislada**, aunque la dirección (fin de semana = peor) es coherente con
  el hallazgo de volumen (Kaiko) y con la caída de volumen ya documentada.
- **Mejor ventana horaria citada (PRÁCTICA COMÚN, sin fuente académica):** solapamiento EE.UU.-Europa, ~13:00-17:00 UTC.

### Lo que este documento NO puede responder sin cálculo adicional sobre datos brutos ya descargados

El encargo pregunta específicamente si el coste típico publicado (el de `coste_operar.md`) **subestima** el coste real
en las horas malas, y en cuánto. **Esto es una pregunta que se puede calcular directamente sobre los datos M1 ya
descargados en `02-datos/bruto/` (spread/ATR por hora UTC), no algo que deba buscarse fuera** — es exactamente el caso
que cubre la regla 14 de `CLAUDE.md` ("todo dato numérico se calcula sobre datos brutos, salvo que exista fuente
primaria homogénea demostrable"). Lo que sí existe ya calculado dentro del proyecto es una partición **por percentil de
ATR** (`coste_relativo.md`, ampliación p10/p90), no una partición **por hora del reloj** — son dos cortes distintos del
mismo problema (una vela tranquila puede caer a cualquier hora; una hora mala concentra más velas tranquilas pero no
todas). No se ha hecho esa segunda partición todavía en el proyecto. Se declara como **cálculo pendiente, no hueco de
búsqueda**: no hace falta salir a buscarlo, un `constructor-datos` puede calcularlo sobre lo ya descargado.

### Conclusión de la pregunta 7

- **PUBLICADO, con cifra y fuente (Kaiko/Decrypt):** caída de volumen de fin de semana en bitcoin, de 24% (2018) a 13%
  (2024).
- **PRÁCTICA COMÚN, sin fuente académica de la magnitud exacta:** ensanchamiento de spreads en el rollover forex
  (~21:00-22:00 UTC) y en fin de semana cripto; cifras ilustrativas encontradas (20 pips, 11%) proceden de fuentes
  únicas o educativas, no verificadas de forma independiente — no se usan como número de referencia, solo como
  dirección del efecto.
- **Ya verificado dentro del proyecto, no repetido aquí:** la pausa diaria del oro hacia las 21:00-22:00 UTC
  (`coste_relativo.md`).
- **Cálculo pendiente sobre datos ya descargados, no hueco de búsqueda:** coste por hora UTC del reloj, partición que
  el proyecto no ha hecho todavía.

---

## Resumen de huecos declarados (sin dato fiable, no rellenados)

1. **P1:** no existe una fuente externa con el criterio "coste ≤ X% del ATR" en esa forma exacta; los anclajes externos
   miden coste frente a retorno/edge esperado (Carver, Chan), no frente a volatilidad bruta.
2. **P2:** no hay una cifra mínima de *operaciones* (a diferencia de *ensayos/variantes*, que sí tiene marco DSR) con
   fuente académica primaria verificada.
3. **P3:** no se encontró evidencia externa publicada de que un sistema de 15 minutos en forex minorista sí sobreviva a
   los costes reales (solo evidencia en la dirección contraria).
4. **P4:** no hay fuente para el valor exacto 0,7 como umbral de correlación de activos.
5. **P5:** no hay ningún factor de deslizamiento publicado desglosado por clase de activo, vela u hora del día.
6. **P6:** lote mínimo de Pepperstone en oro/cripto (sin fuente primaria leída esta sesión); tamaño mínimo de compra al
   contado de cripto en XTB (sin dato recuperado esta sesión). Ninguno de los dos huecos cambia la conclusión principal
   (basada en IC Markets, con fuente primaria completa) de que el oro en vela de 4h es el punto de fricción real, no el
   bitcoin.
7. **P7:** partición del coste por hora del reloj UTC — no es un hueco de búsqueda, es un cálculo pendiente sobre datos
   ya descargados en `02-datos/bruto/` (regla 14).

---

*Este documento mide y contrasta evidencia externa: no elige mercado, no elige vela, no recomienda broker. La decisión
corresponde a la puerta G1, con el CEO. Estado: entregado para revisión independiente antes de que el orquestador lo dé
por hecho (regla 16 de `CLAUDE.md`: quien construye no valida su propio trabajo).*
