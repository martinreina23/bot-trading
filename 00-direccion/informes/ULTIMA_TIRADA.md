# Parte de la última tirada

**Fecha: lunes 3 de agosto de 2026.** Este fichero se sobrescribe en cada parada. Git guarda
el historial (regla 28 de CLAUDE.md). Se escribe para leerse **en frío**, sin haber seguido
la conversación.

---

## 1. ESPERA POR EL CEO — una sola cosa

**Ficha D-19: puerta G1, qué mercados y qué vela.** Aprobada por revisión independiente y
lista. Respuesta de una letra.

- **A)** ORO + USDJPY + GBPUSD, vela 4h ← **recomendada**
- **B)** ORO + USDJPY + EURUSD, vela 4h
- **C)** La A con vela de 1h
- **D)** La A más BITCOIN

**Dos avisos que van con la decisión, los dos verificados:**
1. El coste que sostiene el criterio principal mezcla brokers y tipos de cuenta en 7 de los 8
   mercados: esa cifra no existe en ningún broker real y se remide al elegir broker (04.01.02).
2. **Ningún mercado cumple el criterio del hueco de fin de semana.** O el bot cierra antes del
   viernes, o G2 declara por escrito que una operación puede perder **hasta 5,05 veces** lo
   arriesgado — máximo medido en el ORO, que es el mercado principal de la cesta recomendada.
   Marcado *no probado*: el texto aprobado dice 4,5x y la medición original dice 5,05x, y esa
   discrepancia sigue sin resolver.

**Por qué corre prisa:** la fecha de no retorno hacia la puerta GM (1 de septiembre) es el
**10 de agosto**, cuando hay que tener broker firmado. G1 desbloquea 17 de las 41 tareas vivas.

---

## 2. TERMINADO Y VERIFICADO

**El motor de backtest existe.** `03-motor/backtester/` estaba vacío por la mañana. Commit
`0c35959`. Es la pieza sin la cual no hay Fase 04 ni respuesta en GM.

- `verificar_motor.py` → código de salida **0** (3 pruebas).
- `pytest` → **44 de 44**.
- Verificado por Claude Code ejecutándolo, no solo por quien lo escribió.

**Decisiones D-17 y D-18 firmadas por el CEO, registradas y propagadas a `CLAUDE.md`:**
- **D-17 = B:** ratifica las reglas actuales y **suspende el techo del 20% de motor** hasta que
  03.01.05 esté hecha o hasta el 01/09, lo que llegue antes.
- **D-18 = B, con enmienda del mismo día:** el lunes deja de ser la única ventana del CEO y pasa
  a ser checkpoint de revisión. Lo que esté listo le llega el día que esté listo, **sin tope de
  número**; el CEO marca el final del día.

**Dependencia falsa corregida:** `03.01.08` figuraba dependiendo de `03.01.03`, que nunca fue
cierto — su primera pasada se ejecutó el 31/07 sin que 03.01.03 existiera. Corregida a
`03.01.01, 03.01.02`. Desbloquea `03.01.08` y `03.01.11`.

**Dos lecciones nuevas:** L-024 (una decisión firmada que no se propaga deja el proyecto
funcionando con la premisa vieja) y L-025 (una orden dirigida al CEO debe declarar dónde se
teclea).

---

## 3. RECHAZADO — dos de tres entregas, y por qué importa

**El motor se hacía trampas a su favor.** Cobraba el coste de operar al entrar pero **no al
salir**, salvo cuando la operación salía por tiempo — que es la excepción. Stop y objetivo, que
son la salida normal, no lo pagaban. Casi toda operación pagaba medio coste, y el error iba
**siempre en la dirección de hacer parecer la estrategia mejor de lo que es**. Es la misma
familia de fallo que ya tumbó la pieza T1. Reparado, y la revisión lo confirmó con una tabla de
10 escenarios: las 10 cobran exactamente el coste completo, ninguna de menos ni de más.

**El informe de G1 escondía el riesgo mayor.** Detectó que la pérdida posible medida es 5,05x y
lo dejó en la sección técnica, **no en la ficha que lee el CEO**, que decía 4,5x. Reparado: el
número mayor ya está en la ficha.

**Ninguno de los dos fallos lo vio quien lo escribió.** Los dos habrían llegado al CEO como
buenos.

---

## 4. DECIDIDO SIN CONSULTAR — por si el CEO quiere otro camino

- **La lista de motor bajó de 9 tareas a 7.** Fuera la ejecución desatendida (servía para avisar
  cuando el CEO no está, y ha declarado que está a diario) y la estrategia de ramas (sin ningún
  incidente vivo detrás: una sola rama, un solo árbol de trabajo).
- **El techo del 20% de motor vuelve el viernes 07/08**, no el 01/09 que el CEO concedió. Es un
  límite que el orquestador se impone a sí mismo, más estricto que lo firmado.
- **Se cerrarán con hueco declarado `01.02.03` y `01.02.04`** (auditoría del ecosistema y de los
  MCP) en vez de seguir: tres investigaciones seguidas concluyen «ninguna pieza / ningún
  servidor» y ya consumieron dos tiradas cada una. **El CEO ordenó la segunda pasada de MCP; si
  prefiere terminarla, tiene que decirlo.**
- **Solo se guardó en git el motor**, no el resto del trabajo del día: los demás cambios aún no
  han pasado revisión y guardarlos sería darlos por buenos sin que nadie distinto los mire.

---

## 5. HALLAZGO NUEVO, SIN REPORTAR HASTA AHORA

`04-resultados/registro-cajon.md` tiene **dos entradas de hoy** que nadie había mencionado:

```
2026-08-03 14:26:49 · COMPROBAR · RECHAZADO: incorrecta
2026-08-03 14:26:53 · COMPROBAR · correcta
```

Alguien ejecutó la comprobación del cajón reservado hoy: falló con contraseña incorrecta y
acertó 4 segundos después. **Esto exige una terminal real**, que ningún agente tiene. La lectura
más probable es que fue el propio CEO, que dijo haberla tecleado él. Si no fue él, es un
incidente y hay que abrirlo.

**Consecuencia buena:** es la **prueba por ejecución** de que la contraseña en vigor es correcta
—hasta ahora solo se tenía la palabra del CEO— y de que el guardia **rechaza** una contraseña
equivocada. El registro creció 2 líneas y no borró ninguna: sigue siendo de solo añadir.

---

## 6. PENDIENTE / SIGUE ABIERTO

| Qué | Estado |
|---|---|
| `02.03.03` — puerta G1 | Espera la letra del CEO |
| `03.01.11` y `03.01.08` — cajón y barreras | Desbloqueadas, sin arrancar |
| `03.01.14`, `03.01.16`, `03.01.17` — el Excel del CEO | Fichas escritas, sin arrancar |
| Excel `WBS_Bot_Trading_v0.9.xlsx` | **Sin regenerar.** El verificador da 8 fallos, todos por estar desfasado respecto al WBS |
| Cambios en WBS, reglas y decisiones | Escritos, **sin revisar y sin guardar en git** |
| `00-direccion/informes/FICHA_D-17.md` | Borrador caducado que había que borrar. **Sigue ahí** |
| Discrepancia 4,52x vs 5,05x | Sin resolver. Exige recalcular sobre datos brutos |
| `requirements.txt` | No lista `pytest`, y sí lista `yfinance`, fuente ya jubilada |
