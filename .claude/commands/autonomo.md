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

## Paso 3 — Revisión y corrección (SIN orquestador)

Invoca al agente de REVISA DESPUES con el entregable y QUE DEBE BUSCAR EL REVISOR.
Nunca puede ser el mismo que ejecutó. Un rechazo es un resultado bueno.

- Si ACEPTA → Paso 5.
- Si RECHAZA → vuelves a invocar al ejecutor con los motivos del rechazo, tal cual, y
  luego otra vez al revisor. **MÁXIMO DOS VUELTAS.**

No invocas al orquestador entre vuelta y vuelta. Su orden del Paso 1 ya contiene el
criterio de aceptación: el revisor lo aplica, no hace falta que nadie lo reinterprete.

## Paso 4 — Cierre o escalado (UNA invocación del orquestador)

- Si el revisor ACEPTÓ → invoca al `orquestador` en Modo JUZGAR, UNA vez, con el
  entregable y el dictamen del revisor. Cierra o escala.
- Si tras DOS vueltas sigue sin aceptar → **PARA**. No hay tercera vuelta. Invoca al
  `orquestador` solo para que prepare el escalado al CEO.

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

## Paso 7 — Dejar el contrato del encadenador. SIEMPRE, pase lo que pase

**Este paso es el ultimo y no se salta nunca**, ni aunque la tarea saliera mal, ni aunque te
quedaras sin avanzar. Si esta sesion la lanzo `03-motor/desatendido/controlador.sh`, estos dos
ficheros son lo UNICO que el controlador puede leer de ti: si faltan o vienen mal, **la cadena
para en seco** y nadie se entera hasta el dia siguiente. Si la sesion la lanzo una persona, se
escriben igual: no estorban y el controlador borra `DESENLACE.txt` antes de cada tirada.

**1. `03-motor/desatendido/DESENLACE.txt` — dos lineas, ni una mas.**

```
CERRADA
03.01.23
```

- **Linea 1:** EXACTAMENTE una de estas tres palabras, sola, sin adornos ni puntuacion:
  - `CERRADA` — el orquestador dijo CERRAR.
  - `ESCALADA` — dijo ESCALAR, o aparecio una excepcion inmediata de `CLAUDE.md`.
  - `BLOQUEADA` — te quedaste sin poder avanzar.
- **Linea 2:** SOLO el codigo WBS de la tarea trabajada, con el formato exacto `NN.NN.NN`.

Cualquier otra cosa —fichero ausente, linea 1 con otro valor, linea 2 con un codigo mal
formado— **para la cadena igual**. Falla cerrado a proposito: nunca sigue por defecto.

**2. `03-motor/desatendido/ESTADO.md` — el traspaso a la sesion siguiente.**

Lo **sobreescribes** en esta sesion (el controlador comprueba la fecha: un resto de una tirada
anterior no cuela) y **no pasa de 100 lineas** (`MAX_LINEAS_ESTADO` de `config.env`). Lleva: que
tarea trabajaste, con que desenlace, que queda pendiente, y **que se rechazo y por que** — si se
pierde el «por que», la siguiente sesion decide peor.

**3. `03-motor/desatendido/PARA-CEO.md`, solo si el desenlace fue `ESCALADA` o `BLOQUEADA`.**
Ficha en el formato obligatorio de `CLAUDE.md`: una linea de que se decide, 2-4 opciones
cerradas, la recomendada con motivo, que se bloquea, respuesta de una letra.

> **Por que esto esta escrito aqui y no solo en el controlador.** Comprobado por ejecucion el
> 12/08/2026: `controlador.sh` inyecta este mismo contrato en el prompt que lanza, pero
> `autonomo.md` no lo habia mencionado nunca —ni en la version del 31/07, ni en la del 01/08,
> ni en la del 12/08—. El contrato vivia en un solo sitio, y ese sitio no era el comando que la
> sesion cree estar siguiendo. Queda en los dos.

## Condiciones de parada

Cola de producto agotada · 3 bloqueos seguidos · el motor de esta semana llega al 20% ·
excepcion que requiere al CEO (gasto nuevo, dinero real, bloqueo de mas de 24 h).
