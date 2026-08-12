#!/usr/bin/env bash
# Regla 25: un verificador que nunca ha fallado no esta verificado.
# Le mete al verificador siete fixtures rotos (cinco WBS, una LECCIONES.md y una marca de
# estado descolocada) y comprueba que los caza TODOS.
# No toca ningun fichero del proyecto: trabaja sobre copias en un temporal.
#
# Uso:  bash 05-vista-ceo/prueba_inyeccion.sh
# Sale con codigo 1 si alguna inyeccion se le escapa.

set -u
cd "$(dirname "$0")/.." || exit 1
PY=.venv/bin/python
WBS=00-direccion/WBS.md
XLSX=05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fallos=0

[ -x "$PY" ] || { echo "falta $PY: crea el entorno con python3 -m venv .venv"; exit 1; }
[ -f "$XLSX" ] || { echo "falta el Excel: ejecuta antes generar_excel.py"; exit 1; }
cp "$XLSX" "$TMP/copia.xlsx"

probar_argv () {  # $1 nombre  $2 fuente buena  $3 fuente rota  $4 prueba que DEBE fallar  -- resto: argv para verificar_excel.py
  # Version generalizada de "probar" (tarea 03.01.16): las pruebas 6 y 7 no rompen el
  # WBS, rompen LECCIONES.md o insertan una marca de estado descolocada, y necesitan
  # pasarle a verificar_excel.py mas rutas que WBS+XLSX. Mismo guardia FIXTURE que abajo
  # (L-026): si la inyeccion no cambio nada, el roto es el test, no el verificador.
  local nombre="$1" buena="$2" rota="$3" prueba="$4"; shift 4
  if cmp -s "$buena" "$rota"; then
    echo "  FIXTURE  $nombre  <-- LA INYECCION NO CAMBIO NADA: el roto es el test, no el verificador"
    fallos=$((fallos + 1)); return
  fi
  out=$($PY 05-vista-ceo/verificar_excel.py "$@" 2>&1); rc=$?
  if [ $rc -ne 0 ] && echo "$out" | grep -q "FALLO  $prueba"; then
    echo "  CAZADO   $nombre"
  else
    echo "  ESCAPA   $nombre  (codigo $rc) <-- EL VERIFICADOR NO DETECTA ESTO"
    fallos=$((fallos + 1))
  fi
}

probar () {  # $1 nombre  $2 wbs roto  $3 prueba que DEBE fallar
  # Guardia anadido el 03/08/2026: una inyeccion que no cambia nada NO es una
  # inyeccion. Antes, si el texto que buscaba el sed dejaba de existir en el WBS,
  # el fichero "roto" salia identico al real, el verificador pasaba, y el script
  # acusaba al VERIFICADOR de estar ciego. Es lo que llevaba pasando con el caso 2
  # desde que la celda de 01.02.01 se amplio el 02/08. Un test que miente sobre
  # quien falla es peor que no tenerlo (L-009, L-016).
  if cmp -s "$WBS" "$2"; then
    echo "  FIXTURE  $1  <-- LA INYECCION NO CAMBIO NADA: el roto es el test, no el verificador"
    fallos=$((fallos + 1)); return
  fi
  out=$($PY 05-vista-ceo/verificar_excel.py "$2" "$TMP/copia.xlsx" 2>&1); rc=$?
  if [ $rc -ne 0 ] && echo "$out" | grep -q "FALLO  $3"; then
    echo "  CAZADO   $1"
  else
    echo "  ESCAPA   $1  (codigo $rc) <-- EL VERIFICADOR NO DETECTA ESTO"
    fallos=$((fallos + 1))
  fi
}

echo "PRUEBA DE INYECCION DEL VERIFICADOR"

# Casos 1 y 2: se localiza la victima por ESTRUCTURA (primera fila de tarea cuya
# celda ESTADO declara **hecha**), no por su prosa. Asi no vuelven a caducar cada
# vez que alguien amplia una celda del WBS.
$PY - "$WBS" "$TMP/w1.md" "$TMP/w2.md" <<'PY'
import re, sys
wbs, o1, o2 = sys.argv[1], sys.argv[2], sys.argv[3]
lineas = open(wbs, encoding="utf-8").read().split("\n")
victima = next(i for i, l in enumerate(lineas)
               if re.match(r"^\| \d\d\.\d\d\.\d\d ", l) and "**hecha**" in l.split("|")[5])

# 1. una tarea hecha que el WBS pasa a pendiente: el Excel se queda desfasado
c = lineas[victima].split("|")
c1 = list(c); c1[5] = " pendiente — estado cambiado a proposito por la prueba de inyeccion "
open(o1, "w", encoding="utf-8").write("\n".join(lineas[:victima] + ["|".join(c1)] + lineas[victima+1:]))

# 2. celda de estado que no declara ningun estado (el fallo real del 31/07/2026)
c2 = list(c)
c2[5] = " FICHA (prueba de inyeccion): entregado, ver carpeta "
open(o2, "w", encoding="utf-8").write("\n".join(lineas[:victima] + ["|".join(c2)] + lineas[victima+1:]))
print(f"  (inyectando sobre la tarea {c[1].strip()})")
PY
probar "estado distinto del Excel" "$TMP/w1.md" "estados"
probar "estado sin declarar" "$TMP/w2.md" "estado declarado"

# 3. tarea nueva en el WBS que el Excel todavia no tiene.
# El codigo inyectado se ELIGE COMPROBANDO QUE NO EXISTE, no se escribe a mano. Antes
# estaba fijo a "07.01.03", y esa tarea acabo existiendo de verdad: la inyeccion dejo de
# ser una tarea nueva y paso a ser un duplicado, que el censo no mira. El caso seguia
# diciendo CAZADO porque el Excel llevaba semanas desfasado y el grep de "FALLO  censo"
# encontraba OTRO fallo de censo, no el inyectado. Un test que aprueba por un fallo
# distinto del que prueba es un test que miente (L-009, L-016). Detectado el 12/08/2026
# al regenerar el Excel: con el censo limpio, el caso 3 se destapo como ESCAPA.
$PY - "$WBS" "$TMP/w3.md" <<'PY'
import re, sys
wbs, destino = sys.argv[1], sys.argv[2]
lineas = open(wbs, encoding="utf-8").read().split("\n")
existentes = {m.group(1) for l in lineas
              if (m := re.match(r"^\| (\d\d\.\d\d\.\d\d) ", l))}
libre = next(f"07.{g:02d}.{n:02d}" for g in range(90, 100) for n in range(90, 100)
             if f"07.{g:02d}.{n:02d}" not in existentes)
ancla = next(i for i, l in enumerate(lineas) if re.match(r"^\| 07\.\d\d\.\d\d ", l))
fila = f"| {libre} | Tarea inventada | Constructores | 03.01.01 | pendiente |"
open(destino, "w", encoding="utf-8").write(
    "\n".join(lineas[:ancla + 1] + [fila] + lineas[ancla + 1:]))
print(f"  (inyectando la tarea {libre}, comprobado que no existe en el WBS)")
PY
probar "tarea que falta en el Excel" "$TMP/w3.md" "censo"

# 4. dependencia hacia una tarea que no existe
awk '{gsub(/\| 03\.01\.01, 01\.02\.01 \|/, "| 09.99.99 |"); print}' "$WBS" > "$TMP/w4.md"
probar "dependencia fantasma" "$TMP/w4.md" "dependencias existen"

# 5. dependencia circular
awk '{if ($0 ~ /^\| 03\.01\.01 /) gsub(/\| 01\.01\.01 \|/, "| 03.01.02 |"); print}' "$WBS" > "$TMP/w5.md"
probar "ciclo de dependencias" "$TMP/w5.md" "ciclos"

# 6. tarea 03.01.16(c): una leccion NUEVA en LECCIONES.md, sin tocar el WBS ni el Excel,
# tiene que hacer caer el recuento de la hoja LECCIONES. Se localiza el ID mas alto por
# ESTRUCTURA (no se copia la prosa de ninguna leccion real) y se anade uno consecutivo.
LECCIONES=00-direccion/LECCIONES.md
$PY - "$LECCIONES" "$TMP/lecciones_rota.md" <<'PY'
import re, sys
from datetime import date
origen, destino = sys.argv[1], sys.argv[2]
texto = open(origen, encoding="utf-8").read()
ultimo = max(int(n) for n in re.findall(r"^## L-(\d+) ", texto, flags=re.M))
nuevo = ultimo + 1
bloque = (f"\n## L-{nuevo:03d} · Lección inyectada por prueba_inyeccion.sh (fixture, no real)\n"
          f"**Causa raiz:** fixture de la prueba de inyección de la tarea 03.01.16, no una lección real.\n"
          f"**Regla:** ninguna: existe solo para comprobar que el recuento de la hoja LECCIONES cae.\n"
          f"**Evento:** {date.today().isoformat()}, prueba_inyeccion.sh, caso 6.\n")
open(destino, "w", encoding="utf-8").write(texto + bloque)
print(f"  (inyectando L-{nuevo:03d} sobre una copia de LECCIONES.md; {ultimo} lecciones reales ahora mismo)")
PY
probar_argv "lección nueva sin tocar el Excel (recuento)" "$LECCIONES" "$TMP/lecciones_rota.md" "hoja LECCIONES" \
  "$WBS" "$TMP/copia.xlsx" "CLAUDE.md" "$TMP/lecciones_rota.md" "00-direccion/DECISIONES.md"

# 7. tarea 03.01.16(e): una marca de estado en negrita insertada EN MEDIO de una celda
# real (ni cierra una transición -no la precede un guion-, ni abre la celda, ni va
# citada entre comillas invertidas) tiene que hacer caer la prueba de POSICIÓN. Se
# inserta 40 caracteres ANTES de la marca real de cierre (misma tarea que los casos 1-2,
# localizada por estructura) para que el ESTADO que se lee siga siendo el correcto: la
# marca en medio no falsea el estado, solo descoloca FICHA/RESULTADO (03.01.16).
$PY - "$WBS" "$TMP/w7.md" <<'PY'
import re, sys
wbs, destino = sys.argv[1], sys.argv[2]
lineas = open(wbs, encoding="utf-8").read().split("\n")
victima = next(i for i, l in enumerate(lineas)
               if re.match(r"^\| \d\d\.\d\d\.\d\d ", l) and "**hecha**" in l.split("|")[5])
celdas = lineas[victima].split("|")
estado = celdas[5]
ultima_marca = list(re.finditer(r"\*\*(pendiente|en_curso|hecha|bloqueada)\*\*", estado, flags=re.I))[-1]
punto = max(0, ultima_marca.start() - 40)
corte = estado.rfind(" ", 0, punto) if punto > 0 else 0
if corte < 0:
    corte = 0
inyectado = (estado[:corte]
             + " nota suelta con **pendiente** sin guion delante, en medio de la ficha,"
             + estado[corte:])
celdas[5] = inyectado
lineas[victima] = "|".join(celdas)
open(destino, "w", encoding="utf-8").write("\n".join(lineas))
print(f"  (inyectando sobre la tarea {celdas[1].strip()}, 40 caracteres antes de su marca real "
      f"en posición {ultima_marca.start()})")
PY
probar_argv "estado en medio de la celda (posición)" "$WBS" "$TMP/w7.md" "posición del estado" \
  "$TMP/w7.md" "$TMP/copia.xlsx"

echo "  --"
if $PY 05-vista-ceo/verificar_excel.py >/dev/null 2>&1; then
  echo "  OK       el WBS real pasa la verificacion completa"
else
  echo "  MAL      el WBS real NO pasa la verificacion: mirala antes de seguir"
  fallos=$((fallos + 1))
fi

[ $fallos -eq 0 ] && echo "RESULTADO: el verificador muerde en los 7 casos." || echo "RESULTADO: $fallos problemas."
exit $fallos
