# Motor de backtest -- 04.03.07

Construido desde cero contra `03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`, sin leer el motor
anterior (`git show 0c35959`) ni `/home/server/projects/gold-bot-2` (prohibicion de la ficha,
cumplida -- ver la lista de ficheros leidos en el mensaje de entrega).

## Raiz del motor

`<dir_motor>` = **`03-motor/backtester/`** (este directorio). Todas las pruebas de aceptacion de
la especificacion (`grep -rn ... <dir_motor>`, `pytest -q <dir_motor> ...`) se ejecutan contra
este directorio completo, incluida `tests/`.

## Los dos nombres de simbolo que exige R-06(c)

Declaracion obligatoria (seccion 6 de la orden de la tarea, R-06(c) de la especificacion): para
que la prueba de sabotaje se pueda ejecutar, el README tiene que nombrar la funcion de fill de
stop y la funcion de cargo de swap, sin ambiguedad.

| Requisito | Simbolo | Fichero |
|---|---|---|
| Funcion de fill de un stop de proteccion (R-02) | **`resolver_fill_stop`** | `03-motor/backtester/motor.py` |
| Funcion de cargo de swap (R-03/C-7) | **`calcular_apuntes_swap`** | `03-motor/backtester/motor.py` |

Las dos son funciones de MODULO (no metodos de clase, no lambdas, no closures locales), y
`simular()` las llama siempre por su nombre de modulo -- nunca via un alias local capturado antes
del bucle -- para que `pytest -q 03-motor/backtester -k camino_unico` (el test `test_camino_unico`
de `tests/test_r06_camino_unico.py`) pueda interceptarlas con
`monkeypatch.setattr(motor, "resolver_fill_stop", ...)` / `monkeypatch.setattr(motor,
"calcular_apuntes_swap", ...)` y medir si algun fill o algun apunte se produjo sin pasar por ahi.

## Estructura

```
03-motor/backtester/
  __init__.py
  configuracion.py     -- dataclasses de config (ConfigInstrumento, ConfigCuenta) y el loader que
                           lee `config_datos/*.json` (C-8: ninguna cifra de mercado vive en .py)
  datos.py              -- R-12 (carga estricta del CSV.gz de precios_mercado.py) y R-06(a)/R-08
                           (remuestreo a 4h via `remuestrear` de precios_mercado.py, sin reimplementar)
  motor.py              -- el motor: resolver_fill_stop, calcular_apuntes_swap, dimensionar,
                           simular() y las estructuras de registro (Apunte, Operacion, Decision,
                           SimulacionResultado)
  config_datos/
    xauusd.json          -- config PROVISIONAL de XAUUSD (R-09, R-13), versionada en git
  tests/
    conftest.py           -- fixtures comunes, incluidos los tres casos a lapiz (CL-1, CL-2, CL-2b)
    test_r01_costes.py .. test_r16_rutas_explicitas.py  -- una prueba de aceptacion por requisito
```

## Como ejecutar las pruebas

```
.venv/bin/python -m pytest 03-motor/backtester/tests -v
```

Sabotaje de camino unico (R-06c) en solitario:

```
.venv/bin/python -m pytest -q 03-motor/backtester -k camino_unico -s
```

## Convenciones que este motor da por sentadas

Todas las de la especificacion (C-1 a C-8, R-01 a R-16); ver el documento para el detalle. Resumen
de las que mas moldean el codigo:

- **Todo el dinero se mueve en `decimal.Decimal`**, nunca en `float` (R-05: los tres casos a lapiz
  piden la caja final exacta al centimo, sin tolerancia).
- **Ninguna cifra de mercado esta cableada en un `.py`** (C-8): spread, comision y swaps viven en
  `config_datos/*.json`, versionado en git.
- **Un unico camino de ejecucion para largo y corto** (R-06): `resolver_fill_stop` y
  `calcular_apuntes_swap` toman la direccion como parametro, no hay una rama duplicada por
  direccion en otro sitio.
- **Sin mirada al futuro** (C-4/R-14): la estrategia solo ve velas cerradas hasta `t`; su orden se
  ejecuta en la apertura de `t+1`.

## Decisiones de diseño declaradas (no vienen de un caso a lapiz)

`motor._nivel_stop_desde_distancia` fija el nivel de stop de un CORTO por simetria con el LARGO
(que si esta fijado sin ambiguedad por CL-1/CL-2/CL-2b): `nivel = open_bid_entrada + distancia +
spread`. Ningun caso a lapiz de la especificacion ejercita un corto abierto por distancia (los
tres son largos; R-02(e) da el nivel de un corto directamente, nunca derivado de una distancia),
asi que esta convencion queda documentada en el codigo en vez de adivinada en silencio (regla 6 de
CLAUDE.md). No afecta a ninguna de las 16 pruebas de aceptacion: R-02(e) y R-03(b) prueban la
mecanica de corto con el nivel/las fechas dados directamente, sin pasar por esta formula.
