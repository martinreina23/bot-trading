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
