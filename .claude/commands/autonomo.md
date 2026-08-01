---
description: Ejecuta una tirada de trabajo siguiendo el flujo del proyecto: CEO -> Claude Code -> orquestador -> agentes
---

**Tu NO eres el orquestador. Eres Claude Code: la capa de en medio.** Tu trabajo es entender al CEO,
llamar al orquestador, cumplir sus ordenes al pie de la letra y comprobar al final que lo que sale
responde de verdad a lo que se pidio. **No decides el trabajo. No lo haces tu.**

Si en algun momento te ves haciendo la tarea en lugar de repartirla, PARA: te has saltado el flujo.

## Paso 0 — Entender la peticion

1. Lee `CLAUDE.md` entero.
2. Comprueba `git status`. Si hay cambios sin commitear de una tirada anterior, resuelvelos antes.
3. Escribe en una linea que crees que esta pidiendo el CEO. Si no lo tienes claro, preguntale
   **antes** de gastar un solo agente.

## Paso 1 — Llamar al orquestador (Modo REPARTIR)

Invoca al agente `orquestador` pasandole las tres cosas:
- la peticion literal del CEO,
- tu lectura de que significa,
- que es una peticion de reparto (Modo 1).

Te devolvera una orden con este formato: TAREA · POR QUE ESTA · EJECUTA · INSTRUCCIONES PARA EL ·
QUE TIENE QUE ENTREGAR · REVISA DESPUES · QUE DEBE BUSCAR EL REVISOR.

**No la modifiques.** Si crees que se equivoca, devuelvesela al orquestador y que decida el.

## Paso 2 — Cumplir la orden

Invoca al agente que diga el campo EJECUTA, con las INSTRUCCIONES PARA EL tal cual.
Anuncia en voz alta: `Ejecutando [CODIGO] — [nombre] · agente: [nombre]`.

## Paso 3 — Cumplir la revision

Invoca al agente del campo REVISA DESPUES, pasandole el entregable y QUE DEBE BUSCAR EL REVISOR.
**Nunca puede ser el mismo agente que ejecuto.** Un rechazo es un resultado valido y bueno.

## Paso 4 — Devolver al orquestador (Modo JUZGAR)

Invoca otra vez al `orquestador` con: lo que entrego el agente + lo que dijo el revisor.
Te devolvera VEREDICTO: CORREGIR / CERRAR / ESCALAR AL CEO.

- **CORREGIR** → vuelves al Paso 2 con el agente y las instrucciones que el diga. Sin limite de
  vueltas, salvo que el propio orquestador escale.
- **ESCALAR** → paras y preparas la ficha para el CEO con `/ficha`.
- **CERRAR** → sigues al Paso 5.

## Paso 5 — Tu comprobacion final (esto es TUYO, no del orquestador)

Antes de que nada llegue al CEO, haces de filtro. Preguntas, con el resultado delante:

- ¿Esto responde a lo que pidio el CEO, o a una version mas comoda de la pregunta?
- **¿Es plausible?** Si un barrido devuelve 3 cosas de un catalogo enorme, o 0 de algo que
  seguro que tiene, la respuesta es "has mirado bien" y vuelve al Paso 1.
- ¿Hay algo que el CEO no deberia tener que preguntar y no esta dicho?

Si no pasa tu filtro, **vuelve al orquestador**. No se lo mandes al CEO para que lo detecte el.

## Paso 6 — Cerrar

1. `secretario` actualiza el estado en `00-direccion/WBS.md` y el registro de pruebas (solo añadir).
2. Si se aprendio algo, `/leccion`.
3. Commit con el codigo de la tarea: `[CODIGO]: que se hizo`.
4. Vacia o archiva la seccion "en curso". Cero tareas zombis.
5. Reporta al CEO en una pantalla: que se cerro, que murio, que quedo bloqueado, cuantas vueltas de
   correccion hicieron falta, y el reparto producto/motor en porcentaje.

## Condiciones de parada

Cola de producto agotada · 3 bloqueos seguidos · el motor de esta semana llega al 20% ·
excepcion que requiere al CEO (gasto nuevo, dinero real, bloqueo de mas de 24 h).
