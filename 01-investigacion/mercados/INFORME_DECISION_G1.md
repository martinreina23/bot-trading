# INFORME DE DECISIÓN — Puerta G1: mercados y tamaño de vela (Tarea 02.03.02)

**Agente:** `validador` (`claude-fable-5`, modelo principal disponible, sin respaldo — regla 29 de
CLAUDE.md). **Fecha:** 03/08/2026. **Orden:** del orquestador, ejecutada por Claude Code (C4 de
CLAUDE.md). **Método:** consolidación de los entregables cerrados de la Fase 02 (02.02.01 a
02.02.05 y 02.03.01) contra los siete criterios G1-C1..G1-C7 aprobados en D-11
(`00-direccion/DECISIONES.md`, sección `## D-11 · 2026-08-01 · Siete criterios de G1 aprobados
(G1-C1 a G1-C7)`; forma operativa en `00-direccion/WBS.md`, sección `## Puertas`). **No se ha
recalculado ningún artefacto cerrado** (ATR, costes, correlaciones, arrastre, deriva). La única
ejecución nueva es `03-motor/scripts/cestas_g1.py`, que LEE el JSON cerrado de correlaciones y
enumera qué cestas cumplen G1-C5 — comparación contra el umbral aprobado, no un recálculo
(regla 9 de CLAUDE.md, nivel 1; reproducible por cualquier tercero). **No se ha tocado
`02-datos/reservado/`** (regla 22 de CLAUDE.md). Referencias por nombre de sección o símbolo,
nunca por número de línea (regla 13 de CLAUDE.md). Todas las citas de decisiones y veredictos
fueron localizadas por grep antes de citarse (regla 12 de CLAUDE.md).

---

## 0. CONDICIÓN HEREDADA — el defecto del motivo 5, declarado con las palabras del veredicto

El ACEPTA de la revisión transversal 02.03.01 es **condicional**. Su texto exacto
(`04-resultados/veredictos/veredicto_fase_02.md`, sección `## VEREDICTO GLOBAL (una línea)`,
localizado por grep):

> **ACEPTA CON HUECOS DECLARADOS** — válido SOLO si el defecto del motivo 5 (G1-C1 suma costes de
> brokers y tipos de cuenta distintos) llega DECLARADO al CEO en la ficha de la puerta G1; si esa
> ficha lo omite, este veredicto decae y rige el RECHAZA de la primera pasada.

El motivo 5, con sus palabras (mismo fichero, sección `### Motivo 5 — Coste de entrar y coste de
mantener vienen de brokers y tipos de cuenta distintos en 7 de 8 instrumentos, y G1-C1 los suma`):

> **7 de 8, confirmado.** Y G1-C1 los suma [...]

> **Agravante encontrado en esta pasada (número ejecutado, no argumento):** la «forma operativa» de
> G1-C1 [...] está calculada SOLO con el coste de entrar/salir. [...] Es decir, el texto aprobado
> mete el swap dentro del 5% pero sus topes operativos gastan el 5% entero en entrar/salir.

> **Escalado que se pide (decisión del CEO, no de esta revisión):** la ficha de la puerta G1 debe
> declarar que (a) el número de G1-C1 es un constructo de brokers y cuentas distintos en 7 de 8
> instrumentos, no un coste contratable en ningún broker real, provisional hasta 04.01.02; y (b)
> los topes 29–105 / 62–217 / 126–426 no reservan presupuesto para el swap que el propio criterio
> dice incluir.

El detalle instrumento a instrumento está en la tabla de ese mismo motivo 5: las 5 divisas y el oro
toman el coste de entrar de IC Markets/Pepperstone (Raw/ECN) y el de mantener de OANDA TMS/XTB;
ETHUSD mezcla Pepperstone (entrar) con OANDA (mantener); **solo BTCUSD comparte broker y documento**
(Pepperstone, PDF feb-2025). Esta declaración va también, en lenguaje del CEO, como AVISO 1 de la
ficha D-19 (sección 3). Con esto la condición del ACEPTA queda cumplida.

---

## 1. Recomendación: cesta de 3 mercados y una vela

**Cesta recomendada: XAUUSD (oro al contado) + USDJPY + GBPUSD. Vela: 4h (una sola).**

**Primero, el límite que manda: la ficha pide «3-5 mercados poco correlacionados», y los datos solo
permiten 3.** Medido por ejecución (`cestas_g1.py` sobre `04-resultados/correlaciones_8x8.json`,
umbral 0,7 de G1-C5 en las tres ventanas, vela 4h):

- **Ninguna cesta de 4 o 5 instrumentos no-cripto es admisible a 4h.** Los 6 pares del bloque dólar
  (EURUSD, GBPUSD, AUDUSD, USDCHF entre sí) superan |0,7| en al menos una ventana — todos fallan en
  la de 3 meses: EURUSD/GBPUSD 0,87 · EURUSD/USDCHF 0,85 · GBPUSD/USDCHF 0,82 · GBPUSD/AUDUSD 0,80
  · EURUSD/AUDUSD 0,79 · AUDUSD/USDCHF 0,76. Confirma el aviso ya escrito en
  `correlaciones_8x8.md`, sección `## Pares que superan |0,7| en alguna de las tres ventanas`:
  cinco pares de forex no son cinco apuestas.
- **Existen exactamente 4 cestas de 3 admisibles a 4h**, todas de la forma XAUUSD + USDJPY + uno
  del bloque dólar: con GBPUSD (máx |corr| de la cesta **0,548**), con AUDUSD (0,583), con EURUSD
  (0,615), con USDCHF (0,651).
- **Cripto no amplía la cesta por el criterio aprobado:** G1-C5 (WBS, sección `## Puertas`, viñeta
  **G1-C5**) dice literalmente «Cripto queda FUERA de la cesta por defecto: solo tiene 1 de las 3
  ventanas, es inverificable (regla 26 de CLAUDE.md, los guardias bloquean por defecto)». Medido:
  BTCUSD/ETHUSD solo tienen dato real en 4h/3 meses; las ventanas de 1 y 2 años son hueco.

De las 4 cestas admisibles se recomienda **la de GBPUSD** porque domina a las otras tres en los dos
ejes que G1 mide: es la de **menor correlación máxima** (0,548) y su tercer miembro es el **más
barato del bloque dólar a 4h** (G1-C2 sobre p10: GBPUSD 3,22% < USDJPY… ver tabla; G1-C1 central:
GBPUSD 2,05% frente a EURUSD 2,45%, USDCHF 2,70%, AUDUSD 3,20%), con el coste de mantener más bajo
y simétrico del bloque (OANDA: largo −0,88%, corto −1,05% anual).

### 1.1 La cesta recomendada, criterio por criterio (vela 4h)

Fuentes: `coste_relativo.md` (secciones de tablas mediana y p10), `arrastre_coste.md` (secciones
`## 3. Calculo 1` y `## 4. Calculo 2`), `coste_swap.md` (tabla 8×3), `correlaciones_8x8.json`
(medido con `cestas_g1.py`), `veredicto_fase_02.md` (motivo 3, deriva del oro) y el texto aprobado
de D-11.

| Criterio (umbral D-11) | XAUUSD 4h | USDJPY 4h | GBPUSD 4h |
|---|---|---|---|
| **G1-C1** coste total anual ≤5% | **PASA CON RESERVAS** — 0,94% central; bajo la cota de deriva del coste (×1,82 / ×2,34): 1,71% / 2,19%. Pero su tope publicado de 426 ops/año baja a 234/182 bajo deriva, y ningún tope reserva swap (motivo 5) | **PASA** — 1,93% central | **PASA** — 2,05% central |
| **G1-C2** coste/ATR p10 ≤10% | **PASA** — 2,32%; bajo deriva 4,22% / 5,43% (pasaría a ser el peor de los 6, pero pasa) | **PASA** — 3,84% | **PASA** — 3,22% |
| **G1-C3** mantener, dentro del 5% | **DEPENDE de las noches** — largo −6,64% / −8,16% anual (OANDA/XTB); una noche por operación ≈ +2,36% anual (dato de D-11). Corto: +0,64% / −0,76% | **PASA en largo** (crédito +1,61% / +0,68%); corto cuesta −3,52% / −4,73% | **PASA** — largo −0,88% / −1,48%; corto −1,05% / −1,54%, el más bajo del bloque |
| **G1-C4** ≥1.000 velas/año | **PASA** — 1.598 | **PASA** — 1.609 | **PASA** — 1.611 |
| **G1-C5** \|corr\| ≤0,7 en 3 ventanas | **PASA en esta cesta** — máx del trío 0,548 (GBPUSD/USDJPY); XAUUSD/GBPUSD 0,547; XAUUSD/USDJPY 0,307 | **PASA** | **PASA** |
| **G1-C6** operable con 1.000-2.000 € | **DEPENDE del broker** — necesita 1.962 € (cabe bajo el techo de 2.000) o lote ≤0,1 oz; es requisito para 04.01.01, no eliminación | **PASA** — sin caso límite señalado en D-11 | **PASA** — sin caso límite señalado en D-11 |
| **G1-C7** hueco del lunes ≤0,5 | **NO CUMPLE** | **NO CUMPLE** | **NO CUMPLE** |

**G1-C7 no lo cumple ningún instrumento de la cesta (ni de los 8 candidatos).** La consecuencia
obligatoria del criterio aprobado va en la sección 2 y en la ficha del CEO.

### 1.2 Los cinco que quedan fuera, y por qué

| Instrumento | Veredicto | Motivo, criterio por criterio |
|---|---|---|
| EURUSD | **FUERA de la cesta recomendada; admisible solo sustituyendo a GBPUSD** | G1-C5: 0,87/0,85/0,79 contra GBPUSD/USDCHF/AUDUSD a 4h. Individualmente pasa G1-C1 (2,45%) y G1-C2 (4,32%), pero es más caro que GBPUSD y su swap largo (−2,41% anual) es el peor del bloque: D-11 ya declara que dos noches lo llevan a 7,01% > 5% |
| AUDUSD | **FUERA; admisible solo sustituyendo a GBPUSD** | G1-C5: 0,80/0,79/0,76 contra GBPUSD/EURUSD/USDCHF a 4h. Es el más caro de los 6 a 4h (G1-C2 p10 5,24%; G1-C1 3,20%) y a 1h falla G1-C2 (11,22% > 10%) |
| USDCHF | **FUERA; admisible solo sustituyendo a GBPUSD** | G1-C5: 0,85/0,82/0,76 contra EURUSD/GBPUSD/AUDUSD a 4h. Pasa G1-C1 (2,70%) y G1-C2 (4,37%); su swap largo es crédito (+2,60%). Cae por correlación de cesta (0,651 con USDJPY, la mayor de las 4 cestas admisibles) |
| BTCUSD | **FUERA por defecto (criterio aprobado)** | G1-C5 inverificable (1 de 3 ventanas; regla 26 de CLAUDE.md). G1-C1 y G1-C4: HUECO (sin velas/año — `arrastre_coste.md`, sección `## 3. Calculo 1`). G1-C2 a 4h pasa con ambas cifras (3,83% / 6,99% p10) — es el único filtro de coste que lo mide. G1-C3: mantener cuesta −33,64% anual (OANDA) / −22,5% (Pepperstone largo, feb-2025). ATR `reproducible: false`. Solo entra por decisión expresa del CEO contra el criterio |
| ETHUSD | **FUERA — el único que falla un filtro eliminatorio** | **NO PASA G1-C2 a 4h**: 15,13% / 35,37% sobre p10 con las dos cifras de coste (umbral ≤10%). Además: todo lo de BTCUSD, y su swap tiene una sola fuente fiable (por debajo del mínimo de dos, hueco declarado en `coste_swap.md`) |

### 1.3 Qué cumple, qué no, y qué depende de dónde se ponga el corte

- **Cumplen los siete criterios menos G1-C7** (que no cumple nadie): XAUUSD, USDJPY y GBPUSD a 4h
  — XAUUSD con dos condiciones declaradas (broker de G1-C6; deriva y L-007 del coste, sección 2).
- **No cumplen y no hay corte que los salve:** ETHUSD (G1-C2 a 4h, con las dos cifras de coste);
  toda cesta de 4+ instrumentos no-cripto a 4h (G1-C5, medido); 15m como vela (en p10 nadie queda
  ≤10%: el mejor es XAUUSD con 10,88%, que además sube a 19,80–25,46% bajo la cota de deriva).
- **Dependen de dónde se ponga el corte:**
  - *El tercer miembro de la cesta*: las 4 cestas admisibles solo difieren en cuál de los cuatro
    del bloque dólar entra. GBPUSD gana por coste y correlación; EURUSD/AUDUSD/USDCHF son cortes
    alternativos legales (opción B de la ficha para el más plausible).
  - *XAUUSD a 1h*: 4,71% base sobre p10, pero 8,56% / **11,01%** bajo la cota de deriva del coste
    — con la cota alta deja de cumplir G1-C2. Por eso 1h solo se ofrece condicionada (opción C).
  - *USDCHF a 1h*: 9,99% sobre p10 — pasa el umbral de 10% por 0,01 puntos. Filo de navaja, no base
    para decidir.
  - *La cesta de 4 a 1h*: existe UNA (USDJPY+AUDUSD+USDCHF+XAUUSD, medido) pero su peor par queda a
    0,698 de 0,70 — margen de 0,002 — y AUDUSD falla G1-C2 a 1h (11,22%). No se ofrece como opción:
    dos filos de navaja y un criterio incumplido no son una cesta.
  - *Nota:* bajo el umbral aprobado en D-11, G1-C2 es **≤10% sobre p10**; la banda «10-15%» que
    aparece en entregables anteriores es numeración/umbral pre-D-11 y no se usa aquí (motivo 2 del
    veredicto de fase, abierto).

### 1.4 La vela: por qué 4h, y en qué condiciones 1h

- **4h** es la única vela donde el texto aprobado de G1-C1 declara robustez: «con retornos objetivo
  entre 10% y 30%, la vela de 4h pasa 6 de 6 instrumentos en todos los casos; para que 1h pasara
  entera habria que declarar un retorno del 75,5% anual» (WBS, sección `## Puertas`, viñeta
  **G1-C1**). A 4h la cesta pasa G1-C2 con margen incluso en la vela tranquila y G1-C4 con
  1.598–1.611 velas/año.
- **1h no está prohibida** (G1-C1 «NO prohibe ninguna vela: impone un tope»), pero queda
  condicionada: tope de 62–217 operaciones/año (calculado además sin reservar swap — motivo 5), y
  con el arrastre del escenario central (actividad 5%) en 6,81–25,17% anual, muy por encima del 5%:
  solo cabría una estrategia de baja actividad. Y XAUUSD a 1h puede dejar de cumplir G1-C2 bajo la
  cota de deriva. Se ofrece únicamente como segunda vela, con estas condiciones delante (opción C).
- **15m queda descartada**: sobre la vela tranquila (p10) ningún instrumento queda ≤10% y el
  arrastre central anual es 56–212% del capital (`arrastre_coste.md`, sección `## 4. Calculo 2`).
- **Consecuencia de elegir 4h, ya identificada y no vetada:** la muestra se adelgaza y obliga a
  ampliar el histórico antes de partir los cajones (04.01.03). La salida está confirmada por
  02.02.04: Dukascopy publica desde 2003, gratis (`veredicto_criterios_g1.md`, sección `## Ataques
  que NO han tumbado`, frente 2).

---

## 2. Huecos y límites declarados, sin suavizar

1. **El defecto del motivo 5** — declarado con sus palabras en la sección 0 y como AVISO 1 de la
   ficha. El coste que alimenta G1-C1 mezcla brokers y tipos de cuenta en 7 de los 8 instrumentos;
   no es contratable en ningún broker real; los topes operativos 29–105 / 62–217 / 126–426 gastan
   el 5% entero en entrar/salir sin reservar el swap que el criterio dice incluir. Re-verificación
   obligatoria en 04.01.02.
2. **G1-C7: NINGÚN instrumento lo cumple.** Texto aprobado (WBS, sección `## Puertas`, viñeta
   **G1-C7**): «el hueco supera el stop ENTERO entre 11 y 17 veces en 696 dias (6-9 veces al año)
   en los 6 instrumentos no-cripto; percentil 90 entre 1,10x y 1,50x el stop; maximo 4,52x en
   EURUSD. Consecuencia obligatoria: la estrategia cierra posiciones antes del viernes, o G2
   declara explicitamente que la perdida real puede alcanzar 4,5 veces el riesgo nominal.» Esa
   consecuencia viaja con CUALQUIER cesta elegida y queda como requisito de diseño para G2.
3. **Las 6 celdas de cripto heredan un ATR marcado `reproducible: false`** en
   `04-resultados/atr_15m_1h_4h.json` (ventana deslizante de Kraken, sin arreglo contra el endpoint
   público). Y no es solo reproducibilidad: son **otro tipo de estimador** — 7,4 / 30 / 120 días de
   un único régimen frente a ~700 días multi-régimen en las 18 celdas de divisas y oro
   (`coste_relativo.md`, sección `## Herencia de la limitación del ATR de cripto`). Todo ratio de
   cripto citado aquí es una fotografía del 31/07/2026, no un número estable.
4. **BTCUSD y ETHUSD llevan DOS cifras de coste con fechas distintas, y no se promedian**
   (`coste_operar.md`, Tabla FINAL): BTCUSD **20,22 USD (feb-2025) / 36,90 USD (abr-2026)**; ETHUSD
   **3,01 USD (feb-2025) / 7,04 USD (abr-2026)**. Dos documentos oficiales de Pepperstone, dos
   fechas; promediar sería inventar. Esas mismas dos parejas son la fuente de los factores de
   deriva (+82,5% / +133,9% en 14 meses) usados como cota superior para el oro.
5. **Deriva del coste del oro (motivo 3 del veredicto de fase, cerrado por ejecución):** el coste
   de XAUUSD es de feb-2025. Bajo la cota (×1,82 / ×2,34), **a 4h el veredicto NO cambia** (G1-C2
   4,22% / 5,43% ≤10%); a **1h rompe el 10% en la cota alta (11,01%)** y a **15m deja de pasar
   (19,80–25,46%)**; el tope de operaciones «426» baja a 234/182.
6. **L-007 sin propagar (motivo 4, abierto):** la duda de instrumento del oro —la fórmula de
   Pepperstone para materias primas referencia «front-month future»— está declarada solo en
   `coste_swap.md`, sección `## Advertencias`, punto 2, y no en los dos documentos que usan la
   cifra. El coste del oro podría ser de un producto con componente de futuro mientras su ATR es de
   contado (Dukascopy). Se verifica con la ficha de contrato del broker en 04.01.02.
7. **Numeración pre-D-11 viva (motivo 2, abierto):** `coste_swap.md`, `coste_relativo.md`,
   `correlaciones_8x8.md` y `evidencia_umbrales_g1.md` citan «criterio 1/2/4» y la banda «10-15%».
   Este informe usa exclusivamente G1-C1..G1-C7 con los umbrales de D-11; la corrección documental
   sigue pendiente de reparto.
8. **Deslizamiento: hueco declarado de G1** (WBS, sección `## Puertas`, viñeta **HUECO DECLARADO EN
   G1**). No existe factor publicado; no hay número en ningún criterio; se mide con precios del
   broker real en 04.01.02 y **obliga a re-verificar G1 si algún resultado cambia**.
9. **Forex llega con ~5 semanas de retraso de publicación** (HistData: los 5 pares terminan el
   2026-06-26; oro 2026-07-29; cripto 2026-07-31). Las correlaciones usan el ancla común
   declarada en `correlaciones_8x8.md`, sección `## Límites de este resultado`.
10. **ETHUSD, swap con una sola fuente fiable** (OANDA; XTB lo ofrece como spot sin swap y
    Pepperstone no publica cifra): por debajo del mínimo de dos fuentes independientes, declarado
    en `coste_swap.md`, sección `## Huecos que quedan sin cubrir`.
11. **Todo el paquete de costes es PROVISIONAL hasta 04.01.02** (broker real). Los umbrales se
    re-verifican ahí; G1 se reabre si algún resultado cambia.

### Discrepancias encontradas al consolidar — se declaran, NO se arreglan (orden de la ficha)

- **D-a. Cifras de G1-C7:** el texto aprobado (WBS/D-11, arriba) dice p90 entre 1,10x y 1,50x,
  máximo 4,52x (EURUSD) y 11–17 veces en 696 días, atribuido al recálculo independiente del
  orquestador del 01/08/2026. La medición original del validador
  (`veredicto_criterios_g1.md`, ataque **A5**) da p90 entre 1,05x y 1,42x, máximos 4,84x (EURUSD) y
  **5,05x (XAUUSD)**, y 5,8–8,9 huecos >1×ATR al año, con consecuencia propuesta «hasta 5x». La
  ficha (AVISO 2) lleva el número más alto conocido y sin resolver — **5,05x, XAUUSD, marcado no
  probado** (regla 9 de CLAUDE.md: no se ha reejecutado aquí) — por orden de la revisión de
  02.03.02: XAUUSD es el ancla de la cesta recomendada y el CEO no lee esta sección. La
  discrepancia entre el texto aprobado y la medición original sigue declarada y sin resolver:
  la zanja quien la repare reejecutando el cálculo sobre `02-datos/bruto/`, no este informe.
- **D-b. Fecha de la puerta:** `coste_relativo.md` y `coste_swap.md` sitúan la decisión de G1 el
  «lunes 3 de agosto»; la orden vigente de esta tarea fija la decisión del CEO el lunes 10/08. No
  se corrige aquí.
- **D-c. 02.01.01 sigue «pendiente» en el WBS:** los 8 candidatos se usan de hecho en toda la fase;
  la ratificación formal del CEO llega con la propia respuesta a la ficha D-19 (elegir cesta
  ratifica candidatos). Declarado para que el cierre administrativo no se pierda.

---

## 3. Ficha para el CEO (formato de la sección «Qué llega al CEO y qué no» de CLAUDE.md)

**D-19 — Puerta G1: mercados y vela del bot**
AVISOS: (1) el coste de G1-C1 mezcla brokers y cuentas en 7 de 8 mercados: no existe en
ningún broker real, se remide en 04.01.02 y sus topes ignoran el coste nocturno. (2) ningún
mercado cumple G1-C7: o se cierra antes del viernes o G2 declara pérdidas de hasta 5,05x lo
arriesgado (máximo medido en el ORO, principal de la cesta; no probado; aprobado: 4,5x).
A) ORO + USDJPY + GBPUSD, vela 4h
B) ORO + USDJPY + EURUSD, vela 4h
C) A + vela 1h
D) A + BITCOIN (4 mercados)
RECOMENDADA: A — no cabe cesta de 4-5; de las 4 de 3, la de menor correlación (0,55) y coste.
SI ELIGES OTRA: B: más correlación (0,62) y coste. C: 1h deja pocas operaciones; el oro puede
fallar si su coste subió. D: contra el criterio aprobado (inverificable, no reproducible,
mantener 22-34%/año); exige decisión expresa.
BLOQUEA: 02.03.03 y todo lo que depende de G1.
RESPUESTA: una letra.

---

## 4. Nota de proceso

- La celda 02.03.02 del WBS no llevaba ficha escrita antes de trabajarse (regla 5 de CLAUDE.md);
  hace de ficha la orden del orquestador recibida por esta sesión. Se anota en vez de disimularse.
- Regla 16 de CLAUDE.md: este informe **no se autovalida**. Pendiente de revisión por un agente
  distinto antes de que 02.03.03 lo ponga delante del CEO. Quien revise puede reproducir la
  enumeración de cestas ejecutando `03-motor/scripts/cestas_g1.py` y cada cifra citada contra la
  sección nombrada de su artefacto de origen.
- Artefacto nuevo de esta tarea: `03-motor/scripts/cestas_g1.py` (lee el JSON cerrado; no
  recalcula correlaciones). Artefacto entregado: este informe.
- 03/08, tras RECHAZA de `critico-codigo` sobre esta entrega, reparado por el `validador`
  (regla 16 de CLAUDE.md: él revisa, no repara): (1) la ficha pasa de D-18 a **D-19** —
  D-18 fue firmada hoy por el CEO para otra decisión; D-19 verificada libre por grep en
  `DECISIONES.md`; (2) el AVISO 2 lleva ahora el número más alto conocido y sin resolver,
  **5,05x en XAUUSD** (medición del ataque **A5** de `veredicto_criterios_g1.md`), marcado
  **no probado** porque aquí no se reejecutó el cálculo (regla 9 de CLAUDE.md); (3) la ficha
  comprimida de 1.566 a **910 caracteres, 168 palabras, 15 líneas** (32 envuelta a 40
  columnas), medido por ejecución con el método declarado (`len`/`split`/`fold -s -w 40`),
  sin eliminar ninguna de las 4 opciones (L-023) ni ningún elemento obligatorio del formato.
- Restricciones respetadas de `veredicto_fase_02.md`, sección `## Lo que 02.03.02 NO PUEDE
  afirmar`: sin numeración vieja, sin oro a 15m/1h sin banda de deriva, sin presentar G1-C1 como
  coste real de un broker, sin promedios de cripto, sin deslizamiento como dato.
