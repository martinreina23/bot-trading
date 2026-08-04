# Revisión de la especificación del motor de backtest — Tarea 04.03.06

**Revisor:** `constructor-datos` (`claude-sonnet-5`) · **Fecha:** 03/08/2026
**Autor revisado:** `arquitecto` (`claude-fable-5`, sin respaldo)
**Artefacto revisado:** `03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`
**Regla 16 de CLAUDE.md:** cumplida — el revisor no construyó ni escribió la especificación; no revisa
su propio trabajo. El revisor es la persona que midió los ficheros de costes que la especificación
tiene que honrar (`01-investigacion/mercados/coste_swap.md`, `coste_operar.md`, `coste_relativo.md`
son de `investigador`/02.02.05; el JSON `04-resultados/atr_15m_1h_4h.json` es de `constructor-datos`/02.02.01).
**Congelación respetada:** ningún `git commit`/`checkout`/`stash`/`restore`, ningún paquete instalado.
Toda ejecución se hizo sobre una copia defensiva en
`/tmp/claude-1000/.../scratchpad/04.03.06/` y con un script Python de solo lectura/aritmética.
**Prohibido y no hecho:** no se juzga rentabilidad, PnL, Sharpe ni ninguna métrica de resultado (reglas
17 y 18 de CLAUDE.md); esta revisión juzga solo fidelidad a la especificación.

## VEREDICTO GLOBAL: **RECHAZA** (parcial — un solo defecto puntual, fácil de corregir)

Los cuatro primeros puntos pasan limpio. El quinto (los tres eliminatorios) también pasa. El
**punto 4** encuentra un requisito real, R-06(c), cuya prueba de aceptación está escrita como
"Revisión del revisor" — una revisión manual, no un comando ejecutable — lo que incumple
literalmente el criterio de hecho de la propia ficha 04.03.06: *"cada requisito tiene su prueba de
aceptación ejecutable al lado; un requisito sin prueba ejecutable no es un requisito"*. No es un
fallo de fondo (la mecánica, la aritmética y las citas son correctas), pero deja un hueco de
no-ambigüedad (regla 6 de CLAUDE.md) que corresponde cerrar antes de que 04.03.07 empiece a
construir contra este documento, para que el constructor y su revisor no tengan que interpretar
cuándo "una sola función" cuenta como una. Se detalla en el punto 4. Recomendación: sustituir R-06(c)
por un comando ejecutable concreto (p. ej. un conteo de definiciones de función por nombre de símbolo
con `grep -c` o `ast`) y volver a presentar. No se requiere tocar nada más del documento.

---

## PUNTO 1 — Hueco H-7: fila T2 del historial de git

La ficha 04.03.06 ordenaba `git show HEAD:00-direccion/WBS.md` para leer la fila T2 de la sección
«Trasplante desde gb2 — criterios de aceptación». `arquitecto` tiene solo `Read, Grep, Glob` (sin
terminal): la orden era imposible de cumplir para él, lo declaró como hueco H-7 y no lo rellenó. Yo
sí tengo terminal. Confirmado primero que la sección ya no vive en el WBS de disco (la borró la
cirugía de D-21 el 03/08):

```
$ grep -n "Trasplante desde gb2" /home/server/projects/bot-trading/00-direccion/WBS.md
(sin resultado)
$ grep -c "T2 — Motor de backtest" /home/server/projects/bot-trading/00-direccion/WBS.md
0
```

Ejecutado `git show HEAD:00-direccion/WBS.md` y localizada la fila T2 en el historial:

```
$ git show HEAD:00-direccion/WBS.md | grep -n "T2 — Motor de backtest"
253:| **T2 — Motor de backtest** | Costes reales nativos: entrada al precio de compra y salida al de
venta, stops sin mejora de precio, financiación asimétrica con triple miércoles, dimensionado | Se
ejecuta con un caso hecho a mano cuyo resultado se calcula con lápiz y papel; si no coincide, no
entra. Además se prueba que un stop nunca ejecuta a mejor precio del disparado | Los drivers
duplicados (`scripts/backtest_f03*.py`): en gb2 la lógica vivía en dos sitios con riesgo de
divergencia |
```

**Texto real de la columna "Qué se trae" (los cuatro requisitos técnicos):**
1. Costes reales nativos: entrada al precio de compra y salida al de venta
2. Stops sin mejora de precio
3. Financiación asimétrica con triple miércoles
4. Dimensionado

**Contraste con la sección 3 de la especificación (R-01 a R-04):**

| Requisito de T2 (texto real, git HEAD) | Requisito de la especificación |
|---|---|
| Costes reales nativos: entrada al precio de compra y salida al de venta | R-01 "Costes nativos dentro de la simulación" — coincide palabra por palabra en la mecánica (entrada a compra, salida a venta) |
| Stops sin mejora de precio | R-02 "Un stop nunca ejecuta a mejor precio que el disparado" — coincide |
| Financiación asimétrica con triple miércoles | R-03 "Financiación asimétrica con triple miércoles" — coincide literal |
| Dimensionado | R-04 "Dimensionado por riesgo" — coincide |

También coincide la columna "Criterio de aceptación" de T2 ("se ejecuta con un caso hecho a mano...
si no coincide, no entra") con R-05 ("El caso hecho a mano es la prueba maestra"), y la columna "Qué
se descarta" (los drivers duplicados `backtest_f03*.py`, lógica en dos sitios) con R-06 ("La lógica
vive en un solo sitio"). No hay ninguna palabra de T2 que la especificación tergiverse o se salte.

**VEREDICTO PUNTO 1: los cuatro requisitos técnicos que usó `arquitecto` COINCIDEN con el texto real
de la fila T2. H-7 queda cerrado: no hace falta ninguna corrección de la especificación por este
punto.**

---

## PUNTO 2 — Aritmética a lápiz de los tres casos, rehecha de forma independiente

Rehecha con un script Python de solo aritmética (sin importar nada del motor viejo ni de gb2),
aplicando exclusivamente las fórmulas que la propia especificación declara en C-5, C-6, C-7 y en el
texto de la sección 7, sobre los datos que la propia especificación da. Guardado en
`/tmp/.../scratchpad/04.03.06/verificacion_casos.py`. Salida completa:

```
=== CL-1 — largo con swap (triple miercoles) y salida por señal ===
entry_ask = 3000.00 + 0.20 = 3000.2
stop_bid = 3000.0 - 55.0 = 2945.0  (dado: 2.945,00)
size_teorico = 20.0/55.0 = 0.363636 -> redondeo a la baja a paso 0.1 = 0.3
riesgo_nominal = 55.0 * 0.3 = 16.5  (dado: 16,50)
precio_pl = (3050.0 - 3000.2) * 0.3 = 14.94  (dado: +14,94)
comision = 0.10 * 0.3 = -0.03  (dado: -0,03)
base_swap = 3000.0 * 0.3 = 900.0  (dado: 900,00)
apunte martes (mult=1) = 900.0 * -0.0001 * 1 = -0.09  (dado: -0,09)
apunte miercoles (mult=3) = 900.0 * -0.0001 * 3 = -0.27  (dado: -0,27)
neto = 14.94 - 0.03 + -0.09 + -0.27 = 14.55
CAJA FINAL CL-1 = 2000.00 + 14.55 = 2014.55   <-- dado: 2.014,55
CL-1: REPRODUCE EXACTO

=== CL-2 — stop saltado por hueco de fin de semana de 5,05x ===
stop_bid2 = 3000.0 - 100.0 = 2900.0  (dado: 2.900,00)
size2 = 20.00/100.0 = 0.2 oz exactas (dado: 0,2)
gap = 2900.0 - 2395.0 = 505.0; veces = 505.0/100.0 = 5.05x  (dado: 5,05x)
precio_pl2 = (2395.0 - 3000.2) * 0.2 = -121.04  (dado: -121,04)
comision2 = 0.10 * 0.2 = -0.02  (dado: -0,02)
base_swap2 = 3000.0 * 0.2 = 600.0  (dado: 600,00)
apunte viernes = 600.0 * -0.0001 * 1 = -0.06  (dado: -0,06)
neto2 = -121.04 - 0.02 + -0.06 = -121.12
CAJA FINAL CL-2 = 2000.00 + -121.12 = 1878.88   <-- dado: 1.878,88
CL-2: REPRODUCE EXACTO

=== CL-2b — mismo caso, stop dentro de vela (sin hueco) ===
apertura 2950.0 no viola el stop (2900.0); L 2890.0 <= 2900.0 -> toca dentro de la vela
precio_pl2b = (2900.0 - 3000.2) * 0.2 = -20.04  (dado: -20,04)
neto2b = -20.04 - 0.02 + -0.06 = -20.12
CAJA FINAL CL-2b = 2000.00 + -20.12 = 1979.88   <-- dado: 1.979,88
CL-2b: REPRODUCE EXACTO

RESUMEN: CL-1=2014.55  CL-2=1878.88  CL-2b=1979.88 -- LOS TRES REPRODUCEN
```

Puntos verificados a mano además del resultado final, porque un caso a mano que no reproduce cada
paso intermedio no es un caso a mano completo:
- Número de cruces de 22:00 UTC con la posición abierta en CL-1: exactamente 2 (martes ×1, miércoles
  ×3), verificado contando explícitamente `r_D` cruzado entre `ts_entrada` (mar 16:00) y
  `ts_cierre_atribuido` (jue 04:00) — el jueves no cruza porque la salida (04:00) es anterior a las
  22:00 del propio jueves.
- Magnitud del hueco de CL-2: `2.900,00 − 2.395,00 = 505,00`, y `505,00 / 100,00 = 5,05×` exacto,
  coincidiendo con el máximo medido del oro citado en R-11.
- CL-2b: el nivel de ejecución es el nivel del stop (2.900,00), no la apertura (2.950,00), porque la
  apertura no viola el stop pero el mínimo de la vela sí — mecánica C-5/R-02 aplicada correctamente.

**VEREDICTO PUNTO 2: los tres casos REPRODUCEN exactos a 2 decimales: 2.014,55 · 1.878,88 · 1.979,88
USD. Ninguno diverge.**

---

## PUNTO 3 — Cada cifra citada, contra su fuente

```
$ grep -n "XAUUSD" /home/server/projects/bot-trading/01-investigacion/mercados/coste_swap.md
71:| XAUUSD ⁴ | Largo | −6,64 % · −18,19 $ | −8,16 % · −22,36 $ | sin dato fiable |
72:| XAUUSD ⁴ | Corto | +0,64 % · +1,75 $ | −0,76 % · −2,08 $ | sin dato fiable |
```
→ **Localizada.** Rango de la especificación (R-09): largo entre −8,16 % (XTB) y −6,64 % (OANDA);
corto entre −0,76 % (XTB) y +0,64 % (OANDA). Coincide exacto.

```
$ grep -n "0,19\|0,07\|0,26" /home/server/projects/bot-trading/01-investigacion/mercados/coste_operar.md
46:| **XAUUSD** (oro) | Raw/ECN ... | 0,19 USD/oz ... | 0,07 USD/oz ... | **0,26 USD/oz** | 0,15–0,30 ... |
```
→ **Localizada.** spread 0,19 y comisión 0,07 USD/oz (total 0,26), citados en R-13 y usados en la
config común de la sección 7. Coincide exacto.

```
$ grep -n "22,1527\|1,17%" /home/server/projects/bot-trading/01-investigacion/mercados/coste_relativo.md
127:| XAUUSD | 4h | 22,1527 | **1,17%** | 1,28x | **PASA ≤10%** |
```
→ **Localizada, y en la fila correcta.** Esta fila está en la tabla de la sección «CORRECCIÓN (31/07)
— sesgo del ATR medio en XAUUSD», que usa `atr14_mediana` (22,1527), NO en la tabla original de más
arriba del mismo fichero que usa la media sesgada (línea 74: XAUUSD 4h = 28,4289 / 0,92%). La
especificación (R-13b) usa la cifra correcta (mediana, la que el propio proyecto corrigió), no la
sesgada. Aritmética contrastada: `0,26 / 22,1527 × 100 = 1,1737...% ≈ 1,17 %` — coincide dentro de
±0,01 punto declarado.

**Hallazgo secundario (declaración de fuentes, no invalida la cifra):** R-13(b) atribuye el 22,1527
a `04-resultados/atr_15m_1h_4h.json`, y esa cifra existe efectivamente ahí:
```
$ grep -n "22.1527\|22,1527" /home/server/projects/bot-trading/04-resultados/atr_15m_1h_4h.json
304:          "atr14_mediana": 22.152714285714215,
```
Pero ese fichero **no está** en la lista "Leídas" de la sección 10 de la especificación (que solo
declara `coste_swap.md`, `coste_operar.md`, `coste_relativo.md`, `veredicto_criterios_g1.md`,
`precios_mercado.py`, WBS.md, DECISIONES.md y CLAUDE.md). El número es correcto y está en las dos
fuentes, pero la especificación cita como origen un fichero que su propia declaración de lecturas
dice no haber abierto. Es una inconsistencia de atribución, no un error de cifra: se corrige
apuntando la cita a `coste_relativo.md` (que sí está declarado leído y contiene el mismo número en la
misma fila) o añadiendo el JSON a la lista de "Leídas". No es, por sí solo, motivo de rechazo.

```
$ grep -n "5,05" /home/server/projects/bot-trading/04-resultados/veredictos/veredicto_criterios_g1.md
116:| XAUUSD | 1,34x | 5,05x | 8,0 |
```
→ **Localizada.** Fila XAUUSD, columna "máx", ataque A5. Coincide con R-11 y con CL-2.

```
$ grep -n "1.962\|1962" /home/server/projects/bot-trading/04-resultados/veredictos/veredicto_criterios_g1.md
74:**2.215 USD = 1.962 EUR → cabe en el techo declarado de 2.000 EUR** (no en 1.500).
```
→ **Localizada.** Ataque A3, recalculado con `atr14_mediana` (no con la media sesgada). Coincide con
R-10 y con D-19 consecuencia 2(c) (`00-direccion/DECISIONES.md`, línea 165: "operar oro exige unos
1.962 € por lote mínimo, contra un techo de cuenta de 2.000 €, salvo que el broker admita lotes
fraccionados de 0,1 oz").

**Nota sobre el encargo de este punto:** las dos últimas cifras (hueco 5,05x y lote mínimo 1.962 €)
no están en ninguno de los tres ficheros nombrados en el encargo (`coste_swap.md`, `coste_operar.md`,
`coste_relativo.md`); están en `veredicto_criterios_g1.md`, que es también donde la propia
especificación las cita. Se verificaron ahí, no en los tres ficheros nombrados, porque esa es la
fuente real declarada — cualquier intento de buscarlas en los tres ficheros habría dado "NO
LOCALIZADA" por buscar en el sitio equivocado, no porque la cifra no exista.

**VEREDICTO PUNTO 3: las cinco cifras están LOCALIZADAS y coinciden con su fuente real. Ninguna
marcada NO LOCALIZADA. Un hallazgo secundario de atribución (JSON no declarado como leído) que no
invalida la cifra pero debería corregirse.**

---

## PUNTO 4 — Caza de requisitos sin prueba ejecutable

Revisados los 16 requisitos (R-01 a R-16) uno a uno contra el criterio propio de la ficha: *"cada
requisito tiene su prueba de aceptación ejecutable al lado; un requisito sin prueba no es un
requisito"*.

**DEFECTO ENCONTRADO — R-06(c):**
> "(c) Revisión del revisor: una sola función de fill de stop y una sola de swap en todo el motor,
> referenciadas por nombre de símbolo."

Esto no es un comando ni una aserción ejecutable: es una revisión manual declarada como tal con sus
propias palabras ("Revisión del revisor"). No hay `grep`, no hay conteo, no hay criterio numérico
de paso/no-paso escrito. Cumple la regla 13 (referencia por nombre de símbolo) pero no la regla 6
(no-ambigüedad): dos revisores distintos podrían discrepar sobre qué cuenta como "una sola función".
Contrasta con R-06(a), que sí es ejecutable (`grep -rn "\.resample(" <dir_motor>` → 0), y muestra que
el propio arquitecto sabe escribir la versión ejecutable de esta clase de comprobación — R-06(c) se
quedó sin ella. Corrección mínima sugerida (no aplicada; no reparo lo ajeno): sustituir por algo del
tipo `grep -c "^def "` sobre los módulos de fill/swap, o un conteo por AST, con la cifra esperada (1)
escrita al lado.

**Observación menor, no bloqueante — R-02(c):**
> "(c) Toque exacto: vela con L = nivel del stop → dispara y ejecuta en el nivel."

A diferencia de sus hermanas (a, b, d, e), no da datos numéricos concretos. Es ejecutable igualmente
(la condición L == nivel es instanciable con cualquier número sin ambigüedad, y el criterio de paso es
preciso), pero rompe el patrón de "todo con velas y config completas" que sí siguen el resto de casos
de R-02 y toda la sección 7. No se marca como fallo porque no requiere adivinar nada para construir el
caso concreto; se anota para que quien construya no dude.

**Resto de requisitos (R-01, R-02 salvo (c), R-03 a R-05, R-06(a)(b), R-07 a R-16):** todos dan un
comando, una fórmula o una aserción con cifra concreta y criterio de paso/no-paso sin ambigüedad.
Ejecutables tal como están escritos.

**VEREDICTO PUNTO 4: UN requisito (R-06c) tiene una prueba NO ejecutable tal como está escrita — es
una revisión manual disfrazada de prueba de aceptación. Esto por sí solo incumple el criterio de
hecho de la ficha 04.03.06 y es motivo de RECHAZO parcial hasta corregirlo.**

---

## PUNTO 5 — Los tres eliminatorios

```
$ grep -n "miércoles" 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
40:  C-7 ... mult(miércoles) = 3 ...
55:  R-03 | Financiación asimétrica con triple miércoles. ...
100: ### CL-1 — largo con swap (triple miércoles incluido) ...
```
**Triple miércoles: PRESENTE**, con convención completa (C-7), requisito con prueba (R-03) y caso a
lápiz que lo ejercita (CL-1, verificado en el punto 2). No es RECHAZO.

```
$ grep -n "mejor precio" 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
54: R-02 | Un stop nunca ejecuta a mejor precio que el disparado. ...
```
**Stop que nunca ejecuta a mejor precio: PRESENTE**, con seis pruebas (a-f) y dos casos a lápiz
(CL-2, CL-2b, verificados en el punto 2). No es RECHAZO.

```
$ grep -n "lote fraccionado\|0,1 on" 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
67: R-10 | Lote fraccionado de 0,1 onzas. ...
```
**Lote fraccionado de 0,1 onzas: PRESENTE**, con paso de tamaño 0,1, redondeo a la baja, rechazo de
operación por debajo del mínimo, y origen explícito citado a D-19 2(c) y `veredicto_criterios_g1.md`
A3 (verificado en el punto 3). No es RECHAZO.

**VEREDICTO PUNTO 5: los tres eliminatorios están cubiertos con requisito y prueba propios. Ninguno
de los tres dispara el rechazo automático.**

---

## ADEMÁS — declaración de fuentes del arquitecto (sección 10) contra lo citado en el cuerpo

```
$ grep -n "backtest_f03\|gold-bot-2\|gb2\|0c35959\|backtester" 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
8:  sin leer el motor anterior (03-motor/backtester/), sin ejecutar git show 0c35959 y sin abrir
9:  /home/server/projects/gold-bot-2 — prohibiciones de la ficha 04.03.06, cumplidas...
49:  «Trasplante desde gb2 — criterios de aceptación», fila T2.
198-199: NO leídas, cumpliendo la prohibición de la ficha: 03-motor/backtester/ (ni un fichero),
  el commit 0c35959 (ningún git show ni variante), y /home/server/projects/gold-bot-2.
```
No aparece en ningún otro punto del documento ningún nombre de función, variable o estructura propia
del motor viejo o de gb2 (por ejemplo, no se menciona `backtest_f03` fuera de la cita literal de la
fila T2 del WBS, que es prosa de dirección, no código). No hay indicio de que se haya abierto lo
prohibido. Las tres prohibiciones de la ficha (no abrir `03-motor/backtester/`, no `git show
0c35959`, no abrir gb2) se declaran cumplidas y no encuentro nada que las contradiga.

Contraste de la lista "Leídas" contra las rutas citadas en el cuerpo del documento: coincide en 7 de
8 ficheros citados como fuente de una cifra concreta. La única discrepancia es la ya señalada en el
punto 3 (`04-resultados/atr_15m_1h_4h.json`, citado pero no declarado leído). `02-datos/bruto/XAUUSD/1m.csv.gz`
también se cita (R-08b, R-12c) pero no como fuente de una cifra ya usada — es la ruta que un test
FUTURO (04.03.07) cargará, no un dato que el arquitecto necesitara tener delante hoy; no se cuenta
como discrepancia de la misma clase.

---

## RESUMEN POR PUNTO

| Punto | Veredicto |
|---|---|
| 1 — Hueco H-7 (fila T2) | PASA — coincide con el texto real |
| 2 — Aritmética de los tres casos | PASA — los tres reproducen exactos |
| 3 — Citas contra fuente | PASA — 5/5 localizadas (1 hallazgo secundario de atribución, no de cifra) |
| 4 — Pruebas no ejecutables | **NO PASA** — R-06(c) es una revisión manual, no una prueba ejecutable |
| 5 — Los tres eliminatorios | PASA — los tres están cubiertos |

## VEREDICTO FINAL: **RECHAZA**

Motivo único: R-06(c) no cumple el criterio de hecho de la propia ficha 04.03.06 ("un requisito sin
prueba ejecutable no es un requisito"). Corrección sugerida y acotada: reescribir R-06(c) como un
comando o aserción ejecutable con cifra de paso/no-paso (p. ej. conteo de definiciones de función por
nombre de símbolo), y de paso corregir la atribución de la cifra 22,1527 en R-13(b) a una fuente que
sí figure en la lista "Leídas" de la sección 10. Ningún otro cambio necesario: los cinco puntos del
encargo, salvo este, pasan limpio, y la aritmética y las citas de fondo son correctas.

---
---

# RONDA 2 — revisión de las tres correcciones acotadas

**Revisor:** `constructor-datos` (`claude-sonnet-5`) · **Fecha:** 04/08/2026
**Orden:** dictada por el `orquestador`, transmitida por Claude Code (C4 de CLAUDE.md).
**Alcance:** limitado a las tres correcciones dictadas por `arquitecto` (R-06(c), R-13(b) y las tres
citas por línea de la sección 10), más dos comprobaciones transversales que el `orquestador` añadió:
(4) que nada más cambió, y (5) coherencia de la lista "Leídas" en las dos direcciones.
**Congelación respetada:** ningún `git commit`/`checkout`/`stash`/`restore`/`reset`/`rebase`/`amend`,
ningún paquete instalado. No se reparó nada.
**Regla 16 de CLAUDE.md:** cumplida — no se revisa trabajo propio; el veredicto de ronda 1 (arriba,
sin reescribir) es de la misma revisora por decisión del `orquestador`, no por autoasignación.
**Nota de reanudación:** esta ronda se interrumpió una vez por un 529 del servidor entre los puntos 2
y 3; se retomó desde el parte parcial sin volver a suponer nada de lo ya medido por ejecución.

## VEREDICTO GLOBAL: **ACEPTA**

Los tres puntos de la orden (R-06(c), R-13(b), citas por línea) están corregidos, son ejecutables sin
tener que preguntar nada, y no arrastran ningún otro cambio al documento. La comprobación transversal
5 (coherencia de "Leídas") encuentra un hallazgo real pero menor —seis referencias declaradas como
leídas que nunca se citan por su código en el cuerpo— que es plausible como lectura de contexto
contiguo (el mismo patrón que la propia sección 10 ya usa explícitamente para el WBS) y no equivalente
en gravedad al hallazgo de atribución que causó el rechazo de la ronda 1. No es motivo de rechazo.

---

## PUNTO 1 — R-06(c): leído como quien va a implementarlo

Texto vigente de R-06(c) (cita completa, no resumida, porque aquí el resumen es el riesgo):

> Camino único probado por sabotaje, no por ojo. 04.03.07 declara en el README del motor los dos
> nombres de símbolo: la función de fill de stop y la función de cargo de swap. Test
> `test_camino_unico`, ejecutado con `pytest -q <dir_motor> -k camino_unico`, determinista (R-15), en
> tres pasos: (1) ejecuta el motor sobre los datos de CL-1, CL-2, CL-2b y de los casos R-02(d), R-02(e)
> y R-03(a)-(b) —largos y cortos; stop por hueco, dentro de vela y en la vela de entrada; apuntes de
> swap en las dos direcciones— y guarda cada precio de fill de stop y cada importe de apunte de swap;
> (2) sustituye por nombre de símbolo (monkeypatch) la función de fill declarada por una envoltura que
> suma +1,00 USD a todo precio de fill que devuelve, reejecuta y cuenta `fills_intactos` = número de
> fills de stop cuyo precio no cambió respecto al paso 1; (3) restaura, sustituye la función de swap
> por una envoltura que suma +1,00 USD a cada importe de apunte, reejecuta y cuenta `apuntes_intactos`.
> Salida: los dos recuentos, impresos por el test. Pasa: `fills_intactos == 0` y `apuntes_intactos ==
> 0`. No pasa: cualquiera de los dos ≥ 1 [...]. Límite declarado: no detecta un duplicado muerto que
> estas ejecuciones no recorran [...].

**Las cuatro condiciones exigidas por el orquestador:**

| Condición | Veredicto | Por qué |
|---|---|---|
| (i) Comando que un tercero ejecuta sin preguntar | CUMPLE | `pytest -q <dir_motor> -k camino_unico`. `<dir_motor>` no es una laguna nueva: es la misma convención que ya usan R-06(a), R-07(a), R-08(b), R-12, R-14 y R-16 en todo el documento — "el directorio raíz del motor nuevo, que 04.03.07 fija en su primer commit y declara en su README" (nota al pie de la sección 4). Los dos nombres de símbolo a sustituir por monkeypatch siguen la misma lógica: 04.03.07 los declara en su README. Un tercero que llegue después de 04.03.07 no tiene que preguntarle a nadie: lee el README y ejecuta. |
| (ii) Salida numérica | CUMPLE | Dos enteros, `fills_intactos` y `apuntes_intactos`, impresos por el propio test. |
| (iii) Valor que pasa y valor que no pasa, declarados | CUMPLE | Pasa: `== 0` y `== 0`. No pasa: cualquiera `≥ 1`. Sin zona gris. |
| (iv) Reproducible | CUMPLE | El test corre sobre datos fijos (CL-1/CL-2/CL-2b y los casos R-02(d)/(e), R-03(a)-(b), todos con velas y cifras concretas en las secciones 3-4-7) y el motor es determinista por R-15 (misma entrada y config → salida bit-idéntica, con la aserción de cuadre R-01(c) apoyándola). Dos ejecuciones del mismo test sobre el mismo commit del motor dan el mismo par de recuentos. |

**¿Tendría que interpretar algo para construirlo?** No encuentro ningún punto en el que tenga que
adivinar o preguntar:
- Los datos de entrada (CL-1, CL-2, CL-2b, R-02(d), R-02(e), R-03(a)-(b)) están completos con velas,
  precios y cifras concretas en otras partes del mismo documento; no hay que inventar ningún dato para
  construir el fixture del test.
- "La función de fill declarada" es, sin ambigüedad, la de **stop** (el propio R-06 dice "la función de
  fill de stop y la función de cargo de swap" — dos símbolos, no más, y el paso (2) dice
  "`fills_intactos` = número de **fills de stop**"). No hay una tercera función de fill (de entrada o de
  salida por señal) que pueda confundirse con la sustituida.
- El orden de los tres pasos es explícito y con "restaura" entre el paso 2 y el 3, así que las dos
  sustituciones no se mezclan (se prueba una variable a la vez).
- El criterio de paso/no-paso es un entero exacto contra cero, no un umbral ni una tolerancia que haya
  que fijar por criterio propio.

**Veredicto de fondo — ¿de verdad caza una duplicación escrita como método, `lambda` o en línea?** Sí,
y el argumento se sostiene, con un límite real y declarado:
- El monkeypatch sustituye el objeto al que apunta el nombre de símbolo declarado. Cualquier código que
  produzca un fill de stop o un apunte de swap **pasando por ese nombre** queda necesariamente afectado
  por el +1,00, sea el símbolo una función de módulo, un método de clase invocado a través de ese
  nombre, o una `lambda` asignada a ese nombre — el monkeypatch no distingue la sintaxis de la
  definición, solo el nombre al que está enlazada la llamada.
- El argumento de "sin punto fijo" es correcto: `f(x) = x + 1,00` no tiene solución para `f(x) = x`
  sobre los reales, así que ningún valor que atraviese genuinamente la función sustituida puede
  quedarse igual por casualidad numérica.
- Si existe una duplicación real —una segunda función, método o `lambda`, con el mismo cálculo, que
  algún camino del motor invoca en vez de (o además de) la declarada— esa duplicación **no** pasa por
  el símbolo parcheado, así que su salida no cambia, y aparece exactamente como un caso de
  `fills_intactos ≥ 1` o `apuntes_intactos ≥ 1`. La cobertura de casos (largo y corto, hueco/vela/vela de
  entrada para el stop, largo y corto para el swap) está elegida a propósito para forzar que, si hay dos
  caminos —uno por dirección, que es precisamente lo que R-06 prohíbe—, ambos se ejerciten y al menos
  uno de ellos quede "intacto".
- **Límite que la propia prueba declara, y que es real:** un duplicado que ningún caso de la lista
  ejercite (código muerto, o una rama condicional que estos siete casos no disparan) no se detecta por
  este mecanismo. El documento lo dice explícitamente y lo remite a la revisión de código de 04.03.07
  (regla 16 de CLAUDE.md), que es donde corresponde — no es una promesa incumplida, es un límite
  reconocido de una técnica de caja negra.

**VEREDICTO PUNTO 1: PASA.** R-06(c) es una prueba ejecutable, sin ambigüedad de construcción, que
cumple las cuatro condiciones exigidas, y su argumento de fondo (mide comportamiento, no texto) se
sostiene con un límite declarado y razonable. No tengo que preguntar nada a nadie para construirla.

---

## PUNTO 2 — R-13(b): atribución de fuente, verificada por ejecución

```
$ grep -n "22.152714285714215\|22,1527" 04-resultados/atr_15m_1h_4h.json
304:          "atr14_mediana": 22.152714285714215,

$ grep -n "22,1527" 01-investigacion/mercados/coste_relativo.md
127:| XAUUSD | 4h | 22,1527 | **1,17%** | 1,28x | **PASA ≤10%** |

$ grep -n "22.152714285714215" 01-investigacion/mercados/coste_relativo.md
(sin resultado)

$ grep -n "22,1527" 04-resultados/atr_15m_1h_4h.json
(sin resultado)
```

**Confirmado por ejecución:** el JSON contiene el número largo (`22.152714285714215`, con punto y
quince decimales); `coste_relativo.md` contiene el número corto (`22,1527`, con coma y cuatro
decimales), y cada fichero contiene únicamente su propia forma — ninguno contiene la del otro. El
razonamiento del `arquitecto` para reatribuir la fuente (el formato corto con coma es el de la tabla,
no el largo con punto del JSON) es correcto y verificable.

**Sección, tabla y fila que R-13(b) cita ahora, comprobadas con esos títulos exactos:**

```
$ grep -n "CORRECCIÓN (31/07)" 01-investigacion/mercados/coste_relativo.md
92:## CORRECCIÓN (31/07) — sesgo del ATR medio en XAUUSD: la tabla de arriba usa una media inflada...

$ grep -n "coste relativo contra ATR MEDIANA" 01-investigacion/mercados/coste_relativo.md
114:### Tabla — coste relativo contra ATR MEDIANA (divisas, oro y cripto)

$ sed -n '127p' 01-investigacion/mercados/coste_relativo.md
| XAUUSD | 4h | 22,1527 | **1,17%** | 1,28x | **PASA ≤10%** |
```

La sección «CORRECCIÓN (31/07) — sesgo del ATR medio en XAUUSD» existe (línea 92; el título completo
continúa tras los dos puntos, R-13(b) cita el fragmento hasta "XAUUSD", que es subcadena literal). La
tabla «Tabla — coste relativo contra ATR MEDIANA (divisas, oro y cripto)» existe (línea 114) y la fila
XAUUSD/4h (línea 127, dentro de esa tabla, sin ningún encabezado `##`/`###` intermedio entre la 114 y
la 127) contiene exactamente 22,1527 y 1,17%, las dos cifras que R-13(b) usa. `coste_relativo.md` está
en la lista "Leídas" de la sección 10; `04-resultados/atr_15m_1h_4h.json` no lo está, y R-13(b) ahora lo
dice explícitamente ("fichero que el autor no leyó y que no figura en la sección 10") en vez de
ocultarlo.

**VEREDICTO PUNTO 2: PASA.** La atribución de fuente es correcta y verificada por ejecución; la
sección, la tabla y la fila citadas existen con esos títulos exactos; la cifra no se movió.

---

## PUNTO 3 — Sección 10: cero citas por número de línea, comprobado por ejecución

```
$ grep -n "línea\|líneas" 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
60:[...] aunque el duplicado sea un método de clase, una `lambda` o código insertado en línea [...]
66:[...] `grep -rniE "\bpips?\b" <dir_motor>` → 0 líneas [...]
```

**Los dos únicos resultados NO son citas por número de línea:** la línea 60 usa "en línea" con el
sentido de "inline" (un tipo de código, no una referencia a un número de línea de un fichero); la
línea 66 usa "líneas" como unidad de la salida de `grep` ("0 líneas" = cero líneas de salida
coincidentes, el resultado esperado del comando, no una cita de dónde vive algo). **Cero citas por
número de línea de un fichero fuente, verificado.**

**Las tres viñetas de la sección 10 que se corrigieron, y lo que cita cada una ahora, comprobado que
existe con esos títulos exactos (repitiendo por ejecución independiente lo que ya localicé en el punto
2, sin asumirlo):**

```
$ grep -n "Fase 02 — ELEGIR MERCADO Y TAMAÑO DE VELA" 00-direccion/WBS.md
77:## Fase 02 — ELEGIR MERCADO Y TAMAÑO DE VELA (puerta G1)
$ grep -n "^| 02.02.02 \|^| 02.03.03 " 00-direccion/WBS.md
84:| 02.02.02 | ...
90:| 02.03.03 | ...
$ grep -n "Fase 03 — MONTAR LA CASA" 00-direccion/WBS.md
92:## Fase 03 — MONTAR LA CASA (Claude Code) — EN PARALELO con la Fase 02
$ grep -n "Fase 04 — HIPÓTESIS Y VALIDACIÓN" 00-direccion/WBS.md
116:## Fase 04 — HIPÓTESIS Y VALIDACIÓN (puerta G2)
$ grep -n "Límites del CEO" 00-direccion/WBS.md
193:## Límites del CEO (29/07/2026, cerrados el 01/08/2026 en la tarea 01.01.03)
$ grep -n "04.03 Laboratorio de pruebas" 00-direccion/WBS.md
133:### 04.03 Laboratorio de pruebas (por hipótesis y variante)
$ grep -n "^| 04.03.06 \|^| 04.03.07 " 00-direccion/WBS.md
141:| 04.03.06 | ...
142:| 04.03.07 | ...

$ grep -n "^## D-16\|^## D-17\|^## D-18\|^## D-19\|^## D-20\|^## D-21" 00-direccion/DECISIONES.md
137:## D-16 · ...   144:## D-17 · ...   151:## D-18 · ...
158:## D-19 · ...   171:## D-20 · ...   181:## D-21 · ...

$ grep -n "Ataques que SÍ han tumbado algo" 04-resultados/veredictos/veredicto_criterios_g1.md
22:## Ataques que SÍ han tumbado algo (con su experimento)
$ grep -n "^### A3\|^### A4\|^### A5" 04-resultados/veredictos/veredicto_criterios_g1.md
69:### A3 — ...   86:### A4 — ...   104:### A5 — ...
```

Todas las secciones, filas de tabla y entradas de decisión que las tres viñetas corregidas de la
sección 10 citan ahora existen hoy, con esos títulos exactos, y ninguna referencia sobrevive por
número de línea.

**VEREDICTO PUNTO 3: PASA.**

---

## PUNTO 4 — Nada más cambiado: verificado por `diff`, no "no verificado"

**Base de comparación:** no hay commit del documento (no existe ningún `git show` posible), pero sí
tengo una base fiable: la copia defensiva que yo misma guardé en la ronda 1, **antes** de que
`arquitecto`/`secretario` aplicaran las tres correcciones, en el mismo directorio de scratchpad de esta
sesión (`.../scratchpad/04.03.06/03-motor-copia/ESPECIFICACION_MOTOR_BACKTEST.md`, con fecha de
modificación 03/08 23:30:14, anterior a la del fichero actual, 04/08 09:00:55). Verifiqué su
autenticidad antes de usarla: el texto de R-06(c) y de R-13(b) que contiene esa copia coincide
palabra por palabra con lo que mi propio veredicto de ronda 1 citó como defecto — no es una copia
cualquiera, es la que yo revisé y rechacé.

```
$ diff -u 03-motor-copia/ESPECIFICACION_MOTOR_BACKTEST.md 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
```

Resultado íntegro: **cuatro bloques de diferencia, ni uno más:**
1. Línea de cabecera añadida: "**Ronda 2 (03/08):** tres correcciones dictadas por `arquitecto`..." —
   la cadena de custodia admitida.
2. La celda de prueba de R-06(c) completa, sustituida por el texto del punto 1.
3. La celda de prueba de R-13(b), sustituida por el texto del punto 2.
4. Las tres viñetas de la sección 10 (WBS.md, DECISIONES.md, veredicto_criterios_g1.md), cada una
   cambiando de "líneas N–M" a una referencia descriptiva por sección/fila — el objeto del punto 3.

Ninguna cifra de los tres casos a lápiz (CL-1, CL-2, CL-2b), ningún requisito R-01 a R-16 salvo R-06 y
R-13, ninguna exclusión de la sección 8, ningún hueco de la sección 9, y ninguna otra línea de la
sección 10 cambió. **VERIFICADO, no "no verificado".**

**VEREDICTO PUNTO 4: PASA.**

---

## PUNTO 5 — Coherencia de la lista "Leídas" en las dos direcciones

**Dirección A — todo lo citado en el cuerpo está declarado leído:** repasadas todas las rutas de
fichero citadas en el cuerpo (`coste_swap.md`, `coste_operar.md`, `coste_relativo.md`,
`veredicto_criterios_g1.md`, `precios_mercado.py`, WBS.md, DECISIONES.md, CLAUDE.md): las ocho están en
la lista "Leídas". Las tres excepciones que aparecen en el texto no rompen esta dirección porque
ninguna es una cita viva de una cifra actual: `02-datos/bruto/XAUUSD/1m.csv.gz` es la ruta de datos que
un test FUTURO de 04.03.07 cargará (no algo que el arquitecto necesitara tener delante hoy, ya aceptado
así en la ronda 1); `04-resultados/atr_15m_1h_4h.json` se menciona solo para decir que NO se leyó (es el
objeto de la corrección del punto 2, autoflagelado en el propio texto); `04-resultados/coste_relativo.md`
se menciona solo para decir que NO existe (nota de discrepancia de insumo, ya presente desde la ronda
1). **Dirección A: PASA, sin excepción real.**

**Dirección B — todo lo declarado leído se usa en el cuerpo:** aquí encuentro un hallazgo real, por
ejecución:

```
$ for d in D-16 D-17 D-18 D-19 D-20 D-21; do echo -n "$d: "; grep -c "$d\b" ESPECIFICACION_MOTOR_BACKTEST.md; done
D-16: 1   D-17: 0   D-18: 0   D-19: 8   D-20: 0   D-21: 1

$ for a in A3 A4 A5; do echo "-- $a --"; grep -n "\b$a\b" ESPECIFICACION_MOTOR_BACKTEST.md; done
-- A3 -- línea 69 (R-10) y línea 197 (la propia declaración de "Leídas")
-- A4 -- solo línea 197 (la propia declaración de "Leídas")
-- A5 -- líneas 37 (C-2), 70 (R-11), 146 (CL-2) y 197
```

Las únicas apariciones de "D-16" y de "D-21" en todo el documento son dentro de la propia frase de la
sección 10 que los declara leídos ("entradas D-16 a D-21"); ninguno de los dos se cita luego por su
código para justificar ningún requisito. Lo mismo pasa con D-17, D-18 y D-20 (cero apariciones fuera de
esa frase). Y el ataque **A4** se declara leído junto a A3 y A5, pero a diferencia de esos dos —que sí
se citan explícitamente por su código junto a una cifra concreta (A3 en R-10, A5 en C-2/R-11/CL-2)— A4
no vuelve a aparecer en ningún otro punto del cuerpo.

**Juicio sobre la gravedad:** esto es un hallazgo real de la comprobación que se me pidió, no un
invento para justificar un rechazo. Pero su explicación más probable es benigna y distinta en
naturaleza del hallazgo de la ronda 1 (que era una cifra atribuida a un fichero nunca abierto): D-16 a
D-21 son seis entradas consecutivas y cercanas en fecha (01-03/08) dentro del mismo fichero cronológico,
y A3-A4-A5 son tres secciones `###` consecutivas dentro de la misma sección `##` ("Ataques que SÍ han
tumbado algo"). Es la forma normal de leer un documento por bloques contiguos, no de "espigar" solo lo
que conviene citar — sería más raro leer A3 y A5 sin que A4, que está físicamente entre ambas, pasara
también por delante. La propia sección 10 ya reconoce esta distinción para el WBS.md, separando
explícitamente "contexto de fases" (leído en bloque, no todo citado) de "el detalle" (la ficha de
04.03.06/04.03.07, sí citada punto por punto) — pero no aplica esa misma separación explícita a
DECISIONES.md ni a `veredicto_criterios_g1.md`, que se declaran en bloque sin esa aclaración. Esa
asimetría de formato es la raíz del hallazgo, no una prueba de que se citara algo sin haberlo tenido
delante.

**VEREDICTO PUNTO 5: PASA CON HALLAZGO MENOR, NO BLOQUEANTE.** Dirección A (citado→declarado) limpia.
Dirección B (declarado→usado) tiene seis referencias (D-16, D-17, D-18, D-20, D-21, A4) declaradas
leídas que nunca se citan por código en el cuerpo. Recomendación, no exigida por esta ronda: si
`arquitecto` vuelve a tocar la sección 10, aplicar a DECISIONES.md y a `veredicto_criterios_g1.md` la
misma separación explícita "contexto / detalle" que ya usa para el WBS.md, para que la lista de
"Leídas" no dé la impresión de que cada entrada declarada aporta una cita, cuando en realidad varias son
contexto de bloque.

---

## ADEMÁS (fuera del alcance de esta ronda, solo para que no se pierda)

Confirmado que las tres cosas que `arquitecto` señaló y NO arregló a propósito siguen igual, tal como
se esperaba — no las marco como defecto de esta ronda:
- (a) La sección 3 y el hueco H-7 siguen diciendo "Verificación pendiente para el revisor" (línea 50) y
  "Revisor de esta especificación: ejecutar `git show HEAD:00-direccion/WBS.md`..." (hueco H-7, sección
  9) pese a que la ronda 1 ya lo ejecutó y coincidió (ver PUNTO 1 del veredicto de ronda 1, arriba).
- (b) La cabecera sigue diciendo "**Estado:** PENDIENTE DE REVISIÓN por un agente distinto del autor".
- (c) La observación menor sobre R-02(c) (sin datos numéricos concretos, a diferencia de sus hermanas)
  sigue sin corregir.

**Nota sobre contexto externo, verificada pero fuera de alcance:** el mensaje de reanudación menciona
que el CEO autorizó una segunda lectura de gb2, ratificó la vela de 4h y dejó D-2 suspendida con
disparador. Comprobado por `grep`: existe **D-25 · 2026-08-04** en `00-direccion/DECISIONES.md` con
ese contenido exacto (segunda apertura de gb2 acotada a la prueba de aceptación de 04.03.07; D-2
"SUSPENDIDA CON DISPARADOR, no derogada", sustituyendo la cláusula de D-19). El documento bajo revisión
no cita "D-2" en ningún punto (verificado por `grep`, sin resultado) y mi `diff` del punto 4 confirma
que nada relacionado con esto cambió en él. D-25 no afecta al veredicto de esta ronda porque el
documento revisado no depende de esa cláusula; queda anotado por trazabilidad, no como hallazgo.

## RESUMEN POR PUNTO — RONDA 2

| Punto | Veredicto |
|---|---|
| 1 — R-06(c), leído como quien va a implementarlo | PASA — ejecutable, sin ambigüedad, caza duplicación por comportamiento, límite declarado |
| 2 — R-13(b), atribución de fuente | PASA — verificado por ejecución: JSON tiene el número largo, `coste_relativo.md` el corto y la sección/tabla/fila citadas existen |
| 3 — Sección 10 sin citas por línea | PASA — cero citas por número de línea; las tres viñetas corregidas citan secciones que existen hoy |
| 4 — Nada más cambiado | PASA — VERIFICADO por `diff` contra una copia defensiva auténtica de ronda 1: solo los cuatro cambios admisibles |
| 5 — Coherencia de "Leídas" en las dos direcciones | PASA CON HALLAZGO MENOR — dirección citado→declarado limpia; dirección declarado→usado tiene 6 referencias sin cita explícita, explicación benigna (lectura de bloque contiguo) |

## VEREDICTO FINAL RONDA 2: **ACEPTA**

Las tres correcciones dictadas resuelven exactamente lo que la ronda 1 y el `orquestador` pidieron
resolver, son ejecutables sin tener que preguntar nada, y no arrastran ningún cambio no autorizado al
resto del documento (verificado por `diff` contra una base fiable, no supuesto). El hallazgo del punto
5 es real pero menor, de una clase distinta y más benigna que el que causó el rechazo de la ronda 1, y
no impide que `04.03.07` construya contra este documento sin tener que interpretar ni preguntar nada.
