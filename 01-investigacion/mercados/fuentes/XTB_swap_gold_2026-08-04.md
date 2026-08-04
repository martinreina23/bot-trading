# Fuente primaria — XTB — Swap Points / Financing Costs, fila GOLD

**Entidad:** XTB (documento con entidad "AE" en la URL — Emiratos Árabes Unidos; mismo grupo XTB que
publica la tabla CY de especificación; XTB opera un pricing/swap común documentado por instrumento,
no por país, según se lee en el propio documento).
**Documento:** "Table of Swap Points Rates and Financing Costs — Effective from 03-08-2026".
**URL origen:** https://www.xtb.com/ae-en/swaps_ae.pdf → redirige a
`https://xas-new-cdn.xtb.com/file/0102/28/701b4b31-64ad-451c-95f6-055569bea899/swaps-ae.pdf`
**Fecha de descarga:** 04/08/2026.

## Cita literal — tabla "CFD on Derivative Instruments on Indices and Commodities", subtabla
"Table of Swap Points Rates ... CFD on Commodities", cuenta STANDARD

> GOLD | Long Position: -0.022361% | Short Position: -0.002083%

(Valores diarios, en %. Fórmula declarada en el documento: para posiciones cortas en CFD, "the
Financing Cost value cannot be positive" — coherente con el signo negativo también en corto.)

## Cálculo de conversión a % anual (regla 14 de CLAUDE.md: cálculo declarado, no medida directa)

- Largo: −0,022361 % × 365 = **−8,16 % anual**
- Corto: −0,002083 % × 365 = **−0,76 % anual**

Coincide con la cifra ya registrada en `01-investigacion/mercados/coste_swap.md` (tarea 02.02.05,
fuente del 31/07/2026): Largo −8,16 % anual, Corto −0,76 % anual. Confirmado con documento vigente
al 03/08/2026, sin cambios frente a la semana anterior.

## Nota de instrumento

Este documento no repite la clasificación spot/futuro; esa evidencia vive en
`XTB_especificacion_contrato_oro_2026-08-04.md` (nota 5 y la ausencia de asterisco en la fila GOLD).
