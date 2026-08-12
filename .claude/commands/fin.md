---
description: Cierra la tarea en curso pasando por las dos puertas obligatorias
---

Cierra la tarea en curso. **Doble puerta: nadie se auto-aprueba.**

## Puerta 1 — Mecanica
- Los tests pasan.
- `git status --porcelain 02-datos/` sale VACIO (regla 26 de CLAUDE.md: los datos no entran en git).
- El entregable de la tarea existe en disco y se puede abrir.
- Ninguna referencia a decision `D-N` sin `grep` que la localice (regla 11 de CLAUDE.md).
- Ninguna referencia a codigo por numero de linea (regla 12 de CLAUDE.md).

## Puerta 2 — Revision por otro agente
- Codigo → invoca a `critico-codigo`.
- Estrategia o backtest → invoca a `validador`.
- El revisor NO puede ser quien hizo el trabajo.
- Su trabajo es encontrar motivos para rechazar. Un rechazo es un resultado valido.

## Si pasa
1. Marca `hecha` en el WBS con la fecha.
2. Añade al registro de pruebas si hubo prueba (solo añadir, nunca reescribir).
3. Commit: `[CODIGO]: [que se hizo]`.

## Si no pasa
1. Marca `bloqueada` con el motivo textual del revisor.
2. Si van 2 rondas de reparacion sin cerrar, PARA y escala al CEO. En el proyecto anterior, tres
   tareas seguidas murieron porque cada reparacion introducia un defecto nuevo (L de gb2).
