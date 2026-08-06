# Comparación de brokers — XAUUSD al contado (tarea 04.01.01)

**Rol:** investigador (`claude-sonnet-5`, sin necesidad de respaldo). **Fecha del barrido pasada 1:**
04/08/2026. **Fecha del barrido pasada 2 (esta):** 04/08/2026.
**Alcance pasada 2:** ampliar de 4 a **7 brokers** (se añaden **TMGM, Infinox y PU Prime**) y de 8 a
**12 criterios** (se añaden (9) entidad exacta + acceso API de esa entidad, (10) admisión de un
residente en España y entidad concreta, (11) depósito/retirada en criptomoneda, (12) régimen
regulatorio con 4 datos en la misma celda), **y reparar 3 defectos de la pasada 1** señalados por el
revisor (L-030 de LECCIONES.md y desajuste de entidad por columna). **Capital de referencia:
1.000-2.000 €** (G1-C6, D-11).

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
"hallazgo estructural" después de la tabla, para cada caso.

| Bróker (marca) | Entidad de referencia, criterios 1-9 | Regulador | ¿Es la entidad que admite España? |
|---|---|---|---|
| XTB | XTB Limited | CySEC (Chipre), licencia 169/12 | **NO** — ver hallazgo estructural XTB |
| Pepperstone | Pepperstone Limited | FCA (Reino Unido), registro 684312 | **NO confirmado** — la entidad UE del grupo (Pepperstone EU Ltd, CySEC 388/20) EXCLUYE España por nombre; ver hallazgo |
| IC Markets | Raw Trading Ltd ("IC Markets Global") | FSA Seychelles, licencia SD018 | **NO** — ver hallazgo estructural IC Markets |
| OANDA | Fragmentado entre al menos 2 entidades — ver aviso ya declarado en pasada 1 | KNF (Polonia) para el dato de swap | **Sin resolver** — ver hallazgo estructural OANDA |
| TMGM | **Sin identificar** — las páginas de producto y condiciones son genéricas de marca, no citan qué entidad legal de las 4 declaradas describen | Depende de la entidad (ASIC Australia / VFSC Vanuatu / FSA Seychelles / FSC Mauricio) | Sin confirmar con cita primaria (hueco, criterio 10) |
| Infinox | **Sin identificar** para los criterios 1-8 — mismo problema que TMGM | Depende de la entidad | **SÍ, indicio fuerte** — Infinox Limited (FSC Mauricio, GB20025832); España no está en su lista de países restringidos, con aviso explícito de exclusión de MiFID II |
| PU Prime | **Sin identificar** para los criterios 1-8 — mismo problema | Depende de la entidad | Indicio de admisión general de marca (España no aparece en la lista de restringidos), **entidad concreta sin confirmar** |

**Consecuencia de esto para quien lea la tabla de abajo (no es una recomendación):** en XTB, IC
Markets, TMGM, Infinox y PU Prime, los datos de las columnas 1-8 **no se pueden dar por válidos
automáticamente** para la entidad con la que un residente en España abriría realmente la cuenta. Los
criterios 9-12 se han investigado tratando de anclar cada dato a la entidad correcta, y se declara
hueco donde no ha sido posible.

## Tabla A — Criterios 1 a 4 (lote, spread/comisión, swap, tipo de instrumento)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **1. Lote mínimo y fraccionado 0,1 oz** | Pedido mínimo 0,003 lote (0,3 oz); paso mínimo de transacción 0,001 lote = **0,1 oz exactas** (cuenta retail). Cuenta profesional: mínimo 0,01 lote (1 oz). Fuente: `fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` | **hueco** — el documento de costes solo da el tamaño de contrato (100 oz/lote), no el mínimo de operación ni el paso | Mínimo 1 oz (MT4 volumen 0,01). **No se ha localizado un paso de 0,1 oz.** Fuente: `fuentes/ICMarkets_commodity_spec_2026-08-04.md` | **hueco** para OANDA TMS Brokers S.A. | Mínimo 0,01 lote = **1 oz** (misma unidad mínima que IC Markets, MAYOR que 0,1 oz); máximo 80 lotes. **No se ha localizado paso de 0,1 oz.** Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` (página genérica de marca, entidad sin identificar) | **hueco** — no localizado con fuente primaria | **hueco** — no localizado con fuente primaria |
| **2. Spread y comisión reales del oro (USD/oz, ida y vuelta)** | Spread estándar 0,35, **sin comisión aparte** en cuenta Standard. Fuente: igual que fila 1 | Cuenta Razor: spread mínimo 0,05 / medio 0,19; **sin comisión aparte** ("reflected in the spread"). Fuente: `fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | XAUUSD: spread mínimo 0,00 / medio 0,63 pips, **más comisión "Raw Spread"** de 7 USD por lote, ida y vuelta. Fuente: `fuentes/ICMarkets_commodity_spec_2026-08-04.md` | **hueco** | "Spreads from 0.0 Pips", **sin cifra media ni comisión citada** en esta página. **Hueco parcial.** Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | Spread "18" (unidad no declarada verbatim; interpretado como centavos/puntos de precio, no confirmado como pip ni como USD/oz exacto), cuenta STP estándar, **"indicative in nature"** según la propia página; sin comisión ni lote citados. **Hueco parcial, con interpretación declarada, no verbatim.** Fuente: `fuentes/Infinox_condiciones_oro_2026-08-04.md` | **hueco** — las cifras de 3,0 pips (Standard) / 0,8 pips (Prime) que circulan en fuentes no admitidas (reseñas) NO se han podido confirmar con una cita literal de una página propia de PU Prime en esta sesión; no se usan |
| **3. Swap del oro, largo y corto por separado** | **HUECO POR ENTIDAD (reparación de la pasada 2):** existe cifra confirmada — Largo −8,16 %/Corto −0,76 % anual — pero **procede de la entidad de Emiratos** (documento `swaps_ae.pdf`), no de XTB Limited (Chipre, CySEC 169/12), la entidad de referencia del resto de columnas de XTB. La fuente afirma que "XTB opera un pricing/swap común documentado por instrumento, no por país" pero **no lo sostiene con cita literal** (regla de esta pasada: cita literal o hueco). Se declara hueco para esta tabla; cifra AE queda documentada aparte en `fuentes/XTB_swap_gold_2026-08-04.md` | **hueco numérico** — el documento confirma el MÉTODO (TomNext, igual que forex) pero no una cifra. Fuente: `fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | **hueco** — no se ha localizado tabla de swap | Largo **−6,65 % anual** (−18,22 USD/día/100.000 USD) · Corto **+0,65 % anual** (+1,78 USD/día). Fuente: `fuentes/OANDA_swap_gold_2026-08-04.md` — entidad OANDA TMS Brokers S.A. | **hueco numérico** — el documento declara el método ("SWAP_BY_POINTS", triple swap el miércoles) pero no una cifra de largo/corto. Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | **hueco** — no localizado | **Dato parcial, ILUSTRATIVO, no confirmado como vigente hoy ni separado por largo/corto:** el propio centro de ayuda de PU Prime da un ejemplo de cálculo — "-4,85 × 1 lote × 100 × 0,01 × 1 día = -4,85 USD" — presentado como ejemplo pedagógico de la fórmula, sin fecha de vigencia ni distinción largo/corto. **No se usa como cifra de swap actual**, se declara como lo que es: un ejemplo. Fuente: `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` (nota: el ejemplo de swap vive en un artículo de ayuda distinto, citado igual con fecha 04/08/2026) |
| **4. Instrumento: contado o con componente de futuro (L-007)** | La fila GOLD no lleva el asterisco que marca "referenciado a futuro" (nota 5). Indicio documental, no declaración explícita | El swap se calcula con la MISMA fórmula que forex (TomNext), separada expresamente de la fórmula de futuro que usa para "Commodities and Treasuries". Indicio documental más claro de los 7 de que se trata como spot | **hueco** — no localizado. **Añadido a la lista consolidada de huecos del resumen (reparación de la pasada 2, punto 2 del encargo)** | Cita textual: **"OANDA prices are calculated from the theoretical spot prices derived from underlying futures"** — el propio bróker admite que deriva de futuros subyacentes | **hueco** — no localizado con fuente primaria en esta sesión | **hueco** — no localizado | **hueco** — no localizado |

## Tabla B — Criterios 5 a 8 (demo, API, regulador/protección general, horario)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **5. Cuenta demo, disponibilidad y caducidad** | **hueco** — no confirmado | **HUECO POR ENTIDAD (reparación):** dato existente — MT4/MT5 caduca a 60 días, cTrader no caduca si se accede cada 90 días — pero procede de `pepperstone.com/en/help-and-support/...` (dominio global "en"), **sin ninguna mención de que aplique a Pepperstone Limited (UK, FCA 684312)**, la entidad de referencia del resto de columnas. Sin cita literal que lo ligue a esa entidad → hueco. Contenido conservado en `fuentes/Pepperstone_demo_api_proteccion_2026-08-04.md` | **hueco** — accesos fallidos en esta sesión | Existe demo genérica (`developer.oanda.com`), pero **para OANDA TMS Brokers S.A. específicamente**, la caducidad se ha localizado ahora: **"The demo account expires 180 days after your last login"** (actualiza el hueco de la pasada 1). Fuente: `fuentes/OANDA_TMS_espana_demo_2026-08-04.md`. Aviso nuevo, ver criterio 10: **residentes en España no pueden abrir demo con esta entidad "por motivos regulatorios"** | **30 días** desde la creación (MT5); se pueden crear cuentas ilimitadas con fondos nuevos. **No se declara si existe conversión a "sin caducidad".** Fuente: `fuentes/TMGM_demo_2026-08-04.md` | **hueco** — no localizado | **hueco** — no localizado |
| **6. API o acceso programático** | **RESUELTO (mandato explícito de esta pasada): NO.** Fuente primaria propia de XTB, cita literal: *"API access is no longer available. The service was discontinued on March 14, 2025."* Confirmado en dos páginas oficiales del centro de ayuda (`/en/` y `/int/`). Cierra la pregunta abierta que dejó la pasada 1 con fuentes secundarias no admisibles. Fuente: `fuentes/XTB_api_discontinuada_2026-08-04.md` | **HUECO POR ENTIDAD (reparación):** cTrader Automate mencionado en `pepperstone.com/en-eu/...` — dominio de la UE, **SIN ningún aviso** de que sea otra jurisdicción (a diferencia de la celda de protección, que sí avisa). Sin cita que lo ligue a Pepperstone Limited (UK) → hueco. Es, según la propia ficha de esta tarea, "la celda peligrosa", precisamente porque nada advertía del cambio de dominio | cTrader Open API, confirmado por páginas oficiales (blog corporativo y cAlgo), coherentes con la entidad Raw Trading Ltd usada en el resto de columnas de IC Markets | **NO — confirmado por fuente primaria:** excluida explícitamente de la API REST v20. Cita: *"available to all divisions except OANDA Global Markets and OANDA TMS BROKERS S.A."* Fuente: `fuentes/OANDA_api_v20_entidades_2026-08-04.md` | **hueco** — MT4/MT5 ofrecen Expert Advisors (trading algorítmico dentro de la plataforma), pero no se ha localizado una API REST/FIX propia de TMGM independiente de MetaTrader. Fuente: `fuentes/TMGM_demo_2026-08-04.md` | **hueco** — no localizado con fuente primaria propia | **hueco** — MT4/MT5 con Expert Advisors mencionados en marketing general; no se ha localizado una página propia de PU Prime con detalle técnico de API verificable por cita literal |
| **7. Regulador y protección de saldo (general)** | XTB Limited, CySEC (Chipre), licencia 169/12. ICF: tope **20.000 € por cliente** (documento de mayo 2019). Protección de saldo negativo: hueco. Fuente: `fuentes/XTB_regulador_icf_2026-08-04.md` | Pepperstone Limited, FCA (Reino Unido), registro 684312 — **identidad de entidad no se toca, es background**. **HUECO POR ENTIDAD para el CONTENIDO de protección** (segregación de fondos, NBP retail): procede de `pepperstone.com/en-au/...` (dominio australiano), con aviso YA declarado en la pasada 1 de que puede no aplicar palabra por palabra a la entidad UK. Bajo la regla de esta pasada (cita literal o hueco), sin esa cita el contenido de protección pasa a **hueco explícito**, no solo "con reserva". Fuente: `fuentes/Pepperstone_demo_api_proteccion_2026-08-04.md` | Raw Trading Ltd, FSA Seychelles, licencia SD018. Fondos segregados confirmados. **Protección de saldo negativo: hueco.** Fuente: `fuentes/ICMarkets_regulacion_2026-08-04.md` | OANDA TMS Brokers S.A., KNF (Polonia). Protección de saldo/fondos: hueco | Cuatro entidades (ver tabla de arriba). **Protección citada es de marca, no por entidad:** seguro de responsabilidad profesional hasta 10 millones AUD, miembro de "The Financial Commission" (organismo privado de resolución de disputas con fondo de compensación propio, no un fondo de garantía de inversores estatal). Fuente: `fuentes/TMGM_entidades_2026-08-04.md` | Cuatro entidades (Mauricio FSC, Anguila sin regular, EAU CMA, Chipre solo pagos). Seguro declarado hasta **500.000 USD por reclamante**, vigente 01/06/2026-31/05/2027. Fuente: `fuentes/Infinox_entidades_legal_2026-08-04.md` | Seis entidades (ver tabla de arriba). Fondo de compensación de marca (no estatal): hasta **20.000 € por caso**, vía membresía en "The Financial Commission". NBP declarada de marca, con reseteo manual o asistido, no automático. Fuente: `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` |
| **8. Horario de negociación del oro** | Sesión "12:00 am - 11:00 pm"; viernes corta a las 22:00 CET/CEST. Apertura domingo: hueco. Fuente: `fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` | L-J 01:01-23:59, V 01:01-23:55, huso GMT+3 (servidor). Cierre viernes ≈ 20:55 UTC, apertura domingo ≈ 22:01 UTC. Fuente: `fuentes/Pepperstone_horario_trading_hours_2026-08-04.md` | **hueco parcial** — solo huso de servidor confirmado | Apertura domingo 23:00 UTC, cierre viernes 22:00 UTC, pausa diaria 45 min. Fuente: `fuentes/OANDA_horario_operacion_metales_2026-08-04.md` | Apertura domingo 22:00 UTC, cierre viernes 21:59 UTC, pausa diaria ~1 minuto hacia las 22:00 UTC. **Entidad sin identificar** (página genérica de marca). Fuente: `fuentes/TMGM_oro_specs_2026-08-04.md` | **hueco** — no localizado | **hueco** — no localizado |

## Tabla C — Criterios 9 y 10 (entidad exacta + API de esa entidad · admisión de residente en España)

| Criterio | XTB | Pepperstone | IC Markets | OANDA | TMGM | Infinox | PU Prime |
|---|---|---|---|---|---|---|---|
| **9. Entidad legal exacta de la fila (criterios 1-8), y si ESA entidad da acceso por API** | XTB Limited (Chipre, CySEC 169/12). ¿API de esta entidad? Confirmado grupo-wide que NO hay API (criterio 6); no hay evidencia de que sea distinto por entidad, dato de producto/plataforma | Pepperstone Limited (Reino Unido, FCA 684312). ¿API de esta entidad? **Hueco** — el único dato de API encontrado viene de otro dominio, sin ligar a esta entidad | Raw Trading Ltd "IC Markets Global" (Seychelles, FSA SD018). ¿API de esta entidad? **SÍ**, cTrader Open API confirmado desde fuentes corporativas coherentes con esta marca/entidad | OANDA TMS Brokers S.A. (Polonia, KNF). ¿API de esta entidad? **NO**, confirmado explícitamente | **Hueco de asignación** — ninguna de las 4 entidades de TMGM (ASIC Australia AFSL 436416 · VFSC Vanuatu 40356 · FSA Seychelles SD224 · FSC Mauricio GB22201012) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/TMGM_entidades_2026-08-04.md` | **Hueco de asignación** — ninguna de las 4 entidades de Infinox (FSC Mauricio GB20025832 · Anguila sin regular · CMA EAU 20200000379 · Chipre HE440832 solo pagos) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/Infinox_entidades_legal_2026-08-04.md` | **Hueco de asignación** — ninguna de las 6 entidades de PU Prime (ASIC Australia 410681 · CMA EAU 20200000388 · FSC Mauricio GB23202672 · FSA Seychelles SD050 · FSCA Sudáfrica 52218 · Chipre HE414308) se ha podido ligar con cita literal a los datos de los criterios 1-8. Fuente: `fuentes/PUPrime_regulacion_2026-08-04.md` |
| **10. ¿Admite a un residente en España? ¿Qué entidad concreta?** | **HALLAZGO ESTRUCTURAL — SÍ, pero con OTRA entidad**: **XTB S.A., Sucursal en España** (rama de XTB S.A., Polonia — KNF —, supervisada también por la CNMV). **Es DISTINTA de XTB Limited** (Chipre, CySEC), la entidad de los criterios 1-9. Fuente: `fuentes/XTB_sucursal_espana_2026-08-04.md` (documento oficial "información básica", PDF de XTB, y redirección propia del sitio) | **NO, con cita literal directa del propio bróker:** *"The information on this site is not intended for residents of Belgium, Spain or the United States"* — página de Pepperstone EU Ltd (Chipre, CySEC 388/20), la entidad que normalmente serviría a un cliente de la UE/EEE. **No se ha localizado ninguna entidad de Pepperstone (Reino Unido, Australia) que declare admitir expresamente a España**; el Reino Unido, tras el Brexit, típicamente no sirve a clientes UE bajo pasaporte —razón de ser de la propia entidad de Chipre—, pero esto es un indicio razonado, no una cita literal propia. Fuente: `fuentes/Pepperstone_EU_fondos_espana_excluida_2026-08-04.md` | **HALLAZGO ESTRUCTURAL — SÍ, pero con OTRA entidad**: **IC Markets (EU) Ltd** (Chipre, CySEC 362/18 — número confirmado por registro público del regulador, no por el bróker). La propia página de regulación de IC Markets, al identificar visitantes de la UE/EEE, los redirige a esta entidad y declara literalmente que Raw Trading Ltd (la entidad de los criterios 1-9) *"is not established in the European Union or regulated by an EU National Competent Authority"*. Fuente: `fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` (redirección UE/EEE) y `fuentes/ICMarkets_EU_cysec_registro_2026-08-04.md` (número de licencia, registro público de CySEC) | **HUECO, con dato parcial contradictorio a favor de investigar más:** OANDA TMS Brokers S.A. **bloquea la cuenta DEMO** a residentes en España "por motivos regulatorios" (cita literal), lo que sugiere indirectamente que la cuenta REAL sí podría existir, pero **no hay cita primaria que lo confirme positivamente**. Existe indicio (no citable como fuente, de un registro mercantil de terceros) de una sucursal española de esta entidad con estado de actividad no verificado. Fuente: `fuentes/OANDA_TMS_espana_demo_2026-08-04.md` | **HUECO** — no se ha localizado, con las herramientas de esta sesión, una declaración positiva ni negativa verificable sobre España con cita literal propia de TMGM. El PDF del Client Agreement no fue legible (no hay `poppler-utils` para renderizarlo, y el modelo de extracción de texto lo describió como binario no legible); las páginas de registro están renderizadas por JavaScript y no devolvieron contenido con WebFetch | **SÍ**, vía **Infinox Limited** (Mauricio, FSC GB20025832). España NO figura en la lista literal de regiones restringidas de esta entidad (Bielorrusia, Bélgica, Canadá, Guam, India, Irán, Israel, Myanmar, Corea del Norte, Puerto Rico, Rusia, Sudáfrica, Sudán del Sur, Reino Unido, Islas Vírgenes de EE. UU., EE. UU.). **Con aviso explícito del propio bróker** de que operar con esta entidad implica quedar fuera de MiFID II. Fuente: `fuentes/Infinox_restringidos_mifid_2026-08-04.md` | **Indicio de admisión general, entidad concreta sin confirmar**: España no figura en la lista literal de países restringidos de marca ("Singapur, EE. UU., Australia, China, Filipinas, Corea del Norte, Irán" + lista FATF). **No hay cita que declare CON QUÉ entidad concreta** (de las 6) se abriría la cuenta de un residente en España; las candidatas más plausibles por ser "internacionales" son Seychelles (SD050) o Mauricio (GB23202672), pero es una conjetura razonada, no una cita — se declara hueco la asignación de entidad. Fuente: `fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` |

## Tabla D — Criterios 11 y 12 (depósito/retirada en criptomoneda · régimen regulatorio, 4 datos)

Los criterios 11 y 12 se responden **para la entidad que admite a España** identificada en el
criterio 10 (columna anterior), no para la entidad de referencia de las columnas 1-9. Donde el
criterio 10 es hueco, el 11 y el 12 heredan ese hueco: no se puede describir el régimen de una
entidad que no se ha podido identificar.

| Criterio | XTB (Sucursal España) | Pepperstone (sin entidad que admita España) | IC Markets (EU) Ltd | OANDA (entidad sin confirmar) | TMGM (entidad sin confirmar) | Infinox Limited (Mauricio) | PU Prime (entidad sin confirmar) |
|---|---|---|---|---|---|---|---|
| **11. Depósito y retirada en criptomoneda, residente en España, ¿misma vía de vuelta?** | **hueco** — no investigado para esta entidad en esta sesión | **No aplica** — se hereda el hueco de admisión del criterio 10; no hay entidad confirmada con la que evaluarlo | **NO, confirmado por fuente primaria:** la página oficial de financiación de IC Markets (EU) Ltd solo lista tarjetas (Visa, Mastercard) y transferencias bancarias (varios proveedores), en USD/EUR/GBP; **no menciona ninguna criptomoneda**. Fuente: página `icmarkets.eu/en/trading-accounts/funding`, consultada 04/08/2026 (no guardada aparte, mismo hallazgo que `fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` documenta con su URL y fecha) | **hueco** — depende de resolver primero el criterio 10 | **hueco** — depende de resolver primero el criterio 10; una búsqueda no admitida (solo resumen de motor de búsqueda, sin fetch directo citable) sugiere USDT/USDC entre los métodos de TMGM, pero **no se usa como fuente** por no tener cita literal guardada de una página propia | **No confirmado — la página oficial NO lo menciona:** la guía oficial de depósitos de Infinox (`infinox.com/global/en/help-center/important-guidelines-for-making-deposits/`) solo cita depósito mínimo de 50 USD, tarjetas prepago y la norma de "sin pagos de terceros"; **no menciona Bitcoin, USDT ni ninguna criptomoneda**, lo que contradice indicios de fuentes no admitidas que sí las mencionaban. Se declara **no confirmado con fuente primaria**, ni en positivo ni en negativo definitivo. Fuente: `fuentes/Infinox_condiciones_oro_2026-08-04.md` (nota: el hallazgo de esta celda vive en la URL de arriba, consultada 04/08/2026, mismo día que el resto de fuentes de Infinox) | **hueco** — depende de resolver primero el criterio 10 |
| **12. Régimen regulatorio (i) fondo de garantía, importe · (ii) apalancamiento máximo · (iii) protección de saldo negativo · (iv) vía de reclamación real desde España** | **(i) hueco** — el ICF de 20.000 € verificado en la pasada 1 pertenece a XTB Limited (Chipre) y **no se hereda** a la Sucursal española (sería repetir el error de L-007 de LECCIONES.md, esta vez sobre la entidad); no se ha podido extraer del PDF de la Sucursal una cifra propia con las herramientas de esta sesión. **(ii) hueco** — no extraído. **(iii) hueco** — no extraído. **(iv) parcial:** contacto declarado `sales@xtb.es` / `support@xtb.es`, doble supervisión CNMV (España) + KNF (Polonia) confirmada, pero sin un proceso formal de reclamación citado literalmente. Fuente: `fuentes/XTB_sucursal_espana_2026-08-04.md` | **No aplica** — sin entidad admitida, los 4 datos no tienen a qué entidad anclarse | **(i) Fondo de Compensación de Inversores (ICF, Chipre): hasta el 90% del reclamado o 20.000 €, lo que sea menor** (cita literal). **(ii) Apalancamiento: 1:30 para clientes minoristas, hasta 1:500 para profesionales** (cita literal). **(iii) Protección de saldo negativo: SÍ para minoristas, explícitamente NO para profesionales** (cita literal). **(iv) Formulario de reclamación al Departamento de Cumplimiento**, `compliance@icmarkets.eu`, bajo supervisión de CySEC (cita literal). Los 4 datos, con fuente primaria y cita literal. Fuente: `fuentes/ICMarkets_EU_faqs_2026-08-04.md` | Los 4 datos son **hueco** — dependen de resolver primero el criterio 10 (qué entidad admite a España) | Los 4 datos son **hueco** — dependen de resolver primero el criterio 9/10 (qué entidad de las 4 corresponde a los datos ya reunidos) | **(i) hueco** — sin cifra de fondo de garantía tipo UE citada para esta entidad; el propio bróker avisa expresamente, en la misma página que confirma la admisión, de que operar aquí implica quedar **fuera del régimen MiFID II** ("you will lose all protections afforded under EU regulation and law", cita literal). **(ii) hueco** — no se ha localizado cifra de apalancamiento propia de esta entidad para oro. **(iii) Mencionada de forma genérica, sin mecanismo ni cifra:** *"under FSC Regulation, INFINOX offers Best Execution protections and Balance Protection to protect accounts from negative balances"* (cita literal, sin más detalle). **(iv) hueco** — no se ha localizado un proceso de reclamación específico de esta entidad con cita literal. Fuente: `fuentes/Infinox_restringidos_mifid_2026-08-04.md` | Los 4 datos son **hueco** — dependen de resolver primero qué entidad concreta (de las 6) admite a España |

## Hallazgos estructurales — fragmentación de entidad (tres casos, misma familia)

**No son una recomendación: son una advertencia de proceso**, igual que ya se declaró para OANDA en
la pasada 1. Los tres casos comparten el mismo patrón: la marca no es una sola entidad legal, y la
entidad usada para comparar precios y condiciones (criterios 1-9) **no siempre es** la que un
residente en España usaría de verdad (criterio 10).

### OANDA (pasada 1, sigue sin resolver del todo)

La única cifra de swap de oro verificada pertenece a OANDA TMS Brokers S.A. (Polonia, KNF), excluida
de la API REST v20. El documento de horario no declara su entidad. **Novedad de esta pasada:** se ha
confirmado la caducidad de la demo de OANDA TMS Brokers S.A. (180 días) y que esta misma entidad
**bloquea la demo a residentes en España por motivos regulatorios**, lo que apunta a que la cuenta
real sí podría existir para España con esta MISMA entidad — pero sin cita primaria que lo confirme
en positivo. Sigue sin resolverse si las filas 3, 6 y 8 corresponden todas a la misma entidad.

### XTB (nuevo en esta pasada)

**XTB Limited** (Chipre, CySEC 169/12) es la entidad de referencia de los criterios 1-9 de esta
tabla desde la pasada 1. **Un residente en España abriría cuenta con XTB S.A., Sucursal en España**
—rama de XTB S.A. (Polonia, KNF), con doble supervisión CNMV + KNF—, una entidad **distinta**. La
API confirmada como discontinuada (criterio 6) es un dato de marca/plataforma que razonablemente
aplica a ambas, pero el fondo de garantía de 20.000 € (ICF de Chipre), el spread, el swap y el lote
mínimo verificados en los criterios 1-3 y 7 **pertenecen a XTB Limited y no se han vuelto a verificar
para la Sucursal española** en esta tarea.

### IC Markets (nuevo en esta pasada)

**Raw Trading Ltd** ("IC Markets Global", Seychelles, FSA SD018) es la entidad de referencia de los
criterios 1-9. La propia página de regulación de IC Markets declara, con cita literal, que esta
entidad **no está establecida en la Unión Europea ni regulada por una autoridad nacional competente
de la UE**, y redirige a los visitantes de la UE/EEE hacia **IC Markets (EU) Ltd** (Chipre, CySEC —
ver criterio 10 de la Tabla C para el número de licencia con cita literal a fuente primaria) — la
entidad que sí ha confirmado, con cita literal y los 4 datos completos, admitir a España con su
régimen regulatorio (criterio 12). El lote mínimo, spread, comisión y swap de los criterios 1-3
**no se han verificado para IC Markets (EU) Ltd.**

### Pepperstone (nuevo en esta pasada, y es el más tajante de los tres)

A diferencia de OANDA, XTB e IC Markets —donde existe una entidad alternativa que sí admite a
España—, en Pepperstone la única entidad de la Unión Europea localizada (**Pepperstone EU Ltd**,
Chipre, CySEC 388/20) **excluye a España por nombre, en su propia página**. No se ha encontrado, con
cita primaria propia, ninguna entidad de Pepperstone que declare expresamente admitir a España. Se
deja constancia expresa: **esto no es una recomendación de descarte, es lo que dice la fuente**; la
decisión de qué hacer con ese dato es del CEO.

## Lo que NO se ha podido verificar (declarado expresamente, regla 6 de CLAUDE.md)

**Heredado de la pasada 1, sigue sin resolver:**
- Lote mínimo y fraccionado de 0,1 oz de Pepperstone y de OANDA (TMS Brokers).
- Cifra numérica de swap de oro de Pepperstone e IC Markets (entidad de referencia).
- Caducidad de la cuenta demo de XTB e IC Markets (entidad de referencia).
- Detalle técnico de la API de Pepperstone e IC Markets más allá de "existe cTrader Open API".
- Protección de saldo negativo de XTB, IC Markets y OANDA (entidad de referencia).
- Horario exacto de apertura del domingo de XTB e IC Markets.
- A qué entidad legal de OANDA corresponde el documento de horario de mercado (criterio 8).
- **Instrumento contado o futuro (criterio 4) de IC Markets** — huella consolidada aquí por primera
  vez (reparación de la pasada 2, punto 2 del encargo: faltaba en el resumen aunque estaba bien
  declarada en la tabla desde la pasada 1).

**Nuevo de esta pasada, por la reparación de entidad-por-columna (punto 3 del encargo):**
- **Swap del oro de XTB** (criterio 3): pasa de "dato confirmado" a **hueco**, porque la cifra
  existente pertenece a la entidad de Emiratos y no hay cita que la ligue a XTB Limited (Chipre), la
  entidad de referencia de esta tabla.
- **Demo de Pepperstone** (criterio 5): pasa a hueco por la misma razón — sin cita que ligue el dato
  del dominio global a Pepperstone Limited (Reino Unido).
- **API de Pepperstone** (criterio 6): pasa a hueco por la misma razón — es, según la propia ficha de
  esta tarea, la celda más peligrosa, porque nada advertía del cambio de dominio.
- **Protección de fondos y saldo negativo de Pepperstone** (criterio 7): pasa de "con reserva" a
  hueco explícito, por la misma razón.

**Nuevo de esta pasada, por la ampliación a 7 brokers y 12 criterios:**
- Prácticamente todo el criterio 1-8 de **TMGM, Infinox y PU Prime está sin entidad asignada**: sus
  páginas de producto son genéricas de marca y no citan a qué de sus 3, 4 o 6 entidades legales
  corresponden los datos (ver "Hueco de asignación" en la Tabla C, criterio 9).
- Swap numérico de TMGM (solo método, no cifra) y de Infinox (no localizado).
- Spread y comisión exactos de PU Prime (los datos de 3,0/0,8 pips que circulan en reseñas no se han
  podido confirmar con cita literal de una página propia de PU Prime).
- API dedicada (más allá de Expert Advisors de MetaTrader) de TMGM, Infinox y PU Prime.
- Horario exacto de Infinox y PU Prime.
- Depósito/retirada en criptomoneda: **NO confirmado en positivo para ninguno de los 7 brokers.**
  Para IC Markets (EU) Ltd se confirma que NO existe (fuente primaria, solo tarjeta y transferencia).
  Para Infinox Limited (Mauricio) la página oficial de depósitos tampoco lo menciona, lo que
  contradice indicios de fuentes no admitidas. Para el resto, el criterio queda hueco porque antes
  no se resolvió con qué entidad concreta se abriría la cuenta (criterio 10).
- Los 4 datos del régimen regulatorio (criterio 12) de OANDA, TMGM y PU Prime: huecos, porque
  primero falta identificar la entidad exacta con la que un residente en España operaría.
- Apalancamiento y fondo de garantía exactos de la entidad española de XTB (Sucursal en España): el
  PDF oficial no se pudo leer completo con las herramientas disponibles en esta sesión (sin
  `poppler-utils` para renderizar páginas; el modelo de extracción no transcribe el documento
  completo). Se declara hueco en vez de inferir por analogía con la entidad de Chipre.
- Admisión de España por parte de TMGM: ni confirmada ni descartada con cita primaria verificable
  (PDF del Client Agreement ilegible con las herramientas de esta sesión; páginas de registro
  renderizadas por JavaScript).

## Lo que SÍ se puede comparar hoy sin huecos, entre los 7 (derivado estrictamente de la tabla, L-030)

- **4 de los 7** (XTB, Pepperstone —solo tamaño de contrato, el resto de la fila 1 es hueco—, IC
  Markets y TMGM) tienen el contrato de 100 oz por lote estándar confirmado por fuente primaria en
  algún punto de la fila 1 o 2. **Para Infinox, OANDA y PU Prime esta tabla no tiene, en esta pasada,
  una cita propia que confirme el tamaño de contrato**: queda hueco, no se hereda por analogía con
  los otros 4.
- **2 de los 7** (XTB —vía la entidad de Emiratos, no la de referencia de esta tabla, hueco para la
  entidad de Chipre— y OANDA —TMS Brokers—) tienen una cifra numérica de swap del oro con fuente
  primaria en algún punto de la investigación, frente a los otros 5 (Pepperstone, IC Markets, TMGM,
  Infinox, PU Prime) que quedan en hueco para una cifra numérica fiable de swap.
- **Acceso programático (criterio 6), contado con precisión sobre las 7 celdas de la Tabla B:** **1
  de los 7** (IC Markets, vía Raw Trading Ltd, su entidad de referencia) tiene cTrader Open API
  confirmado por fuente primaria coherente con esa entidad. **XTB y OANDA (TMS Brokers S.A.) tienen
  confirmado por fuente primaria que NO ofrecen API** — el dato más sólido de toda la tabla en este
  criterio, porque en los dos casos es una negación explícita del propio bróker, no una ausencia de
  dato. **Los otros 4 (Pepperstone, TMGM, Infinox, PU Prime) quedan en HUECO** para este criterio en
  su entidad de referencia: en Pepperstone porque el único dato encontrado no se pudo ligar por cita
  a la entidad correcta (reparación de esta pasada, antes figuraba como dato con reserva); en los
  otros 3, porque no se ha localizado con cita primaria propia.
- **De los 3 brokers cuya entidad de admisión de España se ha podido confirmar con cita primaria
  (XTB, vía Sucursal en España; IC Markets, vía IC Markets (EU) Ltd; e Infinox, vía Infinox Limited
  Mauricio), solo IC Markets (EU) Ltd tiene los 4 datos completos del régimen regulatorio (criterio
  12) con cita literal.** Para XTB (Sucursal España) 3 de los 4 datos son hueco y el cuarto es
  parcial; para Infinox (Mauricio) el propio bróker avisa de que el cliente queda fuera de MiFID II,
  con solo 1 de los 4 datos citado (protección de saldo, sin cifra) y los otros 3 en hueco.
- **Pepperstone es, de los 7, el único con una cita primaria propia que EXCLUYE por nombre a España**
  en la entidad de la Unión Europea que normalmente le correspondería.

## Registro de proceso

- **Modelo usado:** `claude-sonnet-5`. No hizo falta el respaldo (`claude-haiku-4-5-20251001`): el
  modelo no rechazó ninguna petición en ninguna de las dos pasadas.
- **Herramientas usadas:** `WebSearch` solo como orientación para localizar URL oficiales (NUNCA
  citada como fuente de un dato de la tabla); `WebFetch` como herramienta de cita, incluyendo el
  proxy `r.jina.ai` cuando `infinox.com` y `puprime.com` devolvían 403 directo (mismo dominio del
  bróker, solo cambia la ruta de acceso; el contenido citado sigue siendo la página oficial del
  bróker, con su URL original declarada en cada ficha de `fuentes/`). Dos PDF (TMGM Client Agreement,
  XTB información básica) no se pudieron transcribir por completo por falta de `poppler-utils` en
  este entorno; se declara hueco lo que no se pudo leer, no se completa por analogía.
- **Recuento de fuentes, verificado por `Glob` sobre el disco, no estimado (regla 14 de CLAUDE.md,
  L-020 de LECCIONES.md):** `01-investigacion/mercados/fuentes/` contiene **25 ficheros** al cerrar
  esta pasada. **11 son de la pasada 1** (conservados sin tocar; sus 24 celdas verificadas se
  mantienen intactas, salvo las 4 reparaciones de entidad-por-columna, que RELEEN esas mismas 11
  fuentes con más rigor, sin buscar nada nuevo). **14 son nuevos de esta pasada** (3 de TMGM, 3 de
  Infinox, 2 de PU Prime, 1 de la resolución de la API de XTB, 1 de la Sucursal española de XTB, 1 de
  la exclusión de España por Pepperstone EU, 2 de IC Markets (EU) Ltd, 1 de OANDA TMS y España).
- **Congelación respetada:** no se ejecutó ningún `git commit`, `checkout`, `stash`, `restore`,
  `reset` ni `amend`; no se instaló ningún paquete; no se tocó nada fuera de
  `01-investigacion/mercados/`.
- **No se abrió cuenta demo ni real de ningún bróker** (fuera de alcance de esta tarea).
- **No hay ninguna recomendación de bróker en este documento ni en las fuentes guardadas.** Los
  hallazgos de admisión (criterio 10) —en particular la exclusión expresa de España por Pepperstone
  EU Ltd, y el cambio de entidad de XTB e IC Markets— se presentan como datos con cita, no como
  descartes: la decisión de qué hacer con ellos es del CEO.
- **Resumen derivado de la tabla, contrastado frase a frase antes de entregar (L-030 de
  LECCIONES.md):** ninguna frase de las secciones "Hallazgos estructurales" ni "Lo que SÍ/NO se puede
  comparar" afirma algo que su celda correspondiente no diga; donde una celda es hueco, la frase del
  resumen que la menciona también dice "hueco". En particular: la celda de API de Pepperstone es
  HUECO en la Tabla B (criterio 6, reparación de esta pasada), y el resumen NO la cuenta entre los
  brokers con acceso programático confirmado — es el mismo defecto exacto que L-030 describe, y se
  ha corregido antes de entregar, no después.
