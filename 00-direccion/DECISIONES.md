# Registro de decisiones

**Solo se AÑADE. Nunca se reescribe una entrada.** Una correccion es una entrada nueva que cita a la
anterior. Regla 21 de CLAUDE.md.

Formato: `## D-N · AAAA-MM-DD · [decision en una linea]` + Motivo + Quien decide + Que bloqueaba.

---

## D-1 · 2026-07-29 · Producto antes que motor; el motor en paralelo con techo del 20%
**Motivo:** en el proyecto anterior el 70% del esfuerzo se fue al motor y se probo 1 de 13 hipotesis.
**Decide:** CEO.

## D-2 · 2026-07-29 · Portafolio de 3-5 mercados poco correlacionados, no un solo par
**Motivo:** repartir riesgo y ganar muestra de operaciones.
**Decide:** CEO.

## D-3 · 2026-07-29 · Mercado y tamaño de vela se deciden en la puerta G1 con datos, no de antemano
**Motivo:** evitar decisiones por corazonada.
**Decide:** CEO.

## D-4 · 2026-07-29 · El CEO revisa una hora los lunes y decide en las puertas; no firma tareas
**Motivo:** direccion por excepcion.
**Decide:** CEO.

## D-5 · 2026-07-29 · Horizonte de 1 mes con evaluacion el 1 de septiembre de 2026 (puerta GM)
**Motivo:** obligar a mirar los numeros pronto. NO es fecha de demo: el objetivo del mes es tener
veredicto sobre si existe una estrategia que merezca ir a demo.
**Decide:** CEO.

## D-6 · 2026-07-30 · Repositorio nuevo con trasplante de 5 piezas verificadas de gb2
**Motivo:** reescribir motor y datos desde cero se comeria el mes sin acercar la respuesta. Lo que
fallaba en gb2 no era el motor, era la capa de gestion, que no se hereda.
**Decide:** CEO. **Condicion:** cada pieza pasa su criterio de aceptacion, ejecutado aqui.

## D-7 · 2026-07-30 · Jerarquia de la prueba: ejecucion > verificacion documental > contraste entre agentes
**Motivo:** el consenso entre agentes no es prueba. En gb2 hubo tres diagnosticos seguidos del mismo
componente, dos falsos; los corrigio leer el codigo y reproducir el fallo, no debatir mas.
**Decide:** CEO.

## D-8 · 2026-07-30 · Cada agente lleva identificador exacto de modelo; ningun alias, ningun agente sin modelo
**Motivo:** en gb2, 7 de 13 agentes usaban alias contra su propia politica, y el agente que firmaba
decisiones no tenia modelo asignado.
**Decide:** direccion tecnica.

## D-9 · 2026-07-30 · Los datos nunca entran en git
**Motivo:** gb2 versiono 50.089 ficheros de datos (1,4 GB por clon) contra su propio .gitignore.
**Decide:** direccion tecnica.

## D-10 · 2026-07-31 · El cajon reservado se protege cifrandolo con una contraseña que solo tiene el CEO
**Motivo:** el 31/07 `verificar_barreras.py` demostro POR EJECUCION que el guardia anterior era un filtro sobre el TEXTO del comando: un comando que nombraba la ruta se bloqueaba, pero un programa que la construia por dentro entraba sin obstaculo. La condicion que activaba la exencion la elegia el vigilado, que es justo lo que prohibe la regla 26. Cifrar convierte el bloqueo en un hecho matematico que no depende de la buena voluntad de ningun agente.
**Decide:** CEO. **Condicion:** la contraseña no se guarda en ningun sitio (ni fichero, ni variable de entorno, ni sesion); cada operacion la vuelve a pedir; nada se descifra a disco; el cajon se queda dentro del proyecto. Toda apertura queda anotada en `04-resultados/registro-cajon.md`.
**Que bloqueaba:** 04.01.03 (partir el historico en tres cajones) y, detras, toda la puerta G2.

## D-11 · 2026-08-01 · Siete criterios de G1 aprobados (G1-C1 a G1-C7)
**Motivo:** definicion de la barra de elegibilidad de mercados y vela. **G1-C1** presupuesto de coste TOTAL al año ≤5% del capital, formula compuesta, con el coste de mantener DENTRO de ese mismo 5% (no aparte); anclado en la regla publicada de Robert Carver ("no gastar mas de un tercio del retorno esperado en costes") con retorno objetivo del 15% anual, que ES UN SUPUESTO ELEGIDO POR EL ORQUESTADOR Y APROBADO POR EL CEO, NO UN DATO MEDIDO. **G1-C2** coste de ida y vuelta ÷ ATR de la vela tranquila (percentil 10) ≤10%. **G1-C3** coste de mantener, sin umbral propio, suma dentro de G1-C1. **G1-C4** minimo 1.000 velas/año en la vela elegida, sin minimo de operaciones (ninguna fuente primaria lo respalda). **G1-C5** correlacion ≤0,7 entre los elegidos en las tres ventanas (3 meses, 1 año, 2 años), filtra la CESTA y no instrumentos sueltos. **G1-C6** tamaño minimo operable con capital de 1.000-2.000 €, medido con ATR MEDIANA, que no elimina instrumentos sino que impone requisito al broker de 04.01.01. **G1-C7** criterio nuevo del hueco de fin de semana: percentil 90 del salto del lunes ÷ stop de 1xATR ≤0,5, que no cumple ningun instrumento. Recorrido: constructor-datos, investigador, critico-codigo y validador; la propuesta del orquestador fue corregida en cuatro puntos por el critico y el validador antes de llegar al CEO. Lo que SALE de G1: "operable sin nadie delante", que pasa a la Fase 03. Hueco declarado: el deslizamiento, sin factor publicado, se mide con precios del broker real en la tarea 04.01.02 y obliga a re-verificar G1 si algun resultado cambia.
**Decide:** CEO.
**Que bloqueaba:** 02.03.01 (revision transversal, RECHAZA 31/07 por criterios sin numerar ni aprobar) y puerta G1 completa.

## D-12 · 2026-08-01 · Fecha tope el 01/12/2026, con revision de avance el dia 1 de cada mes
**Motivo:** D-5 fijaba la evaluacion GM del 01/09/2026 pero NO fijaba ninguna fecha de parada, y las
tres salidas de GM (arrancar demo, dar otra vuelta, replantear) tampoco cerraban el proyecto: no
existia fecha tope en ningun documento. Sin fecha de parada el proyecto puede derivar
indefinidamente, que es lo que ocurrio en gb2.
**Forma operativa:** revision de avance el dia 1 de cada mes (01/09 = GM, 01/10, 01/11), cada una
con poder explicito de PARAR el proyecto ademas de las tres salidas que GM ya tenia. La pregunta de
cada revision la fija el CEO: "¿avanza por buen camino?". El 01/12/2026 es fecha tope dura: si a esa
fecha no hay ninguna estrategia en demo, el proyecto se cierra y se escribe el informe de por que.
**Decide:** CEO (opcion B de la ficha, con el seguimiento mensual añadido por el CEO).
**Que bloqueaba:** cierre de 01.01.03 y puerta G0.
**Consecuencia:** GM gana una cuarta salida explicita (parar) y el proyecto gana una fecha tope que
antes no existia. No toca G4, que sigue siendo la puerta mensual de la fase de dinero real.

## D-13 · 2026-08-01 · Tope de 5 fichas por revision del lunes; la hora es minimo garantizado, no techo
**Motivo:** D-4 fija 1 h los lunes, pero lo que se desborda no es el tiempo sino el numero de
decisiones acumuladas: cerrar solo la tarea 01.01.03 genero 3 fichas en un dia.
**Forma operativa:** maximo 5 fichas de decision por revision del lunes; si hay mas, el orquestador
prioriza y las sobrantes esperan al lunes siguiente. El CEO declara que ademas sigue el proyecto dia
a dia y que pasar de la hora no le supone problema: la hora del lunes es un MINIMO GARANTIZADO, no
un techo.
**Decide:** CEO (opcion B de la ficha, con la aclaracion del CEO de que la hora no es techo).
**Que bloqueaba:** cierre de 01.01.03 y puerta G0.
**Aviso registrado:** el modelo de autonomia de CLAUDE.md esta construido sobre un CEO escaso. Con
un CEO disponible a diario el riesgo deja de ser su tiempo y pasa a ser que el equipo consulte en
vez de decidir. Se mantiene SIN CAMBIO la lista de lo que el equipo cierra sin consultar: que el CEO
este disponible no amplia lo que se le puede preguntar.

## D-14 · 2026-08-01 · Dinero real: aviso a -25% y parada dura automatica a -30% del capital inicial
**Motivo:** el WBS registraba una contradiccion viva sin resolver — parada dura propuesta en -25%
frente a una tolerancia del 50-60% mencionada por el CEO. El CEO fija el nivel entre el 25% y el 30%
y pide explicitamente que no se pare solo, porque una estrategia puede bajar y recuperar. Eso obliga
a DOS niveles, no a uno.
**Forma operativa:** (1) AVISO a -25% del capital inicial ingresado: NO para nada, se reporta al CEO
y decide el CEO. (2) PARADA DURA a -30% del capital inicial: el bot deja de abrir posiciones,
automaticamente y sin exencion activable desde dentro (regla 26). Se mide sobre el CAPITAL INICIAL
INGRESADO, no sobre el maximo alcanzado. Recuperar desde -30% exige +43%.
**Decide:** CEO (opcion A de la ficha refinada). SIN recomendacion del equipo:
`.claude/commands/ficha.md` prohibe recomendar en decisiones de tolerancia al riesgo.
**Que bloqueaba:** cierre de 01.01.03 y puerta G0. Da numero a G4, que hasta hoy decia "si pierde
mas de lo escrito en 01.01.03" sin que existiera nada escrito.
**Requisito tecnico que genera:** la parada dura la aplica EL BOT de forma continua, no la revision
mensual. Comprobada una vez al mes, una caida del -30% puede ser del -45% cuando alguien mire. Pasa
a ser requisito de 05.01.01 y 06.01.01, y se verifica por inyeccion antes de declararla activa
(regla 25).
**Declarado como NO resuelto:** el CEO declara que su tolerancia real llega mas abajo ("mientras no
pierda la cuenta entera"). La parada de -30% NO refleja esa tolerancia: la limita a proposito,
porque la condicion con la que el CEO toleraria mas ("si se que puede recuperar") no se puede
conocer por adelantado ni la puede verificar el sistema.

## D-15 · 2026-08-01 · Flujo obligatorio de cuatro capas: CEO → Claude Code → orquestador → agentes
**Motivo:** medido sobre los transcripts de sesion, de 39 invocaciones de subagente el `orquestador`
tenia UNA, y era la prueba de activacion del 30/07: cero trabajo real. La causa: los comandos
suplantaban a los agentes en vez de invocarlos (`/autonomo` empezaba con "Eres el ORQUESTADOR" y
`/informe` con "Eres el SECRETARIO"), asi que el rol se ejercia desde la sesion principal y el agente
no hacia falta nunca. Consecuencia real: el 01/08 un barrido del catalogo `awesome-claude-code`
devolvio 3 hallazgos, nadie lo cuestiono y tuvo que ser el CEO quien dijera que era imposible. Con el
flujo de capas, esa implausibilidad la caza el orquestador al juzgar, y si se le escapa la caza
Claude Code en el filtro final. El CEO no deberia ser el primer control de calidad.
**Forma operativa:** ver la seccion "Como se trabaja: las cuatro capas" de `CLAUDE.md`. En corto:
el CEO pide · Claude Code entiende y llama al `orquestador` · el orquestador REPARTE (que tarea, que
agente, con que instrucciones y quien revisa) · Claude Code cumple la orden sin alterarla · un agente
distinto REVISA · el orquestador JUZGA buscando discrepancias y manda corregir tantas veces como
haga falta · cuando da el CERRAR, Claude Code aplica su FILTRO ("¿responde a lo que se pidio?, ¿es
plausible la cantidad?") y solo entonces sube al CEO.
**Decide:** CEO.
**Que bloqueaba:** que el orquestador, el jefe de proyecto, no se usara nunca; y que llegasen al CEO
resultados sin que nadie hubiera preguntado "¿has mirado bien?".
**Limite tecnico comprobado POR EJECUCION (01/08/2026):** un subagente NO puede invocar a otro
subagente. Se añadio la herramienta `Agent` a la ficha del orquestador y se le invoco: el sistema se
la retira y solo recibe Read, Edit, Write, Bash. Por eso el orquestador DECIDE a quien se llama y con
que instrucciones exactas, y Claude Code ejecuta esa llamada por el. La autoridad es del orquestador;
Claude Code no puede cambiar su reparto, solo devolverselo para que decida el.
**Premisa que se registra a peticion del CEO:** el CEO dirige y NO es tecnico. Todo lo que le llegue
va masticado: opciones cerradas, recomendada con motivo, consecuencias, respuesta de una letra.
Ninguna ficha puede pedirle redactar, buscar ni calcular nada.

## D-16 · 2026-08-01 · CLAUDE.md es la unica lista de reglas normativa; la del WBS se sustituye por un puntero
**Motivo:** el proyecto tenia DOS listas de "29 reglas" con contenido distinto bajo el mismo numero. Verificado por ejecucion: una en `CLAUDE.md` bajo "## Las 29 reglas" y otra en `00-direccion/WBS.md` bajo "## Reglas (sin ambiguedad posible)". Medido con `grep -inoE 'regla[s]? [0-9]+'` sobre el repositorio: **24 de las 29 reglas divergen**; solo coinciden en sustancia la 1, 2, 3, 4 y 6. Ejemplos: "los datos nunca entran en git" es la regla 27 en CLAUDE.md y la 24 en el WBS; la regla 25 es "toda barrera se verifica por ejecucion" en CLAUDE.md y "cada agente lleva el identificador exacto de su modelo" en el WBS; la regla 26 es "los guardias bloquean por defecto" frente a "antes de crear un agente se comprueba que el WBS contiene tareas de su tipo". Consecuencia: ninguna cita "regla N" del proyecto era verificable por la regla 12 de CLAUDE.md (ninguna referencia entra sin un grep que la localice fichero y linea). Por que gana CLAUDE.md y no hubo eleccion real de contenido: **los muros mecanicos y todas las decisiones ya firmadas apuntan a esa numeracion**. Verificado: **12 instancias sobre 6 numeros distintos (1, 13, 21, 22, 26, 27) en `.githooks/`**, **4 en `DECISIONES.md`** y **1 en `.claude/settings.json`**. Todas resuelven contra CLAUDE.md; ninguna contra el WBS (salvo la regla 1, identica en ambas listas). Elegir la lista del WBS habria obligado a reescribir los dos hooks, volver a probarlos por ejecucion, y añadir entradas nuevas a `DECISIONES.md` declarando que D-10 y D-14 citaban mal, porque ese fichero solo admite añadir. El CEO eligio ademas que NO se mantengan dos copias identicas: el WBS lleva un puntero de 5 lineas a CLAUDE.md, sin texto de regla propio. Motivo dado por el CEO: que quede centralizado. Motivo tecnico que lo respalda: dos copias que "deben" decir lo mismo es justo lo que produjo esta averia; nadie decidio que la regla 25 significara dos cosas, alguien toco una copia y no la otra.
**Decide:** CEO.
**Que bloqueaba:** cierre de la tarea 03.01.13, y toda cita "regla N" del proyecto, que hasta hoy significaba dos cosas distintas.
**Forma operativa:** toda cita se escribe **"regla N de CLAUDE.md"**, nunca "regla N" a secas. La seccion "## Reglas (sin ambiguedad posible)" del WBS se sustituye por un puntero sin texto propio. Las 39 instancias de "regla N" que hay hoy en el WBS se traducen con la tabla ya escrita en `00-direccion/PENDIENTE-03.01.13-lista-de-reglas.md`, que se borra al aplicarse.
**Nota de proceso:** la edicion de `CLAUDE.md` declarando la derogacion se hizo ANTES de esta firma, y el revisor `critico-codigo` la rechazo por ese motivo — la ficha de 03.01.13 reservaba la eleccion al CEO. La decision del CEO llega ahora y la convalida. El rechazo fue correcto y queda registrado.

## D-17 · 2026-08-03 · Techo del 20% de motor (regla 8 de CLAUDE.md) suspendido hasta que 03.01.05 esté hecha o 01/09/2026
**Motivo:** el CEO ordenó el 03/08 construir el motor antes que el producto, lo que incumple la regla 8 de CLAUDE.md (cada tirada autónoma cierra al menos una tarea que avanza el PRODUCTO). B lo pone por escrito con condición de vuelta automática en vez de saltarse la regla en silencio cada semana. La regla 8 NO se elimina —tiene incidente vivo detrás: el proyecto anterior murió al 70% de motor— se suspende con disparador que impone el sistema, no el vigilado (regla 26 de CLAUDE.md).
**Forma operativa:** la suspensión es por DOS condiciones, ambas deben cumplirse para levantar la suspensión: (1) la tarea 03.01.05 esté hecha, O (2) llegue la fecha 01/09/2026, lo que ocurra PRIMERO. Si llega el 01/09 y 03.01.05 sigue pendiente, la suspensión se retira automáticamente; la regla 8 vuelve a aplicarse sin necesidad de ficha nueva. Mientras esté en vigor la suspensión, el equipo puede dedicar más del 20% a motor en una tirada si es necesario para desbloquear producto.
**Decide:** CEO (opción B de la ficha, con la condición de vuelta automática).
**Que bloqueaba:** la ejecución del plan de motor de la semana actual.
**Requisito administrativo:** añadir esta decisión a la sección de límites del CEO en el WBS.

## D-18 · 2026-08-03 · El lunes deja de ser la única ventana de decisión del CEO
**Motivo:** D-13 ya decía «1 h los lunes como MÍNIMO garantizado, no techo», pero el equipo siguió calculando el calendario solo por lunes disponibles. El CEO supervisa durante toda la semana y lo que esté listo le llega el día que esté listo. La hora de los lunes se creó para revisar, no para ser su única ventana.
**Forma operativa (versión inicial del 03/08):** lo que esté listo con su ficha se le presenta al CEO el día que esté listo, con un tope de 2 fichas al día entre semana; lo que exceda se acumula al lunes. **ENMIENDA DEL MISMO 03/08 — ANTES DEL PRIMER COMMIT:** el CEO rechaza el tope de 2. Palabras del CEO: «si estoy aquí que me lleguen lo que me tenga que llegar, si no puedo continuar ya lo dejamos para el día siguiente, pero mientras pueda se hace». Forma operativa corregida: lo que esté listo con su ficha se le presenta al CEO **el día que esté listo, sin tope de número**. El CEO marca el final del día — cuando dice que no puede seguir, lo que quede se acumula al día siguiente. **Lo que le protege no es el número de fichas, sino que cada una llegue en formato obligatorio** (sección «Qué llega al CEO y qué no» de `CLAUDE.md`): masticada, con opciones cerradas, recomendada con motivo, respuesta de una letra. El lunes sigue siendo **checkpoint de revisión**: qué se hizo la semana anterior, dónde estamos, qué falla, qué falta, cómo se sigue. Consecuencia: el calendario del proyecto **deja de calcularse por lunes disponibles** — G1 y la elección de broker ya no esperan a un lunes.
**Decide:** CEO (opción B de la ficha, enmendada el mismo 03/08/2026).
**Que bloqueaba:** el calendario del proyecto, que se calculaba contando lunes disponibles: G1 estaba planeada para lunes 10/08, elección de broker para 17/08, aunque el material estuviera listo antes.
**Nota registrada:** esta decisión hace que D-13 (que ya lo decía) no haya sido recogida en el WBS ni en el reparto. Materia de lección, pero no se escribe aquí. **El tope de 5 fichas del checkpoint del lunes (D-13) NO se toca** — sigue vigente.

## D-19 · 2026-08-03 · PUERTA G1: un solo mercado, ORO al contado (XAUUSD), vela de 4h
**Qué se decide:** el bot se construye sobre **XAUUSD (oro al contado) y vela de 4 horas, un único mercado**. No es ninguna de las cuatro opciones A-D de la ficha presentada: es una quinta opción del propio CEO, que se registra como tal.
**Motivo, con las palabras del CEO:** «el oro converge en todo y todo está de acuerdo con el oro, vamos de momento con el oro; cuando encontremos y probemos que las hipótesis ganan dinero de verdad, entonces ya nos metemos con otra moneda, la que sea, ya veremos; vamos a centralizar de momento en esto y poner foco en una cosa».
**Verificación de la observación del CEO (regla 9 de CLAUDE.md, nivel 1 — ejecutado):** `03-motor/scripts/cestas_g1.py` sobre `04-resultados/correlaciones_8x8.json` enumera **4 cestas de 3 admisibles a 4h y ninguna de 4 ni de 5**, y XAUUSD está en las 4. La observación es correcta. Matiz declarado: USDJPY también está en las 4; el oro se distingue por ser el más barato de los 8 en coste relativo (0,94% central frente a 1,93% de USDJPY) y el que más margen deja en el filtro de coste sobre volatilidad a 4h (2,32% frente a un umbral de 10%).
**Esta decisión DEROGA D-2** («Portafolio de 3-5 mercados poco correlacionados, no un solo par», 29/07/2026), cuyo motivo era repartir riesgo y ganar muestra de operaciones. El CEO acepta concentrar a cambio de foco, y declara la ampliación a un segundo mercado como paso posterior condicionado a que una hipótesis demuestre ganar dinero.
**Consecuencias que quedan registradas, sin suavizar:**
1. **G1-C5 (correlación ≤0,7 en tres ventanas) queda sin objeto** mientras haya un solo mercado: no hay par que comparar. Vuelve a aplicarse el día que entre el segundo mercado, y ese día la cesta se recalcula, no se hereda.
2. **Los cinco huecos declarados del oro dejan de estar repartidos y pasan a ser el riesgo entero del proyecto:** (a) el hueco de fin de semana máximo medido —5,05x lo arriesgado— se midió precisamente en el oro; (b) mantener una posición larga de oro de una noche a otra cuesta entre −6,64% y −8,16% anual, mientras que en corto es casi neutro: la asimetría es del propio instrumento; (c) operar oro exige unos 1.962 € por lote mínimo, contra un techo de cuenta de 2.000 €, salvo que el broker admita lotes fraccionados de 0,1 oz; (d) el coste del oro es de febrero de 2025 y bajo la cota de deriva medida podría casi duplicarse; (e) L-007 sin resolver — la fórmula de coste del broker referencia un producto con componente de futuro mientras el precio usado es de contado, y podrían no ser el mismo instrumento.
3. Los puntos 2(c), 2(d) y 2(e) **se resuelven todos en 04.01.01 y 04.01.02** (elegir broker y recalcular costes con sus precios reales). Ninguno bloquea hoy.
4. **02.01.01 queda ratificado por la vía de los hechos:** elegir XAUUSD ratifica el censo de candidatos del que salió.
**Decide:** CEO, 03/08/2026, opción propia fuera de la ficha D-19.
**Qué desbloquea:** 02.03.03 (puerta G1) y con ella 04.01.01 y toda la Fase 04.

## D-20 · 2026-08-03 · Las auditorías del ecosistema se cierran; lo que valía de ellas son las ideas, no las piezas
**Qué se decide:** `01.02.03` (catálogo `awesome-claude-code` y mecanismos nativos) y `01.02.04` (servidores MCP) se cierran con hueco declarado. Su resultado no se registra como «cero», sino como **cinco ideas construibles por el propio proyecto**.
**Motivo, con las palabras del CEO, que corrigen el planteamiento con el que se ejecutaron:** «yo no quería buscar algo que ya estaba construido, yo quería ver qué ideas podíamos coger de ahí y aplicarlas para construirlas nosotros con lo que nos interesa».
**Consecuencia de método, y es lo importante de esta decisión:** las dos auditorías se juzgaron con un criterio de admisión de PIEZA INSTALABLE («¿se puede escribir en menos de 100 líneas propias? entonces no entra»). Con ese criterio, todo lo que el proyecto puede construir barato se descartaba por barato. El criterio para futuras auditorías del ecosistema pasa a ser: **se busca la idea aplicable, y que se pueda construir aquí en pocas líneas es un argumento A FAVOR, no en contra.**
**Forma operativa — las cinco ideas y dónde viven:** (1) contador mecánico producto/motor → tarea nueva **03.01.18**; (2) registro de autoría contra la auto-revisión → tarea nueva **03.01.19**; (3) detección de fallo o rechazo de modelo → ya es **03.01.04**, cuya ficha se corrige porque un hook no puede cambiar de modelo por sí solo; (4) arranque desatendido por reloj del sistema → ya es **03.01.03**; (5) aviso al humano sin instalar nada, con hook nativo de tipo `http` → se incorpora a **03.01.03** como implementación recomendada, no como tarea aparte.
**Hallazgo verificado por ejecución al preparar esta decisión:** `.claude/settings.json` contiene solo las claves `permissions` y `_nota`. **El proyecto no tiene configurado ni un solo hook.** Las cinco ideas estaban escritas en dos informes y ninguna existía en el proyecto.
**Hallazgo que las auditorías dejan cerrado y no requiere tarea:** no existe ningún tope de gasto que este proyecto pueda configurar. Lo que hay es el límite del propio plan, que deja de cortar en cuanto se activan créditos de uso. Cualquier salida implica gasto nuevo o cambio de forma de pago, y por tanto decisión del CEO (regla 23 de CLAUDE.md).
**Decide:** CEO, 03/08/2026.
**Qué bloqueaba:** el cierre de 01.02.03 y 01.02.04, que llevaban dos tiradas cada una.

## D-21 · 2026-08-03 · Se elimina el trasplante desde gb2: lo que haga falta se construye desde cero
**Qué se decide:** se elimina del WBS la tarea `01.02.02` («Trasplante pieza a pieza desde gb2») y la sección «Trasplante desde gb2 — criterios de aceptación». **Deroga parcialmente D-6**, que decidió repositorio nuevo MÁS trasplante de cinco piezas verificadas; la mitad del repositorio nuevo sigue vigente, la mitad del trasplante desaparece.
**Motivo, con las palabras del CEO:** «algo que quiero quitar es lo de gb2, de mirarlo; lo que ya hay vamos a construirlo de 0; hay que quitar una tarea».
**Qué se pierde exactamente, comprobado pieza por pieza antes de borrar (regla 11 de CLAUDE.md):** nada vivo. T1 (dataset histórico) quedó sustituido por 02.02.01, que descarga de HistData y Dukascopy. **T2 (motor de backtest) ya se construyó desde cero aquí** — commit `0c35959`; no se copió una sola línea de gb2, y de hecho no se podía: `01-investigacion/herencia-gb2/` contiene únicamente cuatro ficheros `.md` de informe y ningún código de gb2 está en este repositorio. T3 (testbed de invarianza) es la tarea 03.01.10, que ya existe. T4 (guardias del cajón reservado) son las tareas 03.01.08 y 03.01.11, que ya existen. T5 (las 13 fichas de hipótesis) lo sustituye 04.02.01, que barre fuentes desde cero — y el propio informe de gb2 declara que 12 de esas 13 nunca se probaron, así que no eran conocimiento validado.
**Qué NO toca esta decisión:** las lecciones ya extraídas de gb2 (L-009 a L-012 de `LECCIONES.md` y las reglas de `CLAUDE.md` que nacieron de su auditoría). No son código heredado: son conocimiento propio ya incorporado, y se quedan.
**Decide:** CEO, 03/08/2026.
**Qué bloqueaba:** nada. Libera una tarea pendiente de la Fase 01 y cierra la dependencia mental de mirar atrás.

## D-22 · 2026-08-03 · El motor de backtest se tira y se construye desde cero

**Qué se decide:** se retira del árbol de trabajo el motor de backtest introducido por el commit `0c35959` y se construye uno nuevo desde su especificación, sin mirar el anterior.

**Motivo, con las palabras del CEO:** eligió la opción B sobre una A recomendada por el equipo, sabiendo el precio que se le declaró — se deshace el commit de ayer, cumple su orden al 100%, ahorra la auditoría, cuesta una tirada de construcción y pierde 44 pruebas que quizá estaban bien.

**Qué la provoca, medido y no supuesto:** ese motor entró al repositorio el 03/08 con el mensaje literal «pieza T2 del trasplante», que es justo lo que D-21 había ordenado dejar de heredar; ningún fichero fuera de su carpeta lo importaba; y su criterio de aceptación había sido borrado del WBS la noche anterior por la propia cirugía de D-21.

**Forma operativa:** se retira con `git revert`, **nunca reescribiendo el historial**: el código y sus 44 pruebas siguen existiendo en el commit `0c35959` para siempre, como exige la regla 20 de CLAUDE.md y porque son la prueba del incidente del 03/08. La construcción nueva vive en dos tareas del WBS, `04.03.06` (especificación) y `04.03.07` (construcción), colocadas en la Fase 04 porque el motor de backtest es PRODUCTO y no motor de agentes.

**Riesgo declarado, no disimulado:** quien construye el motor nuevo es el mismo agente que escribió el anterior teniendo gb2 delante. El guardia es mecánico y no de confianza: el código viejo se retira del árbol antes de empezar, y el revisor compara el nuevo contra gb2 y contra `0c35959` con el procedimiento del lote (d) de la tarea 07.01.03.

**Decide:** CEO, 03/08/2026, opción B.

**Confirmación del CEO sobre ESTE TEXTO: pendiente al escribirse.** Si corrige algo, se corrige con entrada nueva (regla 21 de CLAUDE.md), nunca editando ésta.

**Qué bloqueaba:** la construcción del motor y el cierre de 07.01.03.

## D-23 · 2026-08-03 · Corrección de hecho sobre D-21: sí se copiaron líneas de gb2

**Qué se corrige, y qué NO:** D-21 decidió eliminar el trasplante desde gb2 y construir desde cero. **Esa decisión no se toca: es del CEO y sigue en pie.** Lo que se corrige es una afirmación de hecho de su motivación, porque `00-direccion/DECISIONES.md` solo admite añadir (regla 21 de CLAUDE.md) y no se puede editar en su sitio.

**La frase corregida:** D-21 afirma «no se copió una sola línea de gb2, y de hecho no se podía». **Las dos mitades son falsas, medidas por ejecución** en el lote (d) de la tarea 07.01.03, con criterio pre-registrado antes de mirar y autorización expresa del CEO para abrir gb2 una vez:

1. **«De hecho no se podía»** — gb2 está en el disco de esta máquina, en `/home/server/projects/gold-bot-2`, y su ruta lleva escrita en este repositorio desde el 30/07, en `01-investigacion/herencia-gb2/INFORME_GB2.md`, puesta por la tarea 01.02.01.
2. **«Ni una sola línea»** — hay **109 líneas no triviales idénticas**: 23 en `costs.py`, **76 en `execution.py`** y 10 en `sizing.py`. «Ni una sola» exige cero.

**Veredicto del lote (d): COPIA**, y se declara qué lo disparó sin redondear: **ningún fichero cruza el umbral del 30% de líneas literales** —el máximo es 24,8% en `execution.py`— **lo que cruza es el umbral del 50% de nombres de símbolo**: `execution.py` comparte 66,7% de los suyos y el 100% de los de gb2; `sizing.py`, 50% y 50%. Símbolos compartidos: `Trade`, `BacktestResult`, `run_backtest`, `_find_exit`, `SizingConfig`, `implied_risk_pct`. Es código reescrito por dentro sobre el mismo esqueleto, que es el escenario para el que ese sub-criterio existía.

**Lo que sí era cierto en D-21:** `01-investigacion/herencia-gb2/` contiene solo cuatro ficheros `.md` y ningún `.py` de gb2 está commiteado en este repositorio. Verificado.

**Lo que remata la corrección:** las 12 menciones a gb2 dentro del código retirado son referencia declarada, no copia encubierta — una de ellas dice «Construido como información, no como copia en bloque de /home/server/projects/gold-bot-2/engine/core/execution.py». **Esa frase solo se puede escribir con el fichero delante.** Constantes y mensajes de error: intersección vacía.

**Consecuencia práctica: ninguna.** El código ya se retiró del árbol el 03/08 (commit `eb7ac2f`) por decisión B del CEO, registrada en D-22. Esta entrada no cambia ninguna decisión: pone el registro de acuerdo con lo medido.

**Decide:** no hay decisión nueva. Es corrección de hecho exigida por la regla 21 de CLAUDE.md, dictada por el `orquestador` y medida por `critico-codigo`.

**Confirmación del CEO sobre ESTE TEXTO: pendiente al escribirse.**

## D-24 · 2026-08-04 · Tres correcciones de hecho sobre D-20, D-21 y D-22

**Por qué una sola entrada y no tres:** las tres salen de la misma auditoría, del mismo lote (a) de la tarea 07.01.03. Separarlas sugeriría tres hallazgos independientes. Cada apartado nombra su decisión para que siga siendo localizable por `grep`.

**(1) Sobre D-21 — «comprobado pieza por pieza… nada vivo».** D-23 corrigió ya la mitad de las líneas copiadas; **esta mitad seguía sin corregir**. Es falsa: al eliminarse la sección «Trasplante desde gb2 — criterios de aceptación» se perdió el **criterio de aceptación de T2**, que era la única especificación escrita del motor de backtest y que no recogía ninguna tarea viva. Hubo que reconstruirla desde cero en la tarea **04.03.06**. La fila del registro de decisiones del WBS que repite «comprobado pieza por pieza» queda igualmente corregida por esta entrada.

**(2) Sobre D-20 — «el proyecto no tiene configurado ni un solo hook».** **Falsa, refutada por ejecución** en el lote (a) y reproducida por el `orquestador` el 04/08/2026 a las 09:05: `git config core.hooksPath` devuelve `.githooks`, con `commit-msg` y `pre-commit` ejecutables desde el 31/07/2026. **Los dos muros mecánicos del proyecto son hooks.** La afirmación solo es cierta restringida a los hooks de Claude Code, y `.claude/settings.json` sigue sin ninguno. **Consecuencia de diseño, y no es menor:** las tareas 03.01.19 y 03.01.20 se plantearon sobre la premisa de que no existía ninguna infraestructura de hooks. Existe, de otra clase, y hay que decidir cuál de las dos usa cada guardia antes de construir nada.

**(3) Sobre D-22 — cronología invertida y un rótulo que no corresponde.** D-22 afirma, bajo el epígrafe «medido y no supuesto», que el criterio de aceptación del motor se había borrado «la noche anterior» a que el motor entrara. **Es al revés, y las dos fechas están medidas:** el commit `0c35959` es del **03/08/2026 a las 17:32:44**, y la cirugía de D-21 que borró el criterio es del **mismo día**, entre las 21:44 y las 21:58. El motor entró **antes** de que existiera la orden que supuestamente contradecía. Y el rótulo «con las palabras del CEO» cubre una elección hecha **sin palabras**: el CEO eligió la opción B y no añadió nada más. **Origen del error, declarado y no repartido:** un endurecimiento introducido al transportar el veredicto entre agentes, que Claude Code detectó y confesó por su cuenta. **La decisión B en sí no se toca: es del CEO y sigue en pie.**

**(4) Corrección de fecha que afecta a D-22 y a la ficha de 04.03.07:** la retirada del motor anterior, commit `eb7ac2f`, es del **03/08/2026 a las 23:08:14**, no del 04/08. Medido con `git show -s --format='%ci'` el 04/08 a las 09:05. Es el mismo error de fecha que se corrigió en el encabezado del PASO 0-bis, y se ataja aquí antes de que se propague.

**Decide:** no hay decisión nueva. Son correcciones de hecho exigidas por la regla 21 de CLAUDE.md. Medidas por `validador` en el lote (a); las de los apartados (2) y (4) reproducidas por el `orquestador` por ejecución.

**Confirmación del CEO sobre ESTE TEXTO: pendiente al escribirse.** Si corrige algo, se corrige con entrada nueva, nunca editando ésta.

## D-25 · 2026-08-04 · Tres respuestas del CEO: segunda lectura de gb2, vela de 4h y D-2, y permiso para arreglar su Excel

**Las tres se contestaron con la letra A sobre fichas presentadas el 04/08/2026.**

**(1) Segunda lectura de gb2 — AUTORIZADA, y acotada.** Se autoriza **una segunda** apertura de `/home/server/projects/gold-bot-2` **en solo lectura**, con un fin único: la prueba de aceptación de la tarea **04.03.07**, que compara el motor de backtest nuevo contra gb2 y contra el motor retirado en el commit `0c35959`. **Qué desbloquea:** esa prueba de aceptación, que estaba parada porque la primera autorización, gastada en el lote (d) de 07.01.03, cubría solo la pregunta de si el motor anterior era copia. **Lo que NO autoriza:** ninguna tercera apertura, ningún otro fin, y ningún traslado de contenido de gb2 a este repositorio. Una apertura posterior necesita autorización nueva.

**(2) Vela de 4h y figura de D-2 — dos cosas, y se registran por separado.**

**(2a) La vela de 4 horas queda ratificada COMO DECISIÓN DEL CEO.** Y se declara lo que corrige: cuando se escribió **D-19**, «vela de 4h» era una **inferencia del equipo** —la cita del CEO no contenía ni «vela» ni «4h», y las cuatro opciones de la ficha la llevaban como base común— y D-19 la firmó como suya **sin declarar que era una inferencia**. Hoy deja de serlo. **La ratificación no borra el defecto de proceso: lo cierra.**

**(2b) D-2 queda SUSPENDIDA CON DISPARADOR, no derogada.** Esto **sustituye** la cláusula de D-19 que decía «Esta decisión DEROGA D-2». Palabras del CEO recogidas en la ficha: dijo literalmente «de momento», dos veces. **Disparador declarado por el CEO:** D-2 —portafolio de 3 a 5 mercados poco correlacionados— vuelve el día que **una hipótesis demuestre ganar dinero**. **HUECO DECLARADO Y NO RELLENADO:** «demuestre ganar dinero» **no tiene hoy definición medible**, y un disparador que no se puede medir no puede dispararlo el sistema, sino el vigilado, que es lo que prohíbe la regla 26 de CLAUDE.md. **No se inventa aquí un umbral.** La definición medible corresponde a los criterios de la puerta G2, que ya viven en las tareas 04.03.05 y 04.04.03, y se escribe allí antes de que este disparador pueda usarse. Mientras tanto, sigue vigente un solo mercado.

**(3) Arreglar el Excel del CEO — PERMISO DE MOTOR CONCEDIDO.** La tarea **03.01.16** queda autorizada a ejecutarse; era deuda de motor y sin permiso del CEO no se tocaba (regla 7 de CLAUDE.md). **Motivo que se le presentó:** hoy su única vista del proyecto le oculta cosas que firmó él. **Medido por el `orquestador` el 04/08/2026 a las 09:09:** `CLAUDE.md` tiene 29 reglas, `LECCIONES.md` 28 lecciones y `DECISIONES.md` 24 decisiones, mientras el Excel le muestra 0 reglas y 18 lecciones. **Aviso obligatorio antes de trabajarla:** la ficha de 03.01.16 fija como objetivo «29 reglas / 23 lecciones / 16 decisiones», cifras **caducadas**. Hay que reescribir la ficha antes de ejecutarla o su propia prueba fallará (regla 6 de CLAUDE.md), y la prueba nueva debe comparar **contra el recuento vivo de cada fuente**, nunca contra un número escrito a mano.

**Decide:** CEO, 04/08/2026, opción A en las tres.

**Qué desbloquea:** la prueba de aceptación de 04.03.07 · el cierre de tres puntos de la lista del CEO · la ejecución de 03.01.16.

**Qué queda abierto:** la definición medible de «demuestre ganar dinero», que va a G2.
