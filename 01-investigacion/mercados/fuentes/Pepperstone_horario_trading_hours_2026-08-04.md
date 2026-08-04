# Fuente primaria — Pepperstone — Horario de negociación del oro (XAUUSD)

**URL:** https://pepperstone.com/en/ways-to-trade/trading-hours/
**Fecha de consulta:** 04/08/2026. **Método:** WebFetch (página HTML, no PDF).

## Cita extraída (tabla de Commodities/Metals de la página, resumida por la herramienta de fetch,
no transcripción carácter a carácter del HTML porque la página no se guardó como fichero binario)

> Gold (XAUUSD) opera de "01:01 - 23:59" de lunes a jueves, y "01:01 - 23:55" el viernes, con mercado
> cerrado sábado y domingo.
> "All times set to GMT+3 (Server time)" — declarado en la cabecera de la sección de horarios de la
> página.
> No se menciona pausa intradía para el oro.

## Conversión a UTC (regla 14 de CLAUDE.md: cálculo declarado sobre el dato bruto, no medida directa)

Con el huso GMT+3 que la propia página declara en el momento de la consulta (04/08/2026):

- **Cierre del viernes:** 23:55 GMT+3 → **20:55 UTC**.
- **Apertura tras el fin de semana:** la tabla dice "lunes 01:01" en horario de servidor GMT+3, que
  equivale a **domingo 22:01 UTC** (01:01 del lunes menos 3 horas cae en el día anterior). Es
  coherente con la convención habitual del mercado del oro (apertura domingo ~22:00 UTC).

## Advertencia declarada, no disimulada

Pepperstone advierte en otras páginas (no citadas aquí como fuente primaria porque no se pudieron
guardar) que su huso de servidor cambia entre GMT+2 y GMT+3 según el horario de verano de EE. UU.
(no de Europa). **La cifra GMT+3 de esta ficha es la vigente en la fecha de consulta (04/08/2026,
verano en EE. UU.)**; no se garantiza que sea constante todo el año. Se declara como limitación, no
se calcula el valor de invierno porque no hay fuente primaria propia consultada para ese caso.
