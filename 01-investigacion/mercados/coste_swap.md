# Coste de mantener posición de un día para otro (swap / financiación nocturna) — 8 instrumentos, 2-3 brokers

**Tarea:** 02.02.05 · **Rol:** investigador. Este informe SOLO mide y documenta el coste de mantener,
separando largo de corto. No elige mercado, no recomienda broker, no saca conclusiones sobre qué
instrumento "conviene". Es el criterio 2 de la puerta G1 (lunes 3 de agosto de 2026).

## TL;DR

- **El aviso conocido se confirma con fuente primaria, tal cual, sin suavizar**: el documento oficial de
  Pepperstone ("Costs and Charges Information & Examples", v5.0, feb-2025) publica un ejemplo de
  financiación de BTCUSD **largo −22,5 % anual**, muy por encima de cualquier spread razonable de
  entrada/salida.
- OANDA (a través de su filial regulada OANDA TMS Brokers S.A.) publica una tabla completa y **vigente
  esta misma semana** (2026.07.27–2026.08.02) con los 8 instrumentos. Es la fuente más completa y más
  actual de las tres.
- XTB publica una tabla completa para 7 de los 8 instrumentos (todo menos cripto), vigente desde el
  03-08-2026. **Hallazgo relevante para L-007**: en el documento consultado, XTB no ofrece BTCUSD ni
  ETHUSD como CFD apalancado — los ofrece como criptoactivo **al contado** (custodia gratuita, comisión
  0 %), así que **no tienen swap**: no es un hueco, es que el instrumento es distinto y no es comparable
  directamente con un CFD apalancado de otro broker.
- Pepperstone solo aportó una cifra verificable y fechada para **BTCUSD** (el ejemplo del propio
  documento). Para los otros 7 instrumentos no se consiguió una cifra actual fiable — se declara el
  hueco, no se estima.
- Donde dos brokers cubren el mismo instrumento (EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD), **el
  signo de largo/corto coincide entre OANDA y XTB** en los 6 casos: sirve como comprobación de cordura,
  no hay indicio de la inversión de signo que señala la lección L-006.

---

## Método

- **Unidad 1 — porcentaje anual**: tal como lo publica cada broker, o calculado por mí cuando el broker
  solo publica la tasa diaria (XTB): `% anual = % diario × 365` (conversión lineal, sin componer
  interés; se declara así para no disfrazar una cifra calculada de medida directa — regla 14).
- **Unidad 2 — coste en dólares por día**, sobre un **nocional declarado de 100.000 USD** igual para los
  8 instrumentos, para que las columnas en dólares sean comparables entre divisas, oro y cripto (lección
  L-004). Fórmula: `USD/día = 100.000 × (% anual / 100) / 365`. **Este nocional NO es necesariamente 1
  lote real del instrumento** (1 lote de oro son 100 onzas, hoy muy por encima de 100.000 USD; 1
  contrato de BTC también). Para dimensionar una posición real hay que usar el % anual sobre el nocional
  real, no esta cifra en dólares.
- Los signos se leen como: **negativo = coste que paga el cliente por mantener la posición; positivo =
  crédito que recibe el cliente.**
- Fecha de consulta de todas las fuentes: **31/07/2026**.

## Brokers consultados (grandes y regulados)

| Broker | Entidad exacta | Regulador(es) | Por qué cuenta como "grande" |
|---|---|---|---|
| OANDA | OANDA TMS Brokers S.A. | KNF (Polonia) | Broker multiactivo más antiguo de Polonia (desde 1997), adquirido por el grupo global OANDA en 2021 con aprobación del regulador polaco |
| XTB | XTB S.A. y entidades del grupo | KNF (Polonia), FCA (Reino Unido), CySEC (Chipre) | Cotiza en la Bolsa de Varsovia; uno de los brokers de CFD más grandes de Europa por clientes |
| Pepperstone | Pepperstone Limited | FCA (Reino Unido); grupo regulado también por ASIC (Australia), CySEC, DFSA | Broker global grande, citado explícitamente en el encargo por su financiación de BTC |

---

## Tabla — 8 instrumentos × 3 brokers × (largo/corto)

Formato de celda: **% anual · USD/día sobre 100.000 USD nocional**

| Instrumento | Posición | OANDA (TMS Brokers)¹ | XTB² | Pepperstone³ |
|---|---|---|---|---|
| EURUSD | Largo | −2,41 % · −6,60 $ | −3,01 % · −8,23 $ | sin dato fiable |
| EURUSD | Corto | +0,44 % · +1,21 $ | −0,04 % · −0,10 $ | sin dato fiable |
| GBPUSD | Largo | −0,88 % · −2,41 $ | −1,48 % · −4,05 $ | sin dato fiable |
| GBPUSD | Corto | −1,05 % · −2,88 $ | −1,54 % · −4,22 $ | sin dato fiable |
| USDJPY | Largo | +1,61 % · +4,41 $ | +0,68 % · +1,86 $ | sin dato fiable |
| USDJPY | Corto | −3,52 % · −9,64 $ | −4,73 % · −12,96 $ | sin dato fiable |
| AUDUSD | Largo | −0,28 % · −0,77 $ | −1,34 % · −3,67 $ | sin dato fiable |
| AUDUSD | Corto | −1,63 % · −4,47 $ | −2,68 % · −7,33 $ | sin dato fiable |
| USDCHF | Largo | +2,60 % · +7,12 $ | +2,22 % · +6,09 $ | sin dato fiable |
| USDCHF | Corto | −4,50 % · −12,33 $ | −5,26 % · −14,42 $ | sin dato fiable |
| XAUUSD ⁴ | Largo | −6,64 % · −18,19 $ | −8,16 % · −22,36 $ | sin dato fiable |
| XAUUSD ⁴ | Corto | +0,64 % · +1,75 $ | −0,76 % · −2,08 $ | sin dato fiable |
| BTCUSD | Largo | −33,64 % · −92,16 $ | no aplica (spot, no CFD) ⁵ | **−22,5 % · −61,64 $** (ejemplo oficial, feb-2025) |
| BTCUSD | Corto | −26,36 % · −72,22 $ | no aplica (spot, no CFD) ⁵ | **+7,5 % · +20,55 $** (ejemplo oficial, feb-2025) |
| ETHUSD | Largo | −33,64 % · −92,16 $ | no aplica (spot, no CFD) ⁵ | sin dato fiable |
| ETHUSD | Corto | −26,36 % · −72,22 $ | no aplica (spot, no CFD) ⁵ | sin dato fiable |

### Fuentes de la tabla

1. **OANDA (TMS Brokers S.A.)** — *"Swap Points Table"*, vigente **2026.07.27 – 2026.08.02**, publicado en
   % anual directamente. Documento oficial:
   `https://www.oanda.com/eu-en/document/91` → PDF `swap_points_tms_en_2026.07.27.pdf`. Consultado
   31/07/2026. Instrumentos citados: `EURUSD.pro`, `GBPUSD.pro`, `USDJPY.pro`, `AUDUSD.pro`,
   `USDCHF.pro`, `GOLD.pro`, `BTCUSD`, `ETHUSD`.
2. **XTB** — *"Table of Swap Points Rates and Financing Costs"*, efectivo desde **03-08-2026**, publicado
   en % diario (convertido a % anual por mí, ver Método). Documento oficial:
   `https://www.xtb.com/ae-en/swaps_ae.pdf` (redirige a
   `xas-new-cdn.xtb.com/file/0102/28/.../swaps-ae.pdf`). Consultado 31/07/2026. Tabla "CFD on FOREX,
   STANDARD"; oro en tabla "CFD on Commodities" bajo el símbolo `GOLD`.
3. **Pepperstone Limited** — *"Costs and Charges Information & Examples"*, versión 5.0, **actualizado
   febrero de 2025**. Documento oficial:
   `https://eu-assets.contentstack.com/v3/assets/.../Pepperstone_Limited_Cost_and_Charges_-_February_2025_.pdf`.
   Consultado 31/07/2026. La cifra de BTCUSD es el **"Example 4 — Swap for Crypto"** del propio
   documento ("Pepperstone swap rate — Long –22.5% yearly charge / Short +7.5% yearly charge"), no una
   tabla de valores en vivo: el documento mismo advierte que "estas son representaciones y ejemplos...
   sujetas a cambio" y remite a la plataforma para la cifra del día.
4. XAUUSD tratado como "oro al contado", ver advertencia 2 más abajo (L-007).
5. Ver advertencia 3.

---

## Advertencias

1. **Aviso del encargo, confirmado tal cual.** La financiación de BTCUSD largo en Pepperstone es −22,5 %
   anual según su propio documento oficial (Example 4), muy por encima del spread mínimo publicado en el
   mismo documento (10,00 puntos mínimo / 20,22 puntos medio, sobre un contrato de ~95.000 USD, es decir
   spread ≈ 0,01-0,02 % del nocional frente a un coste de mantener de varias veces esa magnitud **por
   día**). Se declara sin suavizar, tal como pide el encargo.

2. **Riesgo de instrumento — oro (L-007).** "GOLD.pro" (OANDA) y "GOLD" (XTB) se han tratado como proxy
   de XAUUSD al contado por dos motivos observados en los propios documentos: (a) OANDA lo agrupa en la
   misma tabla que las divisas, no en la de índices con lógica de rollover de futuro; (b) XTB usa para el
   oro una fórmula de diferencial de tasa base + margen, igual que para forex, no la fórmula de "basis
   entre contrato próximo y lejano" que sí usa explícitamente para índices. **No se ha podido confirmar
   con la ficha exacta de especificación de contrato de cada broker** que no exista ningún componente de
   futuro en el pricing. Pepperstone, además, documenta una fórmula de "Commodities and Treasuries" que
   **sí** referencia expresamente precio de "front-month future" y "next-month future" — lo cual sugiere
   que, si Pepperstone cotiza oro con esa fórmula, su producto podría no ser directamente comparable a
   OANDA/XTB. Recomendación: verificar la ficha de especificación de contrato exacta del broker elegido
   en la tarea 04.01.02, antes de dar esta cifra por definitiva.

3. **XTB no ofrece cripto como CFD apalancado en el documento consultado.** Su "Specification Table of
   Spot Cryptocurrencies" (vigente 12-06-2026,
   `https://www.xtb.com/cy/Crypto_Asset_Specifiation_table_12.06.2026.pdf`) muestra BTC y ETH con
   comisión 0 %, markup máximo 5 % incluido en precio, **custodia gratuita** y sin mención de swap: es
   compra real del activo (spot), no una posición apalancada con financiación nocturna. Por eso la celda
   dice "no aplica" y no "sin dato fiable": es un hallazgo real (no hay swap porque no es un CFD), no un
   hueco de búsqueda. **No es comparable directamente** con el coste de mantener un CFD apalancado de
   otro broker.

4. **La tabla de OANDA/TMS asigna la MISMA cifra a las 13 criptomonedas que ofrece** (ADAUSD, AVAXUSD,
   BCHUSD, BNBUSD, BTCUSD, DOGEUSD, DOTUSD, ETHUSD, LINKUSD, LTCUSD, MATICUSD, SOLUSD, UNIUSD: todas
   −33,64 % largo / −26,36 % corto). Es el dato tal como está publicado, no un error de transcripción de
   este informe: sugiere una tarifa plana de financiación cripto en ese broker, no calculada por moneda.

5. **Pepperstone: 6 de 8 instrumentos sin dato fiable, y se declara así en vez de estimarlo.** El
   documento oficial solo publica la fórmula general (TomNext + recargo de hasta el 3 %) y dos ejemplos
   numéricos: uno con AUDCAD (no está entre nuestros 8 instrumentos) y otro con BTCUSD. Un intento de
   leer la cifra "en vivo" en la página pública de Pepperstone para EURUSD devolvió **+0,00 % / +0,00 %**,
   un resultado que se descarta explícitamente por no fiable (con altísima probabilidad es un valor por
   defecto que se muestra antes de que la página cargue los datos reales vía JavaScript, no una tarifa
   real). No se usa en la tabla.

6. **Todas las cifras cambian con frecuencia.** OANDA publica una tabla nueva cada semana; XTB marca la
   suya "vigente desde" una fecha concreta; el propio Pepperstone dice que revisa "frequently". Los
   números de este informe son válidos para las fechas de consulta indicadas (semana del 27/07 al
   02/08/2026 para OANDA, desde el 03/08/2026 para XTB, febrero de 2025 para el ejemplo de Pepperstone) y
   **no deben tratarse como constantes** para calibrar un backtest. En 04.01.02 (recalcular costes con
   precios reales del broker elegido) hay que volver a tomar el dato del broker final, idealmente con
   histórico de swaps si el broker lo publica.

7. **Miércoles/jueves triple no está reflejado en esta tabla.** Tanto Pepperstone (miércoles, mercado
   forex) como XTB (jueves para USDTRY, miércoles para el resto de pares con triple swap) cobran tres
   veces la tarifa diaria un día de la semana para compensar el fin de semana sin mercado. Las cifras de
   esta tabla son el valor de una noche normal. El coste medio real de mantener entre semana es algo
   mayor que "% anual / 365" tal cual, porque reparte 7 noches de coste en 5 días de cotización (o el
   equivalente según convención de cada instrumento). No se ha recalculado con este ajuste: es un aviso
   de método para quien use estas cifras en el backtest.

8. **Fuentes intentadas y descartadas** (no incorporadas a la tabla porque no se pudieron leer o
   verificar completas):
   - **IG** (`ig.com`): la página oficial de ayuda sobre financiación nocturna devolvió error 403 al
     intentar leerla completa; un fragmento indexado por el buscador citaba un ejemplo con BTCUSD (16 %
     anual largo / 4 % anual corto, ambos con signo de coste), pero no se pudo confirmar leyendo el
     documento primario completo ni su fecha exacta. No se usa.
   - **IC Markets** (`ic.com`, antes `icmarkets.com`): página de tarifas de swap renderizada por
     JavaScript; no expuso una tabla de valores accesible sin ejecutar el navegador.
   - **myfxbook.com** y **forex.com**: bloquean el acceso automatizado (403) en las páginas de swaps.

## Huecos que quedan sin cubrir

- **Pepperstone**: sin dato fiable para EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF y XAUUSD (6 de 8
  instrumentos); y sin dato fiable para ETHUSD (el ejemplo oficial solo cubre BTCUSD).
- **XTB**: BTCUSD y ETHUSD no tienen swap porque el instrumento consultado es spot, no CFD — no es un
  hueco de búsqueda, pero significa que **solo hay un broker (OANDA) con cifra de CFD apalancado para
  ETHUSD**, por debajo del mínimo de 2 fuentes independientes que pide la regla de fuentes del proyecto
  para dar un dato por fiable. Se marca como advertencia, no se rellena con una tercera fuente de menor
  calidad.
- **XAUUSD**: cubierto por 2 brokers (OANDA, XTB), pero con la reserva de la advertencia 2 (no se
  confirmó documentalmente que ambos midan exactamente el mismo tipo de contrato que Pepperstone).
