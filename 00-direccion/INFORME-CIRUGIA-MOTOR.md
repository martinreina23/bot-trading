# INFORME DE LA CIRUGÍA DEL MOTOR — 12/08/2026

## 1. Una pantalla: qué ha cambiado

| Medida | ANTES | DESPUÉS | Diferencia |
|---|---|---|---|
| Bytes de lectura obligatoria del orquestador | 275.301 | 156.773 | **−118.528 (−43,1%)** |
| Tareas vivas en el WBS | 67 | 62 | −5 (congeladas, no borradas) |
| Tareas pendientes de motor en el WBS | 17 | 11 | −6 (5 congeladas + 1 hecha) |
| Reparto motor (% de tareas) | 45,9% | 41,1% | −4,8 puntos |
| Reparto motor (% de texto) | 62,4% | 45,0% | −17,4 puntos |
| Tamaño de WBS.md | 168.317 b | 49.039 b | **−119.278 (−70,9%)** |
| Celda más grande del WBS | 10.471 car. | 1.063 car. | **−9.408 (−89,8%)** |
| Límites de vueltas distintos en el sistema | 3 valores, en 5 sitios | **1 valor, «2»** | −2 valores |
| Pruebas de verificar_excel.py que pasan | 4 de 12 | **12 de 12** | +8 |

**Dos avisos para que estas cifras no se lean mejor de lo que son:**

1. **El motor no ha bajado porque se haya hecho menos motor.** Ha bajado porque 5 tareas están
   congeladas y porque el relato de las tareas se mudó a otro fichero. El reparto de esfuerzo
   real, medido sobre commits, es del **58,9%** — casi el triple del techo del 20%. Esa es la
   cifra que hay que mirar el lunes.
2. **El encargo acertaba en que eran tres cifras distintas** («sin límite», 2 y 3), pero
   señalaba cuatro sitios y había **cinco**: se le escapaba la línea 79 del propio WBS, que el
   revisor cazó y se reparó. Aparte de esas cinco, se corrigió una sexta frase de la misma
   familia —la descripción del orquestador decía «Invocar SIEMPRE… cada vez que vuelva un
   resultado»—, que no es un límite de vueltas sino cuántas veces se le llama.

## 2. Bloque por bloque: qué se hizo y qué no

| Bloque | Estado | Qué se hizo | Qué NO se pudo hacer y por qué |
|---|---|---|---|
| 0 Medir antes | HECHO | Medición completa en `MEDICION-CIRUGIA.md`. Árbol limpio antes de operar | — |
| 1 Congelar deuda de motor | HECHO | 5 tareas movidas íntegras a `DEUDA-MOTOR.md` | 3 de las 8 del encargo no se movieron, con motivo comprobado. Ver abajo |
| 2 Auditoría de peso muerto | HECHO | `AUDITORIA-PESO-MUERTO.md`: 30 filas, muros verificados por ejecución, ficha de decisión preparada | — |
| 3 Borrar pasos del flujo | HECHO | Orquestador 1 vez por tarea, límite único de 2 vueltas, recibo de 12 líneas en las 8 fichas | — |
| 4 Contador y regla 8 | HECHO | Contador montado como hook `SessionStart`; reproduce 43,8% exacto; regla 8 reactivada | — |
| 5 Partir el WBS | HECHO | 25 celdas movidas íntegras a `00-direccion/expedientes/`; los dos scripts del Excel las leen | — |
| 6 Revisión independiente | HECHO | `critico-codigo`, 1 pasada, 13 comprobaciones + 1 extra. Encontró 2 huecos reales | — |

**Las 3 tareas del bloque 1 que no se movieron, y por qué:**

- **`03.01.15`** — el encargo la daba por pendiente y estaba **hecha**. Solo se mueve lo pendiente.
- **`03.01.18`** — el propio encargo la excluía: es el contador, y se ejecutó.
- **`03.01.14`** — **`03.01.16` la lleva en su campo «Depende de»**, y `03.01.16` se queda. Sacarla
  habría dejado una dependencia apuntando al vacío, y el verificador del Excel marca eso como
  fallo. Habría roto la vista del CEO para ahorrar una fila.

## 3. Lo que decide el CEO

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

## 4. Veredicto del crítico

Revisó `critico-codigo`, una sola pasada. Informe completo en
`04-resultados/veredictos/revision_cirugia_motor.md`. **Ninguna de las 13 salió NO.**

| # | Comprobación | Veredicto | Prueba |
|---|---|---|---|
| 9 | ¿Se alteró el texto de alguna regla? *(lo comprobó primero, por orden)* | **NO — correcto** | Comparó las 30 reglas línea a línea contra `89cdf08`: ninguna diferencia |
| 1 | ¿Existe `DEUDA-MOTOR.md` con las filas íntegras? | **SÍ** | `diff` de las 5 filas contra `89cdf08`: `IDENTICAL` las 5 veces |
| 2 | ¿Alguna tarea viva depende de una movida? | **NO** | Parseó el campo «Depende de» de las 62 filas buscando los 5 códigos: salida vacía |
| 3 | ¿Se movió alguna que no fuera `pendiente`? | **NO** | Las 5 tenían una única marca, `pendiente`, en `89cdf08` |
| 4 | ¿30 filas y ningún veredicto inventado? | **SÍ** | 30 filas; 24 MANTENER, 4 NO SÉ, 1 CANDIDATA, 1 FUSIONAR; nada fuera de vocabulario |
| 5 | ¿Algún MANTENER con incidente falso? | **NO** | Comprobó al azar las reglas 1, 8 y 27: L-021, D-17, D-1 y D-9 existen y dicen lo que la tabla dice |
| 6 | ¿El grep de vueltas da 2 en todas partes? | **SÍ** | Da 2 líneas, ambas «2». Amplió el barrido y encontró un «3» suelto en el WBS *(reparado, ver §5)* |
| 7 | ¿Las 8 fichas con el bloque y CANTIDADES? | **SÍ** | 8 de 8, una aparición del encabezado y dos de `CANTIDADES` en cada una |
| 8 | ¿`autonomo.md` y el diagrama dicen lo mismo? | **SÍ** | Coinciden en 2 vueltas y en 2 invocaciones del orquestador |
| 10 | ¿Se tocó zona prohibida? | **NO** | `git diff --name-only 89cdf08..HEAD` filtrado por las 5 rutas: sin salida |
| 11 | ¿El contador reproduce 43,8%, con su propio código? | **SÍ** | Escribió su propio clasificador y obtuvo 7 motor / 9 producto = **43,8%** |
| 12 | ¿Las pruebas dan igual o mejor? | **SÍ** | `verificar_excel.py` 10 fallos → 0. `prueba_inyeccion.sh` 7 de 7 y salida 1 → 0 |
| 13 | ¿Se creó alguna tarea nueva? | **NO** | 67 códigos antes, 62 + 5 después. Ni uno nuevo, ni uno perdido |
| extra | ¿Las 25 celdas movidas están íntegras? | **SÍ, las 25** | 24 coinciden byte a byte con `89cdf08`. La 25ª (`03.01.18`) difiere porque **esa tarea se ejecutó durante la cirugía**; comparada contra el commit correcto, coincide byte a byte |

**El crítico corrigió también a quien le encargó la revisión**, y tenía razón: se le dijo que
en el ANTES eran «6 de 7 casos cazados», y el documento de medición dice 7 de 7. Lo verificó en
vez de repetirlo. Esa misma cifra equivocada se coló en el mensaje del commit `28c20da`, que
dice «6 de 7 → 7 de 7». **Lo correcto es: en el ANTES salían 7 CAZADO, pero uno de ellos era un
aprobado falso** (el caso 3 inyectaba una tarea que ya existía). Hoy los 7 son 7 de verdad.

## 5. Huecos declarados

El crítico encontró dos. **Uno se reparó en la ronda única de reparación; el otro era este
informe.**

1. **`WBS.md` línea 79 seguía diciendo «3 vueltas del bucle de hipótesis».** Era la misma frase
   que se corrigió en `CLAUDE.md`, duplicada en el WBS, y el barrido del encargo no la
   alcanzaba porque solo miraba `CLAUDE.md` y `.claude/`. **REPARADO.** Barrido posterior sobre
   todo el repositorio: no queda ningún «3 vueltas» ni «sin límite» vivo.
2. **La sección DESPUÉS de `MEDICION-CIRUGIA.md` estaba vacía.** Correcto en el momento en que
   lo dijo: se rellena en este bloque 7. **HECHO.**

**Hueco que queda abierto y no se tocó:** los 9 avisos de entregables de `verificar_excel.py`
—ficheros que algunas tareas dicen haber entregado y no están en el repositorio—. Eran 3 antes
y son 9 ahora, **no porque haya más ficheros perdidos, sino porque la prueba ahora también lee
los expedientes y ve nombres que antes no miraba**. Repararlos es la tarea `03.01.17`, que ya
existe en el WBS y no se ejecutó aquí.

## 6. Lo que vi y NO toqué

Frases, no tareas. Ninguna de éstas se ha encolado.

1. **El registro de solo-añadir sigue teniendo la puerta de atrás abierta.** Se reprodujo hoy:
   con `add` + `write-tree` + `commit-tree` + `update-ref` se borran líneas de `DECISIONES.md`
   y aterrizan en `HEAD` sin disparar ningún hook y sin usar `--no-verify`.
2. **El aviso de la regla 13 no bloquea nada.** Hay código en `pre-commit` que detecta citas por
   número de línea, imprime `AVISO` y deja pasar el commit. `CLAUDE.md` ni siquiera lo menciona.
   Saltó sobre este mismo trabajo y el commit entró igual.
3. **El agujero del cajón reservado sigue sin tapar.** El patrón `Bash(* 02-datos/reservado*)`
   exige un espacio literal y una línea de python lo esquiva. Está medido desde el 05/08 y el
   parche está escrito y sin aplicar desde entonces.
4. **Esta máquina se aprueba a sí misma todos los permisos** (`bypassPermissions`, D-27). Lo
   único que frena es la lista `deny`, que es exactamente la que tiene el agujero de arriba.
5. **No hay ninguna barrera de gasto, y está demostrado que no puede haberla** con la herramienta
   actual: probado con un tope de un millonésimo de dólar, la llamada se completó entera.
6. **La cola dice que hay 36 tareas vivas y ninguna es de estrategia.** El producto es probar
   hipótesis de trading y no hay ni una sola hipótesis en marcha.
7. **`04-resultados/registro-pruebas.md` tiene 11 líneas y no se toca desde el 30/07.** Cuatro
   reglas del proyecto existen para protegerlo y nunca ha guardado una prueba de estrategia.
8. **Veinticinco de las 62 tareas declaran su estado sin negrita.** Es válido para el verificador,
   que acepta los dos formatos, pero significa que dos convenciones conviven en la única fuente
   de verdad y que cualquiera que escriba un `grep` sobre estados tiene que acordarse de las dos.
9. **`03.01.13` dice haber entregado un fichero llamado `PENDIENTE-…-lista-de-reglas.md`** que no
   existe. La tarea está cerrada como hecha.
10. **Solo 6 de las 36 tareas vivas están en curso; las otras 30 esperan.** Y de esas 6, cuatro
    son de motor o de orden. El cuello de botella no es la falta de tareas.

## 7. Excepciones de proceso de este encargo

Se incumplieron a propósito, y se declaran en vez de disimularse:

1. **No pasó por el `orquestador`** (capa 3 del flujo de D-15). Motivo escrito en el encargo: el
   orquestador lee ~233.000 bytes antes de decidir nada, y eso es justo lo que la cirugía venía a
   arreglar. Invocarlo para arreglarlo era el bucle que se estaba rompiendo.
2. **No hubo ficha previa en el WBS** (regla 5 de `CLAUDE.md`). El encargo del CEO hizo de ficha.
3. **Ejecutó la sesión principal, no un agente.** La regla 16 —nadie valida su propio trabajo— se
   cumplió con la revisión independiente de `critico-codigo` del bloque 6, no se saltó.
4. **Una sola ronda de reparación**, por orden del encargo, en lugar de las dos que permite el
   flujo normal.
5. **Se editaron dos ficheros de `05-vista-ceo/`** (`generar_excel.py` y `prueba_inyeccion.sh`)
   que no estaban en la lista de intocables pero tampoco en la de objetivos. El primero lo
   ordenaba el bloque 5; el segundo salió de encontrar un fixture que aprobaba en falso.

**Nada de esto se ha escrito en `DECISIONES.md`.** Las decisiones las firma el CEO.

## 8. Lo que yo haría a continuación, en tres líneas

Cerrar la puerta de atrás del registro y el agujero del cajón reservado: son los dos únicos
sitios donde el proyecto cree tener muro y no lo tiene, que es exactamente como murió el
proyecto anterior.

Después, no tocar el motor hasta la puerta GM: con el reparto al 58,9% y la regla 8 otra vez
vigente, cualquier tarea de motor que no desbloquee una de producto es deuda, no trabajo.

Y abrir la primera hipótesis de estrategia esta semana, porque el producto de este proyecto es
un bot que gane dinero y a día de hoy no hay ninguna hipótesis en marcha.
