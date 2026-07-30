# Bot de trading algoritmico

Proyecto dirigido por WBS con equipo de agentes. **Empieza leyendo `CLAUDE.md`.**

## Arranque rapido

1. `git init && git add -A && git commit -m "arranque"`
2. Comprueba que los datos NO entran en git: `git status --porcelain 02-datos/` debe salir vacio.
3. Abre Claude Code en esta carpeta y escribe:
   `Lee CLAUDE.md y 00-direccion/WBS.md y dime cual es la siguiente tarea.`

## Mapa

| Carpeta | Que hay |
|---|---|
| `00-direccion/` | WBS (fuente de verdad), decisiones, lecciones, informes semanales |
| `01-investigacion/` | Mercados, hipotesis, herencia del proyecto anterior |
| `02-datos/` | bruto / limpio / **reservado (prohibido)** |
| `03-motor/` | backtester, bot, scripts |
| `04-resultados/` | backtests, veredictos, registro de pruebas |
| `05-vista-ceo/` | El Excel del lunes y su generador |
| `.claude/agents/` | Los 8 agentes |

## Lo unico que hay que recordar

El objetivo es el BOT, no el motor de agentes. Cada tirada cierra al menos una tarea de producto.
