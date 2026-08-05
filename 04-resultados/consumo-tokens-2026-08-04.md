# Consumo de tokens de la sesión del 04/08/2026 — recalculado sobre datos brutos

Tarea WBS: **03.01.21** (diagnóstico de consumo de tokens). Esta ficha cierra el hueco que la propia
celda declaró el 04/08: *"las cifras no están persistidas en ningún fichero del repositorio; viven
solo en el hilo de la sesión"*. Todo lo de abajo se ha vuelto a calcular hoy, 05/08/2026, desde los
JSONL brutos (regla 14 de `CLAUDE.md`), sin copiar ningún número de la celda del WBS.

Intérprete usado en todos los comandos: `/home/server/projects/bot-trading/.venv/bin/python3`.

## 1. Fuentes

| Fuente | Ruta absoluta | Tamaño | Nº de ficheros |
|---|---|---|---|
| Hilo principal | `/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl` | 4.056.818 bytes (verificado con `stat -c '%s' <ruta>`) | 1 |
| Subagentes | `/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/` | 36 MB (`du -sh`, 36.807.524 bytes con `du -sb`) | 150 ficheros en total: 75 `.jsonl` (un transcript por subagente) + 75 `.meta.json` (un metadato por subagente) |

**Discrepancia resuelta (75 subagentes vs. 150 ficheros):** la cifra buena es **75 subagentes**. La
carpeta contiene el doble de ficheros porque Claude Code escribe DOS ficheros por subagente: el
transcript (`agent-*.jsonl`) y su metadato (`agent-*.meta.json`, con `agentType`, `description`,
`toolUseId`, `spawnDepth`, sin tokens). Comando que lo demuestra:

```
find "/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents" -maxdepth 1 -type f -name '*.jsonl' | wc -l    # -> 75
find "/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents" -maxdepth 1 -type f -name '*.meta.json' | wc -l # -> 75
find "/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents" -maxdepth 1 -type f | wc -l                    # -> 150 = 75+75
```

## 2. Método de recuento (mismo para las dos fuentes)

Cada línea `assistant` del JSONL trae un `requestId` y su `usage` (`cache_read_input_tokens`,
`cache_creation_input_tokens`, `input_tokens`, `output_tokens`, `model`). Cuando una respuesta se
compone de varios bloques (pensamiento, texto, uso de herramienta), Claude Code escribe **una línea
por bloque, todas con el mismo `requestId` y el mismo `usage` repetido**. Sumar sin deduplicar
infla el recuento. Todos los comandos de abajo deduplican por `requestId` (se queda con la primera
aparición) antes de sumar o contar.

Cada fuente trae además unas pocas entradas con `model == "<synthetic>"` y `usage` a cero
(reintentos/errores internos sin coste real). El hilo principal las **excluye** al contar
"peticiones" (207 reales de 210 `requestId` totales); los subagentes las **incluye** (1.293 es el
total de `requestId` únicos, reales+sintéticas, de las 75 transcripciones). Esta diferencia de
criterio entre las dos cifras ya venía así en la celda original del 04/08 — se reproduce tal cual,
no se ha unificado, porque unificarla habría cambiado el número que hay que verificar.

## 3. Comandos de una línea (reproducibles sin tener el hilo delante)

```
# 1) hilo principal — peticiones reales (excluye "<synthetic>")
python3 -c "
import json
byreq={}
with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if o.get('type')=='assistant':
            rid=o.get('requestId')
            if rid and rid not in byreq: byreq[rid]=o['message'].get('model')
print(sum(1 for m in byreq.values() if m!='<synthetic>'))"
# -> 207

# 2) hilo principal — tokens leídos de cache (suma cache_read_input_tokens, excluye "<synthetic>")
python3 -c "
import json
byreq={}
with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if o.get('type')=='assistant':
            rid=o.get('requestId')
            if rid and rid not in byreq:
                m=o['message']; byreq[rid]=(m.get('model'), m['usage'].get('cache_read_input_tokens',0))
print(sum(v[1] for v in byreq.values() if v[0]!='<synthetic>'))"
# -> 94913491

# 3) hilo principal — contexto pico (maximo cache_read_input_tokens de una sola peticion real)
python3 -c "
import json
byreq={}
with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if o.get('type')=='assistant':
            rid=o.get('requestId')
            if rid and rid not in byreq:
                m=o['message']; byreq[rid]=(m.get('model'), m['usage'].get('cache_read_input_tokens',0))
print(max(v[1] for v in byreq.values() if v[0]!='<synthetic>'))"
# -> 794459

# 4) hilo principal — contexto medio (suma cache_read_input_tokens / TODAS las peticiones, 210,
#    incluidas las 3 sinteticas de 0 tokens -- este es el denominador que reproduce el "~452.000")
python3 -c "
import json
byreq={}
with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if o.get('type')=='assistant':
            rid=o.get('requestId')
            if rid and rid not in byreq:
                m=o['message']; byreq[rid]=(m.get('model'), m['usage'].get('cache_read_input_tokens',0))
total=sum(v[1] for v in byreq.values())
print(round(total/len(byreq)))"
# -> 451969

# 5) subagentes — numero de subagentes
find "/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents" -maxdepth 1 -type f -name '*.jsonl' | wc -l
# -> 75

# 6) subagentes — peticiones totales (requestId unicos por fichero, incluye "<synthetic>")
python3 -c "
import json, glob
total=0
for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
    seen=set()
    with open(fp, encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            o=json.loads(line)
            if o.get('type')=='assistant':
                rid=o.get('requestId')
                if rid: seen.add(rid)
    total+=len(seen)
print(total)"
# -> 1293

# 7) subagentes — tokens leidos de cache (excluye "<synthetic>", deduplicado por requestId dentro
#    de cada fichero)
python3 -c "
import json, glob
total=0
for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
    byreq={}
    with open(fp, encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            o=json.loads(line)
            if o.get('type')=='assistant':
                rid=o.get('requestId')
                if rid and rid not in byreq:
                    m=o['message']; byreq[rid]=(m.get('model'), m['usage'].get('cache_read_input_tokens',0))
    total+=sum(v[1] for v in byreq.values() if v[0]!='<synthetic>')
print(total)"
# -> 114765547

# 8) subagentes — tokens escritos en cache (cache_creation_input_tokens, mismo metodo que 7)
python3 -c "
import json, glob
total=0
for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
    byreq={}
    with open(fp, encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            o=json.loads(line)
            if o.get('type')=='assistant':
                rid=o.get('requestId')
                if rid and rid not in byreq:
                    m=o['message']; byreq[rid]=(m.get('model'), m['usage'].get('cache_creation_input_tokens',0))
    total+=sum(v[1] for v in byreq.values() if v[0]!='<synthetic>')
print(total)"
# -> 11503375

# 9) total leidos (hilo + subagentes)
python3 -c "print(94913491+114765547)"
# -> 209679038  (=209,7 M)
```

## 4. Tabla: recalculado hoy vs. afirmado el 04/08

| Cifra | Recalculada hoy (05/08) | Afirmada el 04/08 | ¿Coincide? |
|---|---|---|---|
| Hilo principal — peticiones | 207 | 207 | COINCIDE |
| Hilo principal — leídos de cache | 94.913.491 (≈94,9 M) | 94,9 M | COINCIDE |
| Hilo principal — contexto pico | 794.459 | 794.459 | COINCIDE |
| Hilo principal — contexto medio | 451.969 (≈452.000) | ~452.000 | COINCIDE |
| Subagentes — nº de subagentes | 75 | 75 | COINCIDE |
| Subagentes — peticiones | 1.293 | 1.293 | COINCIDE |
| Subagentes — leídos de cache | 114.765.547 (≈114,8 M) | 114,8 M | COINCIDE |
| Subagentes — escritos en cache | 11.503.375 (≈11,5 M) | 11,5 M | COINCIDE |
| Total leídos (hilo + subagentes) | 209.679.038 (≈209,7 M) | ~209,7 M | COINCIDE |
| Suelo fijo por conversación | no reproducible desde estas dos fuentes (ver HUECO) | ~85.000 tokens | NO COINCIDE / NO VERIFICABLE |

Todas las cifras coinciden salvo una. No hay ninguna línea "NO COINCIDE por error de cálculo": la
única discrepancia es de verificabilidad (ver HUECO), no de aritmética.

## 5. Explicación de la única discrepancia

**Suelo fijo ~85.000 tokens por conversación — NO COINCIDE / NO VERIFICABLE con estas dos fuentes.**
Se probaron cuatro formas razonables de derivarlo de los datos brutos y ninguna se acerca a 85.000:

- Contexto total (`cache_read + cache_creation + input`) de la **primera** petición real de cada
  uno de los 75 subagentes: mínimo 10.430, máximo 16.825, mediana 14.984. Comando:
  ```
  python3 -c "
  import json, glob, statistics
  vals=[]
  for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
      primera=None
      with open(fp, encoding='utf-8') as f:
          for line in f:
              line=line.strip()
              if not line: continue
              o=json.loads(line)
              if o.get('type')=='assistant':
                  m=o['message']
                  if m.get('model')=='<synthetic>': continue
                  primera=m.get('usage',{})
                  break
      if primera is None: continue
      vals.append(primera.get('cache_read_input_tokens',0)+primera.get('cache_creation_input_tokens',0)+primera.get('input_tokens',0))
  print('n=',len(vals),'min=',min(vals),'max=',max(vals),'mediana=',statistics.median(vals))"
  # -> n= 75 min= 10430 max= 16825 mediana= 14984
  ```
- Lo mismo pero solo para los 42 subagentes cuya primera petición real arranca con
  `cache_read_input_tokens == 0` (arranque en frío de verdad, sin cache heredada): entre **10.535**
  y **16.825** (corregido 05/08/2026: la cifra anterior, 10.525-16.823, era una errata de
  transcripción — no coincidía con el cálculo sobre datos brutos, regla 14 de `CLAUDE.md`). Comando
  que demuestra la cifra corregida:
  ```
  python3 -c "
  import json, glob
  vals=[]
  for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
      primera=None
      with open(fp, encoding='utf-8') as f:
          for line in f:
              line=line.strip()
              if not line: continue
              o=json.loads(line)
              if o.get('type')=='assistant':
                  m=o['message']
                  if m.get('model')=='<synthetic>': continue
                  primera=m.get('usage',{})
                  break
      if primera is None: continue
      if primera.get('cache_read_input_tokens',0)==0:
          vals.append(primera.get('cache_read_input_tokens',0)+primera.get('cache_creation_input_tokens',0)+primera.get('input_tokens',0))
  print('n=',len(vals),'min=',min(vals),'max=',max(vals))"
  # -> n= 42 min= 10535 max= 16825
  ```
- Contexto de la primera petición real del hilo principal: 37.757 (y ya arranca con
  `cache_read_input_tokens = 20.628` distinto de cero, es decir, ni siquiera es un arranque
  totalmente en frío dentro de este fichero). Comando:
  ```
  python3 -c "
  import json
  primera=None
  with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
      for line in f:
          line=line.strip()
          if not line: continue
          o=json.loads(line)
          if o.get('type')=='assistant':
              m=o['message']
              if m.get('model')=='<synthetic>': continue
              primera=m.get('usage',{})
              break
  print('cache_read=',primera.get('cache_read_input_tokens',0),'cache_creation=',primera.get('cache_creation_input_tokens',0),'input=',primera.get('input_tokens',0))
  print('total=',primera.get('cache_read_input_tokens',0)+primera.get('cache_creation_input_tokens',0)+primera.get('input_tokens',0))"
  # -> cache_read= 20628 cache_creation= 17127 input= 2
  # -> total= 37757
  ```
- `cache_creation_input_tokens` de todas las peticiones reales (1.498 valores, hilo + subagentes):
  mínimo 141, máximo 427.779, mediana 2.379; solo 2 valores caen en la banda 70.000-100.000
  (74.940 y 78.691), no hay ningún valor agrupado cerca de 85.000. Comando (deduplicado por
  `requestId`, mismo método que los comandos 7 y 8 de la sección 3):
  ```
  python3 -c "
  import json, glob, statistics
  vals=[]
  byreq={}
  with open('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9.jsonl', encoding='utf-8') as f:
      for line in f:
          line=line.strip()
          if not line: continue
          o=json.loads(line)
          if o.get('type')=='assistant':
              rid=o.get('requestId')
              if rid and rid not in byreq:
                  m=o['message']
                  if m.get('model')=='<synthetic>': continue
                  byreq[rid]=m['usage'].get('cache_creation_input_tokens',0)
  vals.extend(byreq.values())
  for fp in glob.glob('/home/server/.claude/projects/-home-server-projects-bot-trading/1d064480-a2c4-42fd-a199-5fd72ce78fd9/subagents/*.jsonl'):
      byreq={}
      with open(fp, encoding='utf-8') as f:
          for line in f:
              line=line.strip()
              if not line: continue
              o=json.loads(line)
              if o.get('type')=='assistant':
                  rid=o.get('requestId')
                  if rid and rid not in byreq:
                      m=o['message']
                      if m.get('model')=='<synthetic>': continue
                      byreq[rid]=m['usage'].get('cache_creation_input_tokens',0)
      vals.extend(byreq.values())
  banda=[v for v in vals if 70000<=v<=100000]
  print('n=',len(vals),'min=',min(vals),'max=',max(vals),'mediana(int)=',int(statistics.median(vals)),'banda=',sorted(banda))"
  # -> n= 1498 min= 141 max= 427779 mediana(int)= 2379 banda= [74940, 78691]
  ```

Ninguna combinación de campos de `usage` en estos JSONL reproduce ~85.000. La explicación más
probable es que esa cifra no sale de sumar/contar estos dos ficheros: el hilo principal y sus
subagentes son continuación de UNA sesión ya caliente (con cache de CLAUDE.md/herramientas ya
escrita desde antes de la primera línea capturada aquí), mientras que el "suelo por conversación"
de 03.01.21 describe el coste de arrancar una sesión `claude -p` **nueva y aislada** (el modelo de
`03.01.23`, el encadenador desatendido) — un escenario que no está representado en ninguna de las
dos fuentes que se me han dado para esta tarea.

## HUECO

**HUECO: la cifra "suelo fijo ~85.000 tokens por conversación" no se ha podido reproducir ni
desmentir con aritmética a partir del hilo principal ni de los 75 transcripts de subagentes.**
Ninguna de las magnitudes disponibles en `usage` (primera petición real, arranque en frío,
`cache_creation_input_tokens` mínimo u otros) se acerca a esa cifra; el máximo de contexto de
arranque observado en cualquiera de las dos fuentes es 37.757. Para verificarla haría falta el
transcript de una sesión `claude -p` realmente nueva y aislada (una sola tarea, una sola
conversación, sin cache heredada), que no es ninguna de las dos fuentes que esta tarea autoriza a
usar.
