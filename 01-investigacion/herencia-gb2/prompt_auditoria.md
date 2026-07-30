# Prompt para Claude Code — Tarea 01.02.01 (análisis de gb2)

> Cómo usarlo: abre Claude Code en la carpeta del proyecto gb2 y pega todo lo que hay dentro del bloque. Cuando termine, tráeme el archivo `INFORME_GB2.md` que habrá creado.

```
Eres un auditor técnico independiente. Analizas este proyecto (lo llamamos "gb2") para un
proyecto NUEVO que se va a construir desde cero. No vas a copiar código: vas a extraer
información y lecciones.

REGLA ABSOLUTA: modo solo lectura. No modifiques, no borres, no muevas, no crees ni reorganices
NADA de este proyecto, salvo el único archivo de salida INFORME_GB2.md en la raíz. No ejecutes
el bot ni lances procesos que operen o toquen cuentas. Si algo requiere escribir para poder
analizarlo, no lo hagas: anótalo como limitación.

TONO: auditoría honesta, no informe de cortesía. El objetivo es encontrar lo que falló. Si algo
está mal hecho, dilo con claridad y con la prueba delante. No suavices. No inventes: si un dato
no está en los archivos, escribe "no consta" en vez de deducirlo.

EVIDENCIA: cada afirmación relevante lleva la ruta del archivo y, si aplica, el fragmento
concreto en el que te apoyas. Separa siempre lo que OBSERVAS (hecho comprobable en el código o
en la configuración) de lo que INTERPRETAS (tu hipótesis sobre por qué pasó).

Produce un único archivo llamado INFORME_GB2.md, en español, con estas nueve secciones y en
este orden:

1. MAPA DEL PROYECTO
   Estructura de carpetas real. Qué hay en cada una. Cuántos archivos y de qué tipo. Señala
   duplicados, versiones múltiples del mismo documento, archivos huérfanos y todo aquello que
   haga que un agente no pueda saber cuál es el archivo bueno. Nombra los casos concretos.

2. INVENTARIO DE AGENTES
   Tabla con una fila por agente definido en el proyecto: nombre, archivo donde está definido,
   descripción literal, modelo asignado, herramientas o permisos que tiene, y si se le llama de
   forma automática o explícita. Si el proyecto asigna modelos distintos a agentes distintos,
   documenta exactamente qué modelo lleva cada uno y qué razón se da (si se da alguna).

3. AGENTES QUE NUNCA SE ACTIVARON
   Busca evidencia de uso: registros, historiales, journals, logs, archivos de sesión, commits
   o cualquier rastro de ejecución. Para cada agente indica: hay rastro de que trabajara, sí o
   no. Para los que no tienen rastro, analiza la causa probable con la evidencia delante:
   descripción demasiado vaga o genérica, nombre o ruta incorrectos, permisos que lo bloquean,
   creado después de la última sesión activa, nunca referenciado por el orquestador, o solapado
   con otro agente que se lo comía. Sé concreto por agente, no en general.

4. CÓMO SE NOMBRABAN Y SEGUÍAN LAS TAREAS
   Cómo se identificaban las tareas (por ejemplo identificadores tipo "t55"), dónde se
   guardaban, si había una lista maestra, si existía criterio de "tarea terminada" y si se
   registraba el resultado. Explica qué hacía imposible saber, mirando el sistema, qué se
   estaba haciendo en cada momento.

5. EL MODO AUTÓNOMO
   Localiza el comando o flujo de trabajo autónomo (busca algo tipo /autonomo o equivalente).
   Qué instrucciones recibía exactamente. Qué priorizaba. Reconstruye con la evidencia
   disponible en qué gastó el tiempo realmente: mejorar el motor frente a avanzar el plan de
   trabajo. Aporta números si puedes (commits, archivos tocados, entradas de registro) y di
   claramente qué parte es dato y qué parte es estimación.

6. RESTRICCIONES Y PERMISOS
   Lista todas las restricciones que el sistema imponía a los agentes: permisos, listas de
   prohibiciones, hooks, reglas escritas en archivos de instrucciones. Para cada una: qué
   impedía, si hay rastro de que hubiera que relajarla o quitarla después, y qué problema real
   causó. Presta atención especial a si los agentes podían o no borrar y mover archivos, y a
   qué consecuencias tuvo.

7. QUÉ FUNCIONABA BIEN
   Piezas, ideas, estructuras o decisiones que merecen sobrevivir al proyecto nuevo. Explica por
   qué funcionaban. Distingue entre "esta idea es buena" y "este código es bueno".

8. LOS DIEZ ERRORES A NO REPETIR
   Los diez fallos más importantes, ordenados por daño causado al proyecto. Cada uno con: qué
   pasó, la evidencia, por qué hizo daño y qué regla concreta lo evitaría en un proyecto nuevo.
   Escribe la regla en una frase que se pueda copiar tal cual a un documento de normas.

9. LIMITACIONES DE ESTE ANÁLISIS
   Qué no has podido comprobar y por qué: archivos ausentes, sin registros, sin historial, sin
   acceso. Sé explícito, porque quien lea el informe necesita saber dónde no mirar.

REQUISITOS DE FORMA
- Español, palabras normales. Si usas un término técnico, explícalo entre paréntesis la primera
  vez.
- Tablas donde haya que comparar; texto corrido donde haya que explicar.
- Sin recomendaciones sobre qué construir en el proyecto nuevo: eso se decide fuera. Tu trabajo
  termina en las lecciones.
- Longitud: la que haga falta para que esté completo. No resumas para acortar.

Empieza recorriendo la estructura del proyecto antes de escribir nada, para que el informe se
apoye en lo que hay de verdad y no en lo que parece que debería haber.
```
