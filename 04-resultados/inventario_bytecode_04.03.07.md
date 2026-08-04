# Inventario del bytecode retirado — tarea 04.03.07 (PASO 0-bis)

Medición propia, hecha ANTES del borrado, el 04/08/2026 (fecha del sistema en el momento de
ejecutar este inventario; ver NOTA DE FECHA en la ficha de `04.03.07` sobre la falta de fiabilidad
de fechas dictadas sin medir).

## Unidad de recuento

**Ficheros regulares** (`find -type f`), uno por línea, contados sobre el árbol de
`03-motor/backtester/` tal y como estaba en disco inmediatamente antes de ejecutar el `rm -rf` del
paso 3. Total de ficheros en todo `03-motor/backtester/`: **16**. De esos, **15** están dentro de
las tres rutas que la ficha ordena borrar (`__pycache__/`, `tests/__pycache__/`, `.pytest_cache/`)
y **1** (`.gitkeep`) queda fuera y no se toca — es el único fichero que debe seguir presente tras el
borrado, criterio comprobado en el paso 5.

## Comando exacto

Listado de rutas (ejecutado desde `/home/server/projects/bot-trading`):
```
find 03-motor/backtester/ -type f \( -path '*/__pycache__/*' -o -path '*/.pytest_cache/*' \) | sort
```

Tamaño por fichero (bytes, `stat -c "%s"`):
```
find 03-motor/backtester/ -type f \( -path '*/__pycache__/*' -o -path '*/.pytest_cache/*' \) | sort | xargs -I{} sh -c 'printf "%s\t" "{}"; stat -c "%s" "{}"; '
```

`sha256` por fichero:
```
find 03-motor/backtester/ -type f \( -path '*/__pycache__/*' -o -path '*/.pytest_cache/*' \) | sort | xargs sha256sum
```

Recuento total del árbol (incluye `.gitkeep`, que no se borra):
```
find 03-motor/backtester/ -type f | wc -l
```
Resultado: **16**.

## Tabla: los 15 ficheros borrados (ruta · tamaño en bytes · sha256)

| Ruta | Tamaño (bytes) | sha256 |
|---|---:|---|
| `03-motor/backtester/.pytest_cache/.gitignore` | 37 | `3ed731b65d06150c138e2dadb0be0697550888a6b47eb8c45ecc9adba8b8e9bd` |
| `03-motor/backtester/.pytest_cache/CACHEDIR.TAG` | 191 | `37dc88ef9a0abeddbe81053a6dd8fdfb13afb613045ea1eb4a5c815a74a3bde4` |
| `03-motor/backtester/.pytest_cache/README.md` | 302 | `73fd6fccdd802c419a6b2d983d6c3173b7da97558ac4b589edec2dfe443db9ad` |
| `03-motor/backtester/.pytest_cache/v/cache/nodeids` | 2581 | `0e3ce9b5656489c1016c6a5f601b11dfdcaee372677e63ea420af3b9c94dbc8c` |
| `03-motor/backtester/__pycache__/__init__.cpython-312.pyc` | 972 | `b40e3b593a1f3591895f86c915042ac3d8c0826574496b586ece26deec3892a7` |
| `03-motor/backtester/__pycache__/costs.cpython-312.pyc` | 9870 | `5259e3b125cc4ad0cbac8428e4670a9af9bc653ad2d44e4b36e1bd96d98717bb` |
| `03-motor/backtester/__pycache__/execution.cpython-312.pyc` | 16351 | `6ad21f44d063402f660bf96ca7dce984f062b591e5d15a30441262b65f587f55` |
| `03-motor/backtester/__pycache__/sizing.cpython-312.pyc` | 4918 | `80be982b1db737bca5aab69d2b6add2b739a4744e4f04a3cae6a036618f21c30` |
| `03-motor/backtester/tests/__pycache__/__init__.cpython-312.pyc` | 168 | `89013fd0e468c6f5dddbeebed0e4b6cafaac25516373c9b3a6c15ebe1695e46e` |
| `03-motor/backtester/tests/__pycache__/test_costs.cpython-312-pytest-9.1.1.pyc` | 22346 | `6579f6d35e5d2c3e9115fc33a0ab371bce5864181e477151e7fbb27c453ce4a8` |
| `03-motor/backtester/tests/__pycache__/test_costs.cpython-312.pyc` | 8640 | `ce362fc5a2608b9185a7f59e31e2cf8ed7f7e029618570be49bb3f74ce7e8a14` |
| `03-motor/backtester/tests/__pycache__/test_execution.cpython-312-pytest-9.1.1.pyc` | 52439 | `e06a53f5a6fe8dd3b6075519b6c7e42a0dc0a80a85c7bfff635db7461a7d4bf0` |
| `03-motor/backtester/tests/__pycache__/test_execution.cpython-312.pyc` | 16954 | `1da4a377942ebf532e05b4962793a44edf522ebb7c6888eac5a93108871231a5` |
| `03-motor/backtester/tests/__pycache__/test_sizing.cpython-312-pytest-9.1.1.pyc` | 24643 | `daa9b72d7b678e121f2f466d69fe0a6a7d0070afa939016f2c1f2c2643b7e277` |
| `03-motor/backtester/tests/__pycache__/test_sizing.cpython-312.pyc` | 7795 | `21e616e5f868e336e501518ac3b08f1b217777a98332bf400202fa5a0c998f70` |

15 filas de datos = 15 ficheros. Suma de tamaños: 168207 bytes (verificado con
`python3 -c "print(sum([37,191,302,2581,972,9870,16351,4918,168,22346,8640,52439,16954,24643,7795]))"`
tras detectar y corregir un error de suma manual antes de entregar).

## Comprobación previa al borrado — patrones de `.gitignore` distintos (L-018, unidad declarada)

```
git check-ignore -v 03-motor/backtester/__pycache__/ 03-motor/backtester/tests/__pycache__/ 03-motor/backtester/.pytest_cache/
```
Resultado:
```
.gitignore:11:__pycache__/	03-motor/backtester/__pycache__/
.gitignore:11:__pycache__/	03-motor/backtester/tests/__pycache__/
.gitignore:13:.pytest_cache/	03-motor/backtester/.pytest_cache/
```
Confirma lo que dice la ficha: `__pycache__/` (línea 11) y `.pytest_cache/` (línea 13) son dos
patrones distintos de `.gitignore`, así que ninguno de los dos tocaba al otro.

## Comprobación de que el original sigue vivo (commit `0c35959`)

```
git show 0c35959 --stat
```
Resultado (extracto relevante):
```
 03-motor/backtester/__init__.py             |  25 ++
 03-motor/backtester/costs.py                | 184 +++++++++++
 03-motor/backtester/execution.py            | 361 ++++++++++++++++++++++
 03-motor/backtester/sizing.py               | 111 +++++++
 03-motor/backtester/tests/__init__.py       |   0
 03-motor/backtester/tests/test_costs.py     | 157 ++++++++++
 03-motor/backtester/tests/test_execution.py | 458 ++++++++++++++++++++++++++++
 03-motor/backtester/tests/test_sizing.py    | 148 +++++++++
 03-motor/backtester/verificar_motor.py      | 381 +++++++++++++++++++++++
 9 files changed, 1825 insertions(+)
```
**9 ficheros, 1.825 líneas** — coincide exactamente con lo exigido en la ficha. El original está
intacto y el borrado de esta tarea procede.

## Borrado ejecutado (paso 3)

Comando ejecutado con rutas relativas al repo (una ruta absoluta con `rm -rf` cae en la regla
`deny` `Bash(rm -rf /*)` de `.claude/settings.json` y se rechaza sin más — comprobado por
ejecución: el primer intento con rutas absolutas fue denegado directamente. El segundo intento,
con las mismas tres rutas en forma relativa, pasó por la confirmación del sistema de permisos, tal
y como anticipaba la ficha, y se ejecutó):
```
rm -rf 03-motor/backtester/__pycache__/ 03-motor/backtester/tests/__pycache__/ 03-motor/backtester/.pytest_cache/
```
No se usó `python3`, `mv` ni ninguna otra vía para rodear la confirmación (prohibido por la ficha
y por L-028 de `LECCIONES.md`).

## Comprobaciones finales (paso 5)

```
find 03-motor/backtester/ -type f
```
Resultado:
```
03-motor/backtester/.gitkeep
```
Solo queda `.gitkeep`, tal y como exige el criterio de hecho.

```
git status --porcelain
```
Resultado — idéntico, línea a línea, al capturado inmediatamente antes de iniciar esta tarea (los
tres directorios borrados nunca estuvieron rastreados por git, así que el borrado no debía
cambiar nada aquí, y no cambió nada):
```
 M .claude/agents/secretario.md
 M .claude/commands/informe.md
 M .gitignore
 M 00-direccion/DECISIONES.md
 M 00-direccion/LECCIONES.md
 M 00-direccion/WBS.md
 M 04-resultados/registro-cajon.md
 M 05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx
 M 05-vista-ceo/generar_excel.py
 M 05-vista-ceo/prueba_inyeccion.sh
 M 05-vista-ceo/ultimo_estado.json
 M CLAUDE.md
?? 00-direccion/informes/FICHA_D-17.md
?? 00-direccion/informes/ULTIMA_TIRADA.md
?? 01-investigacion/mercados/INFORME_DECISION_G1.md
?? 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
?? 03-motor/scripts/cestas_g1.py
?? 04-resultados/veredictos/auditoria_07.01.03_a_registros_direccion.md
?? 04-resultados/veredictos/auditoria_07.01.03_bc_wbs_y_excel.md
?? 04-resultados/veredictos/auditoria_07.01.03_d_procedencia_motor.md
?? 04-resultados/veredictos/revision_04.03.06.md
?? 04-resultados/veredictos/revision_07.01.03_bc.md
```

## Nota sobre las cifras retiradas

Este inventario no cita «63 símbolos, 19 constantes, 44 pruebas» (retiradas por falsas según la
orden de esta tarea). Las cifras correctas de esa medición previa (64 símbolos, 29 constantes, 39
`nodeids` frente a 44 funciones de prueba del commit) no son objeto de este inventario, que mide
únicamente los ficheros de bytecode y sus tamaños/hashes — se mencionan aquí solo para dejar
constancia de que no se han reutilizado en este documento.

## Cadena de custodia

Este fichero lo persiste `constructor-motor` (tiene `Write` en su ficha), en la ruta exacta que
fija la ficha de `04.03.07`: `04-resultados/inventario_bytecode_04.03.07.md`.
