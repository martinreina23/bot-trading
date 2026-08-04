# Fuente primaria — OANDA TMS Brokers S.A. — Swap Points Table (GOLD.pro)

**Broker / entidad exacta:** OANDA TMS Brokers S.A. (Polonia, regulador KNF).
**Documento:** "Swap Points Table — OANDA TMS Brokers S.A." — Valid from 2026.08.03 – 2026.08.09.
**URL origen:** https://www.oanda.com/eu-en/document/91 (redirige a un PDF con nombre de fichero
`swap_points_tms_en_2026.08.03.pdf`).
**Fecha de descarga:** 04/08/2026.
**Método de descarga:** herramienta WebFetch (el PDF se recibió como binario, decodificado con la
herramienta Read; el texto de abajo es transcripción literal de esa lectura).

## Cita literal (fila GOLD.pro, tabla "FOREX, CASH INDICES, CRYPTOCURENCIES")

> GOLD.pro | Long swap: -6.65% | Short swap: 0.65%

Cabecera de la tabla: "Published swap points are calculated in percentage points per annum."

## Nota de comparación con la medida anterior del proyecto

`01-investigacion/mercados/coste_swap.md` (tarea 02.02.05, fuente fechada 31/07/2026) midió para el
mismo instrumento y el mismo bróker: Largo −6,64 % anual, Corto +0,64 % anual. La tabla de esta
semana (03/08–09/08/2026) da −6,65 % / +0,65 %: variación de una centésima, coherente con que la
tabla se republica semanalmente (así lo advierte el propio documento).

## Cálculo en USD/día (nocional 100.000 USD, no es 1 lote real de oro)

- Largo: 100.000 × (−6,65/100) / 365 = **−18,22 USD/día**
- Corto: 100.000 × (0,65/100) / 365 = **+1,78 USD/día**

## Advertencia de identidad de entidad (importante, ver hallazgo en comparacion_brokers.md)

Este documento es de **OANDA TMS Brokers S.A.**, la única división de OANDA verificada en esta tarea
como NO compatible con la API REST v20 (ver `OANDA_api_v20_entidades_2026-08-04.md`). No se ha
verificado en esta sesión que el documento de horario de operación (`OANDA_horario_operacion_metales_2026-08-04.md`)
corresponda a esta misma entidad.
