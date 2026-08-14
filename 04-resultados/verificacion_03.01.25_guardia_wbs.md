# Verificación 03.01.25 — Guardia de la métrica L-027 sobre el WBS en `.githooks/pre-commit`

**Agente:** `constructor-motor` · **Modelo:** `claude-sonnet-5`. No se usó el respaldo
`claude-opus-5`: no hubo rechazo ni atasco.

**Numeración de reglas usada en este informe:** la NUEVA (D-35, 12/08/2026, ver tabla de
correspondencia al final de la sección "Las 28 reglas" en `CLAUDE.md`), confirmada por `grep`
directo sobre `CLAUDE.md` antes de escribir esta línea (`grep -n "^## Las" CLAUDE.md` → `23:##
Las 28 reglas`).

**Alcance de esta orden:** el guardia YA EXISTE (bloque citado por el comentario
`# --- Metrica L-027 (00-direccion/LECCIONES.md) sobre el WBS ---` en `.githooks/pre-commit`,
construido en una tirada anterior — ver `04-resultados/verificacion_03.01.25.md`). Esta orden NO
lo construye: lo verifica por inyección real (regla 24 de CLAUDE.md) contra el WBS de HOY, y solo
si sale gratis, lo amplía con la comprobación de punteros a expedientes.

Todo lo de este informe se ejecutó en un **clon aislado**, nunca sobre el repositorio real:

```
git clone /home/server/projects/bot-trading <scratchpad>/clon
cd <scratchpad>/clon
git config core.hooksPath .githooks
```

Ruta real del clon usada: `/tmp/claude-1000/-home-server-projects-bot-trading/5ae9e134-fcfd-48f0-a192-c333c77120c0/scratchpad/clon`.
HEAD del clon al arrancar: `9f29da0 03.01.23: restituir el contrato del encadenador en /autonomo y taparlo en .gitignore`
(idéntico al HEAD del repositorio real en el momento de clonar).

---

## PASO 0 — Medir el terreno (sin dar por buena ninguna cifra dictada)

Comando ejecutado sobre el **repositorio real** (`/home/server/projects/bot-trading`):

```
$ grep -cE '^\| *[0-9]{2}\.[0-9]{2}\.[0-9]{2} *\|' 00-direccion/WBS.md
64
$ grep -oE 'expedientes/[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.md' 00-direccion/WBS.md | sort -u | wc -l
25
$ ls -1 00-direccion/expedientes/ | wc -l
25
```

Listado de los 25 punteros distintos citados en el WBS (`grep -oE 'expedientes/[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.md' 00-direccion/WBS.md | sort -u`):

```
expedientes/01.01.03.md   expedientes/03.01.03.md   expedientes/03.01.21.md
expedientes/01.02.03.md   expedientes/03.01.04.md   expedientes/03.01.23.md
expedientes/01.02.04.md   expedientes/03.01.08.md   expedientes/04.01.01.md
expedientes/02.01.02.md   expedientes/03.01.11.md   expedientes/04.01.04.md
expedientes/02.02.01.md   expedientes/03.01.13.md   expedientes/04.03.06.md
expedientes/02.02.02.md   expedientes/03.01.15.md   expedientes/04.03.07.md
expedientes/02.02.03.md   expedientes/03.01.16.md   expedientes/07.01.01.md
expedientes/02.03.01.md   expedientes/03.01.17.md   expedientes/07.01.03.md
expedientes/03.01.18.md
```

Comprobación de que el conjunto de punteros y el conjunto de ficheros en disco son el MISMO
conjunto (no solo la misma cuenta):

```
$ diff <(grep -oE 'expedientes/[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.md' 00-direccion/WBS.md | sed 's#expedientes/##' | sort -u) \
       <(ls -1 00-direccion/expedientes/ | sort -u)
$ echo "diff exit=$?"
diff exit=0
```

**Cifras del PASO 0: 64 filas de tarea · 25 punteros `expedientes/NN.NN.NN.md` distintos · 25
ficheros en `00-direccion/expedientes/` · coinciden 1:1 (diff vacío).** Esto es lo que hace
posible que A1 (más abajo) dé cero falsos positivos hoy.

---

## PASO 1 — Seis inyecciones obligatorias (clon aislado, `git config core.hooksPath .githooks`)

Metodología común a los seis casos: se resetea el clon a `9f29da0` antes de cada caso
(`git reset --hard 9f29da0`), se inyecta la corrupción, se comprueba con `diff` que **cambió
algo de verdad** respecto al `HEAD` del clon (regla del hallazgo L-026 de
`00-direccion/LECCIONES.md`, confirmado por `grep -n "^## L-026" 00-direccion/LECCIONES.md`), y
solo entonces se intenta `git commit` real. Las filas víctima se localizan **por estructura**
(la fila N-ésima que cumple el patrón `^\| *[0-9]{2}\.[0-9]{2}\.[0-9]{2} *\|`), nunca copiando su
prosa.

### C1 — Control: WBS real sin tocar → DEBE PASAR

El WBS real, tal cual, no genera ningún diff staged por sí solo (ya está en `HEAD`), así que para
poder ejercitar de verdad el guardia sobre el contenido real se añadió una línea en blanco al
final del fichero (cambio no estructural: no toca ninguna fila `| CC.CC.CC | ... |`).

```
$ printf '\n' >> 00-direccion/WBS.md
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
305a306
>
$ echo "diff exit=$?"
diff exit=1        # (diff != HEAD, confirma que SÍ cambió algo real)
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C1 control WBS real con linea en blanco final, sin romper estructura"
[main bedea4a] meta: C1 control WBS real con linea en blanco final, sin romper estructura
 1 file changed, 1 insertion(+)
```

**Veredicto C1: PASA.** (exit del `git commit` = 0). El guardia NO da falso positivo sobre el WBS
real de hoy.

### C2 — Dos filas de tarea adyacentes fusionadas en una línea → DEBE REBOTAR

Localización por estructura: primer par de líneas consecutivas que cumplen el patrón de fila de
tarea (resultaron ser las líneas 87 y 88, correspondientes a `01.01.01` y `01.01.02`). Se fusionan
quitando el salto de línea entre ellas (el incidente exacto de L-027).

```
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
87,88c87
< | 01.01.01 | Aprobar plan y reglas | CEO | ... |
< | 01.01.02 | Aprobar criterios de la puerta G1 | CEO | ... |
---
> | 01.01.01 | Aprobar plan y reglas | CEO | ... || 01.01.02 | Aprobar criterios ... |
$ echo "diff exit=$?"
diff exit=1
$ wc -l 00-direccion/WBS.md
304 00-direccion/WBS.md    # (era 305, confirma la fusión)
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C2 filas 01.01.01 y 01.01.02 fusionadas sin salto de linea"
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 01.01.01: 13 campos (deberian ser 7)
$ echo "EXIT=$?"
EXIT=1
```

**Veredicto C2: REBOTA.** Correcto.

### C3 — Una fila de tarea partida en dos líneas → DEBE REBOTAR

Localización por estructura: la primera fila de tarea (línea 87, `01.01.01`), partida por la
mitad de su longitud (punto de corte estructural, no elegido por el contenido).

```
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
87c87,88
< | 01.01.01 | Aprobar plan y reglas | CEO | ... aprobación decla
> | 01.01.01 | Aprobar plan y reglas | CEO | ... aprobación decla
> rada en las decisiones del 01/08 ... |
$ echo "diff exit=$?"
diff exit=1
$ wc -l 00-direccion/WBS.md
306 00-direccion/WBS.md    # (era 305, confirma la partición)
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C3 fila 01.01.01 partida en dos lineas"
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 01.01.01: 6 campos (deberian ser 7)
$ echo "EXIT=$?"
EXIT=1
```

**Veredicto C3: REBOTA.** Correcto.

### C4 — Una barra vertical de más dentro de la celda de estado de una fila (8 campos) → DEBE REBOTAR

Localización por estructura: primera fila de tarea (línea 87, `01.01.01`); se comprobó primero
que la tabla tiene 5 columnas (`grep -n '^| Código\|^|---' 00-direccion/WBS.md` → cabecera
`| Código | Tarea | Responsable | Depende de | Estado |`, 5 columnas = 7 campos al partir por
`|`), y se insertó una barra vertical de más dentro del último campo (celda Estado), en un punto
intermedio localizado por longitud, no por contenido.

```
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
87c87
< | 01.01.01 | ... aprobación declarada en las decisio nes del 01/08 ... |
---
> | 01.01.01 | ... aprobación declarada en las decisio|nes del 01/08 ... |
$ echo "diff exit=$?"
diff exit=1
$ sed -n '87p' 00-direccion/WBS.md | awk -F'|' '{print "NF="NF}'
NF=8
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C4 barra vertical de mas en la celda de estado de 01.01.01"
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 01.01.01: 8 campos (deberian ser 7)
$ echo "EXIT=$?"
EXIT=1
```

**Veredicto C4: REBOTA.** Correcto.

### C5 — Una columna de menos en una fila de tarea (6 campos) → DEBE REBOTAR

Localización por estructura: primera fila de tarea (línea 87, `01.01.01`); se elimina el cuarto
campo completo (`Depende de`) tras hacer `split("|")` sobre la línea (localizado por posición de
campo, no por su texto).

```
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
87c87
< | 01.01.01 | Aprobar plan y reglas | CEO | — | **hecha** 03/08 ... |
---
> | 01.01.01 | Aprobar plan y reglas | CEO | **hecha** 03/08 ... |
$ echo "diff exit=$?"
diff exit=1
$ sed -n '87p' 00-direccion/WBS.md | awk -F'|' '{print "NF="NF}'
NF=6
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C5 columna Depende de eliminada en fila 01.01.01"
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 01.01.01: 6 campos (deberian ser 7)
$ echo "EXIT=$?"
EXIT=1
```

**Veredicto C5: REBOTA.** Correcto.

### C6 — Tolerancia: línea de prosa fuera de tabla con la barra vertical literal → DEBE PASAR

Se inyectó, fuera de cualquier tabla (empieza por `- **`, no por `| CC.CC.CC |`), una línea nueva
de prosa que **lleva la barra vertical de verdad**, con el comando literal `awk -F'|' '{print
NF}'` dentro. La línea inyectada, mostrada tal cual quedó en el fichero:

```
- **Prueba de tolerancia C6 (inyeccion de verificacion, constructor-motor, 03.01.25):** esta linea es PROSA fuera de cualquier tabla y contiene el comando literal con la barra vertical dentro, `awk -F'|' '{print NF}'`, para comprobar que el guardia de la metrica L-027 la TOLERA y no bloquea el commit.
```

```
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
42a43
> - **Prueba de tolerancia C6 ...** ... `awk -F'|' '{print NF}'` ...
$ echo "diff exit=$?"
diff exit=1
$ git add 00-direccion/WBS.md
$ git commit -m "meta: C6 linea de prosa fuera de tabla con barra vertical literal, prueba de tolerancia"
[main ae80ba9] meta: C6 linea de prosa fuera de tabla con barra vertical literal, prueba de tolerancia
 1 file changed, 1 insertion(+)
$ echo "EXIT=$?"
EXIT=0
```

**Veredicto C6: TOLERA (pasa).** Correcto: la línea de prosa con la barra vertical literal no
bloquea el commit, tal como exige el aviso escrito en la propia fila `03.01.25` del WBS.

**Ningún caso C1-C6 dio resultado distinto del esperado. No hay hallazgo de falso
negativo/positivo en el guardia ya construido.**

---

## PASO 2 — Ampliación: comprobar que todo puntero `expedientes/NN.NN.NN.md` apunta a un fichero existente

### Diseño

Dentro del mismo bloque `if git diff --cached --name-only | grep -qx '00-direccion/WBS.md'; then
... fi` (reutilizando `$wbs_stage` y `$wbs_ok` ya calculados por el bloque L-027 existente), se
añadió, justo antes del `fi` de cierre:

```bash
  # Ampliacion: todo puntero expedientes/NN.NN.NN.md citado en el WBS en stage debe
  # apuntar a un fichero que exista EN EL INDICE (":00-direccion/...", stage 0), no
  # en el arbol de trabajo. Esto acepta un expediente nuevo anadido en el mismo commit
  # que lo referencia, sin exigir que ya estuviera en HEAD.
  if [ "$wbs_ok" = "1" ]; then
    faltan=$(printf '%s\n' "$wbs_stage" | grep -oE 'expedientes/[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.md' | sort -u | while read -r p; do git cat-file -e ":00-direccion/$p" 2>/dev/null || echo "$p"; done) || true
    if [ -n "$faltan" ]; then
      echo "BLOQUEADO (ampliacion L-027): punteros a expedientes que no existen en este commit:"
      echo "$faltan" | sed 's#^#   00-direccion/#'
      fallo=1
    fi
  fi
```

Comprobación por `git cat-file -e ":00-direccion/<puntero>"` (sintaxis de dos puntos = ruta en el
ÍNDICE, stage 0), no en `HEAD` ni en el árbol de trabajo: por eso un expediente nuevo `git add`-eado
en el mismo commit que lo referencia cuenta como existente (exigencia de A3), y un fichero que
solo está en el disco sin `git add` no cuenta.

### Tope de 10 líneas ejecutables — cuenta hecha

```
$ git diff --numstat -- .githooks/pre-commit
12      0       .githooks/pre-commit
$ git diff .githooks/pre-commit | grep '^+' | grep -v '^+++' | grep -c '^+  #'
4     # líneas de comentario
$ git diff .githooks/pre-commit | grep '^+' | grep -v '^+++' | grep -vc '^+  #'
8     # líneas ejecutables
```

**12 líneas añadidas en total → 4 de comentario (no cuentan) → 8 líneas ejecutables. 8 ≤ 10: la
ampliación SÍ cabe en el tope.**

### A1 — WBS real de hoy con sus punteros actuales → DEBE PASAR (cero falsos positivos)

Base: clon con la ampliación ya instalada (`git commit` previo de instalación, no cuenta como
caso de prueba). Igual que en C1, se forzó un cambio trivial (línea en blanco final) para que
`00-direccion/WBS.md` entre en el diff staged y se ejecute la ruta del guardia sobre los 25
punteros reales.

```
$ printf '\n' >> 00-direccion/WBS.md
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
305a306
>
$ echo "diff exit=$?"
diff exit=1
$ git add 00-direccion/WBS.md
$ git commit -m "meta: A1 WBS real de hoy con sus punteros actuales, cero falsos positivos esperados"
[main fc4acd4] meta: A1 WBS real de hoy con sus punteros actuales, cero falsos positivos esperados
 1 file changed, 1 insertion(+)
$ echo "EXIT=$?"
EXIT=0
```

**Veredicto A1: PASA.** Los 25 punteros reales de hoy resuelven todos contra ficheros existentes
en el índice; cero falsos positivos.

### A2 — Puntero a un expediente que no existe → DEBE REBOTAR

Se localizó la fila de tarea `03.01.25` (la propia tarea en curso, sin puntero real hoy) por
estructura (campo código == `03.01.25` tras `split("|")`), y se le añadió dentro de su celda de
estado la cita `` `00-direccion/expedientes/99.99.99.md` ``, un fichero que se comprobó que no
existe ni en disco ni en `HEAD`:

```
$ ls 00-direccion/expedientes/99.99.99.md
ls: cannot access '00-direccion/expedientes/99.99.99.md': No such file or directory
$ diff <(git show HEAD:00-direccion/WBS.md) 00-direccion/WBS.md
136c136
< | 03.01.25 | ... la ficha D-29 no está firmada en `DECISIONES.md`. |
---
> | 03.01.25 | ... la ficha D-29 no está firmada en `DECISIONES.md`.  Puntero de prueba A2: `00-direccion/expedientes/99.99.99.md`. |
$ echo "diff exit=$?"
diff exit=1
$ sed -n '136p' 00-direccion/WBS.md | awk -F'|' '{print "NF="NF}'
NF=7          # (la fila sigue teniendo 7 campos: no dispara L-027, solo la ampliación)
$ git add 00-direccion/WBS.md
$ git commit -m "meta: A2 puntero a expediente inexistente 99.99.99, debe rebotar"
BLOQUEADO (ampliacion L-027): punteros a expedientes que no existen en este commit:
   00-direccion/expedientes/99.99.99.md
$ echo "EXIT=$?"
EXIT=1
```

**Veredicto A2: REBOTA.** Correcto, y queda demostrado que el bloqueo lo dispara la AMPLIACIÓN
(mensaje `BLOQUEADO (ampliacion L-027)`), no la métrica L-027 original (la fila sigue en 7
campos).

### A3 — Expediente nuevo añadido en el mismo commit que lo referencia → DEBE PASAR

Misma fila `03.01.25`, ahora citando `` `00-direccion/expedientes/03.01.25.md` ``, y creando ese
fichero nuevo en el mismo commit (`git add` de ambos ficheros). Se comprobó primero que el
fichero NO estaba en `HEAD`:

```
$ git show HEAD:00-direccion/expedientes/03.01.25.md
fatal: path '00-direccion/expedientes/03.01.25.md' exists on disk, but not in 'HEAD'
$ echo "exit=$?"
exit=128
$ git add 00-direccion/WBS.md 00-direccion/expedientes/03.01.25.md
$ git status --porcelain
M  00-direccion/WBS.md
A  00-direccion/expedientes/03.01.25.md
$ git commit -m "meta: A3 expediente nuevo 03.01.25.md anadido en el mismo commit que lo referencia, debe pasar"
[main 78de500] meta: A3 expediente nuevo 03.01.25.md anadido en el mismo commit que lo referencia, debe pasar
 2 files changed, 5 insertions(+), 1 deletion(-)
 create mode 100644 00-direccion/expedientes/03.01.25.md
$ echo "EXIT=$?"
EXIT=0
```

**Veredicto A3: PASA.** Correcto: la ampliación no exige que el expediente ya estuviera en `HEAD`,
solo que esté en el índice del propio commit.

**A1, A2 y A3 salieron los tres bien → la ampliación SE APLICÓ al repositorio real**
(`/home/server/projects/bot-trading/.githooks/pre-commit`), mismo diff exacto de 12 líneas (8
ejecutables) verificado con `git diff -- .githooks/pre-commit` sobre el repositorio real tras la
edición. La edición quedó en el árbol de trabajo del repositorio real, sin commitear (el commit de
esta tarea corresponde al cierre por `secretario`/`orquestador`, no a este agente).

---

## Veredictos explícitos que pide el CEO

1. **¿MUERDE hoy sobre el WBS de hoy?** SÍ. C1 y A1 (WBS real de hoy, 64 filas de tarea y 25
   punteros reales) pasan sin falso positivo, y C2/C3/C4/C5/A2 (corrupciones reales, inyectadas y
   confirmadas por `diff`) rebotan todos con `git commit` real (exit 1) sobre el clon con
   `core.hooksPath` apuntando a `.githooks`.
2. **¿TOLERA la barra vertical en prosa?** SÍ. C6 inyectó una línea de prosa fuera de tabla con el
   comando literal `awk -F'|' '{print NF}'` (barra vertical real, mostrada arriba tal cual quedó
   en el fichero) y el commit pasó (exit 0).

---

## LO QUE ESTE GUARDIA NO CUBRE

- **Solo mira la versión en STAGE, no el árbol de trabajo.** Todo el guardia (métrica L-027 y su
  ampliación) lee `git show ':00-direccion/WBS.md'`, es decir, el contenido exactamente tal como
  quedará en el commit tras `git add`. Un `00-direccion/WBS.md` roto en el árbol de trabajo pero
  no puesto en stage (o puesto en stage con una versión antigua y luego editado sin volver a
  `git add`) no lo ve el guardia, porque no es lo que va a entrar en el commit.
- **La vía de fontanería de git no dispara hooks.** `git add` + `write-tree` + `commit-tree` +
  `update-ref` deposita un commit en `HEAD` sin pasar por `pre-commit`, sin usar `--no-verify` y
  sin que ningún patrón `deny` lo alcance. Este hueco ya está registrado en `CLAUDE.md`, sección
  "Qué tiene muro mecánico y qué es solo prosa" (localizado por `grep -n "COBERTURA MEDIDA"
  CLAUDE.md`), cita literal con la numeración ya actualizada por D-35 (`CLAUDE.md` se edita in
  situ, no es un registro de solo-añadir): *"COBERTURA MEDIDA EL 09/08/2026: muerde en `git
  commit` y `git commit -a`, y NO cubre la vía de fontanería de git (`add` + `write-tree` +
  `commit-tree` + `update-ref`), que aterriza el borrado en `HEAD` sin disparar ningún hook, sin
  usar `--no-verify` y sin que ningún patrón `deny` lo alcance. Reproducido por ejecución en
  repositorio aislado. Hasta que se cierre, este muro está VERIFICADO SOLO PARCIALMENTE (regla 24
  de CLAUDE.md). Su reparación es tarea del checkpoint del lunes."* No se ha tocado ni cerrado ese
  hueco en esta tarea: sigue abierto.
- **No comprueba el formato interno de los ficheros de `00-direccion/expedientes/`.** Ni la
  métrica L-027 ni la ampliación de esta tarea leen el CONTENIDO de los ficheros
  `NN.NN.NN.md` referenciados: solo comprueban que el puntero citado en el WBS resuelve a un
  fichero que existe en el índice del commit (`git cat-file -e`). Un expediente vacío, corrupto,
  mal formado o con el código WBS equivocado dentro pasaría el guardia igual, porque el fichero
  existe.
- **No comprueba lo inverso:** que todo fichero de `00-direccion/expedientes/` esté citado por
  algún puntero en el WBS (expedientes huérfanos no referenciados no se detectan).
- **No comprueba que el código de tarea del nombre del fichero (`NN.NN.NN.md`) coincida con la
  fila del WBS donde aparece el puntero** (p. ej. que la fila `03.01.25` no cite por error
  `expedientes/03.01.24.md`): solo exige que el fichero citado exista, no que sea coherente con la
  fila que lo cita.
- **El AVISO (regla 13 de CLAUDE.md, numeración vieja — regla 12 de la nueva) sobre referencias
  por número de línea es solo un `echo` de aviso, no bloquea** (`fallo` no se marca a 1 en ese
  bloque): queda fuera del alcance de esta verificación porque no es parte del bloque L-027, pero
  se deja anotado porque comparte fichero.

---

## `git status --porcelain` del repositorio REAL (demuestra que ninguna inyección aterrizó ahí)

Salida literal al terminar esta tarea:

```
$ cd /home/server/projects/bot-trading && git status --porcelain
 M .claude/agents/critico-codigo.md
 M .claude/agents/validador.md
 M .claude/settings.json
 M .githooks/pre-commit
?? 04-resultados/verificacion_03.01.25_guardia_wbs.md
```

**Las dos líneas que corresponden a esta tarea son exactamente las esperadas:** ` M
.githooks/pre-commit` (la ampliación de 12 líneas, 8 ejecutables, idéntica a la probada en el clon
tras superar A1/A2/A3) y `?? 04-resultados/verificacion_03.01.25_guardia_wbs.md` (este mismo
artefacto).

**Las otras tres líneas —`.claude/agents/critico-codigo.md`, `.claude/agents/validador.md`,
`.claude/settings.json`— NO las causó esta tarea.** Nunca se abrieron ni se editaron esos tres
ficheros en esta sesión (ningún comando de este informe los toca; búsqueda del propio historial
de comandos ejecutados confirma cero referencias a ellos). Comprobado por `ls -la
--time-style=full-iso` sobre los cinco ficheros relevantes: la edición de
`.claude/agents/critico-codigo.md` es de `22:15:08`, la de `.claude/agents/validador.md` de
`22:15:11` y la de `.claude/settings.json` de `22:17:51`, todas **posteriores** a mi edición de
`.githooks/pre-commit` (`22:14:47`) y **anteriores** a escribir este artefacto (`22:19:23`): son
cambios de otra tarea/agente corriendo en paralelo sobre el mismo repositorio real durante esta
misma tirada (el patrón `CANARIO0301240` en el diff de `settings.json` apunta a la tarea
`03.01.24`, ajena a esta orden). No se han revertido ni tocado: no es mi tarea decidir sobre
trabajo concurrente de otro agente, y revertirlo sería destructivo sobre algo que no me consta que
esté roto.

Ninguna de las inyecciones C1-C6/A1-A3 de esta tarea (WBS roto, `expedientes/99.99.99.md`, líneas
de prosa de prueba) tocó el repositorio real: todas vivieron y murieron en el clon de
`/tmp/claude-1000/-home-server-projects-bot-trading/5ae9e134-fcfd-48f0-a192-c333c77120c0/scratchpad/clon`,
que es descartable y no forma parte del repositorio del proyecto.

No se tocó `00-direccion/WBS.md` real, ni `02-datos/reservado/`, ni la celda de estado de
`03.01.25` (la escribe `secretario` al cerrar).
