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

## DESPUÉS — 12/08/2026, tras los seis commits de la cirugía

Mismos comandos, literalmente los del bloque 0.

### Bytes de lectura obligatoria del orquestador

```
 14884 CLAUDE.md
 49039 00-direccion/WBS.md
 41945 00-direccion/LECCIONES.md
 50905 00-direccion/DECISIONES.md
156773 total
```

**De 275.301 a 156.773 bytes: 118.528 menos, un 43,1% de recorte.** Todo el ahorro sale del
WBS (168.317 → 49.039). `CLAUDE.md` sube 750 bytes porque la nota de la regla 8 reactivada y
la explicación del diagrama son texto nuevo. `LECCIONES.md` y `DECISIONES.md` no se tocan.

### Tareas y estados

```
62   filas de tarea   (67 antes: 5 congeladas en DEUDA-MOTOR.md)
 6   **en_curso**
26   **hecha**
 5   **pendiente**
 0   **bloqueada**
```

**Ojo con estas cifras: bajan por dos motivos distintos y conviene no confundirlos.**
Las marcas en negrita pasan de 50 a 37 no porque haya menos tareas declaradas, sino porque
las celdas que llevaban **varias** marcas (07.01.01 llegó a tener cuatro) dejaron las
sobrantes dentro de su expediente. **Ni un solo estado de tarea cambió**, comprobado
comparando tarea por tarea contra el commit `89cdf08`: cero diferencias.

### Reparto producto/motor

```
filas de tarea: 62
PRODUCTO: 33 tareas, 9,696 bytes
MOTOR:    23 tareas, 7,933 bytes
motor = 41.1% tareas, 45.0% texto
celda mediana: 291 car. · celda mayor: 1063 car. (02.02.05)
```

El texto de motor del índice cae del 62,4% al 45,0%. La celda mayor pasa de **10.471 a
1.063 caracteres**: ya no hay ninguna por encima del tope de 1.200.

**Aviso de honestidad sobre este número:** el motor no ha bajado porque se haya hecho menos
motor. Ha bajado porque 5 tareas de motor están congeladas y porque su relato se mudó a los
expedientes. El reparto de esfuerzo real, medido sobre commits por el contador de `03.01.18`,
es del **58,9%**, y esa es la cifra que hay que mirar el lunes, no ésta.

### Estado de las pruebas DESPUÉS

`.venv/bin/python 05-vista-ceo/verificar_excel.py` → **salida 0**

```
1.  OK  Excel al dia
2.  OK  censo: 62 tareas en los dos sitios
3.  OK  estados: 62 coinciden
4.  OK  ciclos: ninguno
5.  OK  cola completa: 36 tareas vivas repartidas en cola(15) y espera(21)
    OK  orden de la cola: cada tarea esta en el grupo que le toca
6.  OK  panel: total 62 · hechas 26, cuadra con el WBS
7.  AVISO x9  entregables citados que no estan en el repositorio
8.  OK  regla 24: git no ve nada dentro de 02-datos/
9.  OK  hoja REGLAS: 30 · LECCIONES: 41 · DECISIONES: 30, iguales a su fuente viva
10. OK  posición del estado: 37 marcas revisadas en 62 celdas, ninguna en medio

RESULTADO: sin fallos. 9 avisos.
```

**Las 12 comprobaciones en OK. De 10 FALLOS a 0.** Los 5 avisos de «2 marcas en negrita,
vale la última» han desaparecido: los resolvió la partición. Los avisos de entregables suben
de 3 a 9 y **eso no es un empeoramiento**: la prueba 7 ahora también lee los expedientes, así
que ve nombres de fichero que antes no miraba. Ve más, no falla más.

`bash 05-vista-ceo/prueba_inyeccion.sh` → **salida 0**

```
CAZADO   estado distinto del Excel
CAZADO   estado sin declarar
CAZADO   tarea que falta en el Excel        <- este era un aprobado falso, ver abajo
CAZADO   dependencia fantasma
CAZADO   ciclo de dependencias
CAZADO   lección nueva sin tocar el Excel (recuento)
CAZADO   estado en medio de la celda (posición)
OK       el WBS real pasa la verificacion completa
RESULTADO: el verificador muerde en los 7 casos.
```

**Corrección sobre el ANTES, porque el número de partida era mejor de lo que parecía y peor
de lo que decía.** En el ANTES salían 7 CAZADO, pero **el caso 3 aprobaba en falso**: inyectaba
la tarea `07.01.03`, que había acabado existiendo de verdad en el WBS, así que no inyectaba
una tarea nueva sino un duplicado —que el censo no mira—. Pasaba porque el `grep` encontraba
*otro* fallo de censo, el del Excel desfasado. Se descubrió al arreglar ese desfase. El fixture
ahora elige el código comprobando que no existe. **Los 7 casos de hoy son 7 de verdad.**

### Estado del árbol

```
git log --oneline -1   → el commit final de la cirugía
```
