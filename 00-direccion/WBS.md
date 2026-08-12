# WBS — Bot de Trading Algorítmico (v0.9)

> Fuente de verdad para agentes. El Excel (WBS_Bot_Trading_v0.9.xlsx) es la vista del CEO y se genera de este archivo, nunca al revés.

## Reglas (sin ambigüedad posible)

La lista normativa del proyecto vive en `CLAUDE.md`, sección «## Las 29 reglas». Toda cita se
escribe «regla N de CLAUDE.md», nunca «regla N» a secas. La lista de 29 reglas que ocupaba
esta sección quedó DEROGADA el 01/08/2026 por decisión del CEO (D-16 en
`00-direccion/DECISIONES.md`; tarea 03.01.13; origen L-015). Aquí no hay texto de regla
propio y no se vuelve a poner ninguno. El texto derogado y su tabla de equivalencias quedan
en el historial de git de este fichero.

## Estados y cadencia de este WBS

- **Estados de una tarea:** `pendiente | en_curso | hecha | bloqueada`. La celda ESTADO
  declara uno solo y en negrita. Es el vocabulario que leen `05-vista-ceo/generar_excel.py` y
  `05-vista-ceo/verificar_excel.py` (símbolo `ESTADOS`).
- **Cadencia de entregables:** este WBS en texto se actualiza SIEMPRE que cambie algo. El
  Excel de vista del CEO se regenera para la revisión de los lunes y para las puertas.
- **Índice y expedientes (12/08/2026).** Este fichero es el **índice**: dice qué tareas hay,
  en qué estado están y de qué dependen. La **historia** de cada tarea —quién rechazó qué, en
  qué ronda y por qué— vive en `00-direccion/expedientes/NN.NN.NN.md`. El 12/08/2026 se
  movieron ahí, **íntegras y sin resumir**, las 25 celdas ESTADO que pasaban de 1.200
  caracteres: 111.494 caracteres que todo agente leía entero para averiguar una sola cosa,
  qué toca ahora. **No se borró nada.**
  - **Esto NO rompe la regla 28 de CLAUDE.md** (una sola fuente de verdad por tema): el
    índice sigue siendo la única fuente del **estado**, y cada expediente la única fuente de
    su **historia**. Son temas distintos.
  - Los expedientes se comportan como los registros de solo-añadir: se corrigen añadiendo.
  - Quien necesite la historia de una tarea abre su expediente. **Quien solo necesite saber
    qué toca, no tiene que abrirlo.** Ese es todo el objetivo.
  - `05-vista-ceo/generar_excel.py` y `05-vista-ceo/verificar_excel.py` los leen (símbolo
    `expediente_de` en ambos). El verificador **bloquea** si una celda apunta a un expediente
    que no existe o al de otra tarea.

> No son reglas de conducta —esas están en `CLAUDE.md`—, sino el vocabulario de operación de
> este fichero. Vienen de las antiguas reglas 29 y 11 de la lista derogada, que no tienen
> equivalente en `CLAUDE.md`. La antigua regla 26 del WBS no se rescata aquí: su contenido
> vive en L-010 de `00-direccion/LECCIONES.md`.

- **Cómo se cuenta una fila de tarea (métrica de L-027 de `00-direccion/LECCIONES.md`).** No se cuenta a ojo ni por columnas: se ejecuta. Una fila de tarea correcta da **7** al partirla por la barra vertical — `awk -F'|' '{print NF}'` devuelve 7, y `split('|')` en Python devuelve 7 elementos, que son **5 columnas más los dos campos vacíos de los bordes**. **Esos dos vacíos cuentan a propósito:** son lo que delata una fila fusionada con la de al lado o partida en dos, que es el incidente del que nació L-027. Quien lea «5 columnas» y quien lea «7 campos» está diciendo lo mismo; **la cifra normativa es 7 y la produce el comando, no la vista.**

## Plantilla de ficha de decisión (obligatoria)

```
D[n] — [Qué se decide, una línea]
A) [opción]   B) [opción]   C) [opción]
RECOMENDADA: [letra] — [motivo en una línea]
SI ELIGES OTRA: [consecuencia de cada una, una línea]
BLOQUEA: [qué tareas no pueden avanzar hasta que respondas]
RESPUESTA: [una letra]
```

## Equipo de agentes (modelo por rol)

| Agente | Qué hace | Qué NO puede hacer | Modelo | Respaldo |
|---|---|---|---|---|
| Orquestador | Reparte tareas por código, cierra contra criterio de hecho, escala excepciones al CEO | Construir; validar su propio reparto | Opus 5 | Sonnet 5 |
| Investigador | Barre fuentes (papers, libros, foros, GitHub, X); fichas de hipótesis | Elegir sus propias fichas; tocar código o datos | Sonnet 5 | Haiku 4.5 |
| Constructor de datos | Históricos, limpieza, los 3 cajones, costes reales | Abrir el cajón reservado (OOS) | Sonnet 5 | Haiku 4.5 |
| Constructor de motor/bot | Backtester, bot, ejecución desatendida | Validar sus backtests; tocar el cajón reservado | Sonnet 5 | Opus 5 tras 2 atascos |
| Crítico de código | Revisa código ajeno; analiza gb2 (01.02.01) | Revisar código propio | Sonnet 5 (Opus 5 en código que toca dinero real) | Sonnet 5 |
| Validador de estrategias | Filtro de sentido, prueba OOS, Monte Carlo, veredictos pasa/no pasa | Construir estrategias; suavizar veredictos | **Fable 5** | Opus 5 |
| Arquitecto (puntual) | Diseña el motor al arrancar Fase 03; revisa el planteamiento si el bucle falla 3 veces | Trabajo del día a día | **Fable 5** | Opus 5 |
| Secretario | Informes, WBS, DECISIONES.md, LECCIONES.md, registro de pruebas | Decidir | Haiku 4.5 | Sonnet 5 |

**Precios oficiales por millón de tokens** (platform.claude.com, consultado 29/07/2026): Fable 5 (`claude-fable-5`) 10 $/50 $ · Opus 5 (`claude-opus-5`) 5 $/25 $ · Sonnet 5 (`claude-sonnet-5`) 3 $/15 $, con 2 $/10 $ hasta el 31/08/2026 · Haiku 4.5 (`claude-haiku-4-5-20251001`) 1 $/5 $. Contexto de 1M tokens salvo Haiku (200k).

> Aviso Fable 5: estuvo suspendido en junio de 2026 por controles de exportación y volvió el 1 de julio; además puede rechazar peticiones por sus filtros. Respaldo obligatorio (tarea 03.01.04).
> Propuesta inicial: se confirma con el análisis de gb2 (01.02.01) y la prueba de agentes (03.01.02). Mientras trabajemos en chats: chat director = Orquestador + Validador; chat analista = Investigador.

## Autonomía: qué llega al CEO y qué no

**Lo cierra el equipo, sin consultar:** cerrar tareas que cumplen su criterio · orden de tareas ya aprobadas · subtareas dentro de alcance · descartar hipótesis o variantes que no pasan el filtro · reescribir tareas ambiguas · mover, corregir o borrar archivos para mantener el orden (git deshace).

**Llega al CEO, en el informe semanal:** mejoras del motor no previstas (sin aprobación, no se hacen) · tareas nuevas de primer nivel.

**Llega al CEO como excepción inmediata (se para hasta respuesta):** gasto nuevo (datos de pago, VPS, broker, créditos extra) · cualquier cosa con dinero real · bloqueo de más de 24 h · 2 vueltas sin éxito.

**Llega al CEO solo en una puerta:** cambiar de mercado, de tamaño de vela o de planteamiento.

## Fase 01 — ARRANQUE (puerta G0)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 01.01.01 | Aprobar plan y reglas | CEO | — | **hecha** 03/08 — FICHA (incumplimiento de regla 5 de CLAUDE.md declarado: se trabajó sin ficha previa): aprobación del WBS v0.7 (29/07/2026), que antecede a `CLAUDE.md`. El 01/08/2026 se aprobaron las decisiones D-1 a D-16, que ratificaban el WBS vigente más `CLAUDE.md`. El 03/08/2026 se aprobó D-17, que suspende la regla 8 de CLAUDE.md hasta que 03.01.05 esté hecha o llegue el 01/09/2026, lo que ocurra primero. CRITERIO DE HECHO: aprobación declarada en las decisiones del 01/08 (D-1 a D-16) y la del 03/08 (D-17) en `00-direccion/DECISIONES.md`. RESUELTO: lo que el CEO aprobó el 29/07 (WBS v0.7 anterior a `CLAUDE.md`) se ratifica ahora por D-1 a D-16, que fijan la lista completa de valores, límites y criterios. La ambigüedad en la que vivía esta tarea entre dos versiones del documento (v0.7 vs. lo que dice D-16 hoy) se cierra citando D-17 como corolario que actualiza el régimen de motor para la ejecución, sin reabrir lo ya ratificado. |
| 01.01.02 | Aprobar criterios de la puerta G1 | CEO | 01.01.01 | **hecha** 01/08 — opción A de la ficha: los 7 criterios G1-C1..G1-C7 aprobados (D-11). Recorrido: constructor-datos, investigador, crítico-código, validador. Propuesta inicial corregida en cuatro puntos por crítico y validador. FICHAS DE APOYO (localizadas en 07.01.01(c), 02/08): `01-investigacion/mercados/evidencia_umbrales_g1.md` (investigador, evidencia externa; se autodeclara «Apoya a: 01.01.02») y `04-resultados/veredictos/veredicto_criterios_g1.md` (validador, contraataque a la propuesta C1-C7; título propio «tarea 01.01.02»). |
| 01.01.03 | Fijar límites: fecha tope, horas CEO/semana, pérdida máxima futura | CEO | 01.01.01 | **hecha** 01/08 — los tres limites del CEO firmados: D-12 fecha tope, D-13 horas, D-14 perdida maxima → `00-direccion/expedientes/01.01.03.md` |
| 01.02.01 | Analizar gb2 como información (no copia) | Crítico | 01.01.01 | **hecha** 30/07 — `INFORME_GB2.md`. FICHA DE APOYO (localizada en 07.01.01(c), 02/08): `01-investigacion/herencia-gb2/HERENCIA_GB2.md`, que se autodeclara en su primera línea «Tarea 01.02.01 cerrada. Fuente: INFORME_GB2.md» y contiene la ficha D6 del trasplante. |
| 01.02.03 | Auditar el catálogo `awesome-claude-code` **y, por ampliación del CEO (01/08), las fuentes oficiales de Anthropic y los mecanismos nativos de Claude Code**; proponer máximo 4 piezas concretas para el motor, con motivo y coste de integración. **Carril de motor: cuenta contra el 20%** y se limita a 1 tirada | Investigador | 03.01.02 | **hecha** 03/08 — auditoria del ecosistema: las cuatro propuestas nativas repartidas a 03.01.18, 03.01.19, 03.01.04 y 03.01.03 → `00-direccion/expedientes/01.02.03.md` |
| 01.02.04 | **NUEVA 01/08 (petición del CEO):** evaluar si merece la pena añadir servidores MCP al proyecto, con veredicto por servidor y regla de admisión escrita para el futuro. **Carril de motor: cuenta contra el 20%** y se limita a 1 tirada | Investigador | 03.01.02 | **hecha** 03/08 — veredicto sobre MCP: cero servidores; las reglas deny no alcanzan al espacio de nombres mcp__ → `00-direccion/expedientes/01.02.04.md` |

## Fase 02 — ELEGIR MERCADO Y TAMAÑO DE VELA (puerta G1)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 02.01.01 | Confirmar 8 candidatos: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD, BTC, ETH | CEO + Orquestador | 01.01.02 | **hecha** 03/08 — ratificado por la vía de los hechos: **D-19** elige XAUUSD, y elegir un miembro del censo ratifica el censo del que sale. Los 8 se usaron en toda la Fase 02 (ATR, costes, correlaciones, arrastre). No queda ratificación formal pendiente. |
| 02.01.02 | Costes típicos de operar por mercado (PROVISIONAL hasta 04.01.02) | Investigador | 02.01.01 | **hecha** 31/07 — coste de entrar y salir de 8 instrumentos, ida y vuelta, con el tipo de cuenta declarado → `00-direccion/expedientes/02.01.02.md` |
| 02.02.01 | **CORREGIDA 29/07:** descargar precios y CALCULAR el ATR de 15m, 1h y 4h (no buscarlo publicado: no existe). Script `atr_local.py` | Constructor de datos | 02.01.01 | **hecha** 31/07 — ATR real de 8 instrumentos en 15m, 1h y 4h: 24 de 24 celdas calculadas sobre precios descargados → `00-direccion/expedientes/02.02.01.md` |
| 02.02.02 | Coste relativo: coste ÷ movimiento medio, en % (el número clave). Coste de USDJPY corregido a 1,16 pips | Constructor de datos | 02.01.02, 02.02.01 | **hecha** 31/07 — coste relativo, el criterio 1 de G1: coste entre ATR en cuatro escenarios de vela → `00-direccion/expedientes/02.02.02.md` |
| 02.02.03 | **CORREGIDA 30/07:** CALCULAR la matriz de correlaciones en 3 ventanas (3 meses, 1 año, 2 años) con hora de corte única (22:00 UTC) y en la vela elegida, no solo diaria. No existe publicada de forma homogénea | Constructor de datos | 02.01.01 | **hecha** 31/07 — 12 matrices de correlaciones 8x8 sobre rendimientos logaritmicos, corte unico 22:00 UTC → `00-direccion/expedientes/02.02.03.md` |
| 02.02.04 | Historial disponible: años, fuente, coste | Investigador | 02.01.01 | **hecha** — Dukascopy (tick desde 2003, forex y oro al contado), HistData, TrueFX, Binance, Kraken. Todo gratis, muy por encima de los 5 años exigidos |
| 02.02.05 | **NUEVA:** coste de mantener posición de un día para otro (swap/financiación) en los 8 instrumentos, 2-3 brokers. En cripto CFD puede superar varias veces al spread | Investigador | 02.01.01 | **hecha** 31/07 — `coste_swap.md`. Coste de mantener posicion en 8 instrumentos x 3 brokers (OANDA, XTB, Pepperstone), largo y corto por separado, en % anual y $/dia sobre 100.000 USD. VERIFICADO por recalculo independiente: las 30 celdas con % y $/dia cuadran; signos de USDJPY y USDCHF coherentes entre brokers (L-006 comprobada, sin inversion de convencion). HALLAZGO PARA G1: mantener cripto cuesta -33,6% anual (OANDA) y -22,5% (Pepperstone), entre 20 y 30 veces mas que entrar y salir; el oro -6,6%/-8,2%; y USDCHF y USDJPY en largo PAGAN (+2,6% y +1,6%). Implicacion: si entra cripto en el portafolio, la estrategia no puede aguantar posiciones de un dia para otro. HUECO DECLARADO: ETHUSD queda con una sola fuente fiable (XTB lo ofrece al contado, no CFD; Pepperstone no publica cifra de ETH), por debajo del minimo de dos fuentes independientes. |
| 02.03.01 | Revisión independiente de método, fuentes y números | Orquestador | 02.02.* | **hecha** 02/08 — revision transversal de la Fase 02: ACEPTA CON HUECOS DECLARADOS, con el motivo 5 al CEO → `00-direccion/expedientes/02.03.01.md` |
| 02.03.02 | Informe de decisión: mercado y vela. El alcance original decía 3-5 mercados poco correlacionados y 1-2 velas, alcance que **D-19 sustituye por un solo mercado** | Orquestador | 02.03.01 | **hecha** 03/08 — `01-investigacion/mercados/INFORME_DECISION_G1.md` y `03-motor/scripts/cestas_g1.py`. Escrito por el `validador`, **RECHAZADO** por `critico-codigo` en ronda 1 por tres motivos (la ficha colisionaba con D-18, ya firmada ese día; el máximo medido de 5,05x quedaba fuera de la ficha que lee el CEO, que decía 4,5x; ficha de 1.566 caracteres) y **ACEPTADO en ronda 2** tras reparación del propio `validador`. Medido por ejecución y reproducido después por Claude Code: a 4h **no existe ninguna cesta admisible de 4 ni de 5 instrumentos**, existen **exactamente 4 de 3**, y XAUUSD está en las cuatro. La condición del ACEPTA de 02.03.01 queda cumplida: el defecto del motivo 5 llegó declarado al CEO como AVISO 1. |
| 02.03.03 | PUERTA G1: el CEO elige | CEO | 02.03.02 | **hecha** 03/08 — **D-19: XAUUSD (oro al contado), vela de 4h, UN SOLO MERCADO.** Opción propia del CEO, fuera de las cuatro presentadas. **Deroga D-2** (portafolio de 3-5 mercados). La ampliación a un segundo mercado queda condicionada a que una hipótesis demuestre ganar dinero de verdad. Consecuencias registradas en D-19: G1-C5 queda sin objeto mientras haya un solo mercado, y los cinco huecos declarados del oro pasan a ser el riesgo entero del proyecto. |

## Fase 03 — MONTAR LA CASA (Claude Code) — EN PARALELO con la Fase 02
> **Deuda de motor congelada:** hay tareas de esta fase movidas a
> `00-direccion/DEUDA-MOTOR.md` hasta la puerta GM. No se ejecutan ni se citan.

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 03.01.01 | Repositorio: carpetas, WBS texto, CLAUDE.md, DECISIONES.md, LECCIONES.md | Constructores | 01.01.01 | **hecha** 30/07 — repo completo: carpetas, WBS, CLAUDE.md, DECISIONES.md, LECCIONES.md, plantillas y .gitignore (42 ficheros en git). AVISO regla 27 de CLAUDE.md **NO VERIFICADA**: la prueba de inyección de datos no se ha ejecutado; 02-datos/ está vacío. Se ejecuta al bajar los primeros precios en 02.02.01 |
| 03.01.02 | Crear TODOS los agentes del Equipo, cada uno con su modelo y descripción sin ambigüedad; prueba de activación de todos (ningún agente fantasma) | Constructores | 03.01.01, 01.02.01 | **hecha** 30/07 — 8 agentes en .claude/agents/, cada uno con identificador exacto de modelo y respaldo. Prueba de activación ejecutada 30/07: los 8 respondieron y leyeron un fichero real, ningún fantasma. LÍMITE: la prueba no demuestra que el modelo enrutado sea el de la ficha; se verifica en 03.01.04, con atención a claude-fable-5 (validador y arquitecto) |
| 03.01.03 | Ejecución desatendida: arranques programados, permisos AMPLIOS por defecto (git como red de seguridad) y topes de gasto | Constructores | 03.01.02 | **pendiente** 04/08 — ficha escrita: arranque por cron, aviso fuera de sesion y topes de gasto. Sin ejecutar → `00-direccion/expedientes/03.01.03.md` |
| 03.01.04 | Plan de respaldo de modelos: si un modelo no está disponible o rechaza, el agente sigue con su respaldo y lo anota | Constructores | 03.01.02 | **pendiente** 04/08 — ficha escrita: respaldo de modelo probado inyectando un fallo. Sin ejecutar → `00-direccion/expedientes/03.01.04.md` |
| 03.01.05 | PRUEBA REAL DEL MOTOR: un día entero de trabajo desatendido de verdad antes de dar la fase por buena | Orquestador | 03.01.03, 03.01.04 | pendiente |
| 03.01.06 | Plantilla y automatismo de fichas de decisión: el secretario prepara cada decisión del CEO en el formato obligatorio y la adjunta al informe semanal | Secretario | 03.01.02 | pendiente |
| 03.01.07 | Cola de aprobación del CEO: tabla con desplegable Aprobado / Saltar / Corregir y columna de corrección. Lo aprobado se ejecuta solo; lo corregido se rehace Y la corrección se guarda en LECCIONES.md | Secretario | 03.01.06 | pendiente |
| 03.01.08 | **Prueba de fuego de las barreras** (regla 25 de CLAUDE.md): inyectar cada caso prohibido —leer el cajón reservado, escribir fuera del proyecto, borrar datos, gastar dinero— y comprobar que se bloquea de verdad. Lo que no se bloquee se marca "no verificada" | Crítico | 03.01.01, 03.01.02 | **en_curso** 31/07 — primera pasada: 4 barreras de 5 verificadas por ejecucion; el cajon reservado sigue sin verificar → `00-direccion/expedientes/03.01.08.md` |
| 03.01.09 | Enrutado por tipo de tarea y comprobación de que el WBS genera tareas de cada tipo de agente (ver L-010 de LECCIONES.md; sin número propio en CLAUDE.md) | Constructores | 03.01.02 | pendiente |
| 03.01.10 | Testbed sintético de invarianza: resultado de referencia fijo que debe reproducirse tras cualquier cambio del motor | Constructores | 03.01.01 | pendiente |
| 03.01.13 | **NUEVA 01/08 (L-015):** una sola lista de reglas. Hoy `CLAUDE.md` y este WBS llevan cada uno una lista de «29 reglas» con **contenido distinto bajo el mismo número**, así que toda cita `regla N` del proyecto es ambigua | Constructores + CEO | — | **hecha** 03/08 — una sola lista de reglas normativa, la de CLAUDE.md (D-16); la del WBS queda derogada → `00-direccion/expedientes/03.01.13.md` |
| 03.01.11 | **NUEVA 31/07 (D-10):** guardia del cajon reservado por cifrado. Script `cajon_reservado.py`: la contraseña solo la tiene el CEO, no se guarda, se pide en cada operacion y nada se descifra a disco | Constructores | 03.01.08 | **en_curso** 31/07 — cajon_reservado.py probado: 6 de 6 casos prohibidos bloqueados; falta el hueco de settings.json → `00-direccion/expedientes/03.01.11.md` |
| 03.01.14 | **NUEVA 01/08 (deuda detectada al cerrar 03.01.13):** la hoja REGLAS del Excel del CEO la construye `05-vista-ceo/generar_excel.py` leyendo las líneas numeradas de la sección de reglas del WBS, que tras D-16 ya no existen: la hoja saldría vacía bajo el título «LAS 29 REGLAS», y `verificar_excel.py` no comprueba esa hoja, así que sus 8 pruebas pasarían igual (L-016). Hay que leer las reglas de `CLAUDE.md` y añadir una prueba que falle si la hoja sale vacía. **Deuda de motor: no se ejecuta sin permiso del CEO.** | Constructores | 03.01.13 | **pendiente** |
| 03.01.15 | Herramientas del `secretario`: puede escribir los registros que solo admiten añadir pero no puede verificarlos | Constructores | 03.01.02 | **hecha** 10/08 — diagnostico de las herramientas de los ocho agentes; de ahi salieron D-34 y la regla 30 → `00-direccion/expedientes/03.01.15.md` |
| 03.01.16 | Las hojas del Excel se construyen de sus fuentes primarias, no de copias | Constructores | 03.01.13, 03.01.14 | **hecha** 05/08 — las hojas del Excel se construyen de sus fuentes primarias; dos inyecciones nuevas, casos 6 y 7 → `00-direccion/expedientes/03.01.16.md` |
| 03.01.17 | Reparar la prueba 7 de `verificar_excel.py` (entregables de las tareas hechas) | Constructor de motor | 03.01.13 | **pendiente** 03/08 — ficha escrita: reparar la prueba 7 del verificador para que examine celdas completas. Sin ejecutar → `00-direccion/expedientes/03.01.17.md` |
| 03.01.18 | **NUEVA 03/08 (D-20, idea 1 de las auditorías):** contador mecánico del reparto producto/motor, inyectado en el contexto al arrancar cada tirada | Constructores | 03.01.01 | **hecha** 12/08 — contador producto/motor y hook SessionStart; reproduce 43,8% sobre los 16 commits del 01/08 → `00-direccion/expedientes/03.01.18.md` |
| 03.01.21 | Diagnóstico medido del consumo de tokens del motor de agentes | Secretario | 03.01.01 | **hecha** 04/08 — consumo de tokens medido sobre el transcript en disco: 207 peticiones del hilo principal → `00-direccion/expedientes/03.01.21.md` |
| 03.01.22 | Inventario por ejecución de los mecanismos de trabajo desatendido en esta máquina | Constructor de motor | 03.01.01 | **hecha** 04/08 — ejecutado por `constructor-motor`, revisado por `critico-codigo`. Probado por ejecución: `tmux` 3.4 presente · `cron` corriendo (PID 156, activo bajo systemd, persiste tras reinicio) · systemd real en esta WSL2 · `flock` y `jq` presentes · `screen`, `at`, `notify-send`, `mail` y `sendmail` **NO** instalados · `claude` 2.1.221. Hallazgos: `--max-budget-usd` existe (solo con `--print`) · `--max-turns` existe pero oculto, no sale en `claude --help` · `--fallback-model` existe · en modo `-p` un permiso no se queda colgado: se resuelve solo. **HUECOS:** no hay forma de avisar al CEO fuera de la máquina sin webhook, porque no hay `notify-send` ni correo. Pendiente de decisión del CEO. Que `--max-budget-usd` corte de verdad no está probado por ejecución (regla 25 de CLAUDE.md). Criterio de hecho: cada línea del inventario con su comando y su salida real. |
| 03.01.23 | Encadenador de trabajo desatendido: una conversación por tarea | Constructor de motor | 03.01.02 | **en_curso** 04/08 — encadenador desatendido: no se enciende hasta una tirada real supervisada y hasta 03.01.08 → `00-direccion/expedientes/03.01.23.md` |
| 03.01.24 | **NUEVA 05/08 (nace de los huecos medidos por ejecución en 03.01.08):** las tres barreras que hoy NO existen. (a) El patrón `Bash(* 02-datos/reservado*)` de `.claude/settings.json` exige un espacio literal y no cubre la ruta pegada a una comilla, así que una línea de python lo esquiva: sustituirlo por un patrón que cubra cualquier verbo y cualquier forma de escribir la ruta, y probarlo con las TRES formas. (b) Nada impide `rm -rf` dentro de `02-datos/`, y los datos no están en git (regla 27 de CLAUDE.md): no se rehacen deshaciendo un commit, se rehacen volviendo a descargarlos. (c) No hay ninguna barrera de gasto, ni en código ni en configuración; D-26 de `00-direccion/DECISIONES.md` deja escrito que `--max-budget-usd` existe. Regla 24 de CLAUDE.md: las tres nacen de una inyección ejecutada con su salida guardada, no de una sospecha, y ninguna causó daño. Regla 25 de CLAUDE.md: cada barrera nueva se verifica por inyección ANTES de documentarse como activa. | Constructores | 03.01.08 | **pendiente** — **DESCONGELADA 12/08/2026 por D-36 de `00-direccion/DECISIONES.md`**, que da la letra aparte que D-29 exigia para aplicar el parche. Ficha de decisión preparada para el 06/08 **FICHA ESCRITA Y ENTREGADA 06/08:** `00-direccion/informes/FICHA_D-29.md`, dos rondas, **ACEPTA CON REPAROS** de `critico-codigo` en la ronda 2, con sus dos reparos resueltos antes de cerrar. Los puntos (a), (b) y (c) de esta tarea son los puntos (a), (b) y (c) de la ficha. **CORRECCIÓN DE ALCANCE QUE SALIÓ DE LA REVISIÓN, sobre (c):** D-26 avisa de que `--max-budget-usd` puede ser inerte, y la celda de 03.01.23 lo da por medido —no hay clave de API en esta máquina y un tope en dólares no limita nada—, así que (c) puede resultar imposible tal como está escrita. La ficha se lo declara al CEO, y si se autoriza, esta tarea EMPIEZA por comprobar si existe barrera de gasto posible antes de prometer ninguna (regla 25 de CLAUDE.md). **INCIDENTE REGISTRADO, y es sobre una corrección de hecho que no procedía:** esta celda llevó unas horas del 06/08 la frase «decía que la ficha estaba preparada el 05/08 y no existía». Era falsa: el texto anterior decía «Ficha de decisión preparada para el 06/08» — y es ese «para» lo que la hace promesa a futuro y no afirmación de existencia, que es una promesa a futuro y se cumplió el 06/08. No había nada que corregir. La dictó el `orquestador` sin localizar el defecto en el artefacto y la cazó `critico-codigo` en la auditoría de cierre: es L-033 de LECCIONES.md incumplida por quien reparte, esta vez sin revisor intermedio al que atribuirlo. **SIGUE pendiente: no se ejecuta hasta que el CEO responda la letra.** **AVISO DE CITA (regla 12 de CLAUDE.md):** `FICHA_D-29.md` es una ficha a la espera de la letra del CEO. **No existe ninguna D-29 firmada en `00-direccion/DECISIONES.md`, que llega hasta D-27.** Citarla como decisión sería falso hasta que el CEO responda y se escriba. |
| 03.01.25 | **NUEVA 05/08 (nace del incidente de este mismo día):** guardia en `.githooks/pre-commit` que ejecuta la métrica de L-027 de `00-direccion/LECCIONES.md` sobre `00-direccion/WBS.md` y **rechaza el commit** si alguna fila de tarea no da 7 campos al partirla por la barra vertical. Motivo: hoy la métrica existe, está escrita como normativa en este WBS, y no la ejecuta nadie automáticamente; `05-vista-ceo/verificar_excel.py` no la cubre. Es el muro que le falta a la única fuente de verdad del proyecto. Regla 24 de CLAUDE.md: nace de un incidente real y medido — el 05/08 cuatro filas quedaron partidas y ningún guardia se enteró. Regla 25 de CLAUDE.md: se verifica por inyección de una fila rota ANTES de documentarse como activo. AVISO PARA QUIEN LA EJECUTE, medido el mismo día: el propio texto de esta fila no puede contener el comando literal, porque la barra vertical que lleva dentro rompe la fila que describe; el guardia tiene que tolerar esa cita cuando aparezca en prosa fuera de una tabla. | Constructor de motor | 03.01.01 | **pendiente** — **DESCONGELADA 12/08/2026 por D-36 de `00-direccion/DECISIONES.md`**, que da la letra aparte que D-29 exigia para aplicar el parche. Entra como cuarto punto de la ficha D-29 del 06/08 **CUMPLIDO 06/08:** entra como punto (d) de `00-direccion/informes/FICHA_D-29.md`, con la cifra restituida —el 05/08 se partieron cuatro filas— después de que un primer intento la perdiera al apretar prosa; la cazó `critico-codigo` (L-023 y L-034 de LECCIONES.md). **SIGUE pendiente: no se ejecuta hasta que el CEO responda la letra.** Misma advertencia de cita que en 03.01.24: la ficha D-29 no está firmada en `DECISIONES.md`. |

## Fase 04 — HIPÓTESIS Y VALIDACIÓN (puerta G2)

### 04.01 Broker y cajones de datos
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.01.01 | Comparar 3-4 brokers del mercado elegido; elegir uno y abrir demo (CEO firma) | CEO + Orquestador | 02.03.03 | **en_curso** 06/08 — comparacion de brokers: ronda 2 cerrada en falso, con una cita literal falsa cazada → `00-direccion/expedientes/04.01.01.md` |
| 04.01.02 | Recalcular costes con precios reales del broker (sustituye 02.01.02) **REQUISITO AÑADIDO 04/08:** al recalcular con precios reales se comprueba que **la entidad que publica la tarifa es la misma con la que se opera**. Si no coinciden, la cifra vieja no se hereda: se vuelve a medir. | Constructor datos | 04.01.01 | pendiente |
| 04.01.03 | Histórico limpio partido en 3 cajones: construir (train), ajustar (validación) y RESERVADO bajo llave (OOS, se abre una sola vez por variante). Ningún agente toca el reservado | Constructor datos | 04.01.01 | pendiente |
| 04.01.04 | **NUEVA 09/08 (subtarea dentro del alcance de 04.01.01, creada por el orquestador, regla 2 de CLAUDE.md):** re-derivar POR CÁLCULO el tamaño mínimo operable de XAUUSD en 4h y el requisito real de lote que 04.01.01 debe exigir al bróker | Constructor de datos | 02.02.01, 02.03.03 | **en_curso** 09/08 — re-derivacion de la comparacion de brokers; ficha escrita tarde y anotada como incumplimiento → `00-direccion/expedientes/04.01.04.md` |

### 04.02 Investigación de hipótesis
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.02.01 | Barrido de fuentes: papers, libros, foros, GitHub, X. Regla: mínimo 2 fuentes independientes verificables por idea; vendedores de cursos/señales no son fuente | Investigador | 03.01.02 | pendiente |
| 04.02.02 | Ficha por hipótesis: por qué existiría la ventaja, reglas de entrada/salida, mercado y vela. Sin lógica de por qué gana, no entra (nada de probar por probar) | Investigador | 04.02.01 | pendiente |
| 04.02.03 | Filtro de sentido: el Validador puntúa y se eligen las 3-5 mejores | Validador | 04.02.02 | pendiente |
| 04.02.04 | Pre-registro de variantes: cada hipótesis deja escritas sus variantes ANTES de probar (máx. 5-7 por hipótesis). Lo no registrado no se prueba | Validador | 04.02.03 | pendiente |

### 04.03 Laboratorio de pruebas (por hipótesis y variante)
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.03.01 | Backtest con costes reales sobre el cajón de construir | Constructores | 04.01.03, 04.02.04, 04.03.07 | pendiente |
| 04.03.02 | Ajuste SOLO con el cajón de validación; lo que no aguanta, muere aquí | Constructores | 04.03.01 | pendiente |
| 04.03.03 | Prueba de fuego: UNA sola pasada por variante sobre el cajón reservado (OOS). Repetir sería hacerse trampa | Validador | 04.03.02 | pendiente |
| 04.03.04 | Robustez: Monte Carlo (barajar el orden de operaciones y meter pequeños cambios miles de veces: ¿aguanta o era suerte?) + walk-forward (repetir el ajuste avanzando en el tiempo) | Validador | 04.03.03 | pendiente |
| 04.03.05 | Veredicto pasa/no pasa por variante, con los criterios de G2. Quien construyó no vota | Validador | 04.03.04 | pendiente |
| 04.03.06 | **NUEVA 03/08 (decisión del CEO, opción B):** especificación del motor de backtest propio, escrita para una construcción desde cero y no para un trasplante | Arquitecto | 02.03.03 | **hecha** 04/08 — especificacion del motor de backtest: 16 requisitos con prueba ejecutable y 8 casos a mano → `00-direccion/expedientes/04.03.06.md` |
| 04.03.07 | **NUEVA 03/08 (decisión del CEO, opción B):** construir el motor de backtest desde cero contra la especificación de 04.03.06, tras retirar el anterior | Constructor de motor | 04.03.06, 07.01.03 | **hecha** 04/08 — motor de backtest construido desde cero; procedencia independiente de las dos fuentes → `00-direccion/expedientes/04.03.07.md` |

### 04.04 Decisión y bucle
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.04.01 | Informe de la vuelta: qué pasó, qué murió y por qué. Registro de TODAS las pruebas, también fallidas | Secretario | 04.03.05 | pendiente |
| 04.04.02 | Si ninguna pasa: volver a 04.02 con lecciones (vuelta 2, 3…). Tras la 3ª vuelta sin éxito: revisión completa del planteamiento con el CEO | Orquestador | 04.04.01 | pendiente |
| 04.04.03 | PUERTA G2: el CEO decide qué pasa a demo | CEO | 04.04.01 | pendiente |

## Fase 05 — DEMO (puerta G3) — se detalla al cerrar G2

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 05.01.01 | Bot en demo, solo y con guardias automáticos | Constructores | 04.04.03 | pendiente — REQUISITO AÑADIDO POR D-14 (01/08): el guardia de parada dura (-30% del capital inicial) lo aplica el BOT de forma CONTINUA, no una revision periodica; comprobado solo una vez al mes, un -30% puede ser un -45% cuando alguien mire. Se verifica por inyeccion antes de declararlo activo (regla 25 de CLAUDE.md). |
| 05.01.02 | Seguimiento semanal real vs. prometido (8-12 semanas) | Secretario | 05.01.01 | pendiente |
| 05.01.03 | PUERTA G3: CEO decide dinero, cuánto y pérdida máxima | CEO | 05.01.02 | pendiente |

## Fase 06 — REAL (puerta G4) — se detalla al cerrar G3

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 06.01.01 | Dinero pequeño respetando los límites de 01.01.03 | Constructores | 05.01.03 | pendiente — limites ya escritos y firmados (D-14, 01/08): capital 1.000-2.000 €, AVISO a -25% del capital inicial que no para nada, PARADA DURA AUTOMATICA a -30% aplicada por el bot de forma continua y sin exencion activable desde dentro (regla 26 de CLAUDE.md). |
| 06.01.02 | PUERTA G4 mensual: seguir, ampliar o parar. Si pierde más de lo escrito, se para sin discusión | CEO | 06.01.01 | pendiente |

## Fase 07 — MOTOR Y ORDEN (paralela; máx. 20% del esfuerzo semanal)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 07.01.01 | Carpetas y documentos en orden; una fuente de verdad por tema; lo sustituido se borra | Constructores | 03.01.01 | **pendiente** 02/08 — orden de carpetas y documentos: la cifra 246/105 retirada por no reproducirse. Sin cerrar → `00-direccion/expedientes/07.01.01.md` |
| 07.01.03 | **NUEVA 03/08 (incidente de proceso):** auditar todo lo escrito el 03/08/2026 entre las 21:44 y las 21:58 sin flujo de cuatro capas, y el residuo sin commitear del tramo anterior | Orquestador | — | **en_curso** 09/08 — auditoria de lo escrito sin flujo el 03/08; los lotes de aptitud cancelados por el CEO → `00-direccion/expedientes/07.01.03.md` |
| 07.01.02 | Mejoras del motor: SOLO tareas aprobadas en revisión semanal (el motor no manda) | Constructores | 03.01.02 | pendiente |


## Calendario del mes (03 agosto → 1 septiembre 2026)

**Objetivo del mes:** NO es tener el bot en demo. Es llegar al 1 de septiembre con respuesta a "¿existe alguna estrategia que merezca pasar a demo?". **Holgura de calendario: cero.** G1 se cierra 04-05/08; broker se firma 10/08 (NO RETORNO). **Nota crítica:** 04.03.03 (prueba OOS) es una sola pasada por variante sobre el cajón reservado — no se puede repetir ni acelerar.

| Período | Fechas | Tareas | Qué se hace | Fin previsto | Checkpoint |
|---|---|---|---|---|---|
| S1 | 03 – 05 ago | 02.03.02, 02.03.03 | Informe de G1 + puerta (el CEO elige mercados) | Mercados y vela | Mié 4-Jue 5: decisión del CEO |
| S2 | 06 – 10 ago | 04.01.01 | Elegir broker, abrir demo | Broker firmado | **Viernes 10 ago: NO RETORNO** |
| S3 | 11 – 14 ago | 04.01.02, 04.01.03 | Costes reales del broker + tres cajones (train, validación, OOS) | Cajones listos | Lun 12-Jue 14: preparando OOS |
| S4 | 15 – 20 ago | 04.02.01 a 04.02.04 | Barrido de hipótesis + filtro de sentido + pre-registro de variantes | 3-5 hipótesis con variantes registradas | Lun 19-Jue 20: qué entra al backtest |
| S5 | 21 – 25 ago | 04.03.01, 04.03.02 | Backtest sobre train + ajuste sobre validación | Variantes supervivientes tras ajuste | Lun 24-Jue 25: cuántas avanzan |
| S6 | 26 – 30 ago | 04.03.03 a 04.03.05 | OOS sobre cajón reservado (UNA sola pasada) + Monte Carlo + walk-forward + veredicto | Veredicto pasa/no pasa por variante | Lun 26: OOS listo (irreversible) |
| S7 | 31 ago | 04.04.01 | Informe de la vuelta | Informe guardado, métricas listas | Lun 31: preparar GM |
| GM | 1 sept | — | Puerta del mes: arrancar demo / otra vuelta / replantear / PARAR | Decisión del CEO | Mar 1: reunión presencial |
| Nota | 07 ago | 03.01.05 | Fin bloque de motor: Fase 03 (03.01.02 a 03.01.06) lista en 24 h continuas de trabajo desatendido | Motor probado | — |

**Lo que NO cabe en el mes:** la demo (8-12 semanas de mercado real, reloj no acelerable) · más de una vuelta del bucle (cabe una) · el dinero real.

## Límites del CEO (29/07/2026, cerrados el 01/08/2026 en la tarea 01.01.03)

- **Horizonte:** 1 mes. Evaluación el 1 de septiembre (puerta GM). *(D-5)*
- **FECHA TOPE: 01/12/2026** *(D-12)*. Si a esa fecha no hay ninguna estrategia en demo, el proyecto se cierra y se escribe el informe de por qué. Antes del 01/08/2026 no existía ninguna fecha de parada.
- **Revisión de avance el día 1 de cada mes** *(D-12)*: 01/09 (= GM), 01/10 y 01/11. Cada una puede PARAR el proyecto. Pregunta fija: «¿avanza por buen camino?».
- **Tiempo del CEO: 1 hora los lunes, como MÍNIMO GARANTIZADO, no como techo** *(D-4 + D-13 + D-18)*. Lo que esté listo le llega el día que esté listo, sin tope de número; el CEO marca el final del día cuando no puede seguir, lo que quede acumula al día siguiente. Máximo 5 fichas de decisión en el checkpoint del lunes; si hay más, el orquestador prioriza y las sobrantes esperan al lunes siguiente. Lo que protege es que cada ficha llegue en formato obligatorio (sección «Qué llega al CEO y qué no» de `CLAUDE.md`): masticada, opciones cerradas, recomendada con motivo, respuesta de una letra. El CEO sigue el proyecto a diario, lo que NO amplía lo que se le puede preguntar.
- **Dinero real** *(D-14)*: capital 1.000-2.000 € (ya es entrada de G1-C6, D-11; cambiarlo obliga a re-verificar G1-C6). **AVISO a -25%** del capital inicial ingresado, que no para nada: se reporta y decide el CEO. **PARADA DURA AUTOMÁTICA a -30%** del capital inicial, aplicada por el bot de forma CONTINUA y sin exención activable desde dentro (regla 26 de CLAUDE.md). Se mide sobre el capital inicial ingresado, no sobre el máximo alcanzado. Recuperar desde -30% exige +43%.
- **Techo del 20% de motor (regla 8 de CLAUDE.md) SUSPENDIDO** *(D-17)*: El 03/08/2026 el techo de motor quedó SUSPENDIDO hasta que 03.01.05 esté hecha O llegue el 01/09/2026, lo que ocurra PRIMERO. Mientras esté en vigor la suspensión, el equipo puede dedicar más del 20% a motor en una tirada si es necesario para desbloquear producto. La regla 8 no se elimina; se suspende con disparador que impone el sistema (regla 26 de CLAUDE.md).

## Puertas

- **G0** (en curso): CEO aprueba plan, criterios y límites (01.01.01–03).
- **G1** (CRITERIOS APROBADOS 01/08/2026, D-11): siete criterios numerados
  - **G1-C1 — PRESUPUESTO DE COSTE ANUAL.** El coste TOTAL al año (entrar y salir MAS mantener posicion) no puede superar el 5% del capital, calculado con la formula compuesta. Anclaje: regla publicada de Robert Carver ("no gastar mas de un tercio del retorno esperado en costes") con un retorno objetivo declarado del 15% anual. EL 15% ES UN SUPUESTO ELEGIDO POR EL ORQUESTADOR Y APROBADO POR EL CEO, NO UN DATO MEDIDO. Forma operativa: el presupuesto se traduce en un tope de operaciones al año por vela — 15m entre 29 y 105, 1h entre 62 y 217, 4h entre 126 y 426, segun instrumento. NO prohibe ninguna vela: impone un tope. Robustez comprobada: con retornos objetivo entre 10% y 30%, la vela de 4h pasa 6 de 6 instrumentos en todos los casos; para que 1h pasara entera habria que declarar un retorno del 75,5% anual.
  - **G1-C2 — COSTE POR OPERACION EN LA VELA TRANQUILA.** Coste de ida y vuelta dividido por el ATR del percentil 10 (vela tranquila), menor o igual al 10%. Filtra instrumentos. A 4h pasan los 6 no-cripto (el peor es AUDUSD con 5,24%); ETHUSD queda fuera (15,13% a 35,37%).
  - **G1-C3 — COSTE DE MANTENER POSICION.** No tiene umbral propio: suma dentro del 5% de G1-C1. Medido: una noche por operacion añade ~2,28% anual en EURUSD largo y ~2,36% en XAUUSD largo; dos noches llevan EURUSD a 7,01%, por encima del presupuesto.
  - **G1-C4 — MUESTRA.** Minimo 1.000 velas al año por instrumento en la vela elegida (4h da 1.611). NO se fija un minimo de operaciones: la investigacion externa no encontro ninguna fuente primaria que lo respalde. El control de sobreajuste se hace en G2 con el Deflated Sharpe Ratio, que penaliza por numero de VARIANTES probadas, no por numero de operaciones.
  - **G1-C5 — CORRELACION DE LA CESTA.** Los 3-5 instrumentos elegidos no pueden superar 0,7 entre si, en las tres ventanas (3 meses, 1 año, 2 años) y en la vela elegida. Filtra la CESTA, no instrumentos sueltos. Se declara: lo que de verdad importa para diversificar es la correlacion de los rendimientos de la ESTRATEGIA, no la de los activos; en G1 no hay estrategia, asi que se usa la del activo como sustituto y se re-verifica en G2. Cripto queda FUERA de la cesta por defecto: solo tiene 1 de las 3 ventanas, es inverificable (regla 26 de CLAUDE.md, los guardias bloquean por defecto).
  - **G1-C6 — TAMAÑO MINIMO OPERABLE.** Con el capital declarado (1.000-2.000 euros), el instrumento debe permitir arriesgar como mucho el 1% del capital por operacion con un stop de 1 x ATR MEDIANA (no la media, que en el oro esta inflada un 28-30% por su pausa diaria). Recalculado asi, XAUUSD en 4h necesita 1.962 euros y CABE bajo el techo de 2.000. NO elimina ningun instrumento: se convierte en REQUISITO PARA LA ELECCION DE BROKER de la tarea 04.01.01 — el broker elegido debe ofrecer lote minimo de oro igual o menor a 0,1 onzas.
  - **G1-C7 — HUECO DE FIN DE SEMANA (CRITERIO NUEVO).** El percentil 90 del salto de precio del lunes, dividido por el stop de 1 x ATR de la vela, no debe superar 0,5. NINGUN instrumento lo cumple. Medido sobre datos brutos y verificado por recalculo independiente del orquestador el 01/08/2026: el hueco supera el stop ENTERO entre 11 y 17 veces en 696 dias (6-9 veces al año) en los 6 instrumentos no-cripto; percentil 90 entre 1,10x y 1,50x el stop; maximo 4,52x en EURUSD. Consecuencia obligatoria: la estrategia cierra posiciones antes del viernes, o G2 declara explicitamente que la perdida real puede alcanzar 4,5 veces el riesgo nominal.
  - **FUERA DE G1:** el criterio "operable sin nadie delante" sale de la puerta G1 y pasa a la Fase 03, porque no distingue entre los 8 mercados candidatos (todos se operan igual por API): es una propiedad del motor, no del mercado.
  - **HUECO DECLARADO EN G1:** el DESLIZAMIENTO no entra en ningun criterio porque no existe ningun factor publicado por clase de activo, vela u hora. La convencion encontrada (mitad del spread mas impacto de mercado) no da un numero. Se mide con precios del broker real en la tarea 04.01.02 y se re-verifica G1 si algun resultado cambia.
- **G2**: solo pasan variantes que ganan después de costes en OOS, aguantan Monte Carlo y estaban pre-registradas. Veredicto del Validador.
- **G3**: demo de 8-12 semanas parecida a lo prometido; CEO fija dinero y pérdida máxima.
- **G4** (mensual): si toca la parada dura de **-30% del capital inicial** (D-14), se para sin discusión. El aviso de -25% NO para: se reporta y decide el CEO. La parada la aplica el bot de forma continua, no esta revisión mensual.
- **GM** (1 de septiembre de 2026): puerta de evaluación del primer mes. Decisión: arrancar demo, dar otra vuelta al bucle, replantear **o PARAR** (cuarta salida añadida en D-12). Es la primera de las revisiones mensuales de avance; las siguientes, 01/10 y 01/11.
- **FECHA TOPE (1 de diciembre de 2026)** (D-12): si no hay ninguna estrategia en demo, el proyecto se cierra y se escribe el informe de por qué.

## Registro de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-07-29 | Producto antes que motor; motor máx. 20% en paralelo | Evitar la deriva de gb2 |
| 2026-07-29 | Portafolio 3-5 mercados poco correlacionados | Riesgo repartido + muestra |
| 2026-07-29 | Mercado y vela se deciden en G1 con datos | Evitar corazonadas |
| 2026-07-29 | CEO: revisión semanal + puertas, sin firmas por tarea | Dirección por excepción |
| 2026-07-29 | Broker después de G1; costes provisionales mientras | Búsqueda enfocada |
| 2026-07-29 | WBS texto = fuente de verdad; Excel = vista del CEO | Agentes leen texto |
| 2026-07-29 | Cada agente con su modelo según tarea (tabla Equipo); confirmar con análisis gb2 | Replicar lo bueno de gb2 con criterio |
| 2026-07-29 | gb2 se analiza como información, no como copia (01.02.01) | Lecciones sin contaminación |
| 2026-07-29 | Validación: 3 cajones (train/validación/OOS) + Monte Carlo + walk-forward, con pre-registro de variantes (máx. 5-7) y registro de fallidas | Cuantas más variantes, más fácil que una gane por suerte; esto lo controla |
| 2026-07-29 | Bucle de investigación si nada pasa; a la 3ª vuelta sin éxito, revisión con el CEO | Bucle sano, no infinito |
| 2026-07-29 | Regla de no-ambigüedad: tarea que obliga a adivinar vuelve al orquestador | La ambigüedad fue causa del caos en gb2 |
| 2026-07-29 | Restricción justificada: permisos amplios + git; restricciones solo tras incidente real, revisadas cada mes | En gb2 se restringió de más sobre el papel y hubo que ir quitando |
| 2026-07-29 | Modelos por puesto: Fable 5 en validación y arquitectura, Opus 5 en orquestación, Sonnet 5 en construcción e investigación, Haiku 4.5 en secretaría | Fuentes oficiales consultadas 29/07/2026; el modelo caro solo donde un error cuesta dinero |
| 2026-07-29 | Respaldo obligatorio para todo agente con Fable 5 | Fable 5 estuvo suspendido en junio de 2026 y puede rechazar peticiones |
| 2026-07-29 | La Fase 03 no se cierra sin un día entero de trabajo desatendido real (03.01.05) | Evitar el motor perfecto en papel de gb2 |
| 2026-07-29 | Escalado definido (sección Autonomía): el CEO solo interviene en puertas y excepciones | El CEO no firma tareas |
| 2026-07-29 | Formato obligatorio de ficha de decisión del CEO (sección «Qué llega al CEO y qué no» de CLAUDE.md + plantilla) | Reducir al mínimo el tiempo del CEO: ni redactar, ni buscar, ni calcular |
| 2026-07-29 | D1 resuelta: se fija AHORA qué se mide (misma vara para los 8) y se calibran los umbrales en G1 con los números delante | El CEO no quiere cortes a ciegas; sin vara común, cada mercado se mediría distinto |
| 2026-07-29 | Guardarraíles en dos niveles: reversible permisivo, irreversible con barrera desde el minuto uno | Matiz de un vídeo analizado el 29/07 |
| 2026-07-29 | Cola de aprobación con Aprobado / Saltar / Corregir; toda corrección escrita va a LECCIONES.md | El valor está en que la corrección quede guardada |
| 2026-07-29 | 02.02.01 pasa de "buscar ATR publicado" a "calcular ATR sobre precios reales" | El dato no existe publicado; sí existen los precios (L-001) |
| 2026-07-29 | Se añade el swap/financiación como segundo componente del coste (02.02.05 y criterio 1 de G1) | En CFD de bitcoin la financiación (-22,5% anual) supera al spread si se mantiene la posición |
| 2026-07-29 | El Excel se regenera solo los lunes y en las puertas; el WBS en texto, siempre | Decisión del CEO: no necesita la vista cada vez |
| 2026-07-30 | **D6 = B.** Repositorio nuevo con reglas y agentes desde cero; se trasplantan 5 piezas de gb2, una a una, cada una con criterio de aceptación probado aquí | Decisión del CEO. Reescribir motor y datos se comería el mes sin acercar la respuesta |
| 2026-07-30 | Jerarquía de la prueba: ejecución > verificación documental > contraste entre agentes. El consenso entre agentes no cierra nada | Petición del CEO ("miedo a que una IA decida y no tenga razón") + evidencia de gb2 |
| 2026-07-30 | El análisis del catálogo `awesome-claude-code` es trabajo de motor: entra en el carril del 20% y se limita a 1 tirada con máximo 4 propuestas | Aplicación de la regla 8 de CLAUDE.md a una petición del propio CEO |
| 2026-08-01 | 01.02.03 amplía alcance: además del catálogo, fuentes oficiales de Anthropic y mecanismos nativos de Claude Code | Petición del CEO. El catálogo por sí solo dejaba fuera lo que ya está instalado y sin usar |
| 2026-08-01 | Se añade 01.02.04: evaluar MCP con veredicto por servidor y regla de admisión escrita | Petición del CEO; no estaba medido en el WBS |
| 2026-08-01 | Se añade 03.01.12: estrategia de ramas, con el criterio del CEO «agilidad, no complejidad» | Petición del CEO. Hoy todo va en `main` sin norma escrita |
| 2026-08-01 | El orquestador NO se convierte en subagente que lo haga todo: sigue en la sesión principal | Comprobado por lectura: ningún agente de `.claude/agents/` lleva la herramienta `Agent` en `tools`, así que un `orquestador` subagente no puede repartir. Y meter la revisión dentro del subagente degradaría la prueba al nivel 3 de la regla 9 de CLAUDE.md (consenso entre agentes), que es el más débil |
| 2026-08-03 | Techo del 20% de motor (regla 8 de CLAUDE.md) suspendido hasta 03.01.05 hecha o 01/09/2026 | CEO ordenó motor antes que producto, incumpliendo regla 8; se suspende con condición de vuelta automática |
| 2026-08-03 | El lunes deja de ser la única ventana de decisión del CEO; lo que esté listo sube el día que lo esté, SIN tope de número; el CEO marca el final del día | D-18: D-13 ya lo decía pero no se propagó; calendario recalculado sin esperar lunes |
| 2026-08-03 | PUERTA G1: un solo mercado, XAUUSD (oro al contado), vela de 4h. DEROGA D-2 | D-19: foco en una cosa hasta probar que una hipótesis gana dinero; el oro está en las 4 cestas admisibles y es el más barato de los 8 |
| 2026-08-03 | Auditorías del ecosistema cerradas; su valor son las ideas construibles aquí, no las piezas instalables | D-20: el criterio de admisión usado descartaba por barato justo lo que el proyecto puede construir |
| 2026-08-03 | Se elimina el trasplante desde gb2 (tarea 01.02.02 y su sección). Lo que haga falta se construye desde cero. DEROGA parcialmente D-6 | D-21: orden del CEO; comprobado pieza a pieza que no se pierde nada vivo |

## Lecciones aprendidas

| ID | Lección | Origen |
|---|---|---|
| L-001 | Si un dato se puede calcular a partir de datos brutos disponibles, se calcula. Buscar el dato ya masticado pierde tiempo y devuelve fuentes flojas | Revisión 02.03.01 |
| L-002 | Toda conversión de unidades se aplica en la tabla final, no solo se explica en una nota al pie | Revisión 02.03.01 |
| L-003 | Medir el coste de entrar y salir sin medir el de mantener da una foto incompleta | Revisión 02.03.01 |
| L-004 | Los valores absolutos no se comparan entre activos distintos: se normalizan antes | Revisión 02.03.01 |
| L-005 | El modelo no aprende: acumula notas escritas. Si nadie escribe bien las notas, no mejora nada | Análisis del vídeo, 29/07 |
| L-006 | Si dos fuentes usan convenciones distintas (yen y franco invertidos), sus números tienen el signo cambiado. Verificar la convención antes de comparar | Revisión Brief B |
| L-007 | Un nombre parecido no es el mismo instrumento: oro al contado ≠ futuro de oro; bitcoin contra Tether ≠ contra dólar | Revisión Brief B |
| L-008 | Un umbral sobre una magnitud inestable necesita varias ventanas, no una | Revisión Brief B |
| L-009 | Un guardia verificado por presencia y no por ejecución da falsa seguridad, que es peor que no tenerlo | Auditoría gb2 |
| L-010 | Los agentes no se activan solos porque tengan buena descripción: se activan si la cola contiene tareas de su tipo y el reparto enruta por tipo | Auditoría gb2 |
| L-011 | Tener una cola estricta no impide la deriva. gb2 la tenía ("trabajo que no está ahí no se ejecuta"), con IDs contiguos forzados por un hook, y aun así el 70% del esfuerzo se fue al motor. La cola controla QUÉ se ejecuta, no QUÉ se mete en la cola | Auditoría gb2 |
| L-012 | Dos agentes de acuerdo no son una prueba. En gb2 hubo tres diagnósticos seguidos del mismo componente, dos falsos; lo que los corrigió fue leer el código y reproducir el fallo, no debatir más | Auditoría gb2 |
| L-013 | Se trabajó una tarea sin ficha escrita antes: 01.01.02 era una fila de una línea sin alcance ni criterio de hecho, y el trabajo de apoyo se autoasignó alcance dentro de ella. La regla 5 de CLAUDE.md vale también para las tareas del CEO | Revisión del cálculo de arrastre (01.01.02) por `critico-codigo`, 01/08 |
| L-014 | Un supuesto expresado en porcentaje decidió el orden de magnitud sin declararse: fijar la actividad como porcentaje de velas operadas producía un multiplicador de coste x60-x69 entre velas que en valor absoluto cae a x4,3; la conclusión "1h es inviable" era un artefacto del supuesto | Revisión de `arrastre_coste.md`, hallado por `critico-codigo` y confirmado con experimento ejecutado por `validador`, 01/08 |
| L-015 | `CLAUDE.md` y este WBS llevan dos listas de «29 reglas» con contenido distinto bajo el mismo número: toda cita `regla N` es ambigua. Resuelto el 01/08/2026 por D-16: la lista normativa es la de `CLAUDE.md`; toda cita se escribe «regla N de CLAUDE.md» | Revisión 01.02.03 |
| L-016 | Un indicador que solo mira lo etiquetado es ciego justo donde importa: medir el reparto producto/motor contando solo commits con código WBS daba 20% cuando el real es 43,8%, porque `commit-msg` exime a `meta:`, `org:` y `arranque:`, que es donde vive el motor | Revisión 01.02.03 |
| L-017 | L-015 citaba mal su propia regla de grep: decía "la regla 20 de CLAUDE.md exige grep previo" cuando esa exigencia es la regla 12 de CLAUDE.md (la 20 es "se guardan todas las pruebas"). LECCIONES.md es de solo-añadir, así que no se corrige en su sitio, se anota aparte | Tarea 03.01.13, pasada 1 (`constructor-motor`), 01/08 |
| L-018 | Un recuento sin `-i` da cifras bajas aunque lo repitan dos agentes: quien ejecutó y quien revisó grepearon "regla" en minúscula y los dos dieron la misma cifra baja (5/3/36 en vez de 12/4/39), porque el error estaba en el método de los dos, no en el dato | Tarea 03.01.13, pasada 2 (`constructor-motor`, ordenada tras el rechazo de la pasada 1), 01/08 |
