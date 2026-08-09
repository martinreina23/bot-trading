# Tamaño mínimo operable de XAUUSD 4h y requisito real de lote para el broker

**Tarea:** 04.01.04 — subtarea NUEVA dentro del alcance de 04.01.01, creada por el orquestador
(regla 2 de CLAUDE.md). **Agente:** `constructor-datos` (`claude-sonnet-5`; no hizo falta respaldo).

**Método:** cálculo sobre datos brutos ya en disco (regla 14 de CLAUDE.md), sin red. Script:
`03-motor/scripts/tamano_minimo_operable.py`, ejecutado entero y su salida completa leída antes de
escribir este informe (regla 15 de CLAUDE.md). Reejecutado una segunda vez: el JSON de salida es
byte a byte idéntico (`diff` sin diferencias). Salida numérica completa:
`04-resultados/tamano_minimo_operable.json`.

**Entradas usadas, y solo estas:**
- `04-resultados/atr_15m_1h_4h.json` → `instrumentos.XAUUSD.velas.4h.atr14_mediana` = **22,152714285714215 USD/oz**
  (y `atr14_medio` = 28,42890772406983 USD/oz, solo para el punto 7, tal como exige el encargo).
- `04-resultados/atr_15m_1h_4h.json` → `instrumentos.EURUSD.velas.4h.precio_medio` = **1,1290693760155996
  USD por 1 EUR** — tipo de cambio de fuente primaria, independiente de A3, usado en el punto 2 para
  cerrar sin circularidad (corrección ronda 1).
- `04-resultados/veredictos/veredicto_criterios_g1.md`, sección A3, cita literal «2.215 USD = 1.962 EUR».
- `00-direccion/WBS.md`, sección «## Puertas», viñeta **G1-C6**: riesgo máximo 1% del capital, stop
  **1 x ATR MEDIANA** (no la media), capital declarado 1.000-2.000 EUR.
- `00-direccion/DECISIONES.md`, **D-11** (rango de capital 1.000-2.000 EUR) y **D-14** (parada dura
  automática al -30% del capital inicial ingresado).
- `01-investigacion/mercados/coste_relativo.md` (confirma el mismo ATR14 mediana de XAUUSD 4h,
  22,1527 USD/oz, usado por A3).
- `01-investigacion/mercados/comparacion_brokers.md`, **Tabla A, fila del criterio 1** («1. Lote
  mínimo y fraccionado 0,1 oz — anclado a la entidad que admite España, ronda 3...»), columnas
  **«XTB Limited»** (pedido mínimo 0,3 oz; paso 0,1 oz) e **«IC Markets (EU) Ltd»** (1 oz) — origen
  de las tres etiquetas de lote usadas en los puntos 4 y 6. **Añadida en esta corrección (ronda 1):
  se usó en la ronda 1 sin declararla, defecto señalado por la revisión (regla 12 de CLAUDE.md).**

No se ha tocado `01-investigacion/mercados/comparacion_brokers.md`, no se elige ni descarta broker,
no se recomienda nada, no se ha tocado `00-direccion/WBS.md`, no se ha usado red, no se ha usado
ATR medio salvo en el punto 7.

---

## 1. Tipo EUR/USD implícito en la cita de A3

A3 escribe «2.215 USD = 1.962 EUR» sin declarar el tipo de cambio. Se reconstruye de dos formas:

- **(a) De los dos números redondeados que cita A3:**
  `rate = USD_citado / EUR_citado = 2.215 / 1.962 = 1,128950 USD por 1 EUR`
- **(b) Con precisión completa**, usando el ATR14 mediana exacto (el mismo cálculo que A3 dice haber
  hecho) y el único dato en EUR que A3 publica:
  `USD_exacto = ATR14_mediana(4h) / RISK_PCT = 22,152714285714215 / 0,01 = 2.215,271429 USD`
  `rate = USD_exacto / EUR_citado = 2.215,271429 / 1.962 = 1,129088 USD por 1 EUR`

**Se adopta `rate = 1,129088` para el resto del cálculo**, declarado explícitamente aquí, no
supuesto en silencio. A3 no lo dice, como avisa el encargo.

---

## 2. Qué representan los 1.962 EUR — aritmética, no lectura del texto

**Hipótesis probada:** 1.962 EUR es el capital necesario para que el riesgo de **1 oz**, con stop
**1 x ATR14_mediana(4h)**, sea el **1% del capital**.

### Tramo USD — se demuestra desde el dato primario solo, sin circularidad

```
riesgo_usd_1oz   = STOP_MULT_ATR * ATR14_mediana(4h) = 1 * 22,152714 = 22,152714 USD
capital_usd_1oz  = riesgo_usd_1oz / RISK_PCT          = 22,152714 / 0,01 = 2.215,271429 USD
```

`2.215,271429 USD` reproduce el «2.215 USD» de A3 desde el dato primario solo (ATR14 mediana), sin
usar ningún tipo de cambio. Esta parte no tiene el problema de abajo.

### Por qué la versión de la ronda 1 no demostraba nada (corrección ronda 1, regla 9 de CLAUDE.md)

La ronda 1 dividía `capital_usd_1oz` por el `rate` del punto 1 y presentaba el resultado (1.962,00 EUR,
diferencia 2,27e-13) como «confirmación». **Es una tautología, no una prueba**: `rate` (punto 1) se
había construido exactamente como `capital_usd_1oz / 1.962` — el mismo 1.962 que se quería demostrar.
Dividir de nuevo por ese `rate` reproduce 1.962 EUR con cualquier valor de ATR, sea cual sea; el
resultado no aporta información nueva sobre si 1.962 EUR es correcto.

### Tramo EUR — cierre sin circularidad, con tipo de cambio de fuente primaria independiente

Se sustituye `rate` por el tipo de cambio EUR/USD de un dato primario que no depende de A3 ni del
punto 1: `instrumentos.EURUSD.velas.4h.precio_medio` del mismo JSON de ATR.

```
eurusd_4h_precio_medio (primario)     = 1,129069 USD por 1 EUR
capital_eur_1oz_primario = capital_usd_1oz / eurusd_4h_precio_medio
                         = 2.215,271429 / 1,129069 = 1.962,033047 EUR
```

Diferencia con la cita de A3 (1.962 EUR): **+0,0330 EUR (+0,0017%)**.

**VEREDICTO:** el tramo USD queda demostrado desde el dato primario solo. El tramo EUR se cierra,
sin circularidad, contrastando con el tipo de cambio EURUSD 4h primario, y confirma la cifra de A3
dentro de un 0,0017% — una desviación explicable por el redondeo con el que A3 publica «1.962 EUR».
Los 1.962 EUR son, con este cierre, el capital que hace falta para que arriesgar **1 oz** con stop
**1xATR mediana** consuma el **1%** del capital.

---

## 3. Tamaño máximo operable (oz), stop 1xATR mediana, riesgo 1%

```
capital_usd    = capital_eur * rate
riesgo_max_usd = capital_usd * RISK_PCT
oz_max         = riesgo_max_usd / (STOP_MULT_ATR * ATR14_mediana(4h))
```

| Capital (EUR) | capital_usd | riesgo_max_usd (1%) | **oz_max** |
|---|---|---|---|
| 1.000 | 1.129,088394 | 11,290884 | **0,509684 oz** |
| 1.500 | 1.693,632591 | 16,936326 | **0,764526 oz** |
| 2.000 | 2.258,176788 | 22,581768 | **1,019368 oz** |

---

## 4. Capital mínimo (EUR) por tamaño mínimo real de broker

```
riesgo_usd  = lote_oz * STOP_MULT_ATR * ATR14_mediana(4h)
capital_usd = riesgo_usd / RISK_PCT
capital_eur = capital_usd / rate
```

| Lote | Origen | Cita (fila del criterio 1, `comparacion_brokers.md`) | riesgo_usd | capital_usd | **capital_eur** |
|---|---|---|---|---|---|
| 1,0 oz | IC Markets EU | Tabla A, fila criterio 1, columna «IC Markets (EU) Ltd»: «Minimum Lot Size 0,01 = 1 oz, Volume Step 0,01 = 1 oz» | 22,152714 | 2.215,271429 | **1.962,00 EUR** |
| 0,3 oz | pedido mínimo XTB Limited | Tabla A, fila criterio 1, columna «XTB Limited»: «Pedido mínimo 0,003 lote (0,3 oz)» | 6,645814 | 664,581429 | **588,60 EUR** |
| 0,1 oz | paso de XTB | Tabla A, fila criterio 1, columna «XTB Limited»: «paso mínimo de transacción 0,001 lote = 0,1 oz exactas» | 2,215271 | 221,527143 | **196,20 EUR** |
| 0,01 oz | — | — (no proviene de la comparativa) | 0,221527 | 22,152714 | **19,62 EUR** |

---

## 5. EL CÁLCULO QUE FALTA — OPERABILIDAD BAJO PÉRDIDA (lote indivisible, capital inicial 2.000 EUR)

**Fórmula del saldo umbral** (mismo cálculo que el punto 4, aplicado a cada lote fijo indivisible):
el riesgo en EUR de abrir ese lote no cambia con el saldo (depende solo del ATR y del tipo de
cambio); lo que cambia es el 1% del saldo, que se encoge según cae la cuenta. El saldo umbral es
aquel en el que `1% del saldo == riesgo_eur_del_lote`:

```
saldo_umbral_eur = (lote_oz * STOP_MULT_ATR * ATR14_mediana(4h) / RISK_PCT) / rate
caida_eur         = 2.000 − saldo_umbral_eur
caida_pct         = caida_eur / 2.000 * 100

floor_parada_dura_eur = 2.000 * (1 − 0,30) = 1.400 EUR   (D-14)
rango_permitido_eur   = 2.000 − 1.400 = 600 EUR            (rango de pérdida que D-14 permite antes de parar)

Si saldo_umbral_eur > floor_parada_dura_eur:
    fraccion_inoperable_del_rango = (saldo_umbral_eur − floor_parada_dura_eur) / rango_permitido_eur
Si saldo_umbral_eur <= floor_parada_dura_eur:
    fraccion_inoperable_del_rango = 0   (la parada dura corta la cuenta ANTES de que el lote deje de caber)
```

### TABLA DE TRES FILAS

| Lote indivisible | Saldo umbral (EUR) | Caída desde 2.000 EUR | Caída (%) | Suelo parada dura (D-14) | Fracción del rango permitido (0% a −30%) que queda INOPERABLE |
|---|---|---|---|---|---|
| **1,0 oz** | 1.962,00 | 38,00 EUR | **1,90%** | 1.400 EUR | **93,67%** |
| **0,3 oz** | 588,60 | 1.411,40 EUR | 70,57% | 1.400 EUR | **0,00%** |
| **0,1 oz** | 196,20 | 1.803,80 EUR | 90,19% | 1.400 EUR | **0,00%** |

**Lectura de la fila crítica (1,0 oz):** con lote mínimo indivisible de 1 oz, la cuenta deja de poder
abrir UNA posición sin superar el 1% de riesgo apenas cae un **1,90%** desde 2.000 EUR (a 1.962 EUR).
La parada dura de D-14 no llega hasta 1.400 EUR (−30%). Entre 1.962 EUR y 1.400 EUR —**562 de los 600
EUR que D-14 permite perder, el 93,67% de ese rango**— la cuenta ya no puede operar en absoluto con
1 oz, pero D-14 todavía no la ha parado: queda "viva" y sin poder operar durante casi todo el
recorrido permitido de pérdida.

**Lectura de 0,3 oz y 0,1 oz:** su saldo umbral (588,60 EUR y 196,20 EUR) está **por debajo** del
suelo de la parada dura (1.400 EUR). Es decir, la parada dura corta la cuenta a 1.400 EUR **antes**
de que ninguno de esos dos lotes deje de caber. Dentro de todo el rango que D-14 permite perder
(2.000 EUR → 1.400 EUR), la cuenta sigue pudiendo abrir posiciones de 0,3 oz o de 0,1 oz en el 100%
de ese rango: **0,00% inoperable**.

---

## 6. DERIVA EL REQUISITO — lote mínimo máximo admisible (dos motivos, no se mezclan)

**Motivo A (del punto 3):** que el lote quepa en el 1% de riesgo al capital inicial declarado —
`oz_max(capital_inicial)`.

**Motivo B (del punto 5):** que el lote siga siendo operable en el 1% de riesgo **hasta el suelo de
la parada dura de D-14**, no solo al capital inicial — `oz_max(capital_inicial * 0,7)`.

```
Extremo CONSERVADOR (1.000 EUR):
  Motivo A: oz_max(1.000 EUR)          = 0,509684 oz
  Motivo B: floor = 700 EUR; oz_max(700 EUR) = 0,356779 oz
  Motivo que ata (el más estricto de los dos): B
  LOTE MÍNIMO MÁXIMO ADMISIBLE = min(A, B) = 0,356779 oz   ≈ 0,36 oz

Extremo ALTO (2.000 EUR):
  Motivo A: oz_max(2.000 EUR)          = 1,019368 oz
  Motivo B: floor = 1.400 EUR; oz_max(1.400 EUR) = 0,713558 oz
  Motivo que ata (el más estricto de los dos): B
  LOTE MÍNIMO MÁXIMO ADMISIBLE = min(A, B) = 0,713558 oz   ≈ 0,71 oz
```

### Las DOS cifras exigidas por el encargo

| Extremo del rango de capital | LOTE MÍNIMO MÁXIMO ADMISIBLE |
|---|---|
| **1.000 EUR (conservador)** | **≈ 0,357 oz** |
| **2.000 EUR (alto)** | **≈ 0,714 oz** |

**DEMOSTRACIÓN de que son dos motivos distintos y no se mezclan (lo que pide el encargo):** en el
extremo alto (2.000 EUR), el Motivo A por sí solo (punto 3) dice que 1 oz **SÍ cabe**
(`oz_max(2.000 EUR) = 1,019368 oz > 1,0 oz`) — es justo el margen estrecho que ya declaraba A3
(«1.962 EUR cabe bajo el techo de 2.000»). **Pero el Motivo B (punto 5) por sí solo dice que 1 oz NO
es sostenible**: hace falta `oz_max(1.400 EUR) = 0,713558 oz`, muy por debajo de 1 oz. Es decir: **el
punto 3 NO exige lote fraccionado en el extremo alto, pero el punto 5 SÍ lo exige**, y con un margen
grande (0,71 oz frente a 1,0 oz, un 29% por debajo). El motivo que decide de verdad no es la cabida
al capital inicial (motivo A, ya conocido y ya publicado en A3): es la operabilidad hasta la parada
dura (motivo B), que es un cálculo distinto que A3 nunca hizo.

**Consecuencia directa sobre el listón de la comparativa de brokers:** de los cuatro tamaños del
punto 4, comparados contra el lote máximo admisible derivado en este punto (0,357 oz en el extremo
conservador, 0,714 oz en el extremo alto). Cada lote sale de `comparacion_brokers.md`, Tabla A, fila
del criterio 1 («1. Lote mínimo y fraccionado 0,1 oz — anclado a la entidad que admite España, ronda
3...»):
- **1,0 oz (IC Markets EU) — columna «IC Markets (EU) Ltd»: «Minimum Lot Size 0,01 = 1 oz, Volume
  Step 0,01 = 1 oz»: NO supera el motivo B en ningún extremo** (1,0 > 0,357 y 1,0 > 0,714).
- **0,3 oz (pedido mínimo de XTB Limited) — columna «XTB Limited»: «Pedido mínimo 0,003 lote
  (0,3 oz)»: SÍ supera el motivo B en los dos extremos** (0,3 < 0,357 y 0,3 < 0,714).
- **0,1 oz (paso de XTB) — columna «XTB Limited»: «paso mínimo de transacción 0,001 lote =
  0,1 oz exactas»: SÍ supera el motivo B en los dos extremos, con más margen todavía**
  (0,1 < 0,357 y 0,1 < 0,714).

**Margen del pedido mínimo de XTB Limited (0,3 oz) sobre el listón conservador:** 0,3 oz pasa el
extremo conservador (0,356779 oz) por **0,057 oz** (0,356779 − 0,3 = 0,056779 ≈ 0,057 oz, un 15,9%
del listón). Ese margen es función del **ATR14 mediana de XAUUSD 4h medido sobre la ventana que
cierra el 2026-07-29** (`instrumentos.XAUUSD.velas.4h.hasta_utc` del mismo JSON primario): es el
valor de un estimador estadístico sobre una ventana concreta de datos, no una holgura estructural
del bróker ni una garantía permanente — si la ventana o el estimador cambian, el margen cambia con
ellos.

Este párrafo no elige broker: solo compara la cifra de tamaño de cada fila del punto 4 contra el
lote máximo derivado aquí. La elección de broker sigue siendo de 04.01.01 y del CEO.

---

## 7. DEFECTO EN A3 — «0,1 oz ~252 EUR» usa ATR MEDIO, no MEDIANA (corrección, no edición)

A3 (`veredicto_criterios_g1.md`) afirma: «Con 0,1 oz el capital necesario es ~252 EUR».

```
Con ATR14_MEDIO XAUUSD 4h = 28,428908 USD/oz:
  capital_eur(0,1 oz, ATR medio)    = 0,1 * 28,428908 / 0,01 / 1,129088 = 251,7864 EUR  ≈ 252 EUR

Con ATR14_MEDIANA XAUUSD 4h = 22,152714 USD/oz:
  capital_eur(0,1 oz, ATR mediana)  = 0,1 * 22,152714 / 0,01 / 1,129088 = 196,2000 EUR  ≈ 196 EUR
```

**Las dos cifras:** ~252 EUR (con ATR medio) y ~196 EUR (con ATR mediana).

**Cuál corresponde al estimador que G1-C6 declara:** `00-direccion/WBS.md`, sección «## Puertas»,
viñeta G1-C6, cita literal: *"...con un stop de 1 x ATR MEDIANA (no la media, que en el oro esta
inflada un 28-30% por su pausa diaria)."* **El estimador declarado es la MEDIANA.**

**MARCADO COMO CORRECCIÓN** (no se edita `veredicto_criterios_g1.md`, artefacto cerrado; una
corrección es entrada nueva, regla 21 de CLAUDE.md): la cifra de A3 para 0,1 oz (~252 EUR) usa
`atr14_medio`, el mismo estimador que la propia sección A3 identifica como sesgado un 28-30% en el
oro por su pausa diaria y que corrige explícitamente para la cifra de 1 oz (2.215 USD / 1.962 EUR sí
usa la mediana). A3 es, por tanto, **internamente inconsistente**: corrige el sesgo para 1 oz pero no
para 0,1 oz, en el mismo párrafo. Con el estimador que G1-C6 declara (mediana), el capital real para
0,1 oz es **196,20 EUR**, no ~252 EUR.

---

## Resumen ejecutable (sin recomendar broker)

- Los 1.962 EUR de A3 son exactamente correctos: el tramo USD se demuestra desde el dato primario
  solo, y el tramo EUR se cierra sin circularidad contra el tipo de cambio EURUSD 4h primario
  (desviación 0,0017%) — capital para que 1 oz con stop 1xATR mediana arriesgue el 1%.
- El cálculo de cabida simple (punto 3) por sí solo **no** obliga a fraccionar en el extremo alto de
  capital (2.000 EUR): 1 oz cabe, por un margen de 0,019 oz.
- El cálculo de operabilidad bajo pérdida (punto 5) **sí** obliga a fraccionar, y con margen amplio:
  con lote indivisible de 1 oz, el 93,67% del rango de pérdida que D-14 permite (2.000→1.400 EUR)
  queda sin poder abrir ninguna posición dentro del 1% de riesgo. Con 0,3 oz o 0,1 oz, el rango entero
  sigue operable.
- El lote mínimo máximo admisible que sostiene ambos cálculos es **≈0,36 oz en el extremo
  conservador (1.000 EUR)** y **≈0,71 oz en el extremo alto (2.000 EUR)**.
- El pedido mínimo de XTB Limited (0,3 oz) pasa el extremo conservador **por 0,057 oz**: un margen
  que depende del ATR14 mediana de XAUUSD 4h medido sobre la ventana que cierra el 2026-07-29, no una
  holgura estructural.
- La cifra «~252 EUR» de A3 para 0,1 oz es un defecto: usa el estimador sesgado (ATR medio) que la
  propia G1-C6 descarta. La cifra correcta con el estimador declarado es **~196 EUR**.

**Nada de lo anterior elige, descarta o recomienda ningún broker.** Compara únicamente los cuatro
tamaños de lote ya conocidos (punto 4) contra el lote máximo derivado aquí (punto 6): esa
comparación es aritmética, no elección.
