# Fuente primaria — OANDA — Exclusión de la API v20 para TMS Brokers y Global Markets

**URL:** https://developer.oanda.com/rest-live-v20/introduction/
**Fecha de descarga/consulta:** 04/08/2026.
**Método:** WebFetch (fetch directo de la página; no PDF).

## Cita literal

> "To use this API you must have a v20 trading account, which is available to all divisions except
> OANDA Global Markets and OANDA TMS BROKERS S.A."

## Fuente secundaria de refuerzo (NO usada como fuente única, solo como corroboración)

`https://help.oanda.com/us/en/faqs/rest-v20-api-troubleshooting-guide.htm`, consultada la misma
fecha: la página muestra un selector de divisiones ("OANDA Corporation, OANDA (Canada) Corporation,
OANDA Europe Limited, OANDA Australia, OANDA Asia Pacific, OANDA Global Markets, OANDA TMS") pero no
repite la frase de exclusión con las mismas palabras; se usa solo para confirmar que "OANDA TMS" es
una división nombrada oficialmente por OANDA, no una etiqueta inventada en la búsqueda.

## Consecuencia para el criterio 6 (API) de la tabla de comparación

**OANDA TMS Brokers S.A. (Polonia, KNF) — la entidad usada para el dato de swap de oro en este
proyecto (ver `OANDA_swap_gold_2026-08-04.md` y `01-investigacion/mercados/coste_swap.md`) — NO
tiene acceso a la API REST v20**, según la propia documentación de desarrolladores de OANDA. Otras
divisiones de OANDA (Europa, Australia, Asia Pacífico, Canadá, Corporation) sí la tienen, pero sus
condiciones de oro (spread, swap, lote mínimo) NO se han verificado en esta tarea — sería mezclar
datos de dos entidades distintas bajo la misma marca, exactamente el error que L-007 de
LECCIONES.md advierte no cometer.
