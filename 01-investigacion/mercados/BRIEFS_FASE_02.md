# Briefs para el chat analista — Fase 02 (elegir mercado y tamaño de vela)

> Cómo usarlos: abre un chat nuevo (el "chat analista"), pega el Brief A. Cuando entregue, pega el Brief B en el mismo chat. Trae los dos resultados aquí y yo hago la revisión independiente (tarea 02.03.01).
>
> Regla que llevan dentro: el analista entrega **números, método y fuentes**, nunca conclusiones ni recomendaciones. Elegir es trabajo de la puerta G1, no suyo.

---

## BRIEF A — cubre las tareas 02.01.02, 02.02.01 y 02.02.02

```
Actúa como analista cuantitativo de mercados financieros. Trabajas para un proyecto que va a
decidir en qué mercado operará un bot automático. Tu papel es SOLO medir y documentar: no
recomiendas, no eliges y no sacas conclusiones. Otra persona decide con tus números delante.

CANDIDATOS (8): EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD (oro), BTCUSD, ETHUSD
TAMAÑOS DE VELA (3): 15 minutos, 1 hora, 4 horas

ENTREGA 1 — Coste típico de operar cada mercado.
Para cada uno de los 8, indica el spread (horquilla) típico y la comisión típica en brokers
minoristas grandes y regulados. Da el valor en la unidad natural del instrumento (pips o puntos)
y el rango que has encontrado, no un solo número. Cita para cada dato la fuente concreta (nombre
del broker o publicación y enlace) y la fecha del dato.

ENTREGA 2 — Movimiento medio por vela.
Para cada combinación de instrumento y tamaño de vela (8 x 3 = 24 celdas), estima el ATR medio
(rango medio de una vela) de los últimos 2 años. Indica la fuente de los datos de precio y el
periodo exacto usado. Si para alguna celda no hay dato fiable, escribe "sin dato fiable" y
explica por qué; no lo rellenes con una estimación disfrazada de medida.

ENTREGA 3 — Coste relativo.
Calcula, para cada una de las 24 celdas, el coste de operar dividido entre el movimiento medio
de la vela, expresado en porcentaje. Muestra la fórmula y un ejemplo de cálculo completo paso a
paso para que otra persona pueda repetirlo.

FORMATO DE SALIDA
- Tabla 1: costes por instrumento (8 filas).
- Tabla 2: movimiento medio (8 filas x 3 columnas).
- Tabla 3: coste relativo en % (8 filas x 3 columnas).
- Lista de advertencias: qué datos son flojos, qué supuestos has tenido que hacer y dónde puede
  haber error.
- Lista de fuentes con enlaces.

PROHIBIDO: recomendar un mercado, decir cuál es "el mejor", ordenar por preferencia o sacar
conclusiones. Si te falta un dato, dilo; no lo inventes ni lo aproximes en silencio.
```

---

## BRIEF B — cubre las tareas 02.02.03 y 02.02.04

```
Actúa como analista de datos de mercados financieros. Tu papel es SOLO medir y documentar: no
recomiendas, no eliges y no sacas conclusiones.

CANDIDATOS (8): EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD (oro), BTCUSD, ETHUSD

ENTREGA 1 — Matriz de correlaciones.
Calcula o localiza la correlación de los rendimientos diarios entre los 8 instrumentos, con un
mínimo de 2 años de datos. Entrega la matriz completa 8 x 8. Indica el periodo exacto, la fuente
de los precios y el método usado (correlación de Pearson sobre rendimientos diarios, salvo que
uses otro y lo justifiques). Señala si alguna pareja cambia mucho de correlación según el
periodo elegido.

ENTREGA 2 — Datos históricos disponibles.
Para cada instrumento, documenta qué histórico de precios se puede conseguir hoy:
- Años disponibles hacia atrás.
- Tamaño de vela mínimo disponible (idealmente 1 minuto).
- Fuente concreta: nombre del proveedor y enlace.
- Coste: gratis, de pago (con precio) o requiere cuenta.
- Calidad conocida: huecos, fiabilidad, si incluye o no el spread.
Da al menos dos opciones de fuente por instrumento cuando existan.

FORMATO DE SALIDA
- Tabla 1: matriz de correlaciones 8 x 8.
- Tabla 2: datos disponibles (una fila por instrumento y fuente).
- Lista de advertencias sobre calidad y limitaciones.
- Lista de fuentes con enlaces.

PROHIBIDO: recomendar instrumentos, agruparlos por preferencia o sacar conclusiones. Si un dato
no es fiable, dilo claramente en vez de rellenar el hueco.
```

---

## Qué haré yo cuando traigas los resultados (tarea 02.03.01)

1. Comprobar que cada número lleva fuente y método, y descartar los que no.
2. Repetir a mano 2-3 cálculos de coste relativo para ver si cuadran.
3. Buscar contradicciones entre las dos entregas y señalar los datos flojos.
4. Con los números ya limpios, **calibrar los umbrales** de la puerta G1 (dónde se pone el corte
   de coste relativo y de correlación) y preparar el informe de decisión (02.03.02) para que
   elijas en G1.
