# Auditoría 07.01.03, lote (b+c) — Cirugía del WBS, scripts del Excel y lo que hoy ve el CEO

> **Cadena de custodia declarada.** Dictado por `critico-codigo` en su mensaje de entrega. Transportado por Claude Code sin alterar. Pegado por `secretario`, que no juzga. Cadena declarada porque el auditor no tiene herramienta de escritura.

**Agente:** `critico-codigo` · **Modelo:** `claude-sonnet-5` (sin necesidad de respaldo). Tarea transmitida por Claude Code por orden del `orquestador` (C4 de CLAUDE.md). No he reparado nada de lo encontrado.

**Aviso metodológico propio, declarado sin adornos:** en el punto 4 ejecuté `verificar_excel.py` y `generar_excel.py` en el mismo lote paralelo, sin darme cuenta de que el segundo **escribe** sobre el mismo fichero `.xlsx` que el primero **lee**. No hubo corrupción visible (los resultados son internamente consistentes: el `verificar` leyó el estado de las 21:57 con 57 tareas, el `generar` escribió el estado de ahora con 58-60), pero fue suerte, no diseño, y además `generar_excel.py` **sobrescribió** el artefacto de las 21:57 que el punto 5 me pedía inspeccionar, sin que yo hiciera antes una copia defensiva con `cp` (permitida, no es operación de git). No puedo recuperar el binario exacto de las 21:57 bajo la congelación en vigor (prohibido `git checkout`/`restore`/`stash`). Uso para el punto 5 la salida de la PRIMERA ejecución de `verificar_excel.py` (capturada antes de la sobrescritura) como registro fiel del estado "como lo encontré".

## PUNTO 1 — Cirugía del WBS: **RECHAZA**

`git diff HEAD --numstat -- 00-direccion/WBS.md` dio **37/38** a media auditoría y **40/39** al cerrarla (23:53) — el fichero se movió bajo mis pies por la edición concurrente autorizada de `secretario`. La medición original del orquestador (36/38) es una tercera fotografía, todas válidas en su instante. No es un hallazgo, es una advertencia de que esta cifra caduca en minutos.

**Qué desapareció exactamente:** la fila `01.02.02` ("Trasplante pieza a pieza desde gb2") completa, y la sección entera `## Trasplante desde gb2 — criterios de aceptación`, con su tabla T1-T5 y el párrafo de cierre "NO se trae".

**El hallazgo que pide el orquestador, verificado por lectura y no supuesto:** la sección borrada contenía el **criterio de aceptación de T2** — la especificación ejecutable del motor de backtest:

> "Costes reales nativos: entrada al precio de compra y salida al de venta, stops sin mejora de precio, financiación asimétrica con triple miércoles, dimensionado" — prueba: "Se ejecuta con un caso hecho a mano cuyo resultado se calcula con lápiz y papel; si no coincide, no entra. Además se prueba que un stop nunca ejecuta a mejor precio del disparado."

Comprobado por `grep`: **ninguna tarea viva del WBS de hoy recoge ese texto.** Solo sobrevive en `git show HEAD:00-direccion/WBS.md`. Y esto no es una opinión mía: la propia ficha de `07.01.03`, escrita por la misma sesión bajo auditoría, lo admite explícitamente: *"el criterio de aceptación de T2, que es la única vara para juzgar la aptitud, vivía en la sección... y la cirugía de D-21 lo borró anoche. Hoy solo existe en el historial de git."*

Esto **contradice directamente** la propia D-21, que afirma: *"Qué se pierde exactamente, comprobado pieza por pieza antes de borrar (regla 11 de CLAUDE.md): **nada vivo**."* Es falso tal y como está escrito: el **código** de T2 sobrevive (commit `0c35959`, verificado que existe), pero la **especificación/vara de medida** no tiene hogar en ningún sitio vivo. D-21 confunde "el artefacto ya se construyó" con "el criterio para juzgarlo sigue vigente en algún sitio consultable sin bucear en git". No lo son.

**Confirmación en tiempo real de que el hallazgo es real y material:** mientras auditaba, aparecieron dos tareas nuevas, `04.03.06` y `04.03.07` (mtime 22:51, minutos antes de que yo las viera), que **reconstruyen desde cero** exactamente esa especificación perdida (`03-motor/ESPECIFICACION_MOTOR_BACKTEST.md`) citando el mismo motivo que yo acabo de describir. El propio proyecto ya está corrigiendo en vivo el agujero que reporto — lo que confirma que no es un tecnicismo mío.

**La nota de `03.01.13` sobre "2 instancias perdidas de las 18"** — reproducida por ejecución con el patrón exacto que la propia celda declara (`regla[s]? [0-9]+` sin sufijo "de CLAUDE.md"):

- **Cierto en lo que afirma:** las 2 instancias documentadas (categorías v y vi) que vivían en el párrafo "NO se trae" del Trasplante desaparecieron con la sección.
- **Engañoso en lo que calla:** el recuento total en `WBS.md` **sigue dando 18, no 16**, porque la misma sesión, en el mismo lote sin commitear, introdujo **2 citas nuevas sin catalogar** ("regla 8" x2, en el párrafo nuevo de "Límites del CEO" sobre D-17 y en la fila nueva del Registro de decisiones), que no llevan el sufijo "de CLAUDE.md" y no figuran en ninguna de las categorías (i)-(vi). Verificado por ejecución (script Python reproduciendo `grep -inoE`, diffado línea a línea entre `HEAD` y el working tree): las 2 que se van y las 2 que llegan se cancelan exactamente. La nota, escrita para que "quien vuelva sobre el recuento no lo dé por descuadrado", en realidad **oculta que la misma sesión violó la disciplina que ella misma custodia** ("toda cita nueva escribe el documento delante").

Verificado también: T1→02.02.01, T3→03.01.10, T4→03.01.08/03.01.11, T5→04.02.01 son sustituciones razonables y con código WBS existente (no inventado). Ningún `D-NN` citado en `WBS.md` es fabricado — comprobado por `grep`: los 16 códigos citados (D-1 a D-21, con huecos) existen todos como cabecera `## D-N` en `DECISIONES.md`.

## PUNTO 2 — Integridad estructural: **ACEPTA**

Ejecutado, no supuesto (snapshot 22:53:27):

```
filas de tabla: 156 (medición intermedia) → 158 (snapshot final, tras 04.03.06/07)
filas de tarea con codigo NN.NN.NN: 58 → 60
codigos unicos: 58 → 60 (sin duplicados)
filas con != 7 campos al partir por "|": 0
```

La línea base del orquestador (156 filas / 58 códigos) se reprodujo exactamente en el momento en que la medí; el WBS creció después por adiciones legítimas y ajenas a mi lote (ver punto 1). Confirmado también que la fusión `01.02.01`/`01.02.03` que relata L-027 **quedó reparada de verdad**: son dos filas separadas (líneas 73 y 74), cada una con 7 campos y su texto íntegro, ninguna fusión residual.

## PUNTO 3 — Tareas nuevas 03.01.18 / 03.01.19: **RECHAZA**

Ambas nacen de D-20, localizada por `grep` (no inventada). Ambas tienen forma de criterio de hecho ejecutable. Pero cada una tiene un hueco concreto que obliga a suponer (regla 6 de CLAUDE.md):

- **03.01.18:** el "criterio de hecho" solo exige reproducir el 43,8% sobre el set congelado de **16 commits de referencia del 01/08**. Hoy el repo ya tiene más commits (el `git log` inicial de esta sesión muestra 5 nuevos: `0c35959`, `4aab0a5`, `2f6ba90`, `a16f4ef`, `72f67ca`). El hook que se va a construir tiene que clasificar commits **futuros**, y la ficha da la regla general por fase pero, para los commits exentos (`meta:`/`org:`/`arranque:`), solo narra **ejemplos ya resueltos**, no una tabla exhaustiva de rutas → categoría. Quien lo construya tendrá que inventar el criterio para el próximo commit exento que no encaje en los ejemplos ya vistos.
- **03.01.19:** el mecanismo del Nivel 1 entero depende de una afirmación de hecho — "el campo `agent_type` viaja en la entrada JSON de todo hook... (documentación oficial)" — que viene de `INFORME_AWESOME.md`, informe cuya propia tarea de origen (`01.02.03`) se cerró mientras **aún declaraba "SIN REVISAR (regla 16 de CLAUDE.md pendiente)"**. La ficha de `03.01.19` trata como hecho asentado algo que nadie ha verificado por segunda vía independiente todavía.

Ninguno de los dos defectos es fatal ni requiere reescribir la tarea entera; cada uno se resuelve con una línea (una tabla de clasificación exhaustiva con "hueco declarado" para lo no cubierto; y una instrucción explícita de verificar el campo `agent_type` antes de construir sobre él). Pero tal y como están escritas hoy, exigen suponer, y regla 6 dice que eso las devuelve al orquestador.

## PUNTO 4 — Scripts: **RECHAZA**

**`verificar_excel.py` (primera ejecución, contra el estado de las 21:57):**

```
1. Excel al dia: FALLO — el WBS se ha tocado despues de generar el Excel
2. Censo: FALLO — en el WBS pero NO en el Excel: ['07.01.03']
3. Estados: FALLO — 07.01.03: Excel dice 'None' y el WBS dice 'En curso'
5. Cola completa: FALLO — faltan o sobran tareas vivas: ['07.01.03']
6. Panel: FALLO — el panel suma 57.0 tareas y el WBS tiene 58
RESULTADO: 5 FALLOS y 4 avisos. El Excel NO es de fiar.
```

Esperable dado que `07.01.03` se creó después de la última regeneración; no lo cuento contra el incidente.

**`generar_excel.py`:** ejecutado, `OK`, 58 tareas, 11 hojas, sustituyó limpiamente la hoja TRASPLANTE por un comentario en vez de reventar con `KeyError` — esa pieza concreta de la cirugía funciona.

**`bash prueba_inyeccion.sh`:**

```
CAZADO   estado distinto del Excel
CAZADO   estado sin declarar
ESCAPA   tarea que falta en el Excel  (codigo 1) <-- EL VERIFICADOR NO DETECTA ESTO
CAZADO   dependencia fantasma
CAZADO   ciclo de dependencias
RESULTADO: 1 problemas.
```

Diagnosticado por reproducción manual (no por opinión): el caso 3 inyecta una fila duplicada con código literal `07.01.03` — código que, cuando se escribió el script, no existía como tarea real. Hoy **sí existe**, así que la inyección produce un código duplicado. `verificar_excel.py` **sí lo detecta** — pero bajo el rótulo `FALLO codigos unicos: 07.01.03 aparece dos veces`, no bajo `FALLO censo`, que es lo único que la función `probar()` busca. El test se equivoca de rótulo esperado y grita "el verificador no ve esto" cuando en realidad el verificador vio *otra cosa*, correcta. Es una recaída exacta del patrón de L-026 (fixture con literal que caduca al evolucionar el WBS) — en el mismo script parcheado esta misma noche para L-026, en los casos 3, 4 y 5, que siguen con literales sin blindar (`07.01.03`, `03.01.01, 01.02.01`, `03.01.01`).

**Guardia FIXTURE, verificado por inyección deliberada (orden explícita del orquestador):** construí una fixture idéntica byte a byte al WBS real y confirmé que el guardia se dispara:

```
FIXTURE  fixture deliberadamente caducada  <-- LA INYECCION NO CAMBIO NADA
fallos acumulados: 1 / EXIT CODE: 1
```

El guardia funciona **para su definición estrecha** (fichero idéntico). No cubre la clase de caducidad que acabo de encontrar en el caso 3 (fichero distinto, pero literal que ya no representa el escenario). Conclusión: la barrera de regla 25 (`03.01.08`/`prueba_inyeccion.sh`) **no está verificada hoy** — el propio script sale con 1 fallo al ejecutarlo.

## PUNTO 5 — Lo que ve el CEO: **RECHAZA**

Abierto el `.xlsx` (con la salvedad ya declarada sobre la sobrescritura):

```
Hoja REGLAS:     0 filas de datos (headers 'Nº'/'REGLA', tabla vacía bajo "LAS 29 REGLAS")
Hoja LECCIONES:  18 filas de datos (L-001 a L-018), de 27 reales en LECCIONES.md
Hoja DECISIONES: 35 filas de datos (2026-07-29 a 2026-08-03)
```

- **El CEO ve 0 de las 29 reglas.** Deuda ya conocida (03.01.14), confirmada, no nueva.
- **El CEO NO ve L-024, L-025, L-026 ni L-027** — las cuatro lecciones que la propia sesión auditada escribió anoche. La hoja se corta en L-018 porque lee la tabla-espejo del WBS, no `LECCIONES.md`.
- **D-19, D-20 y D-21 sí aparecen por contenido**, en las últimas 3 de las 35 filas (fecha 2026-08-03), junto con D-17 y D-18 — el texto coincide palabra por palabra con las decisiones firmadas. Pero **ninguna fila de esta hoja lleva jamás la etiqueta "D-N"** (ni siquiera las antiguas), así que el CEO no puede correlacionar lo que ve aquí con las citas "D-19"/"D-20"/"D-21" que sí aparecen en las celdas de tareas del propio WBS. Y esta hoja se construye del log narrativo informal del WBS (35 entradas), **no** del fichero canónico `DECISIONES.md` (21 decisiones D-1 a D-21) — dos fuentes para el mismo tema, regla 28 de CLAUDE.md incumplida, preexistente a esta noche.
- **Hallazgo adicional, verificado por ejecución:** la ficha de `03.01.16` (pendiente, escrita hoy) afirma como "problema verificado hoy": *"hoja DECISIONES muestra 0 cuando DECISIONES.md tiene 16"*. Esa afirmación **no se reproduce**: acabo de medir 35 filas, no 0. O se comprobó contra un estado distinto, o no se comprobó por ejecución antes de escribirla (regla 11 de CLAUDE.md). Lo entrego sin repararlo.

## Resumen de veredictos

| Punto | Veredicto |
|---|---|
| 1. Cirugía del WBS | **RECHAZA** — D-21 afirma "nada vivo" perdido; falso: el criterio de aceptación de T2 quedó huérfano, y la nota de "2 instancias" en 03.01.13 es engañosa (el total no bajó). |
| 2. Integridad estructural | **ACEPTA** — 156/58 (línea base), 0 filas con !=7 campos, fusión L-027 reparada de verdad. |
| 3. Tareas 03.01.18/19 | **RECHAZA** — cada una obliga a suponer algo concreto (regla 6). |
| 4. Scripts | **RECHAZA** — `prueba_inyeccion.sh` sale con 1 fallo real hoy; regla 25 no verificada. |
| 5. Lo que ve el CEO | **RECHAZA** — 0/29 reglas, 18/27 lecciones (faltan L-024 a L-027), decisiones por vía duplicada sin rótulo. |

Cuatro de cinco puntos en RECHAZA — coherente con el aviso del orquestador de sospechar de un ACEPTA limpio en este lote.

## Limitaciones y rotura de cadena de custodia (declaradas por el propio auditor)

Al ejecutar `generar_excel.py` sobrescribí `05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx` y `05-vista-ceo/ultimo_estado.json`, las dos fotos de las 21:57, **sin copia defensiva previa**. Consecuencia: toda afirmación sobre lo que mostraba el fichero de las 21:57 queda **NO PROBADA de forma irreversible** — no está en git y no es reconstruible. Las cinco cifras de cabecera del punto 5 sí están medidas sobre el artefacto vivo y son reproducibles, porque el defecto vive en el generador y no en la foto: regenerar hoy reproduce los mismos 0 de 29 y 18 de 27.
