# Auditoría 07.01.03, lote (d) — Procedencia del motor de backtest retirado

> **Cadena de custodia declarada.** Dictado por `critico-codigo` en su mensaje de entrega. Transportado por Claude Code sin alterar. Pegado por `secretario`, que no juzga. Cadena declarada porque el auditor no tiene herramienta de escritura.

Modelo: `claude-sonnet-5`. Sin rechazo, sin necesidad de respaldo (`claude-opus-5`).

Cumplida la congelación: ningún `git commit/checkout/stash/restore`, ninguna instalación, ningún script del repositorio ejecutado. Todo lo leído del commit `0c35959` salió por `git show 0c35959:<ruta>` (objeto git, no árbol de trabajo). Antes de tocar nada que escriba, copia defensiva fuera del repo.

## CRITERIO PRE-REGISTRADO (fijado antes de mirar un solo fichero — no se movió después)

- **COPIA** si en cualquiera de los seis ficheros el **30% o más** de sus líneas no triviales (excluidas blancas, cierres de paréntesis sueltos e `import` de biblioteca estándar) aparece literalmente en su homónimo de gb2, **o** si coincide el **50% o más** de los nombres de símbolo.
- **DE CERO CON GB2 COMO REFERENCIA DECLARADA** si coinciden fichero y responsabilidades pero no cuerpos.
- **INDEPENDIENTE** si no coincide ni la estructura.

## CIFRAS MEDIDAS (los seis pares)

Definición operativa de "línea no trivial" usada (ejecutable, reproducible): blanco, o `^[)\]}]+[,:]?$`, o `import`/`from ... import` de un módulo de la lista `{dataclasses, datetime, enum, zoneinfo, typing, functools, itertools, collections, math, statistics, json, os, sys, pathlib, abc, decimal, re, copy, warnings, io, contextlib, unittest}`. Coincidencia = la línea, tras `.strip()`, existe literalmente en algún punto del fichero homónimo (no exige misma posición).

| Fichero (nuevo, `0c35959`) | líneas no triviales | coinciden literal en gb2 | % líneas | símbolos nuevo | símbolos gb2 | intersección | % sobre nuevo | % sobre gb2 |
|---|---|---|---|---|---|---|---|---|
| `costs.py` | 149 | 23 | **15.4%** | 9 | 6 | 1 (`CostModel`) | 11.1% | 16.7% |
| `execution.py` | 307 | 76 | **24.8%** | 6 | 4 | 4 (`Trade`,`BacktestResult`,`run_backtest`,`_find_exit`) | **66.7%** | **100%** |
| `sizing.py` | 90 | 10 | **11.1%** | 4 | 4 | 2 (`SizingConfig`,`implied_risk_pct`) | **50.0%** | **50.0%** |
| `test_costs.py` | 122 | 3 | 2.5% | 14 | 12 | 0 | 0% | 0% |
| `test_execution.py` | 364 | 3 | 0.8% | 22 | 43 | 0 | 0% | 0% |
| `test_sizing.py` | 114 | 6 | 5.3% | 12 | 16 | 0 | 0% | 0% |

Ninguno de los seis alcanza el 30% de líneas literales (máximo 24.8%, en `execution.py`). Los bloques contiguos ≥4 líneas idénticas (medidos con `difflib.SequenceMatcher`) son en su totalidad *shape* de interfaz: declaración de dataclass (`class Trade:`, campos), imports, y andamiaje de control (`if skipped: skipped_count += 1; trades.append(Trade(...))`) — no hay ningún bloque contiguo que reproduzca el cálculo económico (spread, swap, tamaño) palabra por palabra.

**Constantes numéricas con decimales** — cero solapamiento salvo `0.0`/`0.01` triviales. Los números de calibración de gb2 (`0.293`,`0.403`,`0.45`,`0.60`,`1.20`,`14.42`...) **no aparecen** en el `costs.py` nuevo, que cita en su lugar `01-investigacion/mercados/coste_operar.md`.

**Mensajes de error literales** — intersección vacía en los tres ficheros. El caso más próximo es un parafraseo, no una copia: gb2 `"direccion debe ser 1 (long) o -1 (short); recibido: {direccion!r}"` vs nuevo `"direction debe ser 1 (largo) o -1 (corto); recibido: {direction!r}"` — mismo patrón, variable renombrada, palabras traducidas: evidencia de *idioma compartido*, no de copia literal.

**Diff de cada par** (extracto que sostiene la cifra; reproducible con el procedimiento de la sección siguiente). Ejemplo en `costs.py`, la cabecera al completo se reescribió (docstring, `CostScenario` desaparece, `spread_total`/`commission_total` sustituyen a `commission_per_oz`/`slippage_per_oz`/`spread_assumption`/`total_rt`) — el único bloque idéntico de 4+ líneas es la declaración `@dataclass(frozen=True)` + `class CostModel:` y una función `_ensure_utc`/`_as_utc_timestamp` con 6 líneas de conversión de timezone iguales (patrón estándar de `zoneinfo`, no lógica de negocio).

### Veredicto por fichero, aplicando el criterio pre-registrado (sin moverlo)

- `costs.py` → no cumple ningún umbral (15.4% < 30%; 11–17% < 50%) → por sí solo sería *independiente/referencia*.
- **`execution.py` → cumple el sub-criterio de símbolos (66.7%/100% ≥ 50%) → dispara COPIA.**
- **`sizing.py` → cumple el sub-criterio de símbolos (50.0%/50.0% ≥ 50%, umbral inclusivo) → dispara COPIA.**
- Los tres ficheros de test → no cumplen ningún umbral (0% de símbolos: `TestLongTradeStopHit`/`make_m1`/estilo `unittest` en gb2 frente a `test_*` planos en español en el nuevo) → *independiente*.

**ETIQUETA FINAL, con el número al lado: COPIA** — la disparan `execution.py` (símbolos 66.7%/100%) y `sizing.py` (símbolos 50.0%/50.0%), **no** el umbral de líneas literales (que no lo cruza ningún fichero, máximo 24.8%).

Debo dejar la tensión explícita porque el criterio es disyuntivo y no se puede suavizar a posteriori: **textualmente no hay copia en bloque** (ningún fichero llega al 30% de líneas), pero **la interfaz (nombres de clase y función: `Trade`, `BacktestResult`, `run_backtest`, `_find_exit`, `SizingConfig`, `implied_risk_pct`) reproduce la de gb2 por encima del umbral que yo mismo fijé antes de mirar**. Es exactamente el escenario para el que se diseñó el sub-criterio del 50% de símbolos — código reescrito por dentro pero con el mismo esqueleto — y el criterio pre-registrado dice COPIA, no "referencia declarada", cuando ese umbral se cruza. No lo cambio.

## PROCEDIMIENTO REUTILIZABLE (entregable más importante — prueba de aceptación de `04.03.07`)

Antes de ejecutar esto contra gb2 para revisar el motor de `04.03.07`: **la autorización del CEO de hoy fue "abrir gb2 UNA vez, en solo lectura"** para este lote. No doy por hecho que cubre una segunda apertura futura — el propio texto de la ficha de `07.01.03` dice "la autorización de una sola apertura que dio el CEO se pierde si no se usa", lo que apunta a que es de un solo uso total. **Quien ejecute esto contra `04.03.07` debe pedir al CEO una autorización nueva antes del paso 1**, y anotarla. Esto lo dejo escrito como hueco a resolver por el orquestador, no lo decido yo.

```bash
#!/usr/bin/env bash
set -euo pipefail
# === PARÁMETROS QUE EL EJECUTOR DEBE FIJAR ANTES DE CORRER ===
NEW_DIR="03-motor/backtester"          # donde vive el motor NUEVO en el árbol de trabajo
GB2_CORE="/home/server/projects/gold-bot-2/engine/core"
GB2_TESTS="/home/server/projects/gold-bot-2/engine/tests"
OLD_COMMIT="0c35959"
OLD_PREFIX="03-motor/backtester"       # ruta del motor viejo DENTRO del commit 0c35959
WORK="$(mktemp -d)"                    # SIEMPRE fuera del repo -- aquí solo se lee

mkdir -p "$WORK"/{new,gb2,old}
for f in costs execution sizing; do
  cp "$NEW_DIR/${f}.py"                "$WORK/new/${f}.py"
  cp "$NEW_DIR/tests/test_${f}.py"     "$WORK/new/test_${f}.py"
  cp "$GB2_CORE/${f}.py"               "$WORK/gb2/${f}.py"
  cp "$GB2_TESTS/test_${f}.py"         "$WORK/gb2/test_${f}.py"
  git show "${OLD_COMMIT}:${OLD_PREFIX}/${f}.py"            > "$WORK/old/${f}.py"
  git show "${OLD_COMMIT}:${OLD_PREFIX}/tests/test_${f}.py" > "$WORK/old/test_${f}.py"
done

# 1) diff literal de cada par, en los dos sentidos:
for f in costs execution sizing test_costs test_execution test_sizing; do
  diff -u "$WORK/gb2/${f}.py" "$WORK/new/${f}.py" > "$WORK/diff_gb2_${f}.txt" || true
  diff -u "$WORK/old/${f}.py" "$WORK/new/${f}.py" > "$WORK/diff_old_${f}.txt" || true
done
```

```python
# comparar.py <carpeta_base> <subcarpeta_referencia: gb2|old>
# Aplica EXACTAMENTE el criterio pre-registrado de esta ficha, sin modificarlo.
import re, sys, os, difflib

STDLIB_MODS = {"dataclasses","datetime","enum","zoneinfo","typing","functools",
    "itertools","collections","math","statistics","json","os","sys","pathlib",
    "abc","decimal","re","copy","warnings","io","contextlib","unittest"}

def is_trivial(line):
    s = line.strip()
    if s == "": return True
    if re.fullmatch(r"[)\]}]+[,:]?", s): return True
    m = re.match(r"^(from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", s)
    if m:
        mod = (m.group(2) or m.group(3) or "").split(".")[0]
        if mod in STDLIB_MODS: return True
    return False

def nontrivial(path):
    return [l.rstrip("\n") for l in open(path) if not is_trivial(l)]

def symbols(path):
    names = set()
    for line in open(path):
        m = re.match(r'^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)', line)
        if m: names.add(m.group(1))
    return names

def veredicto(base, ref):
    etiquetas = {}
    for f in ["costs.py","execution.py","sizing.py",
              "test_costs.py","test_execution.py","test_sizing.py"]:
        new_p, ref_p = os.path.join(base,"new",f), os.path.join(base,ref,f)
        new_lines, ref_lines = nontrivial(new_p), nontrivial(ref_p)
        ref_set = set(l.strip() for l in ref_lines)
        matches = [l for l in new_lines if l.strip() in ref_set and l.strip()]
        pct_lines = 100*len(matches)/len(new_lines) if new_lines else 0
        s_new, s_ref = symbols(new_p), symbols(ref_p)
        inter = s_new & s_ref
        pct_sym_new = 100*len(inter)/len(s_new) if s_new else 0
        pct_sym_ref = 100*len(inter)/len(s_ref) if s_ref else 0
        copia = pct_lines >= 30 or pct_sym_new >= 50 or pct_sym_ref >= 50
        etiquetas[f] = (copia, pct_lines, pct_sym_new, pct_sym_ref)
        print(f"{f}: lineas={pct_lines:.1f}% simbolos(nuevo/ref)={pct_sym_new:.1f}%/{pct_sym_ref:.1f}%  -> {'COPIA' if copia else 'no-copia'}")
    global_copia = any(v[0] for v in etiquetas.values())
    print("VEREDICTO GLOBAL:", "COPIA" if global_copia else
          "revisar a mano si aplica REFERENCIA DECLARADA o INDEPENDIENTE (ningun fichero disparo COPIA)")

if __name__ == "__main__":
    veredicto(sys.argv[1], sys.argv[2])
```

```bash
# 2) ejecutar contra las DOS fuentes exigidas por el criterio de hecho de 04.03.07:
python3 comparar.py "$WORK" gb2
python3 comparar.py "$WORK" old
# El criterio de hecho de 04.03.07 exige VEREDICTO GLOBAL = "no-copia" (independiente)
# frente a AMBAS fuentes. Si cualquiera de las dos ejecuciones imprime COPIA, no pasa.
```

Este es el mismo procedimiento que apliqué arriba (produje exactamente esas cifras con este código, ejecutado en el scratchpad). Un tercer agente puede correrlo tal cual sin preguntarme nada, con tres parámetros: dónde vive el motor nuevo, y las dos rutas de referencia.

## (i) Las 12 menciones a «gb2» en el código de `0c35959`

Confirmado por ejecución: exactamente 12 apariciones de la cadena `gb2` (case-insensitive) repartidas en `costs.py` (3), `execution.py` (4), `sizing.py` (1), `test_sizing.py` (1), `verificar_motor.py` (1), `__init__.py` (2). Cero en `test_costs.py` y `test_execution.py`.

Las 12, sin excepción, son **referencia declarada**, no descripción de copia:

- 6 son atribución administrativa: "tarea 01.02.02, pieza T2 del trasplante desde gb2 (D6=B, ...)" repetida en las cabeceras de `costs.py`, `execution.py`, `sizing.py`, `verificar_motor.py`, `__init__.py` (×2).
- 1 es una **negación explícita de copia**, con la ruta absoluta citada literalmente: en `execution.py`, "Construido como informacion, no como copia en bloque de `/home/server/projects/gold-bot-2/engine/core/execution.py`".
- 2 declaran **paridad de comportamiento/arquitectura**, no de código: mismo orden de comprobación stop/target que gb2, misma separación de responsabilidades (el motor no impone una sola posición abierta, igual que gb2).
- 1 declara una **diferencia deliberada** frente a gb2 (`test_sin_max_risk_pct_nunca_salta_por_riesgo_del_minimo`: aquí `max_risk_pct` es opcional, en gb2 no).
- 1 contrasta un hecho de los datos: gb2 tenía bid/ask real de Dukascopy, este proyecto no.

Ninguna de las 12 admite copia literal. Eso es coherente con la medición de líneas (máx. 24.8%) pero **no es toda la historia**: ninguna de las 12 menciona ni reconoce el grado de paralelismo de nombres de símbolo, que es justo lo que dispara la etiqueta COPIA por el criterio pre-registrado.

## (ii) Ficheros de gb2 abiertos y orden (registro de la única apertura autorizada)

Orden real de apertura (todo en solo lectura, todo copiado a scratchpad fuera del repo, nada modificado en gb2):

1. `ls` de `/home/server/projects/gold-bot-2/engine/core/` y `/engine/tests/` (solo listado de nombres, sin contenido).
2. `/home/server/projects/gold-bot-2/engine/core/costs.py`
3. `/home/server/projects/gold-bot-2/engine/tests/test_costs.py`
4. `/home/server/projects/gold-bot-2/engine/core/execution.py`
5. `/home/server/projects/gold-bot-2/engine/tests/test_execution.py`
6. `/home/server/projects/gold-bot-2/engine/core/sizing.py`
7. `/home/server/projects/gold-bot-2/engine/tests/test_sizing.py`

No se abrió ningún otro fichero de gb2 (ni `calendar.py`, ni `test_metrics.py`, ni `test_montecarlo_simulator.py`, ni ningún otro de los que aparecían en el listado). Ni un byte se copió de gb2 al repositorio — todas las copias fueron hacia el scratchpad, nunca al revés.

## (iii) ¿De dónde sale la ruta de gb2 si el CEO no pasó ningún archivo?

**Confirmado por ejecución.** La ruta `/home/server/projects/gold-bot-2` está escrita, en texto plano, en `01-investigacion/herencia-gb2/INFORME_GB2.md`:

```
> `/home/server/projects/gold-bot-2`, rama activa `auto/20260724-1` (sin mergear).
```

Ese fichero lo creó el commit `da1e3c7` ("arranque del proyecto"), fechado 2026-07-30 — la misma fecha que cierra la tarea `01.02.01` (confirmado también por `HERENCIA_GB2.md`, cuya primera línea se autodeclara: *"Tarea 01.02.01 cerrada. Fuente: `INFORME_GB2.md`"*). Permisos del fichero: `664` (lectura para *owner*, grupo y **otros**) — legible por cualquier proceso del disco desde esa fecha, sin credencial especial y sin que el CEO tenga que pasar nada: cualquier agente con `Read`/`Grep` sobre el repositorio lo encuentra desde el 30/07. Esto explica el origen sin necesitar que el CEO haya movido un archivo.

## Hallazgo obligatorio de subir: D-21 afirma algo falso

D-21 (`00-direccion/DECISIONES.md`, localizado por `grep`, registro de solo-añadir) dice literalmente:

> "T2 (motor de backtest) ya se construyó desde cero aquí — commit `0c35959`; **no se copió una sola línea de gb2, y de hecho no se podía**: `01-investigacion/herencia-gb2/` contiene únicamente cuatro ficheros `.md` de informe y ningún código de gb2 está en este repositorio."

Dos partes distintas, con distinta suerte al medirlas:

- **Verdadera, confirmada por ejecución:** `01-investigacion/herencia-gb2/` contiene exactamente 4 `.md` (`HERENCIA_GB2.md`, `INFORME_GB2.md`, `prompt_auditoria.md`, `prompt_awesome_claude_code.md`) y `git ls-files | grep -i gb2` no devuelve ningún `.py` — ningún código fuente de gb2 está commiteado en este repositorio.
- **Falsa, confirmada por ejecución, en dos frentes:**
  1. **"no se copió una sola línea"** — medido arriba: hay 23 líneas idénticas en `costs.py`, 76 en `execution.py`, 10 en `sizing.py` (no triviales, coincidencia literal exacta). "Ni una sola línea" exigiría cero; el número real es de decenas.
  2. **"de hecho no se podía"** — el razonamiento es un salto en falso: que el código de gb2 no esté *commiteado en este repositorio* no significa que no fuera *accesible en disco*. La prueba de que sí era accesible está en el propio código nuevo: `execution.py` cita la **ruta absoluta literal** `/home/server/projects/gold-bot-2/engine/core/execution.py` en su propia cabecera para decir "no es copia de esto" — lo cual solo se puede escribir si ese fichero estaba abierto o visible al escribir el nuevo. D-21 confunde "no está en este repo" con "no se podía copiar", y esa segunda afirmación es la que no se sostiene.

Como `DECISIONES.md` **solo admite añadir** (regla 21 de CLAUDE.md), no lo toco ni lo puedo tocar. Queda para que el orquestador decida si procede una entrada nueva de corrección.

**Lo que no hago:** no opino sobre el destino del motor — ya está decidido (D-22, `git revert` en `eb7ac2f`, reconstrucción vía `04.03.06`/`04.03.07`). Esta entrega es solo medición y procedimiento.
