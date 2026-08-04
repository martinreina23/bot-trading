# Revisión del veredicto del lote (b+c) — tarea 07.01.03 (03/08/2026)

**Agente:** `validador` (`claude-fable-5`, sin respaldo necesario: el modelo principal respondió).
**Papel:** revisar al auditor (`critico-codigo`), no el incidente. Orden del `orquestador`, de
ejecución y no de lectura. **Método:** regla 9 de CLAUDE.md nivel 1 — toda cifra de este documento
sale de una ejecución hecha por mí el 03/08/2026, o de un `git show`/`grep` con fichero delante;
lo que no, va marcado. **No he reparado nada. Congelación respetada:** cero `git commit`, `checkout`,
`stash`, `restore`; cero paquetes instalados. **No se ha abierto `02-datos/reservado/`.**
Los experimentos se ejecutaron sobre copias en el scratchpad de la sesión; ningún fichero del
proyecto ha cambiado por esta revisión.

**Declaración de procedencia (línea añadida a posteriori por orden del `orquestador`, sin alterar
el resto del texto entregado):** esta revisión se ejecutó sobre el veredicto RELATADO en el
encargo, antes de que el artefacto del auditor existiera en disco; el contraste contra el fichero
pegado (`auditoria_07.01.03_bc_wbs_y_excel.md`) se añade en el addendum del final y declara si
alguna frase cambió por el camino.

---

## VEREDICTO GLOBAL (una línea)

**Los cinco veredictos del auditor se sostienen en lo sustancial: CONFIRMO los cinco.** Le refuto
**una subafirmación del punto 5** («ninguna fila lleva la etiqueta D-N»: cuatro filas sí la llevan)
y le corrijo **el estado presente del punto 4** (hoy la prueba de inyección ya ni siquiera falla
donde él dijo: falla peor). La sobrescritura del `.xlsx` **debilita pero no invalida** el punto 5
(juicio completo al final). El auditor NO rechaza de más: donde rechaza, el defecto se reproduce.

---

## Punto 1 — Cirugía del WBS: **CONFIRMO el RECHAZA**

### 1a. El criterio de T2 existía, D-21 lo borró, y ninguna tarea viva lo recoge

**Texto recuperado de git, no de memoria** — `git show HEAD:00-direccion/WBS.md`, sección
«Trasplante desde gb2 — criterios de aceptación (D6 = B, decidido 30/07/2026)», fila T2 literal:

> | **T2 — Motor de backtest** | Costes reales nativos: entrada al precio de compra y salida al de
> venta, stops sin mejora de precio, financiación asimétrica con triple miércoles, dimensionado |
> Se ejecuta con un caso hecho a mano cuyo resultado se calcula con lápiz y papel; si no coincide,
> no entra. Además se prueba que un stop nunca ejecuta a mejor precio del disparado | Los drivers
> duplicados (`scripts/backtest_f03*.py`): en gb2 la lógica vivía en dos sitios con riesgo de
> divergencia |

**Comprobación de que ninguna tarea viva lo recoge, ejecutada:**

```
$ grep -n "lápiz y papel\|mejora de precio\|triple miércoles" 00-direccion/WBS.md
(cero resultados)
$ ls 03-motor/ESPECIFICACION_MOTOR_BACKTEST.md
No such file or directory
```

La única tarea que hoy lo menciona, `04.03.06` (alta de las 22:51, POSTERIOR a la medición del
auditor), no lo contiene: ordena **recuperarlo del historial de git**, y su artefacto no existe en
disco. En el momento de la medición del auditor ni siquiera existía `04.03.06`.

**D-21 dice, literal** (`00-direccion/DECISIONES.md`, entrada D-21): «Qué se pierde exactamente,
comprobado pieza por pieza antes de borrar (regla 11 de CLAUDE.md): **nada vivo**. […] **T2 (motor
de backtest) ya se construyó desde cero aquí** — commit 0c35959». El propio proyecto desmiente el
«nada vivo» esa misma noche: la ampliación de `07.01.03` llama al criterio de T2 «la única vara
para juzgar la aptitud» y declara que «hoy solo existe en el historial de git», y hubo que crear
`04.03.06` para reescribirlo. Además el motor del commit `0c35959` quedó retirado por la opción B
del CEO, así que «ya se construyó» tampoco salva la frase. El RECHAZA se sostiene.

### 1b. Las «2 instancias de las 18» — recuento reproducido, la nota es engañosa

Reproducido con el patrón declarado en la propia ficha de `03.01.13` (`regla[s]? [0-9]+` sin
distinguir mayúsculas, descartando los aciertos seguidos de « de CLAUDE.md»):

| Fichero | Instancias sin sufijo |
|---|---|
| WBS de HEAD (`git show`) | **18** — cuadra con la pasada 4 documentada |
| WBS actual en disco | **19** |

Descomposición exacta, verificada acierto a acierto:
**18 (documentadas) − 2 (perdidas con la sección Trasplante: la de categoría (v) «antigua regla 26»
y la de categoría (vi) «reglas 5, 7, 11…», ambas en la línea del cierre «NO se trae» de HEAD)
+ 2 (NUEVAS y sin catalogar, escritas el 03/08 por la sesión auditada en los dos textos de D-17:
«La regla 8 no se elimina; se suspende…» en la sección de límites, e «incumpliendo regla 8; se
suspende…» en el log de decisiones; ninguna de las dos existe en HEAD)
+ 1 (nueva en la ficha de `04.03.06`, «reglas 17 y 18 de CLAUDE.md» con sufijo compartido, alta de
las 22:51 del orquestador, POSTERIOR a la medición del auditor) = 19.**

Conclusión: en el momento de medición del auditor el recuento daba **18, no 16**, exactamente por
la cancelación que él describe. **CONFIRMADO.** La nota de `03.01.13` («pierde exactamente 2
instancias de las 18… para que quien vuelva sobre el recuento no lo dé por descuadrado») induce a
esperar 16 y es engañosa tal y como el auditor dice. Anoto además que el catálogo sigue
descomponiéndose: hoy son 19, y la instancia 19ª no es del incidente sino del alta posterior.

---

## Punto 2 — Integridad estructural: **CONFIRMO el ACEPTA**

Medido hoy sobre `00-direccion/WBS.md`:

```
filas que empiezan por "|"      : 158
filas de tarea (código NN.NN.NN): 60
campos por fila de tarea        : 60 filas con exactamente 7 campos, 0 con otra cifra
```

El 156/58 «en su momento de medición» no es re-medible (ese estado no se conservó), pero cuadra
aritméticamente: 158/60 menos las dos únicas altas de las 22:51 (`04.03.06`, `04.03.07`), que el
propio auditor ya re-midió como 158/60.

**Fusión de L-027 reparada sin perder texto, verificado campo a campo contra HEAD:**

```
01.02.01: 5 campos, los 5 IDÉNTICOS a HEAD (341 chars)
01.02.03: 5 campos; 4 idénticos; el campo ESTADO contiene ÍNTEGRO el texto de HEAD
          y añade 989 chars (el cierre legítimo por D-20)
```

Nada que objetar.

---

## Punto 3 — Tareas 03.01.18 y 03.01.19: **CONFIRMO el RECHAZA** (con un matiz)

**03.01.18:** leída la ficha completa (fila `03.01.18` del WBS). Contiene la regla por fases
(«02, 04, 05 y 06 producto; 03 y 07 motor; 01.01.\* producto, 01.02.\* motor») pero para los
commits exentos dice solo «las rutas se usan SOLO para los commits que `.githooks/commit-msg`
exime» — **no existe tabla ruta→categoría en la ficha**. Quien implemente tendrá que inventarse el
mapa, que es exactamente lo que la regla 6 de CLAUDE.md prohíbe. Verificación documental: la tabla
no está. Sostenido.

**03.01.19:** la cadena de procedencia se verifica entera:

```
$ grep -rn "agent_type" 01-investigacion/
INFORME_AWESOME.md:113: campo `agent_type` viaja en la entrada JSON de todo hook
                        cuando corre dentro de un subagente (documentación oficial…)
```

Ese hecho no se ha verificado por ejecución en este proyecto (ningún hook lo ha demostrado aquí), y
la tarea de origen del informe, `01.02.03`, se cerró el 03/08 por D-20 declarando en su propia
celda: «la regla 16 de CLAUDE.md queda incumplida en esta tarea». **Matiz que el auditor no da:**
el hueco de revisión declarado es del `INFORME_AWESOME_2.md` (segunda pasada); el `INFORME_AWESOME.md`
que contiene la afirmación de `agent_type` sí pasó tres rondas de revisión — pero centradas en el
cálculo del 43,8%, no en este hecho técnico. El fondo del rechazo aguanta con la regla 11 de
CLAUDE.md: un hecho reportado y jamás ejecutado aquí, presentado en la ficha como cierto. Sostenido.

---

## Punto 4 — Scripts: **CONFIRMO el RECHAZA**, y el estado real hoy es PEOR que el descrito

**Orden 1 ejecutada — `bash 05-vista-ceo/prueba_inyeccion.sh`, salida de hoy:**

```
PRUEBA DE INYECCION DEL VERIFICADOR
  (inyectando sobre la tarea 01.01.01)
  CAZADO   estado distinto del Excel
  CAZADO   estado sin declarar
  CAZADO   tarea que falta en el Excel
  CAZADO   dependencia fantasma
  CAZADO   ciclo de dependencias
  --
  MAL      el WBS real NO pasa la verificacion: mirala antes de seguir
RESULTADO: 1 problemas.   (exit 1)
```

**NO me sale el mismo fallo en la superficie** (a él: `ESCAPA` en el caso 3; a mí: caso 3 `CAZADO`
y `MAL` en la pasada final). La diferencia se explica y **su diagnóstico se confirma en el fondo**
con esta reproducción controlada: construí yo mismo el `w3.md` del caso 3 (mismo `awk` del script)
y pasé el verificador sobre él con copia del Excel actual:

```
FALLO  codigos unicos: 07.01.03 aparece dos veces en WBS.md      <- la inyección cae AQUÍ
FALLO  censo: en el WBS pero NO en el Excel: ['04.03.06', '04.03.07']  <- esto NO es la inyección
```

Es decir: (a) el literal `07.01.03` del caso 3, que no existía al escribirse el script, hoy es una
tarea real y la inyección produce un **duplicado**, cazado bajo «codigos unicos» y no bajo «censo»,
que es lo único que el `grep` del caso busca — **exactamente lo que el auditor afirmó**; (b) el
`CAZADO` de mi pasada de hoy es un **falso aprobado**: el `grep "FALLO  censo"` engancha el fallo
de censo REAL causado por la deriva WBS/Excel (`04.03.06`/`04.03.07`, altas de las 22:51 no
regeneradas), no la inyección. En el momento de la medición del auditor (Excel recién regenerado a
las 22:44, censo limpio) la misma mecánica da `ESCAPA`, que es lo que él reportó. Coherente.

**Guardia FIXTURE verificado por inyección deliberada, ejecutada por mí** sobre una copia del
script en el scratchpad con el patrón del caso 3 sustituido por uno inexistente (inyección que no
cambia nada):

```
FIXTURE  tarea que falta en el Excel  <-- LA INYECCION NO CAMBIO NADA: el roto es el test, no el verificador
```

Muerde. La declaración del auditor sobre FIXTURE queda **confirmada por ejecución**.

**Literales sin blindar en los casos 3, 4 y 5:** verificación documental sobre el fuente del script
(`awk` con `| 07.01.03 |` literal en el caso 3, `gsub` de `| 03.01.01, 01.02.01 |` en el 4 y de
`| 01.01.01 |` en el 5). L-026, leída hoy, manda «localizar a la víctima por estructura, no por su
prosa»: la recaída es literal, en el mismo script parcheado anoche por L-026. Sostenido.

**Conclusión del punto:** la barrera de la regla 25 de CLAUDE.md **no está verificada hoy** — el
script sale con exit 1, y el único caso que parece pasar (caso 3) pasa por contaminación, no por
mérito del verificador. El RECHAZA se queda corto si acaso; jamás sobrado.

---

## Punto 5 — Lo que ve el CEO: **CONFIRMO el RECHAZA en lo sustancial; REFUTO una subafirmación**

**Orden 2 ejecutada — contado por mí sobre el `.xlsx` real en disco** (el de las 22:44), con
`openpyxl`, no sobre el generador:

| Afirmación del auditor | Medición mía | Veredicto |
|---|---|---|
| El CEO ve 0 de las 29 reglas | hoja REGLAS: **0 filas de datos** (solo cabecera, max_row=3) | **CONFIRMO** |
| Ve 18 de 27 lecciones; no ve L-024–L-027 | hoja LECCIONES: **18 filas, L-001…L-018**; `LECCIONES.md`: **27** (L-001…L-027). No ve L-019–L-027, que incluye L-024–L-027 | **CONFIRMO** |
| Ve el contenido de D-19, D-20, D-21 | filas 36–38 de la hoja DECISIONES llevan los tres contenidos | **CONFIRMO** |
| «Ninguna fila lleva la etiqueta D-N» | **FALSO como absoluto:** las filas 35–38 empiezan su columna Motivo por «**D-18:**», «**D-19:**», «**D-20:**», «**D-21:**». Las 31 restantes, ninguna. No hay columna de identificador | **REFUTO la subafirmación** (el hallazgo de fondo — sin identificador sistemático, 31 de 35 sin etiqueta — queda en pie) |
| La hoja se construye del log del WBS (35) y no de `DECISIONES.md` (21) | log «Registro de decisiones» del WBS: **35 filas**; hoja DECISIONES: **35 filas** con textos idénticos al log; `DECISIONES.md`: **21** entradas (D-1…D-21). Dos fuentes para el mismo tema | **CONFIRMO** |
| Hallazgo extra: el «muestra 0» de la ficha `03.01.16` no se reproduce | hoja actual: **35 filas**. Y el `.xlsx` commiteado en HEAD (pre-incidente, recuperado con `git show`): **30 filas**, tampoco 0. El «Problema verificado hoy … muestra 0» es falso contra los DOS artefactos recuperables | **CONFIRMO y refuerzo** |

La subafirmación refutada no tumba el RECHAZA: 0/29 reglas, 9 lecciones invisibles y la doble
fuente bastan por sí solas. Pero queda anotada: **el auditor afirmó un «ninguna» sin mirar las
filas que él mismo citaba como ejemplo.** Quien rechaza también tiene que medir.

**Nota al margen de la misma medición:** la ficha de `03.01.16` también fija como criterio «29
reglas / 23 lecciones / 16 decisiones», cifras que la propia sesión dejó desfasadas esa misma
noche (hoy son 29 / **27** / **21**). Si esa tarea se ejecuta tal cual está escrita, nacerá mal.

---

## Juicio sobre la sobrescritura del `.xlsx` de las 21:57

El auditor ejecutó `generar_excel.py`, que escribe sobre el MISMO fichero que debía inspeccionar,
sin copia defensiva. El artefacto de las 21:57 —lo único que probaba qué produjo la sesión del
incidente con su propio generador— **no está en git (el commiteado es anterior, de las 15:47 del
tramo previo) y es irrecuperable e irreconstruible con exactitud** (entre las 21:57 y las 22:44 el
WBS ganó al menos las filas de `07.01.03`, `03.01.16` y `03.01.17`, así que regenerar no lo
devuelve).

**Mi juicio: DEBILITA el punto 5, no lo invalida.**

- No lo invalida porque las cinco cifras de cabecera del punto 5 están medidas sobre el artefacto
  vivo —el que el CEO abriría hoy— y yo las he reproducido TODAS de forma independiente sobre ese
  fichero. Ninguna depende del artefacto destruido.
- Lo debilita porque cualquier afirmación del auditor sobre **lo que mostraba el fichero de las
  21:57** ya no puede re-ejecutarse por nadie: por la regla 9 de CLAUDE.md queda degradada a
  **NO PROBADO** para siempre. En particular, si alguien quisiera separar qué parte de la vista
  del CEO rompió la sesión del incidente y qué parte ya venía rota, el término de comparación fino
  se ha perdido (queda solo el commiteado de HEAD, más antiguo).
- Y es un incidente en sí mismo: un auditor que altera la evidencia que inspecciona, dentro de una
  tarea que dice «Nada se commitea hasta ese cierre», ha roto la cadena de custodia aunque lo
  declare. Que lo declarara él solo es lo que separa esto de una falta grave; no lo convierte en
  inocuo. Debe constar en el cierre de 07.01.03 y pesar en si este proyecto necesita copias
  defensivas obligatorias antes de ejecutar generadores sobre artefactos bajo auditoría — con este
  incidente ya real detrás, como exige la regla 24 de CLAUDE.md.

---

## Recuento de esta revisión (regla 20 de CLAUDE.md)

Ejecuciones: 9 (prueba de inyección completa · verificador sobre WBS real · reproducción controlada
del caso 3 · FIXTURE con inyección nula · 2 recuentos de instancias HEAD/actual · volcado y conteo
del xlsx actual · conteo del xlsx de HEAD · comparación campo a campo 01.02.01/01.02.03).
Verificaciones documentales por `git show`/`grep`: 8. Reparaciones: **0**. Ficheros del proyecto
modificados: **1** (este veredicto, que es el entregable ordenado).

---

## ADDENDUM (03/08/2026, tras las 23:12) — cierre sobre el artefacto pegado en disco

**Sobre qué artefacto se cierra finalmente esta revisión:**
`04-resultados/veredictos/auditoria_07.01.03_bc_wbs_y_excel.md` — dictado por `critico-codigo`
(`claude-sonnet-5`, sin respaldo), transportado por Claude Code, pegado por `secretario` sin
juzgarlo, con cadena de custodia declarada en su cabecera. Todo lo anterior a este addendum se
escribió contrastando el veredicto RELATADO en el encargo; el fichero no existía entonces en disco
(el fallo de custodia lo asumió el `orquestador`, no fue de `critico-codigo`, que no tiene
herramienta de escritura). Antes de modificar mi entregable hice **copia defensiva fuera del
repositorio** (norma nueva del `orquestador` nacida esta noche):
`md5 72f1997a458412ec05d23ad75f55e73f`, verificado idéntico antes y después de la espera.

### ¿Coincide el fichero con el relato que juzgué?

**En todas las cifras y en los cinco veredictos, SÍ.** Comparación frase a frase: 156/58→158/60 ·
0 filas ≠7 campos · «sigue dando 18, no 16» · las 2 nuevas «"regla 8" x2» · caso 3 con literal
`07.01.03` · «códigos únicos» y no «censo» · recaída de L-026 en casos 3, 4 y 5 · FIXTURE
verificado y disparado · 0/29 · 18/27 · 35 filas frente a 21 · el «muestra 0» de `03.01.16` que no
se reproduce. Ninguna cifra ni veredicto cambió por el camino. Diferencias de texto encontradas,
con la frase exacta:

1. **El relato endureció una palabra.** El encargo decía que «D-21 **miente**»; el fichero dice
   «Esto **contradice directamente** la propia D-21 […] **Es falso tal y como está escrito**» y
   «D-21 **confunde** "el artefacto ya se construyó" con "el criterio para juzgarlo sigue vigente
   en algún sitio consultable"». El auditor afirma falsedad, no intención de engañar. Mi
   confirmación del punto 1 se apoya en la falsedad, que está probada; queda igual.
2. **El relato omitió dos atenuantes que el fichero sí trae:** en el punto 3, «Ninguno de los dos
   defectos es fatal ni requiere reescribir la tarea entera; cada uno se resuelve con una línea»;
   en el punto 5, que el 0/29 es «Deuda ya conocida (03.01.14), confirmada, no nueva». Ninguno
   cambia el RECHAZA; ambos importan para quien repare.
3. **El relato omitió que la sobrescritura fue doble.** El fichero declara: «sobrescribí
   `05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx` **y `05-vista-ceo/ultimo_estado.json`**, las dos
   fotos de las 21:57». Mi dictamen se extiende sin cambiar: dos fotos perdidas, mismo
   razonamiento.
4. **El fichero trae material que el relato no contaba**, y refuerza en vez de contradecir: el
   `numstat` cambiante (37/38 a media auditoría, 40/39 al cierre; mi foto de ahora: **40/39**,
   coincide con la suya); la «Confirmación en tiempo real» de que `04.03.06`/`04.03.07`
   aparecieron A MITAD de su auditoría reconstruyendo la especificación perdida; la verificación
   de las sustituciones T1/T3/T4/T5 y de que ningún D-NN citado en el WBS es fabricado; y la
   salida de la PRIMERA ejecución de `verificar_excel.py` contra el estado de las 21:57
   (5 FALLOS, censo `['07.01.03']`) — registro del estado «como lo encontré», hoy infalsificable
   y declarado como tal por el propio fichero.

### Corrección de precisión a mi propio texto de arriba, a la luz del fichero

Escribí en el punto 1: «En el momento de la medición del auditor ni siquiera existía `04.03.06`».
El fichero precisa que su 156/58 fue «medición intermedia» y que él SÍ vio aparecer
`04.03.06`/`04.03.07` antes de cerrar (su «Confirmación en tiempo real»). Mi frase vale para la
medición intermedia contra la que contrasté, no para su cierre. No altera ningún veredicto:
`04.03.06` sigue sin CONTENER el criterio de T2, que es lo que ambos medimos por separado.

### ¿Siguen en pie mis veredictos contra el fichero?

| Mi veredicto original | Contra el fichero pegado |
|---|---|
| Punto 1: CONFIRMO el RECHAZA | **EN PIE.** El fichero está mejor fundado que el relato (añade la confirmación en tiempo real). |
| Punto 2: CONFIRMO el ACEPTA | **EN PIE.** Cifras idénticas a las mías. Observación menor sobre el artefacto: cita «líneas 73 y 74», y la regla 13 de CLAUDE.md manda referenciar por símbolo, nunca por número de línea. No afecta al fondo. |
| Punto 3: CONFIRMO el RECHAZA, con matiz | **EN PIE, matiz incluido.** El fichero cita el cierre de `01.02.03` con la frase «SIN REVISAR (regla 16 de CLAUDE.md pendiente)», que en la celda del WBS se refiere al `INFORME_AWESOME_2.md`; la afirmación de `agent_type` vive en el primero, revisado tres veces pero por otra cosa. El matiz sigue y sigue sin tumbar el rechazo. |
| Punto 4: CONFIRMO el RECHAZA (hoy peor) | **EN PIE.** Su `ESCAPA` de entonces y mi `CAZADO`-falso de hoy son la misma causa raíz; el fichero documenta además la secuencia completa (primera pasada del verificador, regeneración, prueba de inyección) y su FIXTURE «byte a byte» coincide con mi verificación independiente sobre copia. |
| Punto 5: CONFIRMO en lo sustancial, REFUTO la subafirmación de las etiquetas | **EN PIE, y la refutación apunta ahora a la frase literal del artefacto:** «Pero **ninguna fila de esta hoja lleva jamás la etiqueta "D-N"** (ni siquiera las antiguas)». Medido por mí: las filas 35–38 empiezan su columna Motivo por «D-18:», «D-19:», «D-20:», «D-21:» — el CEO SÍ puede correlacionar esas cuatro; las otras 31, no. Con ella cae también, para esas cuatro filas, la frase derivada «el CEO no puede correlacionar». El hallazgo de fondo (sin identificador sistemático, doble fuente, regla 28) queda en pie y el RECHAZA no se mueve. |
| Sobrescritura: debilita el punto 5, no lo invalida | **EN PIE y extendido** a `ultimo_estado.json` (diferencia 3 de la lista de arriba). |

### Orden 4 del encargo de continuación — la sección de limitaciones

**CUMPLIDA por el fichero.** Existe la sección «Limitaciones y rotura de cadena de custodia
(declaradas por el propio auditor)», que declara la sobrescritura doble sin copia defensiva, marca
como «NO PROBADA de forma irreversible» toda afirmación sobre el estado de las 21:57, y sostiene
—correctamente, y coincide con mi medición— que las cifras de cabecera del punto 5 son
reproducibles porque el defecto vive en el generador y no en la foto. Esa autodeclaración es lo
que separa esto de una falta grave, y está donde tiene que estar.

### Re-medición tras la edición concurrente de las 23:12

El WBS volvió a cambiar después de mis recuentos originales (mtime 23:12:36, edición del
`secretario` autorizada). Re-ejecutado todo lo que caduca: **158 filas · 60 códigos · 60/60 filas
con 7 campos · 35 entradas en el log · 19 instancias sin sufijo · numstat 40/39**. Idéntico a lo
publicado arriba. Ninguna cifra de esta revisión ha caducado.

**Cierre del addendum:** la revisión del lote (b+c) queda cerrada sobre el artefacto en disco. El
texto pegado dice lo que se me relató en lo que pesa —cifras y veredictos—, con las cuatro
diferencias de texto declaradas arriba, ninguna de las cuales mueve un veredicto. CONFIRMO los
cinco puntos del auditor, mantengo la refutación de la subafirmación de las etiquetas D-N (ahora
contra la frase literal del artefacto) y mantengo que la sobrescritura debilita el punto 5 sin
invalidarlo.
