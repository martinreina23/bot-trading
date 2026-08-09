# Verificación 03.01.25 — Guardia en `.githooks/pre-commit` para la métrica de L-027 sobre el WBS

**Modelo declarado:** `claude-sonnet-5`. No se usó el respaldo `claude-opus-5`: no hubo atascos.

**Qué se construyó:** un bloque nuevo en `.githooks/pre-commit` (símbolo del comentario:
`# --- Metrica L-027 (00-direccion/LECCIONES.md) sobre el WBS ---`), añadido **después** del
bloque de la regla 13 de CLAUDE.md y **antes** del `exit $fallo` final. No se tocó ningún bloque
existente (reglas 27, 22, 21, 13 de CLAUDE.md).

**Qué hace el bloque:**
1. Solo actúa si `00-direccion/WBS.md` está en el conjunto en stage (`git diff --cached --name-only`).
2. Lee el contenido **EN STAGE** con `git show ':00-direccion/WBS.md'` — nunca el fichero de
   trabajo — que es exactamente la versión que va a entrar en el commit.
3. Con `awk -F'|'` selecciona SOLO las líneas que **empiezan** por `| CC.CC.CC |` (patrón
   `^[ \t]*\| *[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9] *\|`). La barra vertical citada en prosa fuera
   de tabla (el propio WBS la cita al explicar esta misma métrica) no empieza así y queda fuera.
4. Para cada fila de tarea comprueba `NF != 7` (métrica de L-027, tal cual está normativizada en
   el propio `00-direccion/WBS.md`, sección "Estados y cadencia de este WBS": *"Una fila de tarea
   correcta da 7 al partirla por la barra vertical — `awk -F'|' '{print NF}'` devuelve 7"*).
5. Si alguna fila falla, **bloquea el commit** (`fallo=1`, `exit 1`) y nombra el código de tarea
   y el número de campos obtenido.
6. Bloquea por defecto (regla 26 de CLAUDE.md): si `git show` no puede leer el WBS en stage, o si
   la propia ejecución de `awk` falla por cualquier motivo, también bloquea con mensaje explícito
   en vez de dejar pasar.

Diff real aplicado (`git diff --stat .githooks/pre-commit`): `1 file changed, 39 insertions(+)`,
sin ninguna línea borrada de los bloques anteriores.

## Método de verificación

Regla 25 de CLAUDE.md exige verificar por ejecución antes de documentar el guardia como activo.
Para no comprometer la prohibición de hacer commit, cada caso se probó así: se modificó
`00-direccion/WBS.md` en el árbol de trabajo, se hizo `git add 00-direccion/WBS.md` (deja el
contenido **en stage**, que es exactamente lo que lee el guardia vía `git show ':ruta'`), y se
ejecutó el hook directamente con `bash .githooks/pre-commit` — el mismo script que Git invocaría
en un `git commit` real, operando sobre el mismo índice. Después de cada caso se deshizo la
inyección: `git reset -- 00-direccion/WBS.md` (quita del stage) y se restauró el contenido
original desde una copia de respaldo tomada antes de empezar
(`git hash-object` del original: `6b9db4f68267abe7ea4f04ff45bad1f457a4618b`).

Estado del WBS verificado ANTES de la primera inyección (línea base, orden del orquestador):
`grep -cE '^\| *[0-9]{2}\.[0-9]{2}\.[0-9]{2} *\|' 00-direccion/WBS.md` → **66** filas de tarea,
todas con `NF == 7` (comprobado con `awk` fila a fila, ver más abajo).

---

## Caso 1 — WBS intacto → el commit PASA

Para que el bloque se ejecute de verdad (y no se salte por no haber diferencia con HEAD), se
añadió una línea de prosa inocua al final del fichero (no toca ninguna fila de tabla) y se puso
en stage.

**Comando:**
```
printf '\n<!-- prueba temporal caso 1: verificacion 03.01.25, se revierte -->\n' >> 00-direccion/WBS.md
git add 00-direccion/WBS.md
bash .githooks/pre-commit
echo "EXIT_CODE=$?"
```

**Salida literal:**
```
=== ejecutando: bash .githooks/pre-commit ===
EXIT_CODE=0
```
(Sin salida de `BLOQUEADO`: el hook no imprime nada porque todas las filas de tarea siguen dando
7 campos. `EXIT_CODE=0` → el commit habría pasado.)

**Resultado: PASA. Correcto.**

Revertido con:
```
git reset -- 00-direccion/WBS.md
cp <respaldo> 00-direccion/WBS.md
git hash-object 00-direccion/WBS.md
```
→ `6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (coincide con el original).

---

## Caso 2 — Fila de tarea partida en dos → el commit FALLA y nombra el código

Se partió la fila `03.01.25` en dos líneas con un script Python que localiza la fila por su
código (`line.startswith("| 03.01.25")`) y corta el texto por la mitad, en un espacio, sin tocar
ninguna otra fila.

**Comprobación previa de campos tras la inyección:**
```
awk -F'|' '/^\| *03\.01\.25/{print NF}' 00-direccion/WBS.md
```
Salida: `3` (la primera de las dos líneas resultantes da 3 campos en vez de 7).

**Comando:**
```
git add 00-direccion/WBS.md
bash .githooks/pre-commit
echo "EXIT_CODE=$?"
```

**Salida literal:**
```
=== ejecutando: bash .githooks/pre-commit ===
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 03.01.25: 3 campos (deberian ser 7)
EXIT_CODE=1
```

**Resultado: FALLA y nombra el código `03.01.25`. Correcto.**

Revertido con `git reset -- 00-direccion/WBS.md` + restauración del respaldo. Hash tras revertir:
`6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (coincide con el original).

---

## Caso 3 — Dos filas de tarea fusionadas en una → el commit FALLA

Se fusionaron las filas `04.01.01` y `04.01.02` en una sola línea (se eliminó el salto de línea
entre ambas, uniéndolas con un espacio), reproduciendo exactamente el incidente que originó L-027
(el 03/08/2026, `01.02.01` y `01.02.03` quedaron fusionadas en una línea de 13 campos al borrar
`01.02.02`).

**Comprobación previa de campos tras la inyección:**
```
awk -F'|' '/^\| *04\.01\.01/{print NF}' 00-direccion/WBS.md
```
Salida: `13` (misma cifra que el incidente original de L-027: 5 columnas × 2 filas + 3 barras que
se pierden en la unión = 13).

**Comando:**
```
git add 00-direccion/WBS.md
bash .githooks/pre-commit
echo "EXIT_CODE=$?"
```

**Salida literal:**
```
=== ejecutando: bash .githooks/pre-commit ===
BLOQUEADO (metrica L-027): filas de tarea del WBS que no dan 7 campos al partir por '|':
   tarea 04.01.01: 13 campos (deberian ser 7)
EXIT_CODE=1
```

**Resultado: FALLA y nombra el código `04.01.01`. Correcto.**

Revertido con `git reset -- 00-direccion/WBS.md` + restauración del respaldo. Hash tras revertir:
`6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (coincide con el original).

---

## Caso 4 — Línea de prosa con una barra vertical fuera de tabla → el commit PASA (trampa declarada)

Se insertó una línea nueva de prosa (blockquote `>`), fuera de cualquier tabla, con tres barras
verticales dentro de una cita de código en línea, imitando exactamente el patrón que ya existe en
el propio WBS al citar la métrica de L-027 (`pendiente | en_curso | hecha | bloqueada`):

```
> Prueba temporal caso 4 (verificacion 03.01.25): la sintaxis `estado_a | estado_b | estado_c`
> tambien se cita en prosa, fuera de cualquier tabla, y no debe contarse como fila de tarea.
```

Esta línea NO empieza por `| CC.CC.CC |`, así que el guardia no debe tocarla.

**Comando:**
```
git add 00-direccion/WBS.md
bash .githooks/pre-commit
echo "EXIT_CODE=$?"
```

**Salida literal:**
```
=== ejecutando: bash .githooks/pre-commit ===
EXIT_CODE=0
```
(Sin `BLOQUEADO`: el guardia no confundió la barra vertical en prosa con una fila de tabla.)

**Resultado: PASA. Correcto — no hay falso positivo.**

Revertido con `git reset -- 00-direccion/WBS.md` + restauración del respaldo. Hash tras revertir:
`6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (coincide con el original).

---

## Comprobación final: el WBS queda sin residuo

```
git hash-object 00-direccion/WBS.md
```
Salida: `6b9db4f68267abe7ea4f04ff45bad1f457a4618b` (idéntico al hash tomado ANTES de la primera
inyección).

```
git status --short
```
Salida literal (en el momento de cerrar esta verificación; las líneas de `DECISIONES.md` y los
ficheros sin seguimiento pertenecen a otra tarea en curso en paralelo — `03.01.24` — y no a esta
tarea, no se tocaron):
```
 M .githooks/pre-commit
 M 00-direccion/DECISIONES.md
?? 03-motor/scripts/tamano_minimo_operable.py
?? 04-resultados/tamano_minimo_operable.json
?? 04-resultados/tamano_minimo_operable.md
?? 04-resultados/veredictos/revision_03.01.24_registro.md
?? 04-resultados/veredictos/revision_04.01.04.md
```
Nótese que **no aparece `00-direccion/WBS.md`** en la lista: el fichero está idéntico a HEAD.

```
git diff -- 00-direccion/WBS.md
```
Salida: **vacía** (sin diferencias frente a HEAD).

```
git diff --cached --stat
```
Salida: **vacía** (nada en stage — no se dejó ningún `git add` pendiente de las inyecciones).

## Resumen de los cuatro casos

| Caso | Escenario | Esperado | Obtenido | Código nombrado |
|---|---|---|---|---|
| 1 | WBS intacto (+ línea de prosa inocua) | PASA | `EXIT_CODE=0` | — |
| 2 | Fila `03.01.25` partida en dos | FALLA | `EXIT_CODE=1` | `03.01.25` (3 campos) |
| 3 | Filas `04.01.01` + `04.01.02` fusionadas | FALLA | `EXIT_CODE=1` | `04.01.01` (13 campos) |
| 4 | Prosa fuera de tabla con `|` | PASA (sin falso positivo) | `EXIT_CODE=0` | — |

**Los cuatro casos dan el resultado exigido por la orden. El WBS queda sin ninguna modificación
de esta tarea, demostrado por `git diff` vacío y por el `git hash-object` idéntico al tomado antes
de la primera inyección.**

## Qué NO se tocó (cumplimiento de las prohibiciones de la orden)

- `00-direccion/DECISIONES.md`: sin cambios de esta tarea (su modificación en `git status`
  pertenece a la tarea `03.01.24`, en curso en paralelo).
- `.claude/settings.json`: sin cambios (no aparece en `git status`).
- No se ejecutó `git commit` en ningún momento; toda inyección se probó con `git add` +
  `bash .githooks/pre-commit` directo y se deshizo con `git reset` + restauración del respaldo.
- Los bloques existentes del hook (reglas 27, 22, 21, 13 de CLAUDE.md) no se modificaron: el
  único cambio es el bloque nuevo, íntegro, insertado antes del `exit $fallo` final.
