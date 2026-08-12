# MEDICIÓN DE LA CIRUGÍA DEL MOTOR

Medida por ejecución, con los comandos literales del encargo, antes y después de operar.
No se copian cifras del encargo: todas las de aquí están reproducidas en esta máquina.

---

## ANTES — 12/08/2026, commit `89cdf08`

### Los números del encargo NO cuadraban. Éstos son los reales.

| Medida | El encargo decía | Medido de verdad |
|---|---|---|
| Tamaño de `WBS.md` | 149.829 bytes | **168.317 bytes** |
| Tareas en el WBS | 66 | **67** |
| Reglas en `CLAUDE.md` | 29 | **30** (la 30 entró en el commit `89cdf08`) |
| Tareas `NUEVA` | 16 | **17** |
| ...de ellas, de motor | 13 | **13** ✓ (única cifra que coincide) |

El encargo se escribió antes del commit `89cdf08`, que añadió la regla 30 y engordó el WBS.
**A partir de aquí se usan las cifras medidas, no las del encargo.**

### Bytes de lectura obligatoria del orquestador

```
 14134 CLAUDE.md
168317 00-direccion/WBS.md
 41945 00-direccion/LECCIONES.md
 50905 00-direccion/DECISIONES.md
275301 total
```

### Tareas y estados

```
67   filas de tarea
10   **en_curso**
28   **hecha**
12   **pendiente**
 0   **bloqueada**
```

Suman 50 marcas en 67 celdas. **17 celdas de tarea no declaran estado en negrita.**
Lo confirma la prueba 10 del verificador: *"50 marcas revisadas en 67 celdas"*.

### Reparto producto/motor (fases 02/04/05/06 = producto; 03/07 = motor)

```
filas de tarea: 67
PRODUCTO: 33 tareas, 44,642 bytes
MOTOR:    28 tareas, 74,211 bytes
motor = 45.9% tareas, 62.4% texto
celda mediana: 930 car. · celda mayor: 10471 car. (03.01.13)
```

El motor es el 45,9% de las tareas y se come el **62,4% del texto** del WBS.

### Tareas `NUEVA` nacidas a mitad de camino

```
nuevas: 17 · de ellas motor: 13
['01.02.04', '03.01.11', '03.01.12', '03.01.13', '03.01.14', '03.01.15',
 '03.01.18', '03.01.19', '03.01.20', '03.01.24', '03.01.25',
 '07.01.01', '07.01.03']
```

### Estado de las pruebas ANTES de tocar nada

**Las dos pruebas YA FALLABAN antes de esta cirugía.** Es el listón que hay que igualar o
mejorar, no un listón limpio.

`.venv/bin/python 05-vista-ceo/verificar_excel.py` → **salida 1**

```
VERIFICACION DE LA VISTA DEL CEO
  WBS  : /home/server/projects/bot-trading/00-direccion/WBS.md
  Excel: /home/server/projects/bot-trading/05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx

  AVISO  estado declarado: 01.02.03: 2 marcas en negrita ['en_curso', 'hecha']; vale la ultima
  AVISO  estado declarado: 03.01.16: 2 marcas en negrita ['hecha', 'hecha']; vale la ultima
  AVISO  estado declarado: 03.01.17: 3 marcas en negrita ['hecha', 'hecha', 'pendiente']; vale la ultima
  AVISO  estado declarado: 07.01.01: 4 marcas en negrita ['en_curso', 'pendiente', 'en_curso', 'pendiente']; vale la ultima
  AVISO  estado declarado: 07.01.03: 2 marcas en negrita ['en_curso', 'en_curso']; vale la ultima

1. El Excel es posterior al WBS
  FALLO  Excel al dia: el WBS se ha tocado despues de generar el Excel: regeneralo

2. Censo de tareas: ni una perdida, ni una inventada
  FALLO  censo: en el WBS pero NO en el Excel: ['04.01.04']

3. Estado de cada tarea, leido dos veces con analizadores distintos
  FALLO  estados: 03.01.15: Excel dice 'Pendiente' y el WBS dice 'Hecha'
  FALLO  estados: 04.01.01: Excel dice 'Pendiente' y el WBS dice 'En curso'
  FALLO  estados: 04.01.04: Excel dice 'None' y el WBS dice 'En curso'

4. Ciclos de dependencias
  OK     ciclos: ninguno

5. La cola de SIGUIENTE respeta sus propias reglas
  FALLO  cola completa: faltan o sobran tareas vivas: ['03.01.15', '04.01.04']
  OK     orden de la cola: cada tarea esta en el grupo que le toca

6. Las cuentas del PANEL (formulas evaluadas de verdad)
  FALLO  panel: el panel suma 66.0 tareas y el WBS tiene 67

7. Las tareas hechas tienen su entregable en disco
  AVISO  entregables: 03.01.16 dice haber entregado costs.py y no esta en el repositorio
  AVISO  entregables: 03.01.21 dice haber entregado .meta.json y no esta en el repositorio
  AVISO  entregables: 04.03.07 dice haber entregado costs.py y no esta en el repositorio

8. Regla 24: los datos siguen fuera de git
  OK     regla 24: git no ve nada dentro de 02-datos/

9. Las hojas REGLAS, LECCIONES y DECISIONES traen el recuento VIVO de su fuente
  FALLO  hoja REGLAS: el Excel trae 29 reglas y CLAUDE.md tiene 30 ahora mismo
  FALLO  hoja LECCIONES: el Excel trae 36 lecciones y LECCIONES.md tiene 41 ahora mismo
  FALLO  hoja DECISIONES: el Excel trae 27 decisiones y DECISIONES.md tiene 30 ahora mismo

10. Posición del estado: ninguna marca de estado en negrita 'en medio' de la celda
  OK     posición del estado: 50 marcas revisadas en 67 celdas, ninguna en medio

======================================================================
RESULTADO: 10 FALLOS y 8 avisos. El Excel NO es de fiar.
```

`bash 05-vista-ceo/prueba_inyeccion.sh` → **salida 1**

```
PRUEBA DE INYECCION DEL VERIFICADOR
  (inyectando sobre la tarea 01.01.01)
  CAZADO   estado distinto del Excel
  CAZADO   estado sin declarar
  CAZADO   tarea que falta en el Excel
  CAZADO   dependencia fantasma
  CAZADO   ciclo de dependencias
  (inyectando L-042 sobre una copia de LECCIONES.md; 41 lecciones reales ahora mismo)
  CAZADO   lección nueva sin tocar el Excel (recuento)
  (inyectando sobre la tarea 01.01.01, 40 caracteres antes de su marca real en posición 1)
  CAZADO   estado en medio de la celda (posición)
  --
  MAL      el WBS real NO pasa la verificacion: mirala antes de seguir
RESULTADO: 1 problemas.
```

**Lectura de esto, en claro:** los 7 guardias de inyección **muerden los 7**. El único
"problema" de `prueba_inyeccion.sh` es que arrastra el fallo de `verificar_excel.py`, y ese
fallo es que **el Excel está desfasado respecto al WBS** — no que el WBS esté mal. Nadie
regeneró el Excel después de los últimos commits.

**Listón para el resto de la cirugía:** ≤ 10 FALLOS en `verificar_excel.py` y **7 de 7
CAZADO** en `prueba_inyeccion.sh`. Cualquier bloque que empeore eso se revierte.

### Estado del árbol

```
git status --porcelain   → limpio
git log --oneline -1     → 89cdf08 03.01.15: regla 30, el diagnostico de los ocho agentes
                                    y un muro que no cubria lo que decia
```

---

## DESPUÉS

*(se rellena en el bloque 7)*
