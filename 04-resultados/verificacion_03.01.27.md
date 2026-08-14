# Verificación — agujero de fontanería de git en la regla 20 de CLAUDE.md

**Fecha:** 12/08/2026. **Ejecutor:** `constructor-motor` (`claude-sonnet-5`, sin respaldo:
no hubo rechazo del modelo). **Encargo:** bloque 4 del encargo directo del CEO del 12/08/2026
(«un solo intento contra el agujero de fontanería de git»). **Sin ficha WBS**: por orden expresa
del CEO transmitida en el reparto («PROHIBIDO CREAR TAREAS NUEVAS. Ninguna. Lo que encuentres y
no esté en el alcance va al informe como frase, nunca al WBS»). No se ha tocado
`00-direccion/WBS.md`, no se ha creado ninguna tarea nueva y no se ha hecho ningún commit.

Este artefacto documenta, por ejecución (regla 9 y regla 24 de CLAUDE.md — antigua regla 25 en
la numeración de antes del 12/08, ver tabla de correspondencia D-35), si el hook de fontanería
`reference-transaction` puede cerrar el hueco descrito en la sección "Qué tiene muro mecánico y
qué es solo prosa" de `CLAUDE.md`, medido el 09/08/2026: la secuencia `git add` + `git write-tree`
+ `git commit-tree -p HEAD` + `git update-ref` aterriza un borrado de líneas en `HEAD` sin pasar
por `pre-commit` ni `commit-msg`.

---

## 1. Entorno medido por ejecución

```
$ git --version
git version 2.43.0

$ git config --get core.hooksPath      (en el repositorio real)
.githooks

$ git config --get core.hooksPath      (en el repositorio aislado, tras `git config core.hooksPath .githooks`)
.githooks
```

Repositorio aislado del laboratorio (PASO 1): `/tmp/03.01.27-aislado` — `git init` propio,
`user.name`/`user.email` locales (`constructor-motor-lab` / `lab@example.com`), `.githooks/`
copiado por `cp` desde el `.githooks/pre-commit` y `.githooks/commit-msg` **reales** del
repositorio del proyecto, y copias de los tres ficheros que protege el bucle `for f in ...` de
`pre-commit`: `00-direccion/DECISIONES.md`, `00-direccion/LECCIONES.md`,
`04-resultados/registro-pruebas.md`. Contiene 5 commits base (3 en `main` más 1 en cada una de
`rama-b` y `rama-c`, que divergen de `main`) — cumple el mínimo de 3 commits y 2 ramas pedido en
el reparto. **En ningún momento se ha ejecutado nada de esto sobre el repositorio real** salvo
lo descrito en la sección 6 (PASO 5, instalación), que usa una rama desechable y nunca mueve
`HEAD` ni `refs/heads/main`.

Segundo repositorio local usado solo para la prueba de `fetch` (NO-ROMPE-5): `/tmp/03.01.27-aislado-remoto2`.

---

## 2. La sonda — PASO 2, la pregunta que decide todo

Se instaló `.githooks/reference-transaction` en el repositorio aislado, **ejecutable**
(`chmod +x`, comprobado con `ls -la` antes de cada prueba), con `core.hooksPath` apuntando a
`.githooks` (comprobado arriba). La sonda solo escribe a un log su `$1` y su stdin completo, y
sale 0 siempre (no bloquea nada).

### Veredicto binario: **SE DISPARA.**

La secuencia de fontanería completa —`git add` + `git write-tree` + `git commit-tree -p HEAD` +
`git update-ref HEAD <commit>` (y la variante `git update-ref refs/heads/main <commit>`)— sobre
una versión de `00-direccion/DECISIONES.md` con la línea `linea B` borrada, **sí dispara**
`reference-transaction`, con estados `prepared` y `committed`, y el `update-ref` se ejecuta con
éxito (exit 0 en la sonda porque la sonda no bloquea nada — solo mide).

### Log literal de la sonda para la secuencia de fontanería (tramo final del log completo, la invocación que corresponde al `update-ref HEAD <commit>` sin valor viejo explícito)

```
=== invocacion 2026-08-12T20:16:04Z ===
arg1($1)=prepared
--- stdin ---
0000000000000000000000000000000000000000 12571ad53ae74cc3cc55aa2cf6dea77b10102ffb HEAD
0000000000000000000000000000000000000000 12571ad53ae74cc3cc55aa2cf6dea77b10102ffb refs/heads/main
--- fin stdin ---
=== invocacion 2026-08-12T20:16:04Z ===
arg1($1)=committed
--- stdin ---
0000000000000000000000000000000000000000 12571ad53ae74cc3cc55aa2cf6dea77b10102ffb HEAD
0000000000000000000000000000000000000000 12571ad53ae74cc3cc55aa2cf6dea77b10102ffb refs/heads/main
--- fin stdin ---
```

**Hallazgo crítico dentro de la propia sonda:** el campo "old" (primera columna) que reporta
`git update-ref REF NUEVO` (sin dar el valor viejo explícito, tal y como pide la secuencia del
ataque) llega a `reference-transaction` como **cuarenta ceros**, aunque el ref **ya existía y
tenía contenido real** (`506b319fdb5211ce60abdeef5c1ccb1d18249948`). Se comprobó ampliando la
sonda para que, en estado `prepared`, leyera en vivo con `git rev-parse <refname>` (antes de que
la transacción se aplicase al disco) — y el valor real anterior SÍ aparece correctamente:

```
=== invocacion 2026-08-12T20:17:10Z ===
arg1($1)=prepared
--- stdin ---
0000000000000000000000000000000000000000 b9e7c901219fce88bd3037c8a688339b5b80025d HEAD
0000000000000000000000000000000000000000 b9e7c901219fce88bd3037c8a688339b5b80025d refs/heads/main
--- fin stdin ---
--- rev-parse en vivo durante prepared ---
refname=HEAD rev-parse-en-vivo=506b319fdb5211ce60abdeef5c1ccb1d18249948 (old-stdin=0000000000000000000000000000000000000000)
refname=refs/heads/main rev-parse-en-vivo=506b319fdb5211ce60abdeef5c1ccb1d18249948 (old-stdin=0000000000000000000000000000000000000000)
--- fin rev-parse en vivo ---
=== invocacion 2026-08-12T20:17:10Z ===
arg1($1)=committed
--- stdin ---
...
```

**Consecuencia de diseño:** el guardia NO puede fiarse del campo "old" de stdin cuando viene a
cero; tiene que resolverlo por `git rev-parse --verify -q <refname>` durante el estado
`prepared` (antes de que la transacción se aplique). Así se hizo (ver sección 4).

Cuando `git update-ref` SÍ recibe el valor viejo explícito (uso normal con compare-and-swap), el
campo "old" de stdin es correcto:

```
=== invocacion 2026-08-12T20:16:38Z ===
arg1($1)=prepared
--- stdin ---
12571ad53ae74cc3cc55aa2cf6dea77b10102ffb 506b319fdb5211ce60abdeef5c1ccb1d18249948 HEAD
12571ad53ae74cc3cc55aa2cf6dea77b10102ffb 506b319fdb5211ce60abdeef5c1ccb1d18249948 refs/heads/main
--- fin stdin ---
```

### Log literal completo de la sonda (las 268 líneas, todas las operaciones probadas en orden)

Guardado íntegro y sin editar en `/tmp/03.01.27-aislado-logs/sonda-reference-transaction.FULL.log`
(fuera del repositorio, no se ha commiteado nada). Cubre, en este orden: commit inicial normal
(TEST A), `checkout -b` + vuelta (TEST B), `branch -D` (TEST F, adelantado), `merge --no-ff`
(TEST C), `rebase` (TEST D), `fetch` (TEST E), y la secuencia de fontanería completa (dos veces,
para comprobar el comportamiento del campo "old"). Reproducido aquí íntegro por bloques en las
tablas y extractos de esta sección y la siguiente.

---

## 3. Qué operaciones normales disparan `reference-transaction`

| Operación | ¿Dispara? | Estados vistos | Notas |
|---|---|---|---|
| `git commit` (normal, en HEAD/main) | Sí | `prepared`, `committed` | Una invocación por estado, con dos líneas de stdin (`HEAD` y `refs/heads/<rama>`). |
| `git checkout -b <rama>` (crear rama en el commit actual) | Sí | `prepared`, `committed` | Ref creado con `old=0000...0`, `new=<sha actual>`. |
| `git checkout <otra-rama>` (volver, mismo commit) | **No** | — | Cambiar el símbolo `HEAD` entre ramas que apuntan al **mismo** commit no genera transacción de ref (no hay ningún ref cuyo valor cambie). |
| `git branch -D <rama>` | Sí | `prepared`, `committed`, `aborted`, `prepared`, `committed` (dos ciclos) | Ref pasa a `new=0000...0`. Un `branch -D` dispara la sonda dos veces (reflog + ref), con un `aborted` intermedio; no impide el borrado. |
| `git merge --no-ff` (con commit de merge) | Sí | `prepared`×3, `committed`×3 | Una invocación para `ORIG_HEAD`, otra para `HEAD`+`refs/heads/main` juntos. |
| `git rebase` (aunque solo mueva un commit) | Sí, muchas veces | `prepared`/`committed`/`aborted` repetidos | Toca `ORIG_HEAD`, `REBASE_HEAD`, `CHERRY_PICK_HEAD` (crea y borra, con `aborted` de por medio) y finalmente `HEAD`/la rama. El primer salto de `HEAD` (de la punta de la rama al commit "onto") es una transacción más, **no relacionada por ancestro** con el resto — ver hallazgo de la sección 5. |
| `git fetch <repo-local>` hacia un ref nuevo | Sí | `prepared`, `committed` | Sobre `refs/remotes/<remoto>/<rama>`, con `old=0000...0`. |

**Conclusión de esta tabla, medida antes de escribir el guardia (tal y como pide el reparto):**
el hook se dispara en prácticamente cualquier operación que mueva un ref, incluidas varias
transacciones internas por cada operación de alto nivel (`rebase` en particular puede disparar
más de 10 invocaciones para mover un solo commit). El guardia tiene que ser tolerante a eso.

---

## 4. FINAL 1 — el guardia

Con la sonda confirmando que la secuencia de fontanería sí dispara `reference-transaction`, se
escribió el guardia real. Contenido literal instalado en `.githooks/reference-transaction`
(idéntico en el repositorio aislado y en el repositorio real):

```bash
#!/usr/bin/env bash
# Guardia de la regla 20 de CLAUDE.md (registros que solo admiten anadir)
# via el hook de fontaneria reference-transaction. Tarea: bloque 4 del
# encargo del CEO del 12/08/2026 (ejecutado por constructor-motor, sin
# ficha WBS por orden expresa del CEO). Ver 04-resultados/verificacion_03.01.27.md
# para la medicion completa (sonda, bateria BLOQUEA/NO-ROMPE, limites).
#
# Cierra el agujero medido el 09/08/2026: `git add` + `git write-tree` +
# `git commit-tree -p HEAD` + `git update-ref` no pasa por pre-commit ni
# por commit-msg. Este hook si se dispara para esa secuencia (comprobado
# por ejecucion, paso 2 de 03.01.27).
#
# Solo puede abortar en el estado "prepared" (es el unico momento en que
# abortar tiene efecto). En "committed"/"aborted" no hay nada que hacer:
# consumimos stdin y salimos 0.
#
# Usa UNICAMENTE plumbing de LECTURA (git rev-parse, git cat-file, git
# diff --numstat, git merge-base --is-ancestor) para no recursar ni
# bloquear el lock de refs.

set -u

estado="${1:-}"

if [ "$estado" != "prepared" ]; then
  cat >/dev/null
  exit 0
fi

# Los mismos tres ficheros que protege el bucle `for f in ...` de pre-commit.
protegidos="00-direccion/DECISIONES.md 00-direccion/LECCIONES.md 04-resultados/registro-pruebas.md"

zero_re='^0+$'
fallo=0
motivos=""

while IFS=' ' read -r old new refname; do
  [ -z "${refname:-}" ] && continue

  # Solo nos interesan HEAD y refs/heads/** (incluye refs/heads/foo/bar).
  case "$refname" in
    HEAD) ;;
    refs/heads/*) ;;
    *) continue ;;
  esac

  # Ref borrado (valor nuevo cero) => es un borrado de ref, no reescritura
  # de contenido. No es lo que protege la regla 20.
  if printf '%s' "$new" | grep -qE "$zero_re"; then
    continue
  fi

  # Determinar el valor viejo REAL. El campo "old" del stdin puede venir a
  # cero aunque el ref ya existiese: `git update-ref REF NUEVO` (sin dar el
  # antiguo) no hace compare-and-swap y reporta 0000...0000 aunque el ref
  # tuviera contenido (medido por ejecucion, paso 2 de 03.01.27, con la
  # sonda leyendo en vivo por rev-parse durante "prepared"). En "prepared"
  # la transaccion todavia no se ha aplicado, asi que rev-parse todavia
  # devuelve el valor previo real: por eso podemos fiarnos de el aqui y no
  # del campo "old" de stdin.
  old_real="$old"
  if printf '%s' "$old" | grep -qE "$zero_re"; then
    if live=$(git rev-parse --verify -q "$refname" 2>/dev/null); then
      old_real="$live"
    else
      old_real=""
    fi
  fi

  [ -z "$old_real" ] && continue
  if printf '%s' "$old_real" | grep -qE "$zero_re"; then continue; fi
  [ "$old_real" = "$new" ] && continue

  # Si alguno de los dos extremos no es (o no resuelve a) un commit legible,
  # no podemos comparar arboles: dejamos pasar (no fabricamos un bloqueo
  # sobre algo que no sabemos leer).
  git cat-file -e "${old_real}^{commit}" 2>/dev/null || continue
  git cat-file -e "${new}^{commit}" 2>/dev/null || continue

  # Solo comparamos cuando old_real es antecesor real de new (o sea: new
  # extiende la MISMA linea de historia que old_real, exactamente el patron
  # del ataque descrito: `git commit-tree -p HEAD` fabrica un hijo directo
  # de HEAD). Si old_real NO es antecesor de new, mover el ref de uno a otro
  # no es "reescribir para borrar" sino "apuntar a otra historia" (p.ej. el
  # paso interno de `git rebase` que mueve HEAD de la punta de la rama
  # origen al commit "onto" antes de reaplicar los commits, o un checkout
  # entre ramas divergentes): eso NO es lo que protege la regla 20 y
  # bloquearlo rompe operaciones legitimas (medido por ejecucion: rompia
  # `git rebase` hasta añadir este chequeo). LIMITE DECLARADO: un atacante
  # que fabrique el commit nuevo con un padre distinto de HEAD (o sin
  # padre) y fuerce el ref con update-ref evita este guardia por diseño;
  # ver la seccion de limites del artefacto de verificacion.
  git merge-base --is-ancestor "$old_real" "$new" 2>/dev/null || continue

  for f in $protegidos; do
    # ¿Existia el fichero en el commit viejo? Si no existia, no hay nada
    # que proteger todavia.
    git cat-file -e "${old_real}:${f}" 2>/dev/null || continue

    numstat=$(git diff --numstat "$old_real" "$new" -- "$f" 2>/dev/null)
    [ -z "$numstat" ] && continue

    removed=$(printf '%s' "$numstat" | awk '{print $2}')
    case "$removed" in
      ''|*[!0-9]*) continue ;;   # "-" (binario) u otro formato: no lo tratamos como borrado de lineas
    esac

    if [ "$removed" -gt 0 ]; then
      fallo=1
      motivos="${motivos}BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): ${f} pierde ${removed} linea(s) al mover ${refname} de ${old_real} a ${new}.\n"
    fi
  done
done

if [ "$fallo" -eq 1 ]; then
  printf "%b" "$motivos" >&2
  echo "   Los registros de la regla 20 de CLAUDE.md solo admiten ANADIR." >&2
  echo "   Una correccion es una entrada nueva que cita a la anterior, nunca un borrado." >&2
  exit 1
fi

exit 0
```

Cumple los cuatro requisitos no negociables del reparto:
- Protege los **tres** ficheros del bucle de `pre-commit` (`protegidos=...`).
- Protege `HEAD` y `refs/heads/**` (`case "$refname" in HEAD) ;; refs/heads/*) ;; ...`).
- Solo usa plumbing de **lectura**: `git rev-parse --verify -q`, `git cat-file -e`,
  `git diff --numstat`, `git merge-base --is-ancestor`. Ninguna escritura, ningún riesgo de
  recursar sobre sí mismo ni de bloquear el lock de refs que la propia transacción ya tiene
  tomado.
- Tolera: el valor cero de 40 hexadecimales (creación de ref — `continue` si `new` es cero;
  resolución en vivo si `old` es cero), refs que no apuntan a commits (los `cat-file -e ...^{commit}`
  fallan y se hace `continue`, no se bloquea sobre algo que no se sabe leer), y repositorios sin
  commit previo (mismo camino: `git rev-parse --verify -q` falla limpiamente si el ref nunca
  existió, y se trata como creación, sin petar el script porque no se usa `set -e`).

### 4.1 Batería BLOQUEA — los tres ficheros protegidos

Estado de partida del repositorio aislado antes de esta batería: `HEAD` = `refs/heads/main` =
`ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820`.

**BLOQUEA-1 — `00-direccion/DECISIONES.md` (borra `linea B`):**

```
$ echo "..." | git commit-tree -p HEAD $(git write-tree)
newcommit=5c1e3bc99930bece1e24e8aca16359f918c540f3

$ git update-ref HEAD 5c1e3bc99930bece1e24e8aca16359f918c540f3
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 00-direccion/DECISIONES.md pierde 1 linea(s) al mover HEAD de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a 5c1e3bc99930bece1e24e8aca16359f918c540f3.
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 00-direccion/DECISIONES.md pierde 1 linea(s) al mover refs/heads/main de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a 5c1e3bc99930bece1e24e8aca16359f918c540f3.
   Los registros de la regla 20 de CLAUDE.md solo admiten ANADIR.
   Una correccion es una entrada nueva que cita a la anterior, nunca un borrado.
fatal: ref updates aborted by hook
exit=128

$ git update-ref refs/heads/main 5c1e3bc99930bece1e24e8aca16359f918c540f3
(mismo bloqueo)
exit=128
```

`git rev-parse HEAD` antes = después = `ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820`.
`git rev-parse refs/heads/main` antes = después = `ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820`.
`git show HEAD:00-direccion/DECISIONES.md | wc -l` antes = después = **7** (sin cambio).

**BLOQUEA-2 — `00-direccion/LECCIONES.md` (borra `linea A`):**

```
newcommit=a448a7c056d5870cb8bba4a349b4f9ab3be759b2
$ git update-ref HEAD a448a7c056d5870cb8bba4a349b4f9ab3be759b2
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 00-direccion/LECCIONES.md pierde 1 linea(s) al mover HEAD de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a a448a7c056d5870cb8bba4a349b4f9ab3be759b2.
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 00-direccion/LECCIONES.md pierde 1 linea(s) al mover refs/heads/main de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a a448a7c056d5870cb8bba4a349b4f9ab3be759b2.
fatal: ref updates aborted by hook
exit=128
$ git update-ref refs/heads/main a448a7c056d5870cb8bba4a349b4f9ab3be759b2
(mismo bloqueo) exit=128
```

`rev-parse HEAD` y `refs/heads/main` antes = después = `ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820`.
`git show HEAD:00-direccion/LECCIONES.md | wc -l` antes = después = **5**.

**BLOQUEA-3 — `04-resultados/registro-pruebas.md` (borra `linea A`):**

```
newcommit=260d771927c2e2d121009f0b5eae980fab17ee13
$ git update-ref HEAD 260d771927c2e2d121009f0b5eae980fab17ee13
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 04-resultados/registro-pruebas.md pierde 1 linea(s) al mover HEAD de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a 260d771927c2e2d121009f0b5eae980fab17ee13.
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 04-resultados/registro-pruebas.md pierde 1 linea(s) al mover refs/heads/main de ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 a 260d771927c2e2d121009f0b5eae980fab17ee13.
fatal: ref updates aborted by hook
exit=128
$ git update-ref refs/heads/main 260d771927c2e2d121009f0b5eae980fab17ee13
(mismo bloqueo) exit=128
```

`rev-parse HEAD` y `refs/heads/main` antes = después = `ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820`.
`git show HEAD:04-resultados/registro-pruebas.md | wc -l` antes = después = **5**.

**Las tres pruebas BLOQUEA: `git update-ref` sale con código distinto de 0 (128), el guardia
imprime su motivo, `rev-parse` de `HEAD` y `refs/heads/main` son idénticos antes y después, y el
recuento de líneas del fichero atacado no cambia.**

### 4.2 Batería NO ROMPE — las seis operaciones legítimas

**Hallazgo durante esta batería (se documenta, no se esconde, tal y como pide el reparto):** la
primera versión del guardia (sin el chequeo `git merge-base --is-ancestor`) **SÍ bloqueaba un
rebase legítimo**. El paso interno de `git rebase` mueve `HEAD` directamente de la punta de la
rama que se está rebasando al commit "onto" (aquí, la punta de `main`), antes de reaplicar los
commits — un salto entre dos puntos de historia **no relacionados por ancestro**. Al comparar el
contenido del fichero protegido entre esos dos puntos, el guardia veía "menos líneas" (porque
son ramas distintas con contenido distinto) y lo interpretaba como un borrado:

```
$ git rebase -q main
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 04-resultados/registro-pruebas.md pierde 1 linea(s) al mover HEAD de 2ecae4873fe5b134b57a83e42a91e4977d4f4827 a 8e538fb3040cb131c8b1fcaeaa6f6674c97ef42f.
fatal: ref updates aborted by hook
exit rebase=128
```

`git rebase --abort` restauró el estado exacto anterior sin corrupción (verificado: `rev-parse`
de la rama y de `main` idénticos a antes de intentar el rebase). Esto confirma que el guardia,
incluso al bloquear de más, **nunca deja el repositorio en un estado peor** — pero bloqueaba una
operación legítima, así que se corrigió: se añadió `git merge-base --is-ancestor "$old_real" "$new"`
para que el guardia **solo compare cuando `old_real` es antecesor real de `new`** — exactamente
el patrón del ataque (`commit-tree -p HEAD` fabrica un hijo directo de `HEAD`). Con esa corrección
se repitió la batería completa (BLOQUEA y NO-ROMPE) desde cero en un repositorio aislado limpio,
y los resultados que siguen son los de la versión corregida y final, la misma que quedó instalada.

**NO-ROMPE-1 — `git commit` normal que AÑADE líneas a `DECISIONES.md`:**
```
$ git commit -q -m "..."
exit=0
HEAD antes=ae1ad9cbb3d6e6e28ddc23d52fae1509cd771820 despues=70702820b740884d866bc4df51e00f61b1fe2831
(la linea nueva aparece al final del fichero: "linea NO-ROMPE-1 anadida")
```

**NO-ROMPE-2 — `git checkout -b` a otra rama y vuelta:**
```
$ git checkout -qb no-rompe-tmp
exit checkout -b=0  rama=no-rompe-tmp
$ git checkout -q main
exit checkout main=0  rama=main
$ git branch -D no-rompe-tmp
Deleted branch no-rompe-tmp (was 7070282).
HEAD tras volver = 70702820b740884d866bc4df51e00f61b1fe2831 (sin cambio)
```

**NO-ROMPE-3 — `git merge` con commit de merge:**
```
$ git checkout -q rama-b && printf '...\n' >> 00-direccion/LECCIONES.md && git commit -q -m "..."
exit checkout rama-b=0  exit commit rama-b=0
$ git checkout -q main
$ git merge --no-ff -q -m "03.01.23 prueba: NO-ROMPE-3 merge legitimo rama-b" rama-b
exit merge=0
HEAD antes=70702820b740884d866bc4df51e00f61b1fe2831 despues=b56a0db33df2b2dfef2c32b154a2fa166b2c48bd
(LECCIONES.md termina en "linea rama-b 1" / "linea rama-b 2 (para merge legitimo)": ambas presentes)
```

**NO-ROMPE-4 — `git rebase` (versión final, con el chequeo de ancestro):**
```
$ git checkout -qb rebase-feature && printf 'linea rebase-feature 1\n' >> 04-resultados/registro-pruebas.md && git commit -q -m "..."
$ git checkout -q main && printf 'linea main avanza (para forzar rebase real)\n' >> 00-direccion/DECISIONES.md && git commit -q -m "..."
$ git checkout -q rebase-feature
$ git rebase -q main
exit rebase=0
HEAD despues=10fc99d7abda89a100ebf462e54df4149fefd0a7
(registro-pruebas.md conserva "linea rebase-feature 1"; DECISIONES.md conserva "linea main avanza ...": nada se pierde)
```

**NO-ROMPE-5 — `git fetch` desde un segundo repositorio local hacia el repo guardado:**
```
$ git fetch -q /tmp/03.01.27-aislado-remoto2 +HEAD:refs/remotes/lab-remoto2/master
exit fetch=0
HEAD antes=d82fefef5a67d020871582ca909a1d3a919fe66f despues=d82fefef5a67d020871582ca909a1d3a919fe66f (sin cambio)
refs/remotes/lab-remoto2/master = b3357792052fb886ead66474d4fd108b4ad90f9d (ref nuevo creado)
```

**NO-ROMPE-6 — `git branch -D` de una rama de usar y tirar:**
```
$ git branch -q usar-y-tirar
$ git branch -D usar-y-tirar
Deleted branch usar-y-tirar (was d82fefe).
exit branch -D=0
HEAD antes=d82fefef5a67d020871582ca909a1d3a919fe66f despues=d82fefef5a67d020871582ca909a1d3a919fe66f (sin cambio)
```

**Con el guardia final (el que quedó instalado), las seis operaciones legítimas salen con
código 0 y ninguna pierde contenido.**

### 4.3 Lista de operaciones legítimas que el guardia bloquea

**Ninguna**, en la versión final instalada. La única que se bloqueó (`git rebase`, en la versión
intermedia del guardia sin el chequeo de ancestro) se documenta en la sección 4.2 y se corrigió
antes de instalar nada; no llegó a quedar instalada en esa forma.

---

## 5. Límites declarados (por dónde se salta)

1. **`core.hooksPath` es una configuración de cliente.** Cualquiera con acceso de escritura al
   repositorio puede saltarse cualquier hook de cliente —éste y todos los demás— con
   `git -c core.hooksPath=/dev/null <comando>` o simplemente cambiando `core.hooksPath` en la
   config local. **Esto no cambia el veredicto**: `pre-commit` tiene exactamente la misma
   propiedad con `--no-verify` (o con el mismo truco de `core.hooksPath`) y sigue contando como
   muro — es la misma clase de barrera (cliente, reversible, comprobada por ejecución) que las
   demás de esta sección de `CLAUDE.md`.

2. **Límite propio del guardia, medido por ejecución** (sección 4, ver el comentario que precede
   a `git merge-base --is-ancestor` en el propio script): el guardia solo compara contenido cuando `old_real` es **antecesor real**
   de `new` (verificado con `git merge-base --is-ancestor`). Esto es necesario para no bloquear
   operaciones legítimas como el salto interno de `git rebase` (ver hallazgo de la sección 4.2).
   Consecuencia: si alguien fabrica el commit nuevo con `git commit-tree` **sin** `-p HEAD` (o
   con un padre distinto), de modo que no sea descendiente de `HEAD`, y luego fuerza el ref con
   `git update-ref`, el guardia **no lo detecta por diseño**. Se comprobó por ejecución sobre el
   repositorio aislado, apuntando solo a una rama desechable:

   ```
   $ git merge-base --is-ancestor <HEAD-actual> <commit-huerfano-sin-padre>
   exit=1   (confirmado: NO es antecesor)
   $ git update-ref refs/heads/prueba-evasion <commit-huerfano-sin-padre>
   exit=0   (el guardia NO bloqueó: la variante sin `-p HEAD` evade el guardia)
   ```

   Este límite es idéntico en naturaleza al hueco original que la tarea busca cerrar: cerrar
   *este* también exigiría bloquear cualquier salto de ref no-ancestro hacia atrás en contenido,
   lo cual —medido en la sección 4.2— rompe `git rebase`, una operación legítima de uso diario.
   Se deja **declarado y sin cerrar**, no se inventa una tercera vía (el reparto lo prohíbe
   expresamente: "Prohibido proponer hooks de servidor, réplicas o comprobaciones periódicas" —
   y cerrar este límite del lado del guardia con la información actual exigiría exactamente ese
   tipo de heurística adicional, no probada, con riesgo de repetir el mismo patrón de falso
   positivo ya medido).

3. **El guardia solo puede abortar en estado `prepared`.** En `committed`/`aborted` no hay
   ninguna acción posible (la transacción ya se aplicó o ya se deshizo) — esto es una propiedad
   del hook, no una elección del guardia, y está documentado en su cabecera.

4. **El guardia no cubre `refs/tags/**` ni `refs/remotes/**`** (fuera del alcance del reparto,
   que pide proteger explícitamente "HEAD y refs/heads/**").

---

## 6. PASO 5 — instalación y prueba sobre el repositorio real

Se copió el guardia (contenido idéntico al de la sección 4) a
`/home/server/projects/bot-trading/.githooks/reference-transaction`, con `chmod +x`:

```
$ ls -la .githooks/
-rwxr-xr-x 1 server server  703 Jul 31 20:08 commit-msg
-rwxr-xr-x 1 server server 4265 Aug 12 22:14 pre-commit
-rwxrwxr-x 1 server server 4946 Aug 12 22:29 reference-transaction
$ bash -n .githooks/reference-transaction
(sin salida: sintaxis correcta)
```

Prueba sobre ficheros **reales**, sin poder dañar `HEAD` ni `main`:

- `00-direccion/DECISIONES.md` real tenía 405 líneas (`git show HEAD:... | wc -l`), sin
  modificaciones locales pendientes.
- Se construyó una copia con la última línea no vacía borrada (`head -n -1`), y se inyectó **en
  el índice, sin tocar el fichero en disco**, con `git hash-object -w` +
  `git update-index --cacheinfo` (así el working tree del repositorio real nunca se tocó:
  verificado con `wc -l 00-direccion/DECISIONES.md` = 405 después de inyectar en el índice).
- Se creó `git branch prueba-fontaneria HEAD` (rama desechable, en la punta actual).
- Se construyó el commit del ataque con `git write-tree` + `git commit-tree -p HEAD`, y se
  intentó `git update-ref refs/heads/prueba-fontaneria <commit-con-borrado>` — **nunca
  `HEAD` ni `refs/heads/main`**.

```
$ git update-ref refs/heads/prueba-fontaneria b163d89abf0f1179ae26d2e2d4de1d35f6c68a30
BLOQUEADO (regla 20 de CLAUDE.md, via reference-transaction): 00-direccion/DECISIONES.md pierde 1 linea(s) al mover refs/heads/prueba-fontaneria de 9f29da053ab26ec9c3d9d059c9ca6db75a678c33 a b163d89abf0f1179ae26d2e2d4de1d35f6c68a30.
   Los registros de la regla 20 de CLAUDE.md solo admiten ANADIR.
   Una correccion es una entrada nueva que cita a la anterior, nunca un borrado.
fatal: ref updates aborted by hook
exit=128
```

Estado tras el intento: `git rev-parse HEAD` = `git rev-parse refs/heads/main` =
`git rev-parse refs/heads/prueba-fontaneria` = `9f29da053ab26ec9c3d9d059c9ca6db75a678c33`
(la rama de prueba nunca se movió — el guardia mordió sobre el fichero real). Limpieza:

```
$ git branch -D prueba-fontaneria
Deleted branch prueba-fontaneria (was 9f29da0).
$ git reset HEAD -- 00-direccion/DECISIONES.md
$ git status --porcelain -- 00-direccion/DECISIONES.md
(vacío)
$ wc -l 00-direccion/DECISIONES.md
405 00-direccion/DECISIONES.md
```

Rama de prueba borrada, índice limpio para ese fichero, fichero real intacto en 405 líneas,
`HEAD` y `main` nunca se movieron.

**Nota sobre el estado del repositorio real durante esta tarea:** al llegar a este paso, `git
status --porcelain` del repositorio real ya mostraba varios ficheros modificados sin commit
(`.claude/agents/critico-codigo.md`, `.claude/agents/validador.md`, `.claude/settings.json`,
`.githooks/pre-commit`, `00-direccion/WBS.md`, `00-direccion/expedientes/03.01.17.md`,
`04-resultados/verificacion_03.01.24.md`, `05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx`,
`05-vista-ceo/ultimo_estado.json`, y un fichero nuevo sin trackear
`04-resultados/verificacion_03.01.25_guardia_wbs.md`). Comprobado por `ls -la --time-style=full-iso`:
sus fechas de modificación (22:14-22:28) caen dentro de la ventana de esta misma sesión pero
**ninguno de esos ficheros fue tocado por este trabajo** — esta tarea solo leyó
`00-direccion/DECISIONES.md`, `00-direccion/LECCIONES.md` y `04-resultados/registro-pruebas.md`
(sin dejar diferencia, comprobado en la sección 7) y solo escribió el fichero nuevo
`.githooks/reference-transaction` y este propio artefacto. Es evidencia de otra actividad
concurrente en el mismo repositorio (probablemente otro agente trabajando en paralelo sobre otra
tarea del WBS), no de este trabajo.

---

## 7. `git status --porcelain` del repositorio real, tras terminar

```
 M .claude/agents/critico-codigo.md
 M .claude/agents/validador.md
 M .claude/settings.json
 M .githooks/pre-commit
 M 00-direccion/WBS.md
 M 00-direccion/expedientes/03.01.17.md
 M 04-resultados/verificacion_03.01.24.md
 M 05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx
 M 05-vista-ceo/ultimo_estado.json
?? .githooks/reference-transaction
?? 04-resultados/verificacion_03.01.25_guardia_wbs.md
```

Las nueve líneas `M` y el fichero `04-resultados/verificacion_03.01.25_guardia_wbs.md` son
ajenos a este trabajo (ver nota de la sección 6). Lo que aporta esta tarea es exactamente:
`.githooks/reference-transaction` (nuevo, el guardia) y este mismo artefacto
(`04-resultados/verificacion_03.01.27.md`, que en el momento de este `git status` aún no se
había escrito a disco). `00-direccion/WBS.md` no se ha tocado por esta tarea — su diferencia de
una línea es la misma que ya estaba presente al empezar (confirmado: esta tarea nunca abrió ese
fichero en modo escritura). No se ha hecho ningún commit.

---

## 8. VEREDICTO FINAL

# **FINAL 1 — MURO.**

El hook `reference-transaction`, con `core.hooksPath` apuntando a `.githooks` (ya vigente en el
repositorio real), **cierra el agujero de fontanería medido el 09/08/2026** para los tres
ficheros de la regla 20 de CLAUDE.md, en `HEAD` y en `refs/heads/**`: la secuencia
`git add` + `git write-tree` + `git commit-tree -p HEAD` + `git update-ref` que antes aterrizaba
un borrado sin pasar por ningún hook, ahora se bloquea (código de salida 128, motivo impreso,
refs sin mover — batería BLOQUEA, sección 4.1, y prueba sobre fichero real, sección 6). Las seis
operaciones legítimas probadas (`commit` que añade, `checkout -b`+vuelta, `merge --no-ff`,
`rebase`, `fetch`, `branch -D`) no se rompen (batería NO-ROMPE, sección 4.2). Quedan dos límites
declarados y verificados por ejecución (sección 5): la vía genérica de cliente
`core.hooksPath`/`--no-verify` (que no cambia el veredicto, es la misma propiedad que ya tiene
`pre-commit`), y el caso concreto de un commit fabricado sin `-p HEAD` que evade el chequeo de
ancestro necesario para no romper `rebase`.
