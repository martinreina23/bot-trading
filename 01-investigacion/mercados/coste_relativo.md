# Coste relativo — coste de entrar y salir ÷ ATR medio de la vela × 100

**Tarea:** 02.02.02. **Es el número que decide el criterio 1 de la puerta G1 (lunes 3 de agosto): coste de
entrar y salir ≤10-15% del movimiento medio de la vela.**

**Estado: PROVISIONAL**, hereda el estado de sus dos insumos (`coste_operar.md` es PROVISIONAL hasta 04.01.02
con precios de broker real; el ATR de cripto en `atr_15m_1h_4h.json` está marcado `reproducible: false`).

---

## Insumos (NO recalculados en esta tarea)

- **Coste de ida y vuelta:** `01-investigacion/mercados/coste_operar.md` (tarea 02.01.02, cerrada y verificada).
- **ATR:** `04-resultados/atr_15m_1h_4h.json` (tarea 02.02.01, cerrada y verificada por dos revisiones).

Ninguno de los dos se toca ni se vuelve a calcular aquí. Este documento solo divide.

## Método y la trampa de unidades

Fórmula: `coste_relativo_% = (coste_ida_y_vuelta convertido a la unidad del ATR ÷ ATR14 medio) × 100`.

El JSON de ATR guarda el ATR en **unidad CRUDA de precio**, no en pips. El coste de `coste_operar.md` está en
pips para las 6 divisas, en USD/oz para XAUUSD y en USD para BTCUSD/ETHUSD. Antes de dividir, ambos se ponen en
la misma unidad:

| Fila | Divisor de pip aplicado | Motivo |
|---|---|---|
| EURUSD, GBPUSD, AUDUSD, USDCHF | **0,0001** | 1 pip = 0,0001 en estos cuatro pares |
| USDJPY | **0,01** | 1 pip = 0,01 en JPY, cien veces mayor que en los otros pares |
| XAUUSD, BTCUSD, ETHUSD | **ninguno (1:1)** | no hay pip: coste y ATR ya están ambos en USD de precio |

**Comprobación de control (dada por el encargo, reproducida por el script):**
- EURUSD 15m: ATR crudo 0,00068642 ÷ 0,0001 = **6,86 pips** ✓ (esperado ~6,86)
- USDJPY 15m: ATR crudo 0,12025397 ÷ 0,01 = **12,03 pips** ✓ (esperado ~12,03)

Si se hubiese aplicado 0,0001 a USDJPY (el error que este encargo advertía), el ATR habría salido en 1.203
pips falsos y el coste relativo de USDJPY habría quedado dividido por 100 (parecería el mercado más barato del
mundo). El script `03-motor/scripts/coste_relativo.py` aplica el divisor por fila, según la tabla de arriba,
nunca uno único global.

---

## Tabla 8 instrumentos × 3 velas

Leyenda: **PASA ≤10%** (cumple el extremo estricto del criterio) · **PASA ≤15%** (cumple el extremo laxo, no el
estricto) · **NO PASA** (por encima de 15%, no cumple el criterio 1 de G1 en ninguna lectura).

### Divisas (Raw/ECN, coste en pips convertido con el divisor de la fila)

| Instrumento | Vela | ATR crudo | Coste (pips) | Coste en unidad ATR | Coste relativo | G1 (≤10-15%) |
|---|---|---|---|---|---|---|
| EURUSD | 15m | 0,00068642 | 0,8 | 0,00008 | **11,65%** | PASA ≤15% (no ≤10%) |
| EURUSD | 1h | 0,00140738 | 0,8 | 0,00008 | **5,68%** | **PASA ≤10%** |
| EURUSD | 4h | 0,00285011 | 0,8 | 0,00008 | **2,81%** | **PASA ≤10%** |
| GBPUSD | 15m | 0,00082751 | 0,82 | 0,000082 | **9,91%** | **PASA ≤10%** |
| GBPUSD | 1h | 0,00169472 | 0,82 | 0,000082 | **4,84%** | **PASA ≤10%** |
| GBPUSD | 4h | 0,00341386 | 0,82 | 0,000082 | **2,40%** | **PASA ≤10%** |
| USDJPY | 15m | 0,12025397 | 1,16 | 0,0116 | **9,65%** | **PASA ≤10%** |
| USDJPY | 1h | 0,24859555 | 1,16 | 0,0116 | **4,67%** | **PASA ≤10%** |
| USDJPY | 4h | 0,50730948 | 1,16 | 0,0116 | **2,29%** | **PASA ≤10%** |
| AUDUSD | 15m | 0,00055918 | 0,85 | 0,000085 | **15,20%** | NO PASA (>15%) |
| AUDUSD | 1h | 0,00114800 | 0,85 | 0,000085 | **7,40%** | **PASA ≤10%** |
| AUDUSD | 4h | 0,00232403 | 0,85 | 0,000085 | **3,66%** | **PASA ≤10%** |
| USDCHF | 15m | 0,00057203 | 0,73 | 0,000073 | **12,76%** | PASA ≤15% (no ≤10%) |
| USDCHF | 1h | 0,00117390 | 0,73 | 0,000073 | **6,22%** | **PASA ≤10%** |
| USDCHF | 4h | 0,00238760 | 0,73 | 0,000073 | **3,06%** | **PASA ≤10%** |

### Oro (Raw/ECN, coste y ATR ya en USD/oz, sin conversión)

| Instrumento | Vela | ATR crudo (USD/oz) | Coste (USD/oz) | Coste relativo | G1 (≤10-15%) |
|---|---|---|---|---|---|
| XAUUSD | 15m | 7,0645 | 0,26 | **3,68%** | **PASA ≤10%** |
| XAUUSD | 1h | 14,4647 | 0,26 | **1,80%** | **PASA ≤10%** |
| XAUUSD | 4h | 28,4289 | 0,26 | **0,92%** | **PASA ≤10%** |

### Cripto (CFD spread-only, coste y ATR ya en USD, sin conversión) — DOS ratios por celda, sin promediar

| Instrumento | Vela | ATR crudo (USD) | Coste feb-2025 (USD) | Ratio feb-2025 | Coste abr-2026 (USD) | Ratio abr-2026 | G1 (≤10-15%) |
|---|---|---|---|---|---|---|---|
| BTCUSD | 15m | 123,928 | 20,22 | **16,32%** | 36,90 | **29,78%** | NO PASA (ninguna de las dos) |
| BTCUSD | 1h | 298,694 | 20,22 | **6,77%** | 36,90 | **12,35%** | feb-2025 PASA ≤10%; abr-2026 PASA ≤15% (no ≤10%) |
| BTCUSD | 4h | 809,133 | 20,22 | **2,50%** | 36,90 | **4,56%** | **ambas PASAN ≤10%** |
| ETHUSD | 15m | 5,452 | 3,01 | **55,21%** | 7,04 | **129,12%** | NO PASA (ninguna de las dos) |
| ETHUSD | 1h | 12,248 | 3,01 | **24,58%** | 7,04 | **57,48%** | NO PASA (ninguna de las dos) |
| ETHUSD | 4h | 30,968 | 3,01 | **9,72%** | 7,04 | **22,73%** | feb-2025 PASA ≤10%; abr-2026 NO PASA |

**Prohibido promediar las dos cifras de cripto** (dos fuentes primarias, fechas distintas: feb-2025 y
abr-2026): no lo publica nadie y este documento no lo inventa.

---

## CORRECCIÓN (31/07) — sesgo del ATR medio en XAUUSD: la tabla de arriba usa una media inflada

**`critico-codigo` rechazó esta tarea, no por un error de cálculo (el JSON reejecutado sale bit-idéntico), sino
por un sesgo de método que la primera versión de este informe no nombraba donde el CEO lo va a leer.**

**El hallazgo, con la prueba que lo zanja.** El ratio ATR14 medio ÷ ATR14 mediana de XAUUSD es **1,299 / 1,282 /
1,283** (15m / 1h / 4h) — muy por encima de los otros 7 instrumentos, cuyo ratio va de **0,985 a 1,144**. Ninguno
se acerca al del oro. La causa está documentada en el propio informe de 02.02.01 (sección Dukascopy): **el oro al
contado tiene una pausa diaria real hacia las 21:00-22:00 UTC**, que genera un salto de rango **una vez al día**,
frente a una vez por semana en forex y nunca en cripto. Ese salto diario infla la **media** y apenas mueve la
**mediana**. Consecuencia directa: la columna `atr14_medio` de la tabla de arriba **no es un objeto estadístico
equivalente** entre XAUUSD y el resto, y la ventaja de coste del oro que esa tabla muestra (calculada contra esa
media) **está más inflada que la de ningún otro instrumento** de los 8.

**Lo segundo, igual de importante que lo primero: recalculando las 18 celdas de divisa y oro contra
`atr14_mediana` (tabla siguiente) el orden no cambia en ninguna de las tres velas.** XAUUSD sigue siendo el
instrumento más barato de los 6 (divisas + oro) en 15m, 1h y 4h. Lo que cambia es el margen, no el ganador: la
ventaja de XAUUSD sobre el segundo más barato (USDJPY) pasa de **2,62x a 2,23x en 15m**, de 2,60x a 2,18x en 1h y
de 2,50x a 2,05x en 4h, al pasar de la media a la mediana. El oro sigue siendo "el más barato con diferencia" de
la sección Resumen (más abajo); esa diferencia es real pero menor de lo que sugiere la columna `atr14_medio`
tomada sola.

### Tabla — coste relativo contra ATR MEDIANA (divisas, oro y cripto)

Misma fórmula, mismos costes y divisores de pip que en la tabla de la vela media; único cambio: el denominador es
`atr14_mediana` (ya presente en `04-resultados/atr_15m_1h_4h.json` desde 02.02.01, no recalculado). Columna
"Mult. mediana÷media" = `coste_relativo_%(mediana) ÷ coste_relativo_%(media)`, igual al inverso del ratio
medio/mediana del ATR de la sección de arriba.

**Divisas y oro (Raw/ECN)**

| Instrumento | Vela | ATR mediana crudo | Coste relativo (mediana) | Mult. mediana÷media | G1 (≤10-15%) |
|---|---|---|---|---|---|
| XAUUSD | 15m | 5,4386 | **4,78%** | 1,30x | **PASA ≤10%** |
| XAUUSD | 1h | 11,2797 | **2,31%** | 1,28x | **PASA ≤10%** |
| XAUUSD | 4h | 22,1527 | **1,17%** | 1,28x | **PASA ≤10%** |
| USDJPY | 15m | 0,10864286 | **10,68%** | 1,11x | PASA ≤15% (no ≤10%) |
| USDJPY | 1h | 0,23050000 | **5,03%** | 1,08x | **PASA ≤10%** |
| USDJPY | 4h | 0,48264286 | **2,40%** | 1,05x | **PASA ≤10%** |
| GBPUSD | 15m | 0,00075429 | **10,87%** | 1,10x | PASA ≤15% (no ≤10%) |
| GBPUSD | 1h | 0,00159857 | **5,13%** | 1,06x | **PASA ≤10%** |
| GBPUSD | 4h | 0,00322857 | **2,54%** | 1,06x | **PASA ≤10%** |
| EURUSD | 15m | 0,00060000 | **13,33%** | 1,14x | PASA ≤15% (no ≤10%) |
| EURUSD | 1h | 0,00128071 | **6,25%** | 1,10x | **PASA ≤10%** |
| EURUSD | 4h | 0,00263214 | **3,04%** | 1,08x | **PASA ≤10%** |
| USDCHF | 15m | 0,00050500 | **14,46%** | 1,13x | PASA ≤15% (no ≤10%) |
| USDCHF | 1h | 0,00106571 | **6,85%** | 1,10x | **PASA ≤10%** |
| USDCHF | 4h | 0,00218000 | **3,35%** | 1,10x | **PASA ≤10%** |
| AUDUSD | 15m | 0,00049929 | **17,02%** | 1,12x | NO PASA (>15%) |
| AUDUSD | 1h | 0,00104964 | **8,10%** | 1,09x | **PASA ≤10%** |
| AUDUSD | 4h | 0,00213786 | **3,98%** | 1,09x | **PASA ≤10%** |

**Cripto (CFD spread-only) — hereda `reproducible: false`, ver sección siguiente sobre el tipo de estimador; dos
ratios por celda, sin promediar**

| Instrumento | Vela | ATR mediana crudo (USD) | Ratio feb-2025 (mediana) | Ratio abr-2026 (mediana) | Mult. mediana÷media | G1 (≤10-15%) |
|---|---|---|---|---|---|---|
| BTCUSD | 15m | 110,664 | **18,27%** | **33,34%** | 1,12x | NO PASA (ninguna) |
| BTCUSD | 1h | 303,114 | **6,67%** | **12,17%** | 0,99x | feb-2025 PASA ≤10%; abr-2026 PASA ≤15% (no ≤10%) |
| BTCUSD | 4h | 779,264 | **2,60%** | **4,74%** | 1,04x | **ambas PASAN ≤10%** |
| ETHUSD | 15m | 4,946 | **60,85%** | **142,32%** | 1,10x | NO PASA (ninguna) |
| ETHUSD | 1h | 12,334 | **24,41%** | **57,08%** | 0,99x | NO PASA (ninguna) |
| ETHUSD | 4h | 30,312 | **9,93%** | **23,23%** | 1,02x | feb-2025 PASA ≤10%; abr-2026 NO PASA |

**Confirmación de reproducción del hallazgo del crítico:** el ratio ATR14 medio ÷ ATR14 mediana calculado por
instrumento (mismo cálculo que sustenta esta corrección) es EURUSD 1,144/1,099/1,083 · GBPUSD 1,097/1,060/1,057 ·
USDJPY 1,107/1,079/1,051 · AUDUSD 1,120/1,094/1,087 · USDCHF 1,133/1,102/1,095 · **XAUUSD 1,299/1,282/1,283** ·
BTCUSD 1,120/0,985/1,038 · ETHUSD 1,102/0,993/1,022 (15m/1h/4h). Coincide dígito a dígito con las cifras del
crítico reproducidas por el orquestador.

---

## Herencia de la limitación del ATR de cripto (declaración obligatoria)

Las **6 celdas de BTCUSD y ETHUSD** (15m, 1h, 4h × 2 instrumentos) usan un ATR marcado
`"reproducible": false` en `04-resultados/atr_15m_1h_4h.json`, con motivo documentado ahí: el endpoint público
de Kraken solo sirve las ~720 velas cerradas más recientes de cada intervalo y la ventana se desplaza en cada
ejecución, así que reejecutar la descarga más allá del ancho de esa ventana (7,4 días en 15m, 30 en 1h, 120 en
4h) no comparte ni una vela con la ejecución anterior.

**El coste relativo de esas 6 celdas hereda exactamente esa limitación.** No es solo el ATR el que no es
reproducible: el cociente completo (coste relativo en %) tampoco lo es, porque su denominador cambia si se
recalcula el ATR en otro momento. Estas 12 ratios (6 celdas × 2 fechas de coste) son una fotografía del
31/07/2026, no un número estable. No deben usarse en el testbed de invarianza de 03.01.10 sin congelar antes
los datos de origen (misma condición que ya declaró 02.02.01).

**Corrección (31/07, señalada por `critico-codigo`): "no reproducible" no es la única limitación de cripto, y
no es del mismo tipo que las de divisas y oro.** Decir solo "no reproducible" sugiere que el ATR de cripto es
un estimador igual de válido que el de las 18 celdas restantes, solo que inestable de una ejecución a otra. No
es así: son **dos tipos de estimador distintos**. Las 18 celdas de divisas y oro se calculan sobre
**~700 días** de historia (2024-07-29 a 2026-06/07, ver `desde_utc`/`hasta_utc` en el JSON de 02.02.01), un
tramo que cruza varios regímenes de mercado (tramos de alta y baja volatilidad, distintas fases de tipos de
interés, etc.). Las 6 celdas de cripto se calculan sobre la ventana que sirve el endpoint público de Kraken en
el momento de la descarga: **7,4 días en 15m, 30 días en 1h, 120 días en 4h**, un único tramo reciente, no
representativo de otros regímenes. No es "uno estable y otro inestable": es "uno mide un objeto de ~700 días
multi-régimen y el otro mide un objeto de 7,4-120 días de un único régimen", y esa diferencia de naturaleza
existiría aunque la ventana de Kraken fuese, por casualidad, reproducible.

**Ejemplo de por qué esto importa, no solo en teoría:** ETHUSD 15m con el coste de abr-2026 sale **129,12%**
(tabla de arriba). Esa cifra depende enteramente de que la ventana de 7,4 días capturada el 31/07/2026 tuviera
un ATR bajo; una ventana de 7,4 días distinta, de otro régimen de volatilidad de ETH, habría dado un
`atr14_medio` distinto y por tanto un coste relativo distinto — no porque el mercado haya cambiado, sino porque
la muestra es corta y de un solo tramo. Una cifra calculada sobre ~700 días (como las 18 celdas de divisas y
oro) no tiene esa fragilidad frente a en qué momento se ejecuta la descarga: el peso de un solo día o de una
sola semana rara es marginal sobre 700 días; sobre 7,4 días es casi todo el dato.

Las 18 celdas restantes (las 5 divisas y el oro, 6 instrumentos × 3 velas) sí llevan `reproducible: true`
heredado del ATR y no tienen ninguna de las dos limitaciones (ni la de reproducibilidad ni la de ser un
estimador de una ventana corta y de un solo régimen).

---

## Comparabilidad

- Solo se compara **Raw/ECN con Raw/ECN**: las 5 divisas y el oro usan tipo de cuenta Raw/ECN; BTCUSD y ETHUSD
  usan CFD spread-only (única modalidad documentada por la fuente para cripto en `coste_operar.md`). La columna
  "Spread-only de referencia" de `coste_operar.md` **no entra en esta tabla**, tal como exige ese documento
  ("NO comparable, NO sumar").
- Los ratios de cripto (CFD spread-only) por tanto **no son directamente comparables en tipo de cuenta** con
  los de divisas y oro (Raw/ECN); se presentan en tablas separadas para dejarlo visible, no en una única mezcla.

---

## Prueba de cordura obligatoria

**Regla:** ningún coste relativo de **divisa** (EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF) puede superar el 100%;
si sale, hay un divisor mal puesto.

**Resultado ejecutado:** `OK: True`. El máximo de las 15 celdas de divisas es AUDUSD 15m con 15,20%, muy por
debajo de 100%. Ningún divisor mal puesto. (XAUUSD y cripto no están sujetos a esta prueba concreta porque no
tienen pip que invertir; su propio control es la comprobación de unidad 1:1 con el ATR, que también se cumple:
ambos vienen en USD de precio en la fuente).

---

## Resumen: qué pasa el criterio 1 de G1 (≤10-15%) y qué no

**Pasan con margen amplio (≤10% en las tres velas):** USDJPY (9,65% / 4,67% / 2,29%), GBPUSD (9,91% / 4,84% /
2,40%), USDCHF en 1h y 4h, XAUUSD (3,68% / 1,80% / 0,92%, el más barato con diferencia).

**Pasan solo en algunas velas:** EURUSD (falla en 15m con 11,65%, pasa por debajo de 15% ahí, pasa cómodo en
1h/4h). AUDUSD (falla en 15m con 15,20%, justo por encima del extremo laxo; pasa en 1h/4h). USDCHF (12,76% en
15m, dentro del extremo laxo pero no del estricto; pasa en 1h/4h).

**Oro:** pasa en las tres velas con mucho margen.

**Cripto — heredan la limitación de reproducibilidad y tienen dos cifras sin promediar:**
- BTCUSD: NO pasa en 15m (16,32% / 29,78%). En 1h, la cifra feb-2025 pasa el extremo estricto (6,77%) pero la
  de abr-2026 solo el laxo (12,35%). En 4h pasan ambas cifras con margen (2,50% / 4,56%).
- ETHUSD: NO pasa en 15m ni en 1h con ninguna de las dos cifras. En 4h, la cifra feb-2025 pasa el extremo
  estricto (9,72%) pero la de abr-2026 (22,73%) no pasa en absoluto.

**Conclusión operativa para G1:** en vela de 15 minutos, ningún instrumento cripto cumple el criterio 1 con
ninguna de las dos fechas de coste, y dos de las cinco divisas (AUDUSD, y USDCHF/EURUSD en el extremo estricto)
quedan al límite. En 1h y 4h, todas las divisas y el oro cumplen con margen; la cripto solo cumple en 4h y,
para ETHUSD, únicamente con el coste de feb-2025 (la cifra más reciente de abr-2026 no pasa ni en 4h).

**AVISO — este resumen usa solo el ATR MEDIO.** Un bot no opera la vela media: opera todas, incluidas las
tranquilas. La sección "AMPLIACIÓN" más abajo repite este mismo ejercicio contra `atr14_p10` (vela tranquila)
y `atr14_p90` (vela agitada); en 15m el cuadro cambia bastante: con ATR p10, de las 5 divisas + oro que pasaban
arriba, **solo el oro sigue pasando**. Léase la ampliación antes de usar este resumen para decidir nada en G1.

**AVISO 2 (31/07) — "el más barato con diferencia" es correcto pero la diferencia es menor de lo que sugiere
la media.** Ver la sección "CORRECCIÓN (31/07) — sesgo del ATR medio en XAUUSD", justo después de la tabla
principal: el ATR medio de XAUUSD está más inflado que el de cualquier otro instrumento por la pausa diaria del
oro, y contra `atr14_mediana` la ventaja de XAUUSD sobre el segundo más barato baja de ~2,6x a ~2,2x (sigue
siendo el más barato en las tres velas, el orden no cambia).

---

## AMPLIACIÓN (31/07) — coste relativo contra la vela tranquila (p10) y la agitada (p90)

**Motivo:** el analista del Brief A avisó en `entrega_brief_A.md`, sección "Lo que un experto vería (riesgos y puntos ciegos no evidentes)", de que "el coste relativo medio oculta esa cola" (atribución corregida el 02/08 por la revisión 02.03.01: la frase es del analista, no del revisor) y la lección **L-008**
dice que un umbral sobre una magnitud inestable necesita más de un número. La tabla anterior divide el coste
entre el ATR **medio**, pero un bot no opera la vela media: opera todas, incluidas las tranquilas, que son
justo las que más penalizan un coste fijo (spread) frente a un movimiento pequeño.

**Dato ya existente, no recalculado:** `04-resultados/atr_15m_1h_4h.json` (tarea 02.02.01) trae, además de
`atr14_medio`, los percentiles `atr14_p10` (vela tranquila, una de cada diez) y `atr14_p90` (vela agitada, una
de cada diez), calculados sobre la misma serie y con el mismo corte de 22:00 UTC. Este documento solo divide,
igual que en la tabla de la vela media: mismos costes de `coste_operar.md`, mismos divisores de pip por fila
(0,0001 para EUR/GBP/AUD/CHF, 0,01 para JPY, sin divisor para oro y cripto).

**Multiplicador (columna nueva):** se define como `coste_relativo_%(p10) ÷ coste_relativo_%(media)`, que es
matemáticamente igual a `atr14_medio ÷ atr14_p10` (el coste es el mismo numerador en las dos fracciones, así
que el cociente de los dos ratios es el cociente inverso de los ATR). Un multiplicador de 2,0x significa que en
la vela tranquila el coste pesa el doble de lo que pesa en la vela media. Se calcula igual para p90
(`coste_relativo_%(p90) ÷ coste_relativo_%(media)`), que siempre sale por debajo de 1 porque el denominador
crece.

Los números de la tabla de la vela media (arriba) **no se han tocado**: se verificó por relectura del JSON que
`coste_relativo_pct` de la clave `"ratios"` es bit-idéntico al ya entregado (ejemplo: EURUSD 15m
`11.65467145838654`, USDJPY 4h `2.2865726983374417`).

### Tabla — coste relativo contra ATR p10 (vela TRANQUILA, una de cada diez)

Este es el escenario que un bot que opera "todas las velas" sufre una de cada diez veces, no una rareza.

**Divisas (Raw/ECN)**

| Instrumento | Vela | ATR p10 crudo | Coste (pips) | Coste relativo en p10 | Multiplicador p10÷media | G1 (≤10-15%) |
|---|---|---|---|---|---|---|
| EURUSD | 15m | 0,00032214 | 0,8 | **24,83%** | 2,13x | NO PASA |
| EURUSD | 1h | 0,00081786 | 0,8 | **9,78%** | 1,72x | **PASA ≤10%** |
| EURUSD | 4h | 0,00185400 | 0,8 | **4,32%** | 1,54x | **PASA ≤10%** |
| GBPUSD | 15m | 0,00042500 | 0,82 | **19,29%** | 1,95x | NO PASA |
| GBPUSD | 1h | 0,00108071 | 0,82 | **7,59%** | 1,57x | **PASA ≤10%** |
| GBPUSD | 4h | 0,00254314 | 0,82 | **3,22%** | 1,34x | **PASA ≤10%** |
| USDJPY | 15m | 0,05685714 | 1,16 | **20,40%** | 2,12x | NO PASA |
| USDJPY | 1h | 0,14078571 | 1,16 | **8,24%** | 1,77x | **PASA ≤10%** |
| USDJPY | 4h | 0,30220714 | 1,16 | **3,84%** | 1,68x | **PASA ≤10%** |
| AUDUSD | 15m | 0,00032071 | 0,85 | **26,50%** | 1,74x | NO PASA |
| AUDUSD | 1h | 0,00075786 | 0,85 | **11,22%** | 1,51x | PASA ≤15% (no ≤10%) |
| AUDUSD | 4h | 0,00162357 | 0,85 | **5,24%** | 1,43x | **PASA ≤10%** |
| USDCHF | 15m | 0,00029429 | 0,73 | **24,81%** | 1,94x | NO PASA |
| USDCHF | 1h | 0,00073043 | 0,73 | **9,99%** | 1,61x | **PASA ≤10%** |
| USDCHF | 4h | 0,00166950 | 0,73 | **4,37%** | 1,43x | **PASA ≤10%** |

**Oro (Raw/ECN)**

| Instrumento | Vela | ATR p10 crudo (USD/oz) | Coste (USD/oz) | Coste relativo en p10 | Multiplicador p10÷media | G1 (≤10-15%) |
|---|---|---|---|---|---|---|
| XAUUSD | 15m | 2,3893 | 0,26 | **10,88%** | **2,96x** | PASA ≤15% (no ≤10%) |
| XAUUSD | 1h | 5,5256 | 0,26 | **4,71%** | 2,62x | **PASA ≤10%** |
| XAUUSD | 4h | 11,2099 | 0,26 | **2,32%** | 2,54x | **PASA ≤10%** |

**Cripto (CFD spread-only) — arrastran `reproducible: false` heredado de 02.02.01; dos ratios sin promediar**

| Instrumento | Vela | ATR p10 crudo (USD) | Ratio feb-2025 | Mult. feb-2025 | Ratio abr-2026 | Mult. abr-2026 | G1 (≤10-15%) |
|---|---|---|---|---|---|---|---|
| BTCUSD | 15m | 48,923 | **41,33%** | 2,53x | **75,42%** | 2,53x | NO PASA (ninguna) |
| BTCUSD | 1h | 150,493 | **13,44%** | 1,98x | **24,52%** | 1,98x | feb-2025 PASA ≤15% (no ≤10%); abr-2026 NO PASA |
| BTCUSD | 4h | 527,799 | **3,83%** | 1,53x | **6,99%** | 1,53x | **ambas PASAN ≤10%** |
| ETHUSD | 15m | 2,279 | **132,06%** | 2,39x | **308,87%** | 2,39x | NO PASA (ninguna) |
| ETHUSD | 1h | 7,438 | **40,47%** | 1,65x | **94,64%** | 1,65x | NO PASA (ninguna) |
| ETHUSD | 4h | 19,901 | **15,13%** | 1,56x | **35,37%** | 1,56x | NO PASA (ninguna) — feb-2025 se queda a 0,13 puntos de PASA ≤15% |

### Tabla — coste relativo contra ATR p90 (vela AGITADA, una de cada diez) — MEJOR CASO, no el típico

**Se incluye como referencia del extremo favorable. No es el caso representativo: solo una vela de cada diez
es tan agitada como esta.** El multiplicador p90÷media siempre es menor que 1 porque el ATR crece.

**Divisas y oro (Raw/ECN)**

| Instrumento | Vela | ATR p90 crudo | Coste relativo en p90 | Multiplicador p90÷media | G1 (≤10-15%) |
|---|---|---|---|---|---|
| EURUSD | 15m | 0,00113929 | **7,02%** | 0,60x | **PASA ≤10%** |
| EURUSD | 1h | 0,00211214 | **3,79%** | 0,67x | **PASA ≤10%** |
| EURUSD | 4h | 0,00402464 | **1,99%** | 0,71x | **PASA ≤10%** |
| GBPUSD | 15m | 0,00130714 | **6,27%** | 0,63x | **PASA ≤10%** |
| GBPUSD | 1h | 0,00239657 | **3,42%** | 0,71x | **PASA ≤10%** |
| GBPUSD | 4h | 0,00452829 | **1,81%** | 0,75x | **PASA ≤10%** |
| USDJPY | 15m | 0,19177857 | **6,05%** | 0,63x | **PASA ≤10%** |
| USDJPY | 1h | 0,36665714 | **3,16%** | 0,68x | **PASA ≤10%** |
| USDJPY | 4h | 0,72242857 | **1,61%** | 0,70x | **PASA ≤10%** |
| AUDUSD | 15m | 0,00084929 | **10,01%** | 0,66x | PASA ≤15% (no ≤10%, al límite) |
| AUDUSD | 1h | 0,00159714 | **5,32%** | 0,72x | **PASA ≤10%** |
| AUDUSD | 4h | 0,00316429 | **2,69%** | 0,73x | **PASA ≤10%** |
| USDCHF | 15m | 0,00091857 | **7,95%** | 0,62x | **PASA ≤10%** |
| USDCHF | 1h | 0,00169857 | **4,30%** | 0,69x | **PASA ≤10%** |
| USDCHF | 4h | 0,00323629 | **2,26%** | 0,74x | **PASA ≤10%** |
| XAUUSD | 15m | 12,9690 | **2,00%** | 0,54x | **PASA ≤10%** |
| XAUUSD | 1h | 25,4719 | **1,02%** | 0,57x | **PASA ≤10%** |
| XAUUSD | 4h | 48,7731 | **0,53%** | 0,58x | **PASA ≤10%** |

**Cripto (CFD spread-only, `reproducible: false`)**

| Instrumento | Vela | Ratio feb-2025 p90 | Ratio abr-2026 p90 | G1 (≤10-15%) |
|---|---|---|---|---|
| BTCUSD | 15m | **9,41%** | **17,16%** | feb-2025 PASA ≤10%; abr-2026 NO PASA |
| BTCUSD | 1h/4h | ambas PASAN ≤10% | ambas PASAN ≤10% | **PASA** |
| ETHUSD | 15m | **34,73%** | **81,23%** | NO PASA (ninguna) |
| ETHUSD | 1h | **18,04%** | **42,19%** | NO PASA (ninguna) |
| ETHUSD | 4h | **6,96%** | **16,27%** | feb-2025 PASA ≤10%; abr-2026 NO PASA |

---

## EL HALLAZGO (contrastado contra las cifras dadas por el encargo de ampliación)

**Contraste ejecutado dígito a dígito contra las 6 cifras de control del encargo: TODAS COINCIDEN.**

| Cifra de control del encargo | Mi cálculo | ¿Coincide? |
|---|---|---|
| EURUSD 15m p10 = 24,83% | 24,834% | Sí |
| USDCHF 15m p10 = 24,81% | 24,806% | Sí |
| AUDUSD 15m p10 = 26,50% | 26,503% | Sí |
| USDJPY 15m p10 = 20,40% | 20,402% | Sí |
| GBPUSD 15m p10 = 19,29% | 19,294% | Sí |
| XAUUSD 15m p10 = 10,88% (único que pasa) | 10,882% | Sí |

- **Vela MEDIA a 15m: pasan 5 de 6 instrumentos el umbral del 15%** (EURUSD 11,65%, GBPUSD 9,91%, USDJPY
  9,65%, USDCHF 12,76%, XAUUSD 3,68% pasan; AUDUSD 15,20% NO pasa, por 0,20 puntos). Confirmado.
- **Vela TRANQUILA (p10) a 15m: solo pasa el oro** (10,88%, y solo por el extremo laxo ≤15%, no por el
  estricto ≤10%). Las cinco divisas fallan: EURUSD 24,83%, USDCHF 24,81%, AUDUSD 26,50%, USDJPY 20,40%, GBPUSD
  19,29%. Confirmado.
- **A 1h y 4h, los 6 instrumentos aguantan incluso en p10** (el peor caso en esas velas es AUDUSD 1h con
  11,22%, que pasa el extremo laxo ≤15% pero no el estricto ≤10%; el resto pasa ≤10% con margen). Confirmado.
- **El multiplicador (coste relativo en p10 ÷ coste relativo en media) va de 1,3x a 3,0x** en las 18 celdas de
  divisas y oro: mínimo 1,34x (GBPUSD 4h), máximo 2,96x (XAUUSD 15m). **El más alto es el del oro (2,54x a
  2,96x en sus tres velas)**: su ventaja de coste se estrecha más que la de nadie cuando el mercado está
  parado, aunque en términos absolutos sigue siendo el más barato de los seis en las tres lecturas (media, p10
  y p90). Confirmado.

No hay ninguna discrepancia entre mi cálculo y las cifras de control del encargo: no hace falta parar ni
avisar de un error, los dos cálculos son el mismo número.

### Extensión a cripto (con la limitación de `reproducible: false` heredada)

El multiplicador p10÷media también aplica a BTCUSD y ETHUSD, calculado igual que en divisas y oro pero
recordando que **estas 6 celdas (2 instrumentos × 3 velas) heredan `reproducible: false`** del ATR de
02.02.01: el multiplicador y los ratios en p10/p90 son una fotografía del 31/07/2026, no un número estable, por
el mismo motivo ya declarado en la sección "Herencia de la limitación del ATR de cripto" (más abajo).
Rango de multiplicador en cripto: 1,53x (BTCUSD 4h) a 2,53x (BTCUSD 15m) para BTCUSD, y 1,56x (ETHUSD 4h) a
2,39x (ETHUSD 15m) para ETHUSD — dentro del mismo rango 1,3x-3,0x que divisas y oro, sin superar al oro como
máximo.

**Nota de comparabilidad:** esta comparación de multiplicador entre cripto (CFD spread-only) y divisas/oro
(Raw/ECN) es lícita aunque el resto de este documento insista en que esos dos tipos de cuenta no se mezclan: el
multiplicador es un cociente **adimensional** (coste_relativo_% ÷ coste_relativo_%) que no depende del coste
absoluto ni, por tanto, del tipo de cuenta que fija ese coste. Lo que sigue sin ser comparable entre cripto y
divisas/oro son los **ratios en valor absoluto** (ver "Comparabilidad" más arriba), no el multiplicador.

---

## Reproducción

Script: `03-motor/scripts/coste_relativo.py` (no toca `precios_mercado.py` ni `atr_15m_1h_4h.json`). Ejecutado
con `.venv/bin/python 03-motor/scripts/coste_relativo.py`, salida completa leída antes de escribir este
informe (incluida la ampliación de p10/p90 y la corrección de mediana del 31/07). Volcado numérico completo
(todas las celdas, cuatro escenarios —media, mediana, p10, p90—, ambas cifras de cripto, flags de
`reproducible`, `ratio_medio_vs_mediana_atr` y `multiplicador_vs_media` por celda):
`04-resultados/coste_relativo_15m_1h_4h.json`.

---

## Conclusión de la ampliación, sin recomendar mercado (elegir es de la puerta G1, no de esta tarea)

**En 1h y 4h, las 18 celdas de divisas y oro pasan el umbral de G1 tanto en el escenario típico (media) como en
el desfavorable (p10, vela tranquila). En 15m pasan 5 de 6 en el escenario típico (todas menos AUDUSD) pero
solo 1 de 6 (XAUUSD, y solo por el extremo laxo ≤15%) sigue pasando en el desfavorable: EURUSD, GBPUSD, USDJPY
y USDCHF pasan en media pero dejan de pasar en p10; AUDUSD no pasa en ninguno de los dos escenarios de 15m.**
Esto es un hecho leído de la tabla, no una recomendación de mercado ni de vela.

---

## Estado y siguiente paso

**No se cierra esta tarea en el WBS desde este informe** (regla 16 de CLAUDE.md: quien construye no valida su propio
trabajo). Pendiente de revisión independiente antes de que el orquestador la dé por hecha. El número que
decide G1 el lunes 3 de agosto está calculado y declarado, ahora con la vela típica, la mediana y la tranquila;
el veredicto de qué mercados y qué vela pasan a 02.03.02 corresponde al orquestador y, finalmente, al CEO en
02.03.03.

**31/07 — corrección tras rechazo de `critico-codigo`:** se añadió la tabla contra `atr14_mediana`, el párrafo
de sesgo junto a la tabla principal, la distinción de tipo de estimador para cripto (no solo "no reproducible")
y la nota de comparabilidad del multiplicador. Ningún número de las tablas de media/p10/p90 ya entregadas se
tocó (verificado: mismos valores, ver sección "AMPLIACIÓN"). Sigue pendiente de revisión independiente antes de
cerrarse.
