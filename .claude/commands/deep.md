---
description: Reescribe tu petición como la escribiría un experto del dominio y responde a esa versión reforzada, no al texto original.
argument-hint: <lo que quieras preguntar o pedir, escrito rápido>
---

# /deep — refuerzo del prompt antes de responder

La petición está en `$ARGUMENTS`. **No respondas a ese texto tal cual.** Es una entrada rápida y
probablemente vaga. Conviértela primero en el prompt que habría escrito un experto del dominio para
pedir exactamente eso, y responde a ESE prompt.

Los esteroides van en el input, no en el output. Esto **no** cambia el estilo ni el tamaño de la
respuesta: cambia lo que recibes.

## El mecanismo — en este orden, siempre

**1. Objetivo real.** Qué quiere conseguir de verdad, detrás de la frase literal.

**2. Reescribe como experto.** Redacta internamente la versión reforzada explicitando lo que el
usuario dejó implícito:
- objetivo concreto y medible
- lo que el dominio implica y el usuario no dijo (dice "bot de trading" → broker, tamaño de vela,
  costes de ejecución, gestión de riesgo)
- alcance: qué entra y qué queda fuera
- restricciones implícitas: presupuesto, plataforma, hardware, nivel, jurisdicción
- criterio de éxito: cómo se sabe que la respuesta sirve
- formato de salida más útil
- **longitud que merece la tarea** — el refuerzo fija el tamaño, no lo infla

**3. Prueba de que el refuerzo sirve.** Antes de responder: ¿la versión reforzada contiene al menos
un dato, restricción o criterio que **no estaba** en el original? Si solo es un parafraseo más
largo, el mecanismo ha fallado → vuelve al paso 2.

**4. Responde a la versión reforzada.** No la muestres.

Sin el paso 2 redactado de verdad no hay ancla, y acabas respondiendo al texto flojo: la orden
"reformula internamente" sin escribir la reformulación no hace nada.

## Reglas del refuerzo

**Fidelidad a la intención.** Explicita lo implícito; no inventa objetivos ni restricciones que el
usuario no tendría. Si para reforzar hay que inventar demasiado, el original está vacío de
intención: pregunta.

**Asume y avanza.** Falta un dato menor → la versión reforzada incorpora la suposición más razonable
y la respuesta la declara en una línea al principio: *"Asumo España, presupuesto bajo-medio."*
Suposición declarada = el usuario la corrige en un mensaje. Suposición callada = respuesta inútil
sin que nadie sepa por qué.

**Pregunta solo si equivocarse cuesta caro:** dinero real, riesgo de seguridad, pérdida de datos,
decisión legal o financiera, acción irreversible. Máximo 3 preguntas concretas, con plantilla para
contestar rápido (`dato 1 + dato 2`). Todo lo demás: asume. Si dudas entre preguntar o responder,
responde.

**Proporcionalidad.** Reforzar un prompt no lo convierte en un informe. "comando para ver puertos
abiertos en Linux" reforzado sigue mereciendo dos líneas: `ss -tulnp`, y que `netstat` está obsoleto.

**Rigor factual.** Separa lo verificado de lo afirmado. Un número sin fuente no se escribe; si no
puedes comprobarlo, dilo en la propia frase. No rellenes huecos con plausibilidad.

**Idioma del usuario**, tanto en la reescritura como en la respuesta.

## Qué añade el experto según el dominio

Menús para elegir, no formularios que rellenar. Solo lo que aplique al caso.

- **Técnico / servidores / código:** diagnóstico antes que solución, comandos exactos, cómo
  verificar que funcionó y cómo revertir. Copia de seguridad antes de cualquier cambio destructivo.
- **Compra o decisión:** coste total incluyendo lo oculto, alternativas descartadas con el motivo, y
  **una sola** recomendación con criterio objetivo.
- **Redacción:** entrega la versión final mejorada, con destinatario, intención y tono explicitados.
- **Estudio:** estructura, conceptos clave, qué memorizar, errores típicos de examen.
- **Dinero / trading / inversión:** pérdida máxima posible y escenario negativo **primero**,
  supuestos numerados. Prohibido prometer rentabilidad o suavizar el riesgo. Si la idea de partida
  es mala, se dice antes de optimizarla, no después de tres párrafos de mejoras.
- **Proyecto o negocio:** MVP mínimo, coste, riesgos, métrica de validación y qué NO hacer todavía.

## Si la petición toca este proyecto

El refuerzo **hereda** `CLAUDE.md`, no lo sustituye. La versión reforzada incluye:

- afirmación sobre el proyecto → `grep` previo que la localiza por fichero y **símbolo**, nunca por
  número de línea (reglas 11 y 12 de CLAUDE.md)
- dato numérico → recalculado sobre datos brutos, no copiado de un resumen (regla 13 de CLAUDE.md)
- trabajo a ejecutar → existe en `00-direccion/WBS.md` con su código, o no se ejecuta (reglas 1 y 2 de CLAUDE.md)
- fallo reportado ≠ fallo verificado: reprodúcelo antes de encolar o reparar (regla 10 de CLAUDE.md)
- si la reescritura obliga a suponer algo **del proyecto**, no supongas: ahí sí se pregunta (regla 5 de CLAUDE.md)
- `02-datos/reservado/` no se abre por ninguna vía ni con ninguna excusa (regla 21 de CLAUDE.md)
- dinero real, gasto nuevo o cualquier acción irreversible → ficha de decisión al CEO y parar
  (regla 22 de CLAUDE.md y formato de decisión)
- una barrera sin caso prohibido inyectado y bloqueado se describe como *no verificada* (regla 24 de CLAUDE.md)

## Nunca

- Mostrar la reescritura: es interna.
- Preguntar por comodidad, por cortesía o para repartir la responsabilidad.
- Alargar la respuesta porque el prompt reforzado sea largo.
- Contestar "depende de tus necesidades". El refuerzo existe justamente para matar ese "depende".
  Si de verdad depende, elige el supuesto más probable, decláralo en una línea y responde.

---

Ahora: refuerza `$ARGUMENTS` siguiendo los cuatro pasos y responde a la versión reforzada.
