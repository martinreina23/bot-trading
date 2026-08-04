# `03-motor/desatendido/` — encadenador de sesiones sin nadie delante (03.01.23)

**Reducido por orden del CEO (04/08).** Se había crecido con gobernanza que él
nunca pidió (lista verde, topes en dólares, cron, hook de aviso). Lo que quería,
en sus palabras: *"en vez de enlazar tantas tareas seguidas se parará antes para
no consumir tokens y automáticamente abriera otra sesión de claude con la
próxima tarea"*. Eso es lo único que hace este guion ahora.

## Cómo funciona

`controlador.sh` lanza una sesión `claude -p` nueva que ejecuta `/autonomo`
completo — es el orquestador quien decide qué tarea toca, como ya hace hoy. El
controlador no elige nada. Cuando la sesión termina, el controlador comprueba
tres cosas antes de decidir si sigue:

1. El JSON de la propia sesión (`is_error`): si no es exactamente `false`, para.
2. `ESTADO.md`: tiene que existir, no estar vacío, haberse **actualizado en
   esta sesión** (no ser un resto de una anterior) y no pasar de
   `MAX_LINEAS_ESTADO`. Si algo falla, para.
3. `DESENLACE.txt`, un fichero corto que la sesión tiene que dejar escrito:
   línea 1 EXACTAMENTE `CERRADA`/`ESCALADA`/`BLOQUEADA`, línea 2 el código WBS
   de la tarea (formato `NN.NN.NN`). **Cualquier cosa que no encaje —fichero
   ausente, línea 1 con otro valor, línea 2 con un código mal formado— para
   igual.** Falla cerrado, nunca sigue por defecto.

Con las tres cosas en orden: `CERRADA` → se lanza la siguiente sesión;
`ESCALADA`/`BLOQUEADA` → para y deja `PARA-CEO.md`. Más los cortes que ya
había: `timeout`, JSON inválido, bandera de parada, tope de tareas por tirada.

## Ficheros

| Fichero | Quién lo escribe | Qué es |
|---|---|---|
| `controlador.sh` | — | El bucle. |
| `config.env` | El CEO | `MAX_TURNS`, `TIMEOUT_SESION_SEGUNDOS`, `MAX_TAREAS_POR_TIRADA`, `MAX_LINEAS_ESTADO`. Sin dólares: esta máquina no tiene clave de API (corre sobre plan de suscripción, comprobado), así que un tope en dólares no limitaba nada de verdad. |
| `DESENLACE.txt` | Cada sesión, fresco | `CERRADA`/`ESCALADA`/`BLOQUEADA` en la 1ª línea, código WBS en la 2ª. El controlador lo borra antes de lanzar, lo lee después, y **valida las dos líneas** — un código mal formado para la cadena igual que un desenlace inválido. |
| `ESTADO.md` | Cada sesión al terminar | Corto (tope `MAX_LINEAS_ESTADO`): qué tarea trabajó, con qué desenlace, qué queda pendiente, **qué se rechazó y por qué** (si se pierde esto, la siguiente sesión decide peor). La sesión siguiente lo lee antes de empezar. El controlador nunca escribe su contenido, pero sí **comprueba mecánicamente** que existe, no está vacío, se actualizó en esa sesión, y no pasa del tope. |
| `STOP_CEO.flag` | Solo el controlador | Bandera de parada. Nunca se autolimpia; solo `--reanudar-tras-ceo` la quita. |
| `PARA-CEO.md` | La sesión si escala/bloquea; si no, el controlador deja una de repuesto | Ficha en lenguaje llano. |
| `controlador.log` | Solo el controlador | Registro operativo. |

**No están en el repo a propósito** (los crea la ejecución, no se pre-crean):
`DESENLACE.txt`, `ESTADO.md`, `STOP_CEO.flag`, `PARA-CEO.md`, `controlador.log`,
`cadena.lock`.

**Se borraron por orden del CEO, no se comentaron:** `lista-verde.txt` (y toda
su puerta), `cola.txt`, el tope en dólares (`MAX_BUDGET_USD_SESION`,
`MAX_BUDGET_USD_DIARIO`, `gasto-*.tsv`, el marcador de contabilidad incompleta,
`--max-budget-usd`), `--disallowedTools` (protegía ficheros que ya no existen),
`crontab.propuesto.txt`, `hook-notificacion.ejemplo.json`, `progreso.tsv` (la
idempotencia por código WBS ya no tiene sentido: no hay lista fija de códigos
que recorrer, el orquestador decide cada vez).

## Cómo se usa

```
./controlador.sh --simulacro                       # por defecto, no llama a Claude
./controlador.sh --de-verdad                        # real
./controlador.sh --de-verdad --reanudar-tras-ceo     # tras la firma del CEO
```

## Tabla muro/prosa (solo lo que queda)

| Mecanismo | Estado | Prueba |
|---|---|---|
| `flock`, incluido el arreglo del huérfano (`exec 9>&-`) | **MURO** | Ejecución real: `kill -9` al padre con una sesión hija en marcha (CLAUDE_BIN forzado a un doble) → lock libre de inmediato |
| `timeout` con mínimo 60s | **MURO** | Ejecución real: `TIMEOUT_SESION_SEGUNDOS=0` en `config.env` → no arranca (código 2) |
| `config.env`: sin `source`, lista blanca (4 claves), sin duplicados, con mínimos | **MURO** | Ejecución real: clave no permitida, clave duplicada, y cada mínimo en 0 → todos rebotan |
| **`DESENLACE.txt`, línea 2 (código WBS): código mal formado → PARA** | **MURO** (antes prosa: solo se marcaba "no reconocible" y la cadena seguía) | Ejecución real: `CERRADA` + código roto (`ESTO NO ES UN CODIGO WBS`) → para (código 12), no lanza la siguiente |
| Lógica única de `is_error`, rigor al leer el JSON | **MURO** | Ejecución real: JSON vacío/inválido → para (código 6) |
| `DESENLACE.txt` ausente/vacío/valor raro → PARA (falla cerrado) | **MURO** | Ejecución real: sesión que no lo escribe → para (código 12) sin lanzar la siguiente; valor `ALGO_RARO` → mismo resultado |
| **`ESTADO.md`: es un fichero regular, existe, no vacío, actualizado en la sesión, dentro del tope de líneas** | **MURO** (histórico: CERO MURO → MURO CON GRIETA [`stat` sin `-L`, `wc -l` fallaba abierto] → MURO CON GRIETA [`-s` sin `-f`, symlink-a-directorio] → **MURO**) | Ejecución real, 5 ataques: (1) sesión que deja `CERRADA` sin tocar `ESTADO.md` → para (código 14); (2) más líneas que `MAX_LINEAS_ESTADO` → para igual; (3) symlink a un fichero que la sesión SÍ reescribe → **no da falso positivo** (comparado "antes sin `-L`" vs "después"); (4) `wc -l` sin poder leer el fichero → para con mensaje explícito, nunca "0 líneas" falso; (5) symlink a un **directorio** con actividad real dentro (ficheros creados, tamaño > 0) → **para** (código 14), 5 de 5 — antes (sin `-f`) colaba como `CERRADA` las 5 veces, reproducido el contraste exacto |
| `stat -L` (no `-c` a secas) en las dos comprobaciones de fecha (`ESTADO.md`, `PARA-CEO.md`) | **MURO** | Ejecución real: symlink con mtime propio distinto del fichero real → con `-L` se lee el del fichero real, sin `-L` se leería el del enlace (reproducido el fallo con una copia sin `-L`) |
| `wc -l` con resultado no numérico (fichero borrado/ilegible entre el primer chequeo y este) → PARA, nunca "sigue en silencio" | **MURO** | Ejecución real: `ESTADO.md` sin permiso de lectura tras pasar el primer chequeo → `wc -l` falla, el guion lo detecta y para (código 14) con el mensaje exacto del fallo, no con un "0 líneas" falso |
| `-f` (fichero regular) antes de `-s` en `ESTADO.md` y en `DESENLACE.txt` | **MURO** | `ESTADO.md`: ejecución real, symlink a directorio con actividad → para 5/5 (antes colaba 5/5). `DESENLACE.txt`: mismo endurecimiento por consistencia — aquí no había agujero explotable porque la validación de contenido de más abajo (línea 1 tiene que ser EXACTAMENTE `CERRADA`/`ESCALADA`/`BLOQUEADA`) ya rechazaba un directorio (verificado: `sed -n '1p'` sobre un directorio da error y cadena vacía), pero queda protegido igual, sin depender de esa red |
| `ESCALADA`/`BLOQUEADA` → para y deja `PARA-CEO.md` | **MURO** | Ejecución real: ambos valores probados, para (código 42) sin lanzar la siguiente |
| Tope de tareas por tirada → para limpio, sin firma | **MURO** | Ejecución real: tope=2, dos sesiones `CERRADA` → para (código 20), sin `STOP_CEO.flag` ni `PARA-CEO.md`; relanzable sin `--reanudar-tras-ceo` |
| Bandera de parada persiste hasta `--reanudar-tras-ceo` | **MURO** | Ejecución real: relanzar sin el flag → rechazado; con él → retira la bandera y sigue |
| Construcción del comando real (`-p`, `--output-format json`, `--max-turns`, sin `--max-budget-usd` ni `--disallowedTools`) | **MURO** | Ejecución real con `claude` de mentira: argumentos capturados y verificados |
| Comprobación previa de que `CLAUDE_BIN` se puede ejecutar (modo `--de-verdad`) | **MURO** | Ejecución real: `PATH` mínimo + nombre desnudo → código 11 específico |
| Que una sesión real siga fielmente el prompt (lea `ESTADO.md`, escriba `DESENLACE.txt`/`ESTADO.md`/`PARA-CEO.md` como se le pide) | **NO VERIFICADO POR EJECUCIÓN** — cero invocaciones reales de `claude -p` permitidas en ninguna ronda de esta tarea. El prompt se construyó y se verificó con un doble, no con el binario real | — |
| Ejecución real sin supervisión durante horas | **Cero probado**, no forma parte de este encargo | — |

Cero invocaciones reales de `claude -p` en esta ronda (todas con `CLAUDE_BIN`
forzado a un doble, verificado antes de cada lanzamiento). Nada instalado. Sin
commitear.
