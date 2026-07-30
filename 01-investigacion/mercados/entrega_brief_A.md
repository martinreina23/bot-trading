# Entrega del Brief A (costes, ATR, coste relativo)

# Medición de coste, movimiento medio (ATR) y coste relativo en 8 mercados y 3 tamaños de vela

*Rol: analista cuantitativo que SOLO mide y documenta. Este informe no recomienda, no elige, no ordena por preferencia ni concluye cuál mercado es "mejor". Donde falta un dato, se dice explícitamente "sin dato fiable".*

## TL;DR
- Los **costes de operar** (spread + comisión) están razonablemente bien documentados con fuentes de brokers grandes y regulados; el **movimiento medio por vela (ATR)** está bien documentado a nivel DIARIO pero muy mal a nivel intradía (15m, 1h, 4h): prácticamente ninguna fuente pública ofrece un ATR intradía medido sobre 2 años con el periodo indicado.
- Por eso, de las 24 celdas de ATR pedidas (8 instrumentos × velas de 15m/1h/4h), la gran mayoría quedan como **"sin dato fiable"**; solo hay valores intradía flojos y sin periodo claro para XAUUSD (1h). Todo lo demás intradía se ofrece como **estimación derivada** del ATR diario mediante la regla raíz-del-tiempo, presentada aparte y NO como medida.
- El **coste relativo** (coste ÷ ATR × 100) solo puede calcularse de forma real donde hay ATR real; como el ATR real disponible es diario, se ofrece (a) un cálculo de referencia con ATR diario y (b) una tabla intradía basada en estimaciones derivadas, ambas claramente etiquetadas como tales.

---

## Términos en lenguaje llano (se explican una vez)
- **Spread (horquilla):** diferencia entre el precio al que compras y al que vendes en el mismo instante. Es un coste que pagas siempre al abrir y cerrar.
- **Pip:** unidad mínima habitual de movimiento en divisas. En pares como EUR/USD 1 pip = 0,0001; en pares con yen (USD/JPY) 1 pip = 0,01. En un lote estándar (100.000 unidades) de un par cotizado en dólares, 1 pip ≈ 10 USD.
- **Punto/dólar en oro y cripto:** en oro (XAUUSD) y cripto (BTCUSD/ETHUSD) el movimiento se mide directamente en dólares de precio (p. ej. de 2.300,00 a 2.301,00 = 1 dólar).
- **Lote / lote redondo:** tamaño estándar de operación (100.000 unidades en divisas). "Round turn / lote redondo" = abrir + cerrar.
- **Comisión:** cargo fijo por lote que cobran las cuentas "raw/ECN". Típico en divisas: ~7 USD por lote redondo (3,50 USD por lado).
- **Cuenta "spread-only":** sin comisión, pero con el spread más ancho (el coste va metido en la horquilla).
- **Cuenta "raw / ECN":** spread crudo (muy estrecho) + comisión por lote. ECN = red que conecta directamente con proveedores de liquidez.
- **ATR (Average True Range):** rango medio de una vela (máximo–mínimo, contando huecos), calculado normalmente como media de 14 velas. Mide cuánto se mueve de media una vela; NO indica dirección.

---

## Criterio de desglose (estructura MECE) y dónde hay huecos/solapes
Parto el problema en tres bloques que no se solapan: **(1) coste de operar** (lo que pagas por entrar/salir), **(2) movimiento medio por vela** (ATR), **(3) coste relativo** (cociente de los dos). Dentro del coste, separo por **tipo de cuenta** (spread-only vs raw/ECN) porque son excluyentes y comparables entre sí. Dentro del ATR, separo por **tamaño de vela** (15m/1h/4h) y, aparte, distingo **medida real** frente a **estimación derivada**.

Huecos y solapes que reconozco explícitamente:
- **Hueco grande:** no existe fuente pública homogénea con ATR intradía de 2 años por instrumento y vela. Lo que hay son lecturas puntuales (snapshot) de ATR(14) sin periodo de 2 años, o rangos "típicos" de blogs sin periodo.
- **Solape de tipo de cuenta en oro/cripto:** en algunos brokers la cripto no lleva comisión separada (el coste va en el spread); el oro, en cambio, en varias cuentas raw SÍ lleva comisión (p. ej. Pepperstone Razor cobra comisión también en XAU/USD). Lo señalo caso por caso.
- **Solape de unidades en oro:** las fuentes no coinciden en si 1 "pip" de oro es 0,01, 0,10 o 1,00 dólar. Para evitar el lío, mido el oro en **dólares por onza de precio**, no en pips.

---

## ENTREGA 1 — Coste típico de operar cada mercado

### Tabla 1 — Costes por instrumento (brokers grandes y regulados)
Todos los rangos son "spread típico/medio" declarado por el broker o por reseñas que citan al broker. Comisión indicada por lote redondo. "n/a" = el broker no cobra comisión separada en ese instrumento (coste en el spread).

| Instrumento | Spread típico RAW/ECN (rango entre brokers) | Comisión típica (raw/ECN) | Spread típico SPREAD-ONLY (rango) | Tipo de cuenta y notas | Fuentes (con fecha del dato) |
|---|---|---|---|---|---|
| **EURUSD** | 0,0–0,2 pip (IC Markets: "average on EURUSD being 0.1 pips 24/5"; Pepperstone Razor media 0,1; XM Zero media 0,2) | ~7 USD/lote redondo (IC Markets: "$3.50 per lot payable per side" = 7 USD ida y vuelta; 0,70 mini, 0,07 micro); Pepperstone cTrader 6 USD, plataforma/TradingView 7 USD; XM Zero 7 USD | 0,6–1,5 pip (IG media 0,9; OANDA media 1,4–1,54; Pepperstone Standard 1,1; XM Ultra Low 0,6–1,1) | Raw: spread + comisión. Spread-only: sin comisión | IC Markets Raw Spread (icmarkets.com); Pepperstone Cost&Charges Feb-2025 y pricing oficial; XM (BestBrokers/BrokerChooser 2026); IG (BrokerChooser 2026); OANDA (BestBrokers/CompareForexBrokers 2026) |
| **GBPUSD** | 0,04–0,3 pip (IC Markets min 0,04 / media 0,12) | ~7 USD/lote redondo | 0,9 pip min (IG) | igual que arriba | IC Markets pricing; IG (Commodity.com IG Review Feb-2026) |
| **USDJPY** | 0,03–0,11 pip (IC Markets min 0,03 / media 0,11) | ~7 USD/lote redondo (≈1,0 pip por valor de pip menor; ver conversión) | típico 0,7–1,4 pip | valor del pip en USDJPY ≈ 6,7–7 USD/lote, la comisión en pips sale mayor | IC Markets pricing |
| **AUDUSD** | 0,1–0,2 pip | ~7 USD/lote redondo | 0,6 pip min (IG) | — | IC Markets pricing; IG (Commodity.com Feb-2026) |
| **USDCHF** | 0,09–0,17 pip (IC Markets min 0,09 / media 0,17) | ~7 USD/lote redondo (valor de pip ≈ 12,5 USD, comisión ≈ 0,56 pip) | típico 1,0–1,7 pip | — | IC Markets pricing |
| **XAUUSD (oro)** | 0,08–0,30 USD/oz (Pepperstone Razor: "raw spreads... from 0.08 on XAU/USD", media 0,19; IG min 0,30) | Comisión SÍ en Pepperstone Razor ("raw spread + commission model", 3,50 USD/lado = 7 USD/lote); IC Markets y XM Zero (5,5 USD), Exness (3,5/lado) también cobran; en cuentas Standard va en el spread | 0,15–0,30 USD/oz | según broker/cuenta, el oro lleva o no comisión separada | Pepperstone Cost&Charges Feb-2025 y pricing oficial; IG (Commodity.com Feb-2026); Exness Help Center; XM/BestBrokers |
| **BTCUSD (CFD)** | 10–95 USD (Pepperstone min 10 / media 20,22 Feb-2025; media 36,90 en doc CySEC abr-2026; "desde 15" web; IG min 40–95) | n/a (sin comisión; coste en spread) | igual | CFD minorista; el spread cambia mucho con la volatilidad | Pepperstone Cost&Charges Feb-2025 y doc CySEC (datos 01–30 abr-2026); Pepperstone web cripto; IG (Commodity.com Feb-2026) |
| **ETHUSD (CFD)** | 2–7 USD (Pepperstone min 3 / media 3,01 Feb-2025; media 7,04 doc CySEC abr-2026; "desde 2" web; IG min 2) | n/a (sin comisión) | igual | CFD minorista | Pepperstone Cost&Charges Feb-2025 y doc CySEC; Pepperstone web cripto; IG (Commodity.com Feb-2026) |

**Referencia extra (exchanges cripto al contado, documentado aparte, NO en la tabla principal, para no mezclar modelos de coste):** los exchanges al contado cobran comisión porcentual en lugar de spread ancho. Referencia concreta: **Binance**, comisión spot estándar de partida en 2026 = **0,10 % maker y 0,10 % taker** (reducible a ~0,075 % pagando con 25% de descuento en BNB; niveles VIP hasta ~0,00825 % maker / 0,01725 % taker), según Traders Union / Bitget Academy 2026. Es un modelo distinto al CFD, por eso queda fuera de la tabla homogénea.

### Nota de conversión comisión → pips/dólares
- Divisas cotizadas en USD (EURUSD, GBPUSD, AUDUSD): valor del pip = 10 USD/lote → comisión de 7 USD ÷ 10 = **0,7 pip por lote redondo**.
- USDJPY: valor del pip ≈ 6,7 USD/lote (depende del cambio) → comisión ≈ **1,0 pip**.
- USDCHF: valor del pip ≈ 12,5 USD/lote → comisión ≈ **0,56 pip**.
- Oro (comisión donde exista): 7 USD por lote de 100 oz → **0,07 USD/oz**.
- Cripto CFD: normalmente sin comisión, coste en el spread.

---

## ENTREGA 2 — Movimiento medio por vela (ATR)

### Advertencia central sobre los datos
No encontré ninguna fuente pública que publique un **ATR medio de 2 años (mediados 2024–mediados 2026) por vela de 15m/1h/4h** para estos instrumentos, con el periodo declarado. Lo que existe:
- **ATR/ADR diario** bien documentado (varias fuentes, aunque con periodos distintos entre sí).
- **Lecturas puntuales (snapshot) de ATR(14)** en un día concreto (no una media de 2 años).
- **Rangos "típicos"** citados por blogs de brokers, sin periodo.

Por tanto, la Tabla 2 se rellena mayoritariamente con **"sin dato fiable"** en las velas de 15m/1h/4h, tal como pide el encargo, y el ATR diario se ofrece como columna de referencia (aunque no era una de las 3 velas pedidas) porque es el único nivel con medidas reales.

### Tabla 2 — ATR por vela (MEDIDAS REALES publicadas)
Unidades: divisas en pips; oro y cripto en dólares de precio.

| Instrumento | 15 min | 1 hora | 4 horas | (Referencia) Diario | Fuente y periodo |
|---|---|---|---|---|---|
| **EURUSD** | sin dato fiable | sin dato fiable (solo hora punta ~37 pips de media a las 16:00 GMT+1 en 2023, no es ATR de 2 años) | sin dato fiable | 60 pips (media 10 semanas, jun-2026; la media de 5 semanas era 53 y la de 2 semanas 59); ~75 pips (media multianual); 87 pips (2023, con máximo diario 243 pips el 15-mar-2023 y mínimo 28 pips en agosto) | Trade That Swing (12-jun-2026, base Mataf 10 sem.); forex.in.rs (ATR, 2023 y multianual) |
| **GBPUSD** | sin dato fiable | sin dato fiable | sin dato fiable | ~111,5 pips (media 2014–2025); ~120 pips (típico) | offbeatforex (tabla ADR 2014–2025); PriceActionNinja (2025); Headway (2026) |
| **USDJPY** | sin dato fiable | sin dato fiable | sin dato fiable | ~100 pips (típico); 40–80 pips (rango citado) | PriceActionNinja (2025); Headway (2026) |
| **AUDUSD** | sin dato fiable | sin dato fiable | sin dato fiable | ~70,5 pips (media 2014–2025); 50–90 pips | offbeatforex (2014–2025); Headway (2026) |
| **USDCHF** | sin dato fiable | sin dato fiable | sin dato fiable | ~40 pips (típico) | PriceActionNinja (2025) |
| **XAUUSD (oro)** | sin dato fiable | 20–35 pips "normales" (Pro-Scalper, SIN periodo; ≈2–3,5 USD/oz si 1 pip=0,10) | sin dato fiable | 60–100 USD/oz (normal), 150–300 USD/oz (noticias) | Pro-Scalper (sin fecha); lectura puntual FX Leaders ATR ≈9,68 (intradía, jul-2026) |
| **BTCUSD (CFD)** | sin dato fiable | sin dato fiable | sin dato fiable | ~2.930 USD (ATR(14) EMA, snapshot 19-ago-2025) | Aiolux (snapshot, no media de 2 años) |
| **ETHUSD (CFD)** | sin dato fiable | sin dato fiable (TipRanks ATR(14)=46,30 el 24-jul-2026, snapshot, timeframe no confirmado) | sin dato fiable | ~230 USD (ATR(14) EMA, snapshot 24-oct-2025) | Aiolux (snapshot); TipRanks (24-jul-2026) |

### Tabla 2-bis — ESTIMACIONES DERIVADAS de ATR intradía (NO son medidas)
Regla explícita usada: bajo aproximación de "raíz del tiempo", el rango de una vela ≈ ATR diario × √(duración de la vela ÷ duración del día). Con día de 24 h: factor 15m = √(0,25/24) = 0,102; 1h = √(1/24) = 0,204; 4h = √(4/24) = 0,408. **Es una aproximación cruda** (el rango real no escala exactamente así, sobre todo con huecos y noticias) y se ofrece solo para orden de magnitud; NO sustituye a una medida. ATR diario de partida entre paréntesis.

| Instrumento (ATR diario base) | 15 min (est.) | 1 hora (est.) | 4 horas (est.) |
|---|---|---|---|
| EURUSD (60 pips) | ~6,1 pips | ~12,2 pips | ~24,5 pips |
| GBPUSD (111 pips) | ~11,3 pips | ~22,6 pips | ~45,3 pips |
| USDJPY (100 pips) | ~10,2 pips | ~20,4 pips | ~40,8 pips |
| AUDUSD (70 pips) | ~7,1 pips | ~14,3 pips | ~28,6 pips |
| USDCHF (40 pips) | ~4,1 pips | ~8,2 pips | ~16,3 pips |
| XAUUSD (80 USD/oz) | ~8,2 USD | ~16,3 USD | ~32,6 USD |
| BTCUSD (2.930 USD) | ~299 USD | ~598 USD | ~1.196 USD |
| ETHUSD (230 USD) | ~23,5 USD | ~46,9 USD | ~93,8 USD |

---

## ENTREGA 3 — Coste relativo

**Fórmula general:**
Coste relativo (%) = (coste total de operar, en la unidad del instrumento) ÷ (ATR medio de la vela, misma unidad) × 100.

**Coste representativo elegido y por qué:** uso el **punto medio de la cuenta raw/ECN** (spread crudo medio + comisión convertida), porque es el modelo más usado por bots/EAs y el más comparable entre instrumentos. Valores representativos: EURUSD 0,8 pip; GBPUSD 0,9 pip; USDJPY 0,9 pip; AUDUSD 0,85 pip; USDCHF 0,8 pip; XAUUSD 0,25 USD/oz; BTCUSD 28 USD; ETHUSD 4,5 USD.

### Ejemplo completo paso a paso (EURUSD, vela de 1 hora)
1. Spread medio raw: 0,1 pip (IC Markets: media EURUSD 0,1 pip; Pepperstone Razor 0,1).
2. Comisión: 7 USD/lote redondo ÷ 10 USD por pip = 0,7 pip.
3. Coste total = 0,1 + 0,7 = **0,8 pip**.
4. ATR de 1h: **no hay medida real de 2 años** → uso la estimación derivada 60 × 0,204 = **12,2 pips** (marcado como estimación).
5. Coste relativo = 0,8 ÷ 12,2 × 100 = **6,6 %** (estimado).

### Tabla 3 — Coste relativo (%) con MEDIDAS REALES de ATR
Como no hay ATR real de 15m/1h/4h, casi todas las celdas quedan sin dato.

| Instrumento | 15 min | 1 hora | 4 horas |
|---|---|---|---|
| EURUSD | sin dato fiable | sin dato fiable | sin dato fiable |
| GBPUSD | sin dato fiable | sin dato fiable | sin dato fiable |
| USDJPY | sin dato fiable | sin dato fiable | sin dato fiable |
| AUDUSD | sin dato fiable | sin dato fiable | sin dato fiable |
| USDCHF | sin dato fiable | sin dato fiable | sin dato fiable |
| XAUUSD | sin dato fiable | ~0,7–1,3 % (usando ATR 1h flojo 20–35 pips≈2–3,5 USD y coste 0,25 USD; muy incierto) | sin dato fiable |
| BTCUSD | sin dato fiable | sin dato fiable | sin dato fiable |
| ETHUSD | sin dato fiable | sin dato fiable | sin dato fiable |

**Coste relativo con ATR DIARIO (referencia real, aunque el diario no era una de las velas pedidas):**
- EURUSD: 0,8 pip ÷ 60 pips = 1,33 %.
- GBPUSD: 0,9 ÷ 111 = 0,81 %.
- USDJPY: 0,9 ÷ 100 = 0,90 %.
- AUDUSD: 0,85 ÷ 70 = 1,21 %.
- USDCHF: 0,8 ÷ 40 = 2,00 %.
- XAUUSD: 0,25 USD ÷ 80 USD = 0,31 %.
- BTCUSD: 28 USD ÷ 2.930 USD = 0,96 %.
- ETHUSD: 4,5 USD ÷ 230 USD = 1,96 %.

### Tabla 3-bis — Coste relativo (%) con ESTIMACIONES DERIVADAS (NO son medidas)
Cociente del coste representativo entre el ATR estimado de la Tabla 2-bis. Solo orden de magnitud.

| Instrumento | 15 min | 1 hora | 4 horas |
|---|---|---|---|
| EURUSD | ~13,1 % | ~6,6 % | ~3,3 % |
| GBPUSD | ~8,0 % | ~4,0 % | ~2,0 % |
| USDJPY | ~8,8 % | ~4,4 % | ~2,2 % |
| AUDUSD | ~12,0 % | ~5,9 % | ~3,0 % |
| USDCHF | ~19,5 % | ~9,8 % | ~4,9 % |
| XAUUSD | ~3,0 % | ~1,5 % | ~0,8 % |
| BTCUSD | ~9,4 % | ~4,7 % | ~2,3 % |
| ETHUSD | ~19,1 % | ~9,6 % | ~4,8 % |

---

## Lista de advertencias (datos flojos, supuestos, posibles errores)
1. **ATR intradía = principal debilidad.** No hay medida pública de ATR de 2 años por vela de 15m/1h/4h. Todas las cifras intradía de las Tablas 2-bis y 3-bis son **estimaciones derivadas** con la regla raíz-del-tiempo, no medidas. La regla es cruda y puede errar bastante en velas cortas y en activos con huecos/noticias.
2. **Supuesto de brokers CFD para cripto:** para BTCUSD/ETHUSD se usan spreads de brokers CFD regulados (Pepperstone, IG), no exchanges al contado, para mantener homogeneidad. En exchanges el modelo de coste (comisión %, p. ej. Binance 0,10%/0,10% de partida) es distinto y se documenta aparte.
3. **Periodos distintos entre celdas.** El ATR diario mezcla fuentes con periodos diferentes: EURUSD "media 10 semanas" (jun-2026) y multianual; GBPUSD/AUDUSD tabla 2014–2025; BTC/ETH snapshots de un solo día (ago y oct-2025), NO medias de 2 años. No son estrictamente comparables entre sí ni cubren exactamente mediados 2024–mediados 2026.
4. **Snapshots de cripto están anticuados** (ago/oct-2025) y son ATR(14) EMA de un día, muy sensibles al régimen de ese momento (BTC ~2.930 USD de ATR corresponde a precios de seis cifras). Con otro precio/volatilidad, cambian mucho.
5. **Unidad del oro ambigua.** Las fuentes discrepan sobre cuánto vale 1 "pip" de oro (0,01 / 0,10 / 1,00 USD). Medí el oro en dólares por onza para evitarlo, pero cualquier cifra de oro en "pips" de terceros hay que tomarla con cuidado.
6. **Spread es variable, no fijo.** Los spreads medios de broker son promedios; se ensanchan en noticias y en sesiones de baja liquidez. El coste real de un bot puede ser mayor que el "típico".
7. **Comisión en pips depende del valor del pip.** En USDJPY y USDCHF el valor del pip no es 10 USD, así que 7 USD/lote no equivale a 0,7 pip (ver conversión). Esto afecta al coste representativo de esos dos pares.
8. **Coste representativo elegido (punto medio raw/ECN)** es una decisión mía; si el bot usara cuentas spread-only, los costes en pips serían bastante mayores (p. ej. EURUSD 0,9–1,5 pip en vez de 0,8).
9. **Corrección sobre el oro:** al contrario que la cripto, el oro en cuentas raw (p. ej. Pepperstone Razor) SÍ suele llevar comisión además del spread crudo; el modelo "raw spread + commission" de XAU/USD está confirmado en la documentación oficial de Pepperstone.
10. **Fuentes secundarias.** Varias cifras de spread/volatilidad vienen de reseñas (BrokerChooser, BestBrokers, CompareForexBrokers, Commodity.com, Traders Union) que citan al broker, no siempre de la web oficial. Los PDF oficiales de Pepperstone e IC Markets, y las páginas de pricing oficiales, sí son primarios.

## Lo que un experto vería (riesgos y puntos ciegos no evidentes)
- **El spread varía por sesión y por noticias.** Un ATR de 1h de "12 pips" y un spread de "0,8 pip" conviven mal si el bot opera justo en el minuto de un dato macro, cuando el spread puede multiplicarse por 5–10 y el ATR dispararse. El coste relativo "medio" oculta esa cola.
- **El swap/financiación nocturna NO está incluido** y puede dominar el coste de un bot que mantiene posiciones: en cripto CFD Pepperstone cobra del orden de -22,5% anual en largos de BTC (ejemplo de su propio PDF: a 95.000 USD de nocional, ≈ -59 USD/día en un lote), muy por encima del spread.
- **El slippage (deslizamiento) tampoco está incluido.** En oro y cripto el deslizamiento en entradas/salidas puede igualar o superar el spread, sobre todo en velas de 15m (fuentes de oro citan 3–10 pips de slippage normal y "mucho más" en noticias).
- **El ATR de 2 años mezcla regímenes.** 2024–2026 incluye tramos de baja y alta volatilidad; una media de 2 años puede no parecerse a lo que el bot verá el mes que opere. Para un bot importa más la distribución (percentiles) que la media.
- **Puntos ciegos de la propia pregunta:** para decidir bien faltan datos que no se piden: (a) **tamaño de cuenta y de posición** (define si la comisión pesa mucho o poco), (b) **frecuencia de operaciones del bot** (a más trades, más peso del coste), (c) **horario de operación** (el coste relativo cambia radicalmente por sesión), (d) **si el bot mantiene overnight** (entonces manda el swap, no el spread), (e) **apalancamiento y margen**, (f) **calidad de ejecución del broker** (rechazos, requotes). Sin (b) y (c), el "coste relativo por vela" es solo una foto parcial.

---

## Lista de fuentes (con enlaces y fechas de los datos)

**Costes de broker (primarias):**
- IC Markets — Raw Spread Account y pricing: media EURUSD 0,1 pip, comisión 3,50 USD/lado (7 USD lote redondo); https://www.icmarkets.com/global/en/trading-accounts/raw-spread-account y https://www.icmarkets.com/global/en/trading-pricing/spreads (consultado jul-2026).
- IC Markets — Trading Costs (ejemplo comisión y swaps): https://www.icmarkets.eu/en/trading-pricing/trading-costs (consultado jul-2026).
- Pepperstone — "Costs and Charges Information & Examples", Pepperstone Ltd (FCA), versión 5.0, actualizado **febrero 2025**: spreads Razor EURUSD medio 0,1; XAUUSD min 0,05 / media 0,19; BTCUSD min 10 / media 20,22; ETHUSD min 3 / media 3,01; comisiones 7 USD (plataforma/MT4/MT5), 6 USD (cTrader); ejemplo swap cripto -22,5% anual; https://eu-assets.contentstack.com/v3/assets/bltaec35894448c7261/blt6f7d17fa2d5d2715/67bd29f42d615347c257652c/Pepperstone_Limited_Cost_and_Charges_-_February_2025_.pdf
- Pepperstone — Costs and Charges EU (CySEC), spreads cripto con datos **01–30 abril 2026**: BTCUSD min 30 / media 36,90; ETHUSD min 4 / media 7,04; https://files.pepperstone.com/legal/CYSEC/Costs_and_Charges_Information_Examples.pdf
- Pepperstone — pricing oficial (Razor: comisión desde 3,50 USD/lado; XAU/USD "raw spread + commission"): https://pepperstone.com/en/ways-to-trade/pricing/ ; cripto CFD (BTC "desde 15 USD", ETH "desde 2 USD"): https://pepperstone.com/en/markets/cryptocurrencies/ (consultado jul-2026).
- IG — pricing y detalles de producto (EURUSD/AUDUSD min 0,6; GBPUSD 0,9; oro min 0,3; Bitcoin min 40–95; Ethereum min 2): https://www.ig.com/en/charges y https://commodity.com/brokers/ig-review/ (IG Review, actualizado feb-2026).
- OANDA — spreads (EURUSD spread-only media ~1,4 pip; modelo premium 0,1 pip + 5 USD/lado): https://www.bestbrokers.com/reviews/oanda/spreads-fees-and-commissions/ y https://www.compareforexbrokers.com/us/oanda-review/ (2026).
- XM — spreads/comisiones (Zero media EURUSD 0,2 pip + 3,50 USD/lado; Ultra Low 0,6–1,1 pip): https://www.bestbrokers.com/reviews/xm/spreads-fees-and-commissions/ y https://brokerchooser.com/broker-reviews/xm-review/xm-forex-spread (2026).
- Exness — comisiones metales (XAUUSD 3,5 USD/lado raw, 5,5 USD Zero): https://get.exness.help/hc/en-us/articles/17854173039388-Commodities (consultado jul-2026).
- IC Markets comisiones (comparativa): https://www.compareforexbrokers.com/reviews/ic-markets-review/spreads-fees/ (mar-2026).
- Binance (referencia exchange al contado): comisión spot estándar 0,10% maker/taker de partida (2026), Traders Union / Bitget Academy.

**Volatilidad / ATR:**
- Trade That Swing — EURUSD volatilidad (media 10 sem. 60 pips), fecha del artículo **12-jun-2026**, base Mataf: https://tradethatswing.com/analyzing-eur-usd-volatility-for-day-trading-purposes/
- forex.in.rs — "How Many Pips Does EURUSD Move Daily" (2023: 87 pips; multianual ~75 pips): https://www.forex.in.rs/how-many-pips-does-eurusd-move-daily/
- offbeatforex — tabla Average Daily Range 2014–2025 (GBPUSD ~111,5; AUDUSD ~70,5): https://offbeatforex.com/forex-average-daily-range-table/
- PriceActionNinja — cheatsheet de volatilidad 2025 (USDJPY ~100, USDCHF ~40, EURUSD ~75): https://priceactionninja.com/forex-pair-volatility-cheatsheet-updated-2025/
- Headway — rangos diarios típicos 2026: https://hw.online/faq/average-daily-movements-in-the-forex-market-understanding-average-pip-ranges-and-volatility/
- Pro-Scalper — ATR de oro (H1 20–35 pips; diario 150–300 pips; sin periodo): https://www.pro-scalper.com/indicators/atr-gold-trading y https://www.pro-scalper.com/gold-market/gold-volatility-xauusd
- Aiolux — ATR(14) EMA diario: BTCUSD ~2.930 USD (19-ago-2025), ETHUSD 230 USD (24-oct-2025): https://aiolux.com/reports/analytics-technical-indicators?symbol=BTCUSD&tab_name=atr y ...symbol=ETHUSD...
- TipRanks — ETH-USD ATR(14) 46,30 (snapshot 24-jul-2026): https://www.tipranks.com/cryptocurrency/eth-usd/technical-analysis
- FX Leaders — lectura intradía puntual de ATR de oro ≈9,68 (jul-2026): https://www.fxleaders.com/live-rates/gold/
- Mataf — metodología ATR de volatilidad forex: https://www.mataf.net/en/forex/tools/volatility
- Myfxbook / MarketMilk (Babypips) — herramientas de volatilidad por hora/día/mes (valores no extraíbles por widget JS): https://myfxbook.com/forex-market/volatility y https://marketmilk.babypips.com/

*Nota final: este documento mide y documenta; la elección del mercado corresponde a otra persona con estos números delante.*