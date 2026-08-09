# Fuente primaria — OANDA Asia Pacific Pte Ltd (Singapur) — Minimum trade size (NO es la entidad que admite España)

**URL:** https://help.oanda.com/sg/en/faqs/minimum-trade-size.htm
**Fecha de consulta:** 06/08/2026. Método: WebFetch (HTML).
**Motivo de esta búsqueda:** pista dada por el orquestador — `evidencia_umbrales_g1.md`, sección 6,
citaba (marcada "fuente con reserva, no leída completa") que "OANDA declara un mínimo de 0,1
unidades de oro". Se ha perseguido esa pista hasta la fuente primaria exacta.

## Cita literal — tabla de tamaños mínimos de operación

> Gold CFD | 0.1 | 0.01 | 0.001

**Terminología de la propia página:** la columna correspondiente a la "plataforma OANDA" (fxTrade)
usa **"units"** (unidades); las columnas de MT4 y MT5 usan **"lots"** (lotes).

## Cita literal — pie de página, identidad de la entidad

> "OANDA Asia Pacific Pte Ltd (Co. Reg. No 200704926K)"

## Lectura — NO CONFIRMA el dato para la entidad que admite a España

**Esta es una entidad DISTINTA de OANDA TMS Brokers S.A.** (Polonia, KNF), la entidad que la ronda 3
de esta tarea confirmó admitiendo a un residente en España vía libre prestación de servicios
(ver `CNMV_registro_OANDA_TMS_2026-08-06.md`). OANDA Asia Pacific Pte Ltd es la entidad de
Singapur, que usa la plataforma propietaria "OANDA" (fxTrade) con tamaño en unidades — una
plataforma y un modelo de producto **distintos** del que usa OANDA TMS Brokers S.A., cuya propia
especificación de 72 páginas (`OANDA_TMS_full_specification_2026-08-06.md`) usa lotes de estilo
MetaTrader/TMS Connect (símbolos con sufijo ".pro") y **no incluye ninguna columna de lote mínimo**.

**No hay ninguna base para trasladar la cifra de 0,1 unidades de Singapur a la entidad polaca**: son
dos entidades, dos reguladores (MAS de Singapur vs. KNF de Polonia) y, aparentemente, dos
plataformas de producto distintas. Se comprueba así, con fuente primaria, la reserva que
`evidencia_umbrales_g1.md` ya declaraba ("no leída completa", "posiblemente otra entidad del
grupo"): **era correcta.** El dato de 0,1 unidades es real y confirmado ahora con cita primaria
completa, pero **pertenece a una entidad que no admite a un residente en España** (o al menos no
hay indicio de que lo haga: no se ha buscado si OANDA Asia Pacific Pte Ltd tiene registro CNMV,
pero es más plausible que su ámbito sea APAC).

**Conclusión para el criterio 1 de la tabla de comparación: sigue en HUECO para OANDA TMS Brokers
S.A.** (la entidad admitente). El «cabo suelto» que señalaba el orquestador queda atado: se sabe
ahora exactamente de dónde salía la cifra de 0,1 y por qué no vale como confirmación para la entidad
correcta.
