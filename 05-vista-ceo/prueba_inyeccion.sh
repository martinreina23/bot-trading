#!/usr/bin/env bash
# Regla 25: un verificador que nunca ha fallado no esta verificado.
# Le mete al verificador cinco WBS rotos y comprueba que los caza TODOS.
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

# 3. tarea nueva en el WBS que el Excel todavia no tiene
awk '/^\| 07\.01\.02 /{print; print "| 07.01.03 | Tarea inventada | Constructores | 03.01.01 | pendiente |"; next} {print}' "$WBS" > "$TMP/w3.md"
probar "tarea que falta en el Excel" "$TMP/w3.md" "censo"

# 4. dependencia hacia una tarea que no existe
awk '{gsub(/\| 03\.01\.01, 01\.02\.01 \|/, "| 09.99.99 |"); print}' "$WBS" > "$TMP/w4.md"
probar "dependencia fantasma" "$TMP/w4.md" "dependencias existen"

# 5. dependencia circular
awk '{if ($0 ~ /^\| 03\.01\.01 /) gsub(/\| 01\.01\.01 \|/, "| 03.01.02 |"); print}' "$WBS" > "$TMP/w5.md"
probar "ciclo de dependencias" "$TMP/w5.md" "ciclos"

echo "  --"
if $PY 05-vista-ceo/verificar_excel.py >/dev/null 2>&1; then
  echo "  OK       el WBS real pasa la verificacion completa"
else
  echo "  MAL      el WBS real NO pasa la verificacion: mirala antes de seguir"
  fallos=$((fallos + 1))
fi

[ $fallos -eq 0 ] && echo "RESULTADO: el verificador muerde en los 5 casos." || echo "RESULTADO: $fallos problemas."
exit $fallos
