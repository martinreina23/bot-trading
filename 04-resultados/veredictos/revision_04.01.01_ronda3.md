RECHAZA

# Revisión independiente — ronda 3 de `comparacion_brokers.md` (tarea 04.01.01)

**Quién:** `critico-codigo`. **Modelo real:** `claude-sonnet-5` (modelo primario; NO se usó respaldo,
regla 29 de CLAUDE.md).
**Fecha:** 09/08/2026.
**Punto de control inmutable (L-040 de LECCIONES.md):** medido contra el commit **`f481ce7`**
(`04.01.01: ronda 3 del comparativo y sus 11 fuentes nuevas, guardadas SIN REVISAR`). Verificado por
ejecución que el fichero vivo es idéntico a ese commit antes de empezar:
`diff <(git show f481ce7:01-investigacion/mercados/comparacion_brokers.md) 01-investigacion/mercados/comparacion_brokers.md`
→ **0 líneas de diferencia**. Cito líneas y contenido, nunca número de línea del fichero vivo como
identificador permanente (regla 13 de CLAUDE.md); las líneas dadas son las del propio `f481ce7`.
**No he escrito ni una celda de `comparacion_brokers.md`** (soy revisor independiente, regla 16 de
CLAUDE.md) ni de `04-resultados/tamano_minimo_operable.md`.

No reparo nada, no elijo ni recomiendo bróker: se describe, no se toca.

---

## P1 — Las 11 fuentes nuevas (`2026-08-06`) existen y las celdas dicen lo que dicen

**Existencia, una a una** (ejecutado desde `01-investigacion/mercados`):
`for f in $(grep -oE 'fuentes/[A-Za-z0-9_.-]+\.md' comparacion_brokers.md | sort -u); do test -f "$f" && echo EXISTE || echo NO-EXISTE; done | sort | uniq -c`
→ **37 EXISTE, 0 NO-EXISTE**. Huérfanos (`comm -13` citadas vs `ls fuentes/`) → **vacío**. Las 11 con
fecha `2026-08-06` están todas dentro de esas 37 y las 37 citas son únicas (`sort -u`).

**Las 11 fuentes nuevas, leídas una a una contra la celda que las cita** — coinciden:

| Fuente | Celda que la cita | Contenido de la fuente | ¿Coincide? |
|---|---|---|---|
| `CNMV_registro_XTB_Limited_2026-08-06.md` | c1/c10 XTB | "Número de registro oficial: 3325... Fecha de registro oficial: 05/12/2012. Estado: activo" | SÍ |
| `CNMV_registro_ICMarkets_EU_2026-08-06.md` | c1/c10 IC Markets | "Número de registro oficial: 4666... 12/12/2018. Estado: activo" | SÍ |
| `CNMV_registro_OANDA_TMS_2026-08-06.md` | c1/c10 OANDA | Entrada 1 (4592, activo desde 12/06/2018) + Entrada 2 (Sucursal 160, "QUEDA CERRADA LA SUCURSAL DE ESTA HOJA") | SÍ, con el matiz correcto: la celda separa pasaporte (activo) de sucursal (cerrada) |
| `CNMV_registro_Pepperstone_EU_2026-08-06.md` | c1/c10 Pepperstone | Registro 5001, activo desde 11/11/2020, **y declara la contradicción con la exclusión textual de la propia web** | SÍ — la celda documenta la contradicción, no la resuelve, igual que la fuente |
| `ICMarkets_EU_commodity_spec_2026-08-06.md` | c1 IC Markets (EU) Ltd | "Minimum Lot Size: 0.01 / Volume Step: 0.01" (=1 oz, sin fraccionado) | SÍ |
| `Pepperstone_EU_costs_charges_2026-08-06.md` | c1/c2 Pepperstone EU Ltd | Tabla "Major Metals" sin columna de lote mínimo; spread 5.00/13.81 | SÍ — celda declara hueco de lote, coherente con la ausencia de columna |
| `OANDA_TMS_full_specification_2026-08-06.md` | c1 OANDA TMS | 19 secciones, ninguna con columna de lote mínimo/volume step para GOLD.pro | SÍ — celda declara hueco |
| `OANDA_AsiaPacific_minimum_trade_size_2026-08-06.md` | c1/hallazgo OANDA | "Gold CFD \| 0.1" pertenece a OANDA Asia Pacific Pte Ltd (Singapur), entidad distinta | SÍ — la celda descarta explícitamente el traslado a la entidad admitente |
| `OANDA_EuropeMarkets_extinguida_2026-08-06.md` | c10/hallazgo OANDA | Sucursal de OANDA Europe Markets Limited también extinguida; entidad no investigada a fondo | SÍ |
| `PUPrime_FSA_client_agreement_cy_2026-08-06.md` | c1/c10 PU Prime | Nombra "Finzero Cap Ltd" (HE414308) en vez de "PU Prime (CY) Limited"; no menciona España ni lote | SÍ |
| `TMGM_legal_document_paises_restringidos_2026-08-06.md` | c1/c10 TMGM | "not intended for residents of the United States, Malaysia and Thailand" — España no está | SÍ |

**Verificación por ejecución de las 5 celdas que ronda 2 daba por "confirmadas" sin fuente** (ver P2):
`grep -rin "ctrader" fuentes/ICMarkets*.md` → 0; `grep -rn "4,85\|4\.85" fuentes/` → 0;
`grep -in "funding\|deposit\|crypto\|cripto" fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` → 0;
`grep -in "deposit\|depósit\|crypto\|cripto\|50 usd" fuentes/Infinox_condiciones_oro_2026-08-04.md` → 0.
**Los 4 greps confirman 0 coincidencias, igual que en ronda 2** — la corrección a "hueco" es correcta
y sigue siéndolo hoy.

**P1: sin infracciones.** Las 37 fuentes existen, no hay huérfanas, y cada celda que cita una de las
11 nuevas dice lo que la fuente dice, incluidas las contradicciones que se declaran sin resolver
(Pepperstone) y los descartes explícitos (OANDA Asia Pacific).

---

## P2 — Las reparaciones de ronda 3 contra el veredicto de ronda 2, una a una

| # | Reparación exigida (motivo de `revision_04.01.01.md`) | Veredicto | Prueba ejecutada |
|---|---|---|---|
| 1 | Cita literal falsa del «90%» en c12 IC Markets | **REPARADA** | `grep -n "90%" fuentes/ICMarkets_EU_faqs_2026-08-04.md` → 0. La celda ahora dice "hasta 20.000 € por cliente" (cita literal exacta de la fuente) y explica de dónde salió el 90% falso (Pepperstone EU, otro bróker). `grep -rn "90%" fuentes/` → única coincidencia en `Pepperstone_EU_fondos_espana_excluida_2026-08-04.md` |
| 2 | 5 celdas "confirmadas" sin fuente en disco (c6 ICM, c9 ICM, c11 ICM, c11 Infinox, ejemplo c3 PU Prime) | **REPARADA (las 5)** | Los 4 `grep` de P1 dan 0; las 5 celdas ahora dicen "HUECO (corregido en ronda 3, bloque 0)" con la explicación de qué fichero se atribuyó por error |
| 3 | Otras 6-7 celdas con dato y sin cita (c4 XTB/Pepperstone/OANDA, c7 OANDA, c8 IC Markets, c9 Pepperstone/OANDA) | **PARCIALMENTE NO REPARADA** — ver detalle abajo | 4 de 7 cerradas, **3 siguen sin fuente**: c7 OANDA, c8 IC Markets, c9 Pepperstone |
| 4 | Frase del resumen que afirmaba más que la celda c6 de Pepperstone (L-030) | **PARCIALMENTE NO REPARADA** | Ver detalle en P4 |
| 5 | Recuento de fuentes (26/3 en vez de 25/2) | **REPARADA/CONFIRMADA** | `ls fuentes/ \| wc -l` → 37; el documento declara 37 (26 previos + 11 nuevos) y lo verifiqué con `grep -oE ... \| sort -u \| wc -l` → 37, sin huérfanos. La cifra de "3 de IC Markets EU" antes de esta ronda + 1 nueva (`ICMarkets_EU_commodity_spec`) = 4: `ls fuentes/ \| grep -c "^ICMarkets_EU_"` → 4, coincide |

**Detalle del punto 3 — NO REPARADA en 3 de 7 celdas, verificado leyendo la fila completa de la tabla
(no de memoria):**

- **c7 OANDA** (Tabla B, criterio 7): la celda completa es *"OANDA TMS Brokers S.A., KNF (Polonia).
  Protección de saldo/fondos: hueco"* — **sin ninguna etiqueta `Fuente:`**. El dato de identidad
  (entidad + regulador) sigue sin cita, exactamente el defecto que señalaba la fila 5 de la tabla de
  `revision_04.01.01.md` (`grep -n "KNF" fuentes/OANDA_swap_gold_2026-08-04.md` → línea 3, localizable
  pero no citado en la celda).
- **c8 IC Markets** (Tabla B, criterio 8): la celda completa es *"**hueco parcial** — solo huso de
  servidor confirmado"* — **sin `Fuente:`**. Sigue siendo el mismo defecto de la fila 6 original
  (`grep -n "GMT + 2" fuentes/ICMarkets_commodity_spec_2026-08-04.md` → línea 35, localizable pero no
  citado).
- **c9 Pepperstone** (Tabla C, criterio 9): la celda completa es *"Pepperstone Limited (Reino Unido,
  FCA 684312). ¿API de esta entidad? **Hueco** — el único dato de API encontrado viene de otro
  dominio, sin ligar a esta entidad"* — **sin `Fuente:`** para la identidad FCA 684312 (fila 7
  original: `grep -n "FCA Registration Number 684312" fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md`
  → línea 4, localizable pero no citado).

**Esto contradice la propia declaración de alcance de ronda 3**, que dice explícitamente: *"cerrar
las 11 celdas con dato y sin fuente citada"* (línea 14 de `f481ce7`). Verificado: solo se cerraron 8
de las 11 originales del cubo (iii) de `revision_04.01.01.md`. Las 3 que quedan son datos de
identidad/entidad (KNF Polonia, huso de IC Markets, FCA 684312), no datos numéricos de precio — el
mismo tipo de defecto formal reiterado que ya dio un motivo de rechazo (motivo 3) en la ronda 2.

---

## P3 — Rejuzgar el criterio 1 con el listón corregido (punto central)

**Verificación independiente de las cifras del listón, ANTES de aceptar las de 04.01.04** (regla 9,
nivel 1 — no heredo un número sin recalcularlo): leí `04-resultados/atr_15m_1h_4h.json` y ejecuté mi
propio cálculo:

```
ATR14 mediana 4h XAUUSD = 22.152714285714215 USD/oz
EURUSD 4h precio medio  = 1.1290693760155996
capital USD para 1 oz al 1% = 22.152714 / 0.01 = 2215.2714 USD
capital EUR (vía tipo primario EURUSD) = 2215.2714 / 1.129069 = 1962.03 EUR
capital 1000 EUR -> suelo D-14 (70%) 700 EUR -> lote max admisible = 700*0.01/(22.152714/1.129069) = 0.3568 oz
capital 2000 EUR -> suelo D-14 (70%) 1400 EUR -> lote max admisible = 1400*0.01/(22.152714/1.129069) = 0.7135 oz
```

Coincide con las cifras que trae el encargo (1.962 €, ≈0,357 oz, ≈0,714 oz) y con el recálculo
independiente que ya hizo el `validador` en `revision_04.01.04.md` hasta el último decimal. **Nota
importante que no cambia el número pero sí su peso como antecedente:** `04.01.04` **no tiene ficha en
el WBS** — `grep -rn "04\.01\.04" 00-direccion/WBS.md` → 0 coincidencias — y el veredicto de esa
revisión es **RECHAZA** (por regla 2/5/12 de CLAUDE.md: tarea sin ficha, y por una declaración de
entradas falsa en el informe), no "aceptada". La aritmética (su V1) está confirmada por dos
recálculos independientes coincidentes —el del `validador` y el mío, ahora—, así que la uso como
prueba de nivel 1 de la regla 9; lo que no está firme es el registro de la tarea que la produjo, y
eso se lo debo señalar al orquestador, no callármelo.

### (a) Con el listón corregido, ¿cuántos de los 7 pasan el criterio 1?

**Solo hay DOS celdas con un número real de lote mínimo ancladas a una entidad que el documento cite
como admitente de España** (todas las demás son hueco para esa combinación entidad-admite + dato-de-lote):

- **XTB Limited** (Chipre): pedido mínimo 0,003 lote = **0,3 oz**; paso 0,001 lote = 0,1 oz exactas
  (fuente: `XTB_especificacion_contrato_oro_2026-08-04.md`, verificado por mí directamente: *"GOLD |
  ... | 0,003 | 0,001 | ..."*, línea 13; lectura en línea 20-21).
- **IC Markets (EU) Ltd** (Chipre): Minimum Lot Size 0,01 = **1 oz**, Volume Step 0,01 = 1 oz, sin
  fraccionado (fuente: `ICMarkets_EU_commodity_spec_2026-08-06.md`, verificado directamente: *"Minimum
  Lot Size: 0.01 / Volume Step: 0.01"*).

Contra el listón corregido (0,357 oz a 1.000 €; 0,714 oz a 2.000 €):

- **XTB Limited: 0,3 oz ≤ 0,357 oz Y ≤ 0,714 oz → PASA en todo el rango de capital 1.000-2.000 €**
  (con margen estrecho en el extremo de 1.000 €: 0,057 oz, ~16%, el mismo matiz "O1" que ya señaló
  `revision_04.01.04.md`).
- **IC Markets (EU) Ltd: 1 oz > 0,357 oz Y > 0,714 oz → NO PASA en ningún punto del rango.**

**NÚMERO: 1 de los 7 pasa el criterio 1 con el listón corregido — XTB, vía la entidad XTB Limited.**
Los otros 6 (Pepperstone, IC Markets —ambas entidades—, OANDA, TMGM, Infinox, PU Prime) no pasan: 5
por hueco de dato (Pepperstone, OANDA, TMGM sin entidad, Infinox, PU Prime sin entidad) y 1 por dato
confirmado que no llega (IC Markets EU Ltd, 1 oz).

### (b) ¿El dato de lote del que pasa pertenece a una entidad con cita de admisión a España?

**Sí, con cita en disco, y sin la contradicción que sí existe para Pepperstone.** Comprobé la frase
del documento *"XTB, vía Sucursal en España Y TAMBIÉN vía XTB Limited desde la ronda 3"* contra la
fuente, no la heredé: `fuentes/CNMV_registro_XTB_Limited_2026-08-06.md` dice literalmente *"Número de
registro oficial: 3325... Fecha de registro oficial: 05/12/2012. Estado: activo"* para **XTB Limited**
(la MISMA entidad de Chipre cuyo dato de lote se usa en (a)) — es una habilitación de libre prestación
de servicios activa en España. Busqué además si existe, como en el caso de Pepperstone, alguna
exclusión textual propia de XTB Limited que contradiga esto: `grep -iln "spain\|españa" fuentes/XTB_*.md`
→ solo aparece en `XTB_api_discontinuada` (sin relación con admisión) y en `XTB_sucursal_espana`
(que habla de la OTRA entidad). **No hay ninguna fuente en disco que excluya a España para XTB
Limited.** La afirmación del documento es correcta y no está fabricada.

**Advertencia que sí hay que hacer:** el dato de lote (0,3 oz) está anclado a **XTB Limited**; la
**Sucursal en España** —la otra vía de admisión— tiene el criterio 1 en **hueco** (el PDF de la
Sucursal no se pudo leer). Si el CEO eligiera operar por la Sucursal en vez de por XTB Limited, hoy
**no hay dato que confirme que esa vía concreta pasa el criterio 1** — el "1 de 7 pasa" depende de
qué entidad de XTB se use, y solo una de las dos tiene el número.

### (c) ¿Cambia el listón corregido algo del problema de entidad?

**En general, no — coincido con la lectura del orquestador de que son ejes independientes**: qué
entidad admite a España (criterio 10) se responde con registros CNMV y páginas del propio bróker,
nada de eso depende de qué umbral en onzas se use para el criterio 1. La metodología de investigación
de entidad no cambió ni tuvo que cambiar con el listón.

**Pero hay una consecuencia práctica que si no se dice, se pierde:** bajo el listón viejo (≤0,1 oz),
NINGÚN bróker pasaba el criterio 1, así que la ambigüedad de dos entidades de XTB (Sucursal vs XTB
Limited) era irrelevante para esta pregunta — daba igual cuál se eligiera, ninguna tenía el
fraccionado exigido. **Con el listón corregido, la ambigüedad de entidad de XTB deja de ser
irrelevante**: el "SÍ pasa" depende de que se opere con XTB Limited (que tiene el dato) y no con la
Sucursal (que no lo tiene, está en hueco). El listón corregido no cambia el MÉTODO de resolver
entidad, pero sí convierte, por primera vez, esa elección en una decisión con consecuencia sobre el
criterio 1. Esto no contradice al orquestador; lo completa.

---

## P4 — L-030, resumen contra celda, frase a frase

Contrasté las mismas dos secciones que el veredicto de ronda 2 usó como corpus ("Hallazgos
estructurales" y "Lo que SÍ/NO se puede comparar", incluida "Lo que NO se ha podido verificar").

**El documento declara, en «Registro de proceso» (línea 355 de `f481ce7`):** *"ninguna frase de las
secciones 'Hallazgos estructurales' ni 'Lo que SÍ/NO se puede comparar' afirma algo que su celda
correspondiente no diga"*. **Esta declaración es FALSA — sigue siendo falsa después de ronda 3,**
verificado leyendo la frase completa:

> Línea 205 (`f481ce7`): *"Detalle técnico de la API de Pepperstone e IC Markets más allá de 'existe
> cTrader Open API' — actualización ronda 3: para IC Markets, ni siquiera esa base ('existe cTrader
> Open API') tiene fuente en disco; se corrigió a hueco completo en el criterio 6 y 9 (bloque 0 de
> esta ronda)."*

Ronda 3 **corrigió la mitad de IC Markets** de esta frase (añadiendo la coletilla de que ni esa base
existe para IC Markets), **pero dejó intacta la mitad de Pepperstone**: la cláusula base
*"más allá de 'existe cTrader Open API'"* sigue presuponiendo, para Pepperstone, que existe cTrader
Open API como hecho asentado y que solo falta el "detalle técnico". Contra su propia celda c6 de
Pepperstone: *"**HUECO POR ENTIDAD (reparación):** cTrader Automate mencionado en
`pepperstone.com/en-eu/...` — dominio de la UE, SIN ningún aviso... Sin cita que lo ligue a
Pepperstone Limited (UK) → hueco"* — es decir, **para la entidad de referencia de esta tabla
(Pepperstone Limited, UK), la existencia de cTrader Open API NO está confirmada, está en hueco.** La
frase del resumen sigue afirmando más que su celda para Pepperstone, exactamente el patrón de L-030
que la misma ronda 3 dice haber corregido "tres veces" (y en efecto corrigió tres incumplimientos
distintos — API de IC Markets, fondo de garantía de IC Markets, cripto de IC Markets/Infinox — pero
esta cuarta frase, que mezclaba Pepperstone e IC Markets en el mismo enunciado, solo se corrigió a
medias).

**Frases infractoras: 1** (la de arriba). El resto del corpus contrastado —tabla de entidades de
cabecera, los cuatro "hallazgos estructurales", y el bloque completo de "Lo que SÍ se puede comparar
hoy sin huecos"— lo comprobé celda por celda y **no encontré ninguna otra frase que afirme más que su
celda**; en particular la frase del criterio 1 ("CERO de los 7 confirma el fraccionado de 0,1 oz...
XTB Limited (0,1 oz exactas de PASO, pero con pedido mínimo de 0,3 oz) e IC Markets (EU) Ltd (1 oz,
sin fraccionado)") es exacta y matizada, no exagera nada.

---

## P5 — Sesgo medido por efecto (L-032), con la cuenta pedida

El ejecutor declara en cabecera haber leído la frase de preferencia del CEO sobre el criterio 12. Medí
el efecto sobre las 84 celdas (12 criterios × 7 brokers), contando cuántas celdas por bróker tienen
dato real frente a cuántas son "hueco" o "no aplica" (script propio, no heredado, ejecutado sobre
`comparacion_brokers.md`):

| Bróker | Régimen | Celdas con dato | Huecos/No aplica | % hueco |
|---|---|---|---|---|
| XTB | mixto (Chipre CySEC = UE, Sucursal = UE) | 5/12 | 7/12 | 58,3% |
| OANDA | mixto (TMS Brokers Polonia = UE) | 5/12 | 7/12 | 58,3% |
| Pepperstone | mixto (EU Ltd Chipre = UE, con contradicción) | 4/12 | 8/12 | 66,7% |
| IC Markets | mixto (Raw Trading Seychelles = no-UE; EU Ltd Chipre = UE) | 4/12 | 8/12 | 66,7% |
| TMGM | no-UE (ASIC/VFSC/FSA/FSC) | 3/12 | 9/12 | 75,0% |
| Infinox | no-UE (Mauricio/Anguila/EAU/Chipre-solo-pagos) | 3/12 | 9/12 | 75,0% |
| PU Prime | no-UE (Australia/EAU/Mauricio/Seychelles/Sudáfrica/Chipre) | 1/12 | 11/12 | 91,7% |

**Los tres brokers de régimen mayoritariamente no-UE, los tres añadidos en la pasada 2 (TMGM, Infinox,
PU Prime), son los TRES peor cubiertos de los siete** (75%, 75% y 91,7% de huecos, frente a un rango
de 58,3%-66,7% en los cuatro de la pasada 1). **No hay ningún indicio de que la lectura de la
preferencia del CEO haya inclinado el barrido a favor de un régimen concreto**: si algo, el efecto es
el contrario — los brokers añadidos después de leer la frase están sistemáticamente peor
documentados, no mejor. Esto reproduce, con mi propio recuento y no heredado, la misma conclusión de
`revision_04.01.01.md` (que hacía el conteo solo sobre el criterio 12; aquí lo hice sobre las 84
celdas y el patrón se sostiene). **P5: sin sesgo medible por efecto.**

---

## P6 — Foto de tres columnas: lote mínimo · entidad que admite España · API (sin filtros nuevos)

Solo los criterios 1 y 10 son eliminatorios (WBS línea 129, `grep -on "eliminatori[a-z]*" 00-direccion/WBS.md`
→ `129:eliminatorio`, única aparición). No añado el 5 ni el 6 como filtro (L-039 de LECCIONES.md); el
6 (API) se reporta aquí solo como dato, no como criterio que descarte a nadie.

| Bróker | Lote mínimo (listón corregido) | Entidad que admite España | Acceso por API |
|---|---|---|---|
| **XTB** | **PASA** — vía XTB Limited (0,3 oz ≤ 0,357-0,714 oz). Vía Sucursal: **hueco** | **CONFIRMADA** — dos vías: Sucursal en España (`XTB_sucursal_espana_2026-08-04.md`) y XTB Limited (`CNMV_registro_XTB_Limited_2026-08-06.md`), sin contradicción entre ellas | **CONFIRMADO NO** — cita literal *"API access is no longer available. The service was discontinued on March 14, 2025."* (`XTB_api_discontinuada_2026-08-04.md`) |
| **Pepperstone** | **hueco** — el documento de costes de Pepperstone EU Ltd no trae columna de lote mínimo | **hueco / contradicción no resuelta** — CNMV activa desde 2020 (`CNMV_registro_Pepperstone_EU_2026-08-06.md`) vs. exclusión textual propia (*"not intended for residents of ... Spain"*, `Pepperstone_EU_fondos_espana_excluida_2026-08-04.md`) | **hueco** — cTrader Automate mencionado en dominio `en-eu`, sin cita que lo ligue a la entidad de referencia (UK) |
| **IC Markets** | **NO PASA** — IC Markets (EU) Ltd, 1 oz sin fraccionado (`ICMarkets_EU_commodity_spec_2026-08-06.md`), 1 oz > 0,357 y > 0,714 oz | **CONFIRMADA** — IC Markets (EU) Ltd (`ICMarkets_EU_entidad_espana_2026-08-04.md` + `CNMV_registro_ICMarkets_EU_2026-08-06.md`) | **hueco** — corregido en ronda 3 de "SÍ" (sin cita) a hueco; sin fuente en disco |
| **OANDA** | **hueco** — la especificación de 72 páginas de OANDA TMS Brokers S.A. no trae columna de lote mínimo; el "0,1" de Asia Pacific pertenece a otra entidad (descartado con cita) | **CONFIRMADA** — OANDA TMS Brokers S.A. (`CNMV_registro_OANDA_TMS_2026-08-06.md`, activa desde 2018) | **CONFIRMADO NO** — cita literal *"available to all divisions except OANDA Global Markets and OANDA TMS BROKERS S.A."* (`OANDA_api_v20_entidades_2026-08-04.md`) |
| **TMGM** | **hueco** — hay un dato de marca (1 oz) pero sin entidad a la que anclarlo | **hueco** — España no está en la lista de restringidos, pero ninguna de las 4 entidades se identifica como la que abriría la cuenta | **hueco** — no localizado |
| **Infinox** | **hueco** — sin dato de lote propio de Infinox Limited | **CONFIRMADA (indicio fuerte)** — Infinox Limited, Mauricio (`Infinox_restringidos_mifid_2026-08-04.md`), con aviso de exclusión de MiFID II | **hueco** — no localizado |
| **PU Prime** | **hueco** — sin dato de lote y sin entidad confirmada | **hueco** — indicio de marca, entidad concreta sin resolver (nombre societario en disputa) | **hueco** — no localizado |

**Comprobación pedida sobre la celda c6 de XTB:** confirmado, la celda refleja la cita literal de
`fuentes/XTB_api_discontinuada_2026-08-04.md` con precisión (*"API access is no longer available. The
service was discontinued on March 14, 2025."*), leído directamente en el fichero.

**¿Algún otro de los 7 tiene una negación explícita igual de sólida?** **Sí, uno: OANDA**, vía OANDA
TMS Brokers S.A., con cita literal propia igual de directa (*"available to all divisions except OANDA
Global Markets and OANDA TMS BROKERS S.A."*, `OANDA_api_v20_entidades_2026-08-04.md`, leído
directamente). **Ningún otro** (Pepperstone, IC Markets, TMGM, Infinox, PU Prime) tiene una negación
explícita: los cinco están en hueco por ausencia de dato, no por negación confirmada — coincide
exactamente con lo que el propio documento resume en su sección "Lo que SÍ se puede comparar".

No hay ranking ni recomendación en esta tabla: es una foto de tres columnas.

---

## VEREDICTO

**RECHAZA.**

Motivos, cada uno con nivel de prueba (regla 9 de CLAUDE.md), ninguno de nivel 3:

1. **Ronda 3 declara haber cerrado "las 11 celdas con dato y sin fuente citada" y no es cierto:**
   quedan 3 sin `Fuente:` (c7 OANDA, c8 IC Markets, c9 Pepperstone), leídas completas en P2. **Nivel
   1** — celdas transcritas íntegras, sin fuente en ninguna de las tres.
2. **La declaración de cierre de L-030 ("ninguna frase... afirma algo que su celda... no diga") es
   falsa:** la frase de la línea 205 sigue presuponiendo API confirmada para Pepperstone contra su
   propia celda c6, HUECO POR ENTIDAD. Ronda 3 corrigió la mitad de IC Markets de esa misma frase y
   dejó la mitad de Pepperstone sin tocar. **Nivel 1** — frase y celda transcritas en P4.

**Lo que SÍ se sostiene y no invalida investigar más sobre esta base (conviene que conste):** las 37
fuentes existen y ninguna celda de las 11 nuevas dice algo que su fuente no diga (P1); la cita falsa
del 90% está reparada correctamente (P2.1); las 5 celdas "confirmadas sin fuente" de ronda 2 están
reparadas correctamente, verificado con los mismos `grep` que las destaparon (P2.2); el recuento de
fuentes (37, 11 nuevas, 4 de IC Markets EU) es exacto (P2.5); no hay sesgo medible por régimen
regulatorio, y si algo el efecto es inverso al que se temía (P5); y **el hallazgo central es
correcto y reproducible por mí de forma independiente: con el listón corregido (1.962 € = capital de
1 oz; 0,357 oz a 1.000 €; 0,714 oz a 2.000 €), UN bróker de los 7 pasa el criterio 1 — XTB, vía la
entidad XTB Limited, sin contradicción de admisión de España en disco** (P3). El motivo del rechazo
no es el hallazgo del criterio 1: es que el documento afirma dos veces, explícitamente, que terminó
un trabajo (cerrar 11 celdas sin cita; que ningún resumen sobrepasa su celda) que no terminó del
todo, y esas dos afirmaciones de cierre son en sí mismas datos que van a decisión del CEO junto con
la tabla.

**Nota para el orquestador, no para reparar aquí:** la tarea `04.01.04` (origen de las cifras del
listón corregido) no tiene ficha en el WBS y su propia revisión (`revision_04.01.04.md`) es RECHAZA
por esa causa, no por la aritmética (que confirmé independientemente y coincide). Si el listón
corregido va a sostener una decisión de bróker con dinero real detrás (G3), la tarea que lo produjo
necesita su ficha antes, no después — regla 2 y regla 5 de CLAUDE.md.

**AVISO DE CONCURRENCIA respetado:** no he tocado `.githooks/pre-commit`, `03-motor/` ni
`00-direccion/DECISIONES.md`; no he hecho `git commit`; no he abierto `02-datos/reservado/`.
