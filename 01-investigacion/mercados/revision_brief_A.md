# Informe de revisión — tarea 02.03.01

**Revisor:** chat director · **Revisado:** entrega del chat analista (Brief A) · **Fecha:** 29/07/2026

Veredicto: **el trabajo es bueno en método y honesto en los huecos, pero no sirve todavía para decidir.** Tiene un error de cálculo real, un vacío de datos que invalida el 90% de la matriz, y le falta un coste que en algunos mercados manda sobre todos los demás. Ninguna de las tres cosas es culpa del analista: dos son del encargo que yo escribí.

---

## 1. Lo que está bien y se acepta

- **Costes de operar (Entrega 1): aceptados.** Fuentes primarias (PDF oficiales de Pepperstone e IC Markets, páginas de precios), con fecha del dato y distinguiendo cuenta raw/ECN de cuenta sin comisión. Es exactamente lo que se pedía.
- **Disciplina de "sin dato fiable": aceptada y valorada.** Dejó 22 de 24 celdas vacías en vez de rellenarlas con estimaciones disfrazadas de medida. Eso es lo que separa un análisis útil de uno decorativo.
- **Separación medida / estimación derivada: correcta.** Tablas 2-bis y 3-bis van etiquetadas como estimación y no se mezclan con las medidas.
- **Aritmética: verificada, correcta.** Recalculé las 24 celdas de la tabla 3-bis y los factores raíz-del-tiempo (0,102 / 0,204 / 0,408). Todo cuadra.
- **No sacó conclusiones ni recomendó mercado.** Cumplió el encargo.

## 2. ERROR CONFIRMADO — coste de USDJPY mal calculado

El analista detectó el problema y lo explicó bien en su nota de conversión, pero **luego no lo aplicó a su propia tabla.**

| Par | Valor del pip | Comisión 7 USD en pips | Coste total real | Coste que usó |
|---|---|---|---|---|
| USDJPY | 6,67 USD/lote | 1,05 pips | **1,16 pips** | 0,90 pips |
| USDCHF | 12,50 USD/lote | 0,56 pips | **0,73 pips** | 0,80 pips |

Efecto: **el coste relativo del USDJPY está infravalorado un 29%** en todas sus celdas (15m: 8,8% → 11,4%; 1h: 4,4% → 5,7%; 4h: 2,2% → 2,8%). El USDCHF está ligeramente sobrevalorado, sin consecuencia.

Esto importa porque el USDJPY aparecía como uno de los más baratos y no lo es tanto.

## 3. VACÍO DE DATOS — y su solución, que no es buscar más

El analista dice, con razón, que **no existe ATR intradía publicado de 2 años** para estos instrumentos. Es verdad y por eso 22 de 24 celdas quedaron vacías.

**Pero el encargo estaba mal planteado por mí.** Pedí *buscar* un dato que hay que *calcular*. El ATR intradía no es una cifra que alguien publica: es una cuenta que se hace sobre precios históricos, y los precios históricos sí están disponibles gratis. No hay que seguir buscando: hay que descargar precios y medirlos.

**Corrección de la tarea 02.02.01:** pasa de "buscar el movimiento medio publicado" a "descargar precios y calcular el ATR". Script listo: `atr_local.py`. Yahoo Finance da velas de 1 hora hasta 730 días (dos años exactos, justo lo que se pedía) y de 15 minutos hasta 60 días; las de 4 horas se construyen agrupando las de 1 hora.

Con eso, las 24 celdas pasan de "sin dato fiable" a medidas reales con periodo declarado y reproducibles por cualquiera.

## 4. FALTA UN COSTE, y en cripto manda sobre todos los demás

El analista lo señala en sus puntos ciegos y tiene toda la razón: **el coste de mantener la posición abierta de un día para otro (swap o financiación) no estaba en el encargo.**

Su dato: en CFD de bitcoin, Pepperstone cobra del orden de **-22,5% anual** en posiciones largas. Sobre 95.000 USD de nocional son unos **59 USD al día** — frente a un spread de 28 USD por operación completa. Es decir: **si la estrategia mantiene posiciones más de unas horas, en cripto CFD el coste dominante no es el spread, es la financiación.** El spread se paga una vez; la financiación se paga cada noche.

**Corrección al criterio 1 de la puerta G1:** el coste relativo se mide con dos números, no con uno: coste de entrar y salir (spread + comisión) y coste de mantener (swap diario). El segundo solo aplica si la estrategia aguanta posiciones de un día para otro, cosa que hoy no sabemos — pero medirlo ahora es barato y descubrirlo tarde es caro.

## 5. Hallazgo propio: comparar en porcentaje del precio

Los ATR en unidades naturales (pips, dólares por onza, dólares) **no son comparables entre sí**. Convertidos a porcentaje del precio, se ve el paisaje real:

| Instrumento | ATR diario como % del precio |
|---|---|
| USDCHF | 0,45% |
| EURUSD | 0,56% |
| USDJPY | 0,67% |
| GBPUSD | 0,87% |
| AUDUSD | 1,06% |
| BTCUSD | 3,08% |
| XAUUSD | 3,33% |
| ETHUSD | 6,97% |

El oro y el ether se mueven entre **6 y 15 veces más** que las divisas mayores. Eso confirma con números tu intuición inicial de que el forex tiene "menos picos", y explica por qué el oro sale barato en coste relativo pese a tener un spread mayor: el denominador es enorme.

*Aviso: estos porcentajes usan los ATR diarios del analista, que vienen de periodos distintos entre sí (10 semanas para EURUSD, 2014-2025 para GBPUSD, fotos de un solo día para BTC y ETH). Sirven para ver el orden de magnitud, no para decidir. El cálculo real los sustituye.*

## 6. Dato que hay que tirar

Los ATR de **BTC y ETH** del analista salen de fotos de un solo día (19-ago-2025 y 24-oct-2025), no de medias. Un ATR de bitcoin de una jornada concreta dice lo que pasó ese día y poco más. **No se usan.** El cálculo real los sustituye.

## 7. Qué pasa ahora

1. Ejecutar `atr_local.py` (tarea 02.02.01 corregida) → 24 celdas reales.
2. Lanzar el Brief B (correlaciones e historiales disponibles) — sigue válido tal cual.
3. Pedir al analista un anexo corto: swap/financiación diaria de los 8 instrumentos en 2-3 brokers.
4. Con las tres cosas, calibro los umbrales de G1 y preparo el informe de decisión (02.03.02).

## 8. Lecciones para LECCIONES.md

- **L-001:** Si un dato se puede calcular a partir de datos brutos disponibles, calcularlo; buscar el dato ya masticado hace perder tiempo y devuelve fuentes flojas.
- **L-002:** Toda conversión de unidades (comisión → pips) se aplica en la tabla final, no solo se explica en una nota al pie. El analista tenía la conversión correcta escrita y aun así usó el número sin convertir.
- **L-003:** Medir el coste de entrar y salir sin medir el coste de mantener la posición da una foto incompleta; en algunos mercados el segundo es varias veces mayor que el primero.
- **L-004:** Los valores absolutos no se comparan entre activos distintos. Se normaliza (porcentaje del precio) antes de comparar.
