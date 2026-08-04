# Fuente primaria — IC Markets Global — Commodity Specification Sheet (Gold)

**Entidad:** IC Markets Global (marca); el pie del documento da el teléfono con prefijo de Seychelles
(+248) y la ruta de descarga contiene "/FSA/", coherente con la entidad Raw Trading Ltd (Seychelles
FSA) — ver `ICMarkets_regulacion_2026-08-04.md`.
**URL:** https://cdn.icmarkets.com/uploads/FSA/Commodity-Specification-Sheet.pdf
**Fecha de descarga:** 04/08/2026.

## Cita literal — sección "Basic Information - Metals (Gold, Platinum, Palladium)"

> Spreads: Variable
> Stops Level: 0 (no minimum order distance)
> Contract size (MT4 Volume 1.00): 100
> Minimum Lot Size: 1 Oz (MT4 Volume 0.01)
> Maximum Lot Size: 10,000 Oz (MT4 Volume 100)
> Margin initial: 100.0 | Margin hedge: 50.0
> Min leverage: 1:1 | Max leverage: 1:500
> Commission (Raw Spread): 7AUD, 7CAD, 6.60CHF, 5.5EUR, 5GBP, 27.125HKD, 650JPY, 9NZD, 9SGD, 7USD per
> round turn lot

**Lectura:** contrato = 100 oz/lote (igual convención que los demás brókeres). Lote mínimo = 1 onza
(MT4 volumen 0,01). **No se ha encontrado en este documento una cifra de volumen mínimo por debajo
de 1 onza ni un paso de 0,1 onzas: se declara hueco explícito para el criterio de fraccionado de 0,1
oz.** La comisión citada es "Raw Spread" (cuenta con comisión aparte tipo Razor/Raw); no queda claro
en este documento si existe una cuenta "Standard" sin comisión para Metals (a diferencia de XTB y
Pepperstone, que sí la declaran explícitamente) — hueco declarado.

## Cita literal — tabla "Commodity Pairs" (spreads)

> XAUUSD | Gold in Dollar | Minimum Spread (pips): 0.00 | Average Spread (pips): 0.63

## Nota sobre horario (parcial, no resuelve la columna 8 completa)

> "*To align the daily chart candles with New York close (5pm ET) IC Markets Global server time and
> charts are GMT + 2 or GMT + 3 when daylight savings is in effect."

**Hueco declarado:** esta nota da el huso de servidor pero NO da la hora exacta de cierre del
viernes ni de apertura del domingo para XAUUSD. No se encontró en esta sesión una tabla de horario
de mercado específica de IC Markets para Gold con esos dos datos por fuente primaria propia.
