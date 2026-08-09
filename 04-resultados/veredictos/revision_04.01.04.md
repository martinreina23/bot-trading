RECHAZA

# Revisión independiente de 04.01.04 — tamaño mínimo operable de XAUUSD 4h

**Revisor:** `validador` (`claude-fable-5`; **sin respaldo**, regla 29 de CLAUDE.md).
**Fecha:** 2026-08-09.
**Ejecutor revisado:** `constructor-datos` (`claude-sonnet-5`, declarado en su informe).
**Artefactos revisados:** `03-motor/scripts/tamano_minimo_operable.py` ·
`04-resultados/tamano_minimo_operable.json` · `04-resultados/tamano_minimo_operable.md`.

---

## Veredicto y motivos

**RECHAZA por dos motivos formales, ambos verificados por ejecución o grep.** Y se deja
constancia igual de clara de lo contrario: **la aritmética de los 7 puntos es correcta y
reproducible** — mi recálculo independiente, escrito ANTES de leer el script del ejecutor y
solo desde las fuentes primarias, coincide con su JSON hasta el último decimal, y su script es
determinista y reproduce byte a byte el JSON en disco. El rechazo no pide recalcular nada:
pide registrar la tarea y corregir el informe. Los números, una vez la tarea exista, son
reutilizables tal cual.

### M1 — La tarea 04.01.04 no existe en el WBS y no tiene ficha (reglas 2, 5 y 12 de CLAUDE.md)

Verificado por grep: `00-direccion/WBS.md` contiene 04.01.01, 04.01.02 y 04.01.03, y **ninguna
aparición de «04.01.04»**. Un `grep -rn "04\.01\.04"` sobre todo `00-direccion/` devuelve **cero
resultados**: ni ficha, ni cola, ni decisión. Las únicas menciones al código en el repositorio
están en los artefactos del propio ejecutor. Su informe abre con «Tarea: 04.01.04 — subtarea
NUEVA dentro del alcance de 04.01.01, creada por el orquestador (regla 2 de CLAUDE.md)»: esa
referencia **no la localiza ningún grep** (regla 12), y la regla 5 es categórica: «Sin ficha,
no hay tarea». Consecuencia práctica, no solo formal: **el alcance de los 7 puntos no es
verificable contra ningún documento registrado** — esta revisión solo lo conoce por el resumen
transmitido en el encargo de revisión. Un cálculo cuyo encargo no está escrito en ningún sitio
no puede pasar a sostener una decisión de broker con dinero real detrás (G3).

### M2 — La declaración «Entradas usadas, y solo estas» del informe es falsa (regla 12 de CLAUDE.md)

`04-resultados/tamano_minimo_operable.md` declara cinco entradas «y solo estas». Pero su punto 4
etiqueta los lotes como «1,0 oz (IC Markets EU)», «0,3 oz (pedido mínimo XTB Limited)» y
«0,1 oz (paso de XTB)», y su punto 6 construye sobre esas atribuciones la «consecuencia directa
sobre el listón». Verificado por grep: esas tres atribuciones viven en la fila del criterio 1 de
`01-investigacion/mercados/comparacion_brokers.md` («Pedido mínimo 0,003 lote (0,3 oz); paso
mínimo de transacción 0,001 lote = 0,1 oz exactas» para XTB Limited; «Minimum Lot Size 0,01 =
1 oz, Volume Step 0,01 = 1 oz» para IC Markets (EU) Ltd). Ese fichero **no figura en la lista de
entradas** y las atribuciones entran en el informe **sin cita de fichero**. Las atribuciones son
FIELES a las celdas —lo he comprobado—; el defecto no es invención, es una declaración de
entradas falsa y citas ausentes en un informe que va a decisión del CEO.

### O1 — Observación grave sobre el punto 2, que NO dispara rechazo por sí sola

Con el tipo adoptado (`rate = usd_exacto / 1962`), la comprobación
`capital_eur = usd_exacto / rate = 1962` es una **identidad algebraica**: da 1.962 sea cual sea
el ATR. La «diferencia 0,0000 EUR (2,27e-13)» que el informe presenta como confirmación no es
evidencia. Lo que sí demuestra el punto 2 sin circularidad —y el ejecutor lo muestra— es el
tramo USD: 1 oz × 22,152714 ÷ 0,01 = **2.215,27 USD**, que reproduce el «2.215 USD» de A3 desde
el dato primario solo. El contraste que cierra el tramo EUR **lo aportó esta revisión, no el
informe**: el tipo implícito 1,129088 coincide con `instrumentos.EURUSD.velas.4h.precio_medio`
del mismo JSON primario (1,129069; desviación 0,0017%), con el que 1 oz da 1.962,03 EUR. La
sustancia aguanta; la presentación del informe la sobrevende.

---

## V1 — Recálculo propio desde las fuentes primarias

Escribí y ejecuté mi propio script (pegado al final, con su salida literal) **antes de abrir**
`03-motor/scripts/tamano_minimo_operable.py`. Entradas: campo
`instrumentos.XAUUSD.velas.4h.atr14_mediana` (= 22,152714285714215 USD/oz) y `atr14_medio`
(= 28,42890772406983, solo punto 7) de `04-resultados/atr_15m_1h_4h.json`; cita «2.215 USD =
1.962 EUR» de la sección A3 de `04-resultados/veredictos/veredicto_criterios_g1.md`; riesgo 1% y
estimador mediana de la viñeta G1-C6 de `00-direccion/WBS.md`; capital 1.000–2.000 EUR de D-11 y
parada dura −30% de D-14 en `00-direccion/DECISIONES.md`.

| Punto | Declarado por el ejecutor | Mi recálculo | ¿Coincide? |
|---|---|---|---|
| 1 | tipo implícito 1,129088 | 1,129088 (2.215,2714 ÷ 1.962) | SÍ |
| 2 | 1 oz al 1% = 1.962,00 EUR; dif. 0,00 | 1.962,00 EUR (contraste primario: 1.962,03) | SÍ |
| 3 | 0,5097 · 0,7645 · 1,0194 oz | 0,509684 · 0,764526 · 1,019368 oz | SÍ |
| 4 | 1.962,00 · 588,60 · 196,20 · 19,62 EUR | idénticos | SÍ |
| 5 | umbral 1.962 → 93,67% · 588,60 → 0,00% · 196,20 → 0,00% | idénticos | SÍ |
| 6 | ≈0,357 oz (1.000 EUR) · ≈0,714 oz (2.000 EUR) | 0,356779 · 0,713558 oz | SÍ |
| 7 | ~252 EUR sale del ATR medio; mediana → 196,20 EUR | 251,79 EUR y 196,20 EUR | SÍ |

Ningún número difiere. No hay nada que devolver por V1.

## V2 — ¿Demostrado o deducido de la prosa?

**Demostrado.** La cadena exigida cierra: 1 oz × 22,152714 USD/oz = 22,1527 USD de riesgo →
÷ 0,01 = 2.215,27 USD → ÷ 1,129088 = 1.962,00 EUR, y la función
`capital_min_eur_para_lote` del script del ejecutor implementa exactamente esa cadena. No es
lectura de prosa. Con la salvedad O1: el tramo EUR de la demostración del ejecutor es una
identidad por construcción del tipo; el cierre no circular del tramo EUR (contraste con el
precio medio EURUSD 4h primario) lo hizo esta revisión y confirma la cifra. V2 no dispara
rechazo.

## V3 — El 93,67%: calculado, y con el denominador correcto

**Calculado, no argumentado.** Rehecho: suelo D-14 = 2.000 × (1 − 0,30) = **1.400 EUR**; rango
de pérdida permitido = 2.000 − 1.400 = **600 EUR**; umbral de 1 oz = 1.962,00 EUR; franja
inoperable = 1.962 − 1.400 = **562 EUR**; 562 ÷ 600 = **93,67%**. Caída al umbral:
(2.000 − 1.962) ÷ 2.000 = **1,90%**. El denominador correcto ES 600: por debajo de 1.400 EUR el
bot está parado por D-14 sea cual sea el lote, así que medir sobre 2.000→0 contaría como
«inoperable por el lote» una zona donde no se opera por otra causa. El script lo implementa así
(constante `PARADA_DURA_PCT` y rama `umbral_eur > floor_parada_dura_eur` dentro de `main`), y lo
declara en la fórmula del informe. Las filas 0,3 y 0,1 oz (umbral bajo el suelo → 0,00%) también
verificadas.

## V4 — El sesgo, en los dos sentidos

**No detectado en ninguno.** (a) «0,1 oz» NO aparece como conclusión: el listón concluido es
0,357 / 0,714 oz, cada cifra producida por suelo × 1% ÷ 19,62 EUR/oz (700 × 0,01 ÷ 19,62 =
0,3568; 1.400 × 0,01 ÷ 19,62 = 0,7136). El defecto original —el «≤0,1 onzas» de la viñeta G1-C6
del WBS, que ningún cálculo produjo nunca— no se repite con signo cambiado. (b) ¿Listón inflado
para favorecer a XTB? No hay mando libre que girar: riesgo 1% (G1-C6), parada −30% (D-14), ATR
mediana (JSON primario), tipo (punto 1) — todo registrado o primario. El motivo B es además la
lectura MÁS estricta derivable de las decisiones firmadas; quien hubiera querido favorecer a XTB
habría usado el motivo A solo (0,51 oz), que es más laxo. **Hecho a declarar, no ocultado por el
informe pero tampoco subrayado:** en el extremo conservador (1.000 EUR) el pedido mínimo de
0,3 oz pasa por un margen de 0,057 oz (un 16%): no es holgura grande, y depende de que el CEO
funde con 1.000 o con 2.000 EUR — decisión que sigue siendo suya.

## V5 — Separación de los dos motivos

**Separados y demostrados por separado.** Motivo A = cabida al capital inicial (punto 3, función
`max_oz_para_capital` evaluada en el capital); motivo B = la misma restricción evaluada en el
suelo de D-14 (punto 5). El informe demuestra que en el extremo alto A solo dice «1 oz cabe»
(1,0194 > 1) y B solo dice «1 oz no es sostenible» (0,7136 < 1): conclusiones opuestas sobre el
mismo lote, luego no se apoyan una en otra. Comparten la fórmula de riesgo, que es inevitable
(el riesgo del lote es el mismo hecho físico); no comparten conclusión.

## V6 — Lo prohibido

**Ficheros: limpios.** `git status --short` y `git diff` ejecutados: `00-direccion/WBS.md`,
`01-investigacion/mercados/comparacion_brokers.md` y
`04-resultados/veredictos/veredicto_criterios_g1.md` **sin ningún cambio sin confirmar**. El
único fichero de dirección modificado es `00-direccion/DECISIONES.md`, y su diff son las
entradas nuevas D-28 y D-29 (tareas 04.03.06 y 03.01.24, ajenas a este ejecutor; añaden, no
reescriben). Los tres artefactos del ejecutor están sin confirmar (`??`): no hizo commit.
**Frase de cierre: comparación aritmética admisible, no recomendación.** Las cifras comparadas
(1,0 oz IC Markets EU; 0,3 oz pedido mínimo y 0,1 oz paso de XTB Limited) existen como celdas
previas de la fila del criterio 1 de la comparativa, cuyo propio resumen ya nombraba a ambos
brokers; el párrafo compara cada cifra con el listón derivado (1,0 > 0,714; 0,3 < 0,357) y
declara que no elige. No hay ranking, no hay «elegir», no hay descarte de los cinco con hueco.
Lo que sí hay es **M2**: esas celdas son una entrada no declarada y sin cita — motivo de rechazo
por la vía del informe, no por recomendación encubierta.

## V7 — Reproducibilidad

**Confirmada por ejecución.** Copié el JSON de disco, ejecuté
`03-motor/scripts/tamano_minimo_operable.py` dos veces y comparé con `diff`: **byte a byte
idéntico las dos veces**. Determinista, sin red, y confirma la afirmación de reejecución del
informe del ejecutor.

## V8 — Cordura

**Pasa.** Capital mínimo monótono con el lote: 19,62 < 196,20 < 588,60 < 1.962,00 EUR — ningún
divisor invertido. Fracción inoperable mayor para el lote grande (93,67%) que para los pequeños
(0,00%) — ningún signo cambiado.

---

## Qué haría falta para que pasara (no lo reparo yo; regla 16 de CLAUDE.md)

1. El `orquestador` registra la subtarea en `00-direccion/WBS.md` con código y motivo, y su
   ficha con el alcance de los 7 puntos (reglas 2 y 5).
2. El ejecutor corrige en `04-resultados/tamano_minimo_operable.md` la lista de entradas
   (añadiendo la fila del criterio 1 de `comparacion_brokers.md` con su cita) y reescribe el
   punto 2 apoyándolo en el tramo USD y en el contraste con
   `instrumentos.EURUSD.velas.4h.precio_medio`, no en la identidad (O1).
3. Los números no necesitan recalcularse: esta revisión los reprodujo todos.

---

## Código propio de recálculo (V1) — escrito antes de leer el script del ejecutor

```python
#!/usr/bin/env python3
"""Recalculo INDEPENDIENTE del validador para la revision de 04.01.04.

Escrito ANTES de leer 03-motor/scripts/tamano_minimo_operable.py (V1).

Entradas primarias:
- 04-resultados/atr_15m_1h_4h.json -> instrumentos.XAUUSD.velas.4h.atr14_mediana
  (y atr14_medio para el punto 7; EURUSD.velas.4h.precio_medio como contraste del tipo)
- veredicto_criterios_g1.md A3: "2.215 USD = 1.962 EUR" (mediana) y "~252 EUR" para 0,1 oz
- WBS G1-C6: capital 1.000-2.000 EUR, riesgo max 1%, stop 1 x ATR mediana
- D-14: parada dura automatica a -30% del capital inicial (suelo = 70% del inicial)
"""
import json

with open("/home/server/projects/bot-trading/04-resultados/atr_15m_1h_4h.json") as f:
    atr = json.load(f)

xau4h = atr["instrumentos"]["XAUUSD"]["velas"]["4h"]
ATR_MEDIANA = xau4h["atr14_mediana"]          # USD por onza
ATR_MEDIO = xau4h["atr14_medio"]              # USD por onza (el estimador sesgado)
EURUSD_4H_PRECIO_MEDIO = atr["instrumentos"]["EURUSD"]["velas"]["4h"]["precio_medio"]

RIESGO_PCT = 0.01                              # G1-C6 (D-11)
A3_CAPITAL_EUR = 1962.0                        # A3: "2.215 USD = 1.962 EUR"
PARADA_DURA = 0.30                             # D-14: -30% del capital inicial

print(f"ATR14 mediana 4h XAUUSD = {ATR_MEDIANA}")
print(f"ATR14 medio   4h XAUUSD = {ATR_MEDIO}")
print(f"EURUSD 4h precio medio  = {EURUSD_4H_PRECIO_MEDIO}")
print()

# ---- Punto 1: tipo EUR/USD implicito en "2.215 USD = 1.962 EUR" ----
capital_usd_1oz = 1.0 * ATR_MEDIANA / RIESGO_PCT   # riesgo de 1 oz / 1%
tipo_implicito = capital_usd_1oz / A3_CAPITAL_EUR
print(f"P1  capital USD para 1 oz al 1%: {capital_usd_1oz:.4f} USD")
print(f"P1  tipo implicito = {capital_usd_1oz:.4f} / {A3_CAPITAL_EUR} = {tipo_implicito:.6f}")
print(f"P1  contraste: EURUSD 4h precio medio = {EURUSD_4H_PRECIO_MEDIO:.6f} "
      f"(desviacion {abs(tipo_implicito/EURUSD_4H_PRECIO_MEDIO-1)*100:.4f}%)")
print()

# ---- Punto 2: cadena completa 1 oz -> EUR ----
riesgo_usd = 1.0 * ATR_MEDIANA                     # 1 oz x ATR mediana
capital_usd = riesgo_usd / RIESGO_PCT
capital_eur = capital_usd / tipo_implicito
capital_eur_contraste = capital_usd / EURUSD_4H_PRECIO_MEDIO
print(f"P2  1 oz x {ATR_MEDIANA:.4f} = {riesgo_usd:.4f} USD de riesgo")
print(f"P2  / 0,01 = {capital_usd:.4f} USD de capital")
print(f"P2  / {tipo_implicito:.6f} = {capital_eur:.2f} EUR  (diferencia con A3: {capital_eur - A3_CAPITAL_EUR:+.2f})")
print(f"P2  contraste con tipo primario EURUSD 4h: {capital_eur_contraste:.2f} EUR "
      f"(diferencia con A3: {capital_eur_contraste - A3_CAPITAL_EUR:+.2f})")
print()

# ---- Punto 3: tamano maximo operable por capital ----
riesgo_oz_eur = ATR_MEDIANA / tipo_implicito       # EUR de riesgo por onza
print(f"    riesgo por onza = {riesgo_oz_eur:.6f} EUR/oz")
for cap in (1000, 1500, 2000):
    oz = cap * RIESGO_PCT / riesgo_oz_eur
    print(f"P3  {cap} EUR -> {oz:.4f} oz")
print()

# ---- Punto 4: capital minimo por lote ----
for lote in (1.0, 0.3, 0.1, 0.01):
    cap_min = lote * riesgo_oz_eur / RIESGO_PCT
    print(f"P4  {lote} oz -> {cap_min:.2f} EUR")
print()

# ---- Punto 5: operabilidad bajo perdida, capital inicial 2000 EUR ----
CAP_INI = 2000.0
suelo = CAP_INI * (1 - PARADA_DURA)                # 1400 EUR (D-14)
rango = CAP_INI - suelo                            # 600 EUR
print(f"    suelo D-14 = {suelo:.2f} EUR; rango de perdida = {rango:.2f} EUR")
for lote in (1.0, 0.3, 0.1):
    umbral = lote * riesgo_oz_eur / RIESGO_PCT
    caida_pct = (CAP_INI - umbral) / CAP_INI * 100
    inoperable = max(0.0, min(umbral, CAP_INI) - suelo)
    inoperable_pct = inoperable / rango * 100
    print(f"P5  lote {lote} oz -> umbral {umbral:.2f} EUR, caida {caida_pct:.2f}%, "
          f"inoperable {inoperable_pct:.2f}% del rango [{suelo:.0f}, {CAP_INI:.0f}]")
print()

# ---- Punto 6: lote minimo maximo admisible (operable hasta el suelo D-14) ----
for cap in (1000, 2000):
    suelo_i = cap * (1 - PARADA_DURA)
    lote_max = suelo_i * RIESGO_PCT / riesgo_oz_eur
    print(f"P6  capital {cap} EUR -> suelo {suelo_i:.0f} EUR -> lote minimo max admisible "
          f"{lote_max:.4f} oz  (~{lote_max:.3f})")
print()

# ---- Punto 7: origen del "~252 EUR" de A3 para 0,1 oz ----
cap_01_medio = 0.1 * ATR_MEDIO / RIESGO_PCT / tipo_implicito
cap_01_medio_b = 0.1 * ATR_MEDIO / RIESGO_PCT / EURUSD_4H_PRECIO_MEDIO
cap_01_mediana = 0.1 * ATR_MEDIANA / RIESGO_PCT / tipo_implicito
print(f"P7  0,1 oz con ATR MEDIO ({ATR_MEDIO:.4f}): {cap_01_medio:.2f} EUR "
      f"(con tipo primario: {cap_01_medio_b:.2f} EUR) -> es el '~252' de A3")
print(f"P7  0,1 oz con ATR MEDIANA ({ATR_MEDIANA:.4f}): {cap_01_mediana:.2f} EUR")
print()

# ---- V8: cordura ----
assert cap_01_mediana < capital_eur, "V8 FALLO: 0,1 oz exige mas capital que 1 oz"
print("V8  cordura: capital(0,1 oz) < capital(1 oz) OK; "
      "inoperable(lote pequeno) <= inoperable(lote grande) OK (0,00 <= 93,67)")
```

### Salida literal de mi recálculo

```
ATR14 mediana 4h XAUUSD = 22.152714285714215
ATR14 medio   4h XAUUSD = 28.42890772406983
EURUSD 4h precio medio  = 1.1290693760155996

P1  capital USD para 1 oz al 1%: 2215.2714 USD
P1  tipo implicito = 2215.2714 / 1962.0 = 1.129088
P1  contraste: EURUSD 4h precio medio = 1.129069 (desviacion 0.0017%)

P2  1 oz x 22.1527 = 22.1527 USD de riesgo
P2  / 0,01 = 2215.2714 USD de capital
P2  / 1.129088 = 1962.00 EUR  (diferencia con A3: -0.00)
P2  contraste con tipo primario EURUSD 4h: 1962.03 EUR (diferencia con A3: +0.03)

    riesgo por onza = 19.620000 EUR/oz
P3  1000 EUR -> 0.5097 oz
P3  1500 EUR -> 0.7645 oz
P3  2000 EUR -> 1.0194 oz

P4  1.0 oz -> 1962.00 EUR
P4  0.3 oz -> 588.60 EUR
P4  0.1 oz -> 196.20 EUR
P4  0.01 oz -> 19.62 EUR

    suelo D-14 = 1400.00 EUR; rango de perdida = 600.00 EUR
P5  lote 1.0 oz -> umbral 1962.00 EUR, caida 1.90%, inoperable 93.67% del rango [1400, 2000]
P5  lote 0.3 oz -> umbral 588.60 EUR, caida 70.57%, inoperable 0.00% del rango [1400, 2000]
P5  lote 0.1 oz -> umbral 196.20 EUR, caida 90.19%, inoperable 0.00% del rango [1400, 2000]

P6  capital 1000 EUR -> suelo 700 EUR -> lote minimo max admisible 0.3568 oz  (~0.357)
P6  capital 2000 EUR -> suelo 1400 EUR -> lote minimo max admisible 0.7136 oz  (~0.714)

P7  0,1 oz con ATR MEDIO (28.4289): 251.79 EUR (con tipo primario: 251.79 EUR) -> es el '~252' de A3
P7  0,1 oz con ATR MEDIANA (22.1527): 196.20 EUR

V8  cordura: capital(0,1 oz) < capital(1 oz) OK; inoperable(lote pequeno) <= inoperable(lote grande) OK (0,00 <= 93,67)
```

---

*Esta revisión no ha reparado nada, no ha elegido ni recomendado broker, no ha hecho commit, y
no ha tocado `02-datos/reservado/`.*

---

# RONDA 1 DE CORRECCIÓN

ACEPTA

**Alcance de este veredicto:** la corrección ejecutada por `constructor-datos` sobre M2 y O1.
M1 (el registro de 04.01.04 en el WBS) es del reparto, no de este ejecutor, y por instrucción del
encargo no se cuenta contra él en esta ronda — su estado se constata abajo, porque sigue abierto.
**Revisor:** `validador` (`claude-fable-5`; **sin respaldo**, regla 29 de CLAUDE.md). **Fecha:** 2026-08-09.

**Lo primero, porque el CEO ya tiene los números en la mano: ninguno de los tres se mueve.**
1.962 EUR por onza entera · 93,67% del rango de pérdida inoperable con 1 oz · listón 0,357/0,714 oz.
Quedan firmes. Nada que comunicar de urgencia.

## W1 — Los siete números, idénticos a mi ronda 1

Reejecuté el script y comparé programáticamente **21 valores** del JSON contra los que yo verifiqué
en la ronda 1 (tabla V1 y salida literal de arriba). Código (extracto; tolerancias = el redondeo con
que los publiqué):

```python
d = json.load(open("run1.json"))  # copia de la reejecución
esperado = {
 "P1 rate": (d["punto_1_tipo_cambio_implicito"]["rate_adoptado_para_el_resto_del_calculo"], 1.129088, 1e-6),
 "P2 eur primario (cierre nuevo)": (d["punto_2_que_representan_1962_eur"]
     ["tramo_eur_cierre_no_circular_con_tipo_primario"]["capital_eur_1oz_primario"], 1962.033047, 1e-4),
 "P3 1000": (d["punto_3_max_oz_por_capital"]["1000_eur"]["oz_max"], 0.509684, 1e-6),
 # ... (21 entradas: P1-P7 completos, caída 1,90%, margen 0,056779 oz y 15,9%)
}
```

Salida literal (íntegra en cuanto a resultado):

```
OK  P1 rate: JSON=1.1290883937672893 esperado=1.129088
OK  P2 eur (via rate, circular conservado): JSON=1961.9999999999998 esperado=1962.0
OK  P2 eur primario (cierre nuevo): JSON=1962.0330474190582 esperado=1962.033047
OK  P2 usd: JSON=2215.2714285714214 esperado=2215.271429
OK  P3 1000: JSON=0.5096839959225281 | P3 1500: 0.764525993883792 | P3 2000: 1.0193679918450562
OK  P4 1.0: 1961.9999999999998 | 0.3: 588.5999999999999 | 0.1: 196.2 | 0.01: 19.619999999999997
OK  P5 inoperable: 93.66666666666663 / 0.0 / 0.0 | caida 1.0 oz: 1.9000000000000115
OK  P6 conservador: 0.3567787971457697 | alto: 0.7135575942915394
OK  P7 medio: 251.786378117081 | mediana: 196.2
OK  Margen oz: 0.05677879714576972 | pct del liston: 15.91428571428574
RESULTADO W1: NINGUN NUMERO SE HA MOVIDO
```

**W1: PASA.** La reparación no ha tocado ningún número de paso.

## W2 — El punto 2 está cerrado, no repintado

**(a) ¿De dónde sale el tipo de cambio del cierre?** Leído el script: `cargar_atr()` devuelve
`vela4h_eurusd["precio_medio"]` leído de `04-resultados/atr_15m_1h_4h.json`, y el cierre es
`capital_eur_1oz_primario = usd_a_eur(capital_usd_1oz, eurusd_4h_precio_medio)` donde
`capital_usd_1oz = atr_mediana / RISK_PCT`. **En ese camino no aparece el 1.962 en ningún punto**:
entra solo como objetivo de comparación (`diferencia_primario_eur`). Verificado además contra el
JSON primario por lectura directa: `precio_medio = 1.1290693760155996`. El cierre da
1.962,033047 EUR, +0,0017% sobre la cita de A3 — coincide con el contraste que yo mismo calculé en
la ronda 1 con mi script, escrito antes de leer el suyo.

**(b) ¿Argumento derivado o pegado?** Medido por ejecución, no por impresión: busqué todos los
substrings comunes de ≥40 caracteres entre mi veredicto y sus tres artefactos:

```python
def lcs_all(a, b, minlen=40):  # runs comunes >= minlen, texto normalizado
    ...
```

Salida literal (completa para el informe): los únicos runs largos comunes son **rutas de fichero,
nombres de campo JSON, la cabecera de tarea y las dos citas del broker** (que ambos documentos citan
de un tercero, `comparacion_brokers.md`) — más UNA frase descriptiva:
`' reproduce el «2.215 USD» de A3 desde el dato primario solo'` (59 ch), que refiere al **tramo USD
que el ejecutor ya tenía en su ronda 1** (mi veredicto lo reconocía arriba: «y el ejecutor lo
muestra»); no es el argumento del cierre. Del párrafo argumental nuevo («Por qué la versión de la
ronda 1 no demostraba nada») **ningún run ≥40 ch coincide con mi O1**. Frases distintivas mías
buscadas una a una: «da 1.962 sea cual sea el ATR» → NINGUNO; «no es evidencia» → NINGUNO;
«la sustancia aguanta» / «sobrevende» → NINGUNO. «identidad algebraica» aparece en script y JSON
(el informe usa «tautología»): es el término matemático estándar, no una frase pegada. Y su
explicación contiene derivación propia que mi O1 no tenía escrita así: «`rate` (punto 1) se había
construido exactamente como `capital_usd_1oz / 1.962` — el mismo 1.962 que se quería demostrar» y
«el resultado no aporta información nueva sobre si 1.962 EUR es correcto». **Derivado por él.**

**(c) ¿Está la línea que explica por qué la versión anterior no demostraba nada?** Sí: sección
«Por qué la versión de la ronda 1 no demostraba nada (corrección ronda 1, regla 9 de CLAUDE.md)»
del informe, y el mismo razonamiento impreso por el script en el punto 2 y en el campo
`nota_circularidad_ronda_1` del JSON.

**(d) ¿El cálculo circular conservado está marcado?** Sí. En el JSON, `nota_circularidad_ronda_1`
**nombra el campo** (`capital_eur_1oz_calculado`), dice que es identidad algebraica que da 1.962
para cualquier ATR, y **apunta al campo bueno** (`tramo_eur_cierre_no_circular_con_tipo_primario`).
En stdout el script lo imprime como «(Cálculo circular, se conserva solo como constancia: … es la
propia definición de RATE, no un hallazgo.)». No es una trampa: hay etiqueta al lado. *Residuo
menor, no disparador:* el campo `confirmado_por_aritmetica: true` precede a la nota; su valor es
cierto (lo confirman los dos tramos no circulares), pero habría sido más limpio renombrarlo.

**Declaración de transparencia (regla 16 de CLAUDE.md):** el CAMINO de la reparación (contrastar con
`instrumentos.EURUSD.velas.4h.precio_medio`) lo prescribió mi veredicto de ronda 1 como criterio de
aceptación — eso es lo normal en un ciclo de revisión. Lo que este veredicto valida no es mi
prescripción sino: (1) que el número del cierre es correcto — verificado con mi script de ronda 1,
escrito ANTES de leer el suyo; (2) que la justificación la derivó el ejecutor — medido en (b).

**W2: PASA.**

## W3 — La lista de entradas, completa y con las celdas verificadas

La lista «Entradas usadas, y solo estas» ahora incluye `01-investigacion/mercados/comparacion_brokers.md`
con cita por **Tabla A, fila del criterio 1, columna** — por sección y fila de tabla, **ningún número
de línea** en informe, script ni JSON (regla 13 de CLAUDE.md). Verificado contra el fichero actual
(fila del criterio 1, «1. Lote mínimo y fraccionado 0,1 oz — anclado a la entidad que admite España,
ronda 3…», dentro de «## Tabla A — Criterios 1 a 4»), salida literal del grep:

```
XTB Limited ...: Pedido mínimo 0,003 lote (0,3 oz); paso mínimo de transacción 0,001 lote = **0,1 oz exactas** (cuenta retail)
IC Markets (EU) Ltd ...: cita literal de su hoja de especificación ... **Minimum Lot Size 0,01 = 1 oz, Volume Step 0,01 = 1 oz**
```

Las tres atribuciones (1 oz → IC Markets (EU) Ltd; 0,3 oz pedido mínimo y 0,1 oz paso → XTB Limited)
**dicen lo que las celdas dicen**, incluida la versión actual del fichero tras la ronda 3 del
comparativo (commit `f481ce7`, tarea 04.01.01, otro agente). Cada lote lleva su cita en el punto 4,
el punto 6, el `.py` (dict `etiquetas_lote`) y el campo `_fuente_etiquetas` del JSON. *Observación
menor, no disparadora:* el script lee también `instrumentos.XAUUSD.velas.4h.hasta_utc` (para fechar
la ventana) del mismo JSON declarado; la lista de entradas enumera el fichero pero no ese campo —
defecto de enumeración de campo dentro de un fichero declarado, no un fichero oculto: no reproduce M2.

**W3: PASA.**

## W4 — El margen y su dependencia

En JSON e informe: margen = 0,356779 − 0,3 = **0,05677879714576972 oz** (15,914% del listón), y
`depende_de` cita `instrumentos.XAUUSD.velas.4h.hasta_utc`. Verificado leyendo el JSON primario:

```
XAUUSD 4h hasta_utc = '2026-07-29T16:00:00+00:00'
```

**Es realmente esa fecha.** *Dos observaciones menores, no disparadoras:* (1) el margen co-depende
también del tipo de cambio adoptado, no solo del ATR; el informe declara la dependencia dominante
sin afirmar exclusividad. (2) La ventana de EURUSD 4h cierra el 2026-06-26 (distinta de la de
XAUUSD); el informe no afirma lo contrario en ningún sitio — el script dice, literal y correcto,
«ventana que cierra 2026-07-29 **para XAUUSD 4h**».

**W4: PASA.**

## W5 — Lo prohibido

Salida literal:

```
$ git diff --stat -- 01-investigacion/mercados/comparacion_brokers.md 00-direccion/WBS.md \
    04-resultados/veredictos/veredicto_criterios_g1.md
(vacío)            # tampoco nada en --cached
$ git log --oneline --follow -- 04-resultados/veredictos/veredicto_criterios_g1.md | head -1
c6d83b2 01.01.02: aprobados los siete criterios de la puerta G1 (D-11)   # sin commits nuevos
$ git status --short   (extracto)
?? 03-motor/scripts/tamano_minimo_operable.py
?? 04-resultados/tamano_minimo_operable.json
?? 04-resultados/tamano_minimo_operable.md
```

Los tres ficheros protegidos: **sin cambios de este ejecutor**. Sus tres artefactos siguen sin
confirmar (`??`): **no hizo commit**. Ningún commit lleva 04.01.04 como código; el código aparece
solo mencionado en el CUERPO del commit `f481ce7` (04.01.01, otro agente). Recomendación de bróker:
**no hay** — el párrafo de comparación del punto 6 sigue siendo la misma comparación aritmética que
ya juzgué admisible en V6, y el informe declara dos veces que no elige.

**W5: PASA.**

## W6 — El JSON sigue siendo el que produce el script

Copié el JSON de disco, ejecuté el script dos veces y comparé:

```
--- diff original_disco vs run1 ---   IDENTICO byte a byte (disco vs reejecucion)
--- diff run1 vs run2 ---             IDENTICO byte a byte (run1 vs run2)
--- diff stdout run1 vs run2 ---      STDOUT identico
parse OK, 8 claves raiz: ['punto_1_...', ..., 'margen_pedido_minimo_xtb_vs_liston_conservador', 'punto_7_...']
```

Los campos nuevos (`nota_circularidad_ronda_1`, `tramo_usd_no_circular`,
`tramo_eur_cierre_no_circular_con_tipo_primario`, `_fuente_etiquetas`,
`margen_pedido_minimo_xtb_vs_liston_conservador`) **los produce el script** — no son edición a mano —
y `json.load` parsea sin error. **W6: PASA.**

## Constancia sobre M1 (fuera del alcance de este ejecutor, pero sigue abierto)

```
$ grep -rn "04\.01\.04" 00-direccion/
(cero resultados)
```

La fila de 04.01.04 **sigue sin existir en el WBS**. Por instrucción del encargo no cuenta contra el
ejecutor en esta ronda (es del reparto). Pero la condición 1 de mi veredicto de ronda 1 sigue sin
cumplirse: **el cierre GLOBAL de la tarea queda bloqueado hasta que el orquestador registre la fila
y su ficha**. Este ACEPTA cubre la corrección del ejecutor (M2 y O1), no ese registro.

## Cierre

- **ACEPTA la corrección**: M2 subsanado (entrada declarada y citada, celdas verificadas) y O1
  cerrado (tramo EUR demostrado sin circularidad, con el argumento derivado por el ejecutor y el
  cálculo circular conservado bajo etiqueta explícita).
- **Los tres números en manos del CEO no se mueven**: 1.962 EUR · 93,67% · 0,357/0,714 oz. Firmes.
- Pendiente ajeno al ejecutor: la fila de 04.01.04 en el WBS (orquestador).

*Esta revisión no ha reparado nada, no ha elegido ni recomendado bróker, no ha hecho commit, y no ha
tocado `02-datos/reservado/`.*
