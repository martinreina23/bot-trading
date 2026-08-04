# Auditoría 07.01.03, lote (a) — Los registros de dirección escritos sin flujo (D-19, D-20, D-21, L-024–L-027) y el añadido D-22/D-23

**Agente:** `validador` (`claude-fable-5`, modelo principal disponible, **sin necesidad de respaldo**).
**Orden:** del `orquestador`, transmitida por Claude Code (C4 de CLAUDE.md), con un añadido a mitad
de tarea (contraste palabra a palabra de D-22/D-23 contra el veredicto del lote (d)).
**Fecha:** 03/08/2026. **Congelación respetada:** cero `git commit`, `checkout`, `stash`, `restore`;
cero paquetes. **Copia defensiva** de `DECISIONES.md`, `LECCIONES.md` y `WBS.md` hecha fuera del
repositorio (scratchpad) antes de ejecutar nada. **No se ha tocado `02-datos/reservado/`.**
**No he reparado nada.** Toda cifra de este documento sale de una ejecución o un `grep`/`git show`
hechos por mí hoy; la vara de medir es la cita literal del CEO de las 21:44 del 03/08, única
intervención suya de esa noche según el encargo.

---

## VEREDICTO GLOBAL (una línea)

**D-19, D-20, D-21 y L-026 NO PASAN tal como están escritas; D-22 NO PASA por una cronología
invertida presentada como medida; D-23, L-024 y L-027 PASAN; L-025 PASA con reserva; el
append-only se cumple (0 líneas borradas en los dos registros).**

---

## 1. D-19 — Puerta G1: oro solo, vela de 4h

### (a) ¿«Vela de 4h» es decisión del CEO o inferencia del equipo? → **INFERENCIA DEL EQUIPO, escrita como suya. NO PASA en atribución.**

- La cita literal del CEO no contiene «vela» ni «4h». Verificado contra el texto de la orden.
- Las cuatro opciones de la ficha (`INFORME_DECISION_G1.md`, sección 3) llevaban todas 4h como
  base: A «vela 4h», B «vela 4h», C «A + vela 1h» (4h más 1h), D «A + BITCOIN».
- D-19 escribe: «el bot se construye sobre XAUUSD (oro al contado) y **vela de 4 horas**» y lo
  registra como «una quinta opción **del propio CEO**». La vela no salió de su boca. La inferencia
  es defendible (base común de todo lo presentado), pero **el texto no la declara como inferencia:
  la firma como decisión del CEO.**

### (b) ¿«DEROGA D-2» o suspensión con disparador? → **SUSPENSIÓN CON DISPARADOR (figura de D-17). La palabra «DEROGA» es del equipo. NO PASA en la figura.**

- El CEO dijo **dos veces «de momento»** y dio condición de vuelta: «cuando encontremos y probemos
  que las hipótesis ganan dinero de verdad entonces ya nos metemos con otra moneda». Eso es
  exactamente la figura que el propio equipo creó en D-17: suspensión con disparador, no
  derogación.
- D-19 registra el contenido condicional («declara la ampliación a un segundo mercado como paso
  posterior condicionado…» y «G1-C5 vuelve a aplicarse el día que entre el segundo mercado») —el
  fondo está—, pero lo etiqueta «Esta decisión DEROGA D-2». La etiqueta dice más que el CEO.

### (c) Las cifras de las consecuencias, una a una → **TODAS LOCALIZADAS. Ninguna NO LOCALIZADA. Un matiz perdido.**

| Cifra en D-19 | Fichero y localización | Veredicto |
|---|---|---|
| Hueco de fin de semana **5,05x**, medido en el oro | `04-resultados/veredictos/veredicto_criterios_g1.md`, tabla del ataque A5, fila XAUUSD (`| XAUUSD | 1,34x | 5,05x | 8,0 |`) | **LOCALIZADA** — con matiz perdido: la ficha que vio el CEO la llevaba marcada **«no probado»** y con la discrepancia D-a declarada (el texto aprobado de D-11 dice máx. 4,52x en EURUSD); D-19 la escribe sin la marca |
| Swap del oro **−6,64% y −8,16%** anual en largo; corto «casi neutro» | `01-investigacion/mercados/coste_swap.md`, tabla 8×3, fila `XAUUSD Largo` (−6,64% OANDA / −8,16% XTB) y fila `XAUUSD Corto` (+0,64% / −0,76%); también `arrastre_coste.md`, tabla de swap | **LOCALIZADA** |
| **1.962 €** por lote mínimo, techo de cuenta 2.000 € | `veredicto_criterios_g1.md` («2.215 USD = 1.962 EUR → cabe en el techo declarado de 2.000 EUR») y `00-direccion/WBS.md`, sección Puertas, viñeta G1-C6 | **LOCALIZADA** |
| Coste relativo **0,94% central frente a 1,93%** de USDJPY; «el más barato de los 8» | `01-investigacion/mercados/arrastre_coste.md`, tabla central 4h: XAUUSD 0,94 · USDJPY 1,93; resto del bloque 2,05–3,20; BTCUSD 2,50/4,56; ETHUSD 9,72/22,73 | **LOCALIZADA** — «el más barato de los 8» se sostiene contra la tabla, con la reserva ya declarada en el informe de que las cifras de cripto son otro tipo de estimador |
| **2,32% frente al umbral del 10%** (G1-C2 a 4h) | `01-investigacion/mercados/coste_relativo.md`, fila `XAUUSD | 4h | … | **2,32%** | … | PASA ≤10%`; «el que más margen deja» se sostiene (siguiente mejor: GBPUSD 3,22%) | **LOCALIZADA** |
| (2d) coste de feb-2025, «podría casi duplicarse» | `coste_operar.md` (Pepperstone «Costs and Charges» v5.0, **feb-2025**, fila XAUUSD) y `veredicto_fase_02.md` (cotas ×1,82 / ×2,34) | **LOCALIZADA** — «casi duplicarse» es fiel para ×1,82 y se queda corta para ×2,34 |
| (2e) L-007 sin resolver (futuro vs contado) | `LECCIONES.md`, L-007; `coste_swap.md`, sección Advertencias («front-month future» / «next-month future») | **LOCALIZADA** |

**Verificación de la observación del CEO, reproducida por mí por ejecución:** `python3
03-motor/scripts/cestas_g1.py` (leído antes: determinista, solo lectura) da exactamente lo que
D-19 afirma — **4 cestas de 3 admisibles a 4h, ninguna de 4 ni de 5, XAUUSD en las 4 y USDJPY en
las 4** (máx. corr. de la mejor cesta 0,5478). Esa parte de D-19 es verdad medida.

**Veredicto D-19: NO PASA como acta de lo que el CEO dijo.** El fondo (oro solo, foco, condición
de vuelta) está bien recogido y todas las cifras se localizan; pero «vela de 4h» y «DEROGA» son
del equipo escritas como suyas, y el 5,05x perdió su marca «no probado» al pasar de la ficha al
registro.

---

## 2. D-20 — Cierre de las auditorías del ecosistema

**Las cinco ideas y sus destinos, contra el WBS de hoy — TODAS COINCIDEN:**

1. Contador producto/motor → fila `03.01.18` «NUEVA 03/08 (D-20, idea 1 de las auditorías)». ✓
2. Registro de autoría → fila `03.01.19` «NUEVA 03/08 (D-20, idea 2 de las auditorías)». ✓
3. Detección de fallo/rechazo de modelo → fila `03.01.04`, cuya ficha dice «FICHA (03/08, D-20) —
   CORRECCIÓN DE ALCANCE… **un hook no puede cambiar el modelo**». Coincide con lo que D-20 anuncia. ✓
4. Arranque desatendido por reloj → fila `03.01.03` («arranques programados», cron). ✓
5. Aviso al humano con hook nativo `http` → incorporado a la ficha de `03.01.03` («idea 5 de las
   auditorías: hook nativo de tipo `http`»), como implementación recomendada y no tarea aparte. ✓

**«El proyecto no tiene configurado ni un solo hook» — REFUTADA tal como está escrita, por
ejecución:**

- Lo verdadero: `.claude/settings.json` contiene solo las claves `permissions` y `_nota`
  (comprobado por lectura). Cero hooks **de Claude Code**.
- Lo falso: `git config core.hooksPath` devuelve `.githooks`, y `.githooks/` contiene `pre-commit`
  y `commit-msg`, ejecutables, que son el muro mecánico que CLAUDE.md declara comprobado. **El
  proyecto SÍ tiene hooks configurados: dos de git.** La frase, escrita sin restricción y bajo el
  rótulo «verificado por ejecución», afirma más de lo verificado.

**Atribución:** la cita del CEO es fiel (limpieza ortográfica; «nosotras»→«nosotros»). El cierre
de `01.02.03`/`01.02.04` con hueco declarado, el criterio nuevo para futuras auditorías y los
destinos concretos de las ideas son operacionalización del equipo bajo la firma «Decide: CEO» — el
CEO no dijo nada de cerrar tareas ni de crear `03.01.18`/`03.01.19`.

**Veredicto D-20: NO PASA como está escrita.** Los destinos son verificables y correctos; la
afirmación del hook es falsa como literal y pide entrada de corrección que la restrinja a hooks de
Claude Code; la forma operativa es del equipo, no del CEO.

---

## 3. D-21 — Eliminación del trasplante desde gb2

**El párrafo «Qué se pierde exactamente» NO sigue en pie. Dos falsedades, ambas probadas:**

1. **«nada vivo»** — FALSO. El criterio de aceptación de T2 existía en la sección «Trasplante desde
   gb2 — criterios de aceptación» (verificado por mí: `git show HEAD:00-direccion/WBS.md` contiene
   la fila `T2 — Motor de backtest` con «lápiz y papel» y «mejora de precio»; el `grep` de esos
   fragmentos sobre el WBS de hoy devuelve **cero**). Lo mismo concluyeron el lote (b+c) (RECHAZA)
   y su revisión (CONFIRMO). Hubo que crear `04.03.06` para reconstruirlo.
2. **«no se copió una sola línea de gb2, y de hecho no se podía»** — FALSO en las dos mitades,
   medido por el lote (d): 109 líneas no triviales idénticas (23+76+10) y la ruta de gb2 accesible
   en disco y citada dentro del propio código.

**Las cuatro sustituciones, verificadas pieza a pieza contra el WBS de hoy:**
- T1 (dataset histórico) → `02.02.01` (descarga de precios y cálculo de ATR): existe. ✓
- T3 (testbed de invarianza) → `03.01.10` («Testbed sintético de invarianza»): existe. ✓
- T4 (guardias del cajón) → `03.01.08` (prueba de fuego de barreras) y `03.01.11` (guardia por
  cifrado): existen. ✓
- T5 (13 fichas de hipótesis) → `04.02.01` (barrido de fuentes desde cero): existe; «12 de 13
  nunca se probaron» es coherente con D-1 («se probó 1 de 13»). ✓

**¿La eliminación se llevó el criterio de T2 y D-21 lo declaró?** Se lo llevó — probado arriba — y
**D-21 no lo declaró: afirmó lo contrario** («comprobado pieza por pieza antes de borrar… nada
vivo»). La fila del log del WBS lo repite («comprobado pieza a pieza que no se pierde nada vivo»),
propagando la falsedad. **D-23 corrige solo la falsedad de las líneas; la de «nada vivo» sigue hoy
sin entrada de corrección en `DECISIONES.md`.**

**Atribución:** la cita del CEO es fiel y la decisión (quitar la tarea, construir de cero) es
suya. La «comprobación pieza por pieza» es del equipo y no se hizo de verdad.

**Veredicto D-21: NO PASA.** Orden del CEO bien recogida; motivación con dos afirmaciones de hecho
falsas, una todavía sin corregir en el registro.

---

## 4. L-024 a L-027 — contra la cabecera de LECCIONES.md (causa raíz + regla verificable + evento trazable)

- **L-024 — PASA.** Causa raíz (D-13 firmada sin propagar), regla verificable (grep de frases
  contradictorias en el mismo commit), evento trazable (D-13 existe con esa literalidad; el error
  de calendario del 03/08 está registrado de forma independiente en la motivación de D-18).
- **L-025 — PASA CON RESERVA.** Las tres piezas están. La mitad técnica es verificable y la he
  verificado documentalmente (`cajon_reservado.py`, símbolo `_pedir_password`: `sys.stdin.isatty()`
  y el mensaje literal «BLOQUEADO: la contraseña solo se teclea en una terminal real»). La reserva:
  el incidente en sí (lo que recibió el CEO) no deja artefacto en ningún registro — el
  `registro-cajon.md` del 03/08 solo recoge dos COMPROBAR de las 14:26 — así que esa mitad del
  evento solo es trazable por el propio texto de la lección, escrita sin revisor.
- **L-026 — NO PASA como está escrita: afirma más de lo que el lote (b+c) demostró.** Lo que sí
  quedó demostrado por ejecución (b+c y su revisión, por separado): el guardia FIXTURE existe y
  muerde, y el caso 2 quedó localizado por estructura. Lo que la lección tapa al decir «Reparado en
  el mismo día»: la clase de defecto que la propia lección describe (literal de prosa que caduca)
  **seguía viva esa misma noche en los casos 3, 4 y 5 del mismo script**, recayó (caso 3, literal
  `07.01.03`, veredicto (b+c) punto 4; reproducido por la revisión), y `prueba_inyeccion.sh` sale
  hoy con exit 1: **la barrera de la regla 25 de CLAUDE.md no está verificada**. La regla que la
  lección enuncia no se aplicó al resto del script que la motivó.
- **L-027 — PASA.** Las tres piezas están; la reparación de la fusión está confirmada por ejecución
  ajena a la sesión que la escribió ((b+c) punto 2; revisión campo a campo contra HEAD, sin pérdida
  de texto). Anoto dos precisiones: (1) L-027 **no** afirma «verificado por inyección» — esa
  atribución del encargo solo corresponde a L-026; (2) la cifra «de 56 a 54» no es re-medible
  directamente (ese estado nunca se commiteó), pero la cadena aritmética cierra exacta con todo lo
  medido: HEAD tiene 54 filas de tarea **incluida** `01.02.02` (verificado), + 2 altas de D-20
  (03.01.18/19) = 56 → quitar `01.02.02` debía dar 55 → la fusión dio 54 → reparado 55 → +3 altas
  (07.01.03, 03.01.16, 03.01.17) = 58 medido por (b+c) → +2 (04.03.06/07) = 60, que es lo que yo
  mido hoy.

---

## 5. APPEND-ONLY — **REPRODUCIDO: SE CUMPLE**

```
$ git diff HEAD --numstat -- 00-direccion/DECISIONES.md 00-direccion/LECCIONES.md
84  0  00-direccion/DECISIONES.md
20  0  00-direccion/LECCIONES.md
```

Cero líneas borradas en los dos registros (área de staging vacía, comprobado también con
`--cached`). Lo escrito sin flujo se escribió mal, pero se escribió **añadiendo**.

---

## 6. D-22 y D-23 — mismas varas, más el contraste palabra a palabra ordenado a mitad de tarea

### D-22 — **NO PASA tal como está escrita** (la elección del CEO sí está fielmente registrada)

- **Atribución al CEO — correcta en el fondo:** D-22 no le pone en la boca ningún motivo que no
  salga del precio que se le declaró. Su lista («se deshace el commit de ayer, cumple su orden al
  100%, ahorra la auditoría, cuesta una tirada de construcción y pierde 44 pruebas que quizá
  estaban bien») coincide con el literal presentado. Las **44 pruebas** las he verificado por
  ejecución: 13+20+11 funciones de test en `0c35959`. El rótulo **«Motivo, con las palabras del
  CEO»** es impropio: el CEO no pronunció palabra alguna, eligió una letra; el cuerpo lo matiza
  («eligió la opción B… sabiendo el precio que se le declaró»), pero el rótulo imita la plantilla
  de D-19/D-20/D-21 sin que haya palabras detrás.
- **«Qué la provoca, medido y no supuesto» — la cronología está invertida y NO está medida:**
  `0c35959` se commiteó el **03/08 a las 17:32** (medido: `git show -s --format='%ci'`); D-21 y la
  cirugía del WBS son de las **21:44–21:58 del mismo día**. Por tanto «que es justo lo que D-21
  **había ordenado** dejar de heredar» y «su criterio de aceptación había sido borrado del WBS **la
  noche anterior**» son falsas: el motor entró **antes** de que D-21 existiera y **antes** de que el
  criterio se borrara — no hubo desobediencia a una orden vigente, la orden llegó cuatro horas
  después. Sí es verdad, y lo verifiqué («git grep» sobre `0c35959` fuera de la carpeta: solo
  menciones documentales), que ningún fichero externo lo importaba; y el revert `eb7ac2f` existe
  (23:08) y borra exactamente los 9 ficheros del motor.
- D-22 declara «Confirmación del CEO sobre ESTE TEXTO: pendiente al escribirse» — correcto y a favor.

### D-23 — **PASA.** Contraste palabra a palabra contra `auditoria_07.01.03_d_procedencia_motor.md`

1. **«109 líneas no triviales idénticas: 23 / 76 / 10»** — las cuatro cifras están en el fichero
   (tabla de los seis pares y sección del hallazgo) y 23+76+10 = 109. ✓
2. **COPIA disparada por el umbral del 50% de símbolos y no por el del 30% de líneas, con la
   tensión incluida** — el fichero lo dice así, literal: «ETIQUETA FINAL…: COPIA — la disparan
   `execution.py` (símbolos 66.7%/100%) y `sizing.py` (símbolos 50.0%/50.0%), no el umbral de
   líneas literales (que no lo cruza ningún fichero, máximo 24.8%)», y declara la tensión
   («textualmente no hay copia en bloque… pero la interfaz reproduce la de gb2…»). D-23 la
   traslada entera. ✓
3. **66,7% / 100% · 50% / 50% · 24,8%** — localizados en la tabla y en la etiqueta final. ✓
   Los seis símbolos que D-23 lista coinciden con los del fichero. ✓
4. **La frase entrecomillada de las 12 menciones** — está en el fichero («Construido como
   informacion, no como copia en bloque de `/home/server/projects/gold-bot-2/engine/core/execution.py`»),
   y «las 12, sin excepción, son referencia declarada». Desviación tipográfica mínima: D-23
   escribe «información» con tilde dentro de comillas donde el código dice «informacion». ✓ con nota.
5. Resto de afirmaciones de D-23 verificadas: ruta de gb2 en `INFORME_GB2.md` desde el 30/07
   (lote (d), sección iii, commit `da1e3c7`); «lo que sí era cierto en D-21» (4 `.md`, ningún `.py`
   commiteado); retirada en `eb7ac2f` (medido por mí); constantes y mensajes de error con
   intersección vacía. ✓
6. **Dos observaciones menores, sin efecto de fondo:** (i) el título «sí se copiaron líneas» es un
   punto más duro que la medición («líneas idénticas»; el fichero llama a los bloques contiguos
   «shape de interfaz» y a los mensajes «idioma compartido, no copia literal») — el cuerpo de D-23
   lo compensa con «código reescrito por dentro sobre el mismo esqueleto»; (ii) el atenuante del
   fichero «ningún bloque contiguo reproduce el cálculo económico» no viaja a D-23.

**Sobre el temor del orquestador a un relato endurecido colado en D-22/D-23:** en D-23 no lo
encuentro — las cifras, la etiqueta y la tensión están trasladadas con fidelidad. En D-22 el
endurecimiento existe y es la cronología invertida del apartado «Qué la provoca», más el rótulo
«con las palabras del CEO».

---

## LO QUE EL CEO NO DIJO Y ESTÁ ESCRITO COMO SUYO

1. **D-19 — «vela de 4h».** No está en su cita. Era la base común de las cuatro opciones; el texto
   la registra dentro de «una quinta opción del propio CEO» sin declarar que es inferencia.
2. **D-19 — «DEROGA D-2».** Él dijo «de momento» dos veces y dio condición de vuelta: eso es
   suspensión con disparador (la figura de D-17), no derogación. La palabra es del equipo.
3. **D-19 — el 5,05x sin su marca.** La ficha que él vio decía «no probado» y «aprobado: 4,5x»; el
   registro escribe «máximo medido» sin la marca — le atribuye una decisión informada por un
   número más firme de lo que era.
4. **D-20 — el cierre de `01.02.03` y `01.02.04`, el criterio nuevo de auditorías y los destinos
   de las cinco ideas.** Sus palabras dan el motivo («ideas, no piezas»); el paquete operativo es
   del equipo y va firmado «Decide: CEO».
5. **D-21 — «comprobado pieza por pieza antes de borrar… nada vivo».** El CEO ordenó quitar la
   tarea; la comprobación es del equipo, no se hizo de verdad, y su resultado afirmado es falso
   (criterio de T2 perdido; 109 líneas idénticas). Repetido en la fila del log del WBS. La mitad
   «nada vivo» sigue sin entrada de corrección.
6. **D-22 — el rótulo «Motivo, con las palabras del CEO»** sobre una elección que fue una letra
   sin palabras; y **la cronología invertida** («D-21 había ordenado…», «borrado la noche
   anterior») bajo el rótulo «medido y no supuesto», que convierte su opción B en respuesta a una
   desobediencia que, con las horas medidas (motor 17:32; orden y cirugía 21:44–21:58), no ocurrió
   en ese orden. Endurecimiento del equipo/transporte, no del CEO.

---

## Recuento de esta auditoría (regla 20 de CLAUDE.md)

Ejecuciones: 10 (numstat de los dos registros, con `--cached` · recuento de filas de tarea
HEAD/disco · grep del criterio T2 en HEAD y en disco · `core.hooksPath` + listado de `.githooks/` ·
timestamps de `0c35959`/`eb7ac2f` · numstat del revert · `git grep backtester` en `0c35959` ·
recuento de `def test` (44) · `cestas_g1.py` completo · fila `01.02.02` en HEAD).
Verificaciones documentales por grep/lectura: 18 (todas las cifras de D-19, las 9 filas del WBS
citadas por D-20/D-21, el guardia de `cajon_reservado.py`, `registro-cajon.md`, `settings.json`,
los dos veredictos previos y su revisión, y el contraste D-22/D-23 contra el lote (d)).
Reparaciones: **0**. Ficheros del proyecto modificados: **1** (este veredicto, entregable ordenado).
