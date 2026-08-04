#!/usr/bin/env bash
#
# controlador.sh — encadenador de sesiones desatendidas (03.01.23)
# =============================================================================
# REDUCIDO por orden directa del CEO (04/08): se habia crecido con gobernanza que
# el nunca pidio (lista verde, topes en dolares, cron, hook de aviso). En sus
# palabras: "en vez de enlazar tantas tareas seguidas se parara antes para no
# consumir tokens y automaticamente abriera otra sesion de claude con la proxima
# tarea". Lo que queda es justo eso: un bucle que lanza una sesion, la sesion
# decide su propia tarea via /autonomo, y el controlador solo lee como termino
# para decidir si sigue o para.
#
# QUE HACE: lanza una sesion NUEVA de `claude -p` que ejecuta /autonomo (el
# orquestador decide que tarea toca, como ya hace hoy). Cuando termina, lee tres
# cosas: el JSON de la propia sesion (is_error), el fichero DESENLACE.txt que la
# sesion tiene que dejar escrito, y ESTADO.md (que exista, no este vacio, y no se
# pase del tope de lineas). Si todo esta bien y el desenlace es CERRADA, lanza la
# siguiente. Cualquier otra cosa, para y avisa al CEO.
#
# QUIEN ES DUEÑO DE CADA FICHERO:
#   config.env       -> el CEO fija los numeros. Solo lectura aqui, campo a campo.
#   DESENLACE.txt    -> lo escribe CADA SESION, fresco, al terminar. El
#                       controlador lo borra antes de lanzar y lo lee despues:
#                       ausente tras la sesion = esa sesion no lo dejo escrito.
#   ESTADO.md        -> lo escribe CADA SESION al terminar (corto, tope en
#                       MAX_LINEAS_ESTADO): que tarea trabajo, con que
#                       desenlace, que quedo pendiente, que se rechazo y por
#                       que. La SIGUIENTE sesion lo lee para no arrancar en
#                       blanco. El controlador NUNCA escribe su contenido, pero
#                       SI comprueba mecanicamente que existe, que no esta
#                       vacio, que se actualizo en esta sesion (no es un resto
#                       de una sesion anterior) y que no se paso del tope de
#                       lineas -- si algo de eso falla, para (ver Paso 6).
#   STOP_CEO.flag    -> SOLO el controlador. Se pone cuando decide parar
#                       (desenlace ESCALADA/BLOQUEADA/invalido, ESTADO.md
#                       ausente o demasiado largo, fallo tecnico, o alguien lo
#                       crea a mano). Nunca se autolimpia; solo
#                       --reanudar-tras-ceo, pasado a mano, la quita.
#   PARA-CEO.md      -> la sesion la prepara si escala/bloquea (con la ficha de
#                       verdad); si no la deja, el controlador escribe una de
#                       repuesto para que el CEO no se quede sin nada que leer.
#   controlador.log  -> solo el controlador. Registro operativo, no gobierno.
#
# POR QUE NUNCA --resume NI --continue (aunque parezca mas barato):
#   la razon de que cada sesion sea NUEVA es el problema que mide la tarea
#   03.01.21 ("Diagnostico medido del consumo de tokens del motor de agentes",
#   00-direccion/WBS.md, estado "hecha"): sobre el transcript en disco de una
#   sesion real, el hilo principal leyo **94,9 millones de tokens de cache** en
#   207 peticiones, con un contexto medio de ~452.000 tokens. --resume/--continue
#   reproducirian exactamente eso: acumular pasos en la misma conversacion. NO LO
#   "OPTIMICES" metiendo --resume aqui: es la causa raiz que este guion existe
#   para evitar. (Se cita por codigo de tarea, no por numero de linea del WBS:
#   un numero de linea se rompe en cuanto alguien edite el fichero -- regla 13
#   de CLAUDE.md.)
#
# POR QUE NUNCA --dangerously-skip-permissions NI --permission-mode
# bypassPermissions (esto es SOLO el comentario, no hay mecanismo de permisos
# en este guion: no se toca la configuracion de la maquina):
#   en esta maquina el usuario YA corre en bypassPermissions por defecto
#   (decision D-27, registrada por el CEO, NO la toca este guion). Escribir aqui
#   ese flag otra vez seria redundante Y peligroso: convertiria una exencion que
#   hoy es un HECHO del entorno (verificable, revisable, revertible por el CEO)
#   en una decision fija dentro del codigo, elegida por el propio guion que se
#   ejecuta sin nadie delante. Eso es exactamente lo que la regla 26 de
#   CLAUDE.md prohibe: "la condicion que activa una exencion debe ser un hecho
#   impuesto por el sistema, nunca un dato que elija el vigilado".
#
# MODO POR DEFECTO: --simulacro. No llama a Claude ni una vez, no gasta nada.
# Para encender de verdad hace falta pasar --de-verdad explicitamente.
#
# CLAUDE_BIN: variable de entorno SOLO PARA PRUEBAS. Por defecto vale "claude"
# (el binario real, resuelto por PATH). Se sobreescribe para apuntar a un
# binario de mentira y probar la rama --de-verdad sin gastar dinero real ni
# contar como invocacion real de `claude -p`.
#
# config.env YA NO SE "source"EA: se parsea CAMPO A CAMPO, solo se aceptan las
# claves de la lista blanca de abajo (cada una una sola vez), y cada valor tiene
# un minimo obligatorio donde un 0 seria peligroso (mismo criterio que ya se
# aplico a TIMEOUT_SESION_SEGUNDOS: GNU 'timeout' documenta que "a duration of 0
# disables the associated timeout").
#
# YA NO HAY lista verde, cola.txt, ni tope en dolares (--max-budget-usd): por
# orden del CEO. La lista verde era gobernanza que el nunca pidio; el tope en
# dolares no limitaba nada de verdad porque esta maquina no tiene clave de API
# (corre sobre plan de suscripcion, comprobado). Lo que SI limita el trabajo es
# --max-turns (se queda) y el tope de tareas por tirada. Tampoco hay ya
# --disallowedTools: protegia ficheros (lista-verde.txt, cola.txt, progreso.tsv)
# que ya no existen.

set -u

# ---------------------------------------------------------------------------
# 0. Argumentos
# ---------------------------------------------------------------------------
MODO="simulacro"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REANUDAR_TRAS_CEO=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --simulacro) MODO="simulacro"; shift ;;
    --de-verdad) MODO="de-verdad"; shift ;;
    --dir) DIR="$2"; shift 2 ;;
    --reanudar-tras-ceo) REANUDAR_TRAS_CEO=1; shift ;;
    *) echo "Argumento no reconocido: $1" >&2; exit 64 ;;
  esac
done

CLAUDE_BIN="${CLAUDE_BIN:-claude}"

CONFIG="$DIR/config.env"
LOCK="$DIR/cadena.lock"
STOPFLAG="$DIR/STOP_CEO.flag"
PARA_CEO="$DIR/PARA-CEO.md"
LOG="$DIR/controlador.log"
DESENLACE="$DIR/DESENLACE.txt"
ESTADO="$DIR/ESTADO.md"
SIMULACRO_SECUENCIA="$DIR/simulacro-secuencia.tsv"

readonly MODO DIR CLAUDE_BIN CONFIG LOCK STOPFLAG PARA_CEO LOG DESENLACE ESTADO SIMULACRO_SECUENCIA

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG" >&2; }
# ^ a stderr a proposito: el stdout de las funciones que lanzan una sesion se
# captura como si fuera su JSON. Si log() escribiera a stdout, se colaria ahi.

escribir_para_ceo() {
  local motivo_llano="$1" detalle_tecnico="$2" codigo_tarea="${3:-'(sin identificar)'}"
  if ! cat > "$PARA_CEO" <<EOF
# La cadena automatica se ha parado — necesita que la mires

**Cuando:** $(date '+%Y-%m-%d %H:%M:%S')
**Tarea relacionada:** ${codigo_tarea}

**Que ha pasado, sin tecnicismos:**
${motivo_llano}

**Que hace falta de ti:**
Mira esta ficha y responde cuando puedas. Mientras no borres o muevas
\`STOP_CEO.flag\`, o vuelvas a lanzar el controlador con
\`--reanudar-tras-ceo\`, la cadena NO continua sola. Eso es a proposito.

---
Detalle tecnico (para quien lo revise despues, no hace falta que lo leas tu):
${detalle_tecnico}
EOF
  then
    echo "ERROR CRITICO: no se pudo escribir $PARA_CEO (permiso denegado o disco lleno)." >&2
    return 1
  fi
  log "Escrito $PARA_CEO"
  return 0
}

parar_en_seco() {
  local motivo_llano="$1" detalle_tecnico="$2" codigo_tarea="${3:-}"
  local fallo_bandera=0 fallo_ficha=0
  if ! touch "$STOPFLAG" 2>/dev/null; then
    echo "ERROR CRITICO: no se pudo crear $STOPFLAG (permiso denegado). NO QUEDA BANDERA EN DISCO." >&2
    fallo_bandera=1
  fi
  if ! escribir_para_ceo "$motivo_llano" "$detalle_tecnico" "$codigo_tarea"; then
    fallo_ficha=1
  fi
  log "PARADA EN SECO. Motivo: $detalle_tecnico"
  if [[ "$fallo_bandera" -ne 0 || "$fallo_ficha" -ne 0 ]]; then
    log "FALLO CRITICO: no se pudo dejar constancia en disco de esta parada. Saliendo con codigo 66."
    exit 66
  fi
}

# ---------------------------------------------------------------------------
# 1. flock: nunca dos cadenas a la vez sobre el mismo DIR.
# ---------------------------------------------------------------------------
exec 9>"$LOCK"
if ! flock -n 9; then
  log "YA HAY UNA CADENA CORRIENDO sobre $DIR (flock ocupado). Esta instancia se para sin tocar nada."
  exit 17
fi

log "=== arranca controlador.sh (PID $$, modo=$MODO, dir=$DIR) ==="

# ---------------------------------------------------------------------------
# 2. Bandera de parada: se comprueba ANTES de tocar nada mas. Nunca se limpia
#    sola; solo --reanudar-tras-ceo (accion humana) la quita.
# ---------------------------------------------------------------------------
if [[ -f "$STOPFLAG" ]]; then
  if [[ "$REANUDAR_TRAS_CEO" -eq 1 ]]; then
    log "STOP_CEO.flag presente, pero se paso --reanudar-tras-ceo (accion humana explicita). Se retira la bandera y se sigue."
    rm -f "$STOPFLAG"
  else
    log "STOP_CEO.flag presente. La cadena NO arranca. Hace falta --reanudar-tras-ceo tras la firma del CEO."
    exit 42
  fi
fi

# ---------------------------------------------------------------------------
# 3. config.env: parseo CAMPO A CAMPO, NUNCA `source`. Lista blanca de CUATRO
#    claves. Cada clave una sola vez, cada valor con su minimo obligatorio.
# ---------------------------------------------------------------------------
if [[ ! -f "$CONFIG" ]]; then
  log "ERROR: no existe $CONFIG. La cadena no arranca sin numeros explicitos."
  exit 2
fi

CONFIG_CLAVES_PERMITIDAS=(MAX_TURNS TIMEOUT_SESION_SEGUNDOS MAX_TAREAS_POR_TIRADA MAX_LINEAS_ESTADO)
RE_ENTERO='^[0-9]+$'
MIN_MAX_TURNS=1
MIN_TIMEOUT_SESION_SEGUNDOS=60
MIN_MAX_TAREAS_POR_TIRADA=1
MIN_MAX_LINEAS_ESTADO=1

declare -A CONFIG_VISTA=()

while IFS= read -r linea || [[ -n "$linea" ]]; do
  linea="$(echo "$linea" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$linea" ]] && continue
  [[ "$linea" == \#* ]] && continue

  if [[ ! "$linea" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
    log "ERROR: linea de $CONFIG que no tiene forma CLAVE=VALOR: '$linea'. La cadena no arranca."
    exit 2
  fi
  clave="${BASH_REMATCH[1]}"
  valor="${BASH_REMATCH[2]}"

  permitida=0
  for k in "${CONFIG_CLAVES_PERMITIDAS[@]}"; do
    [[ "$clave" == "$k" ]] && permitida=1 && break
  done
  if [[ "$permitida" -ne 1 ]]; then
    log "ERROR: $CONFIG define '$clave', que no esta en la lista blanca (${CONFIG_CLAVES_PERMITIDAS[*]}). La cadena no arranca."
    exit 2
  fi

  if [[ -n "${CONFIG_VISTA[$clave]:-}" ]]; then
    log "ERROR: $CONFIG define '$clave' MAS DE UNA VEZ (valores '${CONFIG_VISTA[$clave]}' y '$valor'). La cadena no arranca."
    exit 2
  fi
  CONFIG_VISTA[$clave]="$valor"

  case "$clave" in
    MAX_TURNS)
      if [[ ! "$valor" =~ $RE_ENTERO ]] || [[ "$valor" -lt "$MIN_MAX_TURNS" ]]; then
        log "ERROR: $CONFIG: MAX_TURNS tiene que ser un entero >= ${MIN_MAX_TURNS} ('${valor}' no vale). La cadena no arranca."
        exit 2
      fi
      MAX_TURNS="$valor" ;;
    TIMEOUT_SESION_SEGUNDOS)
      if [[ ! "$valor" =~ $RE_ENTERO ]] || [[ "$valor" -lt "$MIN_TIMEOUT_SESION_SEGUNDOS" ]]; then
        log "ERROR: $CONFIG: TIMEOUT_SESION_SEGUNDOS tiene que ser un entero >= ${MIN_TIMEOUT_SESION_SEGUNDOS} ('${valor}' no vale: con 0, GNU 'timeout' desactiva el limite entero). La cadena no arranca."
        exit 2
      fi
      TIMEOUT_SESION_SEGUNDOS="$valor" ;;
    MAX_TAREAS_POR_TIRADA)
      if [[ ! "$valor" =~ $RE_ENTERO ]] || [[ "$valor" -lt "$MIN_MAX_TAREAS_POR_TIRADA" ]]; then
        log "ERROR: $CONFIG: MAX_TAREAS_POR_TIRADA tiene que ser un entero >= ${MIN_MAX_TAREAS_POR_TIRADA} ('${valor}' no vale). La cadena no arranca."
        exit 2
      fi
      MAX_TAREAS_POR_TIRADA="$valor" ;;
    MAX_LINEAS_ESTADO)
      if [[ ! "$valor" =~ $RE_ENTERO ]] || [[ "$valor" -lt "$MIN_MAX_LINEAS_ESTADO" ]]; then
        log "ERROR: $CONFIG: MAX_LINEAS_ESTADO tiene que ser un entero >= ${MIN_MAX_LINEAS_ESTADO} ('${valor}' no vale). La cadena no arranca."
        exit 2
      fi
      MAX_LINEAS_ESTADO="$valor" ;;
  esac
done < "$CONFIG"

for var in MAX_TURNS TIMEOUT_SESION_SEGUNDOS MAX_TAREAS_POR_TIRADA MAX_LINEAS_ESTADO; do
  if [[ -z "${!var:-}" ]]; then
    log "ERROR: $CONFIG no define $var. La cadena no arranca."
    exit 2
  fi
done

# ---------------------------------------------------------------------------
# 4. En modo --de-verdad, comprobar ANTES de lanzar nada que el binario de
#    Claude Code se puede encontrar y ejecutar.
# ---------------------------------------------------------------------------
if [[ "$MODO" == "de-verdad" ]]; then
  if ! command -v -- "$CLAUDE_BIN" >/dev/null 2>&1 && [[ ! -x "$CLAUDE_BIN" ]]; then
    parar_en_seco \
      "No encuentro el programa de Claude Code en esta maquina (CLAUDE_BIN='${CLAUDE_BIN}'). No se ha lanzado ninguna sesion, no se ha gastado nada." \
      "command -v y -x fallaron los dos para CLAUDE_BIN='${CLAUDE_BIN}'." \
      ""
    exit 11
  fi
fi

# ---------------------------------------------------------------------------
# 5. Lanzar UNA sesion: en simulacro, sin tocar Claude para nada; de verdad,
#    UNA sesion nueva de `claude -p` ejecutando /autonomo.
# ---------------------------------------------------------------------------
ejecutar_sesion_simulacro() {
  local n="$1"
  local linea is_error_sim desenlace_sim codigo_sim estado_sim
  linea=""
  if [[ -f "$SIMULACRO_SECUENCIA" ]]; then
    linea=$(awk -F'\t' -v n="$n" '$1==n{print; exit}' "$SIMULACRO_SECUENCIA")
  fi
  if [[ -z "$linea" ]]; then
    is_error_sim="false"; desenlace_sim="CERRADA"; codigo_sim="00.00.$(printf '%02d' "$n")"; estado_sim="ok"
  else
    is_error_sim=$(echo "$linea" | cut -f2)
    desenlace_sim=$(echo "$linea" | cut -f3)
    codigo_sim=$(echo "$linea" | cut -f4)
    # 5a campo, opcional: como se comporta ESTADO.md en esta sesion simulada.
    # "ok" (por defecto si falta el campo) = lo escribe bien; "AUSENTE" = no lo
    # toca; "LARGO" = lo escribe con muchas mas lineas que MAX_LINEAS_ESTADO.
    estado_sim=$(echo "$linea" | cut -f5)
    [[ -z "$estado_sim" ]] && estado_sim="ok"
  fi
  log "  [SIMULACRO sesion #$n] is_error=$is_error_sim desenlace=$desenlace_sim codigo=$codigo_sim estado=$estado_sim"

  # Imita lo que haria una sesion real escribiendo DESENLACE.txt, SALVO si el
  # valor es literalmente "AUSENTE": eso simula una sesion que se olvido de
  # escribirlo (para probar el fallo cerrado por defecto).
  if [[ "$desenlace_sim" != "AUSENTE" ]]; then
    { echo "$desenlace_sim"; echo "$codigo_sim"; } > "$DESENLACE" 2>/dev/null \
      || log "AVISO (simulacro): no se pudo escribir $DESENLACE"
  fi

  case "$estado_sim" in
    ok) echo "resumen corto de mentira para la prueba" > "$ESTADO" 2>/dev/null \
          || log "AVISO (simulacro): no se pudo escribir $ESTADO" ;;
    AUSENTE) : ;;  # no se toca ESTADO.md, para probar el fallo cerrado
    LARGO) seq 1 "$((MAX_LINEAS_ESTADO + 50))" > "$ESTADO" 2>/dev/null \
             || log "AVISO (simulacro): no se pudo escribir $ESTADO" ;;
  esac

  echo '{"is_error":'"$is_error_sim"',"terminal_reason":"completed","subtype":"success","num_turns":3,"permission_denials":[]}'
}

ejecutar_sesion_de_verdad() {
  local prompt
  prompt="Sigue el flujo de .claude/commands/autonomo.md de principio a fin. Nadie va a leer esta conversacion esta noche. Antes de nada, si existe \"${ESTADO}\", leelo: es el resumen corto de en que quedo la ultima tirada. Al terminar, pase lo que pase: (1) sobreescribe \"${ESTADO}\" con un resumen CORTO, de como maximo ${MAX_LINEAS_ESTADO} lineas, de que tarea trabajaste, con que desenlace, que queda pendiente, y que se rechazo y por que -- si se pierde el 'por que', la siguiente sesion decide peor; (2) escribe \"${DESENLACE}\" con EXACTAMENTE una de estas tres palabras en la primera linea y nada mas en esa linea: CERRADA (el orquestador dijo CERRAR), ESCALADA (dijo ESCALAR, o aparecio una excepcion inmediata de CLAUDE.md), o BLOQUEADA (te quedaste sin poder avanzar); en la segunda linea, solo el codigo WBS de la tarea trabajada, con el formato exacto NN.NN.NN. (3) si el desenlace es ESCALADA o BLOQUEADA, ademas prepara \"${PARA_CEO}\" con la ficha para el CEO en el formato habitual del proyecto (una linea de que se decide, 2-4 opciones cerradas, la recomendada con motivo, que bloquea, respuesta de una letra)."

  # "exec 9>&-" cierra DE VERDAD el descriptor del flock (fd 9) en esta funcion
  # (que corre en el subshell creado por `$(...)` al llamarla), para que un
  # `kill -9` sobre el controlador mientras esta sesion sigue viva no deje el
  # flock retenido por un hijo huerfano. OJO: "9>&-" como redireccion al final
  # del comando `timeout ...` NO basta (bash duplica el descriptor a otro
  # numero al aplicar un cierre a una funcion, no lo cierra de verdad); tiene
  # que ser `exec 9>&-` como instruccion propia, la primera de la funcion
  # (verificado con /proc/<pid>/fd).
  exec 9>&- 2>/dev/null

  timeout "${TIMEOUT_SESION_SEGUNDOS}s" "$CLAUDE_BIN" -p "$prompt" \
    --output-format json \
    --max-turns "$MAX_TURNS"
  local codigo_salida=$?
  if [[ "$codigo_salida" -eq 124 ]]; then
    log "AVISO: la sesion no termino en ${TIMEOUT_SESION_SEGUNDOS}s y 'timeout' la mato."
  fi
  return 0
}

# ---------------------------------------------------------------------------
# 6. Bucle principal
# ---------------------------------------------------------------------------
# El formato del codigo WBS SIGUE VALIDANDOSE (se movio: antes protegia contra
# inyeccion de prompt via cola.txt, que ya no existe porque el controlador no
# elige tareas; ahora protege la segunda linea de DESENLACE.txt). Un codigo mal
# formado PARA la cadena igual que un desenlace invalido -- si una sesion no
# sabe decir que tarea hizo, no es una sesion cerrada (hallazgo de
# critico-codigo, reproducido: antes solo se marcaba "no reconocible" en el
# log/ficha y la cadena seguia igual).
RE_CODIGO_WBS='^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'

TAREAS_HECHAS=0

while true; do
  # 6a. bandera de parada: puede haberla puesto el propio controlador en una
  #     vuelta anterior de este mismo bucle, o un humano a mano mientras corria.
  if [[ -f "$STOPFLAG" ]]; then
    log "STOP_CEO.flag presente. No se lanza otra sesion. Cadena parada."
    exit 42
  fi

  # 6b. tope de tareas por tirada: parada LIMPIA, no requiere firma del CEO
  #     (no es una anomalia, es el tamaño de lote configurado).
  if [[ "$TAREAS_HECHAS" -ge "$MAX_TAREAS_POR_TIRADA" ]]; then
    log "=== tope de $MAX_TAREAS_POR_TIRADA tareas alcanzado en esta tirada. Para limpio. ==="
    exit 20
  fi

  # limpia el desenlace de una vuelta anterior ANTES de lanzar, para que
  # "ausente tras la sesion" signifique de verdad que ESTA sesion no lo escribio.
  # ESTADO.md NO se borra (es un traspaso que tiene que sobrevivir si la sesion
  # se cae antes de reescribirlo): en su lugar se guarda la hora de ANTES de
  # lanzar, para comprobar despues si de verdad se toco EN ESTA sesion (si no,
  # seria un resto de una sesion anterior, no un traspaso real -- ver 6d).
  rm -f "$DESENLACE"
  marca_antes_sesion=$(date +%s)

  log "lanzando sesion nueva (numero $((TAREAS_HECHAS + 1)) de esta tirada, tope $MAX_TAREAS_POR_TIRADA)"

  if [[ "$MODO" == "simulacro" ]]; then
    salida_json="$(ejecutar_sesion_simulacro "$((TAREAS_HECHAS + 1))")"
  else
    salida_json="$(ejecutar_sesion_de_verdad)"
  fi

  # "echo '' | jq empty" sale con codigo 0 (input vacio no es un error para
  # jq), asi que se comprueba el vacio aparte, no solo "jq empty".
  if [[ -z "$salida_json" ]] || ! echo "$salida_json" | jq empty 2>/dev/null; then
    parar_en_seco \
      "La sesion no devolvio una respuesta que se pueda leer (algo se rompio a nivel tecnico -- puede ser que se colgara y se cortara sola -- no es un rechazo del trabajo)." \
      "salida de claude -p vacia o no es JSON valido: '$(echo "$salida_json" | head -c 300)'" \
      ""
    exit 6
  fi

  is_error=$(echo "$salida_json" | jq -r '.is_error')
  terminal_reason=$(echo "$salida_json" | jq -r '.terminal_reason')
  subtype=$(echo "$salida_json" | jq -r '.subtype')
  num_turns=$(echo "$salida_json" | jq -r '.num_turns // 0')
  denials=$(echo "$salida_json" | jq -r '.permission_denials | length')

  log "sesion: is_error=$is_error terminal_reason=$terminal_reason subtype=$subtype turnos=${num_turns} denegaciones=${denials}"

  # fallo tecnico de sesion (crash, max-turns, etc.): "false" exacto o para.
  # jq -r '.is_error' sobre un campo ausente devuelve la cadena "null", no
  # vacio y no "true" -- por eso se compara con != "false", no == "true".
  if [[ "$is_error" != "false" ]]; then
    parar_en_seco \
      "La sesion no llego a terminar limpiamente (motivo tecnico: ${terminal_reason} / ${subtype} / is_error=${is_error})." \
      "is_error='${is_error}' terminal_reason=${terminal_reason} subtype=${subtype}" \
      ""
    exit 7
  fi

  # 6c. ESTADO.md: COMPROBACION MECANICA (hallazgo de critico-codigo,
  #     reproducido: antes el guion solo se lo PEDIA a la sesion dentro del
  #     texto del prompt -- prosa pura, nunca comprobado. Una sesion que
  #     cerraba con DESENLACE.txt=CERRADA pero sin tocar ESTADO.md dejaba
  #     que la cadena siguiera igual, y la siguiente sesion arrancaba a
  #     ciegas, que es justo el problema que este guion existe para evitar).
  #     Tres cosas se comprueban: que existe y no esta vacio, que se
  #     actualizo DURANTE esta sesion (mtime >= marca_antes_sesion -- si no,
  #     es un resto de una sesion anterior, no un traspaso real), y que no
  #     se paso del tope de lineas.
  #
  #     "-L" en el stat (hallazgo de critico-codigo, reproducido dentro del
  #     guion completo): sin dereferenciar, si ESTADO.md es un symlink, el
  #     mtime que se lee es el del ENLACE (fijado al crearlo), no el del
  #     fichero real que la sesion reescribe -- falso positivo determinista,
  #     paraba diciendo "no actualizado" con un traspaso que si era real.
  #
  #     "-f" (no solo "-s"): hallazgo de critico-codigo, reproducido 5 de 5.
  #     "-s" solo mira el TAMAÑO, y un symlink a un DIRECTORIO con actividad
  #     tiene tamaño > 0 casi siempre, asi que "[[ ! -s ... ]]" lo dejaba pasar
  #     como si fuera un traspaso real -- sin ni un byte de contenido de
  #     verdad. Encima "wc -l < directorio" imprime "0" en stdout (el error va
  #     a stderr), que es un entero valido, asi que la guarda de mas abajo
  #     tampoco lo pillaba: "0 -gt 100" es falso, y la cadena seguia como
  #     CERRADA. "-f" exige ademas que sea un FICHERO REGULAR (siguiendo
  #     symlinks), que un directorio nunca es. El chequeo de PARA_CEO de mas
  #     abajo ya usaba "-f" y por eso nunca tuvo este agujero.
  if [[ ! -f "$ESTADO" ]]; then
    parar_en_seco \
      "La sesion no dejo un fichero de verdad con el resumen que la siguiente sesion necesita (falta, o es un directorio/enlace roto en vez de un fichero). Por seguridad, se para." \
      "ESTADO.md no es un fichero regular (comprobado con -f, siguiendo symlinks)" \
      ""
    exit 14
  fi
  estado_mtime=$(stat -L -c %Y "$ESTADO" 2>/dev/null || echo 0)
  if [[ ! -s "$ESTADO" ]] || [[ "$estado_mtime" -lt "$marca_antes_sesion" ]]; then
    parar_en_seco \
      "La sesion no dejo (o no actualizo) el resumen corto que la siguiente sesion necesita para no arrancar a ciegas. Por seguridad, se para: sin ese resumen, seguir seria justo el problema que este guion existe para evitar." \
      "ESTADO.md ausente, vacio, o no actualizado en esta sesion (mtime=${estado_mtime}, sesion lanzada en ${marca_antes_sesion})" \
      ""
    exit 14
  fi
  # "wc -l < fichero" seguido de una comparacion numerica FALLA ABIERTO si el
  # fichero desaparece justo entre el chequeo de arriba y este (carrera de
  # microsegundos): $lineas_estado queda vacio, "[[ '' -gt N ]]" no aborta el
  # guion, solo devuelve falso en silencio, y el chequeo de longitud se salta
  # entero (hallazgo de critico-codigo). Igual que ya se hace con los numeros
  # de config.env: si no es un entero valido, PARA -- nunca "sigue porque la
  # comparacion dio falso".
  lineas_estado=$(wc -l < "$ESTADO" 2>/dev/null)
  if [[ ! "$lineas_estado" =~ $RE_ENTERO ]]; then
    parar_en_seco \
      "No se pudo medir el resumen que la sesion dejo para la siguiente (puede haber desaparecido justo despues de escribirse). Por seguridad, se para en vez de asumir que esta bien." \
      "wc -l sobre ESTADO.md no devolvio un numero valido: '${lineas_estado}'" \
      ""
    exit 14
  fi
  if [[ "$lineas_estado" -gt "$MAX_LINEAS_ESTADO" ]]; then
    parar_en_seco \
      "El resumen que cada sesion deja para la siguiente se ha hecho demasiado largo (${lineas_estado} lineas, tope ${MAX_LINEAS_ESTADO}). Un traspaso que crece sin freno es el mismo problema de contexto acumulado que este guion existe para evitar." \
      "ESTADO.md tiene ${lineas_estado} lineas, por encima de MAX_LINEAS_ESTADO=${MAX_LINEAS_ESTADO}" \
      ""
    exit 14
  fi

  # 6d. Desenlace: la mecanica que sustituye a toda la gobernanza que se
  #     quito. Fichero ausente, no regular, o vacio -> PARA.
  #     "-f" ademas de "-s" (repaso pedido junto con el arreglo de ESTADO.md):
  #     aqui NO habia agujero explotable -- si DESENLACE.txt fuera un
  #     directorio, "sed -n '1p'" mas abajo falla y devuelve cadena vacia, que
  #     la validacion de contenido (linea 1 tiene que ser EXACTAMENTE CERRADA/
  #     ESCALADA/BLOQUEADA) ya rechaza -- pero se endurece igual, por
  #     consistencia con ESTADO.md y para no depender de esa red de mas abajo.
  if [[ ! -f "$DESENLACE" ]] || [[ ! -s "$DESENLACE" ]]; then
    parar_en_seco \
      "La sesion termino sin decir claramente como quedo la tarea (no dejo escrito si cerro, escalo o se bloqueo). Por seguridad, se para." \
      "DESENLACE.txt ausente, no es un fichero regular, o esta vacio tras la sesion" \
      ""
    exit 12
  fi

  desenlace_valor="$(sed -n '1p' "$DESENLACE" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  codigo_tarea_bruto="$(sed -n '2p' "$DESENLACE" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

  # Desenlace valido = linea 1 es EXACTAMENTE una de las tres palabras Y linea
  # 2 cumple el formato de codigo WBS. Si CUALQUIERA de las dos falla, se
  # trata igual que cualquier otro desenlace invalido: PARA. Antes, un codigo
  # mal formado en la linea 2 solo se marcaba "no reconocible" y la cadena
  # seguia -- eso contradecia el lema de la pieza ("falla cerrado, nunca sigue
  # por defecto"). Corregido tras el segundo ataque de critico-codigo.
  desenlace_reconocido=0
  case "$desenlace_valor" in
    CERRADA|ESCALADA|BLOQUEADA) desenlace_reconocido=1 ;;
  esac
  codigo_reconocido=0
  [[ "$codigo_tarea_bruto" =~ $RE_CODIGO_WBS ]] && codigo_reconocido=1

  if [[ "$desenlace_reconocido" -ne 1 || "$codigo_reconocido" -ne 1 ]]; then
    parar_en_seco \
      "La sesion dejo escrito algo que no se puede interpretar con seguridad (desenlace: '${desenlace_valor}', codigo de tarea: '${codigo_tarea_bruto}'). Si una sesion no sabe decir con claridad que tarea hizo y como quedo, no se considera una sesion cerrada. Por seguridad, se para en vez de adivinar." \
      "DESENLACE.txt: linea1='${desenlace_valor}' (reconocida=${desenlace_reconocido}), linea2='${codigo_tarea_bruto}' (formato de codigo WBS valido=${codigo_reconocido})" \
      "${codigo_tarea_bruto}"
    exit 12
  fi

  case "$desenlace_valor" in
    CERRADA)
      TAREAS_HECHAS=$((TAREAS_HECHAS + 1))
      log "sesion CERRADA (tarea: ${codigo_tarea_bruto}). Van ${TAREAS_HECHAS}/${MAX_TAREAS_POR_TIRADA} esta tirada."
      ;;
    ESCALADA|BLOQUEADA)
      log "sesion ${desenlace_valor} (tarea: ${codigo_tarea_bruto}). Se detiene la cadena."
      fallo_bandera=0
      if ! touch "$STOPFLAG" 2>/dev/null; then
        echo "ERROR CRITICO: no se pudo crear $STOPFLAG (permiso denegado). NO QUEDA BANDERA EN DISCO." >&2
        fallo_bandera=1
      fi
      # si la sesion ya dejo su propia PARA-CEO.md fresca (actualizada EN esta
      # sesion, no un resto de una anterior), no se sobreescribe; si no, se
      # deja una de repuesto para que el CEO no se quede sin nada que leer.
      # "-L" por el mismo motivo que en ESTADO.md: sin dereferenciar, un
      # symlink daria el mtime del enlace, no el del fichero real.
      fallo_ficha=0
      para_ceo_mtime=$(stat -L -c %Y "$PARA_CEO" 2>/dev/null || echo 0)
      if [[ ! -f "$PARA_CEO" ]] || [[ "$para_ceo_mtime" -lt "$marca_antes_sesion" ]]; then
        if ! escribir_para_ceo \
          "La sesion que trabajaba en ${codigo_tarea_bruto} decidio que hacia falta tu firma (desenlace: ${desenlace_valor}) y paro la cadena." \
          "DESENLACE.txt = ${desenlace_valor}" \
          "$codigo_tarea_bruto"
        then
          fallo_ficha=1
        fi
      fi
      # mismo criterio que parar_en_seco (F3): si no se pudo dejar constancia
      # en disco de la parada, salida ruidosa y distinta, nunca seguir como
      # si no hubiera pasado nada.
      if [[ "$fallo_bandera" -ne 0 || "$fallo_ficha" -ne 0 ]]; then
        log "FALLO CRITICO: no se pudo dejar constancia en disco de esta parada. Saliendo con codigo 66."
        exit 66
      fi
      exit 42
      ;;
  esac
done
