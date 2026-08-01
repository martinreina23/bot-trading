# Lecciones aprendidas

**Solo se AÑADE.** Una leccion entra unicamente con las tres cosas: **causa raiz**, **regla
verificable** y **evento trazable** que la origino. Una regla sin evento que la respalde no tiene
autoridad y no se escribe aqui.

Formato: `## L-NNN · [sintoma en una linea]` + Causa raiz + Regla + Evento.

---

## L-001 · Se perdio tiempo buscando un dato que habia que calcular
**Causa raiz:** el encargo pedia "buscar el ATR intradia publicado". No existe publicado; si existen
los precios para calcularlo.
**Regla:** todo dato numerico se calcula sobre datos brutos salvo que exista fuente primaria
homogenea demostrable.
**Evento:** entrega del Brief A (22 de 24 celdas quedaron "sin dato fiable"), confirmado por el
Brief B (la matriz de correlaciones tampoco existe homogenea). Dos veces el mismo fallo.

## L-002 · Una conversion correcta explicada al pie y no aplicada en la tabla
**Causa raiz:** el analista escribio bien que la comision de 7 USD no son 0,7 pips en USDJPY, y
luego uso 0,9 en su tabla. Coste infravalorado un 29%.
**Regla:** toda conversion de unidades se aplica en la tabla final, no solo se explica en una nota.
**Evento:** revision 02.03.01 del 29/07/2026.

## L-003 · Medir el coste de entrar y salir sin medir el de mantener
**Causa raiz:** el encargo solo pedia spread y comision. En CFD de bitcoin la financiacion nocturna
(-22,5% anual) supera varias veces al spread si se mantiene la posicion.
**Regla:** el coste tiene dos componentes y se miden los dos: entrar/salir y mantener.
**Evento:** punto ciego señalado por el analista, Brief A.

## L-004 · Comparar valores absolutos entre activos distintos
**Causa raiz:** un ATR en pips y otro en dolares no son comparables.
**Regla:** se normaliza (porcentaje del precio) antes de comparar.
**Evento:** revision 02.03.01.

## L-005 · Creer que el sistema "aprende"
**Causa raiz:** el modelo no aprende nada entre sesiones; lo que crece es un monton de ficheros de
notas que se releen. Si nadie escribe bien las notas, no mejora nada.
**Regla:** el secretario y estos ficheros son piezas obligatorias del sistema, no adorno.
**Evento:** analisis de un video divulgativo, 29/07/2026.

## L-006 · Convenciones invertidas cambian el signo de una correlacion
**Causa raiz:** algunas fuentes usan yen y franco invertidos (JPYUSD, CHFUSD).
**Regla:** verificar la convencion antes de comparar numeros de dos fuentes.
**Evento:** revision del Brief B, 30/07/2026.

## L-007 · Un nombre parecido no es el mismo instrumento
**Causa raiz:** se midio el oro con el futuro de COMEX creyendo medir el oro al contado
(correlacion 0,82: alta, pero no son lo mismo). Igual con bitcoin contra Tether y contra dolar.
**Regla:** comprobar QUE se esta midiendo antes de medirlo, y escribirlo en el informe.
**Evento:** revision del Brief B. El fallo era del propio director del proyecto.

## L-008 · Un umbral sobre una magnitud inestable necesita varias ventanas
**Causa raiz:** el criterio "correlacion menor de 0,7" se escribio para una sola ventana.
EURUSD-AUDUSD sale 0,33 o 0,64 segun el periodo; BTC-oro paso de +0,30 a -0,88.
**Regla:** los umbrales sobre magnitudes inestables se miden en tres ventanas y deben cumplirse en
las tres.
**Evento:** revision del Brief B.

## L-009 · Un guardia verificado por presencia da falsa seguridad
**Causa raiz:** en gb2 se auditaba "existe un if con sys.exit" = "esta protegido". Un guardia estaba
estructuralmente muerto y otro cableado al evento equivocado; ninguno se disparo nunca.
**Regla:** toda barrera se verifica por ejecucion, inyectando el caso prohibido.
**Evento:** auditoria de gb2, secciones 6.3 y 6.4.

## L-010 · Los agentes no se activan por tener buena descripcion
**Causa raiz:** en gb2, tres agentes nunca se invocaron pese a tener fichas claras y permisos
suficientes. La cola nunca contuvo tareas de su tipo, y el reparto ignoraba el tipo durante dos
semanas.
**Regla:** el reparto enruta por tipo de tarea; antes de crear un agente se comprueba que el WBS
genera tareas suyas; agente sin tareas en dos semanas se elimina o se justifica.
**Evento:** auditoria de gb2, seccion 3.1.

## L-011 · Tener una cola estricta no impide la deriva
**Causa raiz:** gb2 tenia cola unica, IDs contiguos forzados por hook y criterio de terminado
explicito. Y aun asi el 70% del esfuerzo se fue al motor. La cola controla QUE se ejecuta, no QUE se
mete en la cola.
**Regla:** cada tirada cierra al menos una tarea de producto; la infraestructura que no desbloquee
mecanicamente una tarea de producto se registra como deuda.
**Evento:** auditoria de gb2, seccion 5.3, y las dos congelaciones de motor.

## L-012 · Dos agentes de acuerdo no son una prueba
**Causa raiz:** en gb2 hubo tres diagnosticos consecutivos del mismo componente, dos falsos. Lo que
los corrigio fue leer el codigo y reproducir el fallo.
**Regla:** jerarquia de la prueba (regla 9 de CLAUDE.md).
**Evento:** auditoria de gb2, error 7 de la lista de diez.

## L-013 · Se trabajo una tarea sin ficha escrita antes
**Causa raiz:** la tarea 01.01.02 era una fila de una linea en el WBS sin alcance ni criterio de
hecho, y el trabajo de apoyo (calculo de arrastre e investigacion de umbrales) se autoasigno alcance
dentro de ella.
**Regla:** la regla 5 vale tambien para las tareas asignadas al CEO; una fila del WBS sin alcance no
es una ficha, y antes de trabajarla hay que escribirla.
**Evento:** hallazgo de `critico-codigo` en la revision del calculo de arrastre, 01/08/2026, confirmado
por grep sobre `00-direccion/WBS.md`.

## L-014 · Un supuesto expresado en porcentaje decidio el orden de magnitud sin declararse
**Causa raiz:** fijar la actividad como "porcentaje de velas operadas" hace que a 15 minutos se abran
~15 veces mas operaciones que a 4 horas solo por haber mas velas; eso produjo un multiplicador de
coste x60-x69 entre velas que al fijar el NUMERO de operaciones cae a x4,3. La conclusion "1h es
inviable" era un artefacto del supuesto, no un hallazgo.
**Regla:** todo supuesto expresado en porcentaje se recalcula ademas en valor absoluto antes de sacar
conclusiones, y se declara cual de las dos formulaciones sostiene el titular.
**Evento:** hallado por `critico-codigo` y confirmado de forma independiente por `validador` con
experimento ejecutado, 01/08/2026, sobre `01-investigacion/mercados/arrastre_coste.md`.

## L-015 · Dos listas de reglas con el mismo numero y contenido distinto
**Causa raiz:** `CLAUDE.md` y `00-direccion/WBS.md` contienen cada uno una lista de "29 reglas", y no
coinciden. Comprobado por grep el 01/08/2026: la regla 16 es "nadie valida su propio trabajo" en
CLAUDE.md y "test de compuerta" en el WBS; la 23 es "dos niveles de barrera" frente a "un fallo
reportado no es un fallo verificado"; la 25 es "toda barrera se verifica por ejecucion" frente a
"cada agente lleva el identificador exacto de su modelo". Toda cita `regla N` del proyecto es por
tanto ambigua, incluidas las de los informes y las fichas del WBS.
**Regla:** una sola fuente de verdad por tema, y las citas de regla llevan el documento delante hasta
que exista una sola lista. Un numero de regla sin documento no es una cita verificable, y la regla 20
de CLAUDE.md exige que toda cita se localice con grep antes de entrar en un informe.
**Evento:** hallado por `critico-codigo` al revisar `01-investigacion/ecosistema/INFORME_AWESOME.md`
y reproducido por el orquestador con grep sobre los dos ficheros, 01/08/2026. Se abre 03.01.13.

## L-016 · Un indicador que solo mira lo etiquetado es ciego justo donde importa
**Causa raiz:** se midio el reparto producto/motor contando solo los commits que llevan codigo WBS
(2 de 10 = 20%, "exactamente en el techo"). Pero `.githooks/commit-msg` EXIME de llevar codigo a los
mensajes que empiezan por `meta:`, `org:` o `arranque:`, y ahi es justo donde vive el trabajo de
motor. Clasificando los 16 commits por contenido, el motor sale 7 de 16 (43,8%), mas del doble del
techo. La aritmetica era correcta; el denominador estaba mal construido.
**Regla:** un indicador se valida contra el universo completo, no contra el subconjunto etiquetado.
Antes de automatizar una metrica hay que preguntarse que deja fuera su filtro, porque automatizar un
punto ciego lo vuelve permanente (L-009 aplicada a un indicador en lugar de a un guardia).
**Evento:** hallado por `critico-codigo` al revisar `01-investigacion/ecosistema/INFORME_AWESOME.md`
y reproducido por el orquestador con `git show --stat` sobre los seis commits exentos, 01/08/2026.

## L-017 · L-015 cita mal su propia regla de grep
**Causa raiz:** L-015 afirma "la regla 20 de CLAUDE.md exige que toda cita se localice con grep
antes de entrar en un informe". La regla 20 de CLAUDE.md es "Se guardan TODAS las pruebas,
tambien las fallidas"; la exigencia de grep previo es la regla 12 de CLAUDE.md. LECCIONES.md es
de solo-anadir (regla 21 de CLAUDE.md): no se corrige en su sitio, se anota aqui.
**Regla:** toda cita de regla se verifica por grep contra CLAUDE.md antes de escribirse (regla 12
de CLAUDE.md), incluidas las citas dentro de las propias lecciones.
**Evento:** hallado en la tarea 03.01.13 (pasada 1, constructor-motor), 01/08/2026, verificado por
grep sobre CLAUDE.md: regla 20 = "se guardan las pruebas"; regla 12 = "grep previo a decision".

## L-018 · Un recuento sin `-i` da cifras bajas, aunque lo repitan dos agentes
**Causa raiz:** en la pasada 1 de 03.01.13, quien ejecuto el recuento y quien lo reviso grepearon
"regla" en minuscula, sin `-i`. Los dos dieron la MISMA cifra baja (5 citas operativas en los
hooks en vez de 12, 3 en DECISIONES.md en vez de 4, 36 en el WBS en vez de 39) porque el error
estaba en el metodo de los dos, no en el dato: un `grep` sin `-i` se come toda cita que empiece
con mayuscula (encabezados de comentario `# --- Regla N:`, notas de cabecera `Regla N`).
**Regla:** un recuento se entrega con la UNIDAD de recuento definida por escrito y el comando
exacto que lo produjo pegado al lado (regla 12 de CLAUDE.md, grep previo); sin los dos, el numero
no se acepta, ni siquiera si dos agentes distintos coinciden en el (el contraste entre agentes es
el nivel mas debil de la jerarquia de la prueba, regla 9 de CLAUDE.md, y no zanja lo que zanja
una ejecucion).
**Evento:** hallado en la tarea 03.01.13 (pasada 2, constructor-motor, ordenada por el
orquestador tras el rechazo del revisor de la pasada 1), 01/08/2026. Verificado por ejecucion:
`grep -inoE 'regla[s]? [0-9]+' .githooks/pre-commit .githooks/commit-msg` = 12 (no 5);
`grep -inoE 'regla[s]? [0-9]+' 00-direccion/DECISIONES.md` = 4 (no 3);
`grep -inoE 'regla[s]? [0-9]+' 00-direccion/WBS.md | wc -l` = 39 (no 36).
