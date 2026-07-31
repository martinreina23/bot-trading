# Matriz de correlaciones 8×8 sobre rendimientos logarítmicos (Tarea 02.02.03)

**Agente:** `constructor-datos` (`claude-sonnet-5`). **Fecha de ejecución:** 2026-07-31.
**Script:** `03-motor/scripts/correlaciones_mercado.py` (ejecutado entero, salida completa leída antes
de esta entrega — regla 15 de CLAUDE.md (regla 22 del WBS)). Reutiliza sin duplicar `remuestrear` de
`03-motor/scripts/precios_mercado.py` (T2: la lógica de remuestreo vive en un solo sitio). La única
capacidad nueva se añadió **en ese fichero**, no aquí: la vela `"1d"`, anclada al corte de 22:00 UTC
(`resample("24h", offset=22h)`); 15min/1h/4h no cambiaron ni un bit respecto a la versión ya verificada
en 02.02.01.
**Resultado en bruto:** `04-resultados/correlaciones_8x8.json`.
**No se descargó nada nuevo:** todo se calculó sobre lo ya descargado por 02.02.01 en `02-datos/bruto/`
(`git status --porcelain 02-datos/` sigue vacío tras esta tarea — regla 27 comprobada).

## Qué es EXACTAMENTE cada instrumento (regla 5 del rol, lección L-007)

Idéntico a 02.02.01, sin cambios: **EURUSD/GBPUSD/USDJPY/AUDUSD/USDCHF** = precio BID de forex
minorista agregado (HistData.com) · **XAUUSD** = oro **al contado** (spot/OTC, Dukascopy, lado BID),
**nunca** el futuro GC=F · **BTCUSD/ETHUSD** = pares **reales contra USD** en Kraken (XBTUSD, ETHUSD),
**nunca** contra USDT/Tether.

## Método

- **Rendimientos logarítmicos**, nunca precios: `r_t = ln(close_t / close_{t-1})` sobre el precio de
  cierre de cada vela. Correlacionar precios da correlaciones espurias (por tendencia común, no por
  relación real entre los activos).
- **Correlación de Pearson**, por pares, solo sobre observaciones donde **ambos** instrumentos tienen
  dato real y simultáneo — sin relleno, sin interpolación (regla 14 de CLAUDE.md).
- **3 ventanas:** 3 meses (90 días), 1 año (365 días), 2 años (730 días).
- **4 velas:** 15min, 1h, 4h (las tres pedidas por el WBS) y 1d (diaria, de comprobación).
- **Corte único 22:00 UTC:** ancla el borde de cada ventana y, en la vela diaria, el propio límite del
  "día". Sin este corte único, forex/oro/cripto cortarían el día a horas distintas y la correlación
  medida sería falsa (L-008).
- **Ancla de ventana (el "fin" común):** la fecha `min(hasta_utc)` entre los **6 instrumentos
  forex+oro** para esa vela — nunca se ancla en cripto, porque su caché siempre es la más reciente y
  desplazaría la ventana en cada ejecución. Esto hace la ventana **reproducible** para los 15 pares
  no-cripto. Motivo del ancla no en "hoy": HistData (los 5 pares forex) tiene un retraso de publicación
  real de ~5 semanas frente a Dukascopy/Kraken (los 5 forex terminan el 2026-06-26; XAUUSD llega hasta
  el 2026-07-29; la caché de cripto hasta el 2026-07-31). Anclar en "hoy" habría desperdiciado ~5
  semanas de datos reales de forex sin necesidad.
- **Umbral de hueco:** una celda se declara hueco si (a) las observaciones solapadas son menos de 20
  (mismo umbral que usa 02.02.01 para el ATR), o (b) — el caso que de verdad importa aquí — el
  **historial total** de un instrumento cripto (de punta a punta de su caché) es menor que la ventana
  nominal pedida. Sin (b), un BTCUSD con solo 120 días de caché habría "colado" como si tuviera
  correlación de 1 año o 2 años, solo porque 120 días caben dentro del rango de fechas (enorme) de esas
  ventanas nominales. Es exactamente lo que el encargo prohíbe: no estimar, no rellenar.

## PRUEBA DE CORDURA OBLIGATORIA — EURUSD/USDCHF

**Resultado: PASA.** Fuertemente **NEGATIVO** en las 12 combinaciones de vela × ventana (rango
-0,72 a -0,87; el brief citaba ~-0,97 como referencia orientativa, y L-008 ya advertía que el valor
exacto varía con la ventana). Ningún signo positivo en ninguna celda: no hay indicio de error de
convención (L-006).

| Vela | 3 meses | 1 año | 2 años |
|---|---|---|---|
| 15min | -0,7818 | -0,7952 | -0,7158 |
| 1h | -0,8125 | -0,8214 | -0,7443 |
| 4h | -0,8298 | -0,8497 | -0,7637 |
| 1d | -0,7960 | -0,8720 | -0,8209 |

**Verificación cruzada de convención (más allá de lo exigido, para reforzar la confianza en el
signo):** USDJPY y USDCHF cotizan con el dólar como base (USD/XXX), al revés que EUR/GBP/AUD
(XXX/USD) — L-006. Si la convención estuviera bien, EURUSD debería ir **negativo** también frente a
USDJPY (dólar en el mismo lado que en USDCHF) y USDJPY/USDCHF deberían ir **positivos** entre sí
(mismo lado del dólar). En 4h/3 meses: EURUSD/USDJPY = -0,52, USDJPY/USDCHF = +0,56. Ambos con el
signo esperado. Sin indicio de convención invertida en ningún par.

**Contraste independiente (ejecutado, no solo revisado):** se recalculó EURUSD/USDCHF en 4h/3 meses
con un `resample` directo de pandas, sin pasar por `remuestrear` ni por el resto del script
(`np.log(close/close.shift(1)).corr()` sobre un resample básico `label="left", closed="left"`,
mismo ancla y misma ventana). Resultado: **-0,8298151...** frente a **-0,8298** del script — coincide
a 4 decimales. Se repitió el contraste con BTCUSD/ETHUSD en 4h/3 meses (mismo método, mismo ancla):
**0,8790213...** frente a **0,8790** del script. Coincide.

## Hueco conocido — BTCUSD/ETHUSD (declarado, NO rellenado)

BTCUSD y ETHUSD solo tienen 720 velas cerradas por instrumento en la caché de 02.02.01 (ventana
deslizante de Kraken, endpoint público `/OHLC`, sin profundidad de 1 año/2 años):

| Vela | Profundidad real de la caché |
|---|---|
| 15min | 7,4 días (2026-07-24 → 2026-07-31) |
| 1h | 30 días (2026-07-01 → 2026-07-31) |
| 4h | 120 días (2026-04-02 → 2026-07-31) |
| 1d | **no existe**: no hay 1-minuto de Kraken para remuestrear con el corte 22:00 UTC exacto, y agregar desde las velas 4h nativas (rejilla 0/4/8/12/16/20 UTC, no anclada a 22:00) produciría un día cortado a otra hora — el fallo que el corte único prohíbe. No se descargó una granularidad diaria nueva de Kraken: cambiaría de fuente para rellenar, contra la instrucción explícita del encargo. |

Consecuencia, calculada (no supuesta): la ventana de **2 años NO EXISTE** para BTCUSD/ETHUSD en
ninguna vela, y la de **1 año tampoco**, en ninguna vela — incluida la 4h, cuyos 120 días de caché
son menos que los 365 días de la ventana de 1 año. La **única** combinación cripto con datos reales
suficientes es **4h × 3 meses** (120 días de caché ≥ 90 días de ventana): ahí sí hay 8×8 completa,
incluida BTCUSD/ETHUSD entre sí y frente a los 6 instrumentos forex+oro.

Todas las celdas que involucran BTCUSD o ETHUSD llevan **`reproducible: false`** en el JSON, con el
mismo motivo que 02.02.01: la ventana de Kraken se desliza en cada ejecución, así que una re-ejecución
separada por más de 120 días no comparte ni una sola vela con esta.

Total de huecos: 13 pares (12 cruces forex/oro↔cripto + BTCUSD/ETHUSD) en 11 de las 12 combinaciones
vela×ventana; 0 huecos en 4h/3 meses.

## Matrices 8×8 (rendimiento logarítmico, correlación de Pearson)

Orden: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCHF, XAUUSD, BTCUSD, ETHUSD. `—` = hueco (ver arriba).
`n` de observaciones y desglose completo de huecos con su motivo: `04-resultados/correlaciones_8x8.json`.

### Vela 15min — ventana 3 meses

Ancla (fin común forex+oro): 2026-06-26T21:30 UTC · inicio ventana: 2026-03-28T21:30 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.85 | -0.55 | +0.78 | -0.78 | +0.06 | — | — |
| GBPUSD | +0.85 | +1.00 | -0.50 | +0.77 | -0.72 | +0.04 | — | — |
| USDJPY | -0.55 | -0.50 | +1.00 | -0.48 | +0.53 | -0.01 | — | — |
| AUDUSD | +0.78 | +0.77 | -0.48 | +1.00 | -0.67 | +0.06 | — | — |
| USDCHF | -0.78 | -0.72 | +0.53 | -0.67 | +1.00 | -0.03 | — | — |
| XAUUSD | +0.06 | +0.04 | -0.01 | +0.06 | -0.03 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 15min — ventana 1 año

Ancla: 2026-06-26T21:30 UTC · inicio: 2025-06-26T21:30 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.80 | -0.60 | +0.68 | -0.80 | +0.19 | — | — |
| GBPUSD | +0.80 | +1.00 | -0.53 | +0.68 | -0.66 | +0.20 | — | — |
| USDJPY | -0.60 | -0.53 | +1.00 | -0.41 | +0.60 | -0.09 | — | — |
| AUDUSD | +0.68 | +0.68 | -0.41 | +1.00 | -0.53 | +0.29 | — | — |
| USDCHF | -0.80 | -0.66 | +0.60 | -0.53 | +1.00 | -0.17 | — | — |
| XAUUSD | +0.19 | +0.20 | -0.09 | +0.29 | -0.17 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 15min — ventana 2 años

Ancla: 2026-06-26T21:30 UTC · inicio: 2024-06-26T21:30 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.78 | -0.48 | +0.62 | -0.72 | +0.14 | — | — |
| GBPUSD | +0.78 | +1.00 | -0.41 | +0.66 | -0.58 | +0.15 | — | — |
| USDJPY | -0.48 | -0.41 | +1.00 | -0.26 | +0.62 | -0.06 | — | — |
| AUDUSD | +0.62 | +0.66 | -0.26 | +1.00 | -0.40 | +0.21 | — | — |
| USDCHF | -0.72 | -0.58 | +0.62 | -0.40 | +1.00 | -0.12 | — | — |
| XAUUSD | +0.14 | +0.15 | -0.06 | +0.21 | -0.12 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 1h — ventana 3 meses

Ancla: 2026-06-26T20:00 UTC · inicio: 2026-03-28T20:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.86 | -0.53 | +0.80 | -0.81 | +0.11 | — | — |
| GBPUSD | +0.86 | +1.00 | -0.50 | +0.79 | -0.76 | +0.07 | — | — |
| USDJPY | -0.53 | -0.50 | +1.00 | -0.46 | +0.54 | -0.04 | — | — |
| AUDUSD | +0.80 | +0.79 | -0.46 | +1.00 | -0.70 | +0.08 | — | — |
| USDCHF | -0.81 | -0.76 | +0.54 | -0.70 | +1.00 | -0.06 | — | — |
| XAUUSD | +0.11 | +0.07 | -0.04 | +0.08 | -0.06 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 1h — ventana 1 año

Ancla: 2026-06-26T20:00 UTC · inicio: 2025-06-26T20:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.80 | -0.60 | +0.69 | -0.82 | +0.20 | — | — |
| GBPUSD | +0.80 | +1.00 | -0.54 | +0.69 | -0.68 | +0.20 | — | — |
| USDJPY | -0.60 | -0.54 | +1.00 | -0.41 | +0.62 | -0.06 | — | — |
| AUDUSD | +0.69 | +0.69 | -0.41 | +1.00 | -0.56 | +0.30 | — | — |
| USDCHF | -0.82 | -0.68 | +0.62 | -0.56 | +1.00 | -0.17 | — | — |
| XAUUSD | +0.20 | +0.20 | -0.06 | +0.30 | -0.17 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 1h — ventana 2 años

Ancla: 2026-06-26T20:00 UTC · inicio: 2024-06-26T20:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.79 | -0.51 | +0.61 | -0.74 | +0.15 | — | — |
| GBPUSD | +0.79 | +1.00 | -0.42 | +0.67 | -0.59 | +0.16 | — | — |
| USDJPY | -0.51 | -0.42 | +1.00 | -0.25 | +0.64 | -0.04 | — | — |
| AUDUSD | +0.61 | +0.67 | -0.25 | +1.00 | -0.40 | +0.22 | — | — |
| USDCHF | -0.74 | -0.59 | +0.64 | -0.40 | +1.00 | -0.12 | — | — |
| XAUUSD | +0.15 | +0.16 | -0.04 | +0.22 | -0.12 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 4h — ventana 3 meses (única combinación con cripto completo — 0 huecos)

Ancla: 2026-06-26T16:00 UTC · inicio: 2026-03-28T16:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.87 | -0.52 | +0.79 | -0.83 | +0.57 | +0.25 | +0.28 |
| GBPUSD | +0.87 | +1.00 | -0.51 | +0.80 | -0.82 | +0.55 | +0.26 | +0.28 |
| USDJPY | -0.52 | -0.51 | +1.00 | -0.47 | +0.56 | -0.31 | -0.13 | -0.13 |
| AUDUSD | +0.79 | +0.80 | -0.47 | +1.00 | -0.76 | +0.58 | +0.31 | +0.33 |
| USDCHF | -0.83 | -0.82 | +0.56 | -0.76 | +1.00 | -0.56 | -0.28 | -0.28 |
| XAUUSD | +0.57 | +0.55 | -0.31 | +0.58 | -0.56 | +1.00 | +0.38 | +0.41 |
| BTCUSD | +0.25 | +0.26 | -0.13 | +0.31 | -0.28 | +0.38 | +1.00 | +0.88 |
| ETHUSD | +0.28 | +0.28 | -0.13 | +0.33 | -0.28 | +0.41 | +0.88 | +1.00 |

### Vela 4h — ventana 1 año

Ancla: 2026-06-26T16:00 UTC · inicio: 2025-06-26T16:00 UTC. Cripto hueco (120 días de caché < 365).

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.81 | -0.62 | +0.68 | -0.85 | +0.38 | — | — |
| GBPUSD | +0.81 | +1.00 | -0.55 | +0.69 | -0.72 | +0.37 | — | — |
| USDJPY | -0.62 | -0.55 | +1.00 | -0.41 | +0.63 | -0.20 | — | — |
| AUDUSD | +0.68 | +0.69 | -0.41 | +1.00 | -0.58 | +0.47 | — | — |
| USDCHF | -0.85 | -0.72 | +0.63 | -0.58 | +1.00 | -0.38 | — | — |
| XAUUSD | +0.38 | +0.37 | -0.20 | +0.47 | -0.38 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | +1.00 | — |
| ETHUSD | — | — | — | — | — | — | — | +1.00 |

### Vela 4h — ventana 2 años

Ancla: 2026-06-26T16:00 UTC · inicio: 2024-06-26T16:00 UTC. Cripto hueco (120 días de caché < 730).

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.80 | -0.53 | +0.62 | -0.76 | +0.30 | — | — |
| GBPUSD | +0.80 | +1.00 | -0.43 | +0.67 | -0.61 | +0.31 | — | — |
| USDJPY | -0.53 | -0.43 | +1.00 | -0.25 | +0.65 | -0.17 | — | — |
| AUDUSD | +0.62 | +0.67 | -0.25 | +1.00 | -0.40 | +0.35 | — | — |
| USDCHF | -0.76 | -0.61 | +0.65 | -0.40 | +1.00 | -0.30 | — | — |
| XAUUSD | +0.30 | +0.31 | -0.17 | +0.35 | -0.30 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | +1.00 | — |
| ETHUSD | — | — | — | — | — | — | — | +1.00 |

### Vela 1d — ventana 3 meses (comprobación; cripto hueco — ver sección de huecos)

Ancla: 2026-06-24T22:00 UTC · inicio: 2026-03-26T22:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.88 | -0.51 | +0.83 | -0.80 | +0.68 | — | — |
| GBPUSD | +0.88 | +1.00 | -0.56 | +0.77 | -0.79 | +0.60 | — | — |
| USDJPY | -0.51 | -0.56 | +1.00 | -0.54 | +0.65 | -0.49 | — | — |
| AUDUSD | +0.83 | +0.77 | -0.54 | +1.00 | -0.72 | +0.73 | — | — |
| USDCHF | -0.80 | -0.79 | +0.65 | -0.72 | +1.00 | -0.67 | — | — |
| XAUUSD | +0.68 | +0.60 | -0.49 | +0.73 | -0.67 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 1d — ventana 1 año

Ancla: 2026-06-24T22:00 UTC · inicio: 2025-06-24T22:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.82 | -0.67 | +0.68 | -0.87 | +0.38 | — | — |
| GBPUSD | +0.82 | +1.00 | -0.60 | +0.70 | -0.74 | +0.37 | — | — |
| USDJPY | -0.67 | -0.60 | +1.00 | -0.43 | +0.62 | -0.21 | — | — |
| AUDUSD | +0.68 | +0.70 | -0.43 | +1.00 | -0.59 | +0.52 | — | — |
| USDCHF | -0.87 | -0.74 | +0.62 | -0.59 | +1.00 | -0.42 | — | — |
| XAUUSD | +0.38 | +0.37 | -0.21 | +0.52 | -0.42 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

### Vela 1d — ventana 2 años

Ancla: 2026-06-24T22:00 UTC · inicio: 2024-06-24T22:00 UTC

|  | EURUSD | GBPUSD | USDJPY | AUDUSD | USDCHF | XAUUSD | BTCUSD | ETHUSD |
|---|---|---|---|---|---|---|---|---|
| EURUSD | +1.00 | +0.80 | -0.61 | +0.62 | -0.82 | +0.38 | — | — |
| GBPUSD | +0.80 | +1.00 | -0.52 | +0.68 | -0.64 | +0.39 | — | — |
| USDJPY | -0.61 | -0.52 | +1.00 | -0.34 | +0.68 | -0.26 | — | — |
| AUDUSD | +0.62 | +0.68 | -0.34 | +1.00 | -0.44 | +0.47 | — | — |
| USDCHF | -0.82 | -0.64 | +0.68 | -0.44 | +1.00 | -0.37 | — | — |
| XAUUSD | +0.38 | +0.39 | -0.26 | +0.47 | -0.37 | +1.00 | — | — |
| BTCUSD | — | — | — | — | — | — | — | — |
| ETHUSD | — | — | — | — | — | — | — | — |

## Pares que superan |0,7| en alguna de las tres ventanas — criterio 4 de G1

**8 pares distintos** superan |0,7| en al menos una combinación vela×ventana (de 28 pares posibles),
listados por su correlación máxima en valor absoluto observada:

| Par | \|corr\| máx | Dónde se observó | Reproducible |
|---|---|---|---|
| EURUSD/GBPUSD | 0,8801 | 1d / 3 meses | sí |
| BTCUSD/ETHUSD | 0,8790 | 4h / 3 meses (única ventana con datos cripto reales) | **NO** — ventana Kraken deslizante |
| EURUSD/USDCHF | 0,8720 | 1d / 1 año | sí (esperado: comparten dólar en lados opuestos) |
| EURUSD/AUDUSD | 0,8271 | 1d / 3 meses | sí |
| GBPUSD/USDCHF | 0,8191 | 4h / 3 meses | sí |
| GBPUSD/AUDUSD | 0,8027 | 4h / 3 meses | sí |
| AUDUSD/USDCHF | 0,7616 | 4h / 3 meses | sí |
| AUDUSD/XAUUSD | 0,7331 | 1d / 3 meses | sí |

Detalle completo (las 42 celdas concretas que superan 0,7, con su `n` de observaciones) está en
`04-resultados/correlaciones_8x8.json`, campo `pares_sobre_umbral_g1`.

**Lectura para G1:** de los 5 pares de forex, **4 quedan implicados** en al menos un par que supera
0,7 (todos salvo USDJPY, que en cambio va negativo con EUR/GBP y positivo con USDCHF por la
convención invertida del dólar — L-006 — sin superar 0,7 en ningún caso con ninguno de los 8). Esto
confirma la advertencia ya escrita en el criterio de G1: *"5 pares de forex no son 5 apuestas"* — al
menos EURUSD, GBPUSD, AUDUSD y USDCHF comparten una parte sustancial de su movimiento vía el dólar.
XAUUSD queda por debajo de 0,7 frente a los 5 pares de forex en todas las combinaciones **excepto**
frente a AUDUSD en 1d/3 meses (0,7331): el resto de su correlación con forex se mueve en 0,04–0,68,
bastante más diversificador. BTCUSD/ETHUSD entre sí superan 0,7 en la única ventana con datos reales
(4h/3 meses); frente a forex/oro, cripto se queda siempre por debajo de 0,7 en esa misma ventana
(máximo: XAUUSD/ETHUSD = 0,41).

## Límites de este resultado (para que G1 los tenga delante)

1. **Forex tiene un retraso de publicación real de ~5 semanas** (HistData no ha publicado julio 2026
   todavía al ejecutar esta tarea: los 5 pares terminan en 2026-06-26, mientras que oro llega a
   2026-07-29 y cripto a 2026-07-31). El ancla de ventana usada compensa esto usando el dato real más
   reciente de forex como referencia común, en vez de "hoy" — de lo contrario se habrían desperdiciado
   ~5 semanas de datos reales de forex sin necesidad. Es una propiedad de la fuente, no un error de
   este script; queda documentada aquí porque condiciona directamente el solapamiento disponible con
   cripto.
2. **BTCUSD/ETHUSD no son reproducibles** en ninguna celda por la ventana deslizante de Kraken — igual
   que en 02.02.01. Cualquier reejecución de este script en otro momento dará números de cripto
   distintos (18 celdas no-cripto por combinación se mantienen estables si no pasa un día más).
3. **La vela diaria (1d) es de comprobación**, tal y como pide el encargo; no sustituye a 15min/1h/4h,
   que son las tres que la ficha original preveía. Para cripto queda deliberadamente hueca en la
   vela 1d, por el motivo explicado arriba (no romper el corte único).
4. **Este informe no elige mercado ni vela** — esa decisión es de G1, con el CEO, usando los 12
   matrices completas.
