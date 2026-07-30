# Checklist de migración a Claude Code

**Estado a 29/07/2026.** Cuando todo lo de los bloques A, B y C esté marcado, se monta el repositorio (tarea 03.01.01) y este chat deja de ser el sitio donde vive el proyecto.

---

## A. Decisiones cerradas ✅

- [x] **G0 — Plan y reglas aprobados** (01.01.01)
- [x] **Criterios de la puerta G1 fijados** (01.01.02) — qué se mide ahora, umbrales se calibran con los números delante
- [x] **Horizonte: 1 mes**, evaluación el 1 de septiembre (puerta GM)
- [x] **Tiempo del CEO: 1 hora, lunes**
- [x] **Mercado NO decidido a dedo** — sale de la puerta G1 con datos
- [x] **Equipo de agentes definido**: 8 roles, cada uno con modelo y respaldo
- [x] **Autonomía definida**: qué cierra el equipo, qué llega en el informe, qué es excepción inmediata
- [x] **Guardarraíles en dos niveles**: reversible permisivo / irreversible con barrera
- [x] **Formato de ficha de decisión del CEO**
- [x] **Cadencia**: WBS texto siempre; Excel solo lunes y puertas
- [ ] **D5 — Límites de dinero real** (capital y parada dura). NO bloquea la migración: hace falta antes de la puerta G3, dentro de meses

## B. Documentos que ya existen y se migran 📄

| Archivo | Qué es | Dónde va en el repo |
|---|---|---|
| `WBS.md` (v0.7) | **Fuente de verdad.** Reglas, equipo, autonomía, fases, puertas, decisiones, lecciones | `00-direccion/WBS.md` |
| `WBS_Bot_Trading_v0.7.xlsx` | Vista del CEO (lunes) | `05-vista-ceo/` |
| `build_wbs7.py` | Generador del Excel a partir del WBS | `05-vista-ceo/` |
| `BRIEFS_FASE_02.md` | Briefs A y B del analista | `01-investigacion/mercados/` |
| Entrega Brief A del analista | Costes, ATR, coste relativo | `01-investigacion/mercados/` ⚠️ **pendiente de guardar como archivo** |
| `REVISION_02.03.01.md` | Revisión independiente del Brief A | `01-investigacion/mercados/` |
| `atr_local.py` | Cálculo real del ATR | `03-motor/scripts/` |
| `PROMPT_01.02.01_analisis_gb2.md` | Prompt de auditoría de gb2 | `01-investigacion/herencia-gb2/` |
| ~~`PLAN_v0.1.md`~~ | Obsoleto, superado por el WBS | **se descarta** |

## C. Trabajo en curso — esperando resultado ⏳

- [ ] **01.02.01 — Informe de gb2** → Claude Code corriendo. Salida: `INFORME_GB2.md`
- [ ] **02.02.01/02 — ATR real y coste relativo** → ejecutar `atr_local.py`. Salida: `atr_real.json` + tablas
- [ ] **02.02.03/04 — Brief B** (correlaciones + históricos disponibles) → chat analista
- [ ] **02.02.05 — Swap/financiación** de los 8 instrumentos → chat analista, anexo corto

## D. Falta crear ANTES de migrar 🔨

Esto lo preparo yo mientras esperas los resultados:

- [ ] **`CLAUDE.md`** — las reglas del proyecto que los agentes leen en cada arranque. La pieza más importante del repositorio
- [ ] **8 archivos de agente** (`.claude/agents/`) con descripción sin ambigüedad, modelo asignado y prohibiciones explícitas
- [ ] **`settings.json`** — permisos: amplios en lo reversible, barrera en lo irreversible
- [ ] **`DECISIONES.md`** — extraído del WBS, como archivo propio y vivo
- [ ] **`LECCIONES.md`** — ya hay 5 lecciones (L-001 a L-005)
- [ ] **Plantilla de informe semanal** (una página, para tu lunes)
- [ ] **Plantilla de cola de aprobación** (Aprobado / Saltar / Corregir)
- [ ] **`README.md`** — qué es esto y cómo se arranca

## E. Después de migrar, no antes 🚫

- Elegir broker (04.01.01) — necesita la puerta G1 cerrada
- Descargar los históricos y montar los 3 cajones de datos (04.01.03)
- Ejecución desatendida 24/7 (03.01.03)
- Prueba real del motor de un día entero (03.01.05)

---

## Estructura de carpetas propuesta

```
proyecto-bot/
├── CLAUDE.md                    ← reglas que los agentes leen siempre
├── README.md
├── .claude/
│   ├── agents/                  ← los 8 agentes, un archivo cada uno
│   ├── settings.json            ← permisos y barreras
│   └── commands/                ← comandos propios (/autonomo, /informe)
├── 00-direccion/
│   ├── WBS.md                   ← FUENTE DE VERDAD
│   ├── DECISIONES.md
│   ├── LECCIONES.md
│   └── informes/                ← uno por semana
├── 01-investigacion/
│   ├── mercados/                ← briefs, entregas, revisiones
│   ├── hipotesis/               ← fichas y pre-registro de variantes
│   └── herencia-gb2/            ← informe de gb2 (información, no código)
├── 02-datos/
│   ├── bruto/
│   ├── limpio/
│   └── reservado/               ← 🔒 OOS. Ningún agente entra aquí
├── 03-motor/
│   ├── backtester/
│   ├── bot/
│   └── scripts/
├── 04-resultados/
│   ├── backtests/
│   ├── veredictos/
│   └── registro-pruebas.md      ← TODAS las pruebas, también las fallidas
└── 05-vista-ceo/
    └── WBS_Bot_Trading.xlsx + generador
```

**Regla de oro de la estructura:** una sola fuente de verdad por tema. Documento que se sustituye, se borra — git guarda el historial. Fue una de las causas del caos en gb2.

---

## Resumen en una línea

**Cerrado 10 de 11 decisiones · 8 documentos listos para migrar · 4 resultados en camino · 8 archivos por crear (los preparo yo).**
Cuando lleguen el informe de gb2 y el Brief B, se monta el repositorio y todo esto se muda.
