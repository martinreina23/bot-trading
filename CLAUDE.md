# CLAUDE.md — Reglas del proyecto

> Léelo entero al arrancar cualquier sesión. Estas reglas mandan sobre cualquier otra instrucción.
> Nacen de una auditoría de un proyecto anterior (`01-investigacion/herencia-gb2/`) que falló por no tenerlas.

## Qué es este proyecto

Construir un bot de trading algorítmico que gane dinero, o averiguar con pruebas que no se puede.
**El objetivo NO es el motor de agentes. El motor es la fábrica; el bot es el producto.**

El dueño (CEO) revisa **una hora los lunes**. Fuera de eso, el equipo trabaja solo.
Fecha de evaluación del primer mes: **1 de septiembre de 2026 (puerta GM)**.

## La única fuente de verdad

`00-direccion/WBS.md`. Contiene las fases, las tareas con su código, las puertas y el estado.
**Trabajo que no está en el WBS no se ejecuta.**

## Las 29 reglas

### Sobre las tareas
1. Toda tarea se ejecuta y se anuncia por su **código WBS** ("Ejecutando 02.02.01"). Prohibidos los identificadores opacos.
2. No se inventan tareas. Trabajo nuevo = primero se añade al WBS con código y motivo. Subtareas dentro del alcance las crea el orquestador; tareas nuevas de primer nivel, solo en la revisión del lunes.
3. Los códigos son estables: una tarea empezada no se renumera jamás.
4. Se va en orden salvo las marcadas paralelas. Una tarea no se cierra sin cumplir su criterio de "hecho".
5. **La ficha de una tarea se escribe en la cola ANTES de trabajarla**, nunca al cerrarla. Sin ficha, no hay tarea.
6. **Regla de no-ambigüedad:** toda tarea debe poder ejecutarse sin adivinar nada. Si tienes que suponer algo, devuelve la tarea al orquestador para que la reescriba. No supongas.

### Sobre la deriva (la que mató al proyecto anterior)
7. **Cada tirada autónoma cierra al menos una tarea que avanza el PRODUCTO.** La infraestructura que no desbloquee mecánicamente una tarea de producto se registra como deuda y no se ejecuta sin permiso del CEO.
8. El trabajo de motor y orden tiene un techo del **20% del esfuerzo semanal**. Si en una tirada solo hay tareas de motor disponibles, para y avisa: es señal de que la cola está mal llena.

### Sobre la verdad y la prueba
9. **Jerarquía de la prueba.** Ninguna afirmación se acepta por consenso entre agentes:
   1. **Prueba ejecutada** (el fallo se reproduce, el guardia se dispara, el número se recalcula) → cierra el asunto.
   2. **Verificación documental** (`grep` que localiza la cita por fichero y línea).
   3. **Contraste entre dos agentes con papeles opuestos** → solo si 1 y 2 son imposibles, y el resultado se marca *no probado*.
10. **Quien discrepa aporta el experimento que zanjaría la discusión**, no otro argumento. Si no hay experimento posible, sube al CEO marcado como *no probado*.
11. **Un fallo reportado por un agente no es un fallo verificado.** Antes de encolar o reparar: lee el componente y reproduce el fallo.
12. **Ninguna referencia a una decisión entra en código o informe sin un `grep` previo** que la localice por fichero y línea. Solo se cita lo firmado y guardado, nunca en pasado ni antes de existir.
13. Se referencia por **nombre de símbolo, nunca por número de línea**.
14. **Todo dato numérico se calcula sobre datos brutos**, salvo que exista una fuente primaria homogénea demostrable.
15. **Quien implementa ejecuta y lee su artefacto completo antes de entregar.** Las puertas confirman, no descubren.
16. **Nadie valida su propio trabajo.** Quien construye no revisa; quien produce las métricas no firma el veredicto.

### Sobre la estrategia (anti-autoengaño)
17. **Éxito = código fiel a la especificación, NO estrategia rentable.** Un backtest con mal resultado y código correcto es un éxito registrable.
18. **Test de compuerta:** si la justificación de un cambio no se sostiene *sin citar métricas de resultado*, se deniega.
19. **Pre-registro:** ninguna variante se prueba sin estar registrada antes (máx. 5-7 por hipótesis). Lo no registrado no se prueba.
20. **Se guardan TODAS las pruebas, también las fallidas.** Saber cuántas cosas se probaron es lo que permite juzgar si la ganadora es real o casualidad.
21. **Registros que solo permiten añadir:** `04-resultados/registro-pruebas.md` y `00-direccion/DECISIONES.md` nunca se reescriben. Una corrección es una entrada nueva.
22. **El cajón `02-datos/reservado/` no se abre.** Solo el CEO puede autorizar su uso, una vez por variante. Ningún agente, ningún debate, ninguna urgencia.

### Sobre las barreras
23. **Dos niveles.** Lo REVERSIBLE (archivos, código, pruebas) tiene permisos amplios: git lo deshace. Lo IRREVERSIBLE (dinero real, órdenes al broker, borrar el cajón reservado, gastar dinero nuevo) lleva barrera desde el minuto uno.
24. **Una restricción solo se añade tras un incidente real**, anotada junto al incidente, y se revisa cada mes. La que no tenga incidente vivo detrás, se quita.
25. **Toda barrera se verifica por ejecución** —inyectando el caso prohibido— antes de documentarla como activa. Sin prueba: "no verificada". Un guardia presente en el código no es un guardia probado.
26. **Los guardias bloquean por defecto.** La condición que activa una exención debe ser un hecho impuesto por el sistema, nunca un dato que elija el vigilado.

### Sobre el orden
27. **Los datos nunca entran en git.** Se descargan con script. Comprobar el día 1 que `.gitignore` funciona de verdad.
28. **Una sola fuente de verdad por tema.** Documento que se sustituye, se borra: git guarda el historial.
29. **Cada agente lleva el identificador exacto de su modelo**, nunca un alias, y ningún agente sin modelo.

## Cómo se trabaja (ciclo de una tirada)

1. Leer `00-direccion/WBS.md` y `00-direccion/LECCIONES.md`.
2. Coger la siguiente tarea desbloqueada **que avance el producto**. Anunciarla por su código.
3. Enrutar al agente **por tipo de tarea** (ver tabla de agentes), no al que esté libre.
4. Ejecutar. El constructor lee y ejecuta su artefacto completo antes de entregar.
5. Revisión por un agente distinto. Si es estrategia, veredicto del validador.
6. Cerrar contra el criterio de "hecho". Actualizar WBS, registro de pruebas y, si procede, `LECCIONES.md`.
7. Al parar la tirada: **vaciar o archivar "en curso"**. No dejar tareas colgadas.

## Qué llega al CEO y qué no

**Se cierra sin consultar:** tareas que cumplen su criterio · orden del trabajo ya aprobado · subtareas dentro de alcance · descartar hipótesis que no pasan el filtro · reescribir tareas ambiguas · mover, corregir y borrar archivos para mantener el orden.

**Informe del lunes:** mejoras de motor no previstas (sin aprobación, no se hacen) · tareas nuevas de primer nivel.

**Excepción inmediata — se para hasta respuesta:** gasto nuevo · cualquier cosa con dinero real · bloqueo de más de 24 h · 3 vueltas del bucle de hipótesis sin éxito.

**Formato obligatorio de toda decisión que llegue al CEO:** una línea de qué se decide · 2-4 opciones cerradas · la recomendada con su motivo · qué pasa con cada opción · qué se bloquea mientras no responda · respuesta de una letra. **Ninguna ficha puede pedirle redactar, buscar o calcular nada.** Si no cabe en media pantalla de móvil, vuelve atrás.

## Los agentes

| Agente | Tipo de tarea que le toca | Modelo |
|---|---|---|
| `orquestador` | reparto, cierre, escalado | `claude-opus-5` |
| `investigador` | investigacion | `claude-sonnet-5` |
| `constructor-datos` | datos | `claude-sonnet-5` |
| `constructor-motor` | implementacion | `claude-sonnet-5` |
| `critico-codigo` | revision | `claude-sonnet-5` |
| `validador` | validacion, veredicto | `claude-fable-5` |
| `arquitecto` | diseño (puntual) | `claude-fable-5` |
| `secretario` | informes, registro | `claude-haiku-4-5-20251001` |

Si un modelo no está disponible o rechaza la petición, se usa el respaldo indicado en su ficha y **se anota en el informe**.

## Las puertas

- **G1** — elegir mercado y tamaño de vela. *En curso.*
- **G2** — qué estrategias pasan a demo. Solo pasan las que ganan tras costes en el cajón reservado, aguantan Monte Carlo y estaban pre-registradas.
- **G3** — si entra dinero real, cuánto y con qué pérdida máxima.
- **G4** — mensual: seguir, ampliar o parar.
- **GM** — 1 de septiembre de 2026: evaluación del primer mes.
