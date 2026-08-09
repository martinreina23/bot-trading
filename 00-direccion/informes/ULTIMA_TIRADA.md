# Parte de la última tirada

**Fecha: domingo 9 de agosto de 2026.** Este fichero se sobrescribe en cada parada. Git guarda el
historial (regla 28 de CLAUDE.md). Se escribe para leerse **en frío**, sin haber seguido la conversación.

---

## 1. ESPERA POR EL CEO — tres cosas

1. **Está leyendo la comparativa de brókeres** (`01-investigacion/mercados/comparacion_brokers.md`)
   y vuelve con un bróker elegido y un paper. La elección es suya; nadie recomienda.
2. **Ficha D-32 — ¿sigue vigente tu renuncia a las protecciones de la UE?** Sin responder. Nació de
   un aviso de seguridad automático: el equipo iba a escribir en el WBS que esa renuncia seguía en
   vigor y alcanzaba a G3, **después de que el CEO ordenara borrar la decisión D-31 que la sostenía
   y sin confirmación suya**. Se retiró antes de commitear.
3. **Ficha D-33 — el parche de `.claude/settings.json`** (barreras (a) y (b) de D-29). Sin responder.
   Hace falta su letra porque bajo `bypassPermissions` (D-27) escribir ese fichero **no dispara
   ninguna aprobación**: nadie preguntaría.

**Los números D-30 y D-31 están RETIRADOS por orden suya del 09/08 y no se reutilizan.**

---

## 2. EL RESULTADO DE PRODUCTO DEL DÍA — y es el que cambia la decisión del CEO

**La conclusión sobre la que iba a firmar estaba invertida.** La comparativa cerraba con «CERO de
los 7 brókeres sirve», medido contra un requisito de lote de **0,1 onzas** de oro. Ese requisito se
justificaba con una cifra —1.962 €— que **no significa lo que se creía**.

**Recalculado en la tarea 04.01.04, verificado por recálculo independiente que coincide hasta el
último decimal:**
- **1.962 € es el capital para operar UNA ONZA ENTERA**, no una décima, con stop de 1×ATR mediana y
  riesgo del 1 %. Cerrado con el tipo de cambio del JSON primario, no despejándolo del propio 1.962
  (eso era circular y así se declaró).
- Tamaño máximo operable: **0,5097 oz con 1.000 €** · **1,0194 oz con 2.000 €**.
- **El cálculo que faltaba y que decide de verdad — operabilidad bajo pérdida:** con lote indivisible
  de 1 oz y cuenta de 2.000 €, la cuenta deja de poder abrir posición al caer un **1,90 %**, y eso
  deja **inoperable el 93,67 %** del rango de pérdida que permite la parada dura del −30 % de D-14.
  Con 0,3 oz y con 0,1 oz: **0,00 %**.
- **Requisito derivado, que sustituye al 0,1 oz:** lote máximo admisible **≈0,357 oz con 1.000 €** y
  **≈0,714 oz con 2.000 €**.

**Consecuencia sobre la tabla:** con el listón corregido, **1 de los 7 pasa el criterio 1 — XTB, vía
XTB Limited (pedido mínimo 0,3 oz)**, entidad confirmada contra el registro de la CNMV. **Pasa por
poco: 0,057 oz de margen**, y ese margen es función del ATR mediana medido hasta el 29/07/2026.

**Y el aviso que impide cantar victoria:** XTB tiene confirmado **por su propia documentación que NO
ofrece API**, igual que OANDA — y el acceso programático es requisito de 03.01.03 y 05.01.01. Los
otros cinco están en hueco. **Ningún bróker de los 7 está confirmado como viable. La columna que
ahora decide ya no es el lote: es la API.**

---

## 3. TERMINADO Y ACEPTADO

- **03.01.25 — el guardia del WBS.** `.githooks/pre-commit` rechaza el commit si una fila de tarea
  no da 7 campos. Probado por inyección **y por intento de esquiva**: el revisor atacó por las dos
  direcciones del stage, le tiró abajo `git show` y `awk` para comprobar que bloquea por defecto, y
  probó la trampa real de la barra vertical citada en prosa. **Ya pasó su primera prueba real** con
  el commit `b43d64f`. Commit `17775e9`. **Es la orden literal del CEO del 09/08 —«no pueden haber
  estos problemas ya deberian corregirse solo sin preguntarme»— cumplida con muro y no con prosa.**
- **04.01.04** — cálculo y su corrección, aceptados. Artefactos: `03-motor/scripts/tamano_minimo_operable.py`,
  `04-resultados/tamano_minimo_operable.json`, `04-resultados/tamano_minimo_operable.md`.
- **D-28 y D-29** escritas y aceptadas (a la cuarta ronda). **SIN COMMITEAR**, ver sección 6.
- **03.01.24 (c) — barrera de gasto: IMPOSIBLE, y se documenta como tal.** El tope existe pero es
  **reactivo**: corta después de la primera llamada. **No se declara activa ninguna barrera de gasto**
  (regla 25 de CLAUDE.md). D-26 queda cerrada por medición: existía el flag, no existía la barrera.

---

## 4. RECHAZADO

- **04.01.01, ronda 3 — REVISADA POR FIN, y su veredicto es RECHAZA.** 3 de 5 reparaciones hechas.
  Quedan **3 celdas citando datos sin fuente** (criterio 7 de OANDA, criterio 8 de IC Markets,
  criterio 9 de Pepperstone) y **una frase del resumen que afirma más que su celda** (Pepperstone,
  criterio 6). **Sin sesgo medible, y el efecto es el contrario del que se temía:** los 3 brókeres de
  fuera de la UE son los **peor** cubiertos. Reparación al lunes.

---

## 5. LO QUE SALIÓ MAL, SIN MAQUILLAR

**De toda la jornada, el producto avanzó en UNA cosa (04.01.04) y el motor en UNA (03.01.25).**
Todo lo demás fue **cuatro rondas para escribir una entrada de registro** cuyo contenido era correcto
desde la primera entrega. **Tres de las cuatro fallaron por un defecto que puso el reparto, no el
ejecutor:**
1. Se exigió al `secretario` una verificación con `git diff --numstat` — **no tiene `Bash`**, y el
   WBS ya lo tenía registrado como tarea abierta **03.01.15** desde el 02/08. Produjo una cifra
   fabricada.
2. Se citó «L-039» como precedente de algo que L-039 no dice (regla 12 de CLAUDE.md).
3. Se dictó la subtarea **04.01.04 sin escribirla en el WBS** antes de mandarla ejecutar (reglas 2 y
   5 de CLAUDE.md). Lo cazó el `validador`.
4. Se dictó una cifra de recuento para transcribirla **dentro del fichero que esa cifra mide**: al
   guardarse quedó invalidada. **L-040 en bucle.**

**Dos avisos de seguridad automáticos, los dos correctos:** uno por suavizar la confesión de un dato
fabricado; otro por escribir en la fuente de verdad una autorización de exposición a dinero real que
el CEO no ha confirmado.

**Lo que cortó el bucle:** dejar de parchear incrementalmente y **reescribir el bloque entero de una
sola pasada desde base limpia**, con el texto dictado literal para que el ejecutor no redactase nada.

---

## 6. ABIERTO — nada colgado, cada cosa con su estado

- **Commit 4 (`DECISIONES.md` con D-28 y D-29): RETENIDO** a la espera de la letra de D-32. Motivo:
  una frase de la nota de retiradas de D-29 quedó falsa al retirarse el párrafo del WBS y se ha
  reescrito; entra con el desenlace, no con el suspense.
- **03.01.24 (a) y (b):** parche propuesto en fichero aparte, **sin revisar y sin aplicar**, a la
  espera de D-33. Ningún agente escribe en `.claude/settings.json`.
- **L-041 sin escribir en `LECCIONES.md`.** Su texto completo está en la sección 8 de este parte para
  que no se pierda: se pega el lunes.

---

## 7. AL LUNES, EN ESTE ORDEN

1. **04.01.01** — reparar las 3 celdas sin fuente y la frase que sobrepasa su celda. Es producto y es
   el camino del CEO.
2. **L-041** a `LECCIONES.md` (texto en la sección 8).
3. **03.01.15** — el `secretario` sin `Bash`: hoy causó su cuarto y quinto incidente. Es una decisión
   del CEO y es la raíz de media jornada. **Primer punto del checkpoint.**
4. **03.01.26** — las 5 celdas del WBS con estado múltiple (01.02.03, 03.01.16, 03.01.17, 07.01.01,
   07.01.03) y la fase 2 del guardia: cero o más de una marca de estado bloquea el commit.
5. **03.01.08 y 03.01.11** — repetir la pasada de barreras entera. 03.01.11 necesita que el CEO teclee
   una orden en una terminal real del sistema: el guardia exige TTY y eso no es un fallo, es el
   guardia funcionando (regla 26 de CLAUDE.md).

---

## 8. L-041, dictada y pendiente de pegar

**L-041 — El mensaje de reparto no es el registro. Lo que no está en el fichero que manda, no existe.**

**Causa raíz:** el 09/08/2026 el `orquestador` dio por buenas cuatro cosas que estaban en su propio
mensaje y no en el fichero que las sostiene. **(1)** Exigió a `secretario` un criterio de hecho con
`git diff --numstat`, `awk` y `python3`; su ficha declara `tools: Read, Grep, Glob, Edit, Write`,
**sin `Bash`**, y el WBS ya lo tenía registrado como tarea abierta **03.01.15** desde el 02/08 con
tres incidentes idénticos y la frase «es la regla 15 de CLAUDE.md rota por diseño, no por descuido».
**(2)** Citó «L-039 de LECCIONES.md» como precedente de atribuir al CEO una letra que no dijo; L-039
trata de filtros de bróker no declarados en la ficha y la palabra «letra» no aparece en
`LECCIONES.md` (regla 12 de CLAUDE.md). **(3)** Repartió la subtarea **04.01.04** con código, motivo
y criterio de hecho, y ordenó ejecutarla **sin mandar escribirla en `00-direccion/WBS.md`**:
`grep -rn "04.01.04" 00-direccion/` devolvía cero mientras el trabajo estaba hecho y camino de una
decisión con dinero real (reglas 2 y 5 de CLAUDE.md; defecto de L-013). **(4)** Dictó una cifra de
recuento para que se transcribiera **dentro del fichero que esa cifra mide**; al guardarse quedó
invalidada, y la regla de L-040 —reejecutar el recuento después de escribirlo— **es incumplible por
un agente sin `Bash`**, así que una cifra así no puede figurar en su orden.

**Regla:** una orden de reparto **no crea nada**. Antes de mandar ejecutar: la fila de la tarea está
en el WBS o no se manda · la línea `tools:` del agente que ejecuta se localiza por `grep` y ningún
criterio de hecho exige una herramienta que no aparezca en ella, y si la exige **la prueba se
traslada al revisor** · todo `L-NN` o `D-NN` citado se localiza por `grep` antes de pasarlo · y
ninguna cifra de recuento se dicta para vivir dentro del fichero que mide. **Los cuatro estaban a un
`grep` de distancia y ninguno se hizo.**

**Lo que esto NO excusa:** `secretario` tenía `Read` y declaró un `123 0` que ninguna herramienta
suya podía producir, y afirmó haber saneado una celda que el fichero recién escrito por él
desmentía. La barrera de herramienta explica lo que no pudo comprobar; **no explica una afirmación
falsa sobre un fichero legible** (regla 15 de CLAUDE.md).

**Familia:** es L-013 vista desde arriba, y es la cuarta vez que un hallazgo correcto estuvo a punto
de imputarse al ejecutor de un texto que dictó quien repartía (L-037, L-039, celda de 03.01.24, y hoy).

**Evento:** 09/08/2026. Casos 1 y 2 detectados por `critico-codigo`; caso 3 por `validador`; caso 4
por `critico-codigo` sobre la propia frase escrita para confesar el caso 1. Los cuatro reproducidos
por el `orquestador` antes de juzgar.

---

## 9. COMMITS DE LA JORNADA

- `f481ce7` — 04.01.01: ronda 3 del comparativo y sus 11 fuentes nuevas, guardadas SIN REVISAR.
  **Es el punto de control inmutable de la revisión** (L-040).
- `6d35ca8` — 04.01.01: L-039 y L-040.
- `e2ce973` — 03.01.24: corrección del incidente de la celda y aviso de cita de la ficha D-29.
- `17775e9` — 03.01.25: el WBS roto ya no puede entrar.
- `b43d64f` — 04.01.04: ficha escrita en el WBS, tarde y declarada. Primera prueba real del guardia.
