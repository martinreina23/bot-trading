# Veredicto de la Fase 02 — segunda pasada de 02.03.01 (02/08/2026)

**Agente:** `validador` (`claude-fable-5`, sin respaldo necesario: el modelo principal respondió).
**Papel:** re-veredicto de los 7 motivos del RECHAZA del 31/07 (histórico íntegro en la celda ESTADO
de la fila `02.03.01` de `00-direccion/WBS.md`). **Método:** verificación documental localizada por
búsqueda (regla 12 de CLAUDE.md) y aritmética ejecutada aplicando los factores que manda la ficha
(regla 9 de CLAUDE.md, nivel 1) — script `03-motor/scripts/deriva_oro.py` (en el repositorio, ejecutable
por cualquier tercero), ejecutado el 02/08 desde esa ruta sobre los JSON ya cerrados. **No se ha recalculado ATR, coste ni correlación desde cero** (prohibido por la ficha).
**No se ha abierto `02-datos/reservado/`.** Referencias por nombre de sección o símbolo, nunca por
número de línea (regla 13 de CLAUDE.md).

---

## VEREDICTO GLOBAL (una línea)

**ACEPTA CON HUECOS DECLARADOS** — válido SOLO si el defecto del motivo 5 (G1-C1 suma costes de
brokers y tipos de cuenta distintos) llega DECLARADO al CEO en la ficha de la puerta G1; si esa
ficha lo omite, este veredicto decae y rige el RECHAZA de la primera pasada.

**Balance: 4 motivos CERRADOS (1, 3, 6, 7) · 3 ABIERTOS (2, 4, 5) · el 5 se ESCALA al CEO.**
No se cierran los 7 de golpe ni todos por D-11: D-11 solo resuelve el 1, parte del 2 y el 6.

---

## Los 7 motivos, uno a uno

### Motivo 1 — Dos criterios de G1 sin dato («cientos de operaciones posibles» y «operable sin nadie delante») → **CERRADO**

**Prueba (verificación documental, localizada por búsqueda):**
- `00-direccion/DECISIONES.md`, sección `## D-11 · 2026-08-01 · Siete criterios de G1 aprobados
  (G1-C1 a G1-C7)`, párrafo **Motivo**, dice literalmente: *«**G1-C4** minimo 1.000 velas/año en la
  vela elegida, sin minimo de operaciones (ninguna fuente primaria lo respalda)»* y *«Lo que SALE de
  G1: "operable sin nadie delante", que pasa a la Fase 03»*. Afirmado de verdad, no solo anunciado.
- `00-direccion/WBS.md`, sección `## Puertas`, viñetas **G1-C4 — MUESTRA** y **FUERA DE G1**:
  mismo contenido, operativo en la puerta.
- El criterio sustituto SÍ tiene dato: velas/año contadas (no estimadas) en
  `arrastre_coste.md`, sección `## 3. Calculo 1 — Velas disponibles al año`: a 4h, 1.598–1.611
  velas/año en los 6 no-cripto, por encima del mínimo de 1.000. La ausencia de mínimo de operaciones
  está respaldada por `evidencia_umbrales_g1.md`, sección 2 (ninguna fuente primaria verificada da
  ese mínimo; la cifra «300 operaciones» era una alucinación de WebFetch descartada).

### Motivo 2 — Criterios de G1 sin numerar; los documentos se inventaron su numeración → **ABIERTO**

**Lo que D-11 sí resuelve (localizado):** la numeración existe y está aprobada — título de la
sección `## D-11 · 2026-08-01 · Siete criterios de G1 aprobados (G1-C1 a G1-C7)` de
`00-direccion/DECISIONES.md`, y viñetas **G1-C1** a **G1-C7** de la sección `## Puertas` del WBS.

**Lo que sigue en pie (grep ejecutado el 02/08 sobre los entregables listados en la ficha):**
- `coste_swap.md`, párrafo de cabecera (el que empieza por **Tarea:** 02.02.05): *«Es el criterio 2
  de la puerta G1»*. Bajo D-11 el swap es **G1-C3** y no tiene umbral propio. **Sigue contradiciendo
  la numeración aprobada** — la comprobación exacta que pedía la ficha falla.
- `coste_relativo.md`, cabecera y sección `## Resumen: qué pasa el criterio 1 de G1 (≤10-15%) y qué
  no`: se declara «criterio 1» con umbral «≤10-15%». Bajo D-11, ese cociente es **G1-C2** y su
  umbral aprobado es **≤10% sobre p10**, sin banda 10-15%.
- `correlaciones_8x8.md`, sección `## Pares que superan |0,7| en alguna de las tres ventanas —
  criterio 4 de G1`: bajo D-11 la correlación es **G1-C5**.
- `evidencia_umbrales_g1.md`, sección 1: cita «criterio 1 de G1, ≤10-15%» (heredado de
  `coste_relativo.md`).

Cuatro entregables llevan numeración o umbral pre-D-11. No lo corrijo yo (la ficha solo manda
comprobar): queda como corrección pendiente que debe repartir el orquestador, y mientras tanto
acota lo que 02.03.02 puede citar (ver lista final).

### Motivo 3 — Coste del oro de feb-2025 dividido contra ATR de jul-2026, sin segunda fuente de deriva → **CERRADO (por la vía ii de la ficha: recálculo con cota superior, número delante)**

**Vía usada:** la (ii) — no se localizó segunda fuente primaria de coste del oro ≥2026 dentro de
los entregables, así que se aplicaron los factores de deriva medidos como cota superior. Los
factores salen de los propios documentos (`coste_operar.md`, filas BTCUSD y ETHUSD de la Tabla
FINAL): BTC 36,90/20,22 = **+82,5%**; ETH 7,04/3,01 = **+133,9%** en los mismos 14 meses.

**Números ejecutados (script `deriva_oro.py`, insumos: `atr_15m_1h_4h.json` y coste 0,26 USD/oz de
`coste_operar.md`, fila XAUUSD):**

| XAUUSD | base | coste ×1,82 | coste ×2,34 | umbral | ¿cambia el veredicto? |
|---|---|---|---|---|---|
| **G1-C2 a 4h** (coste/ATR p10 11,2099) | 2,32% | **4,22%** | **5,43%** | ≤10% | **NO: sigue pasando** |
| G1-C2 a 1h (p10 5,5256) | 4,71% | 8,56% | **11,01%** | ≤10% | SÍ en la cota alta: dejaría de pasar |
| G1-C2 a 15m (p10 2,3893) | 10,88% | 19,80% | 25,46% | ≤15% laxo | SÍ: deja de pasar incluso el laxo (coincide con la primera pasada: 19,9–25,4%) |
| **G1-C1 a 4h**, arrastre central 79,9 ops/año (cr mediana 1,1737%) | 0,94% | **1,71%** | **2,19%** | ≤5% | **NO: sigue pasando** |
| G1-C1 a 4h, tope de operaciones/año de XAUUSD | 426 | **234** | **182** | — | el extremo alto publicado «426» deja de valer como cota bajo deriva |

**Declaración con el número, como exige la ficha: el veredicto de G1 a 4h NO cambia.** XAUUSD a 4h
sigue pasando G1-C2 (5,43% ≤ 10% incluso con coste ×2,34; pasaría a ser el peor de los 6, por
delante de AUDUSD 5,24%, pero pasa) y sigue dentro del presupuesto de G1-C1 en el escenario central
(2,19% ≤ 5%). Lo que SÍ cambia bajo la cota: el oro a **15m** deja de pasar la vela tranquila (era
el único que pasaba) y a **1h** rompe el 10% en la cota alta; y el tope «426» de la banda de G1-C1
bajaría a 234/182. Todo ello queda en la lista de restricciones para 02.03.02. El coste del oro
sigue siendo PROVISIONAL hasta 04.01.02 (declarado en `coste_operar.md`, cabecera).

### Motivo 4 — Duda de instrumento (L-007, «front-month future») sin propagar → **ABIERTO**

**Prueba (grep ejecutado el 02/08 sobre `coste_operar.md`, `coste_relativo.md`, `coste_swap.md`,
patrones `front-month|front month|futuro|future`):** la duda existe SOLO en `coste_swap.md`,
sección `## Advertencias`, punto **2. Riesgo de instrumento — oro (L-007)** (la fórmula de
Pepperstone para «Commodities and Treasuries» referencia «front-month future» y «next-month
future»; recomienda verificar la ficha de contrato del broker en 04.01.02). En `coste_operar.md`
(que toma el spread del oro precisamente de Pepperstone Razor) y en `coste_relativo.md` (que divide
ese coste contra un ATR de oro **al contado** de Dukascopy, ver `atr_real_15m_1h_4h.md`, sección
`## Qué es EXACTAMENTE cada instrumento`): **cero menciones**. D-11 tampoco la toca (verificado:
ni «futuro» ni «L-007» aparecen en la sección D-11 de `DECISIONES.md`). La duda sigue sin propagar
a los dos documentos que usan la cifra. Corrección documental pendiente de repartir; mientras
tanto, restricción para 02.03.02.

### Motivo 5 — Coste de entrar y coste de mantener vienen de brokers y tipos de cuenta distintos en 7 de 8 instrumentos, y G1-C1 los suma → **ABIERTO — SE DECLARA Y SE ESCALA AL CEO (defecto en criterio aprobado; no se arregla ni se suaviza aquí)**

**Verificación instrumento a instrumento (fuentes localizadas):**

| Instrumento | Coste de entrar (fuente en `coste_operar.md`) | Coste de mantener (fuente en `coste_swap.md`) | ¿Mismo broker y cuenta? |
|---|---|---|---|
| EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF | IC Markets, cuenta Raw/ECN | OANDA TMS (tabla `.pro`) / XTB (tabla STANDARD) | NO |
| XAUUSD | Pepperstone Razor (raw + comisión) | OANDA TMS / XTB (Pepperstone: «sin dato fiable») | NO |
| ETHUSD | Pepperstone CFD spread-only | OANDA (única fuente fiable, hueco declarado) | NO |
| BTCUSD | Pepperstone (PDF feb-2025) | Pepperstone (Example 4 del MISMO PDF feb-2025) | SÍ (el único) |

**7 de 8, confirmado.** Y G1-C1 los suma: `DECISIONES.md`, sección D-11 — *«G1-C1 presupuesto de
coste TOTAL al año ≤5% del capital (...) con el coste de mantener DENTRO de ese mismo 5% (no
aparte)»* — con el dato de swap de G1-C3 tomado de OANDA (así consta en
`veredicto_criterios_g1.md`, ataque **A4**: «Coste de swap por noche (OANDA, largo)») y el de
entrada de IC Markets/Pepperstone.

**Agravante encontrado en esta pasada (número ejecutado, no argumento):** la «forma operativa» de
G1-C1 (WBS, sección `## Puertas`, viñeta **G1-C1**: topes de operaciones/año, a 4h «entre 126 y
426») está calculada SOLO con el coste de entrar/salir. Reproducido dígito a dígito con
`deriva_oro.py`: 5% ÷ (1% × 1,17367%) = **426,0** (XAUUSD, extremo alto publicado 426) y
5% ÷ (1% × 3,97594%) = **125,8** (AUDUSD, extremo bajo publicado 126). Es decir, el texto aprobado
mete el swap dentro del 5% pero sus topes operativos gastan el 5% entero en entrar/salir. Con el
propio dato de D-11/G1-C3 (una noche por operación ≈ +2,36% anual en XAUUSD largo, +2,28% en
EURUSD largo), el tope real por instrumento y dirección es menor que el publicado; D-11 ya declara
que dos noches en EURUSD dan 7,01% > 5%.

**Escalado que se pide (decisión del CEO, no de esta revisión):** la ficha de la puerta G1 debe
declarar que (a) el número de G1-C1 es un constructo de brokers y cuentas distintos en 7 de 8
instrumentos, no un coste contratable en ningún broker real, provisional hasta 04.01.02; y (b) los
topes 29–105 / 62–217 / 126–426 no reservan presupuesto para el swap que el propio criterio dice
incluir. El CEO decide si mantiene G1-C1 como está (con re-verificación obligatoria en 04.01.02) o
lo re-aprueba corregido. **Esta pasada no propone la corrección: la declara.**

### Motivo 6 — El deslizamiento no aparecía en ningún documento ni criterio → **CERRADO (como hueco declarado; por eso el veredicto global es «CON HUECOS DECLARADOS»)**

**Prueba (localizada por búsqueda):**
- `DECISIONES.md`, sección D-11, cierre del párrafo **Motivo**: *«Hueco declarado: el
  deslizamiento, sin factor publicado, se mide con precios del broker real en la tarea 04.01.02 y
  obliga a re-verificar G1 si algun resultado cambia»*.
- `WBS.md`, sección `## Puertas`, viñeta **HUECO DECLARADO EN G1**: mismo contenido, con la
  convención encontrada (mitad del spread más impacto) y por qué no da un número.
- La tarea receptora existe: fila `04.01.02` del WBS («Recalcular costes con precios reales del
  broker»), estado pendiente.
- Ya no es cierto que «ningún documento» lo mencione: `evidencia_umbrales_g1.md`, sección
  `## 5. Deslizamiento` (convención publicada + hueco de factor por activo/vela/hora) y
  `arrastre_coste.md`, sección `## 8. Calculo 5 — Sensibilidad al deslizamiento (declarada, no un
  dato)` (multiplicadores 1,25x/1,5x/2x declarados sin fuente, no presentados como medida).

**¿Basta?** Sí como declaración: dice qué falta, por qué (ningún factor publicado, verificado en la
sección 5 citada), cuándo se mide (04.01.02) y qué pasa si el número cambia (re-verificar G1). No
basta para un ACEPTA a secas: es exactamente lo que obliga al «CON HUECOS DECLARADOS».

### Motivo 7 — Cita mal atribuida («el coste relativo medio oculta esa cola») → **CERRADO (corregido en esta pasada, por orden expresa de la ficha)**

**Prueba:** la frase es del analista — `entrega_brief_A.md`, sección `## Lo que un experto vería
(riesgos y puntos ciegos no evidentes)`, primera viñeta. El revisor nunca la dijo: grep de
`cola|oculta` sobre `revision_brief_A.md` devuelve **cero**. Estaba atribuida a «el revisor del
Brief A» en `coste_relativo.md`, sección `## AMPLIACIÓN (31/07) — coste relativo contra la vela
tranquila (p10) y la agitada (p90)`, párrafo **Motivo**. **Corregida el 02/08** (única aparición
sustituida; verificación posterior: 0 apariciones de la atribución al revisor, la cita ahora
apunta al analista y a su sección, con nota de corrección fechada). Única edición hecha por esta
pasada, la única que la ficha ordenaba corregir.

---

## Lo que 02.03.02 PUEDE afirmar

1. **El orden de coste por vela**: por operación, 4h < 1h < 15m en los 6 no-cripto; y a 4h los 6
   no-cripto pasan G1-C2 (peor: AUDUSD 5,24% sobre p10). Robusto a la cota superior de deriva del
   oro (XAUUSD 4h: 5,43% ≤ 10% incluso con coste ×2,34).
2. **La muestra de G1-C4 a 4h**: 1.598–1.611 velas/año contadas, sobre el mínimo de 1.000.
3. **Cripto fuera de la cesta por defecto** (G1-C5: solo 1 de las 3 ventanas verificable; regla 26
   de CLAUDE.md) y ETHUSD además fuera por G1-C2 (15,13–35,37% en p10 4h).
4. **G1-C7 no lo cumple ningún instrumento**: consecuencia obligatoria (cerrar antes del viernes o
   declarar en G2 pérdida posible de hasta 4,5x el riesgo nominal) tal como está aprobada.
5. **G1-C6 como requisito al broker** (oro 4h: lote ≤0,1 oz o capital ≥2.000 EUR), no como
   eliminación.
6. Que **todo el paquete de costes es PROVISIONAL hasta 04.01.02**, incluido el deslizamiento
   (hueco declarado con disparador de re-verificación de G1).

## Lo que 02.03.02 NO PUEDE afirmar

1. **Nada con la numeración vieja** («criterio 1», «criterio 2», «criterio 4» de los entregables):
   solo G1-C1..G1-C7 de D-11, y con el umbral aprobado (G1-C2 es ≤10% sobre p10, no «10-15%»)
   — motivo 2 ABIERTO.
2. **Ningún resultado del oro a 15m o 1h sin la banda de deriva delante**: a 15m el oro deja de
   pasar la vela tranquila bajo la cota (19,80–25,46%) y a 1h rompe el 10% en la cota alta
   (11,01%) — motivo 3, consecuencia declarada.
3. **El número de G1-C1 como coste real de un broker**: es una suma de brokers y cuentas distintos
   en 7 de 8 instrumentos, escalada al CEO — motivo 5 ABIERTO. Tampoco el tope «426» como cota
   firme de XAUUSD 4h (bajo deriva sería 234/182; y ningún tope reserva presupuesto para el swap).
4. **Nada del oro sin la advertencia L-007** (el coste podría ser de un producto con componente de
   futuro y el ATR es de contado) mientras `coste_operar.md` y `coste_relativo.md` no la lleven —
   motivo 4 ABIERTO.
5. **Ningún promedio de las dos cifras de cripto** (feb-2025/abr-2026), ningún arrastre anual de
   cripto (HUECO de velas/año), y ninguna cifra de cripto como estable (`reproducible: false`,
   ventana Kraken corta de un solo régimen).
6. **El deslizamiento como coste medido**: no existe número; solo la convención y la sensibilidad
   declarada sin fuente.

---

## Pendientes que este veredicto deja repartidos (no ejecutados por el validador)

- Corregir la numeración pre-D-11 en `coste_swap.md`, `coste_relativo.md`, `correlaciones_8x8.md` y
  `evidencia_umbrales_g1.md` (motivo 2) — corrección documental, la reparte el orquestador.
- Propagar la advertencia L-007 de `coste_swap.md` a `coste_operar.md` y `coste_relativo.md`
  (motivo 4) — ídem.
- Llevar el motivo 5 (con su agravante de los topes) a la ficha del CEO de la puerta G1 —
  condición de validez de este veredicto.

*Pendiente de revisión por un agente distinto (regla 16 de CLAUDE.md): este veredicto no se
autovalida. Quien lo revise puede reproducir toda la aritmética con los valores citados de
`atr_15m_1h_4h.json` y las fórmulas de `arrastre_coste.md`, sección 4.*
