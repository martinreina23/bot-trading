# Especificación del motor de backtest — construcción desde cero

**Tarea:** 04.03.06 · **Autor:** `arquitecto` (`claude-fable-5`, sin respaldo) · **Fecha:** 03/08/2026
**Consumidor:** 04.03.07 (construcción) y su revisor.
**Estado:** PENDIENTE DE REVISIÓN por un agente distinto del autor (regla 16 de CLAUDE.md).

**Ronda 2 (03/08):** tres correcciones dictadas por `arquitecto` en su mensaje de entrega, transportadas por Claude Code sin alterar y pegadas por `secretario`, que no juzga. Cadena declarada porque el autor no tiene herramienta de escritura (L-028 de LECCIONES.md).

**Qué es este documento.** La especificación de un motor de backtest que aún no existe, escrita
sin leer el motor anterior (`03-motor/backtester/`), sin ejecutar `git show 0c35959` y sin abrir
`/home/server/projects/gold-bot-2` — prohibiciones de la ficha 04.03.06, cumplidas; la lista de lo
leído está en la sección 10. Especifica **fidelidad, no ganancia** (reglas 17 y 18 de CLAUDE.md):
aquí no aparece ninguna métrica de resultado, y las cifras de los casos a lápiz son comprobaciones
aritméticas de mecánica sobre datos sintéticos, no resultados de ninguna estrategia.

**Criterio global de hecho (heredado de la ficha del WBS):** cada requisito tiene su prueba de
aceptación ejecutable al lado; un requisito sin prueba no es un requisito; ninguno obliga a suponer
(regla 6 de CLAUDE.md). 04.03.07 no está terminada hasta que TODAS las pruebas de este documento
pasen ejecutadas y lo acepte un agente distinto del que construye.

---

## 1. Alcance fijado por D-19 (`00-direccion/DECISIONES.md`, D-19, 03/08/2026)

- **Instrumento:** XAUUSD, oro **al contado**. Un solo mercado. Nada multi-mercado.
- **Vela:** 4 horas, con el corte de 22:00 UTC que ya usan 02.02.01 y 02.02.03.
- **Capital simulado:** cuenta de 1.000–2.000 € (límites de D-14; ver hueco H-3 sobre la moneda).
- **Qué hace el motor:** simula operaciones sobre velas históricas y emite un registro de
  operaciones con todos los cargos fechados y la caja resultante. **Qué no hace:** no calcula
  ninguna métrica de resultado; eso pertenece a otras tareas (04.03.01 en adelante).

## 2. Convenciones globales (obligatorias; toda prueba las presupone)

| # | Convención |
|---|---|
| C-1 | **Unidad de precio y coste: USD por onza.** No existe el pip en este motor (ver R-07). |
| C-2 | **La serie de datos es BID.** Verificado en `04-resultados/veredictos/veredicto_criterios_g1.md` (ataque A5): los brutos son OHLC BID sin ask. El ask se sintetiza como `bid + spread` de configuración. Limitación declarada: no hay serie ask real (ver H-4). |
| C-3 | **Signo del swap:** negativo = coste que paga la cuenta; positivo = crédito. Misma convención que `01-investigacion/mercados/coste_swap.md` (sección Método). |
| C-4 | **Sin mirada al futuro:** la decisión tomada sobre la vela cerrada `t` se ejecuta en la **apertura de la vela `t+1`**. La interfaz de estrategia solo recibe velas cerradas hasta `t` (ver R-14). |
| C-5 | **Aproximación de vela:** dentro de una vela no hay orden temporal conocible. El instante atribuido a todo evento de la vela es su **apertura**. Si el stop se cumple dentro de una vela, el stop ejecuta en esa vela y la salida por señal ya no se evalúa; el stop se evalúa desde la propia vela de entrada (tras la apertura). |
| C-6 | **Largo:** compra al ask (`bid + spread`), vende al bid. **Corto:** vende al bid, recompra al ask. El spread se paga así una vez por ida y vuelta, igual que en el método de `coste_operar.md`. |
| C-7 | **Swap:** para cada día D de lunes a viernes, sea `r_D` = D 22:00:00 UTC. Se carga `mult(D) × tasa_noche × base` si `ts_entrada < r_D` y `ts_cierre_atribuido > r_D`, con `mult(miércoles) = 3` y `mult = 1` el resto: 7 unidades por semana repartidas en 5 cargos. Sábado y domingo no son días de cargo. `tasa_noche = % anual / 365` (conversión lineal, el método declarado de `coste_swap.md`). Base del cálculo: nocional al bid de entrada — convención PROVISIONAL, ver hueco H-1. Día triple y hora: PROVISIONALES, ver H-1. |
| C-8 | **Toda cifra de mercado vive en configuración versionada, nunca cableada en el código del motor** (spread, comisión, swaps, apalancamiento). Motivo: advertencia 6 de `coste_swap.md` («no deben tratarse como constantes») y el reemplazo previsto por 04.01.02. |

## 3. Requisitos A — herencia técnica, reescrita como construcción propia

Origen: los cuatro requisitos técnicos del criterio de aceptación anterior (fila T2), recuperados
como texto de dirección en la orden de esta tarea. Eran buena ingeniería antes de existir este
motor y se reescriben aquí como requisitos nativos de una construcción desde cero, sin el marco de
trasplante. Verificación pendiente para el revisor: `git show HEAD:00-direccion/WBS.md`, sección
«Trasplante desde gb2 — criterios de aceptación», fila T2.

| Código | Requisito | Prueba de aceptación ejecutable |
|---|---|---|
| R-01 | **Costes nativos dentro de la simulación.** La entrada se ejecuta al precio de compra y la salida al precio de venta (C-6); la comisión y el swap son apuntes fechados dentro del registro de la operación, nunca un descuento porcentual aplicado después. La suma de los apuntes del registro reproduce exactamente la caja final. | (a) Ejecutar CL-1 (sección 7): caja final **2.014,55 USD** exactos a 2 decimales, y el registro contiene los apuntes fechados: comisión −0,03 en la salida, swap −0,09 el martes y −0,27 el miércoles. (b) Ida y vuelta sobre precio plano: corto de 0,1 oz abierto al bid 3.000,00 y recomprado al ask 3.000,20, comisión 0,10 USD/oz → variación de caja exactamente **−0,03 USD** (−0,02 de spread, −0,01 de comisión). (c) Aserción global: `caja_final − caja_inicial == suma de todos los apuntes de todas las operaciones`, sin residuo. |
| R-02 | **Un stop nunca ejecuta a mejor precio que el disparado.** Largo: stop evaluado contra bid; si la vela abre ya por debajo del nivel, ejecuta en la apertura (peor); si lo cruza dentro, ejecuta exactamente en el nivel; jamás por encima del nivel. Corto: stop evaluado contra ask sintético (`bid + spread`), simétrico. | (a) Intra-vela: CL-2b (sección 7) → fill exactamente **2.900,00**, caja final **1.979,88 USD**. (b) Hueco: CL-2 (sección 7) → fill exactamente **2.395,00**, nunca 2.900,00. (c) Toque exacto: vela con L = nivel del stop → dispara y ejecuta en el nivel. (d) Misma vela de entrada: entrada en O bid 3.000,00 (ask 3.000,20), stop 2.945,00, esa misma vela con L 2.940,00 → salida por stop en esa vela a 2.945,00. (e) Corto con spread 0,20 y stop de recompra en ask 3.010,00: vela con H bid 3.009,79 → NO dispara; H bid 3.009,80 → dispara y ejecuta en 3.010,00; con apertura bid 3.050,00 → ejecuta en ask 3.050,20. (f) Aserción global sobre todas las pruebas: para todo stop de largo, `precio_fill ≤ nivel`; para todo stop de corto, `precio_fill ≥ nivel`. |
| R-03 | **Financiación asimétrica con triple miércoles.** Tasas de swap por dirección (largo y corto independientes, con signo C-3), cargadas según C-7. | (a) Posición larga sintética abierta de lunes 00:00 a lunes 00:00 siguiente (semana completa): exactamente **5 apuntes de swap fechados** (lun, mar, mié, jue, vie a las 22:00 UTC), el del miércoles por el triple exacto de los demás, total 7 unidades. (b) La misma semana en corto con `swap_corto` positivo → 5 abonos (signo contrario), mismas fechas. (c) Cambiar la tasa en el fichero de configuración cambia el importe sin tocar código del motor (C-8): dos ejecuciones con dos configs → importes proporcionales a las tasas. |
| R-04 | **Dimensionado por riesgo.** El tamaño sale de `riesgo_por_operación ÷ distancia_de_stop_por_onza`, redondeado **a la baja** al paso de lote (R-10). El riesgo nominal registrado es el del tamaño realmente abierto, no el teórico. | En CL-1: riesgo 20,00 USD, distancia 55,00 USD/oz → 0,3636… → tamaño abierto **0,3 oz** y riesgo nominal registrado **16,50 USD**. Aserción adicional: con distancia 100,00 y riesgo 20,00 → exactamente 0,2 oz (sin redondeo). |
| R-05 | **El caso hecho a mano es la prueba maestra.** Los tres casos de la sección 7 (CL-1, CL-2, CL-2b), con sus velas dadas y su aritmética hecha con lápiz y papel, son pruebas automatizadas permanentes del motor. Si un cambio del motor mueve una sola cifra, la prueba falla. | Las tres cajas finales exactas a 2 decimales, sin tolerancia: CL-1 → **2.014,55** · CL-2 → **1.878,88** · CL-2b → **1.979,88** USD. Estas pruebas alimentan además el testbed de invarianza (03.01.10). |
| R-06 | **La lógica vive en un solo sitio.** El remuestreo a 4h se hace **importando `remuestrear`** (y, si el motor construye la serie, `limpiar`) de `03-motor/scripts/precios_mercado.py`; el motor no reimplementa remuestreo. Un único camino de ejecución para largos y cortos: la mecánica de fills, costes y swap no se duplica por dirección ni por tipo de orden. | (a) `grep -rn "\.resample(" <dir_motor>` → 0 apariciones (el único `resample` del proyecto sigue en `precios_mercado.py`). (b) Serie 1m sintética procesada por el motor y por `remuestrear(df, "4h", inicio, fin)` directamente → velas 4h idénticas bit a bit (timestamps y OHLC). (c) Camino único probado por sabotaje, no por ojo. 04.03.07 declara en el README del motor los dos nombres de símbolo: la función de fill de stop y la función de cargo de swap. Test `test_camino_unico`, ejecutado con `pytest -q <dir_motor> -k camino_unico`, determinista (R-15), en tres pasos: (1) ejecuta el motor sobre los datos de CL-1, CL-2, CL-2b y de los casos R-02(d), R-02(e) y R-03(a)-(b) —largos y cortos; stop por hueco, dentro de vela y en la vela de entrada; apuntes de swap en las dos direcciones— y guarda cada precio de fill de stop y cada importe de apunte de swap; (2) sustituye por nombre de símbolo (monkeypatch) la función de fill declarada por una envoltura que suma +1,00 USD a todo precio de fill que devuelve, reejecuta y cuenta `fills_intactos` = número de fills de stop cuyo precio no cambió respecto al paso 1; (3) restaura, sustituye la función de swap por una envoltura que suma +1,00 USD a cada importe de apunte, reejecuta y cuenta `apuntes_intactos`. Salida: los dos recuentos, impresos por el test. Pasa: `fills_intactos == 0` y `apuntes_intactos == 0`. No pasa: cualquiera de los dos ≥ 1 — significa que existe un fill o un apunte producido sin atravesar el símbolo declarado, es decir, lógica en más de un sitio, aunque el duplicado sea un método de clase, una `lambda` o código insertado en línea: la prueba mide comportamiento, no texto, que es donde un recuento de `def` no llega; y la suma de +1,00 no tiene punto fijo, así que ningún valor legítimo puede quedar igual por casualidad. Límite declarado: no detecta un duplicado muerto que estas ejecuciones no recorran; ese residuo queda para la revisión de código de 04.03.07 (regla 16 de CLAUDE.md), que confirma, no descubre. |

## 4. Requisitos B — lo que exige D-19 y el criterio anterior no podía conocer

| Código | Requisito | Prueba de aceptación ejecutable |
|---|---|---|
| R-07 | **Unidad USD por onza, nunca pips** (C-1). Precios, stops, spreads, comisiones y registros, todos en USD/oz; los importes de caja en USD. | (a) `grep -rniE "\bpips?\b" <dir_motor>` → 0 líneas (no nombrar nada «pipeline» dentro del motor: elegir otro nombre). (b) Ida y vuelta plana de 1 oz con la config medida (spread 0,19, comisión 0,07) → cargo total exactamente **0,26 USD**, la cifra de la fila XAUUSD de `coste_operar.md`. |
| R-08 | **Vela de 4h idéntica a la de 02.02.01/02.02.03.** Rejilla UTC pura 0/4/8/12/16/20, `label="left"`, `closed="left"`; los bordes de la ventana se fijan en cortes de 22:00 UTC; las velas truncadas por el borde de ventana se descartan exactamente como hace `remuestrear` con `inicio`/`fin`. | (a) La prueba R-06(b) sobre una serie que incluya un borde de ventana a las 22:00 UTC: la primera y última vela del motor coinciden con las de `remuestrear`, incluidos los descartes de bins truncados. (b) Sobre un tramo real de `02-datos/bruto/XAUUSD/1m.csv.gz`: todas las aperturas de las velas 4h del motor tienen hora ∈ {0, 4, 8, 12, 16, 20} UTC. |
| R-09 | **Asimetría del swap del oro, calibrada de la medición.** La configuración de XAUUSD trae `swap_largo_anual` y `swap_corto_anual` por separado, con campos `fuente` y `estado: PROVISIONAL (la sustituye 04.01.02)`. Valores dentro de lo medido en `coste_swap.md` (tabla, filas XAUUSD): largo entre **−8,16 % y −6,64 %** anual, corto entre **−0,76 % y +0,64 %** anual. | (a) Test que lee la config y aserta: `−8,16 ≤ swap_largo_anual ≤ −6,64` · `−0,76 ≤ swap_corto_anual ≤ +0,64` · existen los campos `fuente` y `estado`. (b) Test de mecánica: con esa config, una noche normal de largo produce un cargo (negativo) y la misma noche en corto produce un apunte de una magnitud al menos 8 veces menor en valor absoluto (asimetría del instrumento efectivamente aplicada por dirección, no una tasa única). |
| R-10 | **Lote fraccionado de 0,1 onzas.** Paso de tamaño 0,1 oz; mínimo 0,1 oz; el redondeo del dimensionado siempre a la baja; si el tamaño calculado queda por debajo de 0,1 oz, **no se abre la operación** y se registra el motivo. Origen: D-19 consecuencia 2(c) — el lote mínimo de 1 oz exige unos 1.962 € contra un techo de cuenta de 2.000 € (`veredicto_criterios_g1.md`, A3); operar exige el fraccionado. | Casos de dimensionado: 0,3636 → 0,3 · 0,25 → 0,2 · 0,19 → 0,1 · 0,09 → **no se abre**, y el registro contiene una entrada de operación rechazada con motivo «tamaño calculado inferior al lote mínimo de 0,1 oz». Aserción global: ningún tamaño abierto en ninguna prueba es < 0,1 ni deja resto módulo 0,1. |
| R-11 | **Hueco de fin de semana.** Entre el último precio real y el siguiente no existe ningún precio: el motor no ejecuta nada dentro de un hueco. Un stop saltado por el hueco ejecuta al primer precio real (la apertura tras el hueco), y la pérdida registrada es la del hueco, no la del stop. Magnitud de referencia medida: el máximo del oro es **5,05 veces lo arriesgado** (`veredicto_criterios_g1.md`, A5, fila XAUUSD, máx 5,05x). | (a) CL-2 (sección 7), construido con un hueco de exactamente 5,05× la distancia de stop: fill en 2.395,00 y caja final 1.878,88. (b) Aserción global sobre todas las pruebas: todo fill (entrada, salida, stop) lleva el timestamp de una vela existente en la serie de entrada; ningún apunte tiene un timestamp dentro de un tramo sin velas. |
| R-12 | **Lectura del formato que produce `precios_mercado.py`.** Entrada del motor: el fichero `02-datos/bruto/XAUUSD/1m.csv.gz` que escribe `guardar_serie` — CSV comprimido gzip, cabecera `ts_utc,open,high,low,close`, timestamps ISO-8601 en UTC, precios float en USD/oz, lado BID. El motor no adapta en silencio formatos distintos: los rechaza con error. | (a) Generar en el área de pruebas un fichero sintético con ese formato exacto; el motor lo carga y reproduce n de filas, primer y último `ts_utc`. (b) El mismo fichero con la cabecera `timestamp,...` en vez de `ts_utc` → el motor falla con error explícito de formato, no carga. (c) Prueba sobre el fichero real `02-datos/bruto/XAUUSD/1m.csv.gz`: carga sin error y todos los precios caen en el rango de cordura del oro (500–6000 USD/oz, el mismo `RANGO_CORDURA` de `precios_mercado.py`). |

## 5. Requisitos C — los costes ya medidos que el motor honra

| Código | Requisito | Prueba de aceptación ejecutable |
|---|---|---|
| R-13 | **La configuración por defecto de XAUUSD son los valores medidos**, marcados PROVISIONALES: spread 0,19 USD/oz y comisión 0,07 USD/oz de ida y vuelta (total 0,26 USD/oz) de `coste_operar.md` (fila XAUUSD, estado PROVISIONAL hasta 04.01.02), y los swaps de R-09. La config lleva `fuente` (fichero citado) y `estado`. | (a) Test que lee la config por defecto y aserta 0,19 / 0,07 y los campos `fuente` y `estado`. (b) Contraste con `coste_relativo.md`, sección «CORRECCIÓN (31/07) — sesgo del ATR medio en XAUUSD», tabla «Tabla — coste relativo contra ATR MEDIANA (divisas, oro y cripto)», fila XAUUSD 4h: el cargo de ida y vuelta del motor (0,26) dividido por el ATR14 mediana 4h del oro que publica esa fila (22,1527 USD/oz) × 100 = **1,17 %** (±0,01 punto), la cifra de esa misma fila. CORRECCIÓN DECLARADA (ronda 2 de 04.03.06): la versión anterior atribuía el 22,1527 a `04-resultados/atr_15m_1h_4h.json`, fichero que el autor no leyó y que no figura en la sección 10; la fuente real es la fila citada de `coste_relativo.md`, que sí está declarada leída. Se corrige la atribución sin mover la cifra. |

## 6. Requisitos D — decisiones de diseño mínimas del arquitecto

Estas tres no vienen de los insumos: son el mínimo necesario para que los casos a lápiz sean
computables sin ambigüedad (regla 6 de CLAUDE.md) y para que el motor sirva al testbed 03.01.10.

| Código | Requisito | Prueba de aceptación ejecutable |
|---|---|---|
| R-14 | **Sin mirada al futuro** (C-4). La estrategia recibe únicamente las velas cerradas hasta `t`; su orden se ejecuta en la apertura de `t+1`. | Estrategia-sonda que registra, en cada decisión, el timestamp máximo visible: aserción de que siempre es ≤ cierre de la vela `t` y estrictamente menor que el timestamp de ejecución de la orden resultante, en todas las operaciones de todas las pruebas. |
| R-15 | **Determinismo y registro que cuadra.** Misma entrada y misma config → salida bit-idéntica. El artefacto de salida es un registro por operación (dirección, timestamps de señal/entrada/salida, precios, tamaño, motivo de salida, apuntes fechados) más la serie de caja. | Ejecutar dos veces CL-1 con la misma semilla de entorno → los dos ficheros de salida tienen hash idéntico (`sha256sum`). La aserción de cuadre es la R-01(c). |
| R-16 | **El motor no busca datos por su cuenta.** Solo lee las rutas que recibe como parámetro explícito. Sin ruta de datos, falla con error claro. La guardia del cajón `02-datos/reservado/` es del cifrado de 03.01.11, no de este motor; pero el motor no lleva ninguna ruta cableada a ese cajón. | (a) Invocar el motor sin parámetro de datos → error explícito, no exploración de directorios. (b) `grep -rn "reservado" <dir_motor>` → 0 apariciones fuera de comentarios. |

`<dir_motor>` en todas las pruebas: el directorio raíz del motor nuevo, que 04.03.07 fija en su
primer commit y declara en su README.

## 7. Los casos a lápiz (datos completos y aritmética)

Config común de los tres casos — valores de mecánica elegidos redondos a propósito; los medidos se
prueban aparte en R-07/R-09/R-13: spread 0,20 USD/oz · comisión 0,10 USD/oz ida y vuelta (cargada
al cierre) · swap largo −3,65 % anual → −0,01 % por unidad de noche · base del swap = bid de
entrada × onzas (C-7) · capital inicial 2.000,00 USD · riesgo por operación 1 % del capital
inicial = 20,00 USD · paso de lote 0,1 oz. Estrategia-sonda: compra cuando cierra ≥ 3.000,00
estando plana; cierra por señal cuando cierra ≥ 3.045,00. Todos los precios de las tablas son BID.

### CL-1 — largo con swap (triple miércoles incluido) y salida por señal

Velas 4h (apertura UTC · O · H · L · C):

| Vela | O | H | L | C |
|---|---|---|---|---|
| mar 2026-03-03 12:00 | 2.990,00 | 3.001,00 | 2.989,00 | 3.000,00 |
| mar 2026-03-03 16:00 | 3.000,00 | 3.010,00 | 2.995,00 | 3.005,00 |
| mar 2026-03-03 20:00 | 3.005,00 | 3.012,00 | 3.000,00 | 3.010,00 |
| mié 2026-03-04 00:00 | 3.010,00 | 3.015,00 | 3.002,00 | 3.008,00 |
| mié 2026-03-04 04:00 | 3.008,00 | 3.020,00 | 3.006,00 | 3.018,00 |
| mié 2026-03-04 08:00 | 3.018,00 | 3.030,00 | 3.015,00 | 3.025,00 |
| mié 2026-03-04 12:00 | 3.025,00 | 3.035,00 | 3.020,00 | 3.030,00 |
| mié 2026-03-04 16:00 | 3.030,00 | 3.040,00 | 3.028,00 | 3.038,00 |
| mié 2026-03-04 20:00 | 3.038,00 | 3.044,00 | 3.030,00 | 3.040,00 |
| jue 2026-03-05 00:00 | 3.040,00 | 3.052,00 | 3.038,00 | 3.049,00 |
| jue 2026-03-05 04:00 | 3.050,00 | 3.055,00 | 3.045,00 | 3.052,00 |

Recorrido: señal al cierre de la vela de las 12:00 del martes (C = 3.000,00) → entrada en la
apertura siguiente, martes 16:00, al ask 3.000,00 + 0,20 = **3.000,20**. Distancia de stop del
caso: 55,00 USD/oz → stop bid 2.945,00 (no se toca). Dimensionado: 20,00 ÷ 55,00 = 0,3636 → **0,3
oz** (riesgo nominal registrado 16,50). Señal de cierre al cierre del jueves 00:00 (C = 3.049,00 ≥
3.045,00) → salida en la apertura del jueves 04:00 al bid **3.050,00**.

Aritmética a lápiz: precio (3.050,00 − 3.000,20) × 0,3 = **+14,94** · comisión 0,10 × 0,3 =
**−0,03** (ts jueves 04:00) · swap: cruces de 22:00 con la posición abierta = martes (×1) y
miércoles (×3); base 3.000,00 × 0,3 = 900,00; unidad −0,01 % = −0,09 → apuntes **−0,09** (mar
22:00) y **−0,27** (mié 22:00) · neto +14,55 → **caja final 2.014,55 USD**.

### CL-2 — stop saltado por hueco de fin de semana de 5,05×

| Vela | O | H | L | C |
|---|---|---|---|---|
| vie 2026-03-06 00:00 | 2.995,00 | 3.002,00 | 2.990,00 | 3.000,00 |
| vie 2026-03-06 04:00 | 3.000,00 | 3.008,00 | 2.996,00 | 3.004,00 |
| vie 2026-03-06 08:00 | 3.004,00 | 3.010,00 | 2.998,00 | 3.005,00 |
| vie 2026-03-06 12:00 | 3.005,00 | 3.009,00 | 2.999,00 | 3.002,00 |
| vie 2026-03-06 16:00 | 3.002,00 | 3.006,00 | 2.996,00 | 3.001,00 |
| lun 2026-03-09 00:00 | 2.395,00 | 2.420,00 | 2.390,00 | 2.410,00 |

Recorrido: señal el viernes 00:00 (C = 3.000,00) → entrada viernes 04:00 al ask **3.000,20**.
Distancia de stop del caso: 100,00 → stop bid **2.900,00**; dimensionado 20,00 ÷ 100,00 = **0,2
oz** exactas. No hay velas entre el cierre del viernes 20:00 y el lunes 00:00 (ese vacío ES el
hueco). El lunes abre en 2.395,00 = 2.900,00 − 505,00: el hueco más allá del stop es 505,00 =
**5,05×** la distancia de stop, el máximo medido del oro (A5). El stop ejecuta en la apertura,
**2.395,00**, nunca en 2.900,00.

Aritmética a lápiz: precio (2.395,00 − 3.000,20) × 0,2 = **−121,04** · comisión **−0,02** · swap:
único cruce con cargo = viernes 22:00 (×1); base 600,00 → **−0,06** (sábado y domingo no cargan;
el lunes 22:00 ya no hay posición) · neto −121,12 → **caja final 1.878,88 USD**. La pérdida en
precio por onza (605,20) es 6,052× la distancia nominal del stop: el motor reproduce el riesgo del
hueco, no lo recorta al stop.

### CL-2b — mismo caso, stop dentro de vela (sin hueco)

Igual que CL-2, sustituyendo la vela del lunes por: O 2.950,00 · H 2.960,00 · L 2.890,00 ·
C 2.920,00. La apertura (2.950,00) no viola el stop; el L sí (2.890,00 ≤ 2.900,00) → fill
exactamente en **2.900,00**. Aritmética: precio (2.900,00 − 3.000,20) × 0,2 = −20,04 · comisión
−0,02 · swap −0,06 → **caja final 1.979,88 USD**. Nota: la pérdida realizada excede el riesgo
nominal en 0,04 (0,20/oz de spread) — coste nativo visible, no error.

## 8. Lo que queda fuera a propósito, y por qué

| Excluido | Motivo |
|---|---|
| Métricas de resultado de cualquier tipo | Prohibidas en esta especificación (reglas 17 y 18 de CLAUDE.md). El motor emite el registro de operaciones; lo que se calcule encima pertenece a 04.03.01 y siguientes. |
| Monte Carlo y walk-forward | Son la tarea 04.03.04, no el motor. El motor solo debe ser determinista (R-15) para que aquella pueda barajarlo. |
| Órdenes limit, stop de entrada y take-profit | Las hipótesis aún no existen (04.02 pendiente). El juego mínimo es: entrada a mercado en la apertura siguiente + stop de protección. Si una variante pre-registrada necesita otro tipo de orden, se amplía esta especificación con su prueba ANTES de construirlo (regla 19 de CLAUDE.md). |
| Evaluación de stops sobre los datos 1m dentro de la vela 4h | v1 evalúa sobre el OHLC 4h con las reglas C-5/R-02, deterministas y probadas. Afinar con 1m es una ampliación con tarea WBS propia; no se hace en silencio. |
| Multi-mercado, portafolio, correlaciones | D-19: un solo mercado; G1-C5 queda sin objeto. Se reabre solo si entra un segundo mercado. |
| Velas distintas de 4h | D-19 fija 4h. Nada en este motor debe impedirlo a futuro, pero especificarlo hoy sería inventar un requisito. |
| Ejecución en vivo, broker, órdenes reales | Fase 05 en adelante, detrás de sus puertas y barreras (regla 23 de CLAUDE.md). |
| Slippage distinto del ya modelado (spread fijo + regla de stop + hueco) | No hay datos ask ni tick descargados para calibrarlo (C-2). Declararlo sería estimar. |

## 9. Huecos declarados (se escriben, no se rellenan — regla 6 de CLAUDE.md)

| Hueco | Qué falta | Dónde se resuelve |
|---|---|---|
| H-1 | Convención exacta de rollover del broker real: hora del cargo, día del triple, y base del cálculo del swap (nocional de entrada vs. cierre diario). C-7 fija una convención PROVISIONAL (22:00 UTC, miércoles ×3, base = bid de entrada) coherente con la advertencia 7 de `coste_swap.md`, parametrizada para sustituirse sin tocar código. | 04.01.01 / 04.01.02 |
| H-2 | Apalancamiento y margen: sin broker no hay cifra. Parámetro obligatorio de configuración **sin valor por defecto**; los tests le pasan un valor declarado en el propio test. | 04.01.01 / 04.01.02 |
| H-3 | Moneda de la cuenta (EUR vs USD) y fuente del tipo EUR/USD para los límites de 1.000–2.000 € de D-14. Todas las pruebas de esta especificación operan en USD. | 04.01.01 |
| H-4 | Deriva del coste: el 0,19/0,07 es de feb-2025 y D-19 2(d) registra que podría casi duplicarse; además no hay serie ask real (C-2). La config es reemplazable por diseño (C-8). | 04.01.02 |
| H-5 | L-007: la fórmula de coste de algún broker referencia futuros mientras el precio usado es contado; podrían no ser el mismo instrumento (advertencia 2 de `coste_swap.md`, D-19 2(e)). | 04.01.02 |
| H-6 | El swap puntual del oro tiene dos fuentes que discrepan (OANDA −6,64 %/+0,64 %; XTB −8,16 %/−0,76 %). R-09 exige el rango, no un punto; el valor único se fija con el broker elegido. | 04.01.02 |
| H-7 | La fila T2 no pudo leerse de `git show HEAD:` en esta sesión (el autor no tiene herramienta de terminal); el texto usado es el de la orden del orquestador, contrastado con las huellas de T2 en el WBS vivo y en `precios_mercado.py`. | Revisor de esta especificación: ejecutar `git show HEAD:00-direccion/WBS.md` y confirmar palabra por palabra. |

## 10. Fuentes leídas y no leídas (declaración obligatoria de la ficha)

**Leídas (todo lo que el autor tuvo delante):**
- `/home/server/projects/bot-trading/CLAUDE.md` (inyectado al arrancar la sesión)
- `/home/server/projects/bot-trading/00-direccion/WBS.md` — parcial, en dos niveles: como contexto de fases, el tramo final de la sección «Fase 02 — ELEGIR MERCADO Y TAMAÑO DE VELA (puerta G1)» (filas 02.02.02 a 02.03.03), la sección «Fase 03 — MONTAR LA CASA (Claude Code)» y desde la sección «Fase 04 — HIPÓTESIS Y VALIDACIÓN (puerta G2)» hasta el arranque de la sección «Límites del CEO»; y, en detalle, la ficha de las tareas `04.03.06` y `04.03.07` en la sección «04.03 Laboratorio de pruebas»
- `/home/server/projects/bot-trading/00-direccion/DECISIONES.md` — entradas D-16 a D-21 (D-19 completa)
- `/home/server/projects/bot-trading/01-investigacion/mercados/coste_swap.md` — completo
- `/home/server/projects/bot-trading/01-investigacion/mercados/coste_operar.md` — completo
- `/home/server/projects/bot-trading/01-investigacion/mercados/coste_relativo.md` — completo
- `/home/server/projects/bot-trading/04-resultados/veredictos/veredicto_criterios_g1.md` — secciones de los ataques A3, A4 y A5, dentro de «Ataques que SÍ han tumbado algo (con su experimento)»
- `/home/server/projects/bot-trading/03-motor/scripts/precios_mercado.py` — completo (es la fuente del formato de datos de R-12 y del símbolo `remuestrear` de R-06/R-08)

**NO leídas, cumpliendo la prohibición de la ficha:** `03-motor/backtester/` (ni un fichero),
el commit `0c35959` (ningún `git show` ni variante), y `/home/server/projects/gold-bot-2`.

**Nota de discrepancia de insumo:** la orden citaba `04-resultados/coste_relativo.md`, que no
existe; el único fichero con ese nombre en el repositorio es
`01-investigacion/mercados/coste_relativo.md` (su volcado numérico es
`04-resultados/coste_relativo_15m_1h_4h.json`). Verificado por búsqueda global antes de usarlo.
