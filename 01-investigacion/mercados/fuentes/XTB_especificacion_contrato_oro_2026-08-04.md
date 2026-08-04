# Fuente primaria — XTB — Especificación de contrato GOLD (CFD sobre oro)

**Entidad:** XTB Limited (Chipre), licencia CySEC 169/12 (ver `XTB_regulador_icf_2026-08-04.md`).
**Documento:** "Specification Table of CFD derivatives on currencies, indices, commodities and
cryptocurrencies", entidad "CY".
**URL origen:** https://xtb.scdn5.secure.raxcdn.com/file/0104/23/fb5ed011-69ba-41c4-a36e-c2bc9dd07653/specification-table-27092025-cy.pdf
**Fecha de descarga:** 04/08/2026. **Fecha de vigencia del documento:** no lleva fecha explícita en
cabecera; se referencia en la URL "27092025" (27/09/2025); se declara así, no se disfraza de
"vigente hoy".

## Cita literal — fila GOLD (tabla "CFD on commodities")

> GOLD | Gold | Instrument level * USD 100 | 1 | 0.01 | 0,003 | 0,001 | 12:00 am - 11:00 pm | variable | 0,35 | 0,35

Columnas en orden: Instrument, Underlying instrument, Nominal Value of one Lot, Size of one PIP,
Minimum Quotation Step (in points), Minimum Order Size in Lots, Minimum Transaction Step in Lots,
Trading Hours, Spread, Standard Transaction Spread (8-23 CET/CEST), Standard Transaction Spread (24-8
CET/CEST).

**Lectura:** 1 lote = 100 onzas (nominal = precio del oro × 100). Pedido mínimo = 0,003 lotes = 0,3
onzas. Paso mínimo de transacción = 0,001 lotes = **0,1 onzas exactas**. Spread estándar publicado:
0,35 (mismo valor en ambas franjas horarias); unidad no declarada explícitamente en la tabla, se
interpreta como USD por onza por continuidad con el resto de la fila (no se presenta como medida
verbatim, se marca como interpretación).

## Cita literal — tabla "Transaction volumes for experienced and professional clients"

> GOLD | 0,01 | 0,01

(Mínimo de orden y paso mínimo en lotes para clientes profesionales — 0,01 lote = 1 onza, MAYOR que
el mínimo de cliente retail. Confirma que el mínimo de 0,1 oz de paso solo aplica a cuentas retail.)

## Citas literales — notas generales relevantes

> Nota 1: "Minimum Quotation Step is the minimum value, by which the price of all quoted Financial
> Instruments may be changed."
> Nota 4: "On Fridays trading on instruments in XTB is possible till 22:00. This also applies to
> instruments which underlying market allows trading beyond 22:00."
> Nota 5: "XTB reserves that Financial Instruments, for which the Underlying Instruments are actual
> values of stock indices or future contracts on stock indices or future contracts on commodities,
> are the instruments of 'over-the-counter' nature..." — **la fila GOLD no lleva el asterisco que
> marca esta nota** (a diferencia de filas de índices como "S&P/ASX 200*"), lo que indica que XTB NO
> clasifica el oro dentro de los instrumentos "referenciados a futuro" de esta nota.
> Nota 18: "Trading on CFD on currencies, indices and commodities is not available during weekend,
> unless otherwise stated in the table above."
> Nota general de horario (sección "Trading hours"): "Trading hours of particular Financial
> Instruments in the period from last Sunday of October till last Saturday of March are expressed in
> central european time (CET), while central european summer time (CEST) is used to express trading
> hours in period from last Sunday of March till last Saturday of October."

## Hueco declarado

La tabla NO da una hora de apertura del domingo específica para GOLD (a diferencia de las filas de
forex, que sí llevan literalmente "24 h from Sunday 11:00 pm to Friday 10:00 pm"). La fila de GOLD
solo dice "12:00 am - 11:00 pm", sin mención del domingo. **No se infiere una hora de apertura del
domingo**: se declara hueco en la columna 8 de la tabla de comparación.
