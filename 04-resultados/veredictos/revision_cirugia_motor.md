# Revisión independiente — cirugía del motor (12/08/2026)

**Revisor:** `critico-codigo` (`claude-sonnet-5`). No he escrito ninguna línea de la cirugía revisada
(regla 16 de CLAUDE.md). Punto de comparación: `89cdf08`. Commits revisados, en orden:
`8de9d7a`, `28c20da`, `f29dfac`, `98c4e9e`, `a587e3f`, `41a5360` (verificado por `git log --oneline
89cdf08..HEAD`: son exactamente esos seis, en ese orden, nada más y nada menos).

Todo lo de abajo se comprobó **ejecutando**, no leyendo. Cada apartado lleva el comando y la salida
real.

---

## 0. Lo primero: ¿se tocó el TEXTO de las 30 reglas? (pregunta 9, va primero por orden expreso)

**NO.** Comparé línea a línea las 30 reglas numeradas de `CLAUDE.md` (antes vs ahora):

```
$ for n in $(seq 1 30); do
    b=$(grep -m1 "^${n}\. " rules_before.md); a=$(grep -m1 "^${n}\. " rules_after.md)
    [ "$b" != "$a" ] && echo "DIFERENCIA en regla $n"
  done
done comparando 1-30
```
Salida: ninguna diferencia. Las 30 reglas son texto idéntico byte a byte.

El único cambio dentro de la sección de reglas es la **nota de estado** bajo la regla 8 (no es la
regla, es su seguimiento): pasa de "SUSPENDIDA (D-17...)" a "VIGENTE de nuevo desde 12/08/2026...
58,9% de motor", y se añade la frase de que la mide `contador_producto_motor.py`. Esto es exactamente
lo que anuncia el commit `a587e3f` ("regla 8 reactivada") y está permitido: una nota de estado no es
el texto normativo de la regla. También cambió el diagrama de las 4 capas (añade "máximo 2 vueltas" y
"UNA sola invocación") y la frase de "Excepción inmediata" (de "3 vueltas" a "2 vueltas sin éxito") —
coherente con el objetivo declarado del commit `98c4e9e`.

## 1. `DEUDA-MOTOR.md`: ¿existe y las filas movidas están íntegras?

**SÍ.** Existe. Comparé las 5 filas (`03.01.12`, `03.01.19`, `03.01.20`, `03.01.24`, `03.01.25`)
byte a byte contra `git show 89cdf08:00-direccion/WBS.md`:

```
$ for code in 03.01.12 03.01.19 03.01.20 03.01.24 03.01.25; do
    grep "^| $code " wbs_before.md > before_$code.txt
    grep "^| $code " 00-direccion/DEUDA-MOTOR.md > after_$code.txt
    diff before_$code.txt after_$code.txt && echo IDENTICAL
  done
```
Salida: `IDENTICAL` las 5 veces. Ni una palabra resumida, ni una cifra tocada, en las 5.

## 2. ¿Alguna tarea viva en el WBS depende de una tarea movida a `DEUDA-MOTOR.md`?

**NO.** Parseé el campo "Depende de" (4º de 5) de todas las filas de tarea de `00-direccion/WBS.md`
actual buscando los 5 códigos movidos:

```python
for line in WBS.md:
    fields = line.split('|')   # 7 con los bordes
    depende = fields[4]
    if any(code in depende for code in ['03.01.12','03.01.19','03.01.20','03.01.24','03.01.25']):
        print(...)
```
Salida: vacía. Ninguna tarea del índice depende de las 5 congeladas. (`DEUDA-MOTOR.md` afirma lo
mismo por su cuenta en la sección "Qué NO se congeló, y por qué"; lo comprobé de forma independiente
y coincide.)

## 3. ¿Se movió alguna tarea que NO estuviera en `pendiente`?

**NO.** Extraje las marcas en negrita de la celda ESTADO en `89cdf08` con el mismo método normativo
del propio WBS (`\*\*(pendiente|hecha|en_curso|bloqueada)\*\*`, "vale la última"):

```
03.01.12 -> ['pendiente'] => vale la ultima: pendiente
03.01.19 -> ['pendiente'] => vale la ultima: pendiente
03.01.20 -> ['pendiente'] => vale la ultima: pendiente
03.01.24 -> ['pendiente'] => vale la ultima: pendiente
03.01.25 -> ['pendiente'] => vale la ultima: pendiente
```
Las 5 tenían una única marca, `pendiente`, en `89cdf08`.

## 4. `AUDITORIA-PESO-MUERTO.md`: ¿una fila por regla (30, no 29) y veredictos dentro de los 4 permitidos?

**SÍ.**

```
$ awk -F'|' 'NR>=60 && NR<=89 {print $2}' AUDITORIA-PESO-MUERTO.md | wc -l
30
$ awk -F'|' 'NR>=60 && NR<=89 {print $7}' AUDITORIA-PESO-MUERTO.md | sort | uniq -c
      1  `CANDIDATA A RETIRAR`
      1  `FUSIONAR CON 9`
     24  `MANTENER`
      4  `NO SÉ`
$ awk -F'|' 'NR>=60 && NR<=89 {print $7}' AUDITORIA-PESO-MUERTO.md | grep -viE 'MANTENER|CANDIDATA A RETIRAR|FUSIONAR CON|NO SÉ|NO SE'
(vacío)
```
30 filas, 4 veredictos usados y los 4 dentro de la lista permitida. El propio documento avisa de que
son 30 y no 29 (el encargo original pedía 29), y acierta.

## 5. ¿Alguna regla `MANTENER` con incidente inventado? (comprobadas 3 al azar de 24)

Elegí **regla 1, regla 8 y regla 27** (sorteo mental sin patrón, una de cada bloque del documento).

- **Regla 1** cita `LECCIONES.md` L-021 e `INFORME_GB2.md` §4.5.
  `grep -n "L-021" 00-direccion/LECCIONES.md` → existe en la línea 176, "L-021 · Una afirmación sin
  procedencia intentó cerrar un incidente abierto", sobre el borrado de `INSTALAR.md` — coincide con
  lo que dice la tabla, palabra por palabra. `INFORME_GB2.md` tiene sección `4.5`. Real.
- **Regla 8** cita `DECISIONES.md` D-1, D-17.
  `grep -n "^## D-17 " DECISIONES.md` → existe: "D-17 · 2026-08-03 · Techo del 20% de motor (regla 8
  de CLAUDE.md) suspendido...". `grep -n "^## D-1 "` → existe. Reales y relevantes.
- **Regla 27** cita `HERENCIA_GB2.md` §3 y `DECISIONES.md` D-9.
  `grep -n "^## D-9 " DECISIONES.md` → existe: "Los datos nunca entran en git" / "gb2 versiono 50.089
  ficheros de datos (1,4 GB por clon)" — cifra idéntica a la que da la auditoría. Real.

Ninguna de las 3 comprobadas tiene incidente inventado.

## 6. `grep -rn -iE 'sin límite de vueltas|2 rondas|3 vueltas' CLAUDE.md .claude/` → ¿da 2?

```
$ grep -rn -iE 'sin límite de vueltas|2 rondas|3 vueltas' CLAUDE.md .claude/
.claude/agents/orquestador.md:81:**No cierras nada por cansancio.** El tope son **2 vueltas** de correccion. Si van 2 rondas sin
.claude/commands/fin.md:27:2. Si van 2 rondas de reparacion sin cerrar, PARA y escala al CEO. En el proyecto anterior, tres
```
**SÍ, da exactamente 2**, y las 2 son consistentes con el límite único de "2 vueltas/rondas" — ninguna
dice "3 vueltas" ni "sin límite". Amplié a `grep -rn -iE '[0-9] (rondas?|vueltas?)' CLAUDE.md .claude/`
y salen 4 líneas en total (las 2 de arriba más 2 en `CLAUDE.md`), todas en "2".

**Hallazgo colateral, fuera del alcance literal de esta pregunta pero de la misma familia:**
`00-direccion/WBS.md` línea 79 sigue diciendo **"3 vueltas del bucle de hipótesis sin éxito"**
(`grep -n "vueltas" 00-direccion/WBS.md`). Ya estaba así en `89cdf08` (no lo tocó esta cirugía), pero
el objetivo declarado del commit `98c4e9e` es "un solo límite de vueltas" y ese objetivo queda
incompleto: sigue habiendo un "3" suelto en la única fuente de verdad del proyecto. No es una
regresión de esta cirugía, pero tampoco la corrige, y debería.

## 7. ¿Las 8 fichas de `.claude/agents/*.md` tienen el bloque obligatorio con CANTIDADES?

**SÍ, las 8.**

```
$ for f in .claude/agents/*.md; do
    echo "$f -> heading=$(grep -c '^## Formato de entrega' $f) CANTIDADES=$(grep -c CANTIDADES $f)"
  done
arquitecto.md -> heading=1 CANTIDADES=2
constructor-datos.md -> heading=1 CANTIDADES=2
constructor-motor.md -> heading=1 CANTIDADES=2
critico-codigo.md -> heading=1 CANTIDADES=2
investigador.md -> heading=1 CANTIDADES=2
orquestador.md -> heading=1 CANTIDADES=2
secretario.md -> heading=1 CANTIDADES=2
validador.md -> heading=1 CANTIDADES=2
```

## 8. `autonomo.md` y el diagrama de `CLAUDE.md`: ¿mismo número de vueltas y misma cadencia de orquestador?

**SÍ.** `autonomo.md` Paso 3: "MÁXIMO DOS VUELTAS" + "No invocas al orquestador entre vuelta y
vuelta" (criterio ya viaja en la orden del Paso 1). Paso 4: JUZGAR se invoca **UNA vez** si el revisor
acepta; si tras dos vueltas no acepta, PARA y se invoca al orquestador solo para preparar el escalado
(no hay tercera vuelta de corrección). El diagrama de `CLAUDE.md` (sección "Cómo se trabaja: las cuatro capas"): "REPARTE — UNA sola
vez por tarea" → "máximo 2 vueltas, luego se escala" → "SIN orquestador entre vuelta y vuelta" →
"JUZGA — UNA sola invocación" → "Al orquestador se le llama DOS veces por tarea, no una por vuelta".
Coinciden en número de vueltas (2) y en cuántas veces se llama al orquestador (2: repartir y
juzgar/escalar).

## 9. Ver apartado 0 — NO se tocó el texto de ninguna regla.

## 10. ¿Se tocó algo bajo `03-motor/backtester/`, `03-motor/scripts/`, `02-datos/`, `01-investigacion/` o `04-resultados/`?

**NO.**
```
$ git diff --name-only 89cdf08..HEAD | grep -E '^(03-motor/backtester/|03-motor/scripts/|02-datos/|01-investigacion/|04-resultados/)'
(sin salida, exit 1)
```
El `git diff --name-status` completo (28 ficheros) solo toca `.claude/`, `00-direccion/`,
`05-vista-ceo/` y `CLAUDE.md`.

## 11. Contador producto/motor: ¿reproduce 43,8% sobre los 16 commits de referencia, con MI propio script?

**SÍ.** Leí `01-investigacion/ecosistema/INFORME_AWESOME.md` (sección "REGLA DE CLASIFICACIÓN CORREGIDA", bajo el apartado P1) para sacar la regla de
clasificación documentada (WBS con código decide por fase: 01.01.\*/02/04/05/06 = producto,
01.02.\*/03/07 = motor; sin código WBS se clasifica por rutas: `.claude/**`, `.githooks/**`,
`05-vista-ceo/**` o fichero de config raíz = motor, solo `00-direccion/**` = papeleo, resto =
producto; `03-motor/**` nunca es criterio). Escribí mi propio clasificador en
`/tmp/.../clasificador_propio.py` (no importa ni ejecuta
`.claude/hooks/contador_producto_motor.py`) y lo corrí sobre el rango real de 16 commits
(`da1e3c7`..`79902cb`, confirmado root-a-`79902cb` = 16 commits):

```
$ python3 clasificador_propio.py 79902cb
...
Total commits: 16
Motor: 7  Producto: 9  Papeleo: 0  Desconocido: 0
Porcentaje motor (motor / (total - papeleo)): 43.8%
```
Coincide con el 43,8% documentado, calculado de forma independiente.

## 12. `verificar_excel.py` y `prueba_inyeccion.sh`: ¿igual o mejor que ANTES?

**SÍ, mejor en los dos.** Pero antes, un aviso: **la instrucción que recibí decía "6 de 7 casos
cazados" en el ANTES, y eso es falso.** `00-direccion/MEDICION-CIRUGIA.md` dice literalmente "los 7
guardias de inyección **muerden los 7**" y lo repite en la tabla (7 líneas `CAZADO`). El "1 problema"
del ANTES no es un caso no cazado: es que el propio WBS de partida no pasaba la verificación (algo
ajeno a los 7 casos inyectados). Reporto lo que de verdad dice el documento fuente, no lo que decía mi
encargo, tal como exige la regla 11 de CLAUDE.md.

Ejecutado ahora mismo:
```
$ .venv/bin/python 05-vista-ceo/verificar_excel.py; echo EXIT=$?
... RESULTADO: sin fallos. 9 avisos.
EXIT=0
```
Antes: **10 FALLOS, salida 1**. Ahora: **0 FALLOS, salida 0**. Mejora clara. (El censo baja de 67 a 62
tareas en el índice, coherente con las 5 movidas a `DEUDA-MOTOR.md`.)

```
$ bash 05-vista-ceo/prueba_inyeccion.sh; echo EXIT=$?
... RESULTADO: el verificador muerde en los 7 casos.
EXIT=0
```
Antes: **7 de 7 CAZADO pero salida 1** (por el fallo de fondo del WBS, no por los casos inyectados).
Ahora: **7 de 7 CAZADO y salida 0**, porque además el WBS de partida ya pasa la verificación. Igual de
efectivo cazando, y ahora también limpio en el fondo.

**Gap real que sí encontré:** la sección `## DESPUÉS` de `00-direccion/MEDICION-CIRUGIA.md` sigue
diciendo literalmente `*(se rellena en el bloque 7)*` — está vacía. El propio documento se
comprometió a medir "antes y después de operar" y el después no se rellenó, pese a que los 6 commits
de la cirugía ya están cerrados. No es un fallo de las pruebas (que sí mejoran, medidas por mí), es un
artefacto de la cirugía que quedó a medias.

## 13. ¿Se creó alguna tarea nueva en el WBS durante la cirugía?

**NO.**
```python
before = codigos_en('wbs_before.md')      # 67
after  = codigos_en('WBS.md') | codigos_en('DEUDA-MOTOR.md')  # 62 + 5 = 67
after - before  -> []   # nada nuevo
before - after  -> []   # nada perdido
```
Los mismos 67 códigos de siempre, repartidos ahora entre el índice (62) y la deuda congelada (5).

---

## Comprobación adicional: las 25 celdas movidas a `00-direccion/expedientes/`

Comparé cada uno de los 25 expedientes byte a byte contra la celda ESTADO de su tarea en
`git show 89cdf08:00-direccion/WBS.md` (script Python, extrae el 5º campo de la fila y el bloque bajo
"## Celda ESTADO integra..." del expediente, y compara longitudes y contenido exacto):

**24 de 25 coinciden exactamente byte a byte.**

**1 de 25 (`03.01.18`) NO coincide contra `89cdf08`**: 1.399 caracteres en `89cdf08` frente a 1.530 en
el expediente. Investigado el motivo: **no es un fallo de copia**. La tarea `03.01.18` es precisamente
el contador producto/motor, y se **ejecutó dentro de esta misma cirugía** (commit `a587e3f`,
"03.01.18: contador producto/motor + regla 8 reactivada") — está explícitamente excluida del
congelamiento por el propio `DEUDA-MOTOR.md` ("Excluida por el propio encargo: es el contador
producto/motor, y se ejecuta"). Entre `89cdf08` y el commit de partición (`41a5360`) la celda cambió
legítimamente de `**pendiente**` a `**hecha** 12/08 — ...`, por trabajo real. Lo verifiqué comparando
el expediente contra el estado del WBS **inmediatamente antes** del commit de partición
(`git show 41a5360^:00-direccion/WBS.md`), que es el punto de comparación correcto para juzgar la
integridad de la copia:

```python
IDENTICAL: True
```

Coincide byte a byte con lo que de verdad había en el WBS en el momento de mover la celda. **Las 25
copias son íntegras; el único "no-match" contra `89cdf08` es una tarea que avanzó de verdad durante la
cirugía, no una palabra resumida ni una cifra tocada.**

---

## Veredicto

**ENTREGADO.** No encontré ninguna regla alterada, ninguna cita `D-NN` fabricada, ninguna tarea nueva
sin pasar por el WBS, ninguna dependencia rota, ninguna celda recortada, y las dos pruebas de
regresión (`verificar_excel.py`, `prueba_inyeccion.sh`) mejoran sobre el listón real documentado.

Dos cosas para el checkpoint del lunes, ninguna bloqueante:
1. `00-direccion/WBS.md` línea 79 sigue con "3 vueltas" suelto (pregunta 6): el objetivo de "un solo
   límite de vueltas" del commit `98c4e9e` no llegó a esa línea.
2. `00-direccion/MEDICION-CIRUGIA.md` sección `## DESPUÉS` está vacía (pregunta 12): el documento
   promete medir antes y después y solo mide el antes.

Y un aviso sobre el propio encargo que recibí: la cifra "6 de 7 casos cazados" que me dieron para el
ANTES de la pregunta 12 no es lo que dice `00-direccion/MEDICION-CIRUGIA.md` (que dice 7 de 7). Lo
reporto porque la regla 11 de CLAUDE.md obliga a verificar, no a repetir lo que llega en el encargo.
