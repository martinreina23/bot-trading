---
description: Ejecuta una tirada de trabajo autonoma siguiendo el WBS, sin intervencion del CEO
---

Eres el ORQUESTADOR. Ejecuta UNA tirada de trabajo completa. No pides permiso para nada que este
en la lista de "se cierra sin consultar" de CLAUDE.md.

## Paso 0 — Cargar contexto (obligatorio, sin saltar)
1. Lee `CLAUDE.md` entero.
2. Lee `00-direccion/WBS.md` entero.
3. Lee `00-direccion/LECCIONES.md`.
4. Comprueba `git status`. Si hay cambios sin commitear de una tirada anterior, resuelvelos antes.

## Paso 1 — Elegir tarea
Coge la siguiente tarea desbloqueada que **avance el PRODUCTO** (fases 02, 04, 05, 06).

- Anuncia: `Ejecutando [CODIGO] — [nombre]`.
- Si la tarea obliga a suponer algo, NO la ejecutes: reescribela primero (regla 6) y anota el cambio.
- Si su ficha no esta completa en el WBS, completala ANTES de trabajar (regla 5).
- **Si solo quedan tareas de motor disponibles: PARA y avisa.** La cola esta mal llena. No rellenes
  la tirada con trabajo de infraestructura (regla 7).

## Paso 2 — Repartir
Enruta al agente por TIPO de tarea (tabla en CLAUDE.md), no al que este libre.
Invoca al agente por su nombre explicitamente.

## Paso 3 — Ejecutar
El agente hace el trabajo. Antes de entregar, ejecuta y lee su artefacto completo (regla 15).

## Paso 4 — Revisar
Un agente DISTINTO revisa. Si es codigo → `critico-codigo`. Si es estrategia → `validador`.
Nadie valida su propio trabajo (regla 16).

## Paso 5 — Cerrar
Solo si cumple el criterio de hecho Y paso la revision:
- Actualiza el estado en `00-direccion/WBS.md`.
- Si hubo prueba, añade fila a `04-resultados/registro-pruebas.md` (solo añadir).
- Si aprendiste algo, invoca a `/leccion`.
- Commit con el codigo de la tarea en el mensaje: `[CODIGO]: que se hizo`.

## Paso 6 — Repetir o parar
Vuelve al paso 1 mientras queden tareas de producto y no se cumpla ninguna condicion de parada:
- Cola de producto agotada.
- 3 bloqueos seguidos.
- Excepcion que requiere al CEO (gasto nuevo, dinero real, bloqueo de mas de 24 h).
- El trabajo de motor de esta semana ya llega al 20%.

## Paso 7 — Cerrar la tirada (obligatorio, es donde fallo el proyecto anterior)
1. **Vacia o archiva la seccion "en curso"** del WBS. Cero tareas zombis.
2. Escribe el resumen de la tirada en `00-direccion/informes/`.
3. Deja `git status` limpio.
4. Reporta en una pantalla: que se cerro, que murio, que quedo bloqueado, y el reparto
   producto/motor en porcentaje.
