---
description: Regenera la vista Excel del CEO desde el WBS, la verifica por ejecucion y reporta los cambios
---

Regenera `05-vista-ceo/WBS_Bot_Trading_v0.9.xlsx` a partir de `00-direccion/WBS.md`, comprueba por
ejecucion que dice la verdad, y cuenta al CEO que ha cambiado.

**Regla de oro: el Excel se genera del WBS, nunca al reves.** Esta prohibido que este comando
escriba una sola linea en `00-direccion/WBS.md`. Si el WBS esta mal, se reporta; no se toca aqui.

## Los cuatro pasos

**1. Entorno.** Si no existe `.venv/bin/python`:
```
python3 -m venv .venv && .venv/bin/pip install -q openpyxl formulas
```
(El sistema no deja instalar en el Python global. `formulas` es opcional: sin el, las cuentas del
panel se quedan como NO VERIFICADAS y hay que decirlo.)

**2. Generar.**
```
.venv/bin/python 05-vista-ceo/generar_excel.py
```
Lee su salida entera (regla 15 de CLAUDE.md). Trae tres cosas que necesitas: el recuento por fase, los AVISOS de
lectura, y el bloque **CAMBIOS DESDE LA ULTIMA GENERACION**, que es de donde sale tu informe.

**3. Verificar.** El codigo de salida manda, no la impresion que te de el fichero:
```
.venv/bin/python 05-vista-ceo/verificar_excel.py
```
Comprueba 8 cosas, con un analizador del WBS **distinto** al del generador: que el Excel es
posterior al WBS · que no falta ni sobra ninguna tarea · que cada estado coincide leido dos veces ·
que no hay dependencias circulares · que la cola de SIGUIENTE cumple sus reglas · que los COUNTIFS
del panel evaluados dan el numero correcto · que los entregables citados por las tareas hechas
existen en disco · que `02-datos/` sigue fuera de git (regla 27 de CLAUDE.md).

**4. Si sale codigo 1, NO entregues el Excel.** Separa de quien es el fallo:

| El fallo dice | De quien es | Que haces |
|---|---|---|
| `estados`, `censo`, `cola`, `panel` | del generador o el Excel esta viejo | arreglas `generar_excel.py` y repites desde el paso 2 |
| `estado declarado` | del WBS: una celda ESTADO no declara estado | **paras y lo reportas al CEO.** No adivines el estado |
| `dependencias existen`, `ciclos`, `codigos unicos` | del WBS: la cola es incoherente | **paras y lo reportas.** Tocar el WBS no es tuyo |
| `regla 24` | datos entrando en git | **excepcion inmediata al CEO** |
| AVISO `entregables` | una tarea dice hecha y su fichero no esta | lo investigas y lo dices; puede ser una tarea cerrada en falso |

> `regla 24` de la fila de arriba es la etiqueta LITERAL que imprime `fallo()`/`ok()` en
> `05-vista-ceo/verificar_excel.py` (`"regla 24"` hardcodeado): no se toca aqui porque dejaria de
> coincidir con la salida real del script. Por contenido es la regla 27 de CLAUDE.md ("los datos
> nunca entran en git"), no la 24. Desajuste registrado como deuda de motor: el script se corrige en
> tarea aparte, fuera de esta pasada.

## Que le cuentas al CEO

En este orden, corto:

1. **Si el Excel anterior estaba mal, eso va primero**, antes que ninguna otra cosa. Que decia mal,
   por que, y que ya esta corregido.
2. **Que ha cambiado** desde la ultima generacion: usa el bloque CAMBIOS, no tu memoria.
3. **Las tres casillas de arriba de la hoja SIGUIENTE**: AHORA-EQUIPO, AHORA-CEO y CUELLO DE BOTELLA.
4. **Lo que se ve al leerlo y no se veia en el texto**: tareas cerradas sin entregable, trabajo
   empezado con dependencias abiertas, revisiones que rechazan, reparto producto/motor de la cola
   (regla 8 de CLAUDE.md). Dilo aunque incomode: para eso esta la vista.
5. El enlace al fichero.

Nada de "el Excel esta actualizado" a secas. Si las 8 pruebas pasaron, dilo con el numero: cuantas
tareas, cuantas hechas, cuantos avisos.

## Si tocas el generador o el verificador

Vuelve a pasar la prueba de inyeccion antes de dar nada por bueno (regla 25 de CLAUDE.md):
```
bash 05-vista-ceo/prueba_inyeccion.sh
```
Le mete cinco WBS rotos al verificador y comprueba que los caza los cinco. Si alguno **ESCAPA**, el
verificador esta ciego a ese fallo y hay que arreglarlo antes de seguir.

## Por que este comando es asi

El 31/07/2026 el formato del WBS cambio —la ficha paso a ir delante del estado, en la misma celda— y
el generador siguio leyendo solo el principio: **cuatro tareas hechas aparecieron como pendientes en
la vista del CEO y nada aviso**. De ahi salen las tres defensas de aqui: el verificador lee el WBS
con codigo propio, ninguna celda sin estado se da por "pendiente" en silencio, y la prueba de
inyeccion demuestra que el verificador muerde de verdad.
