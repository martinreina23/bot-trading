# Fuente primaria — OANDA — Hours of Operation (Metales / XAU)

**Documento:** "Hours of Operation", encontrado en `https://www.oanda.com/assets/documents/422/Hours_of_Operation_SG.pdf`.
**Fecha de descarga:** 04/08/2026.
**Advertencia de entidad, sin resolver:** el nombre del fichero contiene el sufijo "_SG", lo que
sugiere una división regional de Asia-Pacífico / Singapur. El propio documento NO declara en el
texto extraído qué entidad legal exacta lo publica (solo el logotipo "OANDA" genérico). **No se ha
podido confirmar en esta sesión que esta sea la misma entidad (OANDA TMS Brokers S.A., Polonia)
usada para el dato de swap.** Se declara como hueco de consistencia de entidad, no se fuerza el
encaje.

## Cita literal — sección "Metals"

> All Gold Instruments (XAU) | Max Units per Trade: 1000 | Max Leverage: 5:1 |
> Trading Hours (GMT): Sun-Thurs: 23:00 – 22:15 (next day), Thurs-Fri: 23:00 – 22:00 (next day)

## Cita literal — texto general de la cabecera del documento

> "OANDA's hours of operation coincide with the global financial markets. Trading is available from
> Sunday approximately 5pm to Friday 5pm (New York time)."
> "Spreads (the difference between the bid price and the ask price) typically widen at 4:00 p.m.
> Friday, to reflect decreased liquidity in the global markets."
> "Trading hours are based on when underlying futures reference markets are open. OANDA CFDs will
> not be available for trading during holidays in which reference markets are closed."
> "OANDA prices are calculated from the theoretical spot prices derived from underlying futures."

## Lectura para la tabla de comparación (columna 8, huso UTC)

Tomando el dato literal en GMT (equivalente a UTC, sin componente horario de verano declarado en el
documento):

- **Apertura tras el fin de semana:** domingo 23:00 UTC (fila "Sun-Thurs" arranca a las 23:00).
- **Cierre de la sesión del viernes:** viernes 22:00 UTC (fila "Thurs-Fri" cierra a las 22:00, frente
  a las 22:15 del resto de días).
- **Pausa diaria:** 45 minutos, entre el cierre de una sesión (22:00 o 22:15) y la reapertura a las
  23:00, de domingo a jueves.

## Advertencia adicional

La última frase citada ("OANDA prices are calculated from the theoretical spot prices derived from
underlying futures") es relevante para el criterio 4 (contado vs. futuro): el propio documento dice
que el precio de OANDA se deriva de futuros subyacentes, no que sea un precio "spot" puro. Esto se
traslada como advertencia a la tabla de comparación, no se suaviza.
