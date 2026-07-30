# Revisión independiente del Brief B — tarea 02.03.01 (segunda parte)

**Revisor:** chat director · **Fecha:** 30/07/2026

Veredicto: **entrega mejor que la del Brief A.** Reconoce el hueco estructural en vez de taparlo, documenta las convenciones que rompen las comparaciones, y su hallazgo principal coincide exactamente con el del Brief A. Tres cosas suyas corrigen errores míos.

---

## 1. El mismo hallazgo, por segunda vez: hay que calcular, no buscar

El analista concluye que **no existe ninguna fuente pública con una matriz 8×8 homogénea** — las herramientas de forex no incluyen cripto, las de cripto usan convenciones distintas, y los periodos no coinciden. Su recomendación es calcularla nosotros.

Es la segunda vez en dos entregas que el dato pedido no existe publicado y sí se puede calcular. **La lección L-001 queda confirmada por partida doble y sube de categoría: pasa a ser regla del proyecto**, no lección. Todo dato numérico del proyecto se calcula sobre datos brutos salvo que se demuestre que existe una fuente primaria homogénea.

## 2. Desbloquea la tarea 02.02.04 y también la 04.01.03

La respuesta sobre históricos disponibles es la mejor noticia del día:

| Fuente | Qué da | Desde | Coste |
|---|---|---|---|
| **Dukascopy** | Tick con precio de compra y de venta, forex y **oro al contado** | 2003 (cripto desde 2017) | Gratis con cuenta demo |
| **HistData** | 1 minuto y tick | ~20 años | Gratis, sin cuenta |
| **TrueFX** | Tick con compra/venta, agregado de bancos | 2009 | Gratis con registro |
| **Binance (data.binance.vision)** | 1 minuto y operaciones individuales | ago-2017 | Gratis, sin cuenta |
| **Kraken** | 1 minuto, BTC/USD **real** (no Tether) | inicio de mercado | Gratis |

Nuestro criterio de G1 pedía **mínimo 5 años**; hay **más de 20** en forex y oro, y 9 en cripto, todo gratis y con precio de compra y venta separados (que es lo que permite medir el coste real en el backtest). **El criterio 3 de la puerta G1 deja de discriminar**: lo cumplen los 8 candidatos con holgura. Se mantiene como comprobación, no como filtro.

## 3. TRES CORRECCIONES A MI PROPIO TRABAJO

**3.1 Mi script mide el oro equivocado.** `atr_local.py` usa `GC=F`, que es el **futuro** de oro de COMEX, no el oro al contado (XAUUSD) que operaría el bot. El analista lo señala con dato: su correlación es 0,82 — alta, pero no son el mismo instrumento. Corregido en `medir.py`: el oro al contado se baja de Dukascopy o HistData, y si se usa el futuro queda marcado como aproximación.

**3.2 El bitcoin de Binance no es bitcoin contra dólares.** Los datos de `data.binance.vision` son BTC contra Tether (USDT), no contra dólar real. Para medir coste relativo contra un broker que cotiza en dólares hay que usar Kraken o Dukascopy. Diferencia pequeña, pero es exactamente el tipo de detalle que envenena un backtest sin que se note.

**3.3 Una sola ventana de correlación no vale.** El analista demuestra con números que la correlación cambia radicalmente según el periodo: EURUSD-AUDUSD sale 0,33 en una tabla y 0,64 a 12 meses; BTC-ETH 0,85 a un año y 0,66 en todo el histórico; BTC-oro pasó de +0,30 de media a **-0,88** en marzo de 2026. **Nuestro criterio 4 de G1 ("correlación menor de 0,7") era ingenuo tal como estaba escrito.** Corregido: se calcula en tres ventanas (3 meses, 1 año, 2 años) y el criterio pasa a ser *"que no supere 0,7 en ninguna de las tres"*, más una nota de estabilidad.

## 4. HALLAZGO QUE CAMBIA LA DECISIÓN DE G1

Parte de la correlación entre pares de divisas **no es información de mercado: es aritmética**. Los pares comparten el dólar, así que se mueven en espejo o en paralelo por construcción:

- **EURUSD y USDCHF: -0,97.** Son casi la misma apuesta invertida.
- **EURUSD y GBPUSD: +0,91** (en otra ventana, +0,59).
- **GBPUSD y AUDUSD: +0,69.**

Consecuencia directa: **un portafolio de 5 pares de divisas mayores no es un portafolio de 5 apuestas.** Es aproximadamente una apuesta sobre el dólar, repetida cinco veces. Cuando el dólar se mueva, se moverán todos a la vez — exactamente lo que el criterio 4 existe para impedir.

Y al revés: la diversificación real, si la queremos, probablemente exige **mezclar clases de activo** (divisas + oro + cripto), no elegir más pares de divisas. Es lo contrario de lo que sugería tu idea inicial de "4 o 5 pares de forex".

Esto no lo decido yo: lo lleva el informe de decisión de G1 con los números calculados delante. Pero conviene que lo sepas antes de leerlo.

## 5. Puntos ciegos que el analista señala y son válidos

1. **La correlación diaria no es la correlación intradía.** Un bot de 15 minutos o 1 hora vive en una escala donde las correlaciones son más bajas y más ruidosas. Si el portafolio se dimensiona con correlaciones diarias, se está usando el número equivocado. Lo incorporo: la matriz se calcula también en la vela que elijamos.
2. **La hora de corte del día distorsiona las correlaciones entre clases.** El forex opera 24 horas 5 días, el oro al contado tiene pausas y la cripto no para nunca. Si el "día" se corta a horas distintas, los rendimientos no coinciden y la correlación medida es falsa. Hay que fijar una hora de corte única (propuesta: 22:00 UTC, el cierre convencional del día en forex) antes de calcular nada.
3. **Una matriz de 2 años es una foto, no una constante.**

## 6. Lo que NO se acepta

Los valores de la tabla clásica de correlaciones (etiquetados `[M]` en su informe) **no tienen periodo declarado**. Sirven para ver el patrón estructural —qué signos y qué magnitudes cabe esperar— y **no** para decidir. Se usan como comprobación de cordura del cálculo propio: si nuestra matriz calculada diera EURUSD-USDCHF positivo, sabríamos que hemos metido la pata.

## 7. Lecciones nuevas

- **L-006:** Si dos fuentes usan convenciones distintas (yen y franco invertidos), sus números tienen el signo cambiado. Antes de comparar, se verifica la convención.
- **L-007:** Un instrumento con nombre parecido no es el mismo instrumento: oro al contado ≠ futuro de oro; bitcoin contra Tether ≠ bitcoin contra dólar. Se comprueba qué se está midiendo antes de medirlo.
- **L-008:** Un umbral sobre una magnitud inestable necesita varias ventanas, no una. Un solo número es una foto.
