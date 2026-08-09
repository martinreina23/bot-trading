# Comparación de brokers — XAUUSD al contado (tarea 04.01.01)

**Rol:** investigador (`claude-sonnet-5`, sin necesidad de respaldo). **Fecha del barrido pasada 1:**
04/08/2026. **Fecha del barrido pasada 2:** 04/08/2026. **Fecha de la ronda 3 (reparación, esta):**
06/08/2026.
**Alcance pasada 2:** ampliar de 4 a **7 brokers** (se añaden **TMGM, Infinox y PU Prime**) y de 8 a
**12 criterios** (se añaden (9) entidad exacta + acceso API de esa entidad, (10) admisión de un
residente en España y entidad concreta, (11) depósito/retirada en criptomoneda, (12) régimen
regulatorio con 4 datos en la misma celda), **y reparar 3 defectos de la pasada 1** señalados por el
revisor (L-030 de LECCIONES.md y desajuste de entidad por columna). **Capital de referencia:
1.000-2.000 €** (G1-C6, D-11).
**Alcance ronda 3 (reparación, ordenada por el orquestador, 06/08/2026):** (bloque 0, sin red) corregir
la celda del criterio 12 de IC Markets que atribuía un «90%» a una fuente que no lo dice; cerrar las
11 celdas con dato y sin fuente citada y las 5 cuya fuente citada no sostiene el dato, cada una con
la fuente que ya está en disco o hueco; corregir el recuento de fuentes (26 ficheros, 3 de IC
Markets EU, no 25 y 2). **(bloque 1, con red, prioridad absoluta)** anclar el criterio 1 (lote
mínimo/fraccionado 0,1 oz) a la entidad que de verdad admite a un residente en España, para los
siete brokers, porque es el único criterio que la ficha de 04.01.01 llama eliminatorio
(`grep -on "eliminatori[a-z]*" 00-direccion/WBS.md`, línea 129) y hoy ese dato estaba confirmado en
CERO de los siete para la entidad correcta. **Precisión recibida a media tarea:** donde un bróker
tiene más de una entidad con indicio de admitir a España, se documentan TODAS por separado, con su
nombre societario y su regulador, sin elegir entre ellas — la elección de régimen es del CEO y no
está decidida. **Pista adicional recibida y perseguida hasta su fuente exacta:**
`evidencia_umbrales_g1.md`, sección 6, citaba con reserva ("no leída completa") un mínimo de 0,1
unidades de oro atribuido a OANDA; se ha confirmado con fuente primaria que esa cifra pertenece a
**OANDA Asia Pacific Pte Ltd (Singapur)**, una entidad distinta de la que admite a España — no
sirve para cerrar el hueco del criterio 1 de OANDA, y se documenta por qué. **(bloque 2, si daba
tiempo)** ampliar el criterio 10 de OANDA, TMGM, PU Prime y Pepperstone. **Nota sobre la
reescritura:** este documento se reescribe completo porque la herramienta disponible es `Write`, no
`Edit`; no hay `Bash` ni `git` disponibles para comprobar con `git diff` que lo no ordenado sale
idéntico byte a byte contra el commit `079f1c2` — se ha reproducido cada sección no tocada
copiándola tal cual se leyó, pero esa garantía no se puede verificar por ejecución desde este rol, y
se declara así en vez de afirmarla (orden del orquestador, 06/08/2026).

**PROHIBIDO ELEGIR — no hay recomendación en este documento.** Cada celda lleva su fuente y su
fecha. Lo que no tiene fuente primaria propia del bróker se declara **hueco** y no se rellena
(regla 6 de CLAUDE.md). Todas las fuentes citadas están guardadas en
`01-investigacion/mercados/fuentes/` con la fecha de descarga en el nombre del fichero, para que
`critico-codigo` pueda comprobarlas sin salir a la red — ningún agente revisor tiene herramienta web.

**Nota de proceso sobre L-031 de LECCIONES.md:** la ficha de esta segunda pasada (WBS `04.01.01`)
contiene, tres líneas antes de prohibir al ejecutor conocer preferencias del CEO, la frase «El CEO ha
dicho que eso es lo que busca» referida al criterio 12. Como investigador que ejecuta la ficha entera
tal como está (orden explícita recibida), esa frase ha sido leída. **Se declara aquí, sin disimularlo,
y se ha aplicado el mismo rigor y la misma plantilla de 4 datos a los 7 brokers por igual**, sin
priorizar la búsqueda de ningún bróker sobre otro y sin conjeturar en este documento cuál sería el
régimen "buscado". La elección sigue siendo del CEO.

## Los 7 brokers: entidad usada como referencia para los criterios 1-9, y aviso de fragmentación

**Aviso general, que se repite y se profundiza más abajo:** varios de estos brokers no son una sola
entidad legal. Igual que ya ocurrió con OANDA en la pasada 1, esta pasada encuentra el MISMO problema
en **XTB** y en **IC Markets**: la entidad que admite a un residente en España (criterio 10) **no es
la misma** que la entidad usada como referencia para los criterios 1-9. Se declara con su propio
"hallazgo estructural" después de la tabla, para cada caso. **Actualización de la ronda 3:** para
XTB y OANDA esto ya no es "una sola entidad alternativa admite"; ver hallazgos estructurales
actualizados más abajo — hay más de una entidad con indicio de admitir, y esta ronda no elige entre
ellas.

| Bróker (marca) | Entidad de referencia, criterios 1-9 | Regulador | ¿Es la entidad que admite España? |
|---|---|---|---|
| XTB | XTB Limited | CySEC (Chipre), licencia 169/12 | **NO CONCLUYENTE (actualizado ronda 3)** — la Sucursal en España es DISTINTA (ver hallazgo estructural XTB), pero XTB Limited TAMBIÉN tiene registro CNMV de libre prestación de servicios activo desde 2012; hay dos vías posibles, no una sola "NO" |
| Pepperstone | Pepperstone Limited | FCA (Reino Unido), registro 684312 | **NO confirmado, y con contradicción (actualizado ronda 3)** — la entidad UE del grupo (Pepperstone EU Ltd, CySEC 388/20) EXCLUYE España por nombre en su propia web, pero SÍ tiene registro CNMV de libre prestación activo desde 2020; ver hallazgo |
| IC Markets | Raw Trading Ltd ("IC Markets Global") | FSA Seychelles, licencia SD018 | **NO** — ver hallazgo estructural IC Markets |
| OANDA | Fragmentado entre al menos 2 entidades — ver aviso ya declarado en pasada 1 | KNF (Polonia) para el dato de swap | **SÍ, resuelto en ronda 3** — vía OANDA TMS Brokers S.A., libre prestación de servicios, registro CNMV activo desde 2018; ver hallazgo estructural OANDA actualizado |
| TMGM | **Sin identificar** — las páginas de producto y condiciones son genéricas de marca, no citan qué entidad legal de las 4 declaradas describen | Depende de la entidad (ASIC Australia / VFSC Vanuatu / FSA Seychelles / FSC Mauricio) | Sin confirmar con cita primaria (hueco, criterio 10); España no está en la lista de restringidos de marca, pero eso no resuelve la entidad (ronda 3) |
| Infinox | **Sin identificar** para los criterios 1-8 — mismo problema que TMGM | Depende de la entidad | **SÍ, indicio fuerte** — Infinox Limited (FSC Mauricio, GB20025832); España no está en su lista de países restringidos, con aviso explícito de exclusión de MiFID II |
| PU Prime | **Sin identificar** para los criterios 1-8 — mismo problema | Depende de la entidad | Indicio de admisión general de marca (España no aparece en la lista de restringidos), **entidad concreta sin confirmar, y con una discrepancia nueva de nombre societario para la entidad chipriota (ronda 3)** |

**Consecuencia de esto para quien lea la tabla de abajo (no es una recomendación):** en XTB, IC
Markets, TMGM, Infinox y PU Prime, los datos de las columnas 1-8 **no se pueden dar por válidos
automáticamente** para la entidad con la que un residente en España abriría realmente la cuenta. Los
criterios 9-12 se han investigado tratando de anclar cada dato a la entidad correcta, y se declara
hueco donde no ha sido posible.

## Tabla A — Criterios 1 a 4 (lote, spread/comisión, swap, tipo de instrumento)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **1. Lote mínimo y fraccionado 0,1 oz — anclado a la entidad que admite España, ronda 3; ver metodología en el bloque 1 de la orden y precisión de multi-entidad recibida a media tarea** | **XTB Limited** (Chipre, CySEC 169/12): Pedido mínimo 0,003 lote (0,3 oz); paso mínimo de transacción 0,001 lote = **0,1 oz exactas** (cuenta retail). Cuenta profesional: mínimo 0,01 lote (1 oz). Esta entidad tiene registro CNMV de libre prestación de servicios activo desde 05/12/2012 (fuente: `fuentes/CNMV_registro_XTB_Limited_2026-08-06.md`), lo que la convierte en una SEGUNDA vía posible de admisión de España, además de la Sucursal — no se elige entre ambas. Fuente del dato de lote: `fuentes/XTB_especificacion_contrato_oro_2026-08-04.md`. **XTB S.A., Sucursal en España** (rama de XTB S.A., Polonia, KNF): **hueco** — no se ha podido extraer el lote mínimo del PDF de la Sucursal con las herramientas de esta sesión (regla 6 de CLAUDE.md; mismo hueco ya declarado en la pasada 2 para el fondo de garantía de esta entidad) | **Pepperstone EU Limited** (Chipre, CySEC 388/20 — registro CNMV de libre prestación activo desde 11/11/2020, fuente: `fuentes/CNMV_registro_Pepperstone_EU_2026-08-06.md`; pero su propia web excluye a España por nombre, ver criterio 10, contradicción declarada y no resuelta): **hueco** — su documento oficial de costes y cargos (`fuentes/Pepperstone_EU_costs_charges_2026-08-06.md`, fechado 05/09/2022) da el tamaño de contrato (100 oz/lote) pero no incluye columna de lote mínimo ni de paso para materias primas. No se ha localizado en el registro CNMV, en esta sesión, ninguna otra entidad de Pepperstone | **Raw Trading Ltd** ("IC Markets Global", Seychelles, FSA SD018 — la propia entidad declara no estar establecida en la UE, ver criterio 10): mínimo 1 oz (MT4 volumen 0,01); no se ha localizado paso de 0,1 oz. Fuente: `fuentes/ICMarkets_commodity_spec_2026-08-04.md`. **IC Markets (EU) Ltd** (Chipre, CySEC 362/18 — la entidad que SÍ admite a España, corroborado además por registro CNMV activo desde 12/12/2018, fuente: `fuentes/CNMV_registro_ICMarkets_EU_2026-08-06.md`): cita literal de su hoja de especificación de materias primas — **Minimum Lot Size 0,01 = 1 oz, Volume Step 0,01 = 1 oz**. **Tampoco esta entidad ofrece el fraccionado de 0,1 oz**: su paso mínimo es 1 oz completa, igual que Raw Trading Ltd, pero ahora anclado a la entidad correcta. Fuente: `fuentes/ICMarkets_EU_commodity_spec_2026-08-06.md` | **OANDA TMS Brokers S.A.** (Polonia, KNF — MISMA entidad de referencia de los criterios 1-9, confirmada admitiendo a España por libre prestación de servicios, registro CNMV activo desde 12/06/2018, fuente: `fuentes/CNMV_registro_OANDA_TMS_2026-08-06.md`): **hueco** — su especificación de instrumentos financieros de 72 páginas, vigente desde 26/06/2026 (fuente: `fuentes/OANDA_TMS_full_specification_2026-08-06.md`), da el tamaño de contrato (Price × 100 USD = 100 oz) y el tick de precio (0,01) para GOLD.pro, pero **no incluye ninguna columna de lote mínimo ni de paso de volumen** en ninguna de sus 19 secciones. **Pista perseguida hasta el final:** `evidencia_umbrales_g1.md` citaba, con reserva, un mínimo de "0,1 unidades" de oro para OANDA; confirmado con fuente primaria que esa cifra pertenece a **OANDA Asia Pacific Pte Ltd (Singapur)** — cita literal "Gold CFD | 0.1" en `help.oanda.com/sg/en/faqs/minimum-trade-size.htm`, plataforma "OANDA" (fxTrade) por unidades, no por lotes — una entidad y una plataforma **distintas** de OANDA TMS Brokers S.A. No hay base para trasladar esa cifra a la entidad polaca. Fuente: `fuentes/OANDA_AsiaPacific_minimum_trade_size_2026-08-06.md`. Sigue **hueco** para la entidad admitente. **OANDA Europe Markets Limited** (entidad distinta; su Sucursal en España también aparece extinguida en el registro mercantil, fuente: `fuentes/OANDA_EuropeMarkets_extinguida_2026-08-06.md`): **hueco** — no se ha verificado si tiene registro de libre prestación activo ni ningún dato de lote mínimo | Mínimo 0,01 lote = **1 oz** (misma unidad mínima que IC Markets, MAYOR que 0,1 oz); máximo 80 lotes. **No se ha localizado paso de 0,1 oz.** Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` (página genérica de marca, **entidad sin identificar** — España no figura en la lista de países restringidos de TMGM, fuente: `fuentes/TMGM_legal_document_paises_restringidos_2026-08-06.md`, pero eso no resuelve con cuál de sus 4 entidades se abriría la cuenta; no se ha localizado registro de ninguna entidad de TMGM/Trademax en la CNMV; el dato de 1 oz de esta celda no se puede anclar a la entidad admitente) | **Infinox Limited** (Mauricio, FSC GB20025832 — la entidad que admite a España según el criterio 10, con aviso de exclusión de MiFID II): **hueco** — no se ha localizado, con fuente primaria propia de esta entidad, un lote mínimo ni un paso de 0,1 oz para XAUUSD; la página `infinox.com/global/en/product-information/` (consultada 06/08/2026) confirma la marca pero no detalla el lote mínimo y remite a la plataforma, no verificable sin cuenta abierta | **Entidad sin confirmar** — esta ronda encontró, en el mismo documento contractual (`fuentes/PUPrime_FSA_client_agreement_cy_2026-08-06.md`), dos nombres para la entidad chipriota ("PU Prime (CY) Limited" en fuentes secundarias vs. "Finzero Cap Ltd", HE414308, cita literal del propio documento) — no resuelto si es la misma sociedad renombrada. Sigue sin identificarse con qué entidad concreta (de al menos 3 candidatas: PU Prime Limited Seychelles SD050, PU Prime Ltd Mauricio GB23202672, o la entidad chipriota) se abriría la cuenta de un residente en España, y por tanto **hueco** para el lote mínimo |
| **2. Spread y comisión reales del oro (USD/oz, ida y vuelta)** | Spread estándar 0,35, **sin comisión aparte** en cuenta Standard. Fuente: igual que fila 1 | Cuenta Razor: spread mínimo 0,05 / medio 0,19; **sin comisión aparte** ("reflected in the spread"). Fuente: `fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | XAUUSD: spread mínimo 0,00 / medio 0,63 pips, **más comisión "Raw Spread"** de 7 USD por lote, ida y vuelta. Fuente: `fuentes/ICMarkets_commodity_spec_2026-08-04.md` | **hueco** | "Spreads from 0.0 Pips", **sin cifra media ni comisión citada** en esta página. **Hueco parcial.** Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | Spread "18" (unidad no declarada verbatim; interpretado como centavos/puntos de precio, no confirmado como pip ni como USD/oz exacto), cuenta STP estándar, **"indicative in nature"** según la propia página; sin comisión ni lote citados. **Hueco parcial, con interpretación declarada, no verbatim.** Fuente: `fuentes/Infinox_condiciones_oro_2026-08-04.md` | **hueco** — las cifras de 3,0 pips (Standard) / 0,8 pips (Prime) que circulan en fuentes no admitidas (reseñas) NO se han podido confirmar con una cita literal de una página propia de PU Prime en esta sesión; no se usan |
| **3. Swap del oro, largo y corto por separado** | **HUECO POR ENTIDAD (reparación de la pasada 2):** existe cifra confirmada — Largo −8,16 %/Corto −0,76 % anual — pero **procede de la entidad de Emiratos** (documento `swaps_ae.pdf`), no de XTB Limited (Chipre, CySEC 169/12), la entidad de referencia del resto de columnas de XTB. La fuente afirma que "XTB opera un pricing/swap común documentado por instrumento, no por país" pero **no lo sostiene con cita literal** (regla de esta pasada: cita literal o hueco). Se declara hueco para esta tabla; cifra AE queda documentada aparte en `fuentes/XTB_swap_gold_2026-08-04.md` | **hueco numérico** — el documento confirma el MÉTODO (TomNext, igual que forex) pero no una cifra. Fuente: `fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | **hueco** — no se ha localizado tabla de swap | Largo **−6,65 % anual** (−18,22 USD/día/100.000 USD) · Corto **+0,65 % anual** (+1,78 USD/día). Fuente: `fuentes/OANDA_swap_gold_2026-08-04.md` — entidad OANDA TMS Brokers S.A. | **hueco numérico** — el documento declara el método ("SWAP_BY_POINTS", triple swap el miércoles) pero no una cifra de largo/corto. Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | **hueco** — no localizado | **hueco (corregido en ronda 3, bloque 0)** — el ejemplo de cálculo "-4,85 × 1 lote × 100 × 0,01 × 1 día = -4,85 USD" que la pasada 2 atribuía a `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` **no está contenido en ese fichero** (verificado por `grep` en esta ronda: cero coincidencias de "4,85" en todo `01-investigacion/mercados/fuentes/`). No se ha localizado, en esta sesión, ningún fichero en disco que sostenga esa cifra con cita literal. Se declara hueco, no se cita nada |
| **4. Instrumento: contado o con componente de futuro (L-007)** | La fila GOLD no lleva el asterisco que marca "referenciado a futuro" (nota 5). Indicio documental, no declaración explícita. Fuente (añadida en ronda 3, bloque 0: el dato ya estaba en el fichero, faltaba la cita): `fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` (nota 5 de ese documento) | El swap se calcula con la MISMA fórmula que forex (TomNext), separada expresamente de la fórmula de futuro que usa para "Commodities and Treasuries". Indicio documental más claro de los 7 de que se trata como spot. Fuente (añadida en ronda 3, bloque 0): `fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | **hueco** — no localizado. **Añadido a la lista consolidada de huecos del resumen (reparación de la pasada 2, punto 2 del encargo)** | Cita textual: **"OANDA prices are calculated from the theoretical spot prices derived from underlying futures"** — el propio bróker admite que deriva de futuros subyacentes. Fuente (añadida en ronda 3, bloque 0): `fuentes/OANDA_horario_operacion_metales_2026-08-04.md` | **hueco** — no localizado con fuente primaria en esta sesión | **hueco** — no localizado | **hueco** — no localizado |

## Tabla B — Criterios 5 a 8 (demo, API, regulador/protección general, horario)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **5. Cuenta demo, disponibilidad y caducidad** | **hueco** — no confirmado | **HUECO POR ENTIDAD (reparación):** dato existente — MT4/MT5 caduca a 60 días, cTrader no caduca si se accede cada 90 días — pero procede de `pepperstone.com/en/help-and-support/...` (dominio global "en"), **sin ninguna mención de que aplique a Pepperstone Limited (UK, FCA 684312)**, la entidad de referencia del resto de columnas. Sin cita literal que lo ligue a esa entidad → hueco. Contenido conservado en `fuentes/Pepperstone_demo_api_proteccion_2026-08-04.md` | **hueco** — accesos fallidos en esta sesión | Existe demo genérica (`developer.oanda.com`), pero **para OANDA TMS Brokers S.A. específicamente**, la caducidad se ha localizado ahora: **"The demo account expires 180 days after your last login"** (actualiza el hueco de la pasada 1). Fuente: `fuentes/OANDA_TMS_espana_demo_2026-08-04.md`. Aviso nuevo, ver criterio 10: **residentes en España no pueden abrir demo con esta entidad "por motivos regulatorios"** | **30 días** desde la creación (MT5); se pueden crear cuentas ilimitadas con fondos nuevos. **No se declara si existe conversión a "sin caducidad".** Fuente: `fuentes/TMGM_demo_2026-08-04.md` | **hueco** — no localizado | **hueco** — no localizado |
| **6. API o acceso programático** | **RESUELTO (mandato explícito de esta pasada): NO.** Fuente primaria propia de XTB, cita literal: *"API access is no longer available. The service was discontinued on March 14, 2025."* Confirmado en dos páginas oficiales del centro de ayuda (`/en/` y `/int/`). Cierra la pregunta abierta que dejó la pasada 1 con fuentes secundarias no admisibles. Fuente: `fuentes/XTB_api_discontinuada_2026-08-04.md` | **HUECO POR ENTIDAD (reparación):** cTrader Automate mencionado en `pepperstone.com/en-eu/...` — dominio de la UE, **SIN ningún aviso** de que sea otra jurisdicción (a diferencia de la celda de protección, que sí avisa). Sin cita que lo ligue a Pepperstone Limited (UK) → hueco. Es, según la propia ficha de esta tarea, "la celda peligrosa", precisamente porque nada advertía del cambio de dominio | **HUECO (corregido en ronda 3, bloque 0):** la pasada 2 afirmaba aquí "cTrader Open API, confirmado por páginas oficiales (blog corporativo y cAlgo), coherentes con la entidad Raw Trading Ltd", **sin ninguna cita de fuente**. Verificado por `grep` en esta ronda: ningún fichero de `01-investigacion/mercados/fuentes/` de IC Markets menciona "cTrader" (solo lo menciona el fichero de Pepperstone, de otro bróker). No hay fuente en disco que sostenga esta afirmación para IC Markets. Se declara hueco; no se ha vuelto a salir a la red para esta celda porque no estaba en el encargo de la ronda 3 | **NO — confirmado por fuente primaria:** excluida explícitamente de la API REST v20. Cita: *"available to all divisions except OANDA Global Markets and OANDA TMS BROKERS S.A."* Fuente: `fuentes/OANDA_api_v20_entidades_2026-08-04.md` | **hueco** — MT4/MT5 ofrecen Expert Advisors (trading algorítmico dentro de la plataforma), pero no se ha localizado una API REST/FIX propia de TMGM independiente de MetaTrader. Fuente: `fuentes/TMGM_demo_2026-08-04.md` | **hueco** — no localizado con fuente primaria propia | **hueco** — MT4/MT5 con Expert Advisors mencionados en marketing general; no se ha localizado una página propia de PU Prime con detalle técnico de API verificable por cita literal |
| **7. Regulador y protección de saldo (general)** | XTB Limited, CySEC (Chipre), licencia 169/12. ICF: tope **20.000 € por cliente** (documento de mayo 2019). Protección de saldo negativo: hueco. Fuente: `fuentes/XTB_regulador_icf_2026-08-04.md` | Pepperstone Limited, FCA (Reino Unido), registro 684312 — **identidad de entidad no se toca, es background**. **HUECO POR ENTIDAD para el CONTENIDO de protección** (segregación de fondos, NBP retail): procede de `pepperstone.com/en-au/...` (dominio australiano), con aviso YA declarado en la pasada 1 de que puede no aplicar palabra por palabra a la entidad UK. Bajo la regla de esta pasada (cita literal o hueco), sin esa cita el contenido de protección pasa a **hueco explícito**, no solo "con reserva". Fuente: `fuentes/Pepperstone_demo_api_proteccion_2026-08-04.md` | Raw Trading Ltd, FSA Seychelles, licencia SD018. Fondos segregados confirmados. **Protección de saldo negativo: hueco.** Fuente: `fuentes/ICMarkets_regulacion_2026-08-04.md` | OANDA TMS Brokers S.A., KNF (Polonia). Protección de saldo/fondos: hueco | Cuatro entidades (ver tabla de arriba). **Protección citada es de marca, no por entidad:** seguro de responsabilidad profesional hasta 10 millones AUD, miembro de "The Financial Commission" (organismo privado de resolución de disputas con fondo de compensación propio, no un fondo de garantía de inversores estatal). Fuente: `fuentes/TMGM_entidades_2026-08-04.md` | Cuatro entidades (Mauricio FSC, Anguila sin regular, EAU CMA, Chipre solo pagos). Seguro declarado hasta **500.000 USD por reclamante**, vigente 01/06/2026-31/05/2027. Fuente: `fuentes/Infinox_entidades_legal_2026-08-04.md` | Seis entidades (ver tabla de arriba). Fondo de compensación de marca (no estatal): hasta **20.000 € por caso**, vía membresía en "The Financial Commission". NBP declarada de marca, con reseteo manual o asistido, no automático. Fuente: `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` |
| **8. Horario de negociación del oro** | Sesión "12:00 am - 11:00 pm"; viernes corta a las 22:00 CET/CEST. Apertura domingo: hueco. Fuente: `fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` | L-J 01:01-23:59, V 01:01-23:55, huso GMT+3 (servidor). Cierre viernes ≈ 20:55 UTC, apertura domingo ≈ 22:01 UTC. Fuente: `fuentes/Pepperstone_horario_trading_hours_2026-08-04.md` | **hueco parcial** — solo huso de servidor confirmado | Apertura domingo 23:00 UTC, cierre viernes 22:00 UTC, pausa diaria 45 min. Fuente: `fuentes/OANDA_horario_operacion_metales_2026-08-04.md` | Apertura domingo 22:00 UTC, cierre viernes 21:59 UTC, pausa diaria ~1 minuto hacia las 22:00 UTC. **Entidad sin identificar** (página genérica de marca). Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | **hueco** — no localizado | **hueco** — no localizado |

## Tabla C — Criterios 9 y 10 (entidad exacta + API de esa entidad · admisión de residente en España)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **9. Entidad legal exacta de la fila (criterios 1-8), y si ESA entidad da acceso por API** | XTB Limited (Chipre, CySEC 169/12). ¿API de esta entidad? Confirmado grupo-wide que NO hay API (criterio 6); no hay evidencia de que sea distinto por entidad, dato de producto/plataforma. Fuente (añadida en ronda 3, bloque 0, mismo hecho ya citado en el criterio 6): `fuentes/XTB_api_discontinuada_2026-08-04.md` | Pepperstone Limited (Reino Unido, FCA 684312). ¿API de esta entidad? **Hueco** — el único dato de API encontrado viene de otro dominio, sin ligar a esta entidad | Raw Trading Ltd "IC Markets Global" (Seychelles, FSA SD018). ¿API de esta entidad? **HUECO (corregido en ronda 3, bloque 0):** la pasada 2 afirmaba aquí "SÍ, cTrader Open API confirmado desde fuentes corporativas coherentes con esta marca/entidad", **sin cita de fuente**. No hay fichero en disco que lo sostenga (ver misma corrección en criterio 6 de la Tabla B). Se declara hueco | OANDA TMS Brokers S.A. (Polonia, KNF). ¿API de esta entidad? **NO**, confirmado explícitamente. Fuente (añadida en ronda 3, bloque 0, mismo hecho ya citado en el criterio 6): `fuentes/OANDA_api_v20_entidades_2026-08-04.md` | **Hueco de asignación** — ninguna de las 4 entidades de TMGM (ASIC Australia AFSL 436416 · VFSC Vanuatu 40356 · FSA Seychelles SD224 · FSC Mauricio GB22201012) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/TMGM_entidades_2026-08-04.md` | **Hueco de asignación** — ninguna de las 4 entidades de Infinox (FSC Mauricio GB20025832 · Anguila sin regular · CMA EAU 20200000379 · Chipre HE440832 solo pagos) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/Infinox_entidades_legal_2026-08-04.md` | **Hueco de asignación** — ninguna de las 6 entidades de PU Prime (ASIC Australia 410681 · CMA EAU 20200000388 · FSC Mauricio GB23202672 · FSA Seychelles SD050 · FSCA Sudáfrica 52218 · Chipre HE414308) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/PUPrime_regulacion_2026-08-04.md` |
| **10. ¿Admite a un residente en España? ¿Qué entidad concreta?** | **HALLAZGO ESTRUCTURAL — SÍ, pero con OTRA entidad**: **XTB S.A., Sucursal en España** (rama de XTB S.A., Polonia — KNF —, supervisada también por la CNMV). **Es DISTINTA de XTB Limited** (Chipre, CySEC), la entidad de los criterios 1-9. Fuente: `fuentes/XTB_sucursal_espana_2026-08-04.md` (documento oficial "información básica", PDF de XTB, y redirección propia del sitio). **Actualización ronda 3:** XTB Limited TAMBIÉN tiene registro CNMV de libre prestación activo desde 2012 (ver criterio 1); hay dos entidades con indicio de admitir, no se elige entre ellas | **NO, con cita literal directa del propio bróker:** *"The information on this site is not intended for residents of Belgium, Spain or the United States"* — página de Pepperstone EU Ltd (Chipre, CySEC 388/20), la entidad que normalmente serviría a un cliente de la UE/EEE. **No se ha localizado ninguna entidad de Pepperstone (Reino Unido, Australia) que declare admitir expresamente a España**; el Reino Unido, tras el Brexit, típicamente no sirve a clientes UE bajo pasaporte —razón de ser de la propia entidad de Chipre—, pero esto es un indicio razonado, no una cita literal propia. Fuente: `fuentes/Pepperstone_EU_fondos_espana_excluida_2026-08-04.md`. **CONTRADICCIÓN NUEVA, declarada en ronda 3, no resuelta:** el registro oficial de la CNMV muestra a Pepperstone EU Limited activa en libre prestación de servicios desde el 11/11/2020 (fuente: `fuentes/CNMV_registro_Pepperstone_EU_2026-08-06.md`), lo que contradice en superficie la exclusión textual de la propia web. Ninguna de las dos fuentes primarias se descarta; se documenta el desacuerdo (regla 10 de CLAUDE.md) | **HALLAZGO ESTRUCTURAL — SÍ, pero con OTRA entidad**: **IC Markets (EU) Ltd** (Chipre, CySEC 362/18 — número confirmado por registro público del regulador, no por el bróker; corroborado además por el registro CNMV de libre prestación activo desde 12/12/2018, fuente: `fuentes/CNMV_registro_ICMarkets_EU_2026-08-06.md`). La propia página de regulación de IC Markets, al identificar visitantes de la UE/EEE, los redirige a esta entidad y declara literalmente que Raw Trading Ltd (la entidad de los criterios 1-9) *"is not established in the European Union or regulated by an EU National Competent Authority"*. Fuente: `fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` (redirección UE/EEE) y `fuentes/ICMarkets_EU_cysec_registro_2026-08-04.md` (número de licencia, registro público de CySEC) | **RESUELTO EN RONDA 3 — SÍ.** OANDA TMS Brokers S.A. (Polonia, KNF — la MISMA entidad de referencia de los criterios 1-9) está activa en el registro de la CNMV bajo "libre prestación de servicios" desde el 12/06/2018 (registro 4592), sin baja. Fuente: `fuentes/CNMV_registro_OANDA_TMS_2026-08-06.md`. **Dato adicional, no determinante para esta respuesta:** la Sucursal física que la misma entidad tuvo en España (registro CNMV 160) se cerró formalmente el 02/03/2026 según el Registro Mercantil de Madrid (BORME, boletín 46, vía agregador `iberinform.es`) — la habilitación de pasaporte es un registro independiente y sigue activa. **Existe además una entidad distinta, OANDA Europe Markets Limited**, cuya Sucursal en España también aparece extinguida (fuente: `fuentes/OANDA_EuropeMarkets_extinguida_2026-08-06.md`); no se ha verificado si esta segunda entidad tiene pasaporte activo — se declara hueco para ella, sin elegir | **HUECO** — no se ha localizado, con las herramientas de esta sesión, una declaración positiva ni negativa verificable sobre España con cita literal propia de TMGM. El PDF del Client Agreement no fue legible (no hay `poppler-utils` para renderizarlo, y el modelo de extracción de texto lo describió como binario no legible); las páginas de registro están renderizadas por JavaScript y no devolvieron contenido con WebFetch. **Dato añadido en ronda 3:** el documento de legal de TMGM confirma que España no está en su lista de países restringidos (solo EE. UU., Malasia y Tailandia), y no se ha encontrado registro de ninguna entidad de TMGM/Trademax en la CNMV — ninguno de los dos hechos resuelve CON QUÉ entidad se admitiría a España. Fuente: `fuentes/TMGM_legal_document_paises_restringidos_2026-08-06.md` | **SÍ**, vía **Infinox Limited** (Mauricio, FSC GB20025832). España NO figura en la lista literal de regiones restringidas de esta entidad (Bielorrusia, Bélgica, Canadá, Guam, India, Irán, Israel, Myanmar, Corea del Norte, Puerto Rico, Rusia, Sudáfrica, Sudán del Sur, Reino Unido, Islas Vírgenes de EE. UU., EE. UU.). **Con aviso explícito del propio bróker** de que operar con esta entidad implica quedar fuera de MiFID II. Fuente: `fuentes/Infinox_restringidos_mifid_2026-08-04.md` | **Indicio de admisión general, entidad concreta sin confirmar**: España no figura en la lista literal de países restringidos de marca ("Singapur, EE. UU., Australia, China, Filipinas, Corea del Norte, Irán" + lista FATF). **No hay cita que declare CON QUÉ entidad concreta** (de las 6) se abriría la cuenta de un residente en España; las candidatas más plausibles por ser "internacionales" son Seychelles (SD050) o Mauricio (GB23202672), pero es una conjetura razonada, no una cita — se declara hueco la asignación de entidad. Fuente: `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md`. **Ronda 3:** un documento contractual localizado (`fuentes/PUPrime_FSA_client_agreement_cy_2026-08-06.md`) nombra la entidad chipriota como "Finzero Cap Ltd" (HE414308), no como "PU Prime (CY) Limited"; no se resuelve si son la misma sociedad, y el documento no menciona a España |

## Tabla D — Criterios 11 y 12 (depósito/retirada en criptomoneda · régimen regulatorio, 4 datos)

Los criterios 11 y 12 se responden **para la entidad que admite a España** identificada en el
criterio 10 (columna anterior), no para la entidad de referencia de las columnas 1-9. Donde el
criterio 10 es hueco, el 11 y el 12 heredan ese hueco: no se puede describir el régimen de una
entidad que no se ha podido identificar.

| Criterio | XTB (Sucursal España) | Pepperstone (sin entidad que admita España) | IC Markets (EU) Ltd | OANDA (entidad sin confirmar) | TMGM (entidad sin confirmar) | Infinox Limited (Mauricio) | PU Prime (entidad sin confirmar) |
|---|---|---|---|---|---|---|---|
| **11. Depósito y retirada en criptomoneda, residente en España, ¿misma vía de vuelta?** | **hueco** — no investigado para esta entidad en esta sesión | **No aplica** — se hereda el hueco de admisión del criterio 10; no hay entidad confirmada con la que evaluarlo | **HUECO (corregido en ronda 3, bloque 0):** la pasada 2 afirmaba aquí "NO, confirmado por fuente primaria: la página oficial de financiación de IC Markets (EU) Ltd solo lista tarjetas... Fuente: página icmarkets.eu/en/trading-accounts/funding... (no guardada aparte, mismo hallazgo que `fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` documenta)". **Falso por verificación directa en esta ronda:** ese fichero es sobre la redirección UE/EEE de regulación, no menciona financiación ni criptomonedas en ningún punto. No existe ningún fichero en disco que sostenga el hallazgo de esta celda con cita real. Se declara hueco; no se ha vuelto a salir a la red para esta celda porque no estaba en el encargo de la ronda 3 (bloque 0 es sin red) | **hueco** — depende de resolver primero el criterio 10 | **hueco** — depende de resolver primero el criterio 10; una búsqueda no admitida (solo resumen de motor de búsqueda, sin fetch directo citable) sugiere USDT/USDC entre los métodos de TMGM, pero **no se usa como fuente** por no tener cita literal guardada de una página propia | **HUECO (corregido en ronda 3, bloque 0):** la pasada 2 afirmaba aquí "No confirmado — la página oficial NO lo menciona: la guía oficial de depósitos de Infinox... Fuente: `fuentes/Infinox_condiciones_oro_2026-08-04.md`". **Falso por verificación directa en esta ronda:** ese fichero trata de spread y apalancamiento del oro, no menciona depósitos, mínimos ni criptomonedas en ningún punto. No existe ningún fichero en disco que sostenga el hallazgo de esta celda con cita real. Se declara hueco | **hueco** — depende de resolver primero el criterio 10 |
| **12. Régimen regulatorio (i) fondo de garantía, importe · (ii) apalancamiento máximo · (iii) protección de saldo negativo · (iv) vía de reclamación real desde España** | **(i) hueco** — el ICF de 20.000 € verificado en la pasada 1 pertenece a XTB Limited (Chipre) y **no se hereda** a la Sucursal española (sería repetir el error de L-007 de LECCIONES.md, esta vez sobre la entidad); no se ha podido extraer del PDF de la Sucursal una cifra propia con las herramientas de esta sesión. **(ii) hueco** — no extraído. **(iii) hueco** — no extraído. **(iv) parcial:** contacto declarado `sales@xtb.es` / `support@xtb.es`, doble supervisión CNMV (España) + KNF (Polonia) confirmada, pero sin un proceso formal de reclamación citado literalmente. Fuente: `fuentes/XTB_sucursal_espana_2026-08-04.md` | **No aplica** — sin entidad admitida, los 4 datos no tienen a qué entidad anclarse | **(i) CORREGIDO EN RONDA 3, BLOQUE 0 — Fondo de Compensación de Inversores (ICF, Chipre): hasta 20.000 € por cliente si la empresa no devuelve los fondos del cliente** (cita literal exacta de la fuente: *"Offers compensation up to €20,000 per client if the firm fails to return client funds."*). **La pasada 2 afirmaba aquí "hasta el 90% del reclamado o 20.000 €, lo que sea menor"; esa cifra del 90% NO está en `fuentes/ICMarkets_EU_faqs_2026-08-04.md`** — verificado por `grep`, cero coincidencias de "90%" en ese fichero. El «90%» pertenece, con la misma redacción casi literal, a `fuentes/Pepperstone_EU_fondos_espana_excluida_2026-08-04.md` (*"either the 90% of the cumulative covered claims... or the amount of €20.000, whichever is lower"*), de OTRO bróker. Se corrige a lo que la fuente de IC Markets realmente sostiene. **(ii) Apalancamiento: 1:30 para clientes minoristas, hasta 1:500 para profesionales** (cita literal, sin cambios). **(iii) Protección de saldo negativo: SÍ para minoristas, explícitamente NO para profesionales** (cita literal, sin cambios). **(iv) Formulario de reclamación al Departamento de Cumplimiento**, `compliance@icmarkets.eu`, bajo supervisión de CySEC (cita literal, sin cambios). Fuente: `fuentes/ICMarkets_EU_faqs_2026-08-04.md` | Los 4 datos son **hueco** — dependen de resolver primero el criterio 10 (qué entidad admite a España) — **actualización ronda 3: el criterio 10 de OANDA ya está resuelto (SÍ, vía OANDA TMS Brokers S.A.), pero los 4 datos del régimen regulatorio para ESA entidad no se han investigado en esta ronda; siguen en hueco, ahora por falta de tiempo/alcance, no por falta de entidad** | Los 4 datos son **hueco** — dependen de resolver primero el criterio 9/10 (qué entidad de las 4 corresponde a los datos ya reunidos) | **(i) hueco** — sin cifra de fondo de garantía tipo UE citada para esta entidad; el propio bróker avisa expresamente, en la misma página que confirma la admisión, de que operar aquí implica quedar **fuera del régimen MiFID II** ("you will lose all protections afforded under EU regulation and law", cita literal). **(ii) hueco** — no se ha localizado cifra de apalancamiento propia de esta entidad para oro. **(iii) Mencionada de forma genérica, sin mecanismo ni cifra:** *"under FSC Regulation, INFINOX offers Best Execution protections and Balance Protection to protect accounts from negative balances"* (cita literal, sin más detalle). **(iv) hueco** — no se ha localizado un proceso de reclamación específico de esta entidad con cita literal. Fuente: `fuentes/Infinox_restringidos_mifid_2026-08-04.md` | Los 4 datos son **hueco** — dependen de resolver primero qué entidad concreta (de las 6, o de las al menos 3 candidatas tras el hallazgo de nombre de la ronda 3) admite a España |

## Hallazgos estructurales — fragmentación de entidad (tres casos, misma familia, y una actualización en ronda 3)

**No son una recomendación: son una advertencia de proceso**, igual que ya se declaró para OANDA en
la pasada 1. Los tres casos comparten el mismo patrón: la marca no es una sola entidad legal, y la
entidad usada para comparar precios y condiciones (criterios 1-9) **no siempre es** la que un
residente en España usaría de verdad (criterio 10). **La ronda 3 añade un matiz importante: en dos
de los tres casos (XTB y OANDA) no hay una sola entidad alternativa, sino DOS candidatas con indicio
de admitir — y esta tarea no elige entre ellas, por orden expresa recibida a media tarea.**

### OANDA (pasada 1, actualizado y en gran parte resuelto en ronda 3)

La única cifra de swap de oro verificada pertenece a OANDA TMS Brokers S.A. (Polonia, KNF), excluida
de la API REST v20. El documento de horario no declara su entidad. La pasada 2 confirmó la caducidad
de la demo de OANDA TMS Brokers S.A. (180 días) y que esta misma entidad bloquea la demo a
residentes en España por motivos regulatorios. **La ronda 3 confirma, con el registro oficial de la
CNMV, que esta MISMA entidad (OANDA TMS Brokers S.A.) SÍ tiene una habilitación activa de libre
prestación de servicios en España desde 2018** — no hace falta cambiar de entidad para los criterios
1-9, a diferencia de XTB e IC Markets. Dato adicional, no determinante: la Sucursal física que esta
entidad tuvo en España se cerró formalmente el 02/03/2026 según el Registro Mercantil, pero es un
registro distinto del de libre prestación, que sigue activo. **Existe además una tercera entidad,
OANDA Europe Markets Limited, cuya propia Sucursal en España también aparece extinguida en el
registro mercantil**; no se ha verificado en esta ronda si tiene pasaporte activo — queda declarada
como hueco, sin elegir entre ella y OANDA TMS Brokers S.A. **Sobre el lote mínimo (criterio 1):** se
persiguió una pista concreta que circulaba en `evidencia_umbrales_g1.md` (0,1 unidades de oro,
"fuente con reserva") hasta su origen exacto — pertenece a **OANDA Asia Pacific Pte Ltd (Singapur)**,
otra entidad más, con otra plataforma de producto (unidades, no lotes); no aplica a OANDA TMS
Brokers S.A., que sigue en hueco para este dato. Sigue sin resolverse si las filas 3, 6 y 8
de la Tabla A/B corresponden todas a la misma entidad (OANDA TMS Brokers S.A.) o si el documento de
horario es de otra división del grupo.

### XTB (pasada 2, actualizado en ronda 3)

**XTB Limited** (Chipre, CySEC 169/12) es la entidad de referencia de los criterios 1-9 de esta
tabla desde la pasada 1. **Un residente en España abriría cuenta con XTB S.A., Sucursal en España**
—rama de XTB S.A. (Polonia, KNF), con doble supervisión CNMV + KNF—, una entidad **distinta**. La
API confirmada como discontinuada (criterio 6) es un dato de marca/plataforma que razonablemente
aplica a ambas, pero el fondo de garantía de 20.000 € (ICF de Chipre), el spread, el swap y el lote
mínimo verificados en los criterios 1-3 y 7 **pertenecen a XTB Limited y no se han vuelto a verificar
para la Sucursal española** en esta tarea. **Actualización de la ronda 3, hallazgo nuevo:** el
registro de la CNMV muestra que **XTB Limited (la entidad de Chipre) TAMBIÉN tiene una habilitación
de libre prestación de servicios activa en España, desde el 05/12/2012** — más antigua que la propia
Sucursal. Esto significa que hay DOS vías con indicio de admitir a un residente español: la Sucursal
(constituida después, con doble supervisión) y XTB Limited (con pasaporte desde 2012, y con el dato
de lote mínimo ya confirmado). **Esta tarea no elige entre ellas**: la decisión de régimen —europeo
vía pasaporte o vía Sucursal española— es del CEO, y hoy no está tomada (preguntó por esto mismo el
06/08/2026, sin responder todavía).

### IC Markets (nuevo en la pasada 2, sin cambios de fondo en ronda 3, solo corroboración)

**Raw Trading Ltd** ("IC Markets Global", Seychelles, FSA SD018) es la entidad de referencia de los
criterios 1-9. La propia página de regulación de IC Markets declara, con cita literal, que esta
entidad **no está establecida en la Unión Europea ni regulada por una autoridad nacional competente
de la UE**, y redirige a los visitantes de la UE/EEE hacia **IC Markets (EU) Ltd** (Chipre, CySEC —
ver criterio 10 de la Tabla C para el número de licencia con cita literal a fuente primaria) — la
entidad que sí ha confirmado, con cita literal y los 4 datos completos, admitir a España con su
régimen regulatorio (criterio 12, ya corregido el dato del 90% en esta ronda). **La ronda 3 corrobora
esto con una segunda fuente primaria independiente**, el registro oficial de la CNMV (activo desde
2018) — a diferencia de XTB y OANDA, no se ha encontrado ninguna segunda entidad de IC Markets con
indicio de admitir a España; sigue siendo un caso de UNA sola alternativa, no de ambigüedad múltiple.
El lote mínimo de esta entidad SÍ se ha verificado ya en esta ronda (criterio 1): 0,01 = 1 oz, sin
fraccionado de 0,1 oz. El spread, la comisión y el swap de los criterios 2-3 **siguen sin
verificarse para IC Markets (EU) Ltd.**

### Pepperstone (pasada 2, con una contradicción nueva declarada en ronda 3)

A diferencia de OANDA, XTB e IC Markets —donde existe al menos una entidad alternativa que sí admite
a España—, en Pepperstone la única entidad de la Unión Europea localizada (**Pepperstone EU Ltd**,
Chipre, CySEC 388/20) **excluye a España por nombre, en su propia página**. No se ha encontrado, con
cita primaria propia del bróker, ninguna entidad de Pepperstone que declare expresamente admitir a
España. **Hallazgo nuevo de la ronda 3, que no resuelve lo anterior sino que lo complica:** el
registro oficial de la CNMV muestra que esta MISMA entidad, Pepperstone EU Limited, está activa en
libre prestación de servicios en España desde el 11/11/2020, sin baja. Hay, por tanto, una
contradicción entre dos fuentes primarias —el regulador español (que certifica el derecho de
pasaporte) y la propia declaración textual y vigente del bróker en su web (que excluye
comercialmente a España)— que **esta tarea no resuelve, solo documenta** (regla 10 de CLAUDE.md): no
hay experimento posible desde este rol que dirima cuál prevalece; sería necesario, por ejemplo, un
intento real de apertura de cuenta, fuera de alcance de esta tarea. Se deja constancia expresa:
**esto no es una recomendación de descarte, es lo que dicen las dos fuentes**; la decisión de qué
hacer con ese dato es del CEO.

## Lo que NO se ha podido verificar (declarado expresamente, regla 6 de CLAUDE.md)

**Heredado de la pasada 1, sigue sin resolver:**
- Lote mínimo y fraccionado de 0,1 oz de Pepperstone y de OANDA (TMS Brokers), **ahora anclado a la
  entidad que admite España en cada caso (ronda 3)**: sigue en hueco para ambas, pese a localizarse
  documentos oficiales específicos de esa entidad (Pepperstone EU Limited, OANDA TMS Brokers S.A.),
  porque ninguno de los dos documentos incluye una columna de lote mínimo o paso de volumen para
  materias primas. Para OANDA, además, se descartó explícitamente una cifra que circulaba dentro del
  propio proyecto (0,1 unidades) por pertenecer a otra entidad (OANDA Asia Pacific Pte Ltd,
  Singapur), no a la que admite España.
- Cifra numérica de swap de oro de Pepperstone e IC Markets (entidad de referencia).
- Caducidad de la cuenta demo de XTB e IC Markets (entidad de referencia).
- Detalle técnico de la API de Pepperstone e IC Markets más allá de "existe cTrader Open API" —
  **actualización ronda 3: para IC Markets, ni siquiera esa base ("existe cTrader Open API") tiene
  fuente en disco; se corrigió a hueco completo en el criterio 6 y 9 (bloque 0 de esta ronda)**.
- Protección de saldo negativo de XTB, IC Markets y OANDA (entidad de referencia).
- Horario exacto de apertura del domingo de XTB e IC Markets.
- A qué entidad legal de OANDA corresponde el documento de horario de mercado (criterio 8).
- **Instrumento contado o futuro (criterio 4) de IC Markets** — huella consolidada aquí por primera
  vez (reparación de la pasada 2, punto 2 del encargo: faltaba en el resumen aunque estaba bien
  declarada en la tabla desde la pasada 1).

**De la pasada 2, por la reparación de entidad-por-columna:**
- **Swap del oro de XTB** (criterio 3): pasa de "dato confirmado" a **hueco**, porque la cifra
  existente pertenece a la entidad de Emiratos y no hay cita que la ligue a XTB Limited (Chipre), la
  entidad de referencia de esta tabla.
- **Demo de Pepperstone** (criterio 5): pasa a hueco por la misma razón — sin cita que ligue el dato
  del dominio global a Pepperstone Limited (Reino Unido).
- **API de Pepperstone** (criterio 6): pasa a hueco por la misma razón — es, según la propia ficha de
  esta tarea, la celda más peligrosa, porque nada advertía del cambio de dominio.
- **Protección de fondos y saldo negativo de Pepperstone** (criterio 7): pasa de "con reserva" a
  hueco explícito, por la misma razón.

**Nuevo de esta pasada (2), por la ampliación a 7 brokers y 12 criterios:**
- Prácticamente todo el criterio 1-8 de **TMGM, Infinox y PU Prime está sin entidad asignada**: sus
  páginas de producto son genéricas de marca y no citan a qué de sus 3, 4 o 6 entidades legales
  corresponden los datos (ver "Hueco de asignación" en la Tabla C, criterio 9).
- Swap numérico de TMGM (solo método, no cifra) y de Infinox (no localizado).
- Spread y comisión exactos de PU Prime (los datos de 3,0/0,8 pips que circulan en reseñas no se han
  podido confirmar con cita literal de una página propia de PU Prime).
- API dedicada (más allá de Expert Advisors de MetaTrader) de TMGM, Infinox y PU Prime.
- Horario exacto de Infinox y PU Prime.
- Apalancamiento y fondo de garantía exactos de la entidad española de XTB (Sucursal en España): el
  PDF oficial no se pudo leer completo con las herramientas disponibles en esta sesión (sin
  `poppler-utils` para renderizar páginas; el modelo de extracción no transcribe el documento
  completo). Se declara hueco en vez de inferir por analogía con la entidad de Chipre.
- Admisión de España por parte de TMGM: ni confirmada ni descartada con cita primaria verificable
  (PDF del Client Agreement ilegible con las herramientas de esta sesión; páginas de registro
  renderizadas por JavaScript). **Ronda 3: sigue igual; el único dato nuevo (España no está en la
  lista de restringidos) no identifica la entidad.**

**Nuevo de la ronda 3 (bloque 0 — reparación de citas):**
- **Depósito/retirada en criptomoneda de IC Markets (EU) Ltd (criterio 11):** pasa de "NO, confirmado"
  a **hueco** — la fuente citada en la pasada 2 no contenía ese hallazgo; verificado por `grep`.
- **Depósito de Infinox Limited (criterio 11):** pasa de "no confirmado, con detalle" a **hueco puro**
  — mismo motivo: la fuente citada no contenía el hallazgo.
- **Ejemplo de swap de PU Prime (−4,85, criterio 3):** pasa de "dato parcial ilustrativo" a **hueco**
  — la fuente citada no contiene esa cifra.
- **API de IC Markets (criterios 6 y 9):** pasa de "SÍ, cTrader Open API" a **hueco** en ambos
  criterios — no existía ninguna cita de fuente, ni verdadera ni falsa; simplemente no la había.
- **Fondo de garantía de IC Markets (EU) Ltd (criterio 12(i)):** la cifra "90% del reclamado o
  20.000 €" no pertenece a esta entidad; se corrige a lo que su propia fuente sostiene (hasta
  20.000 € por cliente, sin porcentaje).
- Instrumento contado/futuro de XTB, Pepperstone y OANDA (criterio 4): tenían dato correcto pero sin
  citar el fichero exacto; corregido añadiendo la cita (el dato no cambia, solo se sostiene ahora con
  fuente declarada).

**Nuevo de la ronda 3 (bloque 1 — pista externa perseguida y descartada para la entidad correcta):**
- **Lote mínimo del oro de OANDA, vía la pista de `evidencia_umbrales_g1.md` (0,1 unidades):**
  confirmado con fuente primaria que esa cifra pertenece a OANDA Asia Pacific Pte Ltd (Singapur), no
  a OANDA TMS Brokers S.A. (la entidad que admite a España). Sigue hueco para la entidad correcta;
  el hueco ahora está documentado con más precisión que antes de la pista.

## Lo que SÍ se puede comparar hoy sin huecos, entre los 7 (derivado estrictamente de la tabla, L-030; corregido en ronda 3 donde el resumen decía más de lo que su celda dice)

- **4 de los 7** (XTB, Pepperstone —solo tamaño de contrato, el resto de la fila 1 es hueco—, IC
  Markets y TMGM) tienen el contrato de 100 oz por lote estándar confirmado por fuente primaria en
  algún punto de la fila 1 o 2. **Para Infinox, OANDA y PU Prime esta tabla no tiene, en esta pasada,
  una cita propia que confirme el tamaño de contrato**: queda hueco, no se hereda por analogía con
  los otros 4.
- **2 de los 7** (XTB —vía la entidad de Emiratos, no la de referencia de esta tabla, hueco para la
  entidad de Chipre— y OANDA —TMS Brokers—) tienen una cifra numérica de swap del oro con fuente
  primaria en algún punto de la investigación, frente a los otros 5 (Pepperstone, IC Markets, TMGM,
  Infinox, PU Prime) que quedan en hueco para una cifra numérica fiable de swap.
- **Acceso programático (criterio 6), contado con precisión sobre las 7 celdas de la Tabla B —
  CORREGIDO EN RONDA 3:** la pasada 2 decía aquí que "1 de los 7 (IC Markets, vía Raw Trading Ltd)
  tiene cTrader Open API confirmado por fuente primaria"; esa celda no tenía fuente y se ha corregido
  a hueco (ver bloque 0 de esta ronda). El recuento correcto es: **CERO de los 7 tienen acceso por
  API confirmado en positivo con fuente primaria propia.** **XTB y OANDA (TMS Brokers S.A.) tienen
  confirmado por fuente primaria que NO ofrecen API** — el dato más sólido de toda la tabla en este
  criterio, porque en los dos casos es una negación explícita del propio bróker, no una ausencia de
  dato. **Los otros 5 (Pepperstone, IC Markets, TMGM, Infinox, PU Prime) quedan en HUECO** para este
  criterio en su entidad de referencia.
- **Para el criterio 1 (lote mínimo/fraccionado 0,1 oz), anclado en ronda 3 a la entidad que admite a
  España: CERO de los 7 confirma el fraccionado de 0,1 oz para esa entidad.** Dos brokers sí tienen
  un dato numérico de lote mínimo confirmado para la entidad admitente, y en ambos casos el mínimo es
  MAYOR que 0,1 oz: **XTB Limited (0,1 oz exactas de PASO, pero con pedido mínimo de 0,3 oz)** e **IC
  Markets (EU) Ltd (1 oz, sin fraccionado)**. Los otros 5 (Pepperstone, OANDA, TMGM, Infinox, PU
  Prime) quedan en hueco para el lote mínimo de la entidad admitente, bien porque el documento
  oficial de esa entidad no incluye esa columna (Pepperstone EU Limited, OANDA TMS Brokers S.A. — en
  el caso de OANDA, se persiguió y descartó explícitamente una cifra de 0,1 unidades que pertenecía a
  otra entidad del grupo, Singapur, no a la admitente), bien porque la propia entidad admitente sigue
  sin identificarse (TMGM, PU Prime), bien porque no se ha localizado el dato con fuente primaria
  propia (Infinox).
- **De los brokers cuya entidad de admisión de España se ha podido confirmar con cita primaria
  (XTB, vía Sucursal en España Y TAMBIÉN vía XTB Limited desde la ronda 3; IC Markets, vía IC Markets
  (EU) Ltd; OANDA, vía OANDA TMS Brokers S.A. desde la ronda 3; e Infinox, vía Infinox Limited
  Mauricio), solo IC Markets (EU) Ltd tiene los 4 datos completos del régimen regulatorio (criterio
  12) con cita literal** (corregido en esta ronda: el fondo de garantía ya no dice "90%", dice lo que
  la fuente sostiene). Para XTB (Sucursal España) 3 de los 4 datos son hueco y el cuarto es parcial;
  para Infinox (Mauricio) el propio bróker avisa de que el cliente queda fuera de MiFID II, con solo
  1 de los 4 datos citado (protección de saldo, sin cifra) y los otros 3 en hueco; para OANDA (TMS
  Brokers S.A.) los 4 datos siguen en hueco por falta de investigación en esta ronda, no por falta de
  entidad.
- **Pepperstone es, de los 7, el único con una cita primaria propia que EXCLUYE por nombre a España**
  en la entidad de la Unión Europea que normalmente le correspondería — **y, desde la ronda 3, el
  único con una contradicción documentada entre esa exclusión y un registro activo del regulador
  español para la misma entidad**, sin que esta tarea resuelva cuál de las dos fuentes prevalece.

## Registro de proceso

- **Modelo usado:** `claude-sonnet-5` en las tres pasadas. No hizo falta el respaldo
  (`claude-haiku-4-5-20251001`): el modelo no rechazó ninguna petición en ninguna de las tres pasadas.
- **Herramientas usadas (pasadas 1 y 2):** `WebSearch` solo como orientación para localizar URL
  oficiales (NUNCA citada como fuente de un dato de la tabla); `WebFetch` como herramienta de cita,
  incluyendo el proxy `r.jina.ai` cuando `infinox.com` y `puprime.com` devolvían 403 directo (mismo
  dominio del bróker, solo cambia la ruta de acceso; el contenido citado sigue siendo la página
  oficial del bróker, con su URL original declarada en cada ficha de `fuentes/`). Dos PDF (TMGM Client
  Agreement, XTB información básica) no se pudieron transcribir por completo por falta de
  `poppler-utils` en este entorno; se declara hueco lo que no se pudo leer, no se completa por
  analogía.
- **Herramientas usadas (ronda 3, añadido):** además de `WebSearch` y `WebFetch`, se usó la
  herramienta `Read` para decodificar directamente los PDF binarios que `WebFetch` guardaba sin poder
  extraer texto (funcionó para las especificaciones de IC Markets EU, Pepperstone EU y OANDA TMS,
  donde `WebFetch` había fallado en la lectura); y se consultó **el registro público de la CNMV**
  (Comisión Nacional del Mercado de Valores, el regulador español) como fuente primaria de tipo
  distinto al bróker — un registro oficial, no una reseña ni un comparador — para XTB Limited,
  Pepperstone EU Limited, IC Markets (EU) Ltd y OANDA TMS Brokers S.A. (dos entradas: libre prestación
  y sucursal). Un hallazgo de cierre de sucursal (OANDA TMS Brokers S.A. y OANDA Europe Markets
  Limited) se corroboró vía un agregador comercial (`iberinform.es`) que reproduce el asiento oficial
  del BORME (Boletín Oficial del Registro Mercantil); se declara la naturaleza secundaria del
  agregador pero primaria del asiento que reproduce.
- **Recuento de fuentes, verificado por `Glob` sobre el disco, no estimado (regla 14 de CLAUDE.md,
  L-020 de LECCIONES.md):** `01-investigacion/mercados/fuentes/` contiene **37 ficheros** al cerrar
  esta ronda 3 (corrige el recuento de "25 ficheros, 2 de IC Markets EU" que la pasada 2 dejó mal
  escrito; el recuento correcto de la pasada 2, verificado ahora por `Glob`, era **26 ficheros, 3 de
  IC Markets EU** — `ICMarkets_EU_entidad_espana`, `ICMarkets_EU_faqs`, `ICMarkets_EU_cysec_registro`
  —, y esta ronda 3 añade **11 ficheros nuevos**: `ICMarkets_EU_commodity_spec`,
  `Pepperstone_EU_costs_charges`, `CNMV_registro_Pepperstone_EU`, `CNMV_registro_OANDA_TMS`,
  `OANDA_TMS_full_specification`, `CNMV_registro_XTB_Limited`, `CNMV_registro_ICMarkets_EU`,
  `TMGM_legal_document_paises_restringidos`, `OANDA_EuropeMarkets_extinguida`,
  `PUPrime_FSA_client_agreement_cy`, `OANDA_AsiaPacific_minimum_trade_size`, todos fechados
  2026-08-06).
- **Congelación respetada:** no se ejecutó ningún `git commit`, `checkout`, `stash`, `restore`,
  `reset` ni `amend`; no se instaló ningún paquete; no se tocó nada fuera de
  `01-investigacion/mercados/`.
- **No se abrió cuenta demo ni real de ningún bróker** (fuera de alcance de esta tarea).
- **No hay ninguna recomendación de bróker en este documento ni en las fuentes guardadas.** Los
  hallazgos de admisión (criterio 10) —en particular la exclusión expresa de España por Pepperstone
  EU Ltd (con su contradicción de registro CNMV, no resuelta), y el cambio/multiplicación de entidad
  de XTB, IC Markets y OANDA— se presentan como datos con cita, no como descartes: la decisión de qué
  hacer con ellos, incluida la elección de régimen europeo o extracomunitario, es del CEO.
- **Resumen derivado de la tabla, contrastado frase a frase antes de entregar (L-030 de
  LECCIONES.md):** ninguna frase de las secciones "Hallazgos estructurales" ni "Lo que SÍ/NO se puede
  comparar" afirma algo que su celda correspondiente no diga; donde una celda es hueco, la frase del
  resumen que la menciona también dice "hueco". **En esta ronda 3 se encontraron y corrigieron TRES
  incumplimientos de esta misma regla que la pasada 2 había dejado sin detectar**: la celda de API de
  IC Markets (criterios 6 y 9) y la frase del resumen que la contaba como el bróker con API
  confirmada; la celda del fondo de garantía de IC Markets (criterio 12) con una cifra que pertenecía
  a otro bróker; y las celdas de criptomonedas de IC Markets e Infinox (criterio 11) con una fuente
  citada que no contenía el hallazgo. Las tres correcciones están declaradas explícitamente arriba,
  con el método de verificación (`grep` sobre los ficheros de `fuentes/`) que las detectó.
- **Advertencia sobre la reescritura completa de este fichero (ronda 3):** se ha usado `Write`, no
  `Edit`, porque esa es la herramienta disponible para este rol. Se ha reproducido cada sección no
  tocada copiándola del contenido leído inmediatamente antes de escribir, pero **no hay manera de
  comprobar por ejecución, desde este rol, que el resultado es idéntico byte a byte** a las partes no
  tocadas del commit `079f1c2` — no hay `Bash` ni `git diff` disponibles aquí. Se declara la
  incertidumbre en vez de afirmar una garantía no verificable (orden explícita del orquestador,
  06/08/2026): el revisor (`critico-codigo`) deberá comprobarlo con `git diff` como parte de su
  revisión, no dar por hecho que coincide.
