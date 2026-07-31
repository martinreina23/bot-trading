# Veredicto del validador — Propuesta de criterios de la puerta G1 (tarea 01.01.02)

**Agente:** `validador` (`claude-fable-5`, sin respaldo necesario: el modelo principal respondió).
**Fecha:** 31/07/2026. **Papel:** intentar tumbar la propuesta C1-C7 antes de que llegue al CEO.
**Método:** regla 9 (todo lo afirmado aquí va con experimento ejecutado o grep con fichero; lo que no,
se marca NO PROBADO). No he construido ningún criterio: exijo cambios mínimos y señalo el dato que
los sostiene, que ya existe. No se ha tocado `02-datos/reservado/` en ningún momento.

---

## VEREDICTO GLOBAL: NO PASA tal como está redactada — SE SOSTIENE CON CAMBIOS

La dirección de la propuesta (filtrar por coste, elegir vela por arrastre anual, sacar C7 de G1)
sobrevive a los ataques. Pero **dos criterios tienen defectos demostrados por ejecución** (C1 en su
construcción, C6 en su aplicación al oro), **un parámetro central no existe en ningún documento
firmado** (el retorno objetivo del 15%), y **falta un riesgo cuantificado que pierde dinero y no
aparece en ninguno de los siete** (huecos de fin de semana que saltan el stop entero 6-9 veces al
año). Con los 6 cambios de la sección final, puede volver a presentarse al CEO.

---

## Ataques que SÍ han tumbado algo (con su experimento)

### A1 — El retorno objetivo del 15% no está escrito en ningún sitio (frente 1, parcial)

**Experimento (grep, regla 12):** `grep -rn -i "retorno|objetivo|carver|arrastre" 00-direccion/`
devuelve **cero** apariciones de un retorno objetivo, de Carver, del umbral del 5% o de la palabra
arrastre. El 15% anual es un parámetro que el orquestador introduce con la propuesta, sin decisión
previa en `DECISIONES.md` ni en el WBS.

**Lo que NO se tumba:** el umbral no está amañado para que salga 4h. Experimento ejecutado sobre
`arrastre_coste_anual.json` (escenario central, mediana): para que 1h pasara entero haría falta un
umbral >25,17%, que bajo el ancla de Carver implica declarar un retorno pre-coste del **75,5%
anual** — indefendible. Barrido de retornos defendibles: con 10% / 15% / 20% / 30% de objetivo
(umbral 3,33 / 5,00 / 6,67 / 10,00%), 1h pasa 0/6, 0/6, 0/6 y 1/6; 4h pasa 6/6 en los cuatro casos.
El veredicto de vela es insensible al objetivo elegido **dentro del modelo de actividad porcentual**
(ver A2 para lo que ese modelo esconde).

**Cambio exigido:** el 15% se presenta al CEO como decisión explícita (una letra en la ficha), no
como dato. Y la cita de Carver es de coste **TOTAL** ("expected pre-cost returns on costs",
`evidencia_umbrales_g1.md`, sección 1): gastar todo el presupuesto solo en entrar/salir malinterpreta
el ancla (ver A4).

### A2 — C1 no elige la vela: elige un número de operaciones, y lo esconde (frente 3)

**Experimento:** recalculado el arrastre anual fijando el NÚMERO de operaciones/año en vez del % de
velas (riesgo 1%, stop 1xATR, coste relativo mediana de `arrastre_coste_anual.json`):

| N ops/año | 15m | 1h | 4h |
|---|---|---|---|
| 100 | 4,78–17,02% (pasa 1/6: XAUUSD) | 2,31–8,10% (**pasa 1/6: XAUUSD 2,31%**; GBPUSD 5,13 y USDJPY 5,03 a décimas del umbral) | 1,17–3,98% (pasan 6/6) |
| 250 | 11,95–42,56% (0/6) | 5,76–20,24% (0/6) | 2,93–9,94% (**pasa 1/6: falla 5/6**) |
| 500 | 23,90–85,12% (0/6) | 11,53–40,49% (0/6) | 5,87–19,88% (**0/6**) |

Consecuencias probadas:
- **"1h falla para todos" NO sobrevive:** a igualdad de operaciones (N=100), XAUUSD 1h pasa con
  margen y tres divisas quedan al filo. La cifra "6,81–25,17%" de la propuesta es un artefacto de
  asumir 311 ops/año a 1h frente a 81 a 4h.
- **"4h pasa" tampoco es incondicional:** una estrategia de 250 ops/año a 4h (actividad 15,5%,
  perfectamente posible) revienta el umbral en 5 de 6 instrumentos.
- **Lo que SÍ sobrevive:** el orden. Por operación, 4h es ~2,05x más barato que 1h y ~4,4x que 15m
  en todas las filas; y 15m es el peor en cualquier formulación. La preferencia por 4h es real;
  la eliminación absoluta de 1h no lo es.

**Reformulación honesta de C1 (dato ya calculado):** tope de operaciones/año que caben en el 5%
por instrumento y vela — 15m: 29–105 · 1h: 62–217 · 4h: 126–426. C1 debe presentarse así, o
declarar como supuesto de validez "estrategia de señal por vela con actividad 2–10%".

### A3 — C6 tumba el oro con el estimador que el propio proyecto corrigió, y con el lote de un broker que aún no se ha elegido (frente 5)

**Experimento 1 (estimador):** la cifra de la propuesta (~2.518 EUR) usa `atr14_medio`, que
`coste_relativo.md` (sección "CORRECCIÓN 31/07") demostró inflado un 28–30% para XAUUSD por su pausa
diaria — el único instrumento con ese sesgo. Recalculado con `atr14_mediana` (22,15 USD/oz):
**2.215 USD = 1.962 EUR → cabe en el techo declarado de 2.000 EUR** (no en 1.500).

**Experimento 2 (fuente del lote, verificación documental):** `evidencia_umbrales_g1.md`, sección 6:
el lote mínimo de 1 oz es de **IC Markets** (PDF primario, leído completo — fuente sólida), pero el
mismo documento recoge que **OANDA declara mínimo 0,1 unidades de oro** (fuente con reserva, no
leída completa). Con 0,1 oz el capital necesario es ~252 EUR: el problema desaparece. El broker se
elige en **04.01.01, DESPUÉS de G1**.

**Dictamen:** C6 es un criterio correcto y necesario (nadie había mirado el dimensionado), pero
**no elimina el oro: impone un requisito al broker**. Eliminarlo en G1 por el lote de un broker no
elegido, calculado con el estimador sesgado, es un falso negativo.

### A4 — C1+C3 dejan el swap fuera del presupuesto, y a 4h el swap es tan grande como todo el arrastre de C1 (ataque emergido de los frentes 4 y 6)

**Experimento:** con el dimensionado de C6 (riesgo 1%, stop 1xATR mediana 4h), el nocional es
1,6x–4,3x el capital. Coste de swap por noche (OANDA, largo, `coste_swap.md`) sobre ese nocional,
multiplicado por las 80,6 ops/año del escenario central de C1:

| Instrumento | Arrastre C1 (4h) | Swap con 1 noche/op | Con 2 noches/op | Total 2 noches |
|---|---|---|---|---|
| EURUSD largo | 2,45% | +2,28% | +4,56% | **7,01% > 5%** |
| XAUUSD largo | 0,94% | +2,36% | +4,72% | **5,66% > 5%** |
| GBPUSD largo | 2,05% | +0,79% | +1,59% | 3,64% |

Una posición de vela 4h cruza noches casi por definición. El ancla de Carver es de coste TOTAL;
C1 gasta el 100% del presupuesto en entrar/salir y C3 se limita a "declarar y restringir" sin tope
numérico. Tal como está, la combinación aprueba con 0,94–3,20% instrumentos cuyo coste real anual,
con solo 1–2 noches por operación en largo, dobla o revienta el umbral. (La dirección importa:
EURUSD corto y USDJPY/USDCHF largo son crédito — el dato por dirección ya está en `coste_swap.md`.)

### A5 — Falta un criterio: el hueco de fin de semana salta el stop entero 6-9 veces al año (frente 6)

**Experimento (sobre `02-datos/bruto/`, ~2 años de velas 1m, 6 instrumentos no-cripto):** hueco =
|apertura tras pausa >4h − cierre previo|, comparado con el stop de 1xATR(4h) mediana:

| Instrumento | p90 hueco/ATR4h | máx | huecos >1xATR por año |
|---|---|---|---|
| EURUSD | 1,42x | 4,84x | 8,9 |
| GBPUSD | 1,05x | 3,30x | 6,3 |
| USDJPY | 1,13x | 4,33x | 5,8 |
| AUDUSD | 1,38x | 3,54x | 7,9 |
| USDCHF | 1,17x | 2,36x | 8,9 |
| XAUUSD | 1,34x | 5,05x | 8,0 |

Verificado que los 5 mayores huecos de EURUSD y XAUUSD son todos viernes→domingo (fin de semana
real, no fallo de datos). Lectura: una operación "de riesgo 1%" mantenida el fin de semana puede
perder de golpe **hasta 5x su riesgo nominal** (el stop no ejecuta dentro del hueco), y no es un
suceso raro: el hueco del lunes supera el stop ENTERO 6–9 veces al año en todos los instrumentos
no-cripto. Ninguno de los siete criterios lo contempla. Cripto (24/7) no lo sufre: **distingue
mercados**, que es lo que G1 exige de un criterio. El dato ya existe (este cálculo, reproducible
sobre `02-datos/bruto/`).

**Solo propongo UNO adicional, no dos.** El segundo candidato (coste por hora del reloj / rollover
de 22:00 UTC) **no es calculable con lo descargado**: los brutos son OHLC BID sin ask (verificado
leyendo `02-datos/bruto/EURUSD/1m.csv.gz`: columnas `ts_utc,open,high,low,close`), así que declarar
un umbral sería inventar. Queda como cálculo pendiente si se descargan datos con bid/ask
(Dukascopy tick los tiene), tal como ya anota `evidencia_umbrales_g1.md` §7.

---

## Ataques que NO han tumbado (y lo digo igual de claro)

- **Frente 2 (¿4h destruye la muestra?):** NO tumba. A 4h: actividad 2% / 5% / 10% → 32 / 81 / 161
  ops/año/instrumento; cartera de 3 → 97 / 242 / 483 ops/año; backtest de 2 años cartera → 193 /
  483 / 967. La muestra se adelgaza (a 15m serían 1.245 ops/año/instrumento) pero no muere: el punto
  débil real es el cajón OOS (48–121 ops de cartera en 6 meses; 16/instrumento con actividad 2%).
  La salida ya está confirmada por 02.02.04: hay 20+ años gratis (Dukascopy desde 2003). Elegir 4h
  obliga a ampliar el histórico antes de partir los cajones (04.01.03) — condición, no veto.
- **Frente 4 (¿C2 y C1 miden lo mismo dos veces?):** NO. C1 = mediana × frecuencia (presupuesto
  anual, elige vela); C2 = cola p10 por operación (viabilidad en vela tranquila, filtra
  instrumento). Comparten familia de cociente pero muerden en márgenes distintos: en 4h, C2 solo
  elimina a ETHUSD (p10 15,13%/35,37% > 10%) y **es el único filtro de coste operativo sobre
  cripto**, porque C1 es HUECO ahí (sin velas/año de Kraken, declarado en `arrastre_coste.md` §3).
  No hay doble conteo eliminatorio. C2 se queda.
- **C4 (muestra):** defendible tal como está. El DSR usa T (longitud de la muestra de observaciones)
  y el suelo de 1.000 velas/año lo alimenta (4h da 1.611); la negativa a fijar un mínimo de
  operaciones es honesta: `evidencia_umbrales_g1.md` §2 verificó que la cifra "300 operaciones" era
  una alucinación de WebFetch que no está en el paper, y que la atribución "200-500 a López de
  Prado" no se pudo verificar. No invento la objeción que la literatura no da.
- **C7 (sacar "operable sin nadie delante"):** correcto. No distingue entre los 8 mercados; es
  Fase 03.
- **C5 (correlación):** correcto en lo esencial (filtra cesta, declara la limitación
  activos-vs-estrategia con respaldo externo doble). Una laguna a declarar, no un fallo: para
  BTCUSD/ETHUSD solo existe 1 de las 3 ventanas exigidas (4h/3 meses, `correlaciones_8x8.md`);
  como el criterio exige cumplirse en las tres, una cesta con cripto es **inverificable**, y por la
  regla 26 (bloquear por defecto) queda fuera mecánicamente. Debe escribirse explícito, no dejarse
  a que alguien argumente que "hueco no es fallo".

---

## Cambios mínimos exigidos (sin ellos, NO PASA)

1. **C1 — el 15% de retorno objetivo va a la ficha del CEO como decisión** (hoy no existe en ningún
   documento firmado; grep ejecutado con cero resultados en `00-direccion/`).
2. **C1 — reformular como tope de operaciones/año por vela** (15m: 29–105 · 1h: 62–217 · 4h:
   126–426, ya calculado) o declarar el supuesto de clase de estrategia (señal por vela, actividad
   2–10%). Prohibido presentar "1h inviable" como absoluto: a N=100, XAUUSD 1h pasa.
3. **C1+C3 — el swap entra en el presupuesto del 5%** (coste TOTAL, que es lo que dice el ancla de
   Carver) con el dimensionado de C6 y noches esperadas declaradas, o C3 recibe tope numérico
   propio. Dato ya calculado: a 4h en largo, 1 noche/op ≈ duplica el arrastre de EURUSD y XAUUSD.
4. **C6 — se reformula como requisito al broker de 04.01.01**, recalculado con ATR mediana: "si
   XAUUSD 4h entra en la cesta, el broker debe permitir ≤0,1 oz, o el capital ser ≥2.000 EUR". El
   oro queda **condicionado, no eliminado**.
5. **C5 — añadir la frase:** "cripto no puede verificar las 3 ventanas; por defecto queda fuera de
   la cesta salvo decisión explícita del CEO con la limitación delante".
6. **Criterio nuevo (el único que falta): hueco de discontinuidad vs stop.** Umbral propuesto: si
   p90(hueco)/ATR(vela elegida) > 0,5 —lo cumplen HOY los 6 no-cripto—, toda estrategia sobre ese
   instrumento debe cerrar antes del viernes o declarar en G2 que su pérdida real por operación
   puede llegar a 5x el riesgo nominal. Dato: calculado en este veredicto sobre `02-datos/bruto/`,
   reproducible.

## Nota de proceso

El paquete entero de la Fase 02 se midió contra criterios que el CEO aún no ha firmado (01.01.02
pendiente; ya lo señaló el rechazo de 02.03.01). Este veredicto no lo repara: lo hereda. La ficha
que reciba el CEO debe llevar los cambios 1–6 incorporados ANTES de pedir la firma, no como anexo.
