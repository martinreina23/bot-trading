---
description: Registra una decision firmada en DECISIONES.md
---

**Lo escribe el `secretario`, no tu.** Invocalo con lo que hay que registrar y estas reglas, y
comprueba su entrada antes de darla por buena (Paso 5 de `/autonomo`).

Añade una decision a `00-direccion/DECISIONES.md`. **Solo se añade.** Una correccion es una entrada
nueva que cita a la anterior, nunca una reescritura.

## Antes de escribir — test de compuerta (regla 18 de CLAUDE.md)
Pregunta: **¿la justificacion de esta decision se sostiene SIN citar metricas de resultado?**
Si la unica razon es "porque el backtest sale mejor", **DENIEGALA**. Es la señal de que se esta
ajustando la estrategia al pasado.

## Quien firma
Nunca el mismo agente que produjo los numeros en los que se apoya la decision (regla 16 de CLAUDE.md).
Las decisiones sobre dinero, mercado, planteamiento o datos reservados **son del CEO, no tuyas**.

## Formato
```
## D-N · AAAA-MM-DD · [decision en una linea]
**Motivo:**
**Decide:**
**Que bloqueaba:**
```
