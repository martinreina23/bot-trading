# Auditoria tecnica de gb2

# INFORME_GB2 — Auditoría técnica del proyecto «gb2» (gold-bot-2 / gold-quant)

> Auditoría independiente en **modo solo lectura**, realizada el **2026-07-30** sobre
> `/home/server/projects/gold-bot-2`, rama activa `auto/20260724-1` (sin mergear).
> Objetivo: extraer información y lecciones para un proyecto nuevo. No se ha modificado,
> borrado ni movido nada del proyecto; el único fichero escrito es este informe.
>
> **Convención:** a lo largo del texto, **OBSERVA** marca un hecho comprobable (con su ruta) e
> **INTERPRETA** marca una hipótesis del auditor sobre por qué pasó. Cuando un dato no consta en
> los ficheros, se escribe «no consta» en vez de deducirlo.
>
> **Método:** recorrido inicial de la estructura real + seis barridos de evidencia en paralelo
> (mapa, agentes, rastro de activación, tareas, modo autónomo, restricciones), cruzados con
> lectura directa de `LECCIONES.md`, `docs/lecciones.md`, `docs/decisiones.md`, `ESTADO.md` y los
> CSV de `results/` y `metricas/`.
>
> **Glosario mínimo** (se explica un término técnico la primera vez que aparece):
> *hook* = script que el sistema dispara automáticamente antes o después de una acción (por
> ejemplo, antes de un commit) para permitirla o bloquearla · *guard* = hook cuyo propósito es
> vetar algo · *append-only* = fichero al que solo se puede añadir al final, nunca reescribir lo
> ya escrito · *OOS* (out-of-sample) = datos reservados para validar al final, prohibidos durante
> el diseño · *PF* (profit factor) = ganancias brutas ÷ pérdidas brutas de un backtest ·
> *deny-by-default* = «bloquea todo salvo lo explícitamente permitido».

---

## 1. MAPA DEL PROYECTO

### 1.1 Escala real

**OBSERVA.** El repositorio tiene **50 251 ficheros versionados**, de los cuales **50 089 (99,7 %)
son datos de mercado** bajo `data/raw/` (ficheros `.bi5` de Dukascopy, ~1,4 GB) más 6 `.parquet`
en `data/processed/` (~178 MB). El proyecto «real» (código + documentación + configuración) cabe
en **~160 ficheros**.

**INTERPRETA.** En número de ficheros, el repo es casi enteramente datos. Cualquier clon arrastra
1,4 GB de ticks históricos.

### 1.2 Estructura de carpetas

| Carpeta | Ficheros útiles | Propósito |
|---|---|---|
| `.claude/` | ~40 | Configuración del motor autónomo: `settings.json`, `tarea-actual.json` y subcarpetas `agents/` (13), `commands/` (9), `hooks/` (9), `scripts/` (5), `skills/` (solo `deep/`), `logs/` |
| `.githooks/` | 6 | Hooks de git reales: `pre-commit`, `commit-msg`, `pre-push`, `post-checkout`, `post-commit`, `post-merge` |
| `.github/` | 1 | 1 workflow de integración continua (`workflows/tests.yml`) |
| `data/` | 50 095 | `raw/` (bi5 2015-2022) + `processed/` (parquet). El 99,7 % del repo |
| `docs/` | ~29 | `decisiones.md`, `plan_maestro.md`, `acta_criba.md`, `ARQUITECTURA.md`, `protocolo_backtest.md`, `lecciones.md` + `informes/` (18) + `investigacion_previa/` (4) + `plantillas/` |
| `engine/` | ~28 | Motor de backtest propio: `core/` (calendar, costs, execution, sizing), `metrics/`, `montecarlo/`, `walkforward/`, `run.py`, `tests/` (16) |
| `strategies/` | ~10 | `DUMMY/`, `F03_canal_vol/`, `F13_overnight/`, `_template/` |
| `results/` | ~15 | `registry.csv` + `reports/` (13 informes: 9 DUMMY + 4 F03) |
| `scripts/` | 9 | Drivers de backtest de F03, descarga Dukascopy, `conductor.sh` |
| `metricas/` | 3 | Telemetría del motor: `tareas.csv`, `tiradas.csv`, `rechazos.csv` |
| `logs/` | 1 | `download_20260614.log` (ignorado) |

Ficheros de raíz: `CLAUDE.md` (13,8 KB, reglas + protocolo), `ESTADO.md` (**117 KB**),
`TAREAS.md` (**218 KB**), `LECCIONES.md` (33,8 KB), `ROADMAP.md` (33,3 KB), `README.md`,
`REFERENCIA.md`, `SEGURIDAD.md` (16,9 KB), `METRICAS.md`, `RUN-STATUS.json` (sentinel efímero),
`bucle.sh`, `pyproject.toml`, `requirements.lock`.

### 1.3 Duplicados, versiones múltiples y ficheros que confunden

| Caso | Evidencia (rutas) | Diagnóstico |
|---|---|---|
| **Datos versionados contra su propio `.gitignore`** | `.gitignore` ignora `data/raw/` y `data/processed/` con el comentario *«large, re-downloadable»* / *«not in VCS»*, pero `git ls-files data/raw` devuelve **50 089 ficheros tracked** | **OBSERVA.** Contradicción declarada. **INTERPRETA.** Se añadieron antes de escribir la regla; `.gitignore` no des-trackea lo ya indexado. Es el fallo de higiene más costoso del repo. Nota positiva: solo 2015-2022, la cuarentena OOS (Regla 1) se respeta en el árbol |
| **Dos encadenadores de sesión vivos** | `bucle.sh` (raíz, `claude -p`, marcado «EXPERIMENTAL») y `scripts/conductor.sh` (tmux, «FRENOS portados de bucle.sh») | **INTERPRETA.** `bucle.sh` es el antiguo no retirado; `conductor.sh` es el sucesor. Un operador nuevo no sabe cuál lanzar |
| **Dos «mapas» del repo del mismo día** | `docs/informes/mapa_20260718.md` (41 KB) y `docs/informes/mapa_repo_20260718.md` (48 KB) | **INTERPRETA.** Dos versiones del mismo mapa del mismo día, sin marca de cuál es el bueno |
| **Drivers de backtest duplicados** | `engine/run.py` (runner genérico) vs `scripts/backtest_f03a.py` / `backtest_f03b.py` / `walkforward_f03b.py`; cabecera: *«Driver nuevo (Regla: engine/run.py NO se toca)»* | **OBSERVA.** Duplicación deliberada por la congelación del motor. **INTERPRETA.** La lógica de fills bid-ask y de registro vive en dos sitios; riesgo de divergencia numérica (existe `.claude/scripts/test-parity.sh`, probablemente para mitigarlo) |
| **Dos ficheros de lecciones** | `LECCIONES.md` (vivo) y `docs/lecciones.md` (marcado «PRE-MOTOR CONGELADO — solo lectura») | **OBSERVA.** Ya resuelto con cabeceras. Sombra: la descripción del skill `/leccion` cita como destino `docs/lecciones.md`, que es el congelado |
| **Triple resumen de reglas** | Las Reglas Innegociables se re-resumen en `CLAUDE.md`, `README.md` y `REFERENCIA.md` | **INTERPRETA.** No es duplicado estricto (visión vs chuleta), pero tres copias del mismo resumen derivan con el tiempo |
| **18 informes sin índice de vigencia** | `docs/informes/` con `README.md` de solo 407 bytes | **INTERPRETA.** El README no indexa 18 informes; hallar el vigente exige abrirlos |

### 1.4 Ficheros anómalos por tamaño

`data/raw/` (1,4 GB), `TAREAS.md` (218 KB), `docs/decisiones.md` (154 KB), `ESTADO.md` (117 KB),
`data/processed/XAUUSD_M1_UTC.parquet` (137 MB). **INTERPRETA.** `TAREAS.md` y `ESTADO.md` se leen
al inicio de **cada** sesión (protocolo de `CLAUDE.md`); su tamaño encarece cada arranque y revela
falta de rotación/archivado.

**OBSERVA.** Los artefactos de build/entorno (`gold_quant.egg-info/`, `.venv/`, `.pytest_cache/`,
`__pycache__/`, `logs/`, `.claude/logs/bash-audit.log`, `RUN-STATUS.json`, `.env` vacío) están
correctamente ignorados y no versionados. No hay ficheros sueltos `.bak/.tmp/.orig`. El fallo de
higiene es exclusivo de `data/`.

---

## 2. INVENTARIO DE AGENTES

**OBSERVA.** Hay **13 agentes**, uno por fichero en `.claude/agents/`. Ninguno queda huérfano: los
13 están referenciados por al menos un comando de `.claude/commands/`.

| # | Agente | Fichero | Descripción literal (frontmatter, resumida) | Modelo | Herramientas | Invocación |
|---|---|---|---|---|---|---|
| 1 | **abogado-diablo** | `.claude/agents/abogado-diablo.md` | «Crítica adversarial de specs, informes y decisiones… Usar SOLO bajo demanda explícita (/hater), nunca dentro del loop autónomo.» | `claude-opus-4-8` (effort xhigh) | Read, Grep, Glob | **EXPLÍCITA** (`/hater`) |
| 2 | **auditor-codigo** | `auditor-codigo.md` | «Audita código recién implementado contra su spec buscando lookahead, bid/ask, timezone, swap… Usar en /fin y tras cada tarea tipo implementacion.» | `claude-sonnet-4-6` (effort high) | Read, Grep, Glob, Bash | **AUTO** |
| 3 | **auditor** | `auditor.md` | «Usa este agente SOLO vía /fin o el paso de auditoría de /autonomo… Es adversarial por diseño: su trabajo es encontrar motivos para rechazar.» | `opus` (alias) | Read, Grep, Glob, Bash | **AUTO** |
| 4 | **backtest-runner** | `backtest-runner.md` | «Ejecuta backtests de variantes ya congeladas en el spec, vuelca métricas a registry.csv…» | `claude-haiku-4-5-20251001` | Read, Bash, Write, Grep, Glob | **AUTO** (por Tipo) |
| 5 | **datos** | `datos.md` | «Pipeline de datos históricos — descargas in-sample, resampleo, controles de integridad…» | `claude-sonnet-4-6` (effort medium) | Read, Edit, Write, Bash, Grep, Glob | **AUTO** (por Tipo) |
| 6 | **explorador** | `explorador.md` | «…cualquier lectura o búsqueda de más de 3 ficheros… Úsalo proactivamente antes de implementar. Solo lee.» | `haiku` (alias) | Read, Grep, Glob | **AUTO** |
| 7 | **firmante** | `firmante.md` | «Redacta y firma entradas de docs/decisiones.md… el ÚNICO agente que escribe decisiones de tipo COMPUERTA… nunca lo llama el mismo hilo que produjo las métricas.» | **sin campo `model` → hereda** | Read, Grep, Glob, Edit, Write | **AUTO + EXPLÍCITA** |
| 8 | **implementador** | `implementador.md` | «Implementar UNA tarea ya definida y desbloqueada, o corregir los fallos de un rechazo… No planifica, no explora en profundidad.» | `sonnet` (alias) | Read, Grep, Glob, Edit, Write, Bash | **AUTO** (default) |
| 9 | **mql5-ea** | `mql5-ea.md` | «Expert Advisors MQL5 en MetaTrader 5 — loggers de spread/slippage, exportes CSV…» | `claude-sonnet-4-6` (effort high) | Read, Edit, Write, Grep, Glob | **AUTO** (por Tipo) |
| 10 | **organizador** | `organizador.md` | «SOLO cuando EN CURSO esté vacío y no haya /autonomo activo. Reorganiza estructura — mueve ficheros, elimina código muerto — sin cambiar comportamiento.» | `sonnet` (alias) | Read, Grep, Glob, Edit, Write, Bash | **CONDICIONAL** (solo `/fin`) |
| 11 | **planificador** | `planificador.md` | «SOLO desde /autonomo, cuando PENDIENTES quede vacía y ROADMAP.md tenga hitos sin completar, para granular el SIGUIENTE hito. Propone, nunca escribe. Solo lee.» | `opus` (alias) | Read, Grep, Glob | **AUTO + EXPLÍCITA** |
| 12 | **seguridad** | `seguridad.md` | «Revisa la SEGURIDAD de un diff antes de cerrarlo — obligatorio en riesgo alto… y en /fin sobre el diff agregado. Solo lee y ejecuta análisis.» | `opus` (alias) | Read, Grep, Glob, Bash | **AUTO** |
| 13 | **tester** | `tester.md` | «Escribe o ejecuta tests de una tarea recién implementada, o reproduce un bug. Independiente del implementador para que no valide su propio trabajo.» | `sonnet` (alias) | Read, Grep, Glob, Edit, Write, Bash | **AUTO** |

### 2.1 Reparto de modelos y razón documentada

| Familia | Agentes |
|---|---|
| **opus** (4) | abogado-diablo, planificador, auditor, seguridad |
| **sonnet** (6) | auditor-codigo, datos, mql5-ea, implementador, organizador, tester |
| **haiku** (2) | backtest-runner, explorador |
| **hereda / no consta** (1) | firmante |

**OBSERVA — la razón está en `docs/ARQUITECTURA.md`, no en los propios ficheros** (salvo
abogado-diablo). `ARQUITECTURA.md:310-312`: *«haiku = mecánico con plantilla estricta; sonnet =
implementación y auditoría; opus = solo crítica de diseño para consumo humano (abogado-diablo,
bajo demanda)»*. La «Política de pineado (v1.3)» (`ARQUITECTURA.md:314-322`) exige el **string
exacto** del modelo, no el alias, porque *«un alias resuelve a "lo que toque ese mes": drift
silencioso que contamina la telemetría»*.

**INTERPRETA — divergencias reales entre la política escrita y el roster vivo:**

1. **`opus` fuera de su nicho declarado.** La política dice «opus = SOLO abogado-diablo», pero
   **auditor, seguridad y planificador también corren opus** en su frontmatter; el mapa de pineado
   los asigna a `claude-sonnet-4-6`. El roster contradice la política para 3 agentes.
2. **Alias donde se exige string exacto.** **7 de 13** agentes usan alias (`opus`/`sonnet`/`haiku`),
   justo el «drift silencioso» que la política dice evitar. Ya señalado en
   `docs/informes/mapa_repo_20260718.md:504`.
3. **`firmante` sin modelo pineado.** El único agente que firma decisiones de COMPUERTA hereda el
   modelo del hilo que lo invoca: con qué modelo razona no es determinista ni auditable desde su ficha.
4. **`housekeeping` es un fantasma documental.** `ARQUITECTURA.md:111,310,319` nombra un agente
   `housekeeping` (haiku), pero **no existe fichero** en `.claude/agents/`.
5. **Discrepancia `firmante` description↔comandos.** Su descripción dice «se invoca desde /verdicto
   y desde /fin», pero no aparece por nombre en `fin.md` (sí en `verdicto.md`). Coherencia menor.

---

## 3. AGENTES QUE NUNCA SE ACTIVARON

Fuentes cruzadas para el rastro de ejecución: `metricas/{tareas,tiradas,rechazos}.csv`,
`.claude/logs/bash-audit.log` (~4 700 líneas), `git log --all` (328 commits), `docs/decisiones.md`,
`ESTADO.md`, `TAREAS.md`, `LECCIONES.md`. Nota de método: los agentes que **escriben** dejan rastro
fuerte (commits, filas CSV, entradas firmadas); los **solo-lectura** (explorador, auditor,
seguridad, abogado-diablo) no commitean, así que su rastro es indirecto (columnas de veredicto en
CSV, menciones en meta-commits).

| Agente | ¿Rastro de trabajo? | Evidencia | Causa / matiz |
|---|---|---|---|
| **auditor** | **SÍ (fuerte)** | `metricas/tareas.csv` col `veredicto` en ~40 filas; `rechazos.csv` gate=auditor ×8; commits `revert T-022 — RECHAZO ESTRUCTURAL del auditor` | El agente más activo del repo |
| **auditor-codigo** | **SÍ (fuerte)** | `rechazos.csv` gate=auditor-codigo ×2; `T-074 (auditor-codigo APTO)` | Activo |
| **tester** | **SÍ (fuerte)** | `tareas.csv` col `rondas_tester`; `rechazos.csv` gate=tester ×4 | Activo |
| **seguridad** | **SÍ (fuerte)** | `tareas.csv` col `seguridad`=SEGURO/VULNERABLE; `T-032-fix: REVERT — 2 rondas de seguridad VULNERABLE` | Activo en todo circuito ALTO |
| **implementador** | **SÍ (fuerte)** | Ejecutor por defecto; incontables commits `T-XXX-fix:` | Ejecutor por defecto |
| **firmante** | **SÍ (fuerte)** | Creado 2026-07-20 (D-9); firma entradas en `decisiones.md` | Activo desde su creación |
| **planificador** | **SÍ (fuerte)** | `meta: granula cola…`; `TAREAS.md:801` «Granulado por el planificador» | Activo |
| **abogado-diablo** | **SÍ (fuerte)** | `ESTADO.md`: «abogado-diablo SÍ se ha corrido en el loop… es LETRA MUERTA su "nunca dentro del loop"» | **Se corre pese a que su ficha dice «solo /hater»**. Contradicción documentada (`TAREAS.md:682`) |
| **explorador** | **SÍ (probable, indirecto)** | Mandado por `CLAUDE.md`; listado en el circuito ALTO | Solo-lectura: no deja rastro duro. Muy probablemente invocado |
| **organizador** | **AMBIGUO** | 35 commits `org:`, pero `org:` es una **categoría** que también usa el orquestador | No prueba que el subagente corriera; rastro no concluyente |
| **backtest-runner** | **NO** | El propio repo lo declara: `ESTADO.md:79` y `TAREAS.md:1447` «3 agentes que el loop jamás invoca» | Ver abajo |
| **datos** | **NO** | Igual declaración; `logs/download_20260614.log`: el dataset se construyó el 2026-06-14 | Ver abajo |
| **mql5-ea** | **NO** | Igual; `find` no encuentra ningún `.mq5`/`.mqh` | Ver abajo |

### 3.1 Causa concreta de los tres inactivos

**OBSERVA.** Los tres se crearon el 2026-07-05, el día 1 del motor: su inactividad **no** se debe a
creación tardía. La causa raíz común, con evidencia por agente:

- **backtest-runner** — Hasta T-027 (2026-07-19) `/autonomo` enrutaba **solo por Riesgo** y
  siempre al `implementador`, ignorando el `Tipo` de tarea. T-027 cableó el enrutado por Tipo, pero
  **ninguna tarea posterior de tipo `backtest` se despachó**: los backtests de F03-A/B, DUMMY y
  walk-forward los corrió el `implementador` en línea. Causa: **solapamiento con el implementador**.
- **datos** — El pipeline de datos (dataset XAUUSD 2015-2022) se completó el **2026-06-14, antes de
  que existiera este juego de agentes**. No surgió ninguna tarea `datos` posterior. Causa:
  **trabajo ya consumado antes del motor**.
- **mql5-ea** — El proyecto está en fase de backtesting (FASE 3-6); la operativa en vivo con
  MetaTrader 5 no se ha alcanzado y no hay ningún fichero `.mq5` en el repo. Causa: **dominio de
  trabajo aún no alcanzado**.

**INTERPRETA.** Ninguno de los tres fracasó por descripción vaga, ruta mal escrita ni permisos: los
tres tienen fichas claras y permisos suficientes. Fracasaron porque **la cola nunca contuvo una
tarea de su tipo**, agravado por un defecto de enrutado que durante dos semanas mandó todo al
implementador. Es un fallo de *diseño de la cola*, no de los agentes.

---

## 4. CÓMO SE NOMBRABAN Y SEGUÍAN LAS TAREAS

### 4.1 Identificadores

**OBSERVA.** Tres espacios de nombres, cada uno en su fichero:

| Tipo | Formato | Rango | Consistencia |
|---|---|---|---|
| Tareas | `T-NNN` (3 dígitos) | `T-001`…`T-084` | Contiguo, **84 IDs sin huecos**, forzado por el hook `commit-msg` |
| Decisiones | `D-N` (sin ceros) | `D-1`…`D-16` | Consistente pero sin relleno |
| Lecciones | sin ID | — | Se titulan por fecha: `## AAAA-MM-DD · [síntoma]` |

### 4.2 Lista maestra

**OBSERVA.** `TAREAS.md` (218 KB, 2 550 líneas) es la **única cola** (`CLAUDE.md`: «Trabajo que no
está ahí no se ejecuta»). Secciones: `EN CURSO` (L27), `PENDIENTES` (L473), `HALLAZGOS` (L1499),
`DEUDA DE MOTOR` (L1580), `BLOQUEADAS` (L1809), `EN AUDITORÍA` (vacía, L2014), `HECHAS` (L2017).
Conteo de casillas: 64 `[x]`, 37 `[ ]`, 13 en transición. Total: **84 tareas**. Las colas antiguas
(`tareas.yaml`/`backlog.yaml`/`done.yaml`) están retiradas (0 ficheros); solo quedan menciones en
prosa.

### 4.3 Criterio de «terminada» (Definition of Done) — SÍ existe

**OBSERVA.** Es el **doble gate** de `/fin` (`CLAUDE.md` §CIERRE DE TAREA): (1) puertas de commit en
verde (`pre-commit`: gitleaks + suite completa + validación de alcance por `commit-msg`) **Y** (2)
veredicto **APTO** del `auditor` en tareas de implementación. «Nadie se auto-aprueba.» El resultado
se registra en cuatro sitios: `results/registry.csv` (backtests), `metricas/tareas.csv`,
`metricas/tiradas.csv`, `metricas/rechazos.csv`.

**INTERPRETA.** El DoD es explícito, escrito y con muro mecánico parcial; es de lo más sólido del
sistema. Debilidad: el estado «cerrado» vive en **prosa** dentro de `TAREAS.md`, no en un campo, y
depende de que el orquestador mueva la tarea de sección a mano.

### 4.4 Registro de resultados

**OBSERVA.** `results/registry.csv` es append-only (23 columnas, 42 filas de datos). Sistemas
registrados: `DUMMY` (19 filas), `F03_canal_vol` (21), `MC_CALIBRATION…NOT_A_STRATEGY` (2). Es
decir, **una sola estrategia real (F03) ha llegado a backtest**; el resto es el testbed DUMMY y
calibraciones. `metricas/tareas.csv` tiene 50 filas < 84 tareas: no toda tarea entra en métricas.

### 4.5 Qué rompe la trazabilidad

**OBSERVA — el día de la auditoría, los registros de estado no cuadran entre sí:**

| Fuente | Última señal | Fecha |
|---|---|---|
| git HEAD | `T-082: dossier…` | 2026-07-29 |
| `ESTADO.md` | `T-076 HECHA` (menciona T-082) | 2026-07-29 |
| `RUN-STATUS.json` | `{"fase":"fin","resultado":"bloqueado-seguridad",…}` | **2026-07-27 (2 días stale)** |
| `metricas/tareas.csv` | última fila `T-061` | **2026-07-27 (no registra T-076/T-082)** |
| `TAREAS.md` §EN CURSO | `T-077 BLOQUEADA` | **sigue colgada** |

Fricciones concretas: (1) `T-077` está **duplicada** en `EN CURSO` (L36) y en `BLOQUEADAS` (L1811),
y su estado real solo se entiende leyendo ~15 líneas de prosa en cada sitio; (2) `RUN-STATUS.json`
miente sobre la fase actual; (3) `metricas/tareas.csv` pierde los dos últimos días; (4) 216 KB
mezclan cola viva, archivo histórico y secciones semi-congeladas sin separación física; (5) el
estado de una tarea es prosa, no un dato parseable (solo 9 apariciones de `estado:` en 2 550 líneas).

**INTERPRETA — qué hace imposible saber, mirando el sistema, qué se hacía en cada momento.**
Hay **múltiples registros de verdad que se actualizan a ritmos distintos**: git y `ESTADO.md` van al
día; `TAREAS.md/EN CURSO`, `RUN-STATUS.json` y los CSV se quedan atrás. Quien confíe en el sentinel
o en las métricas ve un proyecto parado el 27-jul que en realidad siguió hasta el 29. Con **solo git
+ ESTADO.md** sí se reconstruye la narrativa; con `TAREAS.md` la señal se ahoga; y falta un paso que
**vacíe/archive `EN CURSO`** al parar una tirada, por lo que quedan tareas zombis que hay que interpretar.

---

## 5. EL MODO AUTÓNOMO

### 5.1 Las piezas y el punto de entrada

**OBSERVA.** El punto de entrada real es el comando **`/autonomo`** (`.claude/commands/autonomo.md`):
no es un script, es un prompt que Claude ejecuta como *orquestador*. La autonomía de horas se logra
**encadenando sesiones desechables** (cada tirada = contexto fresco), no alargando una sesión. El
estado vive en disco (`ESTADO.md`, `TAREAS.md`, CSV), no en la sesión. Dos encadenadores lo llaman:
`scripts/conductor.sh` (tmux, desatendido, de producción) y `bucle.sh` (manual, «EXPERIMENTAL»). El
sentinel `RUN-STATUS.json` señala el fin de cada fase.

### 5.2 Instrucciones exactas (citas literales de `autonomo.md`)

- **Rol** (L5-7): *«Eres el orquestador… No implementas. Las decisiones estratégicas (datos, dinero,
  arquitectura, irreversibles) son del usuario, no tuyas.»*
- **Selección de tarea** (L42-47): *«Selecciona la siguiente tarea desbloqueada… SIEMPRE
  secuencial: un solo implementador a la vez.»* **No hay ninguna heurística de «prioriza estrategia
  sobre motor» dentro del ciclo**: coge la siguiente de `PENDIENTES` en orden. La orientación hacia
  estrategia vive fuera del comando (en `CLAUDE.md` y en cómo se llena la cola).
- **Circuitos por riesgo:** BAJO = implementador → puertas de commit, sin auditoría por tarea («el
  coste de auditar un typo con Opus supera el riesgo del typo»); MEDIO = + tester + auditor-codigo +
  auditor; ALTO = + pase de `seguridad` + aprobación humana del merge.
- **Checkpoint** cada 5 tareas; **reabastecimiento** una vez por tirada desde `ROADMAP.md`;
  **paradas**: cola agotada, 3 bloqueos consecutivos, crítico de seguridad, decisión de usuario, o
  contexto cargado.

### 5.3 En qué gastó el tiempo realmente: motor vs plan de trabajo

**DATO (cifras de git verificables):**

| Métrica | Valor |
|---|---|
| Commits totales (`--all`) | **328** en ~7 semanas (2026-06-12 → 2026-07-29) |
| `meta:` (contabilidad de estado del motor) | **120 (37 %)** |
| `meta:`+`org:`+`merge:`+`leccion:` (gestión/motor/git) | **191 (58 %)** |
| Tareas `T-XXX` (incl. `-fix`) | 105 commits / **51 IDs únicos** |

**DATO — ficheros más tocados:** de los 20 con más commits, **solo 2 son de estrategia**
(`results/registry.csv` en el puesto #5 y `scripts/walkforward_f03b.py` en el #16). Los tres CSV de
`metricas/` suman 76 toques de puro overhead de contabilidad. Los 18 restantes del top-20 son motor
o gestión (`TAREAS.md` 103, `ESTADO.md` 70, `metricas/tareas.csv` 44, `docs/decisiones.md` 26…).

**INTERPRETA (clasificación de commits por título; el ±1-2 de frontera es estimación):** de 51
tareas únicas, **~36 (70 %) son de motor/fontanería** (`.claude/`, hooks, `engine/`, arneses,
guards, git, métricas, DUMMY) y **~15 (30 %) de estrategia**, de las cuales **solo 8 tocaron
código+backtest de una hipótesis** (T-050…053 = F03-A; T-054, 055, 056, 062 = F03-B).

**DATO — cuántas hipótesis se backtestearon de verdad:** de 13 hipótesis del embudo (F01…F13), se
backtesteó **exactamente 1 (F03)**. Solo `F03_canal_vol/spec.md` está `CONGELADO`; F03-C nunca se
escribió; F13 tiene spec-plantilla condicional; seis hipótesis (F01, F02, F04, F07, F08, F09) siguen
sin reglas escritas. **0 estrategias aprobadas**; F03-B quedó **descartada** por su propio spec
(criterio de frecuencia). F01 y F07 solo llegaron a un «dossier» (T-082).

**DATO — hubo que congelar el motor DOS veces**, ambas citando exceso de esfuerzo en él:
1. **D-8 (2026-07-19)** crea el carril `## DEUDA DE MOTOR (congelada por D-8)` en `TAREAS.md`.
2. **CONGELACIÓN DE MOTOR (2026-07-23, orden directa del usuario)** en `CLAUDE.md:87`: *«El objetivo
   del repo es PROBAR HIPÓTESIS de trading, no pulir el motor… NO se abren tareas nuevas de motor.»*

**OBSERVA — el freno no frenó del todo:** después del 2026-07-23 los commits siguieron siendo
mayoritariamente de motor (T-074 conforma `sizing.py`; T-077 instala el muro del contrato; la DEUDA
DE MOTOR sumó T-079, T-080, T-081, todas sin ejecutar), y el último commit del repo (T-082) es de
nuevo preparación, no un backtest.

**INTERPRETA.** El modo autónomo gastó la mayor parte del tiempo **construyendo, endureciendo y
contabilizando el propio motor** en lugar de avanzar el plan de trading, que progresó una sola
casilla (F03, además descartada en su variante B). Las dos congelaciones son la admisión explícita,
con fecha, de que el motor se comía a su propósito. **Matiz honesto:** parte de ese trabajo de motor
era prerrequisito real (bid-ask nativo, swap, sizing C1, guards OOS, invarianza DUMMY); sin él, un
backtest de F03 no sería fiable. Pero la proporción 36:15 y la necesidad de **dos** congelaciones
indican que la balanza se inclinó muy por encima de ese mínimo necesario.

---

## 6. RESTRICCIONES Y PERMISOS

### 6.1 Las capas (5 nominales, **4 reales** — ver §6.4)

| # | Capa | Mecanismo | Qué impide |
|---|---|---|---|
| 1 | `permissions.deny` (`.claude/settings.json`) | Patrones de prefijo | `curl/wget/ssh/scp/rsync/nc/telnet/sudo/su`; `Read` de `.env*`, `*.pem`, `*.key`, `credentials*`, `secrets/**`; **`Read` de OOS** (`data/**/2023*`…`2026*`, `data/oos/**`); `WebFetch` y `WebSearch` enteros |
| 2 | **Sandbox del SO** | `denyRead`/`denyWrite`, red a dominios listados | **NADA en esta instalación — no enforcea (§6.4)** |
| 3 | Hooks del harness (`.claude/hooks/`) | 9 scripts (ver abajo) | Cuarentena OOS, append-only, contrato, formato |
| 4 | Git hooks (`.githooks/`) | `pre-commit`, `commit-msg` | gitleaks + suite + alcance + contrato. **La puerta dura real** |
| 5 | Agentes `seguridad` + `auditor` | Revisión semántica (LLM) | Probabilística |

**Hooks del harness (capa 3):** `guard_bash.py` (veta rutas/descargas OOS, `rm` sobre
`data/`/`docs/`/`tests/`/`registry.csv`, `git push --force`, `--no-verify`, escritura por bash a
`decisiones.md`); `bash-guard.sh` (veta `--no-verify`, reconfigurar `core.hooksPath`, variantes
peligrosas de `git push`/`remote`, escritura de `.env`/`*.pem`/`*.key` — **se autodescribe «la capa
MÁS DÉBIL, regex, evadible»**); `guard_edit.py` + `proteger.sh` (bloquean editar `CLAUDE.md`,
`ROADMAP.md`, `data/`, specs `CONGELADO`); `registry_guard.py` y `decisiones_guard.py` (append-only,
byte a byte contra HEAD); `guard_bloqueadas.py` (impide reactivar tareas de `BLOQUEADAS`);
`gate.sh`, `log-bash.sh` (aviso y forense).

**Git hooks (capa 4):** `pre-commit` corre gitleaks (**falla cerrado** si no está instalado) + suite
pytest completa + append-only del registry con `--no-renames`. `commit-msg` valida formato de
mensaje y **alcance** (cada fichero staged debe estar en `.claude/tarea-actual.json`) y bloquea
`CLAUDE.md`/`ROADMAP.md` salvo si existe `MERGE_HEAD`. `pre-push` y los `post-*` son solo wrappers de
git-lfs: **no validan seguridad**; el muro real del push es el token y la branch protection de GitHub
(del usuario).

### 6.2 Reglas escritas (`CLAUDE.md`) y su respaldo mecánico

Las 8 Reglas Innegociables tienen respaldo desigual: **con muro** → Regla 1 (OOS: permisos +
guard_bash), Regla 4 (registry: registry_guard + pre-commit), Regla 7 (specs congelados:
guard_edit). **Solo prosa/procedimiento** → Regla 2 (no optimizar para métricas), Regla 3 (solo
variantes de spec), Regla 5-6-8 (bid-ask, splits, re-run DUMMY).

### 6.3 ¿Podían los agentes borrar y mover ficheros? — SÍ

**OBSERVA — no existe bloqueo general de `rm`/`mv`:** `guard_bash.py` bloquea `rm` **solo** sobre
`data/`, `docs/`, `tests/`, `registry.csv`; `bash-guard.sh` bloquea `rm`/`mv`/`cp` **solo** cuando el
objetivo es `.env`. **Fuera de esas rutas, un agente podía `rm`/`mv` cualquier fichero** (código en
`engine/`, informes en `results/`, tests fuera de `tests/`) sin que ningún hook lo parase. La única
red bajo eso es git (recuperable) + validación de alcance + auditor.

El agente **organizador** es el que «mueve ficheros y elimina código muerto», pero **todas sus
salvaguardas son prosa en su ficha**, no mecánicas (usar `git mv`, 1 commit por movimiento, suite
tras cada uno, aprobación humana en riesgo alto). Son reglas que un LLM puede desobedecer.

**OBSERVA — consecuencias reales:** no hay evidencia de pérdida grave por un borrado erróneo. Los
borrados en git fueron limpieza deliberada (varios staged por el humano: `059b35b9`, `eac642d6`,
`0ca53e96`, `0b8480a3`). El caso más cercano a un problema (`c0638cbe`, revert de T-022, se borraron
2 tests) **lo cazó el auditor y se revirtió**, no se perdió nada. **INTERPRETA.** El resultado fue
benigno, pero la **ausencia de muro mecánico contra `rm`/`mv`** fuera de rutas críticas es un hueco
real, agravado por §6.4.

### 6.4 «Capa 2 = ficción»: el sandbox del SO no enforcea (T-081)

**OBSERVA.** En el pase de `seguridad` del `/fin` del 2026-07-27 (rama `auto/20260724-1`),
**confirmado de forma independiente por el orquestador y medido a nivel de syscall**, se comprobó que:
`open('./CLAUDE.md','a')` → PERMITIDO; `open('./ROADMAP.md','a')` → PERMITIDO; **leer `./.env`** (que
está en `denyRead`) → PERMITIDO; escribir fuera del proyecto → PERMITIDO. **Todas deberían estar
bloqueadas por el sandbox de `settings.json`; ninguna lo está.** El entorno es WSL2 y `SEGURIDAD.md`
solo advertía de «Windows nativo».

**Qué resultó ficción:** la **capa 2 entera**. Toda la lista `denyRead`/`denyWrite` es declarativa e
inaplicada. La tabla de capas prometía «Alta: kernel-level»; el modelo real es de **cuatro capas, no
cinco**. Consecuencia: `printf >> CLAUDE.md` y la escritura por shell sobre `.env` quedan sin muro
(solo `bash-guard.sh`, regex evadible, para `.env`). Es tan real que T-077-fix **añadió y luego
retiró** una línea `denyWrite` del contrato «por ser ficción que finge protección».

**OBSERVA — lo que SÍ sigue en pie (verificado por ejecución):** las capas 1 y 3. Los guards OOS
**muerden** (bloquearon 6 comandos del revisor en vivo). **Las Reglas 1, 4 y 7 conservan muro real**
porque ninguna dependía de la capa 2.

**INTERPRETA.** Es el hallazgo de seguridad más grave del repo, y es **preexistente**: durante toda
la vida del proyecto la documentación asumió una capa kernel-level que nunca estuvo activa en WSL2.
La honestidad del equipo es notable (lo documentaron en toda su anchura en `SEGURIDAD.md` residual
#14 y lo encolaron como **T-081 [ALTO], PARADA-USUARIO**). Pero implica que toda afirmación previa de
«muro duro por sandbox» descansaba sobre una capa inexistente.

### 6.5 Restricciones relajadas o descubiertas como inexistentes

| Cambio | Fuente | Qué pasó |
|---|---|---|
| Política v5: config del motor pasa a EDITABLE | `SEGURIDAD.md` | `.claude/`, `.githooks/`, `ROADMAP.md`, `SEGURIDAD.md` dejan de estar blindados; se retira `PLANTILLA_ADMIN`. Amenaza «sabotaje de config» ACEPTADA con control humano a posteriori |
| D-9: `decisiones.md` deja de ser humano-only | D-9 (2026-07-20) | Los agentes firman verdictos; el gate anti-curve-fitting pasa de mecánico a procedimental |
| `ROADMAP.md` «protegido» era FICCIÓN | `CLAUDE.md:77`, D-13 | El comentario afirmaba una protección que ninguna línea implementaba; 2 commits de agente editaron el contrato. Corregido en T-077 |
| `commit-msg` eximía `org:`/`merge:` del alcance | `/fin` 2026-07-24 | El prefijo saltaba la validación del contrato. Cerrado en T-077 |
| Exención de merge falsificable | `957c42c8`, PoC del auditor | Escribir «merge:» en el mensaje saltaba el muro entero (sin `MERGE_HEAD`). Corregido; queda residual T-080 |

**INTERPRETA.** El patrón dominante **no** es relajar muros que funcionaban, sino **descubrir que un
muro anunciado nunca existió** (ROADMAP, capa 2, exención de merge). `--no-verify` y reconfigurar
`core.hooksPath` están duramente prohibidos y esa prohibición nunca se relajó.

---

## 7. QUÉ FUNCIONABA BIEN

Separando, como pide el encargo, «la idea es buena» de «el código es bueno»:

**Ideas que merecen sobrevivir:**

1. **La separación de poderes anti-autocomplacencia.** Quien produce las métricas **no** firma la
   decisión; quien implementa **no** testea; el auditor es adversarial por diseño («su trabajo es
   encontrar motivos para rechazar»). El agente que acaba de ver un PF es el peor situado para juzgar
   si un cambio está motivado por ese PF (D-9). Es la defensa estructural correcta contra el
   curve-fitting.
2. **El experimento define el éxito como «código correcto», no «estrategia rentable» (Regla 2).** Un
   backtest con PF 0.8 y código fiel al spec es un éxito registrable. Esto neutraliza el sesgo de
   toquetear parámetros hasta que «sale bien».
3. **La cuarentena OOS con firma humana insustituible (Regla 1).** Los datos 2023-2026 no existen
   para el repo, y ni el debate de agentes ni el `firmante` pueden autorizarlos: solo el humano.
   Verificado además por ejecución: los guards muerden.
4. **Append-only para registry y decisiones.** Una corrección se añade como fila/entrada nueva con
   nota, nunca reescribiendo. Preserva la honestidad del historial contra el borrado conveniente.
5. **El doble gate de cierre** (puertas de commit en verde **Y** veredicto APTO): «nadie se
   auto-aprueba».
6. **La distinción REGISTRO vs COMPUERTA con «test de compuerta»** (D-9): si la justificación de un
   cambio no se sostiene **sin citar métricas de resultado**, se deniega. Es una regla operativa
   afilada contra la racionalización a posteriori.
7. **Sesiones desechables con estado en disco.** La autonomía de horas se logra encadenando
   contextos frescos (`conductor.sh`), no alargando una sesión; el estado sobrevive en
   `ESTADO.md`/`TAREAS.md`. Arquitectura robusta frente al límite de contexto.
8. **`LECCIONES.md` con causa raíz + regla verificable + evento trazable.** Cada lección exige un
   evento de `metricas/` que la origine; «una regla sin evento trazable no tiene autoridad». Es un
   mecanismo de aprendizaje disciplinado y auditable.

**Piezas de implementación que funcionaron:**

9. **El motor de backtest propio con bid-ask nativo** (`engine/core/execution.py`): entradas en ask,
   salidas en bid, fills de stop sin mejora de precio, swap asimétrico con triple miércoles, sizing
   C1. La decisión de no usar vectorbt está justificada y documentada (D del 2026-06-13).
10. **La invarianza DUMMY como ancla de la Regla 8** (PF 0.914152 / 500 trades / 0 skips): un testbed
    sintético de semilla fija que detecta si un cambio de motor altera los números sin causa. Buen
    diseño de test de regresión de extremo a extremo.
11. **El pipeline de datos con test de cordura de precio conocido** (lección L-1: el bug de
    `PRICE_DIVISOR` que ponía el oro a ~$17/oz). Verificación de integridad al 100 % de cobertura
    2015-2022, 0 duplicados, 0 spreads negativos.
12. **La honestidad del equipo ante sus propios fallos.** El hallazgo de la «capa 2 = ficción» se
    documentó en toda su anchura en vez de ocultarse; las lecciones registran incluso cuando un
    diagnóstico previo era **falso** (ver la lección «Tres diagnósticos seguidos del registry, dos
    falsos»). Esta cultura de auto-corrección es, en sí, un activo.

---

## 8. LOS DIEZ ERRORES A NO REPETIR

Ordenados por daño causado al proyecto (mayor primero). Cada regla está escrita para copiarse tal
cual a un documento de normas.

### 1. El motor se comió al propósito: 70 % del esfuerzo en fontanería, 1 de 13 hipótesis probada
**Qué pasó.** En ~7 semanas, el 58 % de los 328 commits fueron gestión/motor/git, ~36 de 51 tareas
fueron de motor, 18 de los 20 ficheros más tocados eran motor/gestión, y de 13 hipótesis se
backtesteó **una** (F03, además descartada en su variante B). Hubo que congelar el motor **dos veces**
(D-8 el 19-jul; orden del usuario el 23-jul) y aun así siguió atrayendo commits.
**Evidencia.** `git log` (prefijos y `--name-only`); `results/registry.csv` (solo DUMMY+F03);
`CLAUDE.md:87`; `TAREAS.md:1580`; `ESTADO.md` («8 días sin correr un backtest»).
**Por qué hizo daño.** El objetivo declarado es probar hipótesis de trading; el sistema construyó
sobre todo más sistema. El plan real avanzó una casilla.
**Regla.** «Cada tirada autónoma debe cerrar al menos una tarea que avance el plan de producto; el
trabajo de infraestructura que no desbloquee mecánicamente una tarea de producto se registra como
deuda y no se ejecuta sin autorización explícita.»

### 2. Un muro de seguridad anunciado que nunca existió (sandbox = ficción durante toda la vida del repo)
**Qué pasó.** La «capa 2» (sandbox del SO, «kernel-level») nunca enforzó en WSL2: leer `.env`,
escribir el contrato y escribir fuera del repo estaban todos permitidos, medido a syscall. Toda la
lista `denyRead`/`denyWrite` era declarativa.
**Evidencia.** `SEGURIDAD.md` residual #14; `ESTADO.md:113-123`; T-081; T-077-fix retiró una línea
`denyWrite` «por fingir protección».
**Por qué hizo daño.** Varias decisiones de diseño («muro duro por sandbox») descansaban sobre una
capa inexistente; el equipo creyó estar protegido durante semanas.
**Regla.** «Toda capa de seguridad se verifica por ejecución —inyectando el caso prohibido y
comprobando que se bloquea— antes de documentarla como activa; una protección no probada se marca
"no verificada", nunca como muro.»

### 3. Guards verificados por presencia y no por ejecución; guards cableados al evento equivocado
**Qué pasó.** El guard OOS de `scripts/backtest_f03b.py` estaba estructuralmente muerto (comprobaba
una condición inalcanzable sobre un DataFrame ya recortado); nunca abortaba. Y `registry_guard`
estaba cableado a `Edit/Write` mientras el vector real de corrupción eran scripts por `Bash`: nunca
se disparó.
**Evidencia.** Lecciones «Guard OOS copiado que no guarda» (T-056) y «Guard cableado al evento
equivocado» (T-022).
**Por qué hizo daño.** Un guard que no muerde da **falsa sensación de seguridad**, peor que no
tenerlo. Se auditó «hay un `if … sys.exit`» = «está protegido».
**Regla.** «Todo guard se prueba disparando el caso prohibido y observando el bloqueo, y su matcher
se verifica contra el vector real de la amenaza (¿Bash? ¿Edit? ¿git hook?); un guard nunca se da por
bueno por su mera presencia en el código.»

### 4. Cada ronda de reparación introducía un defecto nuevo (tareas bloqueadas por agotar rondas)
**Qué pasó.** T-065 (12 defectos, 7 nacidos de reparaciones), T-062 (6 rondas, cada una con un
defecto nuevo) y T-074 se bloquearon **por la reparación**, no por el problema de fondo. El
implementador entregaba sin ejecutar ni leer su propio parche completo.
**Evidencia.** Lecciones 2026-07-23/24; `metricas/rechazos.csv`.
**Por qué hizo daño.** Tres tareas consecutivas agotaron su presupuesto de rondas y quedaron sin
mergear; consumió el grueso del tiempo de las últimas tiradas.
**Regla.** «El implementador ejecuta y lee su artefacto completo —todas las ramas, comentarios y
casos, incluidos los que los datos del día no tocan— antes de entregar; los gates confirman, no
descubren por primera vez.»

### 5. Citas fabricadas a decisiones firmadas, dentro del código de producción (4 apariciones)
**Qué pasó.** Se citó `«docs/decisiones.md, D-14-fix punto 2»` en 9 sitios de código donde
`grep -c "D-14-fix"` = 0 (T-074); se afirmó en `SEGURIDAD.md` que «las ediciones se RATIFICARON
(D-15)» **en pasado** cuando D-15 aún no existía (T-077); antes, una cita inventada a la enmienda
Opción C (T-062). Ya había regla en prosa para esto y no bastó.
**Evidencia.** Lecciones 2026-07-24 y 2026-07-27; también el precedente pre-motor L-8 (Gemini
inventando citas académicas).
**Por qué hizo daño.** Una cita inventada en código sobrevive a la lectura casual y contamina a quien
audite el módulo, y si alimenta el paquete del `firmante`, contamina un veredicto.
**Regla.** «Ninguna referencia a una decisión (`D-NN`, cláusula, enmienda) entra en código,
comentario, test o informe sin un `grep` previo que la localice por fichero y línea; una decisión se
cita solo cuando está firmada Y commiteada, nunca en pasado ni antes.»

### 6. Guards de seguridad afinados perdiendo el deny-by-default; exenciones que el propio agente activa
**Qué pasó.** Para quitar un falso positivo se reescribió un guard de `core.hooksPath` como
«allow-by-default»; `seguridad` demostró 4 bypasses críticos con PoC ejecutado, dos de los cuales
crearon un commit real. Y la exención de merge del muro del contrato se activaba por el **prefijo del
mensaje** («merge:»), que el propio agente escribe.
**Evidencia.** Lecciones «Guard afinado invirtiendo su default» (T-032) y «Una exención que activa un
token que el propio agente escribe no es una exención» (T-077).
**Por qué hizo daño.** Un guard allow-by-default pierde siempre contra quien inventa una forma nueva
de escribir; convierte un muro en un pase libre.
**Regla.** «Un guard de seguridad se escribe siempre deny-by-default (bloquea salvo whitelist
explícita); la condición que activa una exención debe ser un hecho que imponga el sistema (p. ej.
`MERGE_HEAD` lo crea git), nunca un dato que el sujeto controlado elija.»

### 7. Diagnosticar un componente sin leerlo (ni reproducir el fallo)
**Qué pasó.** Se culpó al writer del registry sin leerlo (estaba bien); se decidió cuál de dos
scripts era el bueno leyendo sus **cabeceras de documentación**, no su código, y se concluyó lo
contrario de la verdad (`bucle.sh` vs `conductor.sh`).
**Evidencia.** Lecciones «Tres diagnósticos seguidos del registry, dos falsos» (T-022) y «Duplicado
diagnosticado leyendo cabeceras» (T-026).
**Por qué hizo daño.** T-022 se escopó dos veces mal y se implementó una vez antes de revertirse
entera. La documentación describe la *intención*; solo el código describe el *comportamiento*.
**Regla.** «Un bug reportado por un agente no es un bug verificado: antes de encolar, escopar o
reparar sobre un componente, se lee ese componente y se reproduce el fallo; retirar o desduplicar
algo exige leer el código de todos los candidatos y verificar que el superviviente funciona.»

### 8. El estado del proyecto disperso en registros que no cuadran entre sí
**Qué pasó.** El día de la auditoría, git y `ESTADO.md` iban por T-082 (29-jul) mientras
`RUN-STATUS.json` y `metricas/tareas.csv` se quedaban en el 27-jul, y `T-077` aparecía duplicada y
colgada en `EN CURSO` y en `BLOQUEADAS`.
**Evidencia.** `RUN-STATUS.json`; `metricas/tareas.csv` (última fila T-061); `TAREAS.md:36` y `:1811`.
**Por qué hizo daño.** Quien confía en el sentinel o en las métricas ve un proyecto parado que en
realidad siguió; falta un paso que archive `EN CURSO` al parar una tirada, y quedan tareas zombis.
**Regla.** «Existe una única fuente de verdad del estado en curso, con campos parseables (estado,
fecha de cierre) y no prosa; al parar una tirada, la sección "en curso" se vacía o se archiva de
forma que ningún registro de estado quede stale.»

### 9. Ficha de tarea creada solo al cierre en runs de orden directa
**Qué pasó.** En tareas de orden directa del humano, el orquestador numeraba la tarea pero solo la
añadía a `TAREAS.md` **al cerrar**; durante el run la tarea no estaba en la única cola, así que el
auditor no podía validar su alcance contra la fuente de verdad.
**Evidencia.** Lección «Tarea de orden directa sin ficha en TAREAS.md» (T-058; antecedente T-056).
**Por qué hizo daño.** El alcance (qué ficheros pueden entrar en el commit) quedaba sin referencia
verificable durante todo el trabajo, justo lo que el muro de alcance debe proteger.
**Regla.** «El identificador y la ficha de una tarea se escriben en la cola ANTES de empezar a
trabajarla, nunca al cerrarla; sin ficha en la cola, no hay tarea.»

### 10. Referencias a código por número de línea y a símbolos que el propio cambio borra
**Qué pasó.** Docs, comentarios y docstrings citaban código por número de línea (que cualquier commit
posterior desplaza) o a símbolos que el mismo cambio eliminaba, sin verificar que siguieran
resolviendo. Tres rechazos del auditor por la misma causa (T-015, T-017, T-021).
**Evidencia.** Lección «Citas a código que dejan de resolver»; también «Verificación de retirada
acotada a los ficheros obvios» (T-035: un grep de markdown no ve una ruta muerta en un script).
**Por qué hizo daño.** Las referencias colgantes contaminan a quien lee después y desperdician rondas
de auditoría en fallos de forma.
**Regla.** «Las referencias a código se anclan por símbolo, nunca por número de línea; toda retirada
o renombrado de un símbolo corre `grep` sobre TODO el repo (código, tests, scripts, hooks, docs) y
deja cero referencias vivas antes de cerrar.»

---

## 9. LIMITACIONES DE ESTE ANÁLISIS

1. **Solo se leyó el árbol de la rama activa `auto/20260724-1`.** No se recorrió el contenido de las
   otras ~24 ramas `auto/*` ni de `main`; los conteos de commits usan `git log --all`, pero el estado
   de ficheros analizado es el de la rama activa. Trabajo vivo en otra rama no se ve.

2. **La clasificación «motor vs estrategia» de las tareas es interpretación, no dato.** Se basó en los
   títulos de commit; la frontera (T-074, T-021, T-019) es discutible en ±1-2 tareas. Los conteos de
   commits por prefijo sí son dato verificable.

3. **El rastro de los agentes solo-lectura es indirecto.** `explorador`, `auditor`, `seguridad` y
   `abogado-diablo` no commitean, así que su actividad se infiere de columnas de veredicto en CSV y
   de menciones en meta-commits. Para `organizador` el rastro es **ambiguo**: hay 35 commits `org:`,
   pero `org:` es una categoría que también usa el orquestador, y no se pudo probar que el subagente
   en sí se ejecutara. No se dispone de un log de invocaciones de subagentes que lo dirimiera.

4. **No se ejecutó nada.** Por la regla de solo-lectura no se corrió el motor, ningún backtest, ni
   los hooks o guards; su comportamiento se dedujo de leer su código y de las pruebas que el propio
   repo documenta (p. ej. la medición a syscall de la capa 2 la hizo el equipo, no esta auditoría).
   La afirmación «los guards OOS muerden» se apoya en evidencia del repo y en un bloqueo incidental
   observado durante los barridos, no en una batería de pruebas propia.

5. **Los registros de estado del propio proyecto están desincronizados** (ver §4.5): `metricas/*.csv`
   y `RUN-STATUS.json` se detienen el 2026-07-27, mientras git y `ESTADO.md` llegan al 29. Cualquier
   cifra tomada de las métricas subestima los dos últimos días de trabajo. Se prefirió git + ESTADO.md
   como fuentes cuando hubo conflicto.

6. **No se leyó `docs/decisiones.md` íntegro** (154 KB; se leyó ~1/3 y se localizaron entradas clave
   por `grep`). Es posible que decisiones intermedias no citadas aquí maticen algún punto; el hueco
   D-12 en el listado único de IDs (`D-1..D-16`) no se confirmó como hueco real o como simple no-cita.

7. **No hay acceso a telemetría externa.** `settings.json` envía eventos por `curl` a un panel local
   (`127.0.0.1:4747`); ese panel no es parte del repo y no se pudo consultar, así que cualquier
   métrica de ejecución que viviera solo allí queda fuera del análisis.

8. **`.claude/logs/bash-audit.log` se usó parcialmente.** Es un forense de ~4 700 líneas; se consultó
   por `grep` para el rastro de agentes, pero no se auditó línea a línea, de modo que patrones de uso
   poco frecuentes podrían haberse pasado por alto.

9. **Qué NO se pudo comprobar y no consta:** si los tres agentes inactivos (`backtest-runner`,
   `datos`, `mql5-ea`) **funcionarían** correctamente al invocarse (nunca se ejercitaron); si los
   números de los drivers `scripts/backtest_f03*.py` coinciden con los de `engine/run.py` (existe
   `test-parity.sh` pero no se ejecutó); y el contenido real de los datos OOS 2023-2026, que por la
   Regla 1 no se tocó ni se intentó tocar.
