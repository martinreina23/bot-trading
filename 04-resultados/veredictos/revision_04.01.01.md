# ADENDA DE ESTADO — 06/08/2026, posterior a la auditoría de `critico-codigo` y al juicio del `orquestador`

Escrita por `validador` (`claude-fable-5`) por orden literal del `orquestador` (frente 2). Esta
adenda NO reescribe el veredicto: lo anota. Nada del cuerpo original se ha borrado; las tres
correcciones ordenadas quedan marcadas en el cuerpo con "[CORREGIDO 06/08 — ver adenda]" y esta
cabecera es la fuente de qué cambió y por qué. Herramienta usada: `Write` (única herramienta de
edición de este agente: el fichero se reescribe conservando el contenido íntegro salvo lo marcado).

**1. P8 Y EL MOTIVO 8 QUEDAN ANULADOS.** No por error de análisis del validador, sino porque la
orden de revisión recibida añadió como "eliminatorios" los criterios 5 (demo) y 6 (API), que la
ficha de 04.01.01 no declara eliminatorios. Verificado por ejecución propia de este validador, no
aceptado de palabra (regla 11 de CLAUDE.md):
- `grep -on "eliminatori[a-z]*" 00-direccion/WBS.md` → **`129:eliminatorio`** — una sola aparición
  en todo el WBS, dentro de la ficha de 04.01.01, pegada al criterio 1 ("es eliminatorio de hecho:
  el lote entero son unos 1.962 € contra un techo de cuenta de 2.000 €").
- **Los eliminatorios reales son el 1 y el 10.** El 1 por la frase anterior; el 10 porque la misma
  ficha lo define como criterio de ADMISIÓN: "un broker con condiciones excelentes cuya entidad
  offshore no acepte clientes españoles **queda fuera antes de mirar ni un spread**" (WBS, línea 129).
- **Origen del filtro inflado, verificado en el transcript:** fichero
  `agent-abddab6a788baa2d2.jsonl` (directorio de subagentes de esta sesión), **línea 49** — la
  "entrada 48" del parte del `orquestador` si se cuenta desde cero —, entrada con rol `assistant`.
  Frase literal localizada por ejecución:
  `grep -n "eliminatorios" agent-abddab6a788baa2d2.jsonl` → primera coincidencia en línea 49;
  `sed -n '49p' ... | grep -oE "5 \(demo\) y 6 \(API[^)]*\)"` → **"5 (demo) y 6 (API para ejecución
  desatendida)"**, dentro de "criterios eliminatorios —1 (fraccionado de 0,1 oz, ...), 10
  (admisión...), 5 (demo) y 6 (API...)". Quien dictó el filtro fue el `orquestador`; este validador
  lo ejecutó tal cual sin contrastarlo contra la ficha — la orden era ejecutable y errónea en su
  premisa, y el contraste habría sido posible con un grep.
- **L-039:** anunciada por el `orquestador` como registrada. Verificación a fecha de esta adenda:
  `grep -n "L-039" 00-direccion/LECCIONES.md` → **0 coincidencias**. Se cita como anuncio del
  `orquestador`, no como registro existente (regla 12 de CLAUDE.md: solo se cita lo firmado y
  guardado, nunca antes de existir).

**2. LA "LISTA MÍNIMA" DE P8 CAE CON ÉL.** Consecuencia medida (por el `orquestador`, y
re-verificada por este validador sobre sus propios greps de P3, filas 1 y 3): el único dato que
cumple el criterio 1 — "Paso mínimo de transacción = 0,001 lotes = **0,1 onzas exactas**",
`fuentes/XTB_especificacion_contrato_oro_2026-08-04.md`, línea 21 — pertenece a **XTB Limited
(Chipre)**, mientras que la entidad que admite a un residente en España es **XTB S.A. Sucursal en
España**, distinta según el propio documento. IC Markets, que la lista mínima de P8 nombraba como
candidato, tiene medido "Minimum Lot Size: **1 Oz**" (`fuentes/ICMarkets_commodity_spec_2026-08-04.md`,
línea 14) para Raw Trading Ltd, y para IC Markets (EU) Ltd —la entidad que admite a España— el
criterio 1 es hueco. **Para la entidad que de verdad admitiría al operador, el criterio 1 está
confirmado en CERO de los siete brokers.** La pregunta de si se puede firmar el 10/08 la responde
la ficha D-30 con la tabla reparada; este fichero no la recontesta y P8 no se recomputa aquí.

**3. CORRECCIONES APLICADAS AL CUERPO (las tres ordenadas, y solo esas):**
- **P6.b — TMGM pasa de 4 a 5** celdas con fuente. Error de transcripción de este validador: su
  propio Anexo A da 5 para TMGM (c1, c2, c5, c7, c8), y con 5 el desglose suma 31, el total del
  cubo (i) de P1. El sentido del hallazgo de P6 no cambia.
- **Cifras del registro (26 ficheros / 3 de IC Markets EU):** verificado que **ya figuraban
  correctas** en P2 ("Medido: **26** ficheros y ... → **3**") y en el motivo 5 ("hay 26 y 3");
  comando: `grep -n "hay 26 y 3\|Medido" 04-resultados/veredictos/revision_04.01.01.md`. Las
  apariciones de "25" y "2 de IC Markets" en este fichero citan el error del documento revisado, no
  lo afirman. No se reprodujo fallo alguno y no se finge una corrección (regla 11 de CLAUDE.md).
- **Motivo 6 y cierre de P7:** de las 8 celdas de barrido llamadas "en criterios eliminatorios",
  solo las **3 de c1** lo son bajo el filtro real; las 5 de c5/c6 se reclasifican como **barrido
  ordinario**. La clasificación fuente/barrido de P7 (25/15) no cambia: cambia la etiqueta de
  gravedad de 5 celdas.

**4. EL VEREDICTO SE MANTIENE: RECHAZA.** Sostenido por los motivos 1, 2, 3, 4, 5 y 7, los seis
confirmados por la auditoría independiente de `critico-codigo` con método propio (reclasificación
de las 84 celdas: 31/40/11/2, dígito a dígito; P2 reproducido: 26/26/0; greps re-ejecutados,
incluida la cita literal falsa del "90%"). El motivo 6 queda corregido como se declara arriba; el
motivo 8 queda anulado junto con P8.

---

# Revisión independiente — pasada 2 de `comparacion_brokers.md` (tarea 04.01.01)

**Quién:** `validador`. **Modelo real:** `claude-fable-5` (modelo primario; NO se usó respaldo).
**Fecha:** 06/08/2026.
**Herramientas usadas:** `Read` (documento, ficha del WBS línea 129, LECCIONES.md, las 26 fuentes de
`01-investigacion/mercados/fuentes/`), `Bash` (grep, ls, comm, wc — todos los comandos pegados junto
a cada cifra, regla 14 de CLAUDE.md y L-020 de LECCIONES.md), `Write` (este fichero).
**Qué NO pude comprobar y por qué:**
- **Nada en la red.** No tengo herramienta web. Toda cita se comprueba contra los ficheros de
  `fuentes/` en disco; una cita solo a URL es incomprobable para mí (y la propia ficha de la tarea
  lo declara así, regla 16 de CLAUDE.md).
- **Los ficheros de `fuentes/` son transcripciones del `investigador`, no los PDF/HTML originales.**
  Verifico celda-contra-fichero-en-disco; la fidelidad transcripción-contra-broker no es
  verificable por mí y queda como *no probado* (nivel 3 de la regla 9 de CLAUDE.md, declarado, no
  afirmado).
- **En P7, la existencia de la "página primaria evidente" para un bróker concreto** no es
  demostrable sin web; el criterio usa el precedente del tipo de página dentro de esta misma tabla
  y se declara como presunción con criterio escrito, no como hecho.

No reparo nada: los fallos se describen, no se tocan (quien repara deja de poder revisar). No
elijo ni recomiendo bróker: la elección es del CEO.

---

## P1 — Cobertura (unidad definida antes del número, L-018)

**Unidad de recuento:** *celda* = intersección de un bróker (7 columnas) con un criterio numerado
(12 filas de las tablas A-D). Comando estructural que produce las 12 filas:
`grep -cE '^\| \*\*[0-9]+\.' comparacion_brokers.md` → **12**; columnas de bróker por cabecera de
cada tabla: **7**. Total **84** celdas.

**Regla de clasificación (escrita antes de clasificar, cada celda en exactamente un cubo):**
- **(iii)** la celda afirma al menos un dato del criterio **sin** citar fichero de `fuentes/` ni
  referencia explícita a otra fila/criterio que sí lo cite;
- **(iv)** todo dato afirmado está marcado por la propia celda como estimado, interpretado,
  "indicativo" o "ilustrativo";
- **(i)** el dato nuclear del criterio (o parte de él) está afirmado con fuente citada o referida;
- **(ii)** la celda no afirma dato nuclear: hueco declarado (incluye "no aplica" por herencia).
Precedencia: (iii) > (iv) > (i) > (ii).

**Cifras: (i) = 31 · (ii) = 40 · (iii) = 11 · (iv) = 2 · Total = 84.** La asignación completa,
celda a celda, está en el Anexo A de este fichero (es el "comando" del recuento: reproducible
releyendo cada celda contra la regla).

**Cubo (iii) — infracción del criterio de hecho ("cada celda con su fuente y su fecha"), las 11
celdas una a una:**

| # | Celda | Qué afirma sin fuente citada | ¿Localizable en disco? |
|---|---|---|---|
| 1 | c4 XTB | "La fila GOLD no lleva el asterisco... (nota 5)" | SÍ — `grep -n "asterisco" fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` → línea 41. Defecto formal: la celda no la cita |
| 2 | c4 Pepperstone | fórmula TomNext vs fórmula de futuro | SÍ — `grep -n "TomNext" fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` → líneas 25, 31 |
| 3 | c4 OANDA | cita textual "theoretical spot prices derived from underlying futures" | SÍ — `grep -n "theoretical spot" fuentes/OANDA_horario_operacion_metales_2026-08-04.md` → líneas 25, 40 |
| 4 | c6 IC Markets | "cTrader Open API, confirmado por páginas oficiales (blog corporativo y cAlgo)" | **NO — INCOMPROBABLE**: `grep -rin "ctrader\|open api\|calgo" fuentes/ICMarkets_*` → **0** coincidencias. No hay fuente en disco |
| 5 | c7 OANDA | "OANDA TMS Brokers S.A., KNF (Polonia)" | SÍ — `grep -n "KNF" fuentes/OANDA_swap_gold_2026-08-04.md` → línea 3 |
| 6 | c8 IC Markets | "solo huso de servidor confirmado" | SÍ — `grep -n "GMT + 2" fuentes/ICMarkets_commodity_spec_2026-08-04.md` → línea 35 |
| 7 | c9 Pepperstone | identidad "Pepperstone Limited (Reino Unido, FCA 684312)" | SÍ — `grep -n "FCA Registration Number 684312" fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` → línea 4 |
| 8 | c9 IC Markets | "cTrader Open API confirmado desde fuentes corporativas" | **NO — INCOMPROBABLE** (mismo grep del punto 4, 0 coincidencias) |
| 9 | c9 OANDA | "¿API de esta entidad? NO, confirmado explícitamente" | SÍ — `grep -n "except" fuentes/OANDA_api_v20_entidades_2026-08-04.md` → línea 9. La celda no cita ni refiere |
| 10 | c11 IC Markets | "NO cripto, confirmado por fuente primaria" (página de funding de `icmarkets.eu`) | **NO — INCOMPROBABLE**: la celda admite "no guardada aparte"; `grep -rin "funding\|visa\|mastercard\|cripto\|crypto\|transferencia" fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` → **0** |
| 11 | c11 Infinox | "la página oficial NO lo menciona" (guía de depósitos: 50 USD, tarjetas prepago, sin terceros) | **NO — INCOMPROBABLE**: la celda admite que "el hallazgo vive en la URL"; `grep -rin "deposit\|depósit\|50 USD\|tarjeta\|prepago\|terceros" fuentes/Infinox_condiciones_oro_2026-08-04.md` → **0** |

**Cubo (iv), 2 celdas:** c2 Infinox (spread "18" interpretado, "indicative in nature", con fuente) y
c3 PU Prime (ejemplo −4,85 "ilustrativo, no se usa"). **Agravante en c3 PU Prime:** el ejemplo
tampoco está en el fichero citado — `grep -rn "4,85\|4\.85" fuentes/` → **0** coincidencias; la
propia celda admite que "vive en un artículo de ayuda distinto" que no se guardó. El criterio de
hecho dice "ninguna estimada": estas 2 celdas lo incumplen, aunque lo declaren.

---

## P2 — Las fuentes existen

**Unidad:** ruta distinta con patrón `fuentes/*.md` citada en el documento, tras `sort -u`.

- Rutas distintas citadas: `grep -oE 'fuentes/[A-Za-z0-9_.-]+\.md' comparacion_brokers.md | sort -u | wc -l` → **26**. Confirma la medición de partida del encargo.
- Existencia una a una (no por coincidencia de cifras): bucle
  `for f in $(grep -oE 'fuentes/[A-Za-z0-9_.-]+\.md' comparacion_brokers.md | sort -u); do test -f "$f" && echo "EXISTE: $f" || echo "NO-EXISTE: $f"; done`
  → **26 líneas "EXISTE", 0 "NO-EXISTE"** (salida completa ejecutada en esta revisión; sin repetir el precedente de `INFORME_MCP.md`).
- Ficheros en disco: `ls fuentes/ | wc -l` → **26**. No citados por nadie:
  `comm -13 <(citadas) <(ls fuentes/)` → **vacío** (0 huérfanos).

**Hallazgo — el recuento del propio documento está refutado por ejecución (regla 14, L-020):** la
línea 223 del documento dice que la carpeta "contiene **25 ficheros**", "verificado por Glob", y la
línea 228 enumera "**2 de IC Markets (EU) Ltd**". Medido: **26** ficheros y
`ls fuentes/ | grep -c "^ICMarkets_EU_"` → **3**. La causa es visible en disco:
`ICMarkets_EU_cysec_registro_2026-08-04.md` (mtime 11:24, posterior al resto, 10:46-10:53) se creó
como reparación —su propia cabecera lo dice— y el documento lo **cita** en la Tabla C, pero el
recuento del registro no se re-ejecutó después. La cifra entregada es falsa en el estado entregado.

---

## P3 — El contenido está en la fuente (muestra fijada por el encargo: criterios 1, 10 y 12 × 7 = 21 celdas)

Para las celdas hueco sin nada que localizar, el veredicto comprueba que ninguna fuente en disco
**contradiga** el hueco.

| # | Celda | Fichero | Comando | Veredicto |
|---|---|---|---|---|
| 1 | c1 XTB: mín 0,003 lote; paso 0,001 = 0,1 oz; profesional 0,01 | `XTB_especificacion_contrato_oro_2026-08-04.md` | `grep -n "0,003\|0,001" fuentes/XTB_especificacion_contrato_oro_2026-08-04.md` | LOCALIZADO (líneas 13, 20-21; profesional en línea 28) |
| 2 | c1 Pepperstone: hueco (solo tamaño de contrato) | `Pepperstone_costos_gold_feb2025_2026-08-04.md` | `grep -n "mínimo de lote" fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` | LOCALIZADO — hueco sostenido (línea 19: el documento declara que no trae el mínimo) |
| 3 | c1 IC Markets: mín 1 oz, sin paso 0,1 | `ICMarkets_commodity_spec_2026-08-04.md` | `grep -n "Minimum Lot Size" fuentes/ICMarkets_commodity_spec_2026-08-04.md` | LOCALIZADO (línea 14; hueco de 0,1 oz declarado en líneas 22-24) |
| 4 | c1 OANDA: hueco | (sin fuente citada) | `grep -rin "lot\|lote\|unit" fuentes/OANDA_*.md` | LOCALIZADO — hueco no contradicho (ninguna fuente OANDA da lote mínimo; solo "Max Units per Trade: 1000" en el horario) |
| 5 | c1 TMGM: 0,01 lote = 1 oz, máx 80 | `TMGM_oro_specs_2026-08-04.md` | `grep -n "Min Lot" fuentes/TMGM_oro_specs_2026-08-04.md` | LOCALIZADO (línea 8; máx 80 en línea 9) |
| 6 | c1 Infinox: hueco | `Infinox_condiciones_oro_2026-08-04.md` (citada en c2) | `grep -n "lote mínimo" fuentes/Infinox_condiciones_oro_2026-08-04.md` | LOCALIZADO — hueco sostenido (línea 16, declarado en la propia fuente) |
| 7 | c1 PU Prime: hueco | (sin fuente citada) | `grep -rin "lot\|lote\|unit" fuentes/PUPrime_*.md` | LOCALIZADO — hueco no contradicho (0 datos de lote en las 2 fuentes PUP) |
| 8 | c10 XTB: SÍ, XTB S.A. Sucursal en España, CNMV+KNF | `XTB_sucursal_espana_2026-08-04.md` | `grep -n "CNMV\|Sucursal en España" fuentes/XTB_sucursal_espana_2026-08-04.md` | LOCALIZADO (líneas 12-14, 19) |
| 9 | c10 Pepperstone: NO, cita literal | `Pepperstone_EU_fondos_espana_excluida_2026-08-04.md` | `grep -n "Belgium, Spain" fuentes/Pepperstone_EU_fondos_espana_excluida_2026-08-04.md` | LOCALIZADO (línea 23) |
| 10 | c10 IC Markets: SÍ vía IC Markets (EU) Ltd, CySEC 362/18 | `ICMarkets_EU_entidad_espana_2026-08-04.md` + `ICMarkets_EU_cysec_registro_2026-08-04.md` | `grep -n "not established in the European Union" fuentes/ICMarkets_EU_entidad_espana_2026-08-04.md` · `grep -n "362/18" fuentes/ICMarkets_EU_cysec_registro_2026-08-04.md` | LOCALIZADO (líneas 12 y 16 respectivamente) |
| 11 | c10 OANDA: HUECO + bloqueo de demo a España | `OANDA_TMS_espana_demo_2026-08-04.md` | `grep -n "Spain cannot open a demo" fuentes/OANDA_TMS_espana_demo_2026-08-04.md` | LOCALIZADO — hueco y dato parcial sostenidos (línea 9) |
| 12 | c10 TMGM: HUECO | (sin fuente citada en la celda) | `grep -n "admitiría a un residente" fuentes/TMGM_entidades_2026-08-04.md` | LOCALIZADO — hueco sostenido (línea 31) |
| 13 | c10 Infinox: SÍ vía Infinox Limited (Mauricio) | `Infinox_restringidos_mifid_2026-08-04.md` | `grep -n "Belarus, Belgium" fuentes/Infinox_restringidos_mifid_2026-08-04.md` | LOCALIZADO, con matiz: la fuente sostiene "España no está en la lista de restringidos" + aviso MiFID; el rótulo "SÍ" es una inferencia por ausencia, cuya base la celda declara |
| 14 | c10 PU Prime: indicio de marca, entidad hueco | `PUPrime_compensacion_nbp_paises_2026-08-04.md` | `grep -n "Singapore" fuentes/PUPrime_compensacion_nbp_paises_2026-08-04.md` | LOCALIZADO (línea 34; hueco de entidad sostenido en líneas 38-41) |
| 15 | c12 XTB: (i)(ii)(iii) huecos, (iv) parcial | `XTB_sucursal_espana_2026-08-04.md` | `grep -n "sales@xtb.es\|apalancamiento máximo\|fondo de garantía" fuentes/XTB_sucursal_espana_2026-08-04.md` | LOCALIZADO — contactos en línea 15, huecos declarados en líneas 30-37 |
| 16 | c12 Pepperstone: "No aplica" heredado del c10 | (herencia) | (la base es la fila 9 de esta tabla) | LOCALIZADO por herencia declarada |
| 17 | c12 IC Markets: los 4 datos "con cita literal" | `ICMarkets_EU_faqs_2026-08-04.md` | `grep -n "20,000\|1:30\|Negative Balance\|compliance@" fuentes/ICMarkets_EU_faqs_2026-08-04.md` · `grep -cn "whichever is lower\|lo que sea menor\|90%" fuentes/ICMarkets_EU_faqs_2026-08-04.md` · `grep -rn "90%" fuentes/` | **NO LOCALIZADO EN PARTE** — ver detalle abajo |
| 18 | c12 OANDA: 4 huecos heredados | (herencia del c10) | (la base es la fila 11) | LOCALIZADO — hueco coherente |
| 19 | c12 TMGM: 4 huecos heredados | `TMGM_entidades_2026-08-04.md` | `grep -n "protección de saldo negativo ni límite" fuentes/TMGM_entidades_2026-08-04.md` | LOCALIZADO — hueco sostenido (línea 30) |
| 20 | c12 Infinox: (iii) con cita, resto huecos | `Infinox_restringidos_mifid_2026-08-04.md` | `grep -n "outside of the EU\|Balance Protection" fuentes/Infinox_restringidos_mifid_2026-08-04.md` | LOCALIZADO (líneas 19, 22-23; huecos (i)(ii)(iv) sostenidos) |
| 21 | c12 PU Prime: 4 huecos heredados | (herencia del c10) | (la base es la fila 14) | LOCALIZADO — hueco coherente |

**La NO LOCALIZADA, enumerada como exige el encargo (fila 17):**
- **Lo que dice la celda:** "(i) Fondo de Compensación de Inversores (ICF, Chipre): **hasta el 90%
  del reclamado o 20.000 €, lo que sea menor (cita literal)**".
- **Lo que dice la fuente citada** (`ICMarkets_EU_faqs_2026-08-04.md`, línea 15): *"Offers
  compensation up to €20,000 per client if the firm fails to return client funds."* — sin rastro
  del "90%" ni del "lo que sea menor": `grep -cn "whichever is lower\|lo que sea menor\|90%"
  fuentes/ICMarkets_EU_faqs_2026-08-04.md` → **0**.
- **Dónde SÍ existe esa frase en disco:** `grep -rn "90%" fuentes/` → única coincidencia en
  `fuentes/Pepperstone_EU_fondos_espana_excluida_2026-08-04.md`, línea 18 — la cita del ICF de
  **Pepperstone EU Ltd**, otra entidad y otro bróker. La celda de IC Markets etiqueta como "cita
  literal" un texto que su fuente no contiene; el patrón apunta a arrastre entre celdas. Que la
  regla real del ICF chipriota sea efectivamente "90% o 20.000 €" no lo puedo verificar sin red, y
  aunque fuera cierto, la etiqueta "cita literal" contra esa fuente es falsa.

Resultado P3: **20 de 21 sostenidas; 1 con parte NO LOCALIZADA** (la de la fila 17).

---

## P4 — L-030 como paso nombrado (resumen contra celda, frase a frase)

**Contrastadas 48 afirmaciones:** tabla de entidades de cabecera (7), párrafo "Consecuencia" (1),
hallazgos estructurales OANDA/XTB/IC Markets/Pepperstone (4+3+3+2), "Lo que NO se ha podido
verificar" (21 puntos), "Lo que SÍ se puede comparar" (5 puntos con sus subcláusulas), registro de
proceso (2 afirmaciones numéricas, tratadas en P2).

**Frases infractoras: 1.**

| Frase del resumen | Celda de la que sale |
|---|---|
| Línea 139: "Detalle técnico de la API de Pepperstone e IC Markets **más allá de 'existe cTrader Open API'**" (lista de heredados) | La celda c6 de Pepperstone es **HUECO POR ENTIDAD** tras la reparación de esta misma pasada: no hay "existe cTrader Open API" que dar por sentado para Pepperstone. La frase presupone como existente lo que su celda declara hueco — exactamente el patrón de L-030. Quedó sin actualizar al aplicar la reparación, y contradice a la propia línea 193-201 del documento (que cuenta a Pepperstone en HUECO, correctamente) y a la declaración de las líneas 237-243 ("ninguna frase... afirma algo que su celda no diga"). Comando: `grep -n "Detalle técnico de la API" comparacion_brokers.md` → 139 |

Observaciones no infractoras (resumen igual o más débil que su celda, se declaran por
transparencia): la cabecera llama "SÍ, indicio fuerte" a lo que la celda c10 de Infinox titula
"SÍ" (más débil arriba que abajo — permitido); el hallazgo de OANDA dice "sigue sin resolverse si
las filas 3, 6 y 8 corresponden a la misma entidad" cuando 3 y 6 sí están ancladas a TMS por sus
fuentes y solo la 8 está sin resolver (impreciso hacia lo débil, no hacia lo fuerte). El punto 3 de
"Lo que SÍ" repite la afirmación de la celda c6 de IC Markets ("confirmado por fuente primaria")
con su misma fuerza — el defecto es de la celda (P1, cubo iii, incomprobable), no un exceso del
resumen sobre la celda.

---

## P5 — Las reparaciones ordenadas por la ficha, una a una

| Reparación | Veredicto | Prueba |
|---|---|---|
| (i) Frase que daba por hecho que XTB tiene API con celda en hueco | **HECHA** | La celda c6 de XTB ya no es hueco: "RESUELTO... NO", cita literal *"API access is no longer available..."*, fuente `XTB_api_discontinuada_2026-08-04.md` (líneas 9-15 del fichero). El resumen (líneas 195-197) cuenta a XTB entre los NO confirmados. `grep -in "api" comparacion_brokers.md | grep -i xtb` → ninguna frase afirma que XTB tenga API |
| (ii) Recuento "tres brokers con swap habiendo dos" | **HECHA** | `grep -n "2 de los 7" comparacion_brokers.md` → línea 189, con la cualificación correcta (XTB vía entidad de Emiratos = hueco para la de Chipre) |
| (iii) IC Markets añadido a la lista consolidada de huecos del criterio 4 | **HECHA** | Líneas 143-145 del documento ("huella consolidada aquí por primera vez, reparación de la pasada 2"); la celda c4 de IC Markets lo anota también |
| (iv) Desajuste de entidad del swap de XTB (Emiratos vs Chipre) | **HECHA** | La celda c3 de XTB pasa a "HUECO POR ENTIDAD" y declara que la frase de homogeneidad de la fuente no tiene cita literal; "Lo que NO", líneas 148-150. Nota: el fichero `XTB_swap_gold_2026-08-04.md` conserva en su cabecera (líneas 3-5) la frase de homogeneidad sin cita; la ficha ordenaba la celda, no la fuente, así que no invalida la reparación, pero queda dicho |
| (v.a) Pepperstone API desde `en-eu` | **HECHA** | Celda c6 Pepperstone = "HUECO POR ENTIDAD (reparación)"; el contenido queda conservado en `Pepperstone_demo_api_proteccion_2026-08-04.md` (líneas 18-27) |
| (v.b) Pepperstone regulador/protección desde `en-au` | **HECHA** | Celda c7: el contenido de protección pasa a "hueco explícito", no "con reserva". La identidad FCA 684312 que la celda mantiene como "background" está anclada a la entidad UK por cita literal en disco: portada del PDF de costes de la propia entidad, `grep -n "FCA Registration Number 684312" fuentes/Pepperstone_costos_gold_feb2025_2026-08-04.md` → línea 4 (aunque la celda cita como fuente el fichero del dominio `en-au`, no ese PDF — matiz formal) |
| (v.c) Pepperstone demo desde `en` | **HECHA** | Celda c5 = "HUECO POR ENTIDAD (reparación)", contenido conservado en el mismo fichero (líneas 7-14) |

Las cinco reparaciones se ejecutaron. **Pero la misma regla que las motivó ("cita literal o
hueco") quedó sin aplicar a las celdas del cubo (iii) de P1** — en particular c6/c9/c11 de
IC Markets y c11 de Infinox, que afirman "confirmado" sin fuente en disco. La reparación fue
selectiva: se aplicó a las celdas nombradas por la ficha y no al resto del documento.

---

## P6 — El sesgo, medido por efecto (L-032)

El documento declara en cabecera (líneas 18-24) que su ejecutor leyó la frase de preferencia del
CEO sobre el criterio 12 (hecho ya zanjado en L-031/L-032; no se rejuzga). Medición del efecto:

**(a) Fuentes guardadas por bróker** — comando:
`ls fuentes/ | sed -E 's/^(ICMarkets|Infinox|OANDA|PUPrime|Pepperstone|TMGM|XTB).*/\1/' | sort | uniq -c`
→ XTB **5** · IC Markets **5** · Pepperstone **4** · OANDA **4** · TMGM **3** · Infinox **3** ·
PU Prime **2**.

**(b) Celdas con fuente por bróker** (cubo (i) de P1, asignación del Anexo A):
XTB **8** · IC Markets **5** · Pepperstone **4** · OANDA **4** · TMGM **5** [CORREGIDO 06/08 —
decía 4; el Anexo A da 5 (c1, c2, c5, c7, c8) y con 5 el desglose suma 31, el total del cubo (i);
ver adenda, punto 3] · Infinox **3** · PU Prime **2** (sobre 12 posibles cada uno).

**Lectura:** el gradiente sigue la pertenencia a la pasada 1 (dos sesiones de búsqueda: XTB,
Pepperstone, IC Markets, OANDA) y la accesibilidad técnica (Infinox y PU Prime devolvían 403 y se
leyeron por proxy). **El bróker peor cubierto es PU Prime (2 fuentes, 2 celdas con fuente).** En el
criterio 12 —el del sesgo potencial— el único con los 4 datos es IC Markets (EU) Ltd (entidad UE);
los tres brokers añadidos en la pasada 2 quedan en 0/4, 1/4 y 0/4. Si la preferencia leída hubiera
inclinado la búsqueda a favor de los añadidos de la pasada 2, el resultado la contradice: son los
peor cubiertos. Con las cifras delante: no hay un bróker sistemáticamente mejor cubierto que lo que
explica la pasada de origen y los 403; ningún indicio de cobertura dirigida.

**Marcas de valoración** — comando:
`grep -inE 'mejor|recomend|ideal|óptim|optim|conviene|debería|deberia|el más|el mas' comparacion_brokers.md`
→ 6 coincidencias, todas negaciones ("no hay recomendación", "no es una recomendación", líneas 12,
44, 89, 130, 233) o cita de la ficha (línea 19); barrido ampliado de superlativos
(`grep -inE 'más [a-záéíóú]+|peor|favorit|prefer|aconsej|sugier|destaca' ...`) → "el más tajante de
los tres" (línea 124, califica un hallazgo, no un bróker), "la celda más peligrosa" (línea 154,
cita de la propia ficha), "el dato más sólido de toda la tabla" (línea 196, califica un dato),
"candidatas más plausibles" (línea 73, conjetura de entidad declarada como tal). **Ninguna
aparición ordena ni inclina entre brokers: 0 infracciones del "PROHIBIDO elegir o recomendar".**

---

## P7 — Huecos: de fuente o de barrido (criterio escrito antes de clasificar)

**Criterio:**
- **HUECO DE FUENTE:** la celda o una fuente guardada documentan dónde se buscó (página abierta y
  guardada que no contiene el dato), o una barrera concreta (403, PDF ilegible sin `poppler-utils`,
  página renderizada por JavaScript), o el hueco es herencia lógica de otro hueco (entidad sin
  identificar → no se puede describir su régimen).
- **HUECO DE BARRIDO:** el tipo de página que da ese dato existe demostradamente para otro bróker
  de esta misma tabla (especificación de contrato, tabla de swaps, FAQ de demo, página de horarios,
  página de depósitos, FAQ de help center) y ni la celda ni las fuentes registran intento ni
  barrera para este bróker. *Limitación declarada: sin web no puedo probar que la página exista
  para el bróker concreto; es presunción por precedente de tipo, y así se firma.*

**Población:** los 40 huecos del cubo (ii) de P1. **Cifras: HUECO DE FUENTE = 25 · HUECO DE
BARRIDO = 15.** Asignación completa en el Anexo A; los 15 de barrido, con la página que faltó:

| # | Celda | Página primaria que faltó |
|---|---|---|
| 1 | c1 Pepperstone | Especificación de contrato / condiciones del oro de Pepperstone (el tipo de página que sí se abrió para XTB, IC Markets y TMGM); solo se abrió el PDF de costes, que no la trae |
| 2 | c1 OANDA | Tabla de especificación de instrumentos de OANDA TMS Brokers |
| 3 | c1 PU Prime | Especificación de contrato del oro de PU Prime |
| 4 | c2 OANDA | Tabla de spreads / condiciones de cuenta de OANDA TMS Brokers |
| 5 | c2 PU Prime | La misma especificación / condiciones de PU Prime (las cifras de reseñas se rechazaron bien; la página propia no consta intentada) |
| 6 | c3 XTB | Tabla de swaps de la entidad de Chipre de XTB — la análoga exacta de `swaps_ae.pdf`, que sí se descargó para Emiratos |
| 7 | c3 IC Markets | Tabla pública de swaps de IC Markets (si existe; el spec sheet guardado no la trae y no consta dónde más se buscó) |
| 8 | c4 PU Prime | La misma especificación de contrato de PU Prime (cubriría también c1, c2 y c8) |
| 9 | c5 XTB | FAQ de demo del help center de XTB — **el mismo help center se usó con éxito en esta pasada para la API**, así que era accesible |
| 10 | c5 Infinox | FAQ de demo del help center de Infinox — el help center se usó con éxito (vía proxy) para las regiones restringidas |
| 11 | c5 PU Prime | FAQ de demo de `helpcenter.puprime.com` — usado con éxito para NBP y países |
| 12 | c6 Infinox | Página de plataformas/tecnología de Infinox (clasificación con matiz: probar una negativa exige más, pero no consta intento alguno) |
| 13 | c6 PU Prime | FAQ de API / trading automatizado del mismo helpcenter de PU Prime (la celda alude a "marketing general" sin URL ni fuente guardada) |
| 14 | c8 PU Prime | La misma especificación / página de horarios de PU Prime |
| 15 | c11 XTB | Página de métodos de depósito/retirada de `xtb.com/es` — la celda misma declara "no investigado para esta entidad en esta sesión" |

**El cubo de barrido NO está vacío → la pasada 2 no está completa**; de las 15 celdas de barrido,
**3 pertenecen al criterio eliminatorio real (c1: Pepperstone, OANDA, PU Prime)** y las 12
restantes son barrido ordinario. [CORREGIDO 06/08 — decía "8 de las 15 celdas de barrido
pertenecen a criterios eliminatorios (c1: 3 celdas; c5: 3; c6: 2)" bajo el filtro anulado que
trataba el 5 y el 6 como eliminatorios; ver adenda, puntos 1 y 3. La clasificación fuente/barrido
no cambia.]

---

## P8 — ¿Permite esta tabla firmar un bróker el 10/08 con los criterios eliminatorios 1, 10, 5 y 6?

**NO.**

Justificación: hoy ningún bróker tiene los cuatro criterios eliminatorios resueltos en positivo,
con fuente, **para la entidad que admitiría a un residente en España**:
- **XTB** — c10 SÍ (Sucursal España) pero c6 = **NO hay API** (fuente primaria, dato de marca):
  eliminado por el criterio 6. Es además el único que cumple el fraccionado de 0,1 oz (c1), y lo
  cumple en la entidad de Chipre, no verificado para la Sucursal.
- **OANDA TMS** — c6 = **NO API** (fuente primaria): eliminada esa entidad; c10 además hueco.
- **Pepperstone** — c10 = NO (la entidad UE excluye a España por nombre; ninguna otra confirmada).
- **IC Markets** — c10 SÍ vía IC Markets (EU) Ltd, pero c1, c5 y c6 de ESA entidad: sin verificar
  (los datos existentes son de Raw Trading Ltd; incluso ahí, c1 = mínimo 1 oz sin paso de 0,1, c5
  hueco y c6 sin fuente en disco).
- **TMGM** — c10 hueco; c1 de marca = 1 oz sin paso 0,1 (apunta a eliminación, sin entidad).
- **Infinox** — c10 SÍ (Mauricio, por inferencia declarada); c1, c5 y c6 huecos.
- **PU Prime** — c10 sin entidad; c1, c5 y c6 huecos.

**Lista mínima de celdas para que la respuesta pueda ser SÍ** (no lista de deseos: solo candidatos
no eliminados por una negativa con fuente):
1. **IC Markets (EU) Ltd:** c1 (lote mínimo y paso de 0,1 oz), c5 (demo), c6 (API) — 3 celdas.
2. **Infinox Limited (Mauricio):** c1, c5, c6 — 3 celdas.

Con UN candidato completado en positivo, el CEO puede firmar: mínimo absoluto **3 celdas**;
prudente, **6** (los dos candidatos, por si uno cae). Solo si ambos caen harían falta TMGM y
PU Prime, que exigen primero su c10 (entidad que admite) y luego sus c1/c5/c6.

---

## VEREDICTO

**RECHAZA.**

Motivos, cada uno con su nivel de prueba (regla 9 de CLAUDE.md); ninguno de nivel 3:

1. **Cinco afirmaciones "confirmadas" sin fuente en disco — citas incomprobables** (c6 IC Markets,
   c9 IC Markets, c11 IC Markets, c11 Infinox, y el ejemplo de c3 PU Prime): infringen el criterio
   de hecho de la ficha ("cada celda con su fuente") y su propia regla de que una cita solo a URL
   es incomprobable. **Nivel 1** — greps con 0 coincidencias, pegados en P1.
2. **Una "cita literal" falsa contra su fuente:** la celda c12 de IC Markets atribuye a
   `ICMarkets_EU_faqs` la frase "90% del reclamado o 20.000 €, lo que sea menor", que en disco solo
   existe en la fuente de **Pepperstone EU**. **Nivel 1** — greps pegados en P3, fila 17.
3. **Otras 6 celdas con dato sin fuente citada** (c4 XTB/Pepperstone/OANDA, c7 OANDA, c8 IC
   Markets, c9 Pepperstone/OANDA — localizables en disco pero sin cita en la celda): defecto formal
   reiterado del mismo criterio de hecho. **Nivel 2** — tabla del cubo (iii) en P1, con fichero y
   línea de cada dato.
4. **El resumen vuelve a afirmar más que una celda** (línea 139 contra la c6 de Pepperstone, hueco):
   reincidencia del defecto que dio origen a L-030 en este mismo fichero, y desmiente la
   declaración de las líneas 237-243. **Nivel 2** — grep pegado en P4.
5. **El recuento del registro está refutado por ejecución:** dice 25 ficheros y "2 de IC Markets
   (EU)"; hay 26 y 3. Cifra presentada como "verificado por Glob" que no corresponde al estado
   entregado (regla 14 de CLAUDE.md, L-020). **Nivel 1** — comandos pegados en P2.
6. **15 huecos de barrido, 3 de ellos en el criterio eliminatorio real (c1):** hay páginas
   primarias del tipo ya usado con éxito en esta misma tabla (incluidos help centers ya accedidos
   del mismo bróker) sin constancia de intento. La pasada 2 no está completa. **Nivel 2** —
   criterio escrito y asignación en P7 (con la limitación sin-web declarada). [CORREGIDO 06/08 —
   decía "8 de ellos en criterios eliminatorios" bajo el filtro anulado; las 5 celdas de c5/c6 son
   barrido ordinario; ver adenda, puntos 1 y 3.]
7. **Dos celdas con dato estimado/interpretado** (c2 Infinox, c3 PU Prime) contra el "ninguna
   estimada" del criterio de hecho — declaradas por el ejecutor, pero presentes. **Nivel 2** — P1,
   cubo (iv).
8. **Consecuencia de calendario (P8): NO** — la tabla hoy no permite firmar el 10/08; faltan como
   mínimo las 3 celdas de un candidato viable (lista mínima en P8). **Nivel 2** — derivado
   celda a celda de la tabla, sin opinión.

**Lo que NO invalida este veredicto y conviene que conste:** las 26 fuentes citadas existen todas y
ninguna sobra (P2); 20 de las 21 celdas de la muestra fijada están sostenidas por su fuente (P3);
las 5 reparaciones ordenadas se ejecutaron (P5); y no hay una sola frase que recomiende bróker
(P6). El documento es mayoritariamente honesto en sus huecos; se rechaza porque su criterio de
hecho exige "cada celda con fuente, ninguna estimada, lo que no tenga fuente declarado hueco", y
eso hoy es falso en 13 celdas (11 del cubo iii + 2 del iv), una de ellas con etiqueta de cita
literal que su fuente desmiente — y porque la pasada, medida por su propio objetivo (dejar al CEO
firmar el 10/08), no está terminada.

---

## Anexo A — Asignación celda a celda (base reproducible de P1, P6.b y P7)

Formato: criterio → XTB · Pepperstone · IC Markets · OANDA · TMGM · Infinox · PU Prime.
Cubos: i = con fuente · ii = hueco declarado · iii = dato sin fuente · iv = estimado/interpretado.
Para los (ii): F = hueco de fuente, B = hueco de barrido (P7).

| Criterio | XTB | Pepp | ICM | OANDA | TMGM | Infinox | PUP |
|---|---|---|---|---|---|---|---|
| 1 | i | ii-B | i | ii-B | i | ii-F | ii-B |
| 2 | i | i | i | ii-B | i (parcial) | iv | ii-B |
| 3 | ii-B | ii-F | ii-B | i | ii-F | ii-F | iv |
| 4 | iii | iii | ii-F | iii | ii-F | ii-F | ii-B |
| 5 | ii-B | ii-F | ii-F | i | i | ii-B | ii-B |
| 6 | i | ii-F | iii | i | ii-F | ii-B | ii-B |
| 7 | i | i (parcial) | i | iii | i | i | i |
| 8 | i (parcial) | i | iii | i | i | ii-F | ii-B |
| 9 | i (por referencia al c6) | iii | iii | iii | ii-F | ii-F | ii-F |
| 10 | i | i | i | ii-F | ii-F | i | i (parcial) |
| 11 | ii-B | ii-F | iii | ii-F | ii-F | iii | ii-F |
| 12 | i (parcial) | ii-F | i | ii-F | ii-F | i (parcial) | ii-F |

Sumas por cubo: i = 31 · ii = 40 (F 25 + B 15) · iii = 11 · iv = 2 · **Total 84**.
