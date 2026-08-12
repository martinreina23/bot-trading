# AUDITORÍA DE PESO MUERTO — las reglas de `CLAUDE.md`, una por una

**Fecha:** 12/08/2026. **Ejecuta:** la regla 24 de `CLAUDE.md`, que exige revisar cada mes
si toda restricción sigue teniendo un incidente vivo detrás. Nunca se había ejecutado.

**Ninguna regla se ha borrado ni tocado.** Esto es el análisis; decide el CEO.

---

## Aviso previo: son 30 reglas, no 29

El encargo pedía una tabla de 29 filas. `CLAUDE.md` tiene **30** reglas desde el commit
`89cdf08` (10/08/2026), que añadió la 30 al firmarse D-34. La tabla tiene **30 filas**:
dejar una regla fuera para cuadrar con una cifra vieja sería justo lo contrario de auditar.

```
$ grep -oE '^[0-9]+\.' CLAUDE.md | tr -d '.' | sort -n | tr '\n' ' '
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
```

## Cómo se ha rellenado cada columna

- **Incidente:** buscado por `grep` en `LECCIONES.md`, `DECISIONES.md`, `WBS.md` y en la
  auditoría del proyecto anterior `01-investigacion/herencia-gb2/INFORME_GB2.md`, cuyo
  apartado *«LOS DIEZ ERRORES A NO REPETIR»* (E1–E10) es el origen declarado de las reglas.
  Donde no aparece ninguno, pone **«sin incidente localizado»**. No se ha inventado ninguno,
  ni se ha razonado por qué la regla es buena idea: eso no es un incidente.
- **Muro:** verificado **por ejecución**, no leyendo `CLAUDE.md`. Se montó un repositorio
  git aislado con los hooks reales y se inyectó cada caso prohibido. La sección *«Qué tiene
  muro mecánico y qué es solo prosa»* de `CLAUDE.md` se usó como punto de partida y **está
  desfasada** (ver abajo).

### Lo que dio la prueba de muros, ejecutada hoy en repositorio aislado

| Caso inyectado | Resultado |
|---|---|
| Commit sin código WBS en el mensaje | **BLOQUEADO** |
| Commitear `02-datos/bruto/precios.csv` | **BLOQUEADO** |
| Commitear `02-datos/reservado/x.csv` | **BLOQUEADO** |
| Borrar líneas de `DECISIONES.md` con `git commit` | **BLOQUEADO** |
| Fila de tarea del WBS con 6 campos en vez de 7 | **BLOQUEADO** |
| Citar `motor.py:412` dentro de un `.md` | **PASA — solo imprime AVISO** |
| Borrar líneas por fontanería (`add` + `write-tree` + `commit-tree` + `update-ref`) | **PASA — el borrado aterriza en HEAD** |

**Dos correcciones a `CLAUDE.md` que salen de aquí:**

1. **La regla 13 sí tiene código en `.githooks/pre-commit`, y `CLAUDE.md` no lo menciona.**
   Pero ese código **imprime `AVISO` y no pone `fallo=1`**, así que el commit pasa. Es un
   guardia a medio hacer: ni está en la lista de muros, ni bloquea. Verificado ejecutando
   el hook a mano: salida **0** con la infracción presente.
2. **El hueco de fontanería de la regla 21 está bien declarado en `CLAUDE.md`** y se ha
   reproducido hoy otra vez. Sigue abierto.

---

## La tabla

| # | Qué dice (media línea) | ¿Qué incidente concreto la originó? | ¿Citado en el repo? | ¿Muro mecánico? | Veredicto |
|---|---|---|---|---|---|
| 1 | Toda tarea se anuncia por su código WBS; prohibidos los identificadores opacos | Un mensaje sin código WBS llegó por el canal de órdenes intentando cerrar el incidente del borrado de `INSTALAR.md`, y `critico-codigo` lo rechazó por eso (02/08/2026). Antes, en gb2, los registros de estado no cuadraban entre sí durante 2 días | SÍ — `LECCIONES.md` L-021; `INFORME_GB2.md` §4.5 | **SÍ, bloquea.** `.githooks/commit-msg`. Probado hoy | `MANTENER` |
| 2 | No se inventan tareas: trabajo nuevo entra primero al WBS con código y motivo | En gb2 el motor se comió el propósito: 36 de 51 tareas y el 58% de 328 commits fueron motor/gestión. Y **sigue vivo hoy**: 17 tareas del WBS nacieron a mitad de camino, 13 de ellas de motor | SÍ — `INFORME_GB2.md` E1; `LECCIONES.md` L-011; medido hoy sobre `WBS.md` | NO | `MANTENER` |
| 3 | Los códigos son estables: una tarea empezada no se renumera jamás | **Sin incidente localizado.** `grep -riE 'renumer'` sobre todo el repositorio solo devuelve el texto de la propia regla | NO | NO | `CANDIDATA A RETIRAR` |
| 4 | Se va en orden salvo las paralelas; una tarea no se cierra sin cumplir su criterio de hecho | La mitad del criterio de hecho sí: en gb2, cada ronda de reparación metía un defecto nuevo y tres tareas murieron por agotar rondas. La mitad del «se va en orden» **no tiene incidente localizado** | SÍ (a medias) — `INFORME_GB2.md` E4 | NO | `MANTENER` |
| 5 | La ficha se escribe en la cola ANTES de trabajar la tarea | La tarea `01.01.02` era una fila de una línea sin alcance, y el trabajo se autoasignó alcance dentro de ella (01/08/2026). En gb2, las tareas de orden directa solo se fichaban al cerrar (T-058) | SÍ — `LECCIONES.md` L-013; `INFORME_GB2.md` E9 | NO | `MANTENER` |
| 6 | Regla de no-ambigüedad: si tienes que suponer algo, devuelve la tarea; no supongas | Se le exigió a un agente una comprobación que sus herramientas no podían hacer y **la declaró igual**; y un reparto añadió filtros que la ficha no tenía, con lo que el ejecutor eliminó opciones por el CEO sin saberlo | SÍ — `LECCIONES.md` L-036, L-039 | NO | `MANTENER` |
| 7 | Cada tirada cierra al menos una tarea de PRODUCTO; la infraestructura es deuda | El error nº 1 de gb2: 70% del esfuerzo en fontanería y **1 de 13 hipótesis probada** en 7 semanas. Vivo hoy: el motor es el 45,9% de las tareas y el 62,4% del texto del WBS | SÍ — `INFORME_GB2.md` E1; `LECCIONES.md` L-011 | NO — el contador de `03.01.18` lo **mide**, no lo bloquea | `MANTENER` |
| 8 | Techo del 20% del esfuerzo semanal para motor y orden | Mismo incidente que la 7. Suspendida por D-17 el 03/08 hasta cerrar el bloque de motor | SÍ — `DECISIONES.md` D-1, D-17 | NO | `MANTENER` |
| 9 | Jerarquía de la prueba: ejecución > verificación documental > contraste entre agentes | En gb2 hubo tres diagnósticos consecutivos del mismo componente y dos eran falsos; lo que los corrigió fue leer el código y reproducir el fallo | SÍ — `LECCIONES.md` L-012; `DECISIONES.md` D-7; `INFORME_GB2.md` E7 | NO | `MANTENER` |
| 10 | Quien discrepa aporta el experimento que zanjaría la discusión, no otro argumento | **Sin incidente localizado.** Solo aparece en `CLAUDE.md` y en dos documentos que copian el texto de `CLAUDE.md`. Ningún incidente propio: es el corolario operativo del nivel 1 de la regla 9 | NO (citas, no incidente) | NO | `FUSIONAR CON 9` |
| 11 | Un fallo reportado por un agente no es un fallo verificado: reprodúcelo antes | En gb2 se culpó al escritor del registro sin leerlo (estaba bien) y se eligió entre dos scripts leyendo solo sus cabeceras, concluyendo lo contrario de la verdad | SÍ — `INFORME_GB2.md` E7; `LECCIONES.md` L-012 | NO | `MANTENER` |
| 12 | Ninguna cita a una decisión entra en código o informe sin un `grep` previo | En gb2 se citó una decisión inventada en **9 sitios del código de producción**, 4 apariciones distintas. Aquí: L-017 citó mal su propia regla, y L-041 registró que el mensaje de reparto no es el registro | SÍ — `INFORME_GB2.md` E5; `LECCIONES.md` L-017, L-041 | NO | `MANTENER` |
| 13 | Se referencia por nombre de símbolo, nunca por número de línea | En gb2 la documentación citaba código por número de línea y cualquier commit lo desplazaba | SÍ — `INFORME_GB2.md` E10 | **A MEDIAS.** Hay código en `.githooks/pre-commit`, pero imprime `AVISO` sin poner `fallo=1`: **el commit pasa**. Probado hoy. Y `CLAUDE.md` ni lo menciona | `MANTENER` |
| 14 | Todo dato numérico se calcula sobre datos brutos | Se perdió tiempo buscando un dato que había que calcular; y el orquestador presentó tres estimaciones como si fueran mediciones | SÍ — `LECCIONES.md` L-001, L-020 | NO | `MANTENER` |
| 15 | Quien implementa ejecuta y lee su artefacto completo antes de entregar | El error nº 4 de gb2: cada ronda de reparación metía un defecto nuevo (T-065: 12 defectos, 7 nacidos de reparaciones). Aquí: L-030, el resumen decía más que la tabla de la que salía | SÍ — `INFORME_GB2.md` E4; `LECCIONES.md` L-030, L-041 | NO | `MANTENER` |
| 16 | Nadie valida su propio trabajo; quien produce las métricas no firma el veredicto | Un agente midió su propio artefacto y llamó a eso el suelo del formato (L-022). Y una cifra de verificación **fabricada** por un agente sin la herramienta para producirla, en el registro de `03.01.24` | SÍ — `LECCIONES.md` L-022; `DECISIONES.md` D-29, D-34 | NO — el registro de autoría era `03.01.19`, hoy congelada en `DEUDA-MOTOR.md` | `MANTENER` |
| 17 | Éxito = código fiel a la especificación, NO estrategia rentable | **Sin incidente localizado.** La fase 04 no ha empezado: no se ha probado ninguna estrategia todavía, así que el fallo que previene no ha tenido ocasión de ocurrir | NO | NO | `NO SÉ` |
| 18 | Test de compuerta: si el cambio no se sostiene sin citar métricas de resultado, se deniega | **Sin incidente localizado.** Igual que la 17: protege la fase 04, que no ha empezado. Sí está cableada en `/decision` y en la ficha del `validador` | NO | NO | `NO SÉ` |
| 19 | Pre-registro: ninguna variante se prueba sin registrarse antes (máx. 5-7 por hipótesis) | **Sin incidente localizado.** Hay una aplicación (el criterio pre-registrado de `auditoria_07.01.03_d_procedencia_motor.md`), pero eso es un uso, no el incidente que la originó | NO | NO | `NO SÉ` |
| 20 | Se guardan TODAS las pruebas, también las fallidas | **Sin incidente localizado.** Y `04-resultados/registro-pruebas.md` tiene **11 líneas y 513 bytes**, sin tocar desde el 30/07: la regla nunca se ha ejercido porque no hay pruebas de estrategia que guardar | NO | NO | `NO SÉ` |
| 21 | `registro-pruebas.md` y `DECISIONES.md` solo admiten añadir; corregir es una entrada nueva | Se usa constantemente: D-23, D-24, D-26 y D-28 son correcciones de hecho escritas como entradas nuevas en vez de reescribir las anteriores. Y L-029: «añadir al final» y «sustituir» no se distinguen mirando | SÍ — `DECISIONES.md` D-22 a D-28; `LECCIONES.md` L-017, L-029 | **SÍ, bloquea** en `git commit`. **NO cubre** la vía de fontanería: reproducido hoy, el borrado aterriza en HEAD | `MANTENER` |
| 22 | El cajón `02-datos/reservado/` no se abre; solo el CEO autoriza, una vez por variante | Adoptado de gb2 como práctica que **sí funcionaba** (A4: cuarentena con firma humana insustituible) y fijado en D-10. Con un agujero medido: el patrón `Bash(* 02-datos/reservado*)` exige un espacio literal y una línea de python lo esquiva | SÍ — `DECISIONES.md` D-10, D-29(a); `HERENCIA_GB2.md` A4 | **SÍ, bloquea** en git (probado hoy) y en `settings.json`, **con el agujero de D-29(a) sin tapar** | `MANTENER` |
| 23 | Dos niveles: lo reversible con permisos amplios, lo irreversible con barrera desde el minuto uno | En gb2 se anunció una capa de aislamiento del sistema que **nunca existió** en su entorno, y nadie lo comprobó en meses. Aquí, D-27: esta máquina corre en `bypassPermissions` y ninguna sesión pide permiso | SÍ — `INFORME_GB2.md` E2; `DECISIONES.md` D-20, D-27 | PARCIAL — la lista `deny` de `.claude/settings.json`, que D-27 verificó que sigue mordiendo bajo bypass | `MANTENER` |
| 24 | Una restricción solo se añade tras un incidente real, y se revisa cada mes | En gb2 había restricciones relajadas y otras descubiertas como inexistentes (§6.5). **Este documento es la primera ejecución de esta regla, con un mes de retraso** | SÍ — `INFORME_GB2.md` §6.5; `DECISIONES.md` D-29 | NO | `MANTENER` |
| 25 | Toda barrera se verifica por ejecución, inyectando el caso prohibido | Los errores 2 y 3 de gb2: guardias verificados por presencia, uno estructuralmente muerto y otro cableado al evento equivocado. Y L-009 aquí | SÍ — `INFORME_GB2.md` E2, E3; `LECCIONES.md` L-009 | NO es un muro, pero `prueba_inyeccion.sh` y `/verificar` la ejercen. Hoy: **7 de 7 casos cazados** | `MANTENER` |
| 26 | Los guardias bloquean por defecto; la exención la impone el sistema, no el vigilado | En gb2 se reescribió un guardia perdiendo el «bloquea salvo lo permitido», y hubo exenciones que el propio agente activaba escribiendo una palabra en el mensaje. Aquí, L-028: rodear el límite de herramienta de un agente | SÍ — `INFORME_GB2.md` E6; `LECCIONES.md` L-028 | SÍ — `.githooks/pre-commit` lo declara en su cabecera y lo cumple: si la métrica del WBS no se puede leer, bloquea | `MANTENER` |
| 27 | Los datos nunca entran en git; se descargan con script | En gb2 había **50.089 ficheros de datos versionados contra su propio `.gitignore`**, 1,4 GB en cada clon | SÍ — `HERENCIA_GB2.md` §3; `DECISIONES.md` D-9 | **SÍ, bloquea.** `.githooks/pre-commit` + `.gitignore`. Probado hoy | `MANTENER` |
| 28 | Una sola fuente de verdad por tema; lo que se sustituye, se borra | El error nº 8 de gb2: el estado repartido en cinco registros que no cuadraban, con 2 días de desfase. Aquí: `CLAUDE.md` y el WBS llegaron a tener **dos listas distintas de «29 reglas»** con la misma numeración | SÍ — `INFORME_GB2.md` E8; `LECCIONES.md` L-015; `DECISIONES.md` D-16 | NO | `MANTENER` |
| 29 | Cada agente lleva el identificador exacto de su modelo, nunca un alias | En gb2, tres agentes **nunca se activaron** y había un agente fantasma nombrado en la documentación sin fichero detrás. Aquí, L-010: los agentes no se activan por tener buena descripción | SÍ — `INFORME_GB2.md` §3; `HERENCIA_GB2.md` §3; `LECCIONES.md` L-010; `DECISIONES.md` D-8 | NO | `MANTENER` |
| 30 | Ningún criterio de hecho exige una herramienta que el ejecutor no tiene | Un agente al que se le pidió una verificación imposible **fabricó la cifra**, y el fallo se le imputó a él en vez de a quien repartió (registro de `03.01.24`, 09/08) | SÍ — `LECCIONES.md` L-036; `DECISIONES.md` D-34 | NO | `MANTENER` |

### Recuento

| Veredicto | Cuántas | Cuáles |
|---|---|---|
| `MANTENER` | **24** | 1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 |
| `NO SÉ` | **4** | 17, 18, 19, 20 |
| `CANDIDATA A RETIRAR` | **1** | 3 |
| `FUSIONAR CON 9` | **1** | 10 |

**El titular, y no es el que se esperaba:** las reglas **no son peso muerto**. 24 de 30
tienen detrás un incidente concreto, con fichero y fecha, y casi todos siguen siendo
posibles hoy. Las 4 marcadas `NO SÉ` no son malas reglas: protegen la fase 04, que aún no
ha empezado, así que la prueba de la regla 24 —«¿tiene un incidente vivo detrás?»— no se
les puede aplicar todavía sin retirarlas justo antes de que hagan falta.

**El peso muerto de este proyecto no está en las reglas. Está en el WBS, en la deuda de
motor y en el número de veces que se llama al orquestador.** Eso lo atacan los bloques 1,
3 y 5 de esta cirugía, no esta auditoría.

---

## FICHA DE DECISIÓN PARA EL CEO

> Preparada, **no firmada**. No se ha escrito nada en `DECISIONES.md`.

**QUÉ SE DECIDE:** qué hacer con las 6 reglas de `CLAUDE.md` que no tienen un incidente
detrás (la 3, la 10 y las cuatro de estrategia: 17, 18, 19 y 20).

**OPCIONES**

- **A) Retirar solo la 3, fusionar la 10 con la 9, y dejar las cuatro de estrategia.**
  Quedan 28 reglas.
- **B) No tocar nada.** Se anota la revisión hecha y se repite el 01/09.
- **C) Retirar las seis.** Quedan 24 reglas.

**RECOMENDADA: A.** La 3 no tiene incidente en ningún sitio, ni aquí ni en el proyecto
anterior. La 10 no dice nada que no diga ya la 9. Y las cuatro de estrategia protegen la
fase de probar estrategias, que empieza ahora: retirarlas por no tener incidente sería
quitar el airbag por no haber chocado todavía.

**QUÉ PASA CON CADA UNA**

- **A:** dos reglas menos que leer en cada arranque, y ninguna protección perdida.
- **B:** todo sigue igual; la revisión mensual queda hecha y anotada.
- **C:** se entra en la fase 04 sin pre-registro de variantes ni test de compuerta. Es lo
  que hizo fracasar el proyecto anterior por otra vía.

**QUÉ SE BLOQUEA MIENTRAS NO RESPONDA:** nada. El trabajo sigue con las 30 reglas vigentes.

**RESPUESTA: A, B o C.**
