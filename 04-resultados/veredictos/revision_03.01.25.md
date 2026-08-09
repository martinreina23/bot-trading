ACEPTA

# Revisión independiente 03.01.25 — guardia de la métrica L-027 en `.githooks/pre-commit`

**Revisor:** `critico-codigo`. **Modelo declarado:** `claude-sonnet-5` (regla 29 de CLAUDE.md). No hizo
falta respaldo (`claude-opus-5`): no hubo rechazo ni atasco.

Ejecutado por `constructor-motor`, artefacto declarado en `04-resultados/verificacion_03.01.25.md`.
No escribí ese guardia. Todas las inyecciones de este informe son mías, con códigos distintos de
`03.01.25`, `04.01.01` y `04.02.02` (este último confirmado real y ajeno: WBS.md, fila
`04.02.02` = "Ficha por hipótesis..."). Todas se revirtieron; prueba de reversión en cada bloque.

Punto de partida verificado antes de tocar nada: `git hash-object 00-direccion/WBS.md` =
`6b9db4f68267abe7ea4f04ff45bad1f457a4618b`, `git diff -- 00-direccion/WBS.md` vacío, índice sin
nada en stage salvo lo declarado por el aviso de concurrencia (03.01.24: `.githooks/pre-commit`
modificado bajo revisión, `00-direccion/DECISIONES.md` con 44 inserciones en curso de `secretario`,
y varios ficheros sin seguimiento bajo `04-resultados/` y `03-motor/`). Nada de eso se tocó en
contenido; donde tuve que copiarlo para una prueba (regla 21) quedó restaurado byte a byte,
verificado por `git hash-object`.

---

## G1 — Cuatro inyecciones propias

**Caso 1 (mío) — WBS intacto + fila nueva bien formada `09.09.01`:**
```
EXIT_CODE=0
```
Sin salida de `BLOQUEADO`. Revertido: `git restore --staged` + copia del original.
`git hash-object` tras revertir = `6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (igual al inicial).

**Caso 2 (mío) — fila `09.09.02` partida en 3 líneas por un editor de texto:**
```
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 09.09.02: 3 campos (deberian ser 7)
EXIT_CODE=1
```
Revertido y verificado: hash idéntico al inicial.

**Caso 3 (mío) — filas `09.09.03` y `09.09.04` fusionadas en una sola línea:**
```
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 09.09.03: 13 campos (deberian ser 7)
EXIT_CODE=1
```
Cifra de 13 campos consistente con el propio incidente que originó L-027 (dos filas de 7 campos
que comparten el borde pierden una barra al fusionarse: 7+7-1=13). Revertido y verificado.

**Caso 4 (mío) — prosa fuera de tabla citando el vocabulario de estado con barras**
(`estado_a | estado_b | estado_c`), sin empezar la línea por `| CC.CC.CC |`:
```
EXIT_CODE=0
```
Sin falso positivo. Revertido y verificado.

Los cuatro casos dan el resultado exigido y las cuatro reversiones quedaron probadas por
`git diff` vacío, `git diff --cached` vacío y `git hash-object` idéntico al original en cada una.

---

## G2 — El caso real, no de laboratorio

Probado con el WBS **real e intacto**, que ya contiene las dos citas de barra vertical en prosa
que señala la orden:

- Baseline con el fichero real completo en stage: `EXIT_CODE=0`, sin `BLOQUEADO`.
- Fila real `03.01.25` aislada con el mismo `-F'|'` del hook:
  `awk -F'|' '/^\| *03\.01\.25 *\|/ {print "codigo=" $2 " NF=" NF}'` → `codigo= 03.01.25  NF=7`.
  Pasa: no es un caso de laboratorio, es la fila real, con su propio aviso interno sobre la barra
  vertical escrito en palabras, no como carácter literal.
- Línea de prosa de la sección «Estados y cadencia de este WBS» que **sí** contiene el carácter `|`
  literal dentro de una cita en línea de código (`` `awk -F'|' '{print NF}'` ``), 2 barras
  verticales contadas por `grep -o`: no empieza por `| CC.CC.CC |` (empieza por `- **Cómo se
  cuenta...`), así que no matchea el patrón de arranque del hook
  (`^[ \t]*\| *[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9] *\|`). Verificado con `grep -E` del mismo patrón:
  `NO MATCH (correcto: no se cuenta como fila de tarea)`.

Las dos trampas reales que cita la orden no rompen el guardia. Si el guardia se hubiera tragado
cualquiera de las dos, el veredicto habría sido RECHAZA.

---

## G3 — ¿Lee el stage o el fichero de trabajo? (la trampa que decide)

**G3-A: `git add` del WBS sano, y DESPUÉS se rompe el fichero de trabajo sin volver a añadirlo.**
```
-- stage ahora mismo (sano) --
-- ahora rompo SOLO el fichero de trabajo, sin add --
-- diff no cacheado (demuestra que el working tree esta roto) --
 00-direccion/WBS.md | 3 +++
 1 file changed, 3 insertions(+)
-- ejecuto el hook: debe PASAR porque lo que se commitearia (stage) esta sano --
EXIT_CODE=0
```
PASA, como debe: lo que se commitearía (el stage) está sano aunque el working tree esté roto.

**G3-B: se rompe el fichero, se hace `git add` (queda roto EN STAGE), y LUEGO se arregla el
fichero de trabajo sin volver a añadirlo.**
```
-- stage ahora mismo (roto): --
 00-direccion/WBS.md | 3 +++
 1 file changed, 3 insertions(+)
-- ahora arreglo el working tree, VOLVIENDO al original, sin add --
-- diff no cacheado (demuestra que el working tree ya esta sano de nuevo) --
 00-direccion/WBS.md | 3 ---
 1 file changed, 3 deletions(-)
-- ejecuto el hook: debe BLOQUEAR porque lo que se commitearia (stage) sigue roto --
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 09.09.07: 3 campos (deberian ser 7)
EXIT_CODE=1
```
BLOQUEA, como debe. El guardia lee `git show ':00-direccion/WBS.md'` (versión en stage), nunca el
fichero de trabajo. No se esquiva rompiendo el WBS después de `git add`. Ambas pruebas revertidas
y verificadas por `git hash-object` = `6b9db4f68267abe7ea4f04ff45bad1f457a4618b`.

---

## G4 — ¿Bloquea por defecto ante error? (regla 26 de CLAUDE.md)

**Aviso metodológico importante, hallazgo propio de esta revisión:** un WBS.md en stage
byte-a-byte idéntico a HEAD **no aparece en `git diff --cached --name-only`**, aunque se haya
hecho `git add` — git no reporta diferencia porque no la hay. El guardia solo actúa cuando el
fichero aparece en esa lista. Mi primer intento de forzar el fallo de `awk` con el WBS íntegro dio
`EXIT_CODE=0`, pero **no probaba nada**: el bloque de la métrica ni se ejecutó, porque
`git diff --cached --name-only` no listaba el WBS. Lo repetí con una fila real distinta de HEAD en
stage para que el bloque se ejerciera de verdad.

**G4-A — WBS con un cambio real en stage, `awk` inaccesible en el `PATH` del hook** (stub que
imprime "command not found" y sale 127, antepuesto al `PATH`, sin tocar la resolución de `git`):
```
BLOQUEADO (metrica L-027): fallo al ejecutar la metrica sobre el WBS en stage.
   awk: command not found (simulado por critico-codigo para G4)
EXIT_CODE=1
```
Bloquea, no deja pasar.

**G4-B — `git show` no puede leer el WBS en stage** (forzado con `git rm --cached`, que borra el
WBS del índice y lo deja en estado "en disco pero no en el índice"; `git show ':ruta'` exige que
la ruta exista en el índice):
```
BLOQUEADO (metrica L-027): no se pudo leer 00-direccion/WBS.md en stage.
   fatal: path '00-direccion/WBS.md' exists on disk, but not in el índice
EXIT_CODE=1
```
Bloquea, no deja pasar. `git rm --cached` no borra el fichero de disco (solo del índice); tras
`git restore --staged` + recopia del original, `git hash-object` volvió a dar
`6b9db4f68267abe7ea4f04ff45bad1f457a4618b`.

**Ambos ejes de la regla 26 verificados por inyección: ante fallo real de `git show` o de `awk`,
el resultado es BLOQUEAR, nunca dejar pasar.**

**Hallazgo sobre el artefacto del ejecutor, no sobre el código:** `04-resultados/verificacion_03.01.25.md`
afirma como hecho — "Bloquea por defecto (regla 26 de CLAUDE.md): si `git show` no puede leer el
WBS en stage, o si la propia ejecución de `awk` falla por cualquier motivo, también bloquea con
mensaje explícito" — pero sus cuatro casos documentados (intacto-pasa, partida-falla,
fusión-falla, prosa-pasa) **no incluyen ninguna inyección de ese fallo**. Es exactamente lo que
regla 25 de CLAUDE.md prohíbe declarar como activo sin probarlo por ejecución. La conducta en sí
es correcta —la he verificado yo mismo arriba, con inyección real—, así que no es motivo de
rechazo del guardia, pero **es un hueco real en su propio artefacto** que debería corregirse
(añadir G4-A/G4-B o equivalente a su verificación) antes de que ese documento se dé por completo.

---

## G5 — No ha roto los muros que ya había

```
$ git diff HEAD -- .githooks/pre-commit | grep -E '^-' | grep -v '^---'
(ninguna linea borrada: 0 lineas '-' en el diff completo)
```
`git diff --stat`: `1 file changed, 39 insertions(+)`, cero borrados. Las primeras 38 líneas del
fichero (bloques de las reglas 27, 22, 21 y 13 de CLAUDE.md) son **textualmente idénticas** a
`HEAD:.githooks/pre-commit` (`diff` entre ambos rangos vacío).

**Prueba de que la regla 21 sigue mordiendo de verdad**, sin tocar el contenido en curso de la
tarea 03.01.24 (se restauró exacto después): tomé el `DECISIONES.md` de **HEAD** (no el de trabajo,
que solo tiene inserciones sin commitear y por tanto no sirve para probar un borrado real frente a
HEAD), le quité su última línea (`**Confirmación del CEO sobre ESTE TEXTO: CONFIRMADA el
04/08/2026.**`) y lo puse en stage:
```
$ git diff --cached --numstat -- 00-direccion/DECISIONES.md
0	1	00-direccion/DECISIONES.md
$ bash .githooks/pre-commit
BLOQUEADO (regla 21): 00-direccion/DECISIONES.md solo admite AÑADIR, y este commit borra lineas.
   Una correccion es una entrada nueva que cita a la anterior.
EXIT_CODE=1
```
Bloquea. Restaurado exactamente el `DECISIONES.md` de trabajo (con las 44 inserciones en curso de
`secretario`, ajenas a esta tarea): `diff` contra la copia de referencia tomada al empezar, vacío;
`git hash-object` = `12218a5a06dfeee27930224af7e76976cc78c18b`, igual en ambos extremos.

---

## G6 — Residuo

```
$ git diff -- 00-direccion/WBS.md
(vacío)
$ git diff --cached -- 00-direccion/WBS.md
(vacío)
$ git status --short
 M .githooks/pre-commit
 M 00-direccion/DECISIONES.md
?? 03-motor/scripts/tamano_minimo_operable.py
?? 04-resultados/parche_settings_03.01.24.json
?? 04-resultados/tamano_minimo_operable.json
?? 04-resultados/tamano_minimo_operable.md
?? 04-resultados/veredictos/revision_03.01.24_registro.md
?? 04-resultados/veredictos/revision_04.01.04.md
?? 04-resultados/verificacion_03.01.24.md
?? 04-resultados/verificacion_03.01.25.md
$ awk -F'|' '/^\| *[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9] *\|/ {if (NF!=7) print NR}' 00-direccion/WBS.md
(vacío)
$ git hash-object 00-direccion/WBS.md
6b9db4f68267abe7ea4f04ff45bad1f457a4618b   (idéntico al inicial)
```
Todo lo que queda en `git status` es del aviso de concurrencia (tarea `03.01.24`, en curso en
paralelo: `constructor-motor` sobre `03-motor/` y `04-resultados/`, `secretario` sobre
`DECISIONES.md`) o el propio artefacto declarado de esta tarea (`verificacion_03.01.25.md`, sin
tocar por mí). Ningún residuo mío. Contraste adicional de una cifra del artefacto del ejecutor:
declaran "66 filas de tarea, todas con NF==7" antes de empezar sus inyecciones; reproducido de
forma independiente: `grep -cE '^\| *[0-9]{2}\.[0-9]{2}\.[0-9]{2} *\|' 00-direccion/WBS.md` → `66`,
y el mismo `awk` de arriba confirma `malas: 0`. Cifra correcta.

Confirmado además que `.claude/settings.json` no aparece tocado (`git status --short` y
`git diff --stat` ambos vacíos para ese fichero) y que no hay ningún `git commit` en el historial
de esta revisión (`git log` no cambió).

---

## G7 — Filtro de cantidad (C3 de CLAUDE.md)

39 líneas para: (1) comprobar si el WBS está en el commit, (2) leer su versión en stage con manejo
de error, (3) ejecutar la métrica con manejo de error, (4) formatear el mensaje de bloqueo. No veo
lógica sobrante: no hay ninguna rama que no se ejerza en las pruebas de arriba, y el patrón de
arranque (`^[ \t]*\| *[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9] *\|`) es exactamente tan estricto como
hace falta para no confundir prosa con fila de tarea, verificado con las dos citas reales del WBS
que podían haberlo tentado (G2). El único punto flojo no es el código, es la cobertura del
artefacto de verificación del ejecutor en el eje de error (ver G4). Ajustado, no hay de más.

---

## Citas D-NN y por línea (regla 12 y 13 de CLAUDE.md)

```
$ grep -noE 'D-[0-9]+' .githooks/pre-commit
(vacío: el hook no cita ninguna decisión D-NN)
$ grep -noE 'D-[0-9]+' 04-resultados/verificacion_03.01.25.md
(vacío)
$ grep -nE '\.(py|md|sh):[0-9]+' .githooks/pre-commit 04-resultados/verificacion_03.01.25.md
(vacío: ninguna referencia a código por número de línea)
```
Sin citas fabricadas y sin referencias a línea prohibidas. La única cita a símbolo la hace por
nombre del comentario: `# --- Metrica L-027 (00-direccion/LECCIONES.md) sobre el WBS ---`.

---

## Veredicto

**ACEPTA.** El guardia muerde de verdad, no solo en el laboratorio: reinyecté los cuatro casos con
filas propias (G1), probé el caso real con las dos citas de barra vertical en prosa que existían
ya en el WBS antes de esta tarea (G2), confirmé que lee la versión en stage y no el fichero de
trabajo en las dos direcciones de la trampa (G3), forcé el fallo real de `git show` y de `awk` y en
ambos casos bloqueó (G4), confirmé que no tocó ni desactivó los cuatro bloques anteriores del hook
y que la regla 21 sigue mordiendo (G5), y no quedó ningún residuo en el WBS ni en el índice (G6).
El único defecto real encontrado es de proceso, no de código: el artefacto
`04-resultados/verificacion_03.01.25.md` afirma el comportamiento de bloqueo-por-defecto ante error
sin haberlo probado ellos mismos por inyección (regla 25 de CLAUDE.md) — se recomienda que se
complete con esa prueba antes de darlo por un artefacto cerrado, pero no invalida el guardia, que
ya queda probado por esta revisión independiente.
