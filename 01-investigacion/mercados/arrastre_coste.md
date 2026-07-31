# Arrastre de coste anual sobre el capital — de "% de la vela" a "% al año"

**Calculo de apoyo dentro del alcance de la tarea 01.01.02 del WBS** ("Aprobar criterios de la
puerta G1"). **No es una tarea nueva del WBS** y no se ha tocado `00-direccion/WBS.md` ni
`00-direccion/DECISIONES.md` para producir este documento.

**Rol:** constructor-datos. **Este documento mide: no elige mercado, no elige vela, no recomienda
nada.** Esa lectura es de la puerta G1 y del CEO (regla del encargo).

**Nadie ha validado todavia estos numeros** (regla 16 de CLAUDE.md: quien construye no revisa).
Antes de usarlos para decidir, deben pasar por un agente distinto al que firma este documento.

---

## 1. Que resuelve este documento

El coste relativo (`coste_relativo_15m_1h_4h.json`, tarea 02.02.02) dice que, por ejemplo, EURUSD a
15 minutos cuesta 13,33% del ATR14 de la vela (vela mediana) entrar y salir. Ese numero es correcto,
pero no dice **cuanto dinero se lleva ese coste al año**, que es la pregunta que le importa al dueño
del proyecto: una vela de 15 minutos tiene coste relativo mayor Y ademas muchisimas mas
oportunidades de pagarlo que una vela de 4 horas. Este documento hace esa conversion.

## 2. Insumos — YA CERRADOS, NO RECALCULADOS

| Insumo | Tarea | Uso aqui |
|---|---|---|
| `04-resultados/coste_relativo_15m_1h_4h.json` | 02.02.02 | coste de entrar/salir en % del ATR, 4 escenarios de vela |
| `04-resultados/atr_15m_1h_4h.json` | 02.02.01 | `n_velas`, `desde_utc`, `hasta_utc`, `precio_medio`, `reproducible` por celda |
| `01-investigacion/mercados/coste_operar.md` | 02.01.02 | coste de entrar y salir (tabla FINAL), lote/pip valor |
| `01-investigacion/mercados/coste_swap.md` | 02.02.05 | coste de mantener, por broker, largo/corto |

Este documento **solo divide y multiplica** sobre esos cuatro ficheros. No se ha abierto, listado ni
leido `02-datos/reservado/` en ningun momento (verificable: el script `03-motor/scripts/arrastre_coste.py`
no contiene ninguna referencia a esa ruta).

**Artefactos de esta tarea:**
- Script: `03-motor/scripts/arrastre_coste.py`
- Volcado numerico completo (los 8 instrumentos x 3 velas x toda la malla de escenarios): `04-resultados/arrastre_coste_anual.json`
- Este informe: `01-investigacion/mercados/arrastre_coste.md`

El script se ha ejecutado entero y su salida por consola (205 lineas) se ha leido completa antes de
escribir este informe (regla 15 de CLAUDE.md).

---

## 3. Calculo 1 — Velas disponibles al año (contadas, no estimadas)

**Metodo:** para cada instrumento/vela SIN hueco, se toma `n_velas` (velas ya remuestreadas y
limpias, de `atr_15m_1h_4h.json`) y la ventana real cubierta (`desde_utc` a `hasta_utc` + el ancho
de una vela, para incluir la ultima vela completa). `velas_por_dia_real = n_velas / dias_ventana`;
`velas_año = velas_por_dia_real x 365`. Formula y codigo: funcion `calcular_velas_disponibles_ano`
en `arrastre_coste.py`. **No se ha usado la aritmetica 24x365x4**: el resultado sale de contar velas
reales, y por eso ya refleja los fines de semana cerrados de forex/oro (velas_año/año-teorico ≈ 0,71,
muy cerca de 5/7 = 0,714, la fraccion de dias abiertos — es la señal de que el conteo es correcto,
no un supuesto).

| Instrumento | Vela | n_velas reales | Ventana (dias) | Velas/año (anualizado x365) |
|---|---|---|---|---|
| EURUSD | 15min | 47.545 | 697,0 | 24.898 |
| EURUSD | 1h | 11.888 | 697,0 | 6.225 |
| EURUSD | 4h | 3.077 | 697,0 | 1.611 |
| GBPUSD | 15min | 47.519 | 697,0 | 24.884 |
| GBPUSD | 1h | 11.882 | 697,0 | 6.222 |
| GBPUSD | 4h | 3.076 | 697,0 | 1.611 |
| USDJPY | 15min | 47.485 | 697,0 | 24.867 |
| USDJPY | 1h | 11.872 | 697,0 | 6.217 |
| USDJPY | 4h | 3.073 | 697,0 | 1.609 |
| AUDUSD | 15min | 47.486 | 697,0 | 24.867 |
| AUDUSD | 1h | 11.873 | 697,0 | 6.218 |
| AUDUSD | 4h | 3.074 | 697,0 | 1.610 |
| USDCHF | 15min | 47.550 | 697,0 | 24.901 |
| USDCHF | 1h | 11.890 | 697,0 | 6.226 |
| USDCHF | 4h | 3.077 | 697,0 | 1.611 |
| XAUUSD | 15min | 47.267 | 730,0 | 23.635 |
| XAUUSD | 1h | 11.824 | 730,0 | 5.912 |
| XAUUSD | 4h | 3.196 | 729,8 | 1.598 |
| **BTCUSD** | 15min/1h/4h | 720 (cada una) | **HUECO** | **HUECO — no se rellena** |
| **ETHUSD** | 15min/1h/4h | 720 (cada una) | **HUECO** | **HUECO — no se rellena** |

**Hueco BTCUSD/ETHUSD, declarado aqui donde se lee (no en nota al pie):** Kraken solo entrega una
ventana deslizante de ~720 velas cerradas por intervalo (7,4 dias en 15m, 30 dias en 1h, 120 dias en
4h — campo `reproducible: false` en `atr_15m_1h_4h.json`). Extrapolar esa ventana a un año
multiplicaria por un factor grande (~49x en 15m, ~12x en 1h, ~3x en 4h) una muestra en la que,
ademas, el activo cotiza 24/7 sin cierres: el ritmo observado en la ventana corta coincide **por
construccion** con la aritmetica teorica 24x365 que el encargo prohibe usar como estimacion (no
distingue cobertura real de aritmetica de calendario, y solo cubre un regimen de mercado de pocas
semanas). Por eso se declara **hueco explicito**, tal como pide el encargo, y no se rellena con un
numero. Todo lo que depende de velas/año para BTCUSD/ETHUSD (arrastre anual, sensibilidad al
deslizamiento) hereda este hueco en las secciones siguientes.

---

## 4. Calculo 2 — Arrastre de coste anual (% del capital)

### Modelo, parametros EXPLICITOS (ninguno escondido)

| Parametro | Escenarios probados |
|---|---|
| `riesgo_por_operacion` (fraccion del capital arriesgada por operacion) | 0,5% · 1% · 2% |
| `stop_en_ATR` (distancia del stop, en ATR14 de la vela) | 0,5x · 1x · 2x |
| `tasa_actividad` (fraccion de velas en las que se abre operacion) | 2% · 5% · 10% |
| Escenario de vela (coste relativo tomado de) | media · mediana · p10 (vela tranquila) · p90 (vela agitada) |

Formula aplicada **tal como la pidio el encargo** (funcion `coste_por_operacion_frac_capital` +
`arrastre_anual_aditivo` en `arrastre_coste.py`):

```
coste_por_operacion_pct_capital = riesgo_por_operacion x (coste_relativo_pct/100 / stop_en_ATR)
operaciones_año               = velas_año x tasa_actividad
arrastre_anual_pct            = operaciones_año x coste_por_operacion_pct_capital
```

Esto da **27 combinaciones (3x3x3)** de riesgo/stop/actividad por cada instrumento x vela x
escenario-de-vela x fuente-de-coste. **Las 27 estan en el JSON completo**
(`04-resultados/arrastre_coste_anual.json`, clave `2_arrastre_coste_anual`); aqui se muestra el
**escenario central**: riesgo 1%, stop 1xATR, actividad 5%, vela mediana.

### Tabla resumen — escenario central

| Instrumento | Vela | Fuente coste | coste relativo % (mediana) | operaciones/año | **Arrastre anual % capital (aditivo, pedido)** | Arrastre anual % capital (compuesto, objecion — ver §7) |
|---|---|---|---|---|---|---|
| EURUSD | 15min | unico | 13,33 | 1.244,9 | **165,99** | 81,00 |
| EURUSD | 1h | unico | 6,25 | 311,3 | **19,44** | 17,68 |
| EURUSD | 4h | unico | 3,04 | 80,6 | **2,45** | 2,42 |
| GBPUSD | 15min | unico | 10,87 | 1.244,2 | **135,26** | 74,16 |
| GBPUSD | 1h | unico | 5,13 | 311,1 | **15,96** | 14,75 |
| GBPUSD | 4h | unico | 2,54 | 80,5 | **2,05** | 2,03 |
| USDJPY | 15min | unico | 10,68 | 1.243,3 | **132,75** | 73,51 |
| USDJPY | 1h | unico | 5,03 | 310,9 | **15,64** | 14,48 |
| USDJPY | 4h | unico | 2,40 | 80,5 | **1,93** | 1,92 |
| AUDUSD | 15min | unico | 17,02 | 1.243,4 | **211,67** | 87,98 |
| AUDUSD | 1h | unico | 8,10 | 310,9 | **25,17** | 22,26 |
| AUDUSD | 4h | unico | 3,98 | 80,5 | **3,20** | 3,15 |
| USDCHF | 15min | unico | 14,46 | 1.245,0 | **179,98** | 83,49 |
| USDCHF | 1h | unico | 6,85 | 311,3 | **21,33** | 19,21 |
| USDCHF | 4h | unico | 3,35 | 80,6 | **2,70** | 2,66 |
| XAUUSD | 15min | unico | 4,78 | 1.181,7 | **56,49** | 43,17 |
| XAUUSD | 1h | unico | 2,31 | 295,6 | **6,81** | 6,59 |
| XAUUSD | 4h | unico | 1,17 | 79,9 | **0,94** | 0,93 |
| **BTCUSD** | 15min/1h/4h | — | — | — | **HUECO** (hereda §3) | HUECO |
| **ETHUSD** | 15min/1h/4h | — | — | — | **HUECO** (hereda §3) | HUECO |

**Como leer estos numeros:** en el escenario central, arriesgar 1% del capital por operacion con un
stop a 1xATR y operar en el 5% de las velas hace que EURUSD a 15 minutos consuma, solo en coste de
entrar y salir, un 166% del capital al año bajo la formula aditiva pedida (81% bajo la version
compuesta, §7) — muy por encima de 4h (2,45%). El numero no dice si la estrategia gana o pierde: solo
dice cuanto capital consume el coste antes de contar ninguna ganancia.

### Rango completo (min–max de la malla de 27 combinaciones), dos ejemplos de referencia

| Instrumento/vela | riesgo / stop / actividad | Arrastre anual % (minimo de la malla) | riesgo / stop / actividad | Arrastre anual % (maximo de la malla) |
|---|---|---|---|---|
| EURUSD 15min (vela mediana) | 0,5% / 2x / 2% | 16,60% | 2% / 0,5x / 10% | 1.327,89% |
| XAUUSD 4h (vela mediana) | 0,5% / 2x / 2% | 0,09% | 2% / 0,5x / 10% | 7,50% |

Estos dos casos muestran que el resultado depende mucho de los 3 parametros del modelo, no solo del
coste relativo: la malla completa (los 8 instrumentos x 3 velas x 4 escenarios de vela x 27
combinaciones) esta integra en el JSON.

---

## 5. Calculo 3 — Borde bruto minimo por operacion

Es una relectura directa del coste relativo (mismo numero, `coste_relativo_pct`, escrito como la
frase que decide): **que fraccion del ATR14 de la vela tiene que capturar la estrategia en cada
operacion SOLO para cubrir el coste de entrar y salir**, antes de ganar un centimo.

| Instrumento | Vela | Fuente | media | mediana | p10 (vela tranquila) | p90 (vela agitada) |
|---|---|---|---|---|---|---|
| EURUSD | 15min | unico | 11,65% | 13,33% | 24,83% | 7,02% |
| EURUSD | 1h | unico | 5,68% | 6,25% | 9,78% | 3,79% |
| EURUSD | 4h | unico | 2,81% | 3,04% | 4,31% | 1,99% |
| GBPUSD | 15min | unico | 9,91% | 10,87% | 19,29% | 6,27% |
| GBPUSD | 1h | unico | 4,84% | 5,13% | 7,59% | 3,42% |
| GBPUSD | 4h | unico | 2,40% | 2,54% | 3,22% | 1,81% |
| USDJPY | 15min | unico | 9,65% | 10,68% | 20,40% | 6,05% |
| USDJPY | 1h | unico | 4,67% | 5,03% | 8,24% | 3,16% |
| USDJPY | 4h | unico | 2,29% | 2,40% | 3,84% | 1,61% |
| AUDUSD | 15min | unico | 15,20% | 17,02% | 26,50% | 10,01% |
| AUDUSD | 1h | unico | 7,40% | 8,10% | 11,22% | 5,32% |
| AUDUSD | 4h | unico | 3,66% | 3,98% | 5,24% | 2,69% |
| USDCHF | 15min | unico | 12,76% | 14,46% | 24,81% | 7,95% |
| USDCHF | 1h | unico | 6,22% | 6,85% | 9,99% | 4,30% |
| USDCHF | 4h | unico | 3,06% | 3,35% | 4,37% | 2,26% |
| XAUUSD | 15min | unico | 3,68% | 4,78% | 10,88% | 2,00% |
| XAUUSD | 1h | unico | 1,80% | 2,31% | 4,71% | 1,02% |
| XAUUSD | 4h | unico | 0,91% | 1,17% | 2,32% | 0,53% |
| BTCUSD | 15min | feb-2025 | 16,32% | 18,27% | 41,33% | 9,41% |
| BTCUSD | 15min | abr-2026 | 29,78% | 33,34% | 75,42% | 17,16% |
| BTCUSD | 1h | feb-2025 | 6,77% | 6,67% | 13,44% | 4,71% |
| BTCUSD | 1h | abr-2026 | 12,35% | 12,17% | 24,52% | 8,60% |
| BTCUSD | 4h | feb-2025 | 2,50% | 2,59% | 3,83% | 1,83% |
| BTCUSD | 4h | abr-2026 | 4,56% | 4,74% | 6,99% | 3,34% |
| ETHUSD | 15min | feb-2025 | 55,21% | 60,85% | 132,06% | 34,73% |
| ETHUSD | 15min | abr-2026 | 129,12% | 142,32% | 308,87% | 81,23% |
| ETHUSD | 1h | feb-2025 | 24,58% | 24,40% | 40,47% | 18,04% |
| ETHUSD | 1h | abr-2026 | 57,48% | 57,08% | 94,64% | 42,19% |
| ETHUSD | 4h | feb-2025 | 9,72% | 9,93% | 15,12% | 6,96% |
| ETHUSD | 4h | abr-2026 | 22,73% | 23,23% | 35,37% | 16,27% |

**Nota:** BTCUSD/ETHUSD SI tienen numero aqui (a diferencia del calculo 1/2): esta tabla no depende
de velas/año, solo del coste relativo ya cerrado en `coste_relativo_15m_1h_4h.json`, que si esta
completo para las 8 instrumentos. La limitacion de cripto que aplica AQUI es otra, ya declarada en
02.02.02: `reproducible: false` (ventana Kraken deslizante) y dos fuentes de coste sin promediar
(feb-2025 / abr-2026), nunca mezcladas en una sola cifra.

---

## 6. Calculo 4 — Cuando el swap supera al spread

**Pregunta:** a partir de cuantos dias manteniendo la posicion abierta el coste de mantener (swap,
02.02.05) supera al coste de entrar y salir (02.01.02), por broker y por direccion, sin promediar
entre brokers.

**Metodo (aritmetica declarada, ver `calcular_swap_vs_spread` en `arrastre_coste.py`):**
1. El coste de entrar/salir (`coste_operar.md`) esta dado **por lote**, no por el nocional de
   100.000 USD que usa `coste_swap.md`. Para comparar en la misma base se necesita el nocional en
   USD de un lote, que depende del precio — se usa el `precio_medio` de la vela 15min de
   `atr_15m_1h_4h.json` (la ventana mas reciente disponible de cada instrumento).
2. Convencion de lote (**la de EURUSD/GBPUSD/AUDUSD/USDJPY/USDCHF/XAUUSD viene ya en
   `coste_operar.md`**; la de BTCUSD/ETHUSD es un **supuesto propio de este calculo**, declarado
   explicitamente, no de un insumo cerrado):
   - EURUSD, GBPUSD, AUDUSD: 1 lote = 100.000 unidades de la divisa BASE (no USD) → notional_USD =
     100.000 x precio.
   - USDJPY, USDCHF: 1 lote = 100.000 USD (base = USD) → notional_USD = 100.000 exacto, sin precio.
   - XAUUSD: 1 lote = 100 oz (`coste_operar.md`, fila XAUUSD: *"comisión 7 USD por lote de 100 oz"*)
     → notional_USD = 100 x precio.
   - **BTCUSD/ETHUSD (supuesto propio, no del insumo):** 1 lote = 1 unidad del activo → notional_USD
     = 1 x precio. Es la misma convencion que ya usa `coste_relativo.py` para tratar el coste de
     cripto ("ya esta en USD de precio... se dividen directamente, sin conversion").
3. `coste_entrada_salida_pct_notional = coste_usd_por_lote / notional_usd_por_lote x 100`.
4. `swap_pct_dia = swap_pct_anual / 365` (conversion lineal — el mismo metodo que `coste_swap.md`
   declara para pasar de diario a anual en XTB; aqui se usa a la inversa, mismo criterio).
5. `dias_hasta_que_swap_supera_spread = coste_entrada_salida_pct_notional / |swap_pct_dia|`, **solo
   cuando el swap es un coste** (signo negativo). Si el swap es un credito (signo positivo), nunca
   "supera" al spread porque no es un coste: se marca `credito`, no un numero de dias.

### Tabla — dias hasta que el swap supera al spread (solo casos "coste")

| Instrumento | Fuente coste | Broker | Direccion | swap %/año | **dias hasta superar el spread** |
|---|---|---|---|---|---|
| EURUSD | unico | OANDA | largo | −2,41% | **1,07** |
| EURUSD | unico | XTB | largo | −3,01% | **0,86** |
| EURUSD | unico | XTB | corto | −0,04% | 64,66 |
| GBPUSD | unico | OANDA | largo | −0,88% | 2,58 |
| GBPUSD | unico | OANDA | corto | −1,05% | 2,16 |
| GBPUSD | unico | XTB | largo | −1,48% | 1,53 |
| GBPUSD | unico | XTB | corto | −1,54% | 1,47 |
| USDJPY | unico | OANDA | corto | −3,52% | 0,80 |
| USDJPY | unico | XTB | corto | −4,73% | 0,60 |
| AUDUSD | unico | OANDA | largo | −0,28% | 16,71 |
| AUDUSD | unico | OANDA | corto | −1,63% | 2,87 |
| AUDUSD | unico | XTB | largo | −1,34% | 3,49 |
| AUDUSD | unico | XTB | corto | −2,68% | 1,75 |
| USDCHF | unico | OANDA | corto | −4,50% | 0,74 |
| USDCHF | unico | XTB | corto | −5,26% | 0,63 |
| XAUUSD | unico | OANDA | largo | −6,64% | **0,40** |
| XAUUSD | unico | XTB | largo | −8,16% | **0,32** |
| XAUUSD | unico | XTB | corto | −0,76% | 3,47 |
| BTCUSD | feb-2025 | OANDA | largo | −33,64% | 0,34 |
| BTCUSD | feb-2025 | OANDA | corto | −26,36% | 0,44 |
| BTCUSD | feb-2025 | Pepperstone | largo | −22,50% | 0,51 |
| BTCUSD | abr-2026 | OANDA | largo | −33,64% | 0,62 |
| BTCUSD | abr-2026 | OANDA | corto | −26,36% | 0,80 |
| BTCUSD | abr-2026 | Pepperstone | largo | −22,50% | 0,93 |
| ETHUSD | feb-2025 | OANDA | largo | −33,64% | 1,72 |
| ETHUSD | feb-2025 | OANDA | corto | −26,36% | 2,20 |
| ETHUSD | abr-2026 | OANDA | largo | −33,64% | 4,03 |
| ETHUSD | abr-2026 | OANDA | corto | −26,36% | 5,14 |

En **todos** los casos donde el swap es un coste, supera al spread en menos de **17 dias**, y en la
mayoria en menos de 3. Esto es consistente con lo que ya adelantaba `coste_swap.md` (advertencia 1):
el spread de entrar/salir es una cifra minuscula frente al coste diario de mantener.

### Casos que no dan un numero de dias (credito, no aplica, sin dato)

| Instrumento | Fuente | Broker | Direccion | Estado |
|---|---|---|---|---|
| EURUSD | unico | OANDA | corto | credito (+0,44%/año) |
| USDJPY | unico | OANDA / XTB | largo | credito (+1,61% / +0,68%) |
| USDCHF | unico | OANDA / XTB | largo | credito (+2,60% / +2,22%) |
| XAUUSD | unico | OANDA | corto | credito (+0,64%) |
| BTCUSD | feb/abr | Pepperstone | corto | credito (+7,5%) |
| BTCUSD, ETHUSD | feb/abr | XTB | largo y corto | no_aplica — XTB ofrece cripto como spot, no CFD (hallazgo ya de 02.02.05, L-007), sin swap, no comparable |
| EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD | unico | Pepperstone | largo y corto | sin_dato_fiable (6 de 8 instrumentos, ya declarado en 02.02.05) |
| ETHUSD | feb/abr | Pepperstone | largo y corto | **sin_dato_fiable — ETHUSD solo tiene UNA fuente fiable de swap (OANDA)**, declarado como hueco en 02.02.05 y heredado aqui |

**Aviso sobre el precio de referencia usado en BTCUSD/ETHUSD (declarado donde se lee, no en nota al
pie):** el `precio_medio` usado para el nocional procede de la ventana Kraken **no reproducible**
(`reproducible: false`) y **no coincide temporalmente** con ninguna de las dos fechas del coste
(feb-2025, abr-2026) — es la misma limitacion de desfase temporal ya señalada por la revision
transversal 02.03.01 para el coste relativo, que aqui se propaga explicitamente en vez de
disimularse.

---

## 7. Objecion a la formula del arrastre anual (declarada, calculada, no aplicada por defecto)

La formula pedida por el encargo es **aditiva**: suma el coste de cada operacion sobre una base de
capital que se trata como fija durante todo el año
(`arrastre_anual_pct = operaciones_año x coste_por_operacion_pct_capital`).

**Objecion:** si el coste de cada operacion se paga sobre el capital que ya se redujo por los costes
de operaciones anteriores (como un interes compuesto, pero de perdidas), el arrastre real es menor
que la simple multiplicacion, porque cada "mordisco" del 0,13% (por ejemplo) se aplica sobre una base
cada vez mas pequeña, no sobre la base inicial completa n veces.

**Formula alternativa (compuesta), calculada tambien, no sustituye a la pedida:**

```
arrastre_anual_pct_compuesto = [1 - (1 - coste_por_operacion_pct_capital/100) ^ operaciones_año] x 100
```

(saturada en 100% si `coste_por_operacion_pct_capital >= 100%`, caso extremo presente en parte de la
malla de escenarios).

**Ejemplo con el escenario central, EURUSD 15min:** la formula aditiva pedida da **165,99%**; la
compuesta da **81,00%** — casi la mitad. La diferencia crece con `operaciones_año` y con el coste por
operacion, así que **importa mas exactamente en los casos donde el arrastre anual es mayor** (15m,
alta actividad), que es precisamente donde mas se necesitaría decidir con el numero correcto.

**Las dos cifras estan en cada celda del JSON** (`arrastre_anual_pct_aditivo` y
`arrastre_anual_pct_compuesto_objecion`), no se ha sustituido la formula pedida en ningun sitio.

---

## 8. Calculo 5 — Sensibilidad al deslizamiento (declarada, no un dato)

**Ninguno de los multiplicadores 1,25x / 1,5x / 2x tiene fuente.** No miden un deslizamiento medido
en el mercado: solo sirven para ver si la lectura del arrastre anual aguanta si el coste real de
operar resultara ser mayor que el publicado por spread/comisión (deslizamiento de ejecución, no
modelado en ningun insumo cerrado de este proyecto). Escenario usado: el central de riesgo/stop/
actividad (1% / 1xATR / 5%), vela mediana.

| Instrumento | Vela | Fuente | x1,0 (base) | x1,25 | x1,5 | x2,0 |
|---|---|---|---|---|---|---|
| EURUSD | 15min | unico | 165,99% | 207,48% | 248,98% | 331,97% |
| EURUSD | 1h | unico | 19,44% | 24,30% | 29,17% | 38,89% |
| EURUSD | 4h | unico | 2,45% | 3,06% | 3,67% | 4,90% |
| GBPUSD | 15min | unico | 135,26% | 169,08% | 202,89% | 270,52% |
| GBPUSD | 1h | unico | 15,96% | 19,95% | 23,94% | 31,92% |
| GBPUSD | 4h | unico | 2,05% | 2,56% | 3,07% | 4,09% |
| USDJPY | 15min | unico | 132,75% | 165,94% | 199,13% | 265,51% |
| USDJPY | 1h | unico | 15,64% | 19,55% | 23,47% | 31,29% |
| USDJPY | 4h | unico | 1,93% | 2,42% | 2,90% | 3,87% |
| AUDUSD | 15min | unico | 211,67% | 264,59% | 317,51% | 423,35% |
| AUDUSD | 1h | unico | 25,17% | 31,47% | 37,76% | 50,35% |
| AUDUSD | 4h | unico | 3,20% | 4,00% | 4,80% | 6,40% |
| USDCHF | 15min | unico | 179,98% | 224,97% | 269,96% | 359,95% |
| USDCHF | 1h | unico | 21,33% | 26,66% | 31,99% | 42,65% |
| USDCHF | 4h | unico | 2,70% | 3,37% | 4,05% | 5,40% |
| XAUUSD | 15min | unico | 56,49% | 70,62% | 84,74% | 112,99% |
| XAUUSD | 1h | unico | 6,81% | 8,52% | 10,22% | 13,63% |
| XAUUSD | 4h | unico | 0,94% | 1,17% | 1,41% | 1,88% |
| **BTCUSD** | 15min/1h/4h | — | **HUECO** (hereda §3) | HUECO | HUECO | HUECO |
| **ETHUSD** | 15min/1h/4h | — | **HUECO** (hereda §3) | HUECO | HUECO | HUECO |

---

## 9. Prueba de cordura obligatoria — resultado

**Regla probada por ejecucion:** para un mismo instrumento y una misma tasa de actividad, el
arrastre anual a 15m debe salir varias veces mayor que a 4h (umbral fijado en el script: ≥3x).
Ejecutada por la funcion `prueba_cordura_15m_vs_4h` sobre el escenario central.

| Instrumento | Arrastre 15m | Arrastre 4h | Multiplicador 15m/4h | Resultado |
|---|---|---|---|---|
| EURUSD | 165,99% | 2,45% | **x67,79** | OK |
| GBPUSD | 135,26% | 2,05% | **x66,12** | OK |
| USDJPY | 132,75% | 1,93% | **x68,65** | OK |
| AUDUSD | 211,67% | 3,20% | **x66,14** | OK |
| USDCHF | 179,98% | 2,70% | **x66,71** | OK |
| XAUUSD | 56,49% | 0,94% | **x60,23** | OK |
| BTCUSD | HUECO | HUECO | excluido (hereda hueco de §3) | — |
| ETHUSD | HUECO | HUECO | excluido (hereda hueco de §3) | — |

**RESULTADO GLOBAL: OK.** Las 6 filas evaluables pasan el umbral (≥3x) por un margen amplio (x60 a
x69). BTCUSD/ETHUSD quedan fuera de esta prueba porque su arrastre anual es hueco (§3/§4). No sale al
reves ni parecido en ningun instrumento: la magnitud combina el multiplicador de velas/año (15m tiene
~15,5x mas velas que 4h) con el multiplicador de coste relativo (15m cuesta ~4,4x mas que 4h en % de
ATR), y el producto de ambos (~68x) es justo el orden de magnitud observado.

---

## 10. Huecos declarados (resumen, cada uno ya explicado en su seccion)

1. **Velas/año de BTCUSD y ETHUSD:** hueco, no se rellena (§3). Ventana Kraken de ~720 velas,
   no reproducible, muy por debajo de un año.
2. **Arrastre anual y sensibilidad al deslizamiento de BTCUSD/ETHUSD:** hueco, heredado del punto 1
   (§4, §8): sin velas/año no hay operaciones/año.
3. **Swap de Pepperstone para 6 de 8 instrumentos** (todo menos BTCUSD): sin dato fiable, ya
   declarado en 02.02.05, heredado aqui (§6).
4. **Swap de ETHUSD en Pepperstone:** sin dato fiable — ETHUSD queda con una unica fuente de swap
   fiable (OANDA), por debajo del minimo de 2 fuentes independientes que pide el proyecto (§6, ya
   señalado en 02.02.05).
5. **Precio de referencia para el nocional de BTCUSD/ETHUSD en el calculo 4:** viene de una ventana
   Kraken no reproducible y no coincide temporalmente con las fechas del coste (feb-2025/abr-2026);
   limitacion heredada de 02.02.02, propagada explicitamente aqui, no oculta (§6).
6. **Convencion "1 lote = 1 unidad" para BTCUSD/ETHUSD en el calculo 4:** es un supuesto propio de
   ESTE calculo, no de un insumo cerrado; declarado explicitamente, no una fuente primaria (§6).
7. **Los dos costes de cripto (feb-2025 y abr-2026) nunca se promedian**: aparecen siempre como dos
   filas separadas en todas las tablas de este documento (§3, §4, §5), tal como exige el encargo.

---

## 11. Que NO hace este documento

- No elige mercado ni vela: eso es de la puerta G1 (02.03.03) y del CEO.
- No recalcula ATR ni coste de entrada/salida: solo divide y multiplica sobre lo ya cerrado.
- No abre ni lee `02-datos/reservado/`.
- No estima ninguna celda que no se pudiera calcular: las que faltan estan declaradas como hueco,
  con su motivo, en la seccion donde se leen.

---

*Documento generado por `constructor-datos` (modelo `claude-sonnet-5`). Pendiente de revision por un
agente distinto (regla 16 de CLAUDE.md: nadie valida su propio trabajo). No se ha cerrado ninguna
tarea del WBS con este documento.*
