# 01.02.04 — ¿Merece la pena añadir servidores MCP a este proyecto?

> Entregable de la tarea 01.02.04 (nueva, ordenada por el CEO el 01/08/2026). Completa a
> `INFORME_AWESOME.md` (01.02.03): ese informe cubrió el catálogo `awesome-claude-code` y los
> mecanismos nativos de Claude Code; **este cubre exclusivamente servidores MCP**, sin repetir nada
> de lo ya escrito allí.
>
> Contexto verificado por ejecución, dado por bueno sin repetir la comprobación: `claude --version`
> → 2.1.220 · `git remote -v` vacío (no hay remoto) · no existe `.mcp.json` en el proyecto → **hoy
> hay CERO servidores MCP configurados**.
>
> Método: barrido de los servidores de referencia oficiales (`modelcontextprotocol/servers` y su
> repositorio hermano archivado), de proveedores conocidos (GitHub, Microsoft, Google, Kraken,
> Alpaca), y de servidores de datos financieros y de trading, con verificación de actividad por la
> API de GitHub (`api.github.com/repos/<owner>/<repo>`, campo `pushed_at`) el 01/08/2026 salvo donde
> se indica «no verificado». Es trabajo de investigación sobre el motor: por la misma regla que
> `INFORME_AWESOME.md` (regla 12 de CLAUDE.md), cuenta contra el carril del 20% y se limita a esta
> tirada.

---

## A) VEREDICTO EN UNA LÍNEA

**Cero servidores MCP se proponen añadir HOY. Dos categorías quedan como candidatas condicionales**
(navegador y broker), cada una con un disparador concreto y comprobable que hoy no se cumple; el
resto —datos de mercado, ficheros, memoria, utilidades genéricas— se descarta sin condición.

---

## B) PROPUESTOS

**Ninguno.**

No hay ninguna tarea del WBS hoy bloqueada que un servidor MCP desbloquee mecánicamente y que no
esté ya resuelta con herramientas nativas (`Bash`, `Read`, `WebFetch`) o con el script propio de
`03-motor/scripts/` (`precios_mercado.py`). El criterio que ya fijó `INFORME_AWESOME.md`
para el catálogo de agentes vale igual aquí: **una pieza externa entra solo si desbloquea
mecánicamente una tarea del WBS que hoy está parada, y si lo que hace no se puede escribir en menos
de 100 líneas propias.** Ningún servidor evaluado lo pasa.

---

## C) DESCARTADOS, UNO POR UNO

### Servidores de referencia oficiales (`modelcontextprotocol/servers`)

Los siete viven en el mismo repositorio: **`pushed_at` 2026-07-29, `updated_at` 2026-08-01,
89.111 estrellas** (verificado por la API de GitHub, 01/08/2026). Vivos los siete. Se descartan
todos, uno por uno:

| Servidor | Qué hace | Motivo del descarte | Regla |
|---|---|---|---|
| **filesystem** | Lectura/escritura de ficheros con control de acceso configurable | Duplica exactamente lo que ya hacen `Read`/`Edit`/`Write` nativos, que ya tienen reglas `allow`/`deny` escritas y funcionando. Añadirlo no desbloquea ninguna tarea; solo abre una segunda vía de acceso a disco con un espacio de nombres de permisos distinto (`mcp__filesystem__*`) que las reglas `deny` actuales NO cubren — ver el riesgo documentado más abajo | Reglas 22, 23, 26 |
| **git** | Operaciones de git (status, commit, diff, log, branch...) vía la librería `gitpython` (confirmado en `pyproject.toml` del servidor, dependencia `gitpython>=3.1.50`) | El proyecto ya opera git por `Bash(git *)`, con `.githooks/commit-msg` y `.githooks/pre-commit` verificados contra el binario `git` real. Ningún task del WBS pide un cliente git alternativo. Riesgo adicional sin resolver: `gitpython` no shellea al binario `git`, construye commits de forma programática; si alguna vez se usara para commitear, habría que reverificar por inyección (regla 25) que el hook `commit-msg` (que exige código WBS) sigue disparándose igual que con `git commit` normal — no verificado, y no hace falta verificarlo porque no hay motivo para adoptarlo | Reglas 22, 25 |
| **memory** | Memoria persistente como grafo de conocimiento | Es el mismo problema que `INFORME_AWESOME.md` ya cerró de bloque para toda la categoría "Memory & Context Persistence": la memoria de este proyecto son `DECISIONES.md`, `LECCIONES.md` y `04-resultados/registro-pruebas.md`, texto versionado, solo-añadir, localizable con `grep`. Un grafo opaco no se puede citar por fichero y línea | Reglas 12, 20, 21, 28 |
| **sequential-thinking** | Encadenar pasos de razonamiento explícitos como herramienta | No resuelve ninguna tarea del WBS; es una ayuda de razonamiento genérica, no un dato ni un guardia. El presupuesto de pensamiento ya es configurable de forma nativa (`MAX_THINKING_TOKENS`, citado en `INFORME_AWESOME.md`, propuesta P4) | Criterio de `INFORME_AWESOME.md` (ninguna tarea desbloqueada) |
| **fetch** | Descarga y convierte HTML a Markdown para LLM | Redundante con la herramienta nativa `WebFetch`, usada con éxito en esta misma investigación (documentación oficial, GitHub, etc.). La documentación oficial de costes lo dice de forma literal, sección «Reduce MCP server overhead»: *"Prefer CLI tools when available: Tools like `gh`, `aws`, `gcloud`, and `sentry-cli` are still more context-efficient than MCP servers because they don't add any per-tool listing"* — es exactamente este caso: `WebFetch` ya cubre la descarga y conversión sin el coste de listado por herramienta que añade un servidor MCP | [Manage costs effectively — Claude Code Docs](https://code.claude.com/docs/en/costs), sección «Reduce MCP server overhead», consultada 01/08/2026 |
| **time** | Conversión de hora y zona horaria | `date` por `Bash` y el propio reloj del sistema ya cubren esto; ninguna tarea del WBS necesita zonas horarias adicionales a las ya fijas (corte 22:00 UTC, ya resuelto en `precios_mercado.py`) | Ninguna tarea desbloqueada |
| **everything** | Servidor de referencia/pruebas para demostrar el propio protocolo MCP | Es un servidor de demostración para quien construye *clientes* MCP, no una herramienta de producto | Ninguna tarea desbloqueada |

### `sqlite` — confirmado archivado

**Confirmado por dos fuentes independientes**: el propio repositorio
[`modelcontextprotocol/servers-archived`](https://github.com/modelcontextprotocol/servers-archived)
y el README actual de `modelcontextprotocol/servers`, que remite a él. Se movió al repositorio
archivado el **28-29 de mayo de 2025**, junto con otros 12 servidores de referencia (AWS KB
Retrieval, Brave Search, EverArt, GitHub, GitLab, Google Drive, Google Maps, PostgreSQL, Puppeteer,
Redis, Sentry, Slack). El propio repositorio archivado declara: *"NO SECURITY GUARANTEES ARE
PROVIDED FOR THESE ARCHIVED SERVERS"*. Descartado por dos motivos independientes, cualquiera de los
dos ya basta: (1) sin mantenimiento y sin garantías de seguridad declaradas por el propio autor, (2)
este proyecto no usa SQLite en ningún punto del pipeline — los artefactos de datos son JSON y texto
(`atr_15m_1h_4h.json`, `correlaciones_8x8.json`, `coste_relativo_15m_1h_4h.json`), no hay ninguna
base de datos que consultar.

### `github`

El servidor de referencia de Anthropic para GitHub está deprecado; GitHub tomó la propiedad del
proyecto y lo mantiene como servidor oficial en `github/github-mcp-server`
(**`pushed_at` 2026-07-31, 31.881 estrellas**, verificado por la API de GitHub, vivo). Descartado
por un hecho ya verificado y dado en el contexto de la tarea: **`git remote -v` devuelve vacío. No
hay repositorio remoto, no hay *pull requests*, no hay *issues*, no hay CI que gestionar.** Mismo
motivo exacto por el que `INFORME_AWESOME.md` ya descartó `anthropics/claude-code-action` y
`anthropics/claude-code-security-review`. Usarlo obligaría primero a publicar el proyecto en GitHub,
que es una decisión del CEO y no un detalle técnico de esta tarea.

### Datos de mercado

| Servidor / familia | Actividad verificada | Motivo del descarte | Regla |
|---|---|---|---|
| **yfinance MCP** (`narumiruna/yfinance-mcp`, `pushed_at` 2026-07-30, 173 estrellas; y al menos 6 implementaciones más no oficiales: `barvhaim`, `9nate-drake`, `everdeep`, `St-Lark-Ventures`, `Alex2Yang97`, `AgentX-ai`) | Vivo, pero fragmentado: no hay un único servidor "oficial" | La ficha de la tarea **02.02.01** ya jubiló Yahoo/yfinance explícitamente como fuente ("Se jubila Yahoo/yfinance") a favor de HistData, Dukascopy y Kraken. Un MCP de yfinance reintroduciría exactamente la fuente descartada, con el riesgo adicional de que sus tickers de forex/oro no sean el mismo instrumento que Dukascopy al contado (L-007) | Ficha 02.02.01, L-007 |
| **TradingView MCP** (`bidouilles/mcp-tradingview-server`, `pushed_at` 2026-06-22, 22 estrellas; y al menos 6 forks personales más: `atilaahmettaner`, `pilpilon`, `hilmituncay`, `cklose2000`, `ali-rajabpour`, `tradesdontlie`) | Vivo pero muy fragmentado, todo proyectos personales sin versión oficial de TradingView | Su función central es entregar **indicadores técnicos ya calculados** por TradingView. Es exactamente lo que la regla 14 (y L-001) prohíbe: todo dato numérico se calcula sobre datos brutos disponibles, y aquí los datos brutos (HistData/Dukascopy/Kraken) ya se descargan y el ATR ya se calcula con la función `atr14` de `precios_mercado.py` (script propio) | Regla 14, L-001 |
| **QuantConnect MCP** (`QuantConnect/mcp-server`, oficial, `pushed_at` 2026-05-07, `updated_at` 2026-07-29, 77 estrellas) | Vivo, oficial | Es un puente hacia la *plataforma* QuantConnect (crear proyectos, backtestear y desplegar en vivo dentro de su entorno, con credenciales de cuenta). Contradice directamente la decisión **D-6** (repositorio propio, motor de backtest propio, trasplante verificado pieza a pieza desde gb2 — sección "Trasplante desde gb2", pieza T2). Adoptarlo significaría delegar el motor de backtest a un tercero justo cuando el proyecto decidió lo contrario, y además implica una cuenta y credenciales externas (gasto/dependencia nueva, que exige aviso al CEO) | D-6, regla 23 (gasto/dependencia nueva) |
| **ccxt MCP** (`doggybee/mcp-server-ccxt`, `pushed_at` 2025-06-03 — **más de un año sin empujar** a fecha de esta auditoría; y al menos 4 implementaciones más fragmentadas: `Nayshins`, `carlosatta`, `Obinox04`, `lazy-dinosaur`) | El candidato con más estrellas está desactualizado; el resto, sin versión canónica | Envuelve genéricamente más de 100 exchanges de cripto sin el cuidado que exige L-007 (bitcoin contra Tether ≠ contra dólar) que ya se resolvió a mano en `precios_mercado.py` para Kraken. La tarea 02.02.01 ya está **hecha** con script propio, verificado dígito a dígito por `critico-codigo`; sustituirlo por un MCP genérico no aporta nada y reabre el riesgo de instrumento equivocado | L-007, ficha 02.02.01 |

---

## RIESGO VERIFICADO: ¿abre un MCP de ficheros una segunda vía al cajón reservado?

**Sí, el riesgo es real — confirmado por verificación documental de la documentación oficial de
Claude Code, no por prueba de intrusión (regla 22: el cajón reservado no se toca ni se intenta
abrir).**

Las cuatro reglas `deny` de `.claude/settings.json` que protegen `02-datos/reservado/` —
`Read(./02-datos/reservado/**)`, `Edit(./02-datos/reservado/**)`, `Write(./02-datos/reservado/**)`
y `Bash(* 02-datos/reservado*)` — están escritas contra los nombres canónicos de las herramientas
**nativas** `Read`, `Edit`, `Write` y `Bash`.

La documentación oficial de permisos (`code.claude.com/docs/en/permissions`, sección "MCP",
consultada 01/08/2026) dice explícitamente: *"MCP rules use the server name as configured in Claude
Code, optionally followed by the name of a tool from that server"* — el patrón es
`mcp__<servidor>` o `mcp__<servidor>__<herramienta>` (por ejemplo `mcp__filesystem__read_file`).
Es un **espacio de nombres de permisos completamente distinto** al de las herramientas nativas. La
misma página, en la sección "Read and Edit", limita expresamente el alcance de esas reglas: *"Read
and Edit deny rules apply to Claude's built-in file tools"* — a las herramientas nativas, no a
ninguna otra.

Consecuencia comprobada por lectura de la documentación, no por ejecución: si algún día se añadiera
un servidor MCP de tipo `filesystem` (u otro que lea o escriba ficheros, por ejemplo una `memory`
que persista a disco) con acceso a la raíz del proyecto, **ninguna de las cuatro reglas `deny`
actuales le afectaría**, porque sus herramientas se llamarían `mcp__filesystem__read_file`,
`mcp__filesystem__write_file`, etc., nombres que las reglas de hoy no mencionan. Además, el sistema
de permisos de Claude Code **no ofrece sintaxis de patrón de ruta para herramientas MCP** (el
`Read(./ruta/**)` de estilo gitignore solo existe para `Read`/`Edit`); la única forma mecánica de
bloquear parte de lo que expondría un MCP de ficheros es bloquear la **herramienta o el servidor
entero** (`mcp__filesystem` o `mcp__filesystem__read_file` en `deny`), no una ruta dentro de él.

**Estado de la barrera hoy: no aplica, porque no hay ningún servidor MCP instalado (`.mcp.json` no
existe).** El riesgo es una precondición dormida, no un incidente. Se traduce en una regla de
admisión explícita en la sección E: ningún servidor MCP que lea o escriba ficheros entra sin que se
añada y verifique por inyección (regla 25) su propia regla `deny` con el prefijo `mcp__`, antes de
activarlo — nunca dando por hecho que las reglas nativas ya lo cubren, porque documentalmente no lo
hacen.

Fuente: [Configure permissions — Claude Code Docs](https://code.claude.com/docs/en/permissions),
sección "MCP" y sección "Read and Edit", consultada 01/08/2026.

---

## D) CANDIDATOS CONDICIONALES

Ninguno entra hoy. Ambos con disparador concreto, escrito, y comprobable — no una intuición de que
"podría hacer falta más adelante".

### D1 — Navegador (Playwright MCP)

- **Candidato concreto:** `microsoft/playwright-mcp`, oficial, vivo (`pushed_at` 2026-07-25,
  `updated_at` 2026-08-01, 35.708 estrellas, verificado por la API de GitHub). Se descarta también
  `ChromeDevTools/chrome-devtools-mcp` (oficial, vivo, `pushed_at` 2026-07-31, 48.297 estrellas) como
  candidato para este disparador concreto: está pensado para depuración de rendimiento y red de
  aplicaciones web, no para extraer contenido de una página; Playwright encaja mejor con "leer una
  página renderizada por JavaScript".
- **Disparador, comprobable, no vago:** *si en la tarea 04.01.01 (comparar 3-4 brokers) la página de
  costes de alguno de los brokers candidatos resulta estar renderizada por JavaScript en el
  cliente y `WebFetch` no devuelve el contenido (contenido vacío, solo el esqueleto de la
  aplicación, o error de la herramienta), entonces se reconsidera un MCP de navegador para esa
  tarea concreta.* Es comprobable porque el fallo de `WebFetch` es un hecho observable, no una
  opinión.
- **Qué pasa mientras tanto:** nada se bloquea; 04.01.01 sigue `pendiente` por su propia dependencia
  (02.03.03, cierre de G1), y cuando llegue su turno se prueba primero con `WebFetch` sin más.
- **Coste si el disparador se cumple:** instalación vía `npx @playwright/mcp` o imagen Docker
  oficial, más la regla `deny`/`allow` con prefijo `mcp__playwright` en `.claude/settings.json`
  verificada según la sección anterior. No se estima el tiempo porque depende de qué falle.

### D2 — Broker (Kraken oficial, Alpaca oficial, IBKR)

- **Candidatos concretos evaluados:** Kraken tiene un MCP **oficial** integrado en su CLI
  (`krakenfx/kraken-cli`, `pushed_at` 2026-04-20, `updated_at` 2026-07-29, 677 estrellas), con
  ejecución de órdenes en vivo y también *paper trading*. Alpaca tiene un MCP **oficial**
  (`alpacahq/alpaca-mcp-server`, `pushed_at` 2026-07-31, 896 estrellas), con negociación de
  acciones, opciones y cripto. IBKR **no tiene MCP oficial**: solo implementaciones de comunidad
  (`ArjunDivecha/ibkr-mcp-server`, `pushed_at` 2025-07-23 — más de un año sin empujar — y otras tres
  fragmentadas), ninguna de la propia Interactive Brokers.
- **Por qué NO entran hoy, sin condición:** un MCP de broker es exactamente la categoría que la
  regla 23 de CLAUDE.md marca como irreversible desde el minuto uno — "dinero real, órdenes al
  broker" — sin excepción para cuentas demo, porque el propio texto de la regla no distingue demo
  de real. Hoy no hay broker elegido (04.01.01 `pendiente`), no hay cajones de datos partidos
  (04.01.03 `pendiente`), no hay bot (05.01.01 `pendiente`), y el guardia de parada dura del -30%
  (D-14) todavía no existe ni está verificado por inyección (regla 25). Añadir hoy una herramienta
  capaz de colocar órdenes —aunque sea en demo— antes de que exista ese guardia sería exactamente lo
  que la regla 26 prohíbe: un guardia que no bloquea por defecto.
- **Disparador, comprobable, no vago:** *el equipo NO adopta un MCP de broker en ningún momento sin
  que se cumplan, en este orden, las tres condiciones siguientes: (1) el broker ya está elegido en
  04.01.01; (2) el guardia de parada dura de 05.01.01 (D-14, -30% del capital inicial, aplicado por
  el bot de forma continua) está construido y verificado por inyección —regla 25— de forma
  INDEPENDIENTE de si las órdenes las coloca código propio o un MCP; (3) el CEO aprueba
  explícitamente en la puerta correspondiente (G3 o antes) sustituir código de ejecución propio por
  el MCP del broker, porque es un cambio de planteamiento, no una tarea que el equipo cierre solo.*
  Si las tres no se cumplen, no se reconsidera.
- **Qué pasa si no se usa:** nada se bloquea. El plan ya vigente en el WBS (05.01.01: "Bot en demo,
  solo y con guardias automáticos") ya asume código de ejecución propio, auditable y versionado, no
  un servidor de terceros cuyas salvaguardas internas este proyecto no puede verificar por
  inyección.

---

## E) REGLA DE ADMISIÓN DE MCP

> Un servidor MCP entra solo si desbloquea mecánicamente una tarea del WBS hoy bloqueada y esa
> tarea no se resuelve con una herramienta nativa en menos de 100 líneas propias (mismo umbral que
> 01.02.03). Si toca datos de mercado, solo puede entregar dato bruto — nunca OHLC ni indicador ya
> calculado (regla 14) — y el instrumento debe coincidir exacto con el fijado en 02.02.01 (L-007), o
> no entra. Si toca lo irreversible (dinero real, órdenes al broker), no entra nunca sin aprobación
> del CEO en una puerta (regla 23) y sin un guardia propio, independiente del servidor, verificado
> por inyección (regla 25). Antes de activarse, se escribe y se verifica por inyección su propia
> regla `mcp__<servidor>` en `.claude/settings.json`: las reglas `deny` de herramientas nativas
> (`Read`/`Edit`/`Write`/`Bash`) no protegen frente a MCP, porque viven en un espacio de nombres de
> permisos distinto — verificado documentalmente en este informe, no dar por hecho lo contrario.
