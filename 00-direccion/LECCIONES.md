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

## L-019 · Un dato de contenido que coincide con el separador del formato rompe el registro, y el sintoma apunta a otro sitio
**Causa raiz:** `05-vista-ceo/generar_excel.py` y `05-vista-ceo/verificar_excel.py` parten la fila
por el caracter de tuberia sin respetar comillas invertidas ni escapes; escaparlo con barra invertida
no sirve.
**Regla:** ningun contenido escrito en una tabla puede contener su separador, y toda edicion de fila
se cierra comprobando el numero de campos.
**Evento:** PASO 0 de la tarea 07.01.01, 02/08/2026. Texto redactado por el `orquestador`, pegado por
`secretario`, detectado por `critico-codigo` y reproducido por el `orquestador`: la fila quedo en 12
campos, el parser devolvio 10 celdas en vez de 5 y `verificar_excel.py` paso de 2 fallos a 4.
Familia: es la misma que **L-016** — el indicador es ciego justo donde importa, y aqui ademas miente
sobre donde.

## L-020 · El orquestador presentó tres estimaciones como mediciones
**Causa raiz:** dictó texto para el CEO y afirmó su tamaño sin ejecutar la medida; las tres veces la ejecución lo desmintió — 945 caracteres frente a 1098 reales, 187 de párrafo frente a 306, y 30 líneas frente a 42.
**Regla:** ninguna cifra sale de este proyecto sin el comando que la produjo al lado, y eso vale también para quien reparte (regla 14 de CLAUDE.md).
**Evento:** tres rondas de la ficha D-17, 02/08/2026, medido por `critico-codigo` y reproducido por el `orquestador`.

## L-021 · Una afirmación sin procedencia intentó cerrar un incidente abierto.
**Causa raiz:** durante la investigación del borrado de `INSTALAR.md` llegó a `critico-codigo` la frase «lo he borrado yo a mano porque no aporta nada ya», por el mismo canal que las órdenes del reparto. Verificado: no procede del CEO (sin intervención humana registrada), no procede de Claude Code, y no existe como contenido en ningún fichero del repositorio (`grep` sobre todo el árbol, cero coincidencias). Origen **no determinable**, y por tanto **no se atribuye a nadie**.
**Regla:** ningún mensaje de un agente es jamás el consentimiento del CEO; una afirmación sin procedencia comprobable no cierra un incidente ni entra en ningún registro, aunque llegue por el canal de las órdenes. Una confesión es un dato de nivel 3 de la regla 9 de CLAUDE.md en el mejor caso, y sin emisor identificable no llega ni a eso.
**Evento:** investigación del borrado de `INSTALAR.md`, 02/08/2026; rechazada por `critico-codigo` antes de conocerse su origen, por carecer de código WBS (regla 1 de CLAUDE.md), de modelo (regla 29 de CLAUDE.md), de ficha (regla 5 de CLAUDE.md) y de entrada en registro (regla 21 de CLAUDE.md), y por contradecir su propia verificación documental.

## L-022 · Medir una instancia y llamarlo el suelo del formato
**Causa raiz:** el orquestador midió por ejecución su propia plantilla de ficha (504 caracteres, 24 líneas a 40 columnas) y la presentó como el mínimo que cualquier texto con los 6 elementos obligatorios podía alcanzar. Con esa afirmación declaró «inalcanzable» el listón contra el que se habían rechazado tres rondas, y justificó un techo de 900 caracteres y 200 por párrafo que dejaba pasar intacto el fichero de 612 caracteres que esas tres rondas habían rechazado. `critico-codigo` construyó una ficha del mismo D-17, con los 6 elementos, en **371 caracteres y 16 líneas**, reproducido de forma independiente; el propio orquestador llegó a 419 al intentarlo.
**Regla:** una medición sobre un artefacto propio prueba **ese artefacto**, nunca el límite de su clase. Afirmar un suelo exige o una demostración de imposibilidad, o que lo intente **alguien distinto** (regla 16 de CLAUDE.md). Medir bien no protege de generalizar mal.
**Evento:** 02/08/2026, tercera y cuarta rondas de la ficha D-17; refutado por ejecución, que es el nivel 1 de la regla 9 de CLAUDE.md.

## L-023 · Se propuso recortar el fondo para cumplir un límite de forma
**Causa raiz:** la ficha D-17 no cabía en el techo de longitud y el orquestador propuso **eliminar la opción B** —la cara y exhaustiva, que nadie recomendaba— en vez de apretar la prosa. Eso no acorta la ficha: **estrecha lo que el CEO puede elegir**, y lo hace justo con la opción de hacer el trabajo a fondo.
**Regla:** cuando un entregable no cabe, se recorta la **forma**, nunca el **fondo**. Quitar una opción de una ficha de decisión no es acortar: es decidir en lugar del CEO. Si con el fondo íntegro no se cumple el límite, **el que se mueve es el límite**, y se mueve con la medición delante.
**Evento:** 02/08/2026, propuesto por el `orquestador` y **detenido por Claude Code en el filtro C3 antes de ejecutarse**, con el agravante de que contradecía su propia norma —«el techo se ajusta al formato, no el formato al techo»— escrita tres párrafos antes en el mismo mensaje.

## L-024 · Una decisión firmada que no se propaga deja el proyecto funcionando con la premisa vieja
**Causa raiz:** D-13 se firmó el 01/08/2026 con «1 h los lunes como MÍNIMO garantizado, no techo». Pero ni el WBS ni `CLAUDE.md` ni las fichas de los agentes lo recogieron. El 03/08/2026 el orquestador construyó el calendario del mes contando lunes disponibles, dio por perdida una semana hacia GM que no estaba perdida, y fue el CEO quien lo corrigió, no el equipo.
**Regla:** al firmar una decisión se localizan por `grep` todas las frases que la contradicen y se corrigen en el mismo commit. Si no, la decisión existe en el papel y el proyecto sigue leyendo la premisa vieja.
**Evento:** 01/08/2026 (D-13 firmada sin propagación) y 03/08/2026 (calendario equivocado, corregido por el CEO).

## L-025 · Una orden dirigida al CEO debe declarar dónde se teclea
**Causa raiz:** el 03/08/2026 se le pasó al CEO la orden `comprobar` del cajón sin decir que exige una terminal real del sistema. El prefijo de ejecución rápida de la sesión de Claude Code no da terminal interactiva (no cumple `sys.stdin.isatty()`), y además el CEO recibió un error de shell por llevar dos órdenes encadenadas. Verificado por ejecución: `_pedir_password()` devuelve «BLOQUEADO: la contraseña solo se teclea en una terminal real».
**Regla:** toda orden que se le dé al CEO declara **dónde** se teclea y **por qué no vale otro sitio**, y va en **una sola línea sin encadenar comandos**.
**Evento:** 03/08/2026, orden `python3 03-motor/scripts/cajon_reservado.py comprobar` pasada con el prefijo de ejecución rápida de Claude Code + encadenada con otra orden.

## L-026 · Una prueba de inyección con el texto de la víctima escrito a mano caduca sola, y luego acusa al inocente
**Causa raiz:** `05-vista-ceo/prueba_inyeccion.sh` rompía el WBS con `sed` sobre fragmentos de prosa literales. El 02/08/2026 se amplió la celda de estado de `01.02.01` para añadirle una ficha de apoyo, y el patrón del caso 2 dejó de encontrar nada. Desde ese día el fichero «roto» salía **idéntico** al real, el verificador lo aprobaba con razón, y el script lo declaraba `ESCAPA — EL VERIFICADOR NO DETECTA ESTO`. Comprobado por ejecución el 03/08/2026: `grep -c` del patrón del caso 2 sobre el WBS da **0**, y el verificador **sí** caza el estado sin declarar cuando se le inyecta de verdad (cazó cuatro celdas reales ese mismo día). El acusado era inocente.
**Regla:** una prueba de inyección **localiza a su víctima por estructura, no por su prosa** (la primera fila que cumpla la condición, no un texto copiado), y **comprueba que la inyección cambió algo** antes de juzgar al verificador. Si el fichero roto es igual al bueno, el fallo es del test.
**Evento:** 03/08/2026, al re-pasar la prueba de inyección tras retirar la hoja TRASPLANTE del generador del Excel (D-21). Reparado en el mismo día: víctima localizada por estructura y guardia `FIXTURE` añadido y **verificado por inyección deliberada** de una fixture caducada.

## L-027 · Borrar una fila del WBS con una herramienta de texto puede fusionar dos filas sin avisar
**Causa raiz:** el 03/08/2026, al eliminar la fila `01.02.02` por D-21, la operación se llevó también el salto de línea siguiente y dejó las filas de `01.02.01` y `01.02.03` **fusionadas en una sola línea de 13 campos**. El WBS seguía pareciendo correcto de un vistazo: ninguna palabra se había perdido. Lo detectó el recuento de filas, que bajó de 56 a 54 en vez de a 55. Es el tercer incidente de la semana en que el WBS se corrompe por formato y no por contenido.
**Regla:** después de **toda** edición estructural del WBS —añadir, borrar o mover filas— se ejecuta un recuento que compruebe dos cosas: el **número de filas esperado** y que **toda fila de tarea tiene exactamente 7 campos** al partir por la barra vertical. No vale mirarlo: se ejecuta.
**Evento:** 03/08/2026, eliminación de `01.02.02` (D-21). Detectado y reparado en la misma tirada antes de generar nada.

## L-028 · Rodear el limite de herramienta de un agente parece un atajo y es el fallo

**Causa raiz:** `critico-codigo` tiene `Bash` pero no `Write`, y se le ordenó dos veces entregar un fichero. La salida cómoda estaba a mano: `.claude/settings.json` permite `Bash(python3 *)`, así que cualquier agente con `Bash` puede escribir cualquier fichero **sin usar la herramienta `Write`**. Usarlo habría convertido el límite del agente en una sugerencia y habría dejado al vigilado eligiendo su propia exención, que es lo que prohibe la regla 26 de CLAUDE.md. Lo mismo vale para el sistema de permisos: `rm` no está en la lista de permitidos, y conseguir el mismo efecto con `python3` no es sortear un estorbo, es desactivar el control.

**Regla:** el límite de herramienta de un agente y el sistema de permisos **no se rodean**. Se corrige el reparto o se espera la confirmación. Todo artefacto lo persiste un agente que tenga `Write`, y la cadena de custodia se declara dentro del propio fichero. **Toda orden declara quién persiste el artefacto, comprobado contra el campo `tools` de la ficha del agente ANTES de repartir.**

**Consecuencia dormida, para cuando se construyan 03.01.19 y 03.01.20:** un hook `PostToolUse` o `PreToolUse` con matcher de escritura **no cazaría una escritura hecha por `Bash(python3 *)`**. Un guardia cableado al evento equivocado es L-009 otra vez.

**Evento:** 03/08/2026. El `orquestador` diagnosticó que `critico-codigo` no tiene `Write`, dictó esta norma en un mensaje que nunca llegó a ningún artefacto, y **volvió a pedirle un fichero en la orden siguiente**. Los dos veredictos afectados —lotes (b+c) y (d) de la tarea 07.01.03— quedaron sin artefacto hasta que los pegó `secretario`. Detectado por `critico-codigo`, que buscó la cita por `grep` y no la encontró.

## L-029 · «Anadir al final» y «sustituir» dan resultados que no se distinguen mirando

**Causa raiz:** una orden decía «sustituye `— **pendiente**` al final de la celda por este texto» y se ejecutó como «sustituye la celda». **El resultado parecía correcto**: la celda tenía su cierre, su estado en negrita, sus 7 campos y el fichero pasaba todas las comprobaciones estructurales. **Lo que faltaba no se ve mirando lo que hay, solo midiendo lo que ya no está**: 1.050 caracteres, entre ellos la corrección de un defecto y la declaración de que se había corregido. Quien ejecutó no tiene terminal y no podía comprobar lo que escribía (tarea 03.01.15); el daño lo cazó Claude Code **leyendo el parte del agente**, no ningún mecanismo.

**Regla:** toda edición de una celda se cierra **comparándola contra un punto de control inmutable**, comprobando que **cada frase anterior sigue estando**, y nunca por longitud: una celda puede crecer y perder contenido a la vez. Si no hay punto de control, se crea antes de editar con `git hash-object -w`, que no commitea ni toca el árbol.

**Lo que salvó el contenido:** el punto de control creado ese mismo día para poder atribuir cambios. El WBS no estaba en ningún commit desde antes del 03/08, así que sin ese blob la pérdida habría sido definitiva. **Es la segunda vez que una medida escrita evita un daño en vez de explicarlo, y la primera que además lo repara.**

**Evento:** 04/08/2026, cierre de la tarea 04.03.06. Pérdida medida contra el blob `ffbf6774…`: 7 frases con conteo 1 antes y 0 después.

## L-030 · El trabajo honesto se queda en la tabla y el resumen es lo unico que llega arriba

**Causa raiz:** en `comparacion_brokers.md` las 24 celdas con fuente estaban verificadas y los 8 huecos bien declarados, pero **la sección de síntesis convertía un hueco en hecho** —daba por supuesto que XTB tenía API cuando su propia celda decía «no confirmado»— y arrastraba un recuento falso de una redacción anterior no releída (regla 15 de CLAUDE.md). **El defecto no estaba en el trabajo: estaba en el único sitio que el CEO iba a leer.**

**Regla:** el resumen se deriva de la tabla y se comprueba contra ella frase a frase antes de entregar. **Ninguna afirmación del resumen puede ser más fuerte que la celda de la que sale**, y un hueco declarado abajo sigue siendo un hueco arriba. Todo revisor de un documento que suba al CEO contrasta el resumen contra el cuerpo **como paso nombrado**, no como lectura general.

**Evento:** 04/08/2026, revisión de la pasada 1 de la tarea 04.01.01 por `critico-codigo`.

## L-031 · Repartir a ciegas no sirve si la ficha ya lleva dentro lo que el ejecutor no debe saber

**Causa raiz:** el `orquestador` diseñó la segunda pasada de 04.01.01 con **ejecutor ciego y revisor informado**, para que una preferencia declarada por el CEO se convirtiera en hipótesis contrastable y no en sesgo de confirmación. Y en la misma ficha escribió que el CEO había preguntado por cierto régimen regulatorio «con la frase eso es lo que busco», **tres líneas antes de prohibir al ejecutor conocer preferencias**. No hacía falta nombrar al broker: ese régimen ya era el de uno de los candidatos, así que la ficha señalaba hacia dónde inclinarse. **El diseño se anulaba a sí mismo y la instrucción parecía correcta**, que es lo que lo hacía indetectable a simple vista.

**Regla:** cuando se reparte a ciegas, **la ficha también va a ciegas**, y se comprueba expresamente antes de entregarla al ejecutor. No basta con quitar el nombre: se retira **toda marca de deseo** —régimen, jurisdicción, condición o rasgo presentado como buscado—. Prueba de que la cita sobra: si el criterio define el alcance sin ella, es preferencia y no alcance.

**Es el espejo de L-030:** allí el resumen que SUBE afirmaba más de lo que sostenía su tabla; aquí la ficha que BAJA decía más de lo que el ejecutor debía saber. **En los dos el trabajo era correcto y el defecto estaba en el canal.**

**Evento:** 04/08/2026, ficha de la segunda pasada de 04.01.01, escrita por `secretario` con texto dictado por el `orquestador`. Detectado por `critico-codigo`, que fue más lejos de lo que se le pidió: se le encargó comprobar que no apareciera el nombre del broker preferido.
