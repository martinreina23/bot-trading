# Verificación 03.01.24 — Las tres barreras que hoy no existen (a, b, c)

**Tarea WBS:** 03.01.24. **Autorización:** D-29 opción A (`00-direccion/DECISIONES.md`), firmada
09/08/2026. **Ejecutor:** `constructor-motor`, modelo declarado `claude-sonnet-5` (regla 29 de
CLAUDE.md). **Respaldo:** no ha hecho falta usar `claude-opus-5`; todo el trabajo se hizo con
`claude-sonnet-5`. **Fecha:** 09/08/2026.

**Orden de ejecución:** (c) primero, tal como exigió el reparto, porque podía salir imposible.
Después (a) y (b), como restricción de proceso: el parche vive en un fichero aparte
(`04-resultados/parche_settings_03.01.24.json`), nunca escrito por mí sobre
`.claude/settings.json`.

**Prohibiciones respetadas, declaradas explícitamente:**
- Ningún comando de esta tarea referenció, leyó, listó ni rozó `02-datos/reservado/` real. Todas
  las inyecciones de (a) y (b) se hicieron contra una carpeta decoy dentro del área de pruebas de
  este agente (`/tmp/claude-1000/.../scratchpad/prueba_03.01.24/`), con ficheros de mentira creados
  por mí, nunca contra el cajón real.
- No se escribió sobre `.claude/settings.json` (verificado al final con `git status`/`git diff`).
- No se tocó `00-direccion/WBS.md` ni `00-direccion/DECISIONES.md`.
- No se hizo commit.
- El `02-datos/bruto/` real (NO reservado, sirve de testigo) se contó antes y después: **791
  ficheros, sin cambio**, y `git status --porcelain 02-datos/` da vacío (los datos no entran en
  git, regla 27 de CLAUDE.md).

---

## (c) Barrera de gasto — PRIMERO, por orden expresa

### Lo que dice D-26 (localizado por grep antes de citarlo)

```
$ grep -n "max-budget-usd\|API calls\|inerte" 00-direccion/DECISIONES.md
270:**Devuelve `claude --help` en la versión 2.1.221 instalada:** `--max-budget-usd <amount>` — "Maximum dollar amount to spend on API calls".
272:**Aviso crítico no medido todavía:** el help dice "API calls", y si el proyecto corre sobre plan de suscripción, ese tope puede ser inerte. No se declara activo hasta que se pruebe por inyección con un límite deliberadamente ínfimo y se compruebe que la herramienta corta de verdad (regla 25 de CLAUDE.md).
```

### Paso 1 — el flag existe en esta máquina

```
$ claude --version
2.1.226 (Claude Code)

$ claude --help | grep -A2 "max-budget"
  --max-budget-usd <amount>             Maximum dollar amount to spend on API
                                        calls (only works with --print)
```

Confirmado: el flag existe (versión 2.1.226, una más reciente que la 2.1.221 que citaba D-26; sigue
existiendo). Solo funciona con `--print`.

### Paso 2 — el tipo de cuenta de esta máquina

```
$ env | grep -i "anthropic\|api_key\|claude"
CLAUDE_CODE_CHILD_SESSION=1
AI_AGENT=claude-code_2-1-226_agent
CLAUDE_CODE_SESSION_ID=...
CLAUDE_PID=...
CLAUDE_EFFORT=xhigh
CLAUDE_CODE_MESSAGING_SOCKET=...
CLAUDECODE=1
CLAUDE_CODE_ENTRYPOINT=cli
CLAUDE_CODE_EXECPATH=...
(sin ninguna ANTHROPIC_API_KEY)

$ claude auth status
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "email": "martinreina23@gmail.com",
  "orgId": "506c3b4d-d09d-4d21-9c47-871170377f1a",
  "orgName": "martinreina23@gmail.com's Organization",
  "subscriptionType": "max"
}
```

Confirmado hoy, por ejecución propia (no por cita de una tarea anterior): esta máquina se autentica
por suscripción (`claude.ai`, plan `max`), no por clave de API. Coincide con lo que ya medía
03.01.23 el 04/08, pero se remide aquí en vez de aceptarse de palabra (regla 11 de CLAUDE.md).

### Paso 3 — inyección con límite deliberadamente ínfimo (regla 25 de CLAUDE.md)

**Inyección 1**, presupuesto de $0.000001, formato JSON para ver el desglose:

```
$ claude -p "responde solo con la palabra OK" --model claude-haiku-4-5-20251001 \
    --max-budget-usd 0.000001 --output-format json --max-turns 1
```

Salida literal:

```json
{"is_error":true,"duration_api_ms":924,"num_turns":1,"stop_reason":null,
 "session_id":"47cfab78-39c0-4c4c-8268-12acbc66c698","total_cost_usd":0.000593,
 "usage":{"input_tokens":0,"output_tokens":0,...},
 "modelUsage":{"claude-haiku-4-5-20251001":{"inputTokens":523,"outputTokens":14,
   "costUSD":0.000593,...}},
 "permission_denials":[],
 "terminal_reason":"budget_exhausted",
 "subtype":"error_max_budget_usd",
 "errors":["Reached maximum budget ($0.000001)"],
 "type":"result","duration_ms":1219}
```

Código de salida: **1**.

**Lectura del resultado, literal, sin adornar:** la llamada a la API **SÍ se hizo completa** —523
tokens de entrada, 14 de salida, coste nocional $0.000593— **antes** de que la herramienta
declarara `budget_exhausted`. El presupuesto era $0.000001 y el gasto real fue **593 veces mayor**.
La barrera no impidió el gasto: lo detectó **después** de que ya hubiera ocurrido, y solo entonces
abortó (sin turno adicional que bloquear, porque `--max-turns 1` ya limitaba a uno).

**Inyección 2**, control: ¿puede fijarse presupuesto $0 para que ni siquiera arranque la primera
llamada?

```
$ claude -p "responde solo con la palabra OK" --model claude-haiku-4-5-20251001 \
    --max-budget-usd 0 --output-format json --max-turns 1
```

Salida literal:

```
error: option '--max-budget-usd <amount>' argument '0' is invalid. --max-budget-usd must be a positive number greater than 0
```

Código de salida: 1, pero por validación de argumento **antes** de intentar nada — no cuesta nada,
pero tampoco demuestra que el mecanismo prevenga un gasto real: solo confirma que el mínimo
aceptado es mayor que cero, así que **siempre** hay que dejar pasar al menos una llamada.

**Inyección 3**, repetición con salida de texto para confirmar el mensaje al usuario:

```
$ claude -p "responde solo con la palabra OK" --model claude-haiku-4-5-20251001 \
    --max-budget-usd 0.000001 --max-turns 1
```

Salida literal:

```
Error: Exceeded USD budget (0.000001)
```

Código de salida: 1. Mismo patrón: reactivo, no preventivo.

### Veredicto (c)

**IMPOSIBLE. NO EXISTE BARRERA DE GASTO POSIBLE EN ESTA MÁQUINA que corte de verdad, en el sentido
que pide la regla 25 de CLAUDE.md (impedir el gasto, no solo detectarlo después).**

Motivos, los tres medidos hoy por ejecución:
1. Solo funciona con `--print`, no con el flujo interactivo ni con el encadenador desatendido de
   `03.01.23` tal como está descrito hoy (ese script lanza `claude -p` por tarea, así que SÍ podría
   añadirse el flag ahí — pero eso es cablear el flag en el script, no una barrera de la máquina en
   sí, y no es alcance de esta tarea).
2. **Es reactivo, no preventivo:** con el límite más bajo que la herramienta admite ($0.000001), la
   llamada a la API se completó entera (593× el límite) antes de que la herramienta lo detectara.
   Un caso real de gasto descontrolado en una sola llamada cara (una búsqueda web masiva, un
   contexto enorme) no se evitaría: se detectaría después, con el dinero ya "gastado" según su
   propia cifra.
3. La cuenta de esta máquina es de **suscripción** (`claude.ai`, plan `max`), no de API de pago por
   token (`claude auth status`, confirmado hoy). El `total_cost_usd` que la herramienta reporta es
   una cifra nocional de contabilidad interna del modelo de precios de API, no una confirmación de
   que se cargó dinero real en algún sitio; no hay forma de verificar desde esta máquina que ese
   número tenga contrapartida en una factura. D-26 avisó exactamente de este riesgo («el help dice
   API calls... puede ser inerte») y la medición de hoy lo confirma en el peor sentido: ni siquiera
   corta antes de la primera llamada.

Coste real de estas tres inyecciones: nocional ~$0.0012, deliberadamente ínfimo, dentro de lo que
la propia ficha anticipaba como aceptable para esta prueba.

---

## (a) El agujero del patrón `Bash(* 02-datos/reservado*)`

### Baseline — reproducir hoy, no aceptar de palabra lo del 05/08 (regla 11 de CLAUDE.md)

Carpeta decoy creada, **nunca el cajón real**:

```
$ mkdir -p .../prueba_03.01.24/decoy_root/02-datos/reservado
$ echo "DECOY -- NO es el cajon reservado real. Fichero de prueba creado por 03.01.24." \
    > .../decoy_root/02-datos/reservado/decoy.txt
```

**Forma 1** (la que ya paraba el patrón viejo): verbo con espacio literal antes de la ruta relativa.

```
$ cd .../decoy_root && cat 02-datos/reservado/decoy.txt
```

Salida literal: `Permission to use Bash with command ... has been denied.` — **BLOQUEADO**, igual
que el 05/08.

**Forma 2** (otro verbo, mismo patrón de espacio):

```
$ cd .../decoy_root && head -c 30 02-datos/reservado/decoy.txt
```

Salida literal: `Permission to use Bash with command ... has been denied.` — **BLOQUEADO**.

**Forma 3** (la que se coló el 05/08): línea de python con la ruta pegada a una comilla, sin espacio
literal delante de `02-datos/reservado`.

```
$ cd .../decoy_root && python3 -c "print(open('02-datos/reservado/decoy.txt').read())"
```

Salida literal:
```
DECOY -- NO es el cajon reservado real. Fichero de prueba creado por 03.01.24.

codigo salida forma 3: 0
```

**NO bloqueado.** Agujero reproducido hoy, con datos de mentira, exactamente como lo describe
`00-direccion/WBS.md` en la celda de `03.01.08`.

### Control adicional — confirmar en vivo el estilo de patrón que se propone

Ya existe en `.claude/settings.json` un patrón del mismo estilo que el que propongo (substring puro,
sin exigir espacio delante): `Bash(*--no-verify*)`. Si ese estilo bloquea texto **pegado a
comillas**, es la prueba de que cambiar `02-datos/reservado` al mismo estilo cierra el agujero.

```
$ python3 -c "print('--no-verify')"
```

Salida literal: `Permission to use Bash with command ... has been denied.` — **BLOQUEADO**, con el
texto pegado a comillas de exactamente la misma forma que la forma 3. Confirma en vivo, contra el
motor real (no una suposición), que el estilo de patrón propuesto funciona.

### Validación del patrón propuesto (fnmatch calibrado contra el motor real)

Script: `/tmp/claude-1000/.../scratchpad/prueba_03.01.24/matcher.py`. Reimplementa en Python el
matching de `Bash(...)` como `fnmatch` sobre el texto completo del comando, y se **calibra** contra
los tres resultados medidos en vivo arriba antes de usarse para validar nada:

```
[OK] forma1_cat_espacio: fnmatch(patron_viejo)=True  medido_en_vivo_denegado=True
[OK] forma2_head_espacio: fnmatch(patron_viejo)=True  medido_en_vivo_denegado=True
[OK] forma3_python_comilla_simple: fnmatch(patron_viejo)=False  medido_en_vivo_denegado=False

Reimplementacion fnmatch FIEL a las 3 formas medidas en vivo.
```

Con el matcher calibrado (0 desajustes), se prueba el patrón propuesto `*02-datos/reservado*`
contra 8 casos (los 3 medidos más 5 variantes de la misma familia: comilla doble, `./ruta`, ruta
absoluta, variable de entorno, subshell):

```
caso                             viejo bloquea   nuevo bloquea
forma1_cat_espacio               True            True
forma2_head_espacio              True            True
forma3_python_comilla_simple     False           True
forma3b_python_comilla_doble     False           True
forma4_dotslash                  False           True
forma5_absoluta                  False           True
forma6_dospuntos_var             True            True
forma7_subshell                  True            True

Todo lo que bloqueaba el patron viejo lo sigue bloqueando el nuevo (superset): True
El nuevo patron cierra la forma 3 (comilla pegada), que el viejo NO bloqueaba: True

RESULTADO: patron nuevo VALIDADO por fnmatch calibrado contra el motor real. ENDURECE sin debilitar.
```

### Parche propuesto (a)

Fichero: `04-resultados/parche_settings_03.01.24.json`. Añade **una línea nueva** al array `deny`,
sin tocar ninguna de las existentes:

```json
"Bash(*02-datos/reservado*)"
```

Es un **superset estricto** de `Bash(* 02-datos/reservado*)`: todo comando que el patrón viejo
bloqueaba, el nuevo también lo bloquea (demostrado arriba), y además cierra la forma pegada a
comilla, a `./`, a ruta absoluta o a cualquier otro carácter que no sea un espacio.

**Límite declarado, no escondido:** este patrón sigue siendo un `substring` de texto, no una
resolución de ruta real. Una ofuscación que partiera el texto en trozos (p. ej.
`'02-datos/' + 'reservado/x'` en Python, concatenados en tiempo de ejecución) seguiría sin
contener el substring literal `02-datos/reservado` y **no** quedaría cubierta. Es un hueco
estructural del propio mecanismo de permisos por texto, no un defecto de este parche, y no es lo
que se midió el 05/08 ni lo que autoriza D-29 hoy: se declara para que no se dé por resuelto algo
más amplio de lo que en realidad se resuelve.

### Veredicto (a)

- **Estado en el fichero real `.claude/settings.json`, sin tocar por mí: NO VERIFICADA** — el
  agujero medido el 05/08 se reproduce hoy, igual, con datos de mentira.
- **Parche propuesto: validado por ejecución contra copia/decoy** (fnmatch calibrado + control en
  vivo con un patrón del mismo estilo). Pasará a **ACTIVA** solo cuando Claude Code lo aplique sobre
  el fichero real con la aprobación del usuario y se repita la inyección contra el fichero ya
  parcheado — eso no es alcance de este agente (regla 25 de CLAUDE.md: "un guardia presente en el
  código no es un guardia probado").

---

## (b) `rm -rf` dentro de `02-datos/`

### Baseline — reproducir hoy, con decoy, nunca con datos reales

**Caso medido el 05/08 (ruta relativa):**

```
$ mkdir -p .../decoy_root/02-datos/bruto
$ echo "DECOY -- carpeta de prueba para rm -rf..." > .../decoy_root/02-datos/bruto/decoy_borrar.txt
$ cd .../decoy_root && rm -rf 02-datos/bruto/decoy_borrar.txt
codigo salida rm -rf (sin parche): 0
```

Fichero decoy borrado, código 0, **sin ninguna denegación**. Reproducido tal cual lo mide la celda
de `03.01.08` del WBS.

**Control — ruta absoluta, para saber qué SÍ cubre ya `Bash(rm -rf /*)`:**

```
$ rm -rf /tmp/.../decoy_root2/02-datos/bruto/x.txt
```

Salida literal: `Permission to use Bash with command ... has been denied.` — **BLOQUEADO**. El
patrón viejo `rm -rf /*` ya cubre cualquier `rm -rf` cuyo texto de comando **empiece** literalmente
por `rm -rf /` (cualquier ruta absoluta, no solo la raíz del sistema). El agujero real es el de
rutas **relativas** o comandos **encadenados** donde `rm -rf` no es lo primero del texto.

**Variante — orden invertido (se entra a la carpeta 02-datos primero, luego se borra):**

```
$ cd .../decoy_root3/02-datos/bruto && rm -rf decoy3.txt
codigo salida: 0
```

**Sin bloqueo.** Mismo agujero, con el texto en otro orden.

**Variante — banderas invertidas (`-fr` en vez de `-rf`):**

```
$ cd .../decoy_root4 && rm -fr 02-datos/bruto/decoy4.txt
codigo salida: 0
```

**Sin bloqueo.** Misma acción (GNU `rm` trata `-rf` y `-fr` igual), mismo agujero.

### Validación del patrón propuesto (mismo matcher, calibrado también aquí)

```
--- calibracion patron viejo 'rm -rf /*' contra lo medido en vivo ---
[OK] baseline_relativo_medido_en_vivo: fnmatch=False  medido_en_vivo=False
[OK] absoluto_ya_cubierto: fnmatch=True  medido_en_vivo=True
Calibracion (b): FIEL, sin desajustes

caso                                   viejo bloquea   nuevo bloquea
baseline_relativo_medido_en_vivo       False           True
absoluto_ya_cubierto                   True            True
orden_invertido_cd_primero             False           True
flags_invertidos_fr                    False           True
no_toca_02_datos_control_negativo      False           False

Todo lo que bloqueaba el patron viejo lo sigue bloqueando el nuevo (superset): True
El nuevo patron cierra el caso medido en vivo (relativo, codigo 0 sin parche): True
El nuevo patron cierra el orden invertido (cd al 02-datos primero): True
El nuevo patron cierra el flag invertido (rm -fr): True
El nuevo patron NO bloquea un rm -rf fuera de 02-datos (control negativo, no debe sobre-bloquear): True

RESULTADO (b): patron nuevo VALIDADO por fnmatch calibrado contra el motor real. ENDURECE sin debilitar.
```

El caso `no_toca_02_datos_control_negativo` (`rm -rf` sobre una carpeta que NO es `02-datos/`) se
valida solo con el modelo calibrado, no con una inyección en vivo adicional: no tiene sentido borrar
algo de verdad fuera del área de pruebas solo para confirmar que un patrón que no lo menciona no lo
toca; el modelo ya está calibrado con 0 desajustes contra el motor real en los dos casos que sí
importaban (relativo y absoluto).

### Parche propuesto (b)

Cuatro líneas nuevas en el array `deny`, cubriendo las dos banderas (`-rf`/`-fr`) en los dos órdenes
posibles del texto (`rm` antes de `02-datos` y al revés):

```json
"Bash(*rm -rf*02-datos*)"
"Bash(*02-datos*rm -rf*)"
"Bash(*rm -fr*02-datos*)"
"Bash(*02-datos*rm -fr*)"
```

**Alcance deliberadamente ceñido al incidente medido (regla 24 de CLAUDE.md — una restricción solo
nace de un incidente real):** estas cuatro líneas cubren `rm -rf`/`rm -fr`, que es la acción
exacta que salió con código 0 el 05/08 y su variante trivial de banderas invertidas (misma acción,
mismo dato, dos letras cambiadas de sitio). **Fuera de alcance, declarado y no maquillado:** banderas
separadas (`rm -r -f`), banderas largas (`--recursive --force`), y otras formas de destruir datos
que no son `rm` (`find -delete`, `shred`, `truncate`, `dd`, `shutil.rmtree` de Python). Ninguna de
esas se ha medido con un incidente real hoy; añadir un guardia para ellas sin un incidente sería
inventar una restricción sin la base que exige la regla 24 de CLAUDE.md. Si alguna se mide en el
futuro, es una tarea nueva con su propio incidente, no una ampliación silenciosa de esta.

### Veredicto (b)

- **Estado en el fichero real `.claude/settings.json`, sin tocar por mí: NO VERIFICADA** — nada
  impide `rm -rf` (ni `rm -fr`) dentro de `02-datos/` cuando la ruta es relativa o el comando está
  encadenado; reproducido hoy con tres variantes distintas, las tres con código 0.
- **Parche propuesto: validado por ejecución contra copia/decoy.** Pasará a **ACTIVA** solo cuando
  se aplique sobre el fichero real y se repita la inyección contra el fichero ya parcheado.

---

## Comprobación final de que nada se dañó ni se tocó indebidamente

```
$ find /home/server/projects/bot-trading/02-datos/bruto -type f | wc -l
791
```

Mismo número que medía `03.01.08` el 05/08 (791 ficheros de `bruto/` intactos). `02-datos/reservado/`
**no se ha listado, leído ni referenciado por ningún comando de esta tarea**, ni con ruta real ni de
ninguna otra forma; todas las pruebas de (a) y (b) se hicieron contra una carpeta decoy con el mismo
nombre de subcarpeta (`.../decoy_root/02-datos/reservado/`), nunca contra la ruta real del proyecto.

```
$ git status --porcelain 02-datos/
(vacío)
```

Salida literal de `git status --short` al terminar esta tarea:

```
 M .githooks/pre-commit
 M 00-direccion/DECISIONES.md
?? 03-motor/scripts/tamano_minimo_operable.py
?? 04-resultados/parche_settings_03.01.24.json
?? 04-resultados/tamano_minimo_operable.json
?? 04-resultados/tamano_minimo_operable.md
?? 04-resultados/veredictos/revision_03.01.24_registro.md
?? 04-resultados/veredictos/revision_04.01.04.md
?? 04-resultados/verificacion_03.01.24.md
?? 04-resultados/verificacion_03.01.25.md
```

**De estas líneas, solo dos son mías:** `04-resultados/parche_settings_03.01.24.json` y
`04-resultados/verificacion_03.01.24.md` (los dos artefactos de esta tarea). El resto —
`.githooks/pre-commit`, `00-direccion/DECISIONES.md`, `tamano_minimo_operable.*`,
`revision_03.01.24_registro.md`, `revision_04.01.04.md`, `verificacion_03.01.25.md`— ya estaban
así **antes** de que esta tarea empezara o pertenecen a otros agentes trabajando en paralelo en este
mismo repositorio (03.01.25 y otras tareas abiertas); ninguno lo tocó este agente. `.claude/settings.json`
**no aparece en la lista**: confirmado que no lo escribí (`git diff -- .claude/settings.json` da vacío).
`00-direccion/WBS.md` tampoco aparece: no lo toqué.

No se ha hecho ningún commit.

---

## Resumen de veredictos

| Barrera | Estado en `.claude/settings.json` (sin tocar) | Parche propuesto |
|---|---|---|
| (a) patrón cajón reservado | **NO VERIFICADA** — agujero reproducido hoy (forma 3) | Validado por ejecución contra decoy; superset estricto del patrón viejo |
| (b) `rm -rf`/`rm -fr` en `02-datos/` | **NO VERIFICADA** — reproducido hoy en 3 variantes (relativo, orden invertido, banderas invertidas), todas código 0 | Validado por ejecución contra decoy; 4 líneas nuevas, ceñidas al incidente medido |
| (c) tope de gasto | **IMPOSIBLE — NO EXISTE BARRERA DE GASTO POSIBLE EN ESTA MÁQUINA** | No aplica: no hay parche de `settings.json` para esto; el mecanismo de la CLI es reactivo (deja pasar la primera llamada, 593× el límite fijado) y la cuenta es de suscripción, no de API de pago |

**Artefactos entregados:**
- `04-resultados/parche_settings_03.01.24.json` — parche propuesto (a) y (b), no aplicado por mí.
- `04-resultados/verificacion_03.01.24.md` — este fichero.

**Lo que sigue, y no es mío:** que Claude Code aplique el parche sobre `.claude/settings.json` con
la aprobación del usuario (ningún agente puede autorizarlo); que se repita la inyección de (a) y (b)
contra el fichero ya parcheado para pasar de "validado contra decoy" a **ACTIVA**; el punto (d) de
la ficha D-29, que ejecuta otro agente en 03.01.25.
