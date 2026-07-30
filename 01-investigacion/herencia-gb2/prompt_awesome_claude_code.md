# Prompt para Claude Code — Tarea 01.02.03 (auditar el catálogo awesome-claude-code)

> **Aviso de carril:** esto es trabajo de MOTOR, no de producto. Por la regla 12 cuenta contra el 20% del esfuerzo y se limita a **una sola tirada**. Si empieza a crecer, se para.
>
> Cómo usarlo: pégalo en Claude Code. Salida: `INFORME_AWESOME.md`.

```
Eres un auditor técnico. Vas a evaluar el catálogo público «awesome-claude-code»
(https://github.com/hesreallyhim/awesome-claude-code) para un proyecto concreto, y tu trabajo NO
es resumir el catálogo: es filtrarlo con criterio y proponer como máximo CUATRO piezas.

CONTEXTO DEL PROYECTO QUE VA A USARLAS
Sistema de agentes que trabaja de forma desatendida en un ordenador de casa, dirigido por un WBS
en texto que es la única fuente de verdad. Ocho agentes con papeles separados (orquestador,
investigador, dos constructores, crítico de código, validador de estrategias, arquitecto,
secretario). El humano revisa una hora a la semana. Necesidades reales, por orden:
  1. Que los agentes no se desvíen del WBS y que el reparto enrute por TIPO de tarea.
  2. Memoria persistente entre sesiones (lecciones y decisiones que sobreviven al contexto).
  3. Barreras verificables sobre acciones irreversibles.
  4. Vigilancia del gasto y de los límites de uso sin que el humano tenga que mirar.
  5. Contraste entre agentes con papeles opuestos, sin que nadie se valide a sí mismo.

QUÉ TIENES QUE HACER
1. Recorre el catálogo entero, con atención especial a las categorías: Multi-Agent Orchestration,
   Memory & Context Persistence, Security, Usage & Cost Monitoring, Skills, Observability.
2. Para cada pieza que parezca aplicable a las 5 necesidades de arriba, comprueba ANTES de
   proponerla:
   - Fecha del último commit. Si lleva más de 6 meses parado, se descarta salvo que sea trivial.
   - Si el repositorio existe y es accesible (hay entradas de catálogo que apuntan a proyectos
     muertos).
   - Qué instala realmente y qué permisos necesita.
   - Si depende de servicios externos o de pago.
3. Descarta sin piedad. El catálogo tiene 45.000 estrellas y contiene tanto piezas serias como
   experimentos abandonados. La popularidad NO es criterio.

ENTREGA — fichero INFORME_AWESOME.md, en español, con tres secciones:

A) LAS CUATRO PROPUESTAS (máximo). Una ficha por pieza:
   - Nombre, enlace, última actividad.
   - Qué necesidad de las 5 resuelve, y cómo.
   - Qué habría que hacer para integrarla: pasos concretos y esfuerzo estimado en horas.
   - Qué riesgo introduce (permisos, dependencias, mantenimiento).
   - Qué pasa si NO la usamos: ¿se puede hacer lo mismo con 20 líneas propias? Si la respuesta es
     sí, dilo, porque entonces probablemente no compensa la dependencia.

B) DESCARTADAS CON MOTIVO. Lista de lo que miraste y no propones, con una línea de por qué
   (abandonado, redundante, demasiado permiso, resuelve un problema que no tenemos).

C) LO QUE EL CATÁLOGO NO CUBRE. Cuáles de las 5 necesidades se quedan sin una pieza decente. Es
   información valiosa: significa que hay que construirlo.

REGLAS DE LA AUDITORÍA
- Prohibido proponer algo sin haber comprobado su última actividad. Si no puedes comprobarla,
  dilo y márcalo «no verificado».
- Prohibido recomendar por popularidad o por descripción bonita.
- Máximo 4 propuestas. Si crees que hay 10 buenas, elige las 4 con mejor relación entre lo que
  resuelven y lo que cuestan.
- Si tras el barrido crees que NINGUNA merece la pena, dilo y entrega la sección C. Es un
  resultado perfectamente válido y probablemente el más honesto.
- Español, palabras normales, términos técnicos explicados la primera vez.
```
