# 01.02.03 — SEGUNDA PASADA: cobertura completa del catálogo `awesome-claude-code`

> Ordenada por el CEO el 01/08/2026 tras rechazar la conclusión «cero piezas» de la primera pasada
> (`01-investigacion/ecosistema/INFORME_AWESOME.md`) por poco buscada. Este informe NO contradice
> la primera pasada por contradecir: la completa. Sus descartes ya verificados no se repiten aquí
> salvo que aporten un dato nuevo.
>
> Agente: `investigador` (Sonnet 5). No hizo falta respaldo.

---

## A) COBERTURA

**Herramientas disponibles en esta sesión:** `Read`, `Write`, `WebSearch`, `WebFetch`, `Grep`, `Glob`.
**No hay `Bash`.** No puedo ejecutar `curl` ni contar líneas de un fichero remoto de forma
determinista. Todo lo que sigue pasa por `WebFetch`, que —tal como avisa la orden de esta tarea—
procesa el contenido con un modelo pequeño antes de devolvérmelo. Lo dejo dicho con la misma
crudeza que pide el CEO: **este es exactamente el punto débil que hundió a la primera pasada**, y
lo he tratado como tal, no como un detalle.

### Cuántas entradas tiene el catálogo

El catálogo vive en dos formatos que deberían coincidir: el `README.md` generado (prosa, por
categoría) y `THE_RESOURCES_TABLE_NEW.csv` (los mismos datos en tabla, con columna `ID` única por
fila — es la fuente que usé para contar, por ser mecánica).

Pedí el recuento total del CSV **cinco veces, de cinco formas distintas**, y obtuve **cinco
números distintos: 101, 139, 143, 145 (por suma de categorías) y 137 (por enumeración fila a
fila, columna `ID` + columna `Categoría`, forzando al modelo a listar en vez de resumir)**. Esto
no es ruido menor: es la prueba de que pedir «cuántas hay» a un resumidor no es fiable, ni siquiera
en un segundo intento cuidadoso. El número en el que más confío es **137**, porque es el único que
obtuve por enumeración exhaustiva (no un conteo declarado) y porque, al verificarlo por categoría
—pidiendo por separado todas las filas de «Research & Scientific Inquiry» y contando manualmente el
resultado devuelto—, coincidió dígito a dígito dos veces seguidas (2 filas, confirmado por consulta
directa además de por la enumeración general). **No puedo certificar 137 con la misma fuerza que un
`grep -c` local; lo declaro como la mejor estimación disponible con la herramienta que tengo, no
como una medida.** Si el proyecto necesita el número exacto, la forma correcta es descargar el CSV
con un script (tarea de `constructor-datos`, no de este agente) y contar líneas de verdad.

El catálogo declara **18 categorías de primer nivel** en su tabla de contenidos (confirmado leyendo
el `README.md` crudo): Start Here, From Anthropic, Documentation Knowledge & Learning, Research &
Scientific Inquiry, Providers/Runtime & Integration Infrastructure, Remote Control/Notifications &
Voice I/O, Alternative Clients, Status Lines, Design & UI/UX, Writing & Prose Quality, Creative
Media, Infrastructure & DevOps, Security, Agent Orchestration, Skills, Memory & Context
Persistence, Observability & Monitoring, Linting. Esto coincide con lo que dice la orden de esta
tarea sobre la primera pasada («vio los 18 nombres»).

**Repositorio vivo, comprobado por la API de GitHub el 01/08/2026:** `pushed_at`:
`2026-08-01T09:40:09Z`, `archived: false`, 51.433 estrellas. Mismo dato que ya tenía la primera
pasada, reverificado.

### Cuántas evalué

De las 18 categorías, **evalué entrada por entrada (leí nombre, enlace, autor y descripción
completa) las 6 que el CEO marcó como huecos de la primera pasada**, más una séptima por iniciativa
propia:

| Categoría | Entradas evaluadas | Método |
|---|---|---|
| Research & Scientific Inquiry | 2 de 2 | Fila CSV completa, doble verificación |
| Remote Control, Notifications & Voice I/O | 8 confirmadas (una consulta de conteo dio 9; no resuelto, ver nota) | Fila CSV completa |
| Documentation, Knowledge & Learning | 11 de una categoría que ronda 13 (2 filas con `ID` ambiguo que no pude atribuir con confianza a un nombre — no las invento, quedan fuera) | Fila CSV completa |
| Infrastructure & DevOps | 2 de 2 | Fila CSV completa |
| Linting | 6 de 6 | Fila CSV completa |
| Observability & Monitoring (las 3 subcategorías: Session Monitors, Usage & Cost, Observability) | 20 de ~20 | Fila CSV completa, por subcategoría |
| Providers, Runtime & Integration Infrastructure *(no pedida, la añadí porque «cost/routing» tocaba la necesidad 4)* | 7 de 7 | Fila CSV completa |

**Total leído entrada por entrada en esta pasada: 56.** Sumado a lo que la primera pasada ya
nombró explícitamente (25 piezas con nombre propio, más el bloque de Memoria con 9 nombradas, más 3
de Status Lines/Session Monitors) da una cobertura combinada de **más de 80 entradas con nombre
sobre las ~137 del catálogo**, y las categorías que ninguna de las dos pasadas abrió entrada por
entrada (Alternative Clients 7, Status Lines 3, Design & UI/UX 5, Writing & Prose Quality 2,
Creative Media 5, Agent Orchestration 4, Skills 4, Security ~16-17) siguen sin encaje declarado por
tema, no por pereza: ninguna de ellas —por su propio nombre de categoría— toca las 5 necesidades del
proyecto, y ya lo dijo la primera pasada. No las reabro porque el CEO no las señaló como el fallo, y
reabrirlas sin motivo sería el mismo vicio en sentido contrario (barrer por barrer).

**Nota de discrepancia sin resolver, dicha sin adornos:** una consulta a la categoría «Remote
Control» dio 8 filas completas y otra, pidiendo solo el conteo, dio «9». No encontré la novena fila
al pedirla de nuevo. Lo declaro como diferencia sin cerrar en vez de fingir que cuadra.

---

## B) LO QUE SÍ SIRVE

**Cero piezas.** No es el mismo cero que la primera pasada: aquí sí abrí las categorías, sí evalué
la vigilancia con la distinción correcta (empuja vs. muestra), y el cero sale de evaluar caso por
caso, no de una regla general descartada de un plumazo. Documento los dos candidatos que más
cerca estuvieron, porque el criterio de esta tarea exige explicarlo, no solo declararlo.

### Candidato analizado en profundidad 1 — `ai-agent-notifier` (DevinoSolutions)

- **Enlace:** https://github.com/DevinoSolutions/ai-agent-notifier
- **Última actividad verificada (API de GitHub, 01/08/2026):** `pushed_at: 2026-07-31T07:18:48Z`,
  `archived: false`, 18 estrellas, licencia AGPL-3.0, lenguaje JavaScript.
- **Qué hace:** dispara un aviso de escritorio (toast) y un *push* gratuito al móvil (vía `ntfy`)
  en el momento en que Claude Code termina una tarea o necesita permiso. Cero dependencias
  declaradas, CI que prueba el envío real (no mocks).
- **Qué necesidad ataca:** la 4 — es exactamente lo que la primera pasada descartó sin comprobar
  («toda vigilancia exige un humano delante»), y aquí la afirmación es falsa para este caso
  concreto: un *push* al móvil va a buscar al humano, no le pide que mire un panel.
- **Qué instala y qué permisos pide:** CLI de Node.js corriendo como demonio; permiso de red
  saliente para hacer POST a `ntfy.sh` (o un servidor `ntfy` propio) y acceso a la API de
  notificaciones del sistema operativo. No pide credenciales de broker, no toca datos del proyecto,
  no depende de ningún servicio de pago (`ntfy.sh` es gratis en su nivel público).
- **Por qué NO lo propongo, con el motivo exacto que pide la tarea:** el hueco real que hoy tiene
  este proyecto no es «avisar», es **saber cuánto se ha gastado**. Comprobé la documentación
  oficial de hooks de Claude Code (`code.claude.com/docs/en/hooks`) y **ningún evento de hook trae
  coste ni tokens en su JSON de entrada** — ni `Notification`, ni `Stop`, ni `SessionEnd`. Lo único
  que traen es `transcript_path`, la ruta a un JSONL que hay que parsear y multiplicar por la
  tabla de precios que el propio WBS ya tiene escrita (sección «Equipo de agentes» de
  `00-direccion/WBS.md`, línea de precios oficiales). Ese cálculo es el problema de verdad, y
  `ai-agent-notifier` no lo resuelve: solo envía el mensaje una vez que otro código ya sabe qué
  decir. Y esa parte —el envío— es la trivial: `ntfy` es una petición HTTP `POST` con el mensaje
  como cuerpo, documentada públicamente como una llamada de una línea (no lo he ejecutado yo mismo,
  así que lo marco «no verificado por ejecución», pero está documentado como HTTP simple, no como
  protocolo propio). **Respuesta directa a la pregunta obligatoria: ¿se hace igual con menos de 100
  líneas propias? Sí.** Un hook `Notification` o `Stop` que compare un umbral contra el gasto
  calculado y haga un `curl -d "mensaje" ntfy.sh/tema` cuando se supera cabe holgadamente por
  debajo de 100 líneas, sin instalar Node ni una dependencia AGPL-3.0 (licencia que además conviene
  mirar dos veces si algún día el proyecto empaqueta algo para terceros). No pasa el criterio de
  admisión.

### Candidato analizado en profundidad 2 — la clase «calculadoras de coste» de Observability & Monitoring → Usage & Cost

Ejemplos con actividad verificada por la API de GitHub el 01/08/2026: `cc-probeline`
(`labzink/cc-probeline`, `pushed_at: 2026-06-18`, Go, MIT, 10 estrellas) y `goccc`
(`backstabslash/goccc`, `pushed_at: 2026-07-24`, Go, MIT, 31 estrellas). Hay otras ocho en la misma
subcategoría (Claumon, ccvitals, toktrack, claude-code-status-bar, cc-costline, CCDash, Pacer,
AgentWatch), todas vivas según sus filas del CSV.

- **Qué hacen:** la parte difícil de verdad — parsear el JSONL de transcripción de Claude Code y
  aplicar el precio correcto por modelo, incluida la lectura/escritura de caché, que tiene tarifa
  distinta al token normal.
- **Por qué se quedan cerca:** si este proyecto tuviera que escribir esa lógica de cero, ahí sí hay
  riesgo real de superar 100 líneas y de cometer un error de los que este proyecto ya ha pagado caro
  (el divisor de pip mal puesto en 02.02.02, el ATR del oro en gb2). Reutilizar un cálculo ya
  probado tendría sentido.
- **Por qué NO las propongo:** las nueve están escritas para renderizarse **dentro** de la línea de
  estado de Claude Code en cada turno — es su modelo de ejecución, no una biblioteca que se pueda
  importar y llamar desde un hook con un umbral. Adoptar una de ellas no sería «integrar una pieza»,
  sería instalar una aplicación completa (binario Go, npm, o Swift según el caso) y luego
  desmontarla para robarle la fórmula de precio, que es justo el tipo de dependencia frágil que el
  criterio de esta tarea quiere evitar («no se puede escribir en menos de 100 líneas» es lo
  contrario de «hay que operar sobre el binario de otro para sacarle una fórmula»). Además, la
  fórmula de precio de Anthropic (tokens de entrada, salida, escritura de caché, lectura de caché)
  es pública y ya está en parte en el propio WBS de este proyecto (precios por modelo). Escribirla
  una vez, para los 4 modelos exactos que usa este proyecto, es un problema más pequeño que el que
  resuelven estas herramientas (que cubren N modelos y N proveedores). **No pasa el criterio de
  admisión.**

**Conclusión de la sección B, dicha sin rodeo:** el catálogo no tiene ninguna pieza en el formato
que este proyecto necesitaría (una función pequeña, sin proceso propio, invocable desde un hook).
Tiene aplicaciones completas para mirar (Usage & Cost, todas dashboards/statuslines) y aplicaciones
completas para avisar de eventos genéricos de sesión (Remote Control), pero ninguna hace las dos
cosas que hacen falta juntas: calcular gasto de ESTE proyecto y avisar sin que se mire un panel.

---

## C) DESCARTADAS de las categorías nuevas

### Research & Scientific Inquiry (2 de 2 evaluadas)

| Pieza | Última actividad (API GitHub, 01/08) | Motivo del descarte |
|---|---|---|
| `WenyuChiou/ai-research-skills` | `pushed_at 2026-07-16`, viva, 182 estrellas, MIT | 15 habilidades para el ciclo de un **paper académico** (revisión de literatura → diseño → redacción → respuesta a revisores). Este proyecto no publica papers; su «investigación» es barrido de hipótesis de trading con fuentes verificables, un problema distinto |
| `pedrohcgs/claude-code-my-workflow` | `pushed_at 2026-06-10`, viva, 1.439 estrellas, MIT | Plantilla para académicos en LaTeX/Beamer + R con revisión multi-agente y QA adversarial. La idea de fondo (revisión adversarial, nadie se valida a sí mismo) **ya está construida en este proyecto** con `crítico-código` y `validador`; la plantilla trae una pila técnica (LaTeX, R) que este proyecto no usa (es Python) |

### Remote Control, Notifications & Voice I/O (8 de las evaluadas, aparte de `ai-agent-notifier` ya tratado arriba)

| Pieza | Última actividad | Motivo del descarte |
|---|---|---|
| `anneschuth/claude-threads` | viva, sin verificar por API (fuera de foco: colaboración en equipo) | Pensada para que un EQUIPO vea una sesión en Slack/Mattermost. Aquí hay un humano, no un equipo; añade infraestructura (bot de Slack) sin necesidad detrás |
| `Imolatte/tg-claude` | `pushed_at 2026-04-27`, el repo **cambió de nombre** a `claude-cli-telegram` (comprobado por API: el catálogo enlaza al nombre viejo, GitHub redirige, no está muerto pero el enlace del catálogo ya no es el canónico) | Control remoto vía Telegram para aprobar acciones desde el móvil. Resuelve un problema de otro tipo de proyecto (aprobar comandos peligrosos sobre la marcha); aquí los permisos son amplios por diseño (regla 9 del WBS) y lo irreversible ya lleva barrera propia, no telegram |
| `vimalk78/dictate` | viva | Dictado por voz. No hay necesidad de voz en este proyecto |
| `sorkila/lockpaw` | viva | Bloquea la pantalla mientras el agente trabaja. Resuelve privacidad visual, no una de las 5 necesidades |
| `Rich627/whatsapp-claude-plugin` | viva | Canal de WhatsApp para controlar Claude Code. Mismo motivo que Telegram: control remoto de acciones, no vigilancia de gasto |
| `mbailey/voicemode` | catálogo la marca `Active: FALSE` (dato del propio CSV, no reverificado por API por límite de tiempo) | Conversación de voz. No aplica |
| `marcindulak/stt-mcp-server-linux` | catálogo la marca `Active: FALSE` (mismo aviso) | Voz a texto local. No aplica |

### Documentation, Knowledge & Learning (11 de ~13 evaluadas)

Ninguna desbloquea una tarea del WBS hoy parada. Agrupo por motivo en vez de repetirlo 11 veces:

- **Herramientas para vaults de Obsidian** (`ngmeyer/librarian-mcp`, `iurykrieger/claude-bedrock`):
  este proyecto guarda su memoria en `DECISIONES.md`/`LECCIONES.md`/`registro-pruebas.md`, texto
  plano en git, no un vault de Obsidian. Mismo motivo que ya tumbó a toda la categoría Memoria en la
  primera pasada.
- **Generadores de documentación visual** (`HeyRenan/showreel` — capturas y GIFs anotados;
  `roomi-fields/notebooklm-mcp`, viva `pushed_at 2026-07-30`, 139 estrellas — controla Google
  NotebookLM): este proyecto entrega números y tablas, no material de marketing ni audio generado.
- **Herramientas de código/monorepo** (`Barnett-Studios/cxpak`, viva `pushed_at 2026-07-28`, 22
  estrellas — grafo de dependencias para 43 lenguajes): este proyecto es un puñado de scripts
  Python, no un monorepo poliglota con ese problema.
- **Cursos y tutores** (`TakaGoto/rag-learning-academy` sobre RAG, `Li-Evan/Bloom` tutor de
  aprendizaje espaciado): no hay nada que enseñar aquí sobre esos temas; el proyecto no construye
  RAG.
- **Guías de plataforma** (`ferrumclaudepilgrim/claude-code-android` para correr Claude Code en
  Android): este proyecto corre en Linux/WSL2 según el entorno declarado, no en Android.
- **Revisión humana de documentos** (`oubakiou/mdxg-redline`, herramienta de comentarios en
  navegador sobre documentación generada por IA): es revisión HUMANO↔documento, y la necesidad 5 de
  este proyecto es AGENTE↔AGENTE (que nadie se valide a sí mismo); no es el mismo problema.
- **Meta-análisis** (`tjboudreaux/cc-thinking-skills`, colección de marcos de pensamiento;
  `VILA-Lab/Dive-into-Claude-Code`, análisis académico del propio Claude Code): interesantes de
  leer, no desbloquean ninguna tarea.

### Infrastructure & DevOps (2 de 2)

| Pieza | Última actividad (API, 01/08) | Motivo del descarte |
|---|---|---|
| `antonbabenko/terraform-skill` | viva, sin verificar por API (descarte por tema, no por vida) | Terraform/OpenTofu para AWS/Azure/GCP. Este proyecto no tiene infraestructura cloud que provisionar; corre en una máquina |
| `s3onghyun/otelcol-doctor` | `pushed_at 2026-07-21`, viva, 8 estrellas, Apache-2.0 | Escribe y valida configuraciones del **Collector** de OpenTelemetry. Solo tendría sentido si el proyecto decidiera exportar métricas por OTel para vigilar gasto (mencionado como posibilidad en la primera pasada), y eso sería montar un Collector nuevo para un problema que un script de 100 líneas ya resuelve sin infraestructura nueva. Se queda en el bolsillo por si el proyecto cambia de escala, no hoy |

### Linting (6 de 6)

Los seis viven y ninguno desbloquea una tarea hoy parada: el problema que resolverían mejor
—que `CLAUDE.md` y `00-direccion/WBS.md` tuvieran dos listas de «29 reglas» con contenido
distinto bajo el mismo número, hallazgo ya registrado en la ficha de la tarea 03.01.13 del WBS—
el propio proyecto ya decidió resolverlo por la regla 28 de `CLAUDE.md` (una sola fuente de verdad,
la otra se borra), no por vigilancia continua de sincronía. Un linter de sincronía sería una
solución permanente para un problema que se va a cerrar de una vez.

| Pieza | Última actividad (API, 01/08) | Motivo |
|---|---|---|
| `agent-sh/agnix` | `pushed_at 2026-07-31`, viva, 373 estrellas, Apache-2.0 | Valida sintaxis/estructura de `CLAUDE.md`, `SKILL.md`, hooks y config MCP. No detecta contradicción de SIGNIFICADO entre dos ficheros (que es lo que pasó con las «29 reglas»): es un linter estructural, no semántico |
| `mennanov/blockwatch` | `pushed_at 2026-08-01`, viva, 29 estrellas, MIT | Mantiene código/docs/config sincronizados por marcadores manuales. Resuelve el mismo problema que 03.01.13 ya va a cerrar con «una sola fuente», no con sincronía perpetua |
| `ctxlint/Ctxlint` | `pushed_at 2026-04-13`, viva, 10 estrellas | Detecta referencias muertas, comandos muertos y secretos en ficheros de contexto de IA. Este proyecto no tiene secretos (`git remote -v` vacío, ya verificado en 01.02.04) |
| `Zandereins/schliff` | viva, sin verificar por API (fuera de foco) | Puntuador de calidad de ficheros de instrucciones. No bloquea nada, es una nota informativa |
| `Taiizor/agents-md-cookbook` | viva | Kit para el formato `AGENTS.md`. Este proyecto usa `CLAUDE.md`, no `AGENTS.md` |
| `wei18/Upkeep` | viva | Mismo motivo que BlockWatch: detector de deriva docs/código, redundante con la solución de fuente única ya decidida |

### Observability & Monitoring (20 de ~20: 10 en Usage & Cost, 7 en Session Monitors, 3 en Observability)

Con la distinción correcta esta vez (la que la primera pasada no hizo): **las tres subcategorías
son, sin excepción, cosas que se MUESTRAN** — estadísticas de línea de estado, apps de barra de
menú, paneles web en tiempo real. Ninguna, tras leer su descripción completa, envía nada hacia
fuera (webhook, push, correo, Slack) cuando se cruza un umbral; todas exigen que alguien las mire.
Esto confirma, con evidencia y no con una regla general, que el hueco de vigilancia de gasto sigue
abierto — y que la pieza que sí empuja avisos (`ai-agent-notifier`) vive en una categoría distinta
(Remote Control), tal como advertía la orden de esta tarea. Nombres completos, con su subcategoría,
por si hace falta revisarlos otro día: Usage & Cost — Claumon, ccvitals, toktrack, cc-probeline,
claude-code-status-bar, cc-costline, CCDash, Pacer, AgentWatch, goccc. Session Monitors — Claude
Code Agent Monitor, c9watch, claude-status-bar, Claude Status, claude-control, cctop, so-agentbar.
Observability — Multi-Agent Observability, Claude Code Observability Stack, agents-observe. Todas
vivas según su fila del CSV (fechas de «Last Checked» entre el 29/06 y el 19/07/2026); no verifiqué
las 20 una por una contra la API de GitHub por límite de tiempo de esta tirada — lo declaro en vez
de fingir 20 comprobaciones que no hice.

### Providers, Runtime & Integration Infrastructure (7 de 7 — categoría añadida por iniciativa propia, no estaba en la lista del CEO)

La abrí porque «coste» y «enrutado» sonaban a la necesidad 4. Ninguna encaja:

| Pieza | Motivo del descarte |
|---|---|
| `ypollak2/llm-router` | Enruta cada prompt al modelo más barato capaz de resolverlo. **Choca de frente con el diseño ya fijado del proyecto**: cada agente tiene un modelo asignado por su papel (`validador` en Fable 5 precisamente por su forma de juzgar, no por precio) — regla 29 de `CLAUDE.md` («cada agente lleva el identificador exacto de su modelo, nunca un alias»). Un router que reasigna modelos automáticamente rompe esa regla por diseño |
| `openweb-org/openweb`, `EndeavorYen/chrome-cdp-ex`, `zyx77550/sparda`, `SFKislev/Flue`, `aza-ali/turbowebfetch` | Todas dan acceso a navegador/apps de escritorio/APIs web con autenticación real. Este proyecto no automatiza sitios web ni apps de escritorio; su único uso de navegador es `WebFetch` puntual sobre páginas de costes de brokers, ya cubierto y con un condicional propio en `INFORME_MCP.md` (tarea 01.02.04) |
| `congmnguyen/claude-code-wsl2-setup` | Parches de comodidad para WSL2 (portapapeles, notificaciones nativas de Windows). Podría ser útil como referencia de configuración local, pero no desbloquea ninguna tarea del WBS: es ajuste de puesto de trabajo, no del proyecto |

---

## D) VEREDICTO SOBRE LA PRIMERA PASADA

**Su «cero piezas» se sostiene, pero por motivos distintos y con cobertura real esta vez. No era un
cero cómodo del todo: acertó en el resultado y falló en el camino.** Dicho sin diplomacia:

1. **El fallo de razonamiento que el CEO señaló es real y esta pasada lo confirma como fallo.** La
   frase «toda vigilancia exige un humano delante» era falsa: `ai-agent-notifier` y al menos otras
   tres piezas de Remote Control (Telegram, WhatsApp, Claude Threads) empujan avisos activamente.
   La primera pasada nunca las vio porque nunca abrió esa categoría — no es que las viera y las
   descartara mal, es que no llegó a mirarlas. Eso es exactamente «poco buscada».
2. **Pero, tras mirarlas con la distinción correcta (empuja vs. muestra), ninguna pasa el criterio
   de admisión** que el propio proyecto ya tiene escrito («desbloquea mecánicamente una tarea hoy
   parada Y no se puede escribir en menos de 100 líneas propias»). El motivo no es que la
   vigilancia sea innecesaria —es la necesidad 4, real y sin cubrir, tal como dice la orden de esta
   tarea— sino que **la parte difícil (calcular el gasto de este proyecto en concreto) no está en
   ningún sitio del catálogo en forma reutilizable, y la parte fácil (empujar un aviso) es
   trivialmente pequeña.** Ninguna pieza hace ambas cosas juntas, que es lo que hacía falta.
3. **Las categorías Documentation, Infrastructure & DevOps y Linting no aportan nada nuevo**, y esta
   vez lo digo tras leerlas entrada por entrada, no por generalizar desde el nombre de la categoría.
4. **Research & Scientific Inquiry, la categoría que más prometía por nombre, tampoco aporta nada**:
   las dos entradas son para investigación ACADÉMICA (papers, LaTeX, R), un problema de forma
   distinta al de este proyecto (backtesting cuantitativo, Python, costes verificables).

**Conclusión final: sigue siendo cero, pero ahora es un cero probado.** La diferencia con la primera
pasada no está en el número — está en que esta vez el número viene de leer 56 entradas nuevas
(más las ~80 que ya sumaban ambas pasadas juntas) en vez de generalizar desde 18 nombres de
categoría, y en que el hallazgo sobre notificaciones queda documentado con su motivo de descarte
explícito en vez de con una frase que no se sostenía. Si en algún momento el proyecto decide que
vigilar el gasto merece más que un script de 100 líneas propio con un hook y una llamada a `ntfy`,
la puerta que hay que abrir no es el catálogo: es escribir ese script, tarea de
`constructor-motor`, no de este informe.

---

## Nota metodológica final, para quien retome esta tarea

La causa raíz del problema de conteo de la sección A no es este catálogo: es que `WebFetch` en este
entorno no da acceso a texto crudo sin pasar por un modelo resumidor, y ese modelo pierde cuenta en
ficheros largos. Si una tarea futura necesita un número exacto de un fichero remoto grande, la forma
correcta es que `constructor-datos` lo descargue con script (regla 27 de `CLAUDE.md`) y se cuente
con herramientas de texto reales, no que `investigador` lo intente por `WebFetch`. Lo dejo escrito
para no repetir el mismo tropiezo una tercera vez.
