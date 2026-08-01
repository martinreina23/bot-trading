# 01.02.04, SEGUNDA PASADA — Familias no evaluadas: canales y avisos, bases analíticas locales, y lo que encaje

> Ordenada por el CEO el 01/08/2026 tras rechazar la conclusión «cero MCP» de `INFORME_MCP.md` **por
> poco buscada**, no por estar mal razonada. Este documento no reabre ni contradice los descartes ya
> aceptados de la primera pasada (servidores de referencia, GitHub, datos de mercado, broker,
> navegador): siguen en pie y no se repiten aquí. Cubre **exclusivamente** lo que la primera pasada
> no evaluó: (1) canales/avisos, (2) bases analíticas locales tipo DuckDB, (3) cualquier familia
> adicional que encaje con lo que este proyecto hace de verdad.
>
> **Nota de método, para que conste:** esta sesión no tiene herramienta `Bash`. Donde la ficha exige
> `curl -sS https://api.github.com/repos/<owner>/<repo>`, se ha usado `WebFetch` contra la misma URL
> de la API de GitHub, pidiendo explícitamente los campos `pushed_at`, `archived` y
> `stargazers_count` en crudo (no una paráfrasis de la página del repositorio). Es una verificación
> documental sobre la fuente primaria (la propia API), no una prueba ejecutada por esta sesión; un
> agente con `Bash` puede repetir cualquiera de las llamadas de abajo con `curl` y debe obtener el
> mismo JSON. Fecha de todas las comprobaciones: 01/08/2026.

---

## A) QUÉ ES UN CANAL

**Fuentes primarias, leídas completas:** [Push events into a running session with channels — Claude Code Docs](https://code.claude.com/docs/en/channels) y [Connect Claude Code to tools via MCP — Claude Code Docs](https://code.claude.com/docs/en/mcp), sección «Push messages with channels», ambas consultadas 01/08/2026.

**Definición literal de la documentación:** *"A channel is an MCP server that pushes events into your
running Claude Code session, so Claude can react to things that happen while you're not at the
terminal."* Técnicamente, un canal es un servidor MCP normal (vive en el mismo espacio de nombres
`mcp__<servidor>__<herramienta>` que cualquier otro) al que además se le declara la capacidad
`claude/channel`, y que se activa explícitamente con la bandera `--channels <plugin>` al arrancar
Claude Code. La página de MCP lo resume como una de las seis cosas que se pueden hacer con MCP:
*"React to external events: an MCP server can also act as a channel that pushes messages into your
session, so Claude reacts to Telegram messages, Discord chats, or webhook events while you're
away."*

**Qué PUEDE hacer, en lenguaje llano:**
- Meter un mensaje externo (un mensaje de Telegram, un DM de Discord, un webhook de CI, una alerta
  de monitorización) **dentro de una sesión de Claude Code que ya está abierta**, como si alguien lo
  hubiera escrito en el propio terminal.
- Ser de ida y vuelta: Claude puede leer el mensaje entrante y **responder por el mismo canal**
  llamando a la herramienta `reply` que el plugin expone — un puente de chat.
- Servir de receptor de webhooks genéricos si se construye un canal propio (`channels-reference`),
  no solo los tres oficiales.
- Los tres canales oficiales en vista previa de investigación (research preview) son **Telegram,
  Discord e iMessage**, cada uno instalado como *plugin* (`/plugin install telegram@claude-plugins-official`,
  etc.), con sus propias credenciales (token de bot) y un sistema de emparejamiento (`pair`) y lista
  blanca de remitentes.

**Qué NO PUEDE hacer, con la cita exacta que lo prueba:**
1. **No despierta una sesión que no existe.** *"Events only arrive while the session is open, so for
   an always-on setup you run Claude in a background process or persistent terminal."* Un canal no
   es un disparador que arranca Claude Code desde frío: hace falta que ya haya un proceso corriendo
   con `--channels <plugin>` para que algo le llegue. No sustituye a `cron` ni a las «arranques
   programados» de 03.01.03: los complementa, si acaso, una vez ese proceso persistente exista, que
   hoy no existe (03.01.03 está `pendiente`).
2. **Es vista previa de investigación (research preview), con dependencias que este entorno no
   cumple sin trabajo previo.** Requiere autenticación de Anthropic vía cuenta claude.ai o clave de
   API de Console; no funciona en Amazon Bedrock, Google Cloud Agent Platform ni Microsoft Foundry.
   En organizaciones Team/Enterprise, un administrador tiene que activar `channelsEnabled`
   explícitamente antes de que cualquier canal entregue nada. Requiere tener **Bun** instalado (los
   plugins oficiales son scripts de Bun), que hoy no está verificado en este entorno.
3. **iMessage requiere macOS** (*"It requires macOS and needs no bot token"*, leyendo directamente el
   fichero de Messages en `~/Library/Messages/chat.db`). Este proyecto corre en Linux/WSL2
   (`env`: `Linux 6.18.33.1-microsoft-standard-WSL2`), así que iMessage queda descartado de raíz, sin
   necesidad de evaluarlo más.
4. **La herramienta de respuesta pasa por el sistema de permisos normal, no lo esquiva.** *"If Claude
   hits a permission prompt while you're away from the terminal, the session pauses until you
   respond"* — salvo que el canal declare la capacidad de «relevo de permiso» (`relay permission
   prompts`, que reenvía el propio prompt al humano por el canal) o se use
   `--dangerously-skip-permissions`. Hoy `.claude/settings.json` no tiene ninguna regla `allow` con
   prefijo `mcp__`, así que la primera llamada a la herramienta `reply` de cualquier canal
   dispararía un prompt de permiso — exactamente lo que se quiere evitar en una tirada desatendida.
5. **No hay sintaxis de patrón de ruta ni garantía de que las reglas `deny` actuales lo cubran**, el
   mismo riesgo dormido que ya documentó `INFORME_MCP.md` para cualquier MCP, agravado aquí: un canal
   *empaquetado en un plugin* usa el patrón `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`
   (documentado en `code.claude.com/docs/en/mcp`, sección «Plugin MCP tool names»), un nombre más
   largo y más fácil de escribir mal en una regla `deny` que el `mcp__<servidor>__<herramienta>`
   simple ya señalado. No se puede escribir la regla exacta sin instalar el plugin y leer el nombre
   real de su herramienta primero — y regla 25 de CLAUDE.md exige verificarla por inyección antes de
   confiar en ella, no solo escribirla.

**Comparación oficial con otros mecanismos** (tabla «How channels compare» de la propia
documentación): un servidor MCP normal, *"Claude queries it during a task; nothing is pushed to the
session"* — es decir, el proyecto no tiene ningún MCP hoy y por eso nada le llega nunca por su
cuenta. Un canal invierte esa dirección, pero solo mientras hay sesión abierta. Nota lateral, fuera
del alcance de esta tarea pero visible al leer la documentación: existe además un mecanismo nativo
distinto, **Scheduled tasks** (`/docs/en/scheduled-tasks`, no es MCP), que «sondea con un temporizador
en vez de reaccionar a eventos empujados» — puede ser relevante para 03.01.03 el día que se diseñen
los arranques programados, pero no se evalúa aquí porque no es un canal ni un MCP y esta tarea no
tiene alcance para decidir sobre él.

---

## B) VEREDICTO

**Cero servidores MCP se proponen añadir, y cero quedan como candidatos condicionales**, en ninguna
de las tres familias nuevas evaluadas. Se comprobó actividad por la API de GitHub de **9 candidatos
concretos** (5 de la familia de avisos, 4 de bases analíticas) más los tres plugins de canal
oficiales (Telegram, Discord, iMessage) empaquetados en un solo repositorio. Ninguno pasa el criterio
de admisión vigente: *desbloquear mecánicamente una tarea del WBS hoy bloqueada, y no resolverse con
menos de 100 líneas propias*. En el caso de los avisos, ni siquiera hacen falta líneas propias: un
mecanismo **nativo de Claude Code, sin MCP y sin bash**, ya lo resuelve (ver sección C).

---

## C) PROPUESTOS

**Ninguno.** Lo que sí hay que dejar escrito, porque responde directamente a lo que pedía la ficha
(«di también si esto se resuelve mejor SIN MCP»):

### La necesidad nº 4 («vigilancia sin que el humano tenga que mirar») se resuelve con un hook nativo, no con 10 líneas de bash: con CERO

Comprobado por lectura completa de [Hooks reference — Claude Code Docs](https://code.claude.com/docs/en/hooks),
consultada 01/08/2026: además del tipo `"command"` (ejecuta un script y lee su stdout/exit code) que
ya usa este proyecto en `.githooks/`, Claude Code tiene un tipo de hook nativo `"http"` que **hace la
petición POST él mismo, sin ningún script intermedio**: *"HTTP hooks (`type: "http"`): send the
event's JSON input as an HTTP POST request to a URL."* Los campos son `url` (obligatorio), `headers`
(opcional, con interpolación de variables de entorno vía `allowedEnvVars`) — no hace falta ni un
binario ni un intérprete instalado, lo ejecuta el propio Claude Code.

Y la lista de eventos de hook (sección «Hook events» del mismo documento) incluye exactamente los que
la ficha nombraba y algunos más útiles todavía:

| Evento | Cuándo dispara | Sirve para |
|---|---|---|
| `Stop` | Cuando Claude termina de responder | Fin de turno — puede ser ruidoso si se dispara en cada turno de una tirada larga |
| `StopFailure` | Cuando el turno termina por un error de la API (matcher por tipo: `rate_limit`, `overloaded`, `authentication_failed`, `billing_error`, `server_error`, etc.) | Exactamente el caso de «algo se rompió mientras nadie miraba» — ya lo usa `INFORME_AWESOME.md` (propuesta P3) para escribir la incidencia en el informe de la tirada; aquí se propone la MISMA señal, además, para avisar al humano fuera de la sesión |
| `Notification`, matcher `idle_prompt` | Claude está inactivo/esperando | Sirve para detectar que la tirada se quedó parada sin nadie delante |
| `Notification`, matcher `permission_prompt` | Se necesita una decisión de permiso | Sirve para detectar que la tirada se bloqueó esperando una aprobación que nadie va a dar en un cron desatendido |
| `SessionEnd` | La sesión termina | Sirve para el resumen de «un día entero de trabajo desatendido» de 03.01.05 |

**Coste real de la alternativa nativa:** una entrada de 6-10 líneas de JSON en `.claude/settings.json`
(cero bash) si el servicio de destino acepta cualquier cuerpo como mensaje — es el caso de **ntfy**
(`POST https://ntfy.sh/<topic>` o un servidor propio; ntfy trata el cuerpo entero de la petición como
el texto del mensaje, sea cual sea su `Content-Type`) —, o un hook `"command"` de unas 3-6 líneas de
bash con `curl` cuando se necesite dar forma al mensaje (por ejemplo el formato JSON exacto
`{"content": "..."}` que exige un webhook entrante de Discord, o los parámetros `token`/`user`/
`message` de Pushover), porque el cuerpo de un hook `"http"` **no es configurable**: siempre es el
JSON de entrada del propio evento, tal cual, sin poder redactarlo. Cualquiera de las dos rutas es
menos código, menos dependencias y menos riesgo de permisos que instalar un MCP o un plugin de canal:
un hook no pasa por el sistema de permisos de herramientas (lo ejecuta el proyecto por configuración,
no lo «pide» el agente), así que no hace falta ninguna regla `allow` nueva ni ningún prefijo `mcp__`.

**Qué pasa si no se usa nada de esto:** nada se bloquea hoy — 03.01.03 (ejecución desatendida) y
03.01.05 (prueba real de un día) siguen `pendiente` por su propia dependencia, no por falta de un
servicio de avisos. Cuando les llegue el turno, el hook `http`/`command` de arriba es la
implementación recomendada por este informe; no requiere ficha nueva de MCP ni regla `mcp__` alguna.

---

## D) DESCARTADOS DE LAS FAMILIAS NUEVAS, UNO POR UNO

### Familia 1 — Canales y avisos

| Candidato | Actividad verificada (API de GitHub, 01/08/2026) | Motivo del descarte |
|---|---|---|
| **Canal Telegram** (`anthropics/claude-plugins-official`, plugin `telegram`) | Repo del plugin: `pushed_at` 2026-08-01, `archived` false, 32.932 estrellas — vivo, oficial | Arquitectura equivocada para la necesidad: es un puente de chat de doble vía que exige sesión persistente abierta con `--channels`, Bun instalado, emparejamiento manual y vista previa de investigación con posible bloqueo de organización. La necesidad declarada es una alerta de una vía (el sistema avisa al humano), que el hook nativo `http`/`command` resuelve con menos piezas y sin abrir el espacio de nombres `mcp__` |
| **Canal Discord** (mismo repo, plugin `discord`) | Igual que arriba | Mismo motivo exacto |
| **Canal iMessage** (mismo repo, plugin `imessage`) | Igual que arriba | Mismo motivo, más uno propio y suficiente por sí solo: requiere macOS; este proyecto corre en Linux/WSL2 |
| **ntfy-me-mcp** (`gitmotion/ntfy-me-mcp`) | `pushed_at` 2026-04-11, `archived` false, 69 estrellas — vivo, comunidad | No oficial (ntfy, el proyecto `binwiederhier/ntfy`, no publica MCP propio). Un hook `http` apuntando directo a `https://ntfy.sh/<topic>` hace lo mismo sin instalar ni mantener un servidor MCP |
| **ntfy-mcp-server** (`cyanheads/ntfy-mcp-server`) | `pushed_at` 2026-07-30, `archived` false, 19 estrellas — vivo, comunidad | Mismo motivo que el anterior |
| **pushover-mcp** (`AshikNesin/pushover-mcp`) | `pushed_at` 2025-03-16, `archived` false, 41 estrellas — **más de un año sin empujar** a fecha de esta auditoría | Doble motivo: desactualizado, y de nuevo sustituible por un hook `command` de pocas líneas con `curl` contra la API de Pushover |
| **mcp-pushover** (`pyang2045/mcp-pushover`) | `pushed_at` 2025-06-25, `archived` false, 2 estrellas — más de un año sin empujar, adopción mínima | Mismo motivo, con menos adopción todavía |
| **Webhook genérico** | No existe un candidato «oficial» o canónico equivalente a los de referencia de `modelcontextprotocol/servers` (ese repositorio no incluye ninguno de tipo webhook, confirmado ya en `INFORME_MCP.md`) | El propio hook `type: "http"` de Claude Code **ya es** un emisor de webhooks nativo; no hace falta un servidor intermedio para emitir uno |

### Familia 2 — Bases analíticas locales (DuckDB)

| Candidato | Actividad verificada (API de GitHub, 01/08/2026) | Motivo del descarte |
|---|---|---|
| **mcp-server-motherduck** (`motherduckdb/mcp-server-motherduck`) | `pushed_at` 2026-07-27, `archived` false, 506 estrellas — vivo, oficial (MotherDuck) | Ver razonamiento completo abajo: no desbloquea ninguna tarea hoy |
| **mcp-server-duckdb** (`ktanaka101/mcp-server-duckdb`) | `pushed_at` 2025-05-05, `archived` false, 177 estrellas — más de un año sin empujar | No oficial, desactualizado, mismo motivo de fondo que el anterior |
| **duckdb-mcp-server** (`mustafahasankhan/duckdb-mcp-server`) | `pushed_at` 2026-03-10, `archived` false, 17 estrellas — vivo, comunidad, adopción baja | Mismo motivo de fondo |
| **mcp-server-duckdb** (`boettiger-lab/mcp-server-duckdb`) | `pushed_at` 2026-01-04, `archived` false, 1 estrella, sin descripción | Mismo motivo de fondo, adopción mínima |

**Razonamiento de fondo, aplicado a los cuatro por igual — los dos usos que pedía la ficha, tratados
por separado:**

1. **¿Sirve para calcular cifras que entran en un informe?** No, y no es un matiz de DuckDB: es
   estructural. La regla 14 de CLAUDE.md exige que todo dato numérico se calcule sobre datos brutos
   mediante un artefacto que se pueda ejecutar y releer (L-001 de `00-direccion/LECCIONES.md`), y la
   práctica ya asentada en este proyecto es que ese artefacto es un script versionado en
   `03-motor/scripts/` (`precios_mercado.py`, `coste_relativo.py`, `correlaciones_mercado.py`,
   `arrastre_coste.py`, comprobados por `Glob` contra el disco el 01/08/2026) que el revisor
   re-ejecuta y recalcula de forma independiente (regla 16 del Equipo: quien produce las métricas no
   firma el veredicto). Una consulta SQL lanzada dentro de una sesión de chat —sea con `pandas` o con
   DuckDB, el motor es irrelevante aquí— no dispositivo por sí sola deja ese rastro ejecutable a
   menos que alguien la copie a un fichero `.py`/`.sql` versionado; en ese momento ya no hace falta el
   servidor MCP, porque el propio script puede importar `duckdb` como librería igual que hoy importa
   `pandas`, con `Bash(python3 *)` que ya está en `allow`. El MCP no añade nada a esta ruta: la
   quita, porque introduce un paso no versionado entre el dato y el número.
2. **¿Aporta para explorar?** Puede que sí en abstracto —DuckDB consulta CSV/Parquet más rápido y con
   menos memoria que cargarlos enteros en `pandas`—, pero **no desbloquea nada hoy**. Los artefactos
   actuales del proyecto son JSON pequeños (`atr_15m_1h_4h.json`, `correlaciones_8x8.json`,
   `coste_relativo_15m_1h_4h.json`, `arrastre_coste_anual.json`, confirmados por `Glob` en
   `04-resultados/`), y `pandas>=2.0` ya está en `requirements.txt` y en uso probado en los cuatro
   scripts de arriba. Aun contando el histórico bruto de 1 minuto de los 8 instrumentos durante 2 años
   completos (del orden de un millón de velas por instrumento en el peor caso, ocho instrumentos:
   cálculo aritmético directo, no una medida — `2 años × 365 días × 24 h × 60 min ≈ 1.051.200`
   velas/instrumento como cota superior, menos en forex por el cierre de fin de semana), sigue siendo
   un volumen que `pandas` maneja sin problema en una máquina normal. **No hay ninguna tarea del WBS
   hoy bloqueada por falta de un motor SQL**, y el criterio de admisión exige justo eso, no una
   posible comodidad futura. Inventar un disparador vago del tipo «si el histórico crece mucho» sería
   exactamente lo que la ficha original ya prohibió («un disparador vago no vale»): no se hace.

### Familia 3 — Lo que se le ocurra al investigador y encaje

Se repasaron, contra el patrón de trabajo real del proyecto (descargar, calcular, verificar por
inyección, registrar solo-añadir, decidir en una hora a la semana), dos candidatos que ya tenían
necesidad aparente y resultaron **ya resueltos sin MCP, con herramientas nativas verificadas contra
el disco**:

- **Extracción de contenido de páginas/PDF de brokers** (necesaria en 02.01.02): ya resuelta sin MCP.
  `01-investigacion/mercados/coste_operar.md` cita explícitamente los PDF oficiales «Costs and
  Charges» de Pepperstone y las páginas de precios de IC Markets como fuente, leídos con las
  herramientas nativas del proyecto (confirmado por `Grep` sobre el propio fichero, 01/08/2026); no
  hizo falta ningún MCP de PDF ni de scraping.
- **Generación del Excel de vista del CEO**: ya resuelta sin MCP, con la librería `openpyxl` (en
  `requirements.txt` y usada en `05-vista-ceo/generar_excel.py`, confirmado por `Grep`), tal como fija
  la propia regla 11 del WBS.

No se encontró ninguna familia de MCP nueva, distinta de canales/avisos y bases analíticas, que
desbloquee mecánicamente algo que estas herramientas ya en uso no cubran. **«Ninguna» es un resultado
válido**, igual que lo declaró la primera pasada.

---

## E) VEREDICTO SOBRE LA PRIMERA PASADA

**Directo:** el número —cero MCP— se sostiene después de cubrir las familias que faltaban. Pero la
forma en que estaba escrito, «CERO servidores MCP hoy» sin más matiz, **era prematura como
afirmación de cobertura**, y el CEO tuvo razón en rechazarla por eso, no por capricho. La primera
pasada evaluó exactamente los ocho grupos que su propia ficha enumeraba (referencia, GitHub, datos de
mercado, broker, navegador) y ninguno más; nunca miró canales ni bases analíticas locales porque no
estaban en su alcance escrito, y aun así presentó el resultado con el peso de un veredicto general
sobre «si merece la pena añadir servidores MCP a este proyecto» — el título de la propia tarea, más
amplio que lo que de hecho barrió. Un «cero» que no ha mirado una familia entera que da de lleno en
una necesidad declarada y sin cubrir del proyecto (la nº 4, vigilancia sin que el humano mire) no es
un cero verificado sobre esa necesidad: es un cero sobre lo que se buscó, y eso es exactamente la
distinción que la jerarquía de la prueba (regla 27 del WBS / regla 9 de CLAUDE.md, L-015 obliga a
citar el documento) exige no confundir.

Lo que esta segunda pasada aporta y la primera no tenía forma de tener, por estar fuera de su
alcance:
1. **Un mecanismo real, verificado contra la documentación oficial, que la primera pasada ni sabía
   que existía**: los canales. Y una razón concreta, no genérica, de por qué no aplican aquí (van en
   la dirección de entrada, no de salida; exigen sesión persistente que el proyecto no tiene
   construida; son vista previa de investigación con dependencias — Bun, autenticación, posible
   bloqueo de organización — que no están comprobadas en este entorno).
2. **Un hallazgo que ni siquiera estaba en el radar de MCP**: el hook nativo `type: "http"` de Claude
   Code resuelve la necesidad de aviso saliente con menos código todavía que los «10 líneas de bash»
   que la propia ficha proponía como vara de medir — con JSON de configuración y cero MCP.
3. **Un descarte razonado y no genérico de DuckDB**, distinguiendo explícitamente explorar de
   calcular-para-informe, en vez de meterlo en el mismo saco que TradingView o QuantConnect por
   asociación.

En una frase: la primera pasada no mintió en su número, pero lo entregó con más seguridad de la que
su propio barrido justificaba. Esta segunda pasada, con el barrido ampliado, confirma el mismo número
por un camino distinto y más completo — y de paso encuentra la pieza que de verdad hacía falta para
03.01.03, que no es un MCP.
