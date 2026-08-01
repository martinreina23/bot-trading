# 01.02.03 — Auditoría del ecosistema externo de Claude Code

> Entregable de la tarea 01.02.03. Carril de MOTOR (regla 12 **del WBS**): cuenta contra el 20% y se
> limitó a una tirada. Ampliación de alcance ordenada por el CEO el 01/08/2026: además del catálogo
> `awesome-claude-code`, se barrieron las fuentes oficiales de Anthropic y los mecanismos nativos
> de Claude Code. Los MCP van en documento aparte (`INFORME_MCP.md`, tarea 01.02.04).
>
> **Estado: REPARADO tras RECHAZO.** Lo escribió el orquestador en sesión principal, no el agente
> `investigador`. Por la regla 16 **de CLAUDE.md** no puede firmarlo quien lo escribió.
> `critico-codigo` lo RECHAZÓ el 01/08 por un fallo de método en el número de la propuesta P1; la
> corrección está aplicada abajo y el hallazgo del revisor está incorporado, no maquillado.
>
> **AVISO DE NUMERACIÓN, y es un hallazgo del revisor que afecta a todo el proyecto.** Existen DOS
> listas de «29 reglas» con contenido distinto bajo el mismo número: la de `CLAUDE.md` y la de
> `00-direccion/WBS.md`. Comprobado por `grep` el 01/08: la regla 16 es «nadie valida su propio
> trabajo» en `CLAUDE.md` y «test de compuerta» en el WBS; la 23 es «dos niveles de barrera» frente
> a «un fallo reportado no es un fallo verificado»; la 25 es «toda barrera se verifica por
> ejecución» frente a «cada agente lleva el identificador exacto de su modelo». **Convención de este
> informe: salvo que se diga «del WBS», toda cita `regla N` es la numeración de `CLAUDE.md`.** El
> arreglo de fondo no es de este informe: es la tarea 03.01.13.

## Resumen en tres líneas

El catálogo `awesome-claude-code` está vivo (51.432 estrellas, último empuje 01/08/2026) y no
contiene **ninguna** pieza que merezca entrar aquí. Las cuatro propuestas que siguen son
**mecanismos nativos de Claude Code que ya están instalados y sin usar**, no dependencias nuevas.
Las cuatro atacan el mismo agujero: reglas que el propio `CLAUDE.md` clasifica como «solo prosa».

Versión sobre la que se audita: `claude --version` → **2.1.220**, comprobado por ejecución el
01/08/2026.

---

## A) LAS CUATRO PROPUESTAS

Ninguna instala software de terceros. Todas son ficheros del propio repositorio.

### P1 — Contador mecánico producto/motor (hook `SessionStart`)

- **Qué necesidad resuelve:** la 1 (que los agentes no se desvíen del WBS). Hoy el techo del 20%
  de motor es prosa: nadie lo mide. En gb2 el 70% del esfuerzo se fue al motor sin que saltara nada.
- **Cómo:** un hook `SessionStart` calcula del `git log` el reparto producto/motor y lo inyecta en el
  contexto con `hookSpecificOutput.additionalContext`. El agente empieza cada tirada con el número
  delante, no con la buena intención.
- **CORRECCIÓN DEL 01/08 TRAS EL RECHAZO DE `critico-codigo`. La primera versión de este informe
  decía «10 commits llevan código WBS; 2 son de fase 03 → 20,0%, exactamente en el techo». La
  aritmética era correcta y el método estaba mal.** El denominador excluía 6 de los 16 commits del
  repositorio: los que `.githooks/commit-msg` **exime de llevar código WBS** por empezar con
  `meta:`, `org:` o `arranque:`. Reproducido por el orquestador con `git show --stat` sobre esos
  seis: cinco son trabajo de motor u orden por contenido — `arranque del proyecto` crea los 8
  agentes y `.claude/settings.json` (es la tarea 03.01.01), `meta: andamiaje v2` crea 9 comandos y
  los dos hooks de git (449 líneas), `org: estados del WBS al dia` toca `generar_excel.py` (1.184
  líneas), `org: vista del CEO` añade `verificar_excel.py` y `prueba_inyeccion.sh` (338 líneas), y
  `org: ignorar los ficheros de bloqueo` es orden pura.
- **DATO REAL, clasificando por contenido y no por prefijo del mensaje:** el motor y el orden suman
  **7 de 16 commits (43,8%)**, u 8 de 16 (50,0%) si se cuenta también el borrado de `atr_local.py`.
  **Más del doble del techo del 20%, no «exactamente en el techo».** El proyecto llevaba desde el
  arranque sin saberlo.
- **Consecuencia para el diseño de P1, que es lo que de verdad reparó el rechazo:** el indicador
  **no puede contar solo los commits con código WBS**. Es ciego por construcción, porque el trabajo
  de motor es precisamente el que se cuela bajo `meta:` y `org:`. Sin esa corrección, P1 habría
  automatizado el punto ciego para siempre: la falsa seguridad de L-009 aplicada a un indicador en
  vez de a un guardia.
- **TRAMPA QUE SE COMIÓ EL PRIMER INTENTO DE ARREGLO, cazada por `critico-codigo` en la ronda 2 y
  reproducida por el orquestador.** La reparación inicial proponía clasificar por rutas tocadas,
  con `03-motor/** → motor`. **Está mal, y es el error contrario.** De los 7 commits que tocan
  `03-motor/scripts/`, **cinco son cálculo de PRODUCTO** — `arrastre_coste.py` (criterio G1-C1),
  `coste_relativo.py` (criterio 1 de G1), `correlaciones_mercado.py` y `precios_mercado.py` (ATR y
  correlaciones) — y solo dos son infraestructura de verdad (`cajon_reservado.py`,
  `verificar_barreras.py`). Es una **colisión de nombres**: «motor» en `CLAUDE.md` significa la
  fábrica de agentes, mientras que la carpeta `03-motor/` es donde vive el cálculo del bot, que
  según esa misma frase de `CLAUDE.md` («el motor es la fábrica; el bot es el producto») **es el
  producto**. Esa regla habría contado como motor el trabajo analítico central del proyecto, y peor
  aún en cuanto se escriba el backtester ahí dentro.
- **REGLA DE CLASIFICACIÓN CORREGIDA, verificada por ejecución el 01/08 sobre los 16 commits:**
  1. Commit **con** código WBS → decide la **fase**: 02, 04, 05 y 06 son producto; **03 y 07 son
     motor**. El código WBS es la declaración autorizada de qué era ese trabajo.
     **La Fase 01 se parte, y no es un detalle** (hallazgo de `critico-codigo` en la ronda 3,
     aplicado aquí): **01.01.\* es producto** (dirección y puertas: aprobar el plan, los criterios de
     G1 y los límites) pero **01.02.\* es MOTOR**, porque sus propias fichas del WBS lo declaran por
     escrito — 01.02.03 y 01.02.04 llevan «Carril de motor: cuenta contra el 20%» en su celda.
     Contar la Fase 01 entera como producto habría clasificado **esta misma auditoría** como
     producto, que es justo lo contrario de lo que dice su ficha. Comprobado por ejecución que no
     mueve la cifra de hoy: los dos únicos commits con código de Fase 01 son `01.01.02` y `01.01.03`,
     ambos dirección. Empezará a importar en cuanto se commiteen 01.02.03 y 01.02.04.
     **Descuadre a resolver en 03.01.13, no aquí:** `.claude/agents/orquestador.md` define el
     producto como «fases 02, 04, 05, 06», sin la Fase 01. Esa lista y esta tienen que decir lo
     mismo, o el indicador y el criterio de cierre de tirada discreparán.
  2. Commit **sin** código WBS (los que `commit-msg` exime por `meta:`, `org:` o `arranque:`) → se
     clasifica por rutas: toca `.claude/**`, `.githooks/**`, `05-vista-ceo/**` o un fichero de
     configuración de la raíz (`CLAUDE.md`, `INSTALAR.md`, `README.md`, `requirements.txt`,
     `.gitignore`) → **motor**; toca **solo** `00-direccion/**` → **papeleo**, que se declara aparte
     y no entra en el cociente; el resto → producto.
  3. **`03-motor/**` no se usa nunca como criterio**, por el motivo del punto anterior.
- **Comprobación de que la regla corregida funciona:** ejecutada sobre los 16 commits da
  **7 motor / 9 producto / 0 papeleo = 43,8%**, el mismo número que la clasificación manual por
  contenido. Que dos métodos independientes coincidan es lo que permite fiarse del indicador; ese
  contraste es el criterio de aceptación del hook cuando se construya.
- **Coste de integración:** ~40 líneas de bash + una entrada en `.claude/settings.json`. Media tirada.
- **Riesgo declarado:** un commit no es una unidad de esfuerzo y un commit puede tocar rutas de los
  dos lados. Es un **indicador**, no una medida. Su valor no está en la cifra exacta sino en que
  deje de ser cero: hasta hoy no existía ninguna.
- **¿Se puede con 20 líneas propias?** Sí, y por eso se propone: son 20 líneas propias, no una
  dependencia. Lo que aporta el mecanismo nativo es que **se ejecuta solo**, sin depender de que
  alguien se acuerde.

### P2 — Registro de autoría y bloqueo de la auto-revisión (hooks `PostToolUse` + `PreToolUse`)

- **Qué necesidad resuelve:** la 5 (nadie se valida a sí mismo). Es la regla 16 y hoy es prosa pura.
- **Cómo, en dos niveles de ambición:**
  - **Nivel 1 (barato, sin riesgo):** un hook `PostToolUse` con matcher `Write|Edit` escribe una
    línea en `04-resultados/autoria.jsonl` con el fichero tocado y el `agent_type` que lo tocó. El
    campo `agent_type` viaja en la entrada JSON de todo hook cuando corre dentro de un subagente
    (documentación oficial de hooks, sección de campos comunes de entrada). Con eso la regla 16
    pasa de incomprobable a **auditable a posteriori**.
  - **Nivel 2 (muro de verdad):** un `PreToolUse` sobre la escritura del veredicto devuelve
    `permissionDecision: "deny"` cuando el `agent_type` que firma coincide con el que consta como
    autor del artefacto. **Diseño propuesto, NO probado.** No entra como activo hasta inyectar el
    caso prohibido —un `critico-codigo` revisando lo que escribió `critico-codigo`— y ver que se
    bloquea (regla 25).
- **Coste:** nivel 1, ~15 líneas y media tirada. Nivel 2, ~60 líneas más su prueba de inyección,
  una tirada entera.
- **Riesgo:** un hook `PreToolUse` mal escrito bloquea escrituras legítimas. Por eso el nivel 1
  primero, y el 2 solo si el registro demuestra que el problema ocurre.

### P3 — Detección de fallo o rechazo de modelo (hooks `StopFailure` + `SubagentStop`)

- **Qué necesidad resuelve:** desbloquea la mitad mecánica de la tarea **03.01.04** (plan de
  respaldo de modelos), hoy `pendiente`. Importa porque `validador` y `arquitecto` corren sobre
  `claude-fable-5`, que estuvo suspendido en junio de 2026 y puede rechazar peticiones.
- **Cómo:** `StopFailure` se dispara cuando un turno termina por error de API y admite matcher por
  **tipo de error** (`rate_limit`, `overloaded`, `authentication_failed`, `server_error`, entre
  otros). El hook escribe la incidencia en el informe de la tirada.
- **Límite honesto, para no vender humo:** un hook **no puede cambiar el modelo**. Convierte un
  fallo silencioso en un fallo registrado, que es la mitad de 03.01.04. El cambio al respaldo
  sigue siendo procedimiento del orquestador. La tarea 03.01.04 debe reescribirse con esa
  separación explícita.
- **Coste:** ~20 líneas. Media tirada.
- **Riesgo:** ninguno; no bloquea nada.

### P4 — Ejecución desatendida nativa, y el agujero del tope de gasto

- **Qué necesidad resuelve:** la 4 (vigilar el gasto sin que el humano mire) y desbloquea **03.01.03**.
- **Cómo:** `claude -p` (modo no interactivo) lanzado desde el `cron` del sistema. No hace falta
  ninguna pieza del catálogo. Los arranques programados de 03.01.03 son dos líneas de crontab.
- **HALLAZGO QUE 03.01.03 NECESITA SABER:** *Claude Code no ofrece un tope de gasto duro por
  sesión ni por proyecto, ni un tope que tú elijas.* Lo que existe, según la documentación oficial
  de costes: `/usage` (mirar, no bloquear), límites de gasto de workspace **solo en la Claude
  Console con clave de API**, y exportación OpenTelemetry a un sistema propio. **Matización añadida
  tras la revisión de `critico-codigo`, que la comprobó en la documentación oficial y el informe
  original se saltaba:** en planes Pro y Max **sí hay un corte automático**, pero no es un tope
  configurable: es el propio límite del plan, que bloquea hasta que se reinicia la ventana o hasta
  que se activan créditos de uso explícitamente. Sirve como techo de gasto solo mientras no se
  activen créditos. Con facturación por token (Console o API), que es el modelo que la tabla de
  precios del WBS asume, no hay corte alguno. **Consecuencia:** el «tope de gasto» que 03.01.03 da
  por hecho no se puede implementar como muro elegido por el proyecto con la configuración actual.
  Las salidas son decisión del CEO, porque implican gasto nuevo o cambio de forma de pago (regla 23).
  Ficha pendiente.
- **Lo que sí se puede hacer sin gastar nada:** `maxTurns` por agente en su ficha (tope de turnos),
  `MAX_THINKING_TOKENS` y niveles de esfuerzo por agente. Son topes de *trabajo*, no de dinero, y
  hay que llamarlos por su nombre.
- **Coste:** crontab, media tirada. La ficha del tope de gasto, aparte.

---

## B) DESCARTADAS, CON MOTIVO

Actividad comprobada por la API de GitHub el **01/08/2026**. Ninguna se descarta por abandono:
**todas están vivas**. Se descartan por no encajar.

| Pieza | Último empuje | Motivo del descarte |
|---|---|---|
| `obra/superpowers` | 2026-07-31 | Paquete de competencias de ingeniería de software (ciclo de desarrollo). Este proyecto no construye software: calcula números y los verifica. Resuelve un problema que no tenemos |
| `garrytan/gstack` | 2026-07-15 | «Fábrica de software» de extremo a extremo. Mismo motivo, y además impone su propio ciclo de trabajo, que competiría con el WBS: rompería la regla de fuente única |
| `frankbria/ralph-claude-code` | 2026-07-18 | Bucle autónomo «hasta terminar». Es exactamente el patrón que mató a gb2: iterar sin puerta de cierre. `/autonomo` ya tiene condiciones de parada explícitas |
| `WenyuChiou/agent-collab-skills` | 2026-07-11 | Reparto y reconciliación entre agentes. Duplica al orquestador, que ya reparte por tipo de tarea |
| `mrtooher/fable-mode` | 2026-07-10 | Planificación multietapa y auto-verificación por *prompt*. Auto-verificación es precisamente lo que la regla 16 prohíbe |
| Categoría **Memory & Context Persistence** entera (`claude-mnemonic` 2026-07-30, `roampal-core` 2026-07-30, `MAMA`, `presence`, `Selvedge`, `Hivemind`, `capy`, `fable`, `Callimachus`) | vivas | **Descarte de bloque y es el descarte importante.** Guardan la memoria en grafos, SQLite o índices propios. Aquí la memoria son `DECISIONES.md`, `LECCIONES.md` y `registro-pruebas.md`: ficheros de texto, versionados en git, que solo admiten añadir y **se pueden localizar con `grep`**. La regla 12 de `CLAUDE.md` (= regla 20 del WBS) exige que toda cita se localice por fichero antes de entrar en código o informe. Una memoria opaca hace esa comprobación imposible: cambiaría un mecanismo verificable por uno que hay que creerse |
| `leeguooooo/claude-code-usage-bar` | 2026-07-27 | Comprobado en su README: **es solo pantalla, no bloquea**. Necesidad 4 dice «sin que el humano tenga que mirar»; una barra de estado exige justo eso. El CEO mira una hora a la semana |
| `stefanprodan/cctop`, `c9watch`, `Claude Code Agent Monitor` | vivas | Paneles de vigilancia en vivo. Mismo motivo: requieren un humano delante |
| `JeongJaeSoon/agent-guard` | 2026-07-30 | Fugas de secretos. Aquí no hay secretos: no hay claves de broker, no hay remoto |
| `cleatdev/cleat` | 2026-07-25 | Jaula Docker para el agente. Contradice la decisión ya firmada de dos niveles (permisos amplios en lo reversible porque git lo deshace). Sería añadir una restricción sin incidente detrás, que la regla 24 prohíbe |
| `kenryu42/claude-code-safety-net` | — | **La entrada del catálogo apunta a una URL que ya no existe**: la API devuelve 301 hacia `kenryu42/cc-safety-net`. Aparte del enlace roto, protege contra `git` y borrados destructivos, que aquí ya cubre el `pre-commit` propio |
| `anthropics/claude-code-action`, `anthropics/claude-code-security-review` | oficiales, vivas | **Inaplicables por un hecho verificado:** `git remote -v` devuelve vacío. No hay repositorio en GitHub, no hay pull requests, no hay CI. Usarlas obligaría a publicar el proyecto, que es una decisión del CEO y no un detalle técnico |
| `anthropics/claude-plugins-official` | 2026-08-01 | Directorio oficial de plugins. Un plugin es una dependencia que se actualiza sola bajo los pies del proyecto. Con ocho agentes propios ya escritos, aporta cero y añade superficie móvil |
| `anthropics/skills` (formato SKILL.md) | 2026-07-24 | El formato ya se usa: los comandos de `.claude/commands/` cumplen la misma función. Sus habilidades de ofimática (xlsx) están cubiertas por `generar_excel.py` y `verificar_excel.py`, que además verifican por ejecución |
| Categorías **Status Lines**, **Alternative Clients**, **Design & UI/UX**, **Creative Media**, **Writing** | — | No tocan ninguna de las cinco necesidades |

**Criterio que produjo estos descartes, dicho a las claras:** el catálogo está construido para
equipos que escriben software y quieren que el agente escriba más deprisa. Este proyecto no tiene
un problema de velocidad: tiene un problema de *confianza en los números*. Casi todo el catálogo
optimiza lo primero.

---

## C) LO QUE EL CATÁLOGO NO CUBRE

| Necesidad | ¿Hay pieza? | Qué falta y quién lo tiene que construir |
|---|---|---|
| 1. No desviarse del WBS | No | Nadie publica un guardia que lea *tu* WBS. Es P1, y es propio |
| 2. Memoria persistente | Sí, pero se rechaza | Los ficheros de texto versionados son **mejores** aquí, no peores, porque son verificables con `grep`. No falta nada |
| 3. Barreras sobre lo irreversible | No | Las piezas públicas protegen ficheros y secretos. Lo irreversible aquí es *dinero real y órdenes al broker*, y no existe pieza pública para eso. Lo construye el proyecto: la parada dura del -30% (D-14) vive en el bot, en 05.01.01 |
| 4. Vigilancia del gasto | **No, y es el hueco serio** | Todo lo publicado es pantalla. Y el propio Claude Code no da tope duro con suscripción. Es lo que hay que llevar al CEO |
| 5. Contraste sin auto-validación | No | Ninguna pieza pública sabe qué agente escribió qué. Es P2, y es propio |

**Conclusión de la sección C, que es la conclusión del informe:** cuatro de las cinco necesidades
no tienen solución externa decente, y la quinta ya está mejor resuelta en casa. Las cuatro
propuestas de la sección A son código propio sobre mecanismos nativos. **Cero dependencias nuevas.**

---

## Criterio para futuras auditorías del ecosistema

Para no repetir esta tirada cada vez que salga un repositorio con estrellas:

> Una pieza externa solo entra si **desbloquea mecánicamente una tarea del WBS** que hoy está
> parada, y si lo que hace **no se puede escribir en menos de 100 líneas propias**. La popularidad
> no es criterio: `superpowers` tiene 264.584 estrellas y no sirve aquí.
