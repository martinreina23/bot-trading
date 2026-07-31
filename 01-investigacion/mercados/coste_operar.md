# Coste de entrar y salir — tabla FINAL consolidada (tarea 02.01.02)

**Estado: PROVISIONAL.** La sustituye 04.01.02 con precios reales del broker elegido, una vez pasada la puerta G1.
No se elige ni se recomienda mercado en este documento: eso corresponde a G1 (02.03.03). Este documento entrega
números, método y fuentes.

**Esto NO es una investigación nueva.** Consolida la Entrega 1 de `entrega_brief_A.md` (tabla de costes de operar),
que el revisor **aceptó explícitamente** en `revision_brief_A.md` con fuentes primarias (PDF oficiales de
Pepperstone e IC Markets, páginas de precios oficiales). Este documento aplica en la tabla las dos correcciones que
el propio revisor detectó y calculó, pero que el analista solo explicó en una nota al pie sin llevarlas a su
tabla — exactamente lo que describe la lección **L-002** (`00-direccion/WBS.md`, fila L-002: *"Toda conversión de
unidades se aplica en la tabla final, no solo se explica en una nota al pie"*).

---

## Método

Coste total de ida y vuelta (round turn) = **spread medio** (ya es coste de ida y vuelta: se paga una vez al
cruzar de precio de compra a precio de venta) **+ comisión por lote redondo, convertida a la unidad natural del
instrumento** (pips en divisas, USD/oz en oro; en cripto CFD no hay comisión separada, el coste va en el spread).

- Spreads y comisiones brutas: `01-investigacion/mercados/entrega_brief_A.md`, Tabla 1 (Entrega 1, ACEPTADA).
- Conversión comisión → pips/dólares: `entrega_brief_A.md`, sección "Nota de conversión comisión → pips/dólares".
- Las dos correcciones (USDJPY, USDCHF): `01-investigacion/mercados/revision_brief_A.md`, sección 2 "ERROR
  CONFIRMADO — coste de USDJPY mal calculado", fila USDJPY y fila USDCHF de la tabla de conversión (localizadas
  por `grep`, ver cita exacta más abajo).

**Tipo de cuenta.** Raw/ECN (spread crudo + comisión) y spread-only (sin comisión, spread más ancho) **no son
comparables entre sí** (regla del encargo). La tabla principal usa **Raw/ECN** para las 6 divisas y el oro (porque
es el modelo con comisión declarada y es el más usado por bots/EAs, criterio ya fijado en la Entrega 1 aceptada) y
**CFD spread-only** para BTCUSD/ETHUSD (única modalidad que documentan las fuentes: "n/a" comisión, coste íntegro en
el spread). Se añade una columna de referencia con el spread-only de las divisas y el oro, **sin sumarla ni
mezclarla** con la columna Raw/ECN.

---

## Tabla FINAL — coste de entrar y salir (ida y vuelta), 8 instrumentos

| Instrumento | Tipo de cuenta usada | Spread medio (fuente) | Comisión convertida (fuente) | **COSTE TOTAL ida y vuelta** | Spread-only de referencia (NO comparable, NO sumar) |
|---|---|---|---|---|---|
| **EURUSD** | Raw/ECN | 0,1 pip — IC Markets, "average on EURUSD being 0.1 pips 24/5" (`entrega_brief_A.md`, Tabla 1, fila EURUSD; consultado jul-2026) | 0,7 pip — comisión 7 USD/lote ÷ pip valor 10 USD/lote (`entrega_brief_A.md`, Nota de conversión, línea "Divisas cotizadas en USD... 0,7 pip por lote redondo") | **0,8 pips** | 0,6–1,5 pip (IG media 0,9; OANDA 1,4–1,54; Pepperstone Standard 1,1; XM 0,6–1,1) — `entrega_brief_A.md` Tabla 1 |
| **GBPUSD** | Raw/ECN | 0,12 pip — IC Markets, min 0,04 / media 0,12 (`entrega_brief_A.md`, Tabla 1, fila GBPUSD; consultado jul-2026) | 0,7 pip — mismo cálculo que EURUSD (pip valor 10 USD/lote, cotiza en USD) | **0,82 pips** | 0,9 pip mín. (IG, Commodity.com Feb-2026) — `entrega_brief_A.md` Tabla 1 |
| **USDJPY** | Raw/ECN | 0,11 pip — IC Markets, min 0,03 / media 0,11 (`entrega_brief_A.md`, Tabla 1, fila USDJPY; consultado jul-2026) | **1,05 pips (CORREGIDO)** — pip valor ≈6,67 USD/lote, no 10; comisión 7 USD ÷ 6,67 = 1,05 pip (`revision_brief_A.md`, sección 2 "ERROR CONFIRMADO — coste de USDJPY mal calculado", fila USDJPY de la tabla de conversión: *"USDJPY \| 6,67 USD/lote \| 1,05 pips \| **1,16 pips** \| 0,90 pips"*) | **1,16 pips (CORREGIDO, no 0,90)** | 0,7–1,4 pip típico — `entrega_brief_A.md` Tabla 1 |
| **AUDUSD** | Raw/ECN | 0,15 pip — IC Markets, rango 0,1–0,2 sin media explícita publicada por la fuente; se toma el punto medio del rango declarado (nota metodológica, no es un promedio del broker) (`entrega_brief_A.md`, Tabla 1, fila AUDUSD) | 0,7 pip — mismo cálculo que EURUSD (cotiza en USD, pip valor 10 USD/lote) | **0,85 pips** | 0,6 pip mín. (IG, Commodity.com Feb-2026) — `entrega_brief_A.md` Tabla 1 |
| **USDCHF** | Raw/ECN | 0,17 pip — IC Markets, min 0,09 / media 0,17 (`entrega_brief_A.md`, Tabla 1, fila USDCHF; consultado jul-2026) | **0,56 pips (CORREGIDO)** — pip valor ≈12,50 USD/lote; comisión 7 USD ÷ 12,50 = 0,56 pip (`revision_brief_A.md`, sección 2 "ERROR CONFIRMADO — coste de USDJPY mal calculado", fila USDCHF de la tabla de conversión: *"USDCHF \| 12,50 USD/lote \| 0,56 pips \| **0,73 pips** \| 0,80 pips"*) | **0,73 pips (CORREGIDO, no 0,80)** | 1,0–1,7 pip típico — `entrega_brief_A.md` Tabla 1 |
| **XAUUSD** (oro) | Raw/ECN (Pepperstone Razor cobra comisión también en XAU/USD) | 0,19 USD/oz — Pepperstone Razor, "raw spreads... from 0.08 on XAU/USD", media 0,19 (Pepperstone "Costs and Charges", v5.0, **feb-2025**; `entrega_brief_A.md` Tabla 1, fila XAUUSD) | 0,07 USD/oz — comisión 7 USD por lote de 100 oz (`entrega_brief_A.md`, Nota de conversión, línea "Oro... 7 USD por lote de 100 oz → 0,07 USD/oz") | **0,26 USD/oz** | 0,15–0,30 USD/oz — `entrega_brief_A.md` Tabla 1 |
| **BTCUSD** (CFD) | CFD spread-only (sin comisión separada; "n/a" en Tabla 1) | 20,22 USD — Pepperstone, media, PDF "Costs and Charges" v5.0 (**feb-2025**) · **o** 36,90 USD — Pepperstone CySEC/EU, media, datos **01–30 abr-2026** (`entrega_brief_A.md`, Tabla 1, fila BTCUSD; dos documentos oficiales distintos, fechas distintas, no promediados) | n/a (sin comisión, coste íntegro en el spread) | **20,22 USD (feb-2025) / 36,90 USD (abr-2026)** — dos cifras, dos fuentes primarias fechadas, no una sola cifra inventada por promedio | — (no aplica: mismo modelo que Raw/ECN en cripto CFD) |
| **ETHUSD** (CFD) | CFD spread-only (sin comisión separada; "n/a" en Tabla 1) | 3,01 USD — Pepperstone, media, PDF "Costs and Charges" v5.0 (**feb-2025**) · **o** 7,04 USD — Pepperstone CySEC/EU, media, datos **01–30 abr-2026** (`entrega_brief_A.md`, Tabla 1, fila ETHUSD) | n/a (sin comisión, coste íntegro en el spread) | **3,01 USD (feb-2025) / 7,04 USD (abr-2026)** — dos cifras, dos fuentes primarias fechadas, no promediadas | — (no aplica: mismo modelo que Raw/ECN en cripto CFD) |

---

## Confirmación explícita de las dos correcciones (núcleo de esta tarea)

- **USDJPY sale 1,16 pips EN LA TABLA** (fila USDJPY, columna "COSTE TOTAL ida y vuelta"), no en una nota al pie. El
  analista había usado 0,90 pips; el valor correcto, calculado y verificado en `revision_brief_A.md` (sección 2
  "ERROR CONFIRMADO — coste de USDJPY mal calculado", fila USDJPY de la tabla de conversión), es 1,16 pips = spread
  medio 0,11 + comisión corregida 1,05 (pip valor ≈6,67 USD/lote, no 10 USD/lote).
- **USDCHF sale 0,73 pips EN LA TABLA** (fila USDCHF, columna "COSTE TOTAL ida y vuelta"), no en una nota al pie. El
  analista había usado 0,80 pips; el valor correcto, calculado y verificado en `revision_brief_A.md` (sección 2
  "ERROR CONFIRMADO — coste de USDJPY mal calculado", fila USDCHF de la tabla de conversión), es 0,73 pips = spread
  medio 0,17 + comisión corregida 0,56 (pip valor ≈12,50 USD/lote).

---

## Huecos declarados (sin dato fiable, no estimados)

- **GBPUSD y AUDUSD:** IC Markets no publica una "media" explícita para el spread de estos dos pares en las fuentes
  disponibles (a diferencia de EURUSD, USDJPY y USDCHF, donde sí hay min/media explícitos). Para GBPUSD se usa el
  valor "media 0,12" que sí está explícito en `entrega_brief_A.md`. Para AUDUSD solo hay un rango (0,1–0,2 pip) sin
  media declarada por la fuente; se toma el punto medio del rango como aproximación transparente, marcada como tal
  en la tabla — no se presenta como un promedio publicado por el broker.
- **BTCUSD y ETHUSD:** no hay un único spread medio "actual". Hay dos documentos oficiales de Pepperstone con
  fechas distintas (feb-2025 y abr-2026, este último para la entidad CySEC/EU) que dan medias distintas. Se
  presentan ambas cifras, con su fecha, en vez de promediarlas o elegir una arbitrariamente.
- **Coste de mantener la posición (swap/financiación):** NO está en esta tabla por diseño (el alcance de 02.01.02
  es solo entrar y salir). Ya está medido aparte en `01-investigacion/mercados/coste_swap.md` (tarea 02.02.05,
  hecha 31/07), y en cripto CFD es entre 20 y 30 veces mayor que el coste de entrar y salir. Lección L-003 aplica:
  medir solo entrada/salida da una foto incompleta; por eso este documento remite explícitamente al otro.
- **Precios de broker real:** esta tabla usa spreads y comisiones publicados por Pepperstone e IC Markets como
  referencia de mercado, no del broker que finalmente se contrate (eso se decide en 04.01.01, después de G1). Por
  eso todo el documento es PROVISIONAL.

## Advertencias de comparabilidad

1. **No sumar ni mezclar** la columna "COSTE TOTAL ida y vuelta" (Raw/ECN) con la columna de referencia
   spread-only: son dos modelos de cuenta distintos y excluyentes.
2. **Las unidades no son comparables entre instrumentos** sin normalizar por el movimiento medio de cada uno (ATR).
   Esa normalización es la tarea 02.02.02 (coste relativo, bloqueada hasta que ambos insumos —esta tabla y el ATR
   de 02.02.01— estén listos; el ATR ya está calculado y aceptado en `atr_real_15m_1h_4h.md`).
3. Ninguna cifra de esta tabla ha sido estimada por quien firma este documento: todas proceden de spreads y
   comisiones publicados por broker (Pepperstone, IC Markets) más aritmética directa de conversión de unidades, con
   las dos correcciones documentadas y citadas.

---

## Fuentes primarias citadas

- IC Markets — Raw Spread Account y pricing oficial: https://www.icmarkets.com/global/en/trading-accounts/raw-spread-account y https://www.icmarkets.com/global/en/trading-pricing/spreads (consultado jul-2026). Citado en `entrega_brief_A.md`, Tabla 1 y lista de fuentes.
- Pepperstone — "Costs and Charges Information & Examples", v5.0, actualizado **febrero 2025**: https://eu-assets.contentstack.com/v3/assets/bltaec35894448c7261/blt6f7d17fa2d5d2715/67bd29f42d615347c257652c/Pepperstone_Limited_Cost_and_Charges_-_February_2025_.pdf. Citado en `entrega_brief_A.md`, Tabla 1 y lista de fuentes.
- Pepperstone — Costs and Charges EU (CySEC), datos **01–30 abril 2026**: https://files.pepperstone.com/legal/CYSEC/Costs_and_Charges_Information_Examples.pdf. Citado en `entrega_brief_A.md`, Tabla 1 y lista de fuentes.
- `01-investigacion/mercados/entrega_brief_A.md` — Entrega 1, Tabla 1 y "Nota de conversión comisión → pips/dólares" (ACEPTADA por el revisor, ver `revision_brief_A.md` sección 1).
- `01-investigacion/mercados/revision_brief_A.md` — sección 2 "ERROR CONFIRMADO — coste de USDJPY mal calculado", tabla de conversión (filas USDJPY y USDCHF, valores corregidos 1,16 y 0,73), localizado por `grep` antes de citarlo.
- `00-direccion/WBS.md` — fila L-002 (lección que exige aplicar la conversión en la tabla, no en nota al pie).

---

*Este documento mide y consolida: no elige mercado ni recomienda ninguno. La elección corresponde a la puerta G1
(tarea 02.03.03). Estado PROVISIONAL — lo sustituye 04.01.02 con precios reales del broker elegido.*
