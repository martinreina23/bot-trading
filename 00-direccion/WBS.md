# WBS — Bot de Trading Algorítmico (v0.9)

> Fuente de verdad para agentes. El Excel (WBS_Bot_Trading_v0.9.xlsx) es la vista del CEO y se genera de este archivo, nunca al revés.

## Reglas (sin ambigüedad posible)

1. Toda tarea se ejecuta y se anuncia por su código WBS. Prohibidos identificadores opacos (t55).
2. No se inventan tareas: trabajo nuevo = primero se añade aquí con código y motivo. Subtareas dentro de alcance las crea el orquestador; tareas nuevas de primer nivel, solo en revisión semanal.
3. Los códigos son estables: una tarea empezada no se renumera jamás.
4. Se va en orden salvo tareas marcadas paralelas. Una tarea no se cierra sin cumplir su criterio de "hecho".
5. Nadie valida su propio trabajo. Los veredictos de estrategia los firma el Validador, no quien construyó.
6. **Regla de no-ambigüedad:** toda tarea debe poder ejecutarse sin adivinar nada. Si un agente tiene que suponer, la tarea vuelve al orquestador para reescribirse.
7. **Pre-registro:** ninguna variante de estrategia se prueba sin estar registrada antes. Se guardan TODAS las pruebas, también las fallidas.
8. Cada agente usa el modelo asignado en la sección Equipo, y su respaldo si ese modelo falla o rechaza la petición.
9. **Restricción justificada, en dos niveles.** Lo REVERSIBLE (archivos, carpetas, código, pruebas) empieza con permisos amplios: git lo deshace todo, y una restricción solo se añade tras un incidente real, anotada junto al incidente y revisada cada mes. Lo IRREVERSIBLE (dinero real, órdenes al broker, borrar el cajón de datos reservado, gastar dinero nuevo) lleva barrera desde el minuto uno y no se negocia. Manga ancha con lo que se puede deshacer, cero manga con lo que no.
10. **Ficha de decisión del CEO:** nada llega al CEO como "opina sobre esto". Toda decisión llega con: 1 línea de qué se decide · 2-4 opciones cerradas · la recomendada marcada con su motivo · qué pasa con cada opción · respuesta de una letra o un número. Ninguna ficha puede pedirle redactar, buscar o calcular nada. Si no cabe en media pantalla de móvil, vuelve atrás.
11. **Cadencia de entregables:** el WBS en texto se actualiza SIEMPRE que cambie algo (no es negociable). El Excel de vista del CEO se regenera solo para la revisión de los lunes y para las puertas.
12. **Cada tirada autónoma cierra al menos una tarea que avanza el producto.** La infraestructura que no desbloquee mecánicamente una tarea de producto se registra como deuda y no se ejecuta sin permiso del CEO. *(gb2: 70% del esfuerzo al motor, 1 de 13 hipótesis probada, motor congelado dos veces sin frenarlo)*
13. **Toda barrera se verifica por ejecución** —inyectando el caso prohibido y comprobando que se bloquea— antes de documentarla como activa. Sin prueba, se marca "no verificada". Un guardia nunca se da por bueno por estar presente en el código. *(gb2: el aislamiento del sistema nunca funcionó y nadie lo comprobó en meses)*
14. **Los guardias bloquean por defecto** (todo prohibido salvo lista explícita). La condición que activa una exención debe ser un hecho impuesto por el sistema, nunca un dato que elija el vigilado. *(gb2: bastaba escribir "merge:" en el mensaje para saltarse el muro)*
15. **Éxito = código fiel a la especificación, NO estrategia rentable.** Un backtest con mal resultado y código correcto es un éxito registrable. *(vacuna contra tocar parámetros hasta que salga bonito)*
16. **Test de compuerta:** si la justificación de un cambio no se sostiene sin citar métricas de resultado, se deniega.
17. **Registros que solo permiten añadir:** el registro de pruebas y el de decisiones nunca se reescriben; una corrección es una entrada nueva.
18. **Todo dato numérico se calcula sobre datos brutos**, salvo que exista una fuente primaria homogénea demostrable. *(confirmado dos veces: ni el ATR intradía ni la matriz de correlaciones existen publicados)*
19. **La ficha de una tarea se escribe en la cola ANTES de trabajarla**, nunca al cerrarla. Sin ficha, no hay tarea.
20. **Ninguna referencia a una decisión entra en código o informe sin un `grep` previo que la localice.** Solo se cita lo firmado y guardado. *(gb2: 4 citas inventadas dentro del código de producción)*
21. **Se referencia por nombre de símbolo, nunca por número de línea.**
22. **Quien implementa ejecuta y lee su artefacto completo antes de entregar.** Las puertas confirman, no descubren.
23. **Un fallo reportado por un agente no es un fallo verificado:** antes de encolar o reparar, se lee el componente y se reproduce el fallo.
24. **Los datos nunca entran en git.** Se descargan con script y se ignoran de verdad, comprobándolo el día 1. *(gb2: 50.089 ficheros de datos versionados contra su propio .gitignore, 1,4 GB por clon)*
25. **Cada agente lleva el identificador exacto de su modelo, nunca un alias, y ningún agente sin modelo.** *(gb2: 7 de 13 con alias y el firmante sin modelo, contra su propia política)*
26. **Antes de crear un agente se comprueba que el WBS contiene tareas de su tipo.** El reparto enruta por tipo de tarea. Un agente sin tareas durante dos semanas se elimina o se justifica en la revisión del lunes. *(gb2: 3 agentes nunca invocados porque la cola nunca tuvo tareas de su tipo)*
27. **Jerarquía de la prueba (contra el "una IA decide y se equivoca").** Ninguna afirmación se acepta por consenso entre agentes. El orden de fuerza es: (1) **prueba ejecutada** — el fallo se reproduce, el guardia se dispara, el número se recalcula: esto cierra el asunto; (2) **verificación documental** — `grep` que localiza la cita por fichero y línea; (3) **contraste entre dos agentes con papeles opuestos** — solo cuando (1) y (2) no son posibles, y el resultado se marca como *no probado*. Dos agentes de acuerdo no son una prueba: en gb2 hubo tres diagnósticos consecutivos del mismo componente, **dos de ellos falsos**, y lo que los corrigió no fue debatir más, fue leer el código y reproducir el fallo.
28. **Quien discrepa aporta el experimento que zanjaría la discusión**, no otro argumento. Si no existe experimento posible, la decisión sube al CEO marcada como *no probada*.
29. Estados: `pendiente | en_curso | hecha | bloqueada`.

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

**Llega al CEO como excepción inmediata (se para hasta respuesta):** gasto nuevo (datos de pago, VPS, broker, créditos extra) · cualquier cosa con dinero real · bloqueo de más de 24 h · 3 vueltas del bucle de hipótesis sin éxito.

**Llega al CEO solo en una puerta:** cambiar de mercado, de tamaño de vela o de planteamiento.

## Fase 01 — ARRANQUE (puerta G0)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 01.01.01 | Aprobar plan y reglas | CEO | — | en_curso |
| 01.01.02 | Aprobar criterios de la puerta G1 | CEO | 01.01.01 | pendiente |
| 01.01.03 | Fijar límites: fecha tope, horas CEO/semana, pérdida máxima futura | CEO | 01.01.01 | pendiente |
| 01.02.01 | Analizar gb2 como información (no copia) | Crítico | 01.01.01 | **hecha** 30/07 — `INFORME_GB2.md` |
| 01.02.02 | **Trasplante pieza a pieza desde gb2** (D6=B). Una tarea por pieza, cada una con su criterio de aceptación (ver sección Trasplante). Ninguna entra sin pasar su prueba ejecutada | Crítico + Constructores | 03.01.01 | pendiente |
| 01.02.03 | Auditar el catálogo `awesome-claude-code` y proponer máximo 4 piezas concretas para el motor, con motivo y coste de integración. **Carril de motor: cuenta contra el 20%** y se limita a 1 tirada | Investigador | 03.01.02 | pendiente |

## Fase 02 — ELEGIR MERCADO Y TAMAÑO DE VELA (puerta G1)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 02.01.01 | Confirmar 8 candidatos: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD, BTC, ETH | CEO + Orquestador | 01.01.02 | pendiente — los 8 candidatos ya se usan de hecho en 02.02.04 (hecha) y en los briefs A y B; falta ratificación formal del CEO en G1 |
| 02.01.02 | Costes típicos de operar por mercado (PROVISIONAL hasta 04.01.02) | Investigador | 02.01.01 | FICHA (31/07): **Alcance:** tabla FINAL de coste de entrar y salir (spread + comision) para los 8 instrumentos, en la unidad natural de cada uno, ida y vuelta. **Base ya existente:** la Entrega 1 del Brief A (`entrega_brief_A.md`), ACEPTADA por el revisor con fuentes primarias (PDF oficiales de Pepperstone e IC Markets). No se rehace la investigacion: se consolida. **Correcciones OBLIGATORIAS, aplicadas EN LA TABLA y no en nota al pie (L-002):** USDJPY = 1,16 pips (no 0,90) y USDCHF = 0,73 pips (no 0,80); ambas ya calculadas en `revision_brief_A.md`, el analista las explico pero no las aplico. **Criterio de hecho:** 8 filas con coste total ida y vuelta, tipo de cuenta declarado (raw/ECN vs spread-only, que no son comparables entre si), y fuente con fecha por celda. Lo que no tenga fuente se declara hueco, no se estima. **PROVISIONAL:** lo sustituye 04.01.02 con precios del broker real una vez elegido. **Es el otro insumo de 02.02.02**, que sin esto sigue bloqueada. — **hecha** 31/07 — `coste_operar.md`. Tabla final de coste de entrar y salir, 8 instrumentos, ida y vuelta, con tipo de cuenta declarado (raw/ECN vs spread-only, que no son comparables entre si). CORRECCIONES DE L-002 APLICADAS EN LA TABLA y no en nota al pie: USDJPY 1,16 pips (no 0,90) y USDCHF 0,73 pips (no 0,80). VERIFICADO por el orquestador: aritmetica de las 8 filas recalculada (spread + comision = total, cuadran las 6 con comision); las cifras citadas existen en el origen, localizadas por grep. RECORRIDO: primera entrega DEVUELTA por incumplir la regla 21 (seis citas por numero de linea, que se rompen solas al editar el origen); corregida a referencias por seccion y fila de tabla, verificado que no queda ninguna y que no se movio ningun numero. BTCUSD y ETHUSD llevan dos cifras de dos documentos con fechas distintas, presentadas ambas sin promediar. PROVISIONAL: lo sustituye 04.01.02 con precios del broker real tras G1. |
| 02.02.01 | **CORREGIDA 29/07:** descargar precios y CALCULAR el ATR de 15m, 1h y 4h (no buscarlo publicado: no existe). Script `atr_local.py` | Constructor de datos | 02.01.01 | FICHA (31/07): **Fuente fijada:** HistData para EURUSD, GBPUSD, USDJPY, AUDUSD y USDCHF · Dukascopy para XAUUSD **al contado** (NO el futuro GC=F, ver L-007) · Kraken para BTCUSD y ETHUSD **contra dolar real, no contra Tether** (L-007). Se jubila Yahoo/yfinance. **Alcance:** descargar historico suficiente para 2 años completos y calcular ATR(14) en velas de 15m, 1h y 4h para los 8 instrumentos. **Corte:** 22:00 UTC, unico para todos. **Artefacto:** un solo script que sirva tambien a 02.02.03 (T2 avisa: en gb2 la logica duplicada divergio). Salida en `02-datos/bruto/` (que git ignora) y resultados en JSON. **Criterio de hecho:** existe la tabla 8 instrumentos x 3 velas con ATR calculado sobre precios descargados, sin celdas estimadas; cada celda declara fuente, periodo y numero de velas usadas; el script se ha ejecutado entero y su salida esta leida. **Prueba de cordura obligatoria:** el oro debe salir en cientos o miles de dolares por onza, no en decenas (en gb2 un divisor mal puesto lo dejo en 17 $/onza). **Lo que NO entra:** estimaciones por raiz-del-tiempo; si un dato no se puede calcular, se declara hueco. — **hecha** 31/07 — `precios_mercado.py`, `atr_15m_1h_4h.json`, `atr_real_15m_1h_4h.md`. Tabla de 8 instrumentos x 3 velas, 24/24 celdas calculadas sobre precios descargados, 0 estimadas, 0 duplicados, 0 velas invalidas. Cordura del oro OK: 3.596,64 USD/oz, en miles. RECORRIDO: entregada, RECHAZADA por `critico-codigo` (bin incompleto contado como completo, en el filtro de ventana y en el primer bin de 4h de los 8 instrumentos), reparada en ronda 1, re-revisada y ACEPTADA. El critico recalculo el ATR desde los datos brutos con su propio codigo y coincide digito a digito con el script (XAUUSD 1h = 14.464676282400184, n=11824); verifico ademas que el descarte de bins de borde NO se come huecos legitimos (801 bins de fin de semana en EURUSD y 643 de la pausa del oro, ninguno recortado). HALLAZGO ADICIONAL del critico, resuelto en un remate: las cifras de cripto no eran reproducibles por dos causas — la vela en formacion (las 721 eran 720 cerradas + 1 abierta) y la ventana deslizante de Kraken. La primera se corrigio descartandola por el cursor `last` de la API; la segunda NO tiene arreglo contra el endpoint publico y queda DECLARADA: las 24 celdas del JSON llevan campo `reproducible` (18 true, 6 false con su motivo), y el informe declara que esas 6 celdas no pueden entrar en el testbed de invarianza de 03.01.10 sin congelar antes los datos. LIMITE CONOCIDO: BTCUSD y ETHUSD cubren 720 velas (7,4 / 30 / 120 dias), no 2 años; decision del CEO pendiente sobre bajar el volcado historico de Kraken. NIVEL DE ESCRUTINIO, para que conste: el motor y la reparacion los verifico `critico-codigo` por recalculo independiente; el remate de cripto lo verifico el orquestador por ejecucion (720 velas, 18 celdas no-cripto intactas digito a digito, 24/24 marcadas), sin una tercera pasada del critico. |
| 02.02.02 | Coste relativo: coste ÷ movimiento medio, en % (el número clave). Coste de USDJPY corregido a 1,16 pips | Constructor de datos | 02.01.02, 02.02.01 | bloqueada — depende de 02.01.02 (pendiente) y de 02.02.01 (sin ejecutar). El coste de USDJPY corregido a 1,16 pips viene de revision_brief_A.md |
| 02.02.03 | **CORREGIDA 30/07:** CALCULAR la matriz de correlaciones en 3 ventanas (3 meses, 1 año, 2 años) con hora de corte única (22:00 UTC) y en la vela elegida, no solo diaria. No existe publicada de forma homogénea | Constructor de datos | 02.01.01 | en_curso — FICHA (31/07): **Alcance:** matriz de correlaciones 8x8 sobre RENDIMIENTOS logaritmicos (nunca sobre precios), en 3 ventanas (3 meses, 1 año, 2 años) y en LAS TRES VELAS (15m, 1h, 4h), mas la diaria como comprobacion. **Por que las tres velas:** la ficha original decia "en la vela elegida", pero la vela se elige en G1, que es despues; calcular las tres evita adivinar (regla 6) y deja a la puerta el dato elija la que elija. **Corte:** 22:00 UTC unico, imprescindible o los rendimientos no coinciden entre clases de activo. **Artefacto:** reutilizar `precios_mercado.py`, sin duplicar logica (T2). **Criterio de hecho:** una matriz 8x8 por cada combinacion ventana x vela, cada celda con su n de observaciones; ninguna celda estimada. **Prueba de cordura obligatoria:** EURUSD/USDCHF debe salir fuertemente NEGATIVO (el brief da -0,97). Si sale positivo hay error de signo o de convencion: parar y avisar (L-006). **Hueco conocido a declarar, no rellenar:** BTCUSD y ETHUSD solo tienen 720 velas, asi que la ventana de 2 años NO EXISTE para ellas; se declara hueco. **Sirve al criterio 4 de G1:** correlacion que no supere 0,7 en ninguna de las tres ventanas. |
| 02.02.04 | Historial disponible: años, fuente, coste | Investigador | 02.01.01 | **hecha** — Dukascopy (tick desde 2003, forex y oro al contado), HistData, TrueFX, Binance, Kraken. Todo gratis, muy por encima de los 5 años exigidos |
| 02.02.05 | **NUEVA:** coste de mantener posición de un día para otro (swap/financiación) en los 8 instrumentos, 2-3 brokers. En cripto CFD puede superar varias veces al spread | Investigador | 02.01.01 | **hecha** 31/07 — `coste_swap.md`. Coste de mantener posicion en 8 instrumentos x 3 brokers (OANDA, XTB, Pepperstone), largo y corto por separado, en % anual y $/dia sobre 100.000 USD. VERIFICADO por recalculo independiente: las 30 celdas con % y $/dia cuadran; signos de USDJPY y USDCHF coherentes entre brokers (L-006 comprobada, sin inversion de convencion). HALLAZGO PARA G1: mantener cripto cuesta -33,6% anual (OANDA) y -22,5% (Pepperstone), entre 20 y 30 veces mas que entrar y salir; el oro -6,6%/-8,2%; y USDCHF y USDJPY en largo PAGAN (+2,6% y +1,6%). Implicacion: si entra cripto en el portafolio, la estrategia no puede aguantar posiciones de un dia para otro. HUECO DECLARADO: ETHUSD queda con una sola fuente fiable (XTB lo ofrece al contado, no CFD; Pepperstone no publica cifra de ETH), por debajo del minimo de dos fuentes independientes. |
| 02.03.01 | Revisión independiente de método, fuentes y números | Orquestador | 02.02.* | en_curso — revisados Brief A (revision_brief_A.md, 29/07) y Brief B (revision_brief_B.md, 30/07). No se cierra hasta que 02.02.* entreguen números. ("parcial" no era un estado legal) |
| 02.03.02 | Informe de decisión: 3-5 mercados poco correlacionados + 1-2 velas | Orquestador | 02.03.01 | pendiente |
| 02.03.03 | PUERTA G1: el CEO elige | CEO | 02.03.02 | pendiente |

## Fase 03 — MONTAR LA CASA (Claude Code) — EN PARALELO con la Fase 02

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 03.01.01 | Repositorio: carpetas, WBS texto, CLAUDE.md, DECISIONES.md, LECCIONES.md | Constructores | 01.01.01 | **hecha** 30/07 — repo completo: carpetas, WBS, CLAUDE.md, DECISIONES.md, LECCIONES.md, plantillas y .gitignore (42 ficheros en git). AVISO regla 24 **NO VERIFICADA**: la prueba de inyección de datos no se ha ejecutado; 02-datos/ está vacío. Se ejecuta al bajar los primeros precios en 02.02.01 |
| 03.01.02 | Crear TODOS los agentes del Equipo, cada uno con su modelo y descripción sin ambigüedad; prueba de activación de todos (ningún agente fantasma) | Constructores | 03.01.01, 01.02.01 | **hecha** 30/07 — 8 agentes en .claude/agents/, cada uno con identificador exacto de modelo y respaldo. Prueba de activación ejecutada 30/07: los 8 respondieron y leyeron un fichero real, ningún fantasma. LÍMITE: la prueba no demuestra que el modelo enrutado sea el de la ficha; se verifica en 03.01.04, con atención a claude-fable-5 (validador y arquitecto) |
| 03.01.03 | Ejecución desatendida: arranques programados, permisos AMPLIOS por defecto (git como red de seguridad) y topes de gasto | Constructores | 03.01.02 | pendiente |
| 03.01.04 | Plan de respaldo de modelos: si un modelo no está disponible o rechaza, el agente sigue con su respaldo y lo anota | Constructores | 03.01.02 | pendiente |
| 03.01.05 | PRUEBA REAL DEL MOTOR: un día entero de trabajo desatendido de verdad antes de dar la fase por buena | Orquestador | 03.01.03, 03.01.04 | pendiente |
| 03.01.06 | Plantilla y automatismo de fichas de decisión: el secretario prepara cada decisión del CEO en el formato obligatorio y la adjunta al informe semanal | Secretario | 03.01.02 | pendiente |
| 03.01.07 | Cola de aprobación del CEO: tabla con desplegable Aprobado / Saltar / Corregir y columna de corrección. Lo aprobado se ejecuta solo; lo corregido se rehace Y la corrección se guarda en LECCIONES.md | Secretario | 03.01.06 | pendiente |
| 03.01.08 | **Prueba de fuego de las barreras** (regla 13): inyectar cada caso prohibido —leer el cajón reservado, escribir fuera del proyecto, borrar datos, gastar dinero— y comprobar que se bloquea de verdad. Lo que no se bloquee se marca "no verificada" | Crítico | 03.01.03 | en_curso — ejecutada la primera pasada 31/07 con verificar_barreras.py: 4 barreras de 5 VERIFICADAS por ejecucion (hooks instalados, datos rechazados en commit, .gitignore ignora 02-datos, mensaje exige codigo WBS). 1 NO VERIFICADA: el cajon reservado era un filtro de texto sobre el comando. Se remedia en 03.01.11 (D-10). No se cierra hasta repetir la pasada con 03.01.11 terminada |
| 03.01.09 | Enrutado por tipo de tarea y comprobación de que el WBS genera tareas de cada tipo de agente (regla 26) | Constructores | 03.01.02 | pendiente |
| 03.01.10 | Testbed sintético de invarianza: resultado de referencia fijo que debe reproducirse tras cualquier cambio del motor | Constructores | 03.01.01 | pendiente |
| 03.01.11 | **NUEVA 31/07 (D-10):** guardia del cajon reservado por cifrado. Script `cajon_reservado.py`: la contraseña solo la tiene el CEO, no se guarda, se pide en cada operacion y nada se descifra a disco | Constructores | 03.01.08 | en_curso — script escrito y probado por ejecucion 31/07: 6 de 6 casos prohibidos bloqueados (contraseña por tuberia, abrir sin declarar variante, lectura a pelo del fichero cifrado, contraseña incorrecta, y ninguna orden de terminal vuelca datos en claro). FALTA: que el CEO ejecute `sellar` en una terminal real para fijar la contraseña |

## Fase 04 — HIPÓTESIS Y VALIDACIÓN (puerta G2)

### 04.01 Broker y cajones de datos
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.01.01 | Comparar 3-4 brokers del mercado elegido; elegir uno y abrir demo (CEO firma) | CEO + Orquestador | 02.03.03 | pendiente |
| 04.01.02 | Recalcular costes con precios reales del broker (sustituye 02.01.02) | Constructor datos | 04.01.01 | pendiente |
| 04.01.03 | Histórico limpio partido en 3 cajones: construir (train), ajustar (validación) y RESERVADO bajo llave (OOS, se abre una sola vez por variante). Ningún agente toca el reservado | Constructor datos | 04.01.01 | pendiente |

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
| 04.03.01 | Backtest con costes reales sobre el cajón de construir | Constructores | 04.01.03, 04.02.04 | pendiente |
| 04.03.02 | Ajuste SOLO con el cajón de validación; lo que no aguanta, muere aquí | Constructores | 04.03.01 | pendiente |
| 04.03.03 | Prueba de fuego: UNA sola pasada por variante sobre el cajón reservado (OOS). Repetir sería hacerse trampa | Validador | 04.03.02 | pendiente |
| 04.03.04 | Robustez: Monte Carlo (barajar el orden de operaciones y meter pequeños cambios miles de veces: ¿aguanta o era suerte?) + walk-forward (repetir el ajuste avanzando en el tiempo) | Validador | 04.03.03 | pendiente |
| 04.03.05 | Veredicto pasa/no pasa por variante, con los criterios de G2. Quien construyó no vota | Validador | 04.03.04 | pendiente |

### 04.04 Decisión y bucle
| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 04.04.01 | Informe de la vuelta: qué pasó, qué murió y por qué. Registro de TODAS las pruebas, también fallidas | Secretario | 04.03.05 | pendiente |
| 04.04.02 | Si ninguna pasa: volver a 04.02 con lecciones (vuelta 2, 3…). Tras la 3ª vuelta sin éxito: revisión completa del planteamiento con el CEO | Orquestador | 04.04.01 | pendiente |
| 04.04.03 | PUERTA G2: el CEO decide qué pasa a demo | CEO | 04.04.01 | pendiente |

## Fase 05 — DEMO (puerta G3) — se detalla al cerrar G2

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 05.01.01 | Bot en demo, solo y con guardias automáticos | Constructores | 04.04.03 | pendiente |
| 05.01.02 | Seguimiento semanal real vs. prometido (8-12 semanas) | Secretario | 05.01.01 | pendiente |
| 05.01.03 | PUERTA G3: CEO decide dinero, cuánto y pérdida máxima | CEO | 05.01.02 | pendiente |

## Fase 06 — REAL (puerta G4) — se detalla al cerrar G3

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 06.01.01 | Dinero pequeño respetando los límites de 01.01.03 | Constructores | 05.01.03 | pendiente |
| 06.01.02 | PUERTA G4 mensual: seguir, ampliar o parar. Si pierde más de lo escrito, se para sin discusión | CEO | 06.01.01 | pendiente |

## Fase 07 — MOTOR Y ORDEN (paralela; máx. 20% del esfuerzo semanal)

| Código | Tarea | Responsable | Depende de | Estado |
|---|---|---|---|---|
| 07.01.01 | Carpetas y documentos en orden; una fuente de verdad por tema; lo sustituido se borra | Constructores | 03.01.01 | pendiente |
| 07.01.02 | Mejoras del motor: SOLO tareas aprobadas en revisión semanal (el motor no manda) | Constructores | 03.01.02 | pendiente |


## Calendario del mes (29 julio → 1 septiembre 2026)

**Objetivo del mes:** NO es tener el bot en demo. Es llegar al 1 de septiembre con respuesta a "¿existe alguna estrategia que merezca pasar a demo?".

| Semana | Fechas | Qué se hace | Hecho al final | Lunes del CEO (1 h) |
|---|---|---|---|---|
| S1 | 29 jul – 4 ago | Fase 02 completa + 01.02.01 (gb2) + 03.01.01 (repo), en paralelo | Mercado y vela elegidos (G1) | Lun 3: leer informe G1 y elegir |
| S2 | 5 – 11 ago | 03.01.02 a 03.01.06 + 04.01.01 (broker) | Motor solo 24 h sin caerse + broker | Lun 10: firmar broker |
| S3 | 12 – 18 ago | 04.01.02, 04.01.03 + 04.02.01 a 04.02.04 | 3-5 hipótesis con variantes pre-registradas | Lun 17: ver hipótesis |
| S4 | 19 – 25 ago | 04.03.01, 04.03.02 | Variantes supervivientes tras ajuste | Lun 24: cuántas siguen vivas |
| S5 | 26 ago – 1 sept | 04.03.03 a 04.03.05 + 04.04.01 | Veredicto pasa/no pasa por variante | Lun 31: preparar evaluación |
| **GM** | **1 sept** | **Puerta del mes con el CEO** | Arrancar demo / otra vuelta / replantear | Mar 1: la reunión |

**Lo que NO cabe en el mes:** la demo (8-12 semanas de mercado real, reloj no acelerable) · las 3 vueltas del bucle (cabe una y media) · el dinero real.

## Límites del CEO (decisión 29/07/2026)

- Horizonte: 1 mes. Evaluación el 1 de septiembre (puerta GM).
- Tiempo del CEO: 1 hora, lunes.
- Dinero real (pendiente de confirmar, ficha D5): capital 1.000-2.000 €, parada dura propuesta en -25%. Nota: el CEO mencionó tolerar caídas del 50-60%, incompatible con parar en -25%; recuperarse de -25% exige +33%, de -50% exige +100% y de -60% exige +150%.

## Puertas

- **G0** (en curso): CEO aprueba plan, criterios y límites (01.01.01–03).
- **G1** (criterios corregidos 30/07): coste de entrar y salir ≤10-15% del movimiento medio de vela **y** coste de mantener posición medido aparte · cientos de operaciones posibles · datos suficientes (deja de discriminar: hay 20+ años gratis para todos) · **correlación que no supere 0,7 en ninguna de las tres ventanas** (3 meses, 1 año, 2 años), medida en la vela elegida y con hora de corte única · operable sin nadie delante. Aviso: parte de la correlación entre pares de divisas es aritmética por compartir el dólar (EURUSD/USDCHF: -0,97), así que 5 pares de forex no son 5 apuestas.
- **G2**: solo pasan variantes que ganan después de costes en OOS, aguantan Monte Carlo y estaban pre-registradas. Veredicto del Validador.
- **G3**: demo de 8-12 semanas parecida a lo prometido; CEO fija dinero y pérdida máxima.
- **G4** (mensual): si pierde más de lo escrito en 01.01.03, se para.
- **GM** (1 de septiembre de 2026): puerta de evaluación del primer mes. Decisión: arrancar demo, dar otra vuelta al bucle o replantear.

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
| 2026-07-29 | Formato obligatorio de ficha de decisión del CEO (regla 10 + plantilla) | Reducir al mínimo el tiempo del CEO: ni redactar, ni buscar, ni calcular |
| 2026-07-29 | D1 resuelta: se fija AHORA qué se mide (misma vara para los 8) y se calibran los umbrales en G1 con los números delante | El CEO no quiere cortes a ciegas; sin vara común, cada mercado se mediría distinto |
| 2026-07-29 | Guardarraíles en dos niveles: reversible permisivo, irreversible con barrera desde el minuto uno | Matiz de un vídeo analizado el 29/07 |
| 2026-07-29 | Cola de aprobación con Aprobado / Saltar / Corregir; toda corrección escrita va a LECCIONES.md | El valor está en que la corrección quede guardada |
| 2026-07-29 | 02.02.01 pasa de "buscar ATR publicado" a "calcular ATR sobre precios reales" | El dato no existe publicado; sí existen los precios (L-001) |
| 2026-07-29 | Se añade el swap/financiación como segundo componente del coste (02.02.05 y criterio 1 de G1) | En CFD de bitcoin la financiación (-22,5% anual) supera al spread si se mantiene la posición |
| 2026-07-29 | El Excel se regenera solo los lunes y en las puertas; el WBS en texto, siempre | Decisión del CEO: no necesita la vista cada vez |
| 2026-07-30 | **D6 = B.** Repositorio nuevo con reglas y agentes desde cero; se trasplantan 5 piezas de gb2, una a una, cada una con criterio de aceptación probado aquí | Decisión del CEO. Reescribir motor y datos se comería el mes sin acercar la respuesta |
| 2026-07-30 | Jerarquía de la prueba: ejecución > verificación documental > contraste entre agentes. El consenso entre agentes no cierra nada | Petición del CEO ("miedo a que una IA decida y no tenga razón") + evidencia de gb2 |
| 2026-07-30 | El análisis del catálogo `awesome-claude-code` es trabajo de motor: entra en el carril del 20% y se limita a 1 tirada con máximo 4 propuestas | Aplicación de la regla 12 a una petición del propio CEO |

## Trasplante desde gb2 — criterios de aceptación (D6 = B, decidido 30/07/2026)

Regla que los gobierna a todos: **ninguna pieza entra por ser buena en gb2. Entra si pasa su prueba, ejecutada aquí.** Una tarea por pieza, revisada por el crítico, que no puede ser quien la trasplanta.

| Pieza | Qué se trae | Criterio de aceptación (prueba ejecutada) | Qué se descarta de ella |
|---|---|---|---|
| **T1 — Dataset histórico** | Precios validados 2015-2022 | Se recalcula la cobertura, los duplicados y los spreads negativos AQUÍ, sin fiarse del informe. Prueba de cordura de precio: el oro debe estar en cientos/miles, no en decenas *(en gb2 un divisor mal puesto lo puso a 17 $/onza)* | Todo lo que esté versionado en git: los datos se descargan, no se clonan (regla 24) |
| **T2 — Motor de backtest** | Costes reales nativos: entrada al precio de compra y salida al de venta, stops sin mejora de precio, financiación asimétrica con triple miércoles, dimensionado | Se ejecuta con un caso hecho a mano cuyo resultado se calcula con lápiz y papel; si no coincide, no entra. Además se prueba que un stop nunca ejecuta a mejor precio del disparado | Los drivers duplicados (`scripts/backtest_f03*.py`): en gb2 la lógica vivía en dos sitios con riesgo de divergencia |
| **T3 — Testbed de invarianza** | Prueba sintética con resultado de referencia fijo | Se corre dos veces y da el mismo número; se altera el motor a propósito y **debe** cambiar. Un testbed que no detecta un cambio inducido no sirve | El número de referencia de gb2: se genera uno nuevo aquí |
| **T4 — Guardias de datos reservados** | Bloqueo de acceso al cajón OOS | Se intenta leer el cajón reservado por tres vías distintas (agente, script, terminal) y las tres deben bloquearse (regla 13). En gb2 estos sí mordían | Los guardias que el propio informe señala como muertos o mal cableados |
| **T5 — Especificaciones e informes de las 13 hipótesis** | Material de partida para la fase 04 | Ninguno: es material de lectura, no código. **Advertencia obligatoria: 12 de las 13 nunca se probaron.** Entran como hipótesis candidatas, no como conocimiento validado | Cualquier conclusión sobre su calidad: no la hay |

**NO se trae:** la configuración de agentes, la cola de tareas, el historial de git, los ficheros de estado, los encadenadores de sesión ni ninguna documentación de gb2 como norma. Las lecciones ya están extraídas en las reglas 12 a 26.

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
