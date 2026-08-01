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
  out=$($PY 05-vista-ceo/verificar_excel.py "$2" "$TMP/copia.xlsx" 2>&1); rc=$?
  if [ $rc -ne 0 ] && echo "$out" | grep -q "FALLO  $3"; then
    echo "  CAZADO   $1"
  else
    echo "  ESCAPA   $1  (codigo $rc) <-- EL VERIFICADOR NO DETECTA ESTO"
    fallos=$((fallos + 1))
  fi
}

echo "PRUEBA DE INYECCION DEL VERIFICADOR"

# 1. una tarea hecha que el WBS pasa a pendiente: el Excel se queda desfasado
sed 's#| \*\*hecha\*\* 31/07 — `coste_swap.md`#| pendiente — texto cambiado a proposito#' "$WBS" > "$TMP/w1.md"
probar "estado distinto del Excel" "$TMP/w1.md" "estados"

# 2. celda de estado que no declara estado (el fallo real del 31/07/2026)
sed 's#| \*\*hecha\*\* 30/07 — `INFORME_GB2.md` |#| FICHA (31/07): entregado, ver carpeta |#' "$WBS" > "$TMP/w2.md"
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
