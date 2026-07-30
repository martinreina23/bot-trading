# Herencia de gb2 — qué adoptamos, qué evitamos y qué cambia en el plan

**Tarea 01.02.01 cerrada.** Fuente: `INFORME_GB2.md` (auditoría en solo lectura, 30/07/2026).

---

## 0. El titular: gb2 no es un desastre, y eso cambia la conversación

La auditoría desmonta la idea de partida. gb2 **no** es un proyecto mal hecho que haya que tirar. Es un sistema con disciplina de ingeniería seria: separación de poderes entre agentes, cuarentena de datos con firma humana, registros que solo permiten añadir, doble puerta de cierre, motor de backtest propio con costes reales, y una cultura de auto-corrección tan honesta que documentó su propio agujero de seguridad más grave en vez de taparlo.

**Lo que falló en gb2 no fue la calidad. Fue el reparto del esfuerzo.** El 70% del trabajo se fue al motor, se probó 1 de 13 hipótesis, y hubo que congelar el motor dos veces (una por decisión interna, otra por orden directa del usuario) sin conseguir frenarlo del todo.

Eso obliga a una pregunta que hay que responder antes de montar nada: **¿de verdad partimos de cero?** Ver ficha D6 al final.

---

## 1. Lo que ADOPTAMOS (ideas probadas, se copian tal cual)

| # | Idea de gb2 | Por qué la queremos |
|---|---|---|
| A1 | **Éxito = código fiel a la especificación, NO estrategia rentable.** Un backtest con resultado malo y código correcto es un éxito registrable | Es la vacuna estructural contra toquetear parámetros hasta que salga bonito. No la teníamos y es de lo mejor del informe |
| A2 | **Test de compuerta:** si la justificación de un cambio no se sostiene *sin citar métricas de resultado*, se deniega | Regla operativa afilada contra la racionalización a posteriori. Cabe en una frase y se puede aplicar |
| A3 | **Registros que solo permiten añadir** (registro de pruebas y de decisiones). Una corrección se añade como entrada nueva, nunca reescribiendo | Impide el borrado conveniente. Es lo que hace creíble el registro de pruebas fallidas que ya teníamos previsto |
| A4 | **Cuarentena de datos reservados con firma humana insustituible:** ni el debate de agentes ni ningún agente firmante puede autorizarlos. Solo tú | Más fuerte que nuestra versión. En gb2 los guardias de esto *sí mordían* (bloquearon 6 comandos en vivo durante la propia auditoría) |
| A5 | **Sesiones desechables con el estado en disco.** La autonomía de horas se logra encadenando contextos frescos, no alargando una sesión | Confirma nuestro diseño y coincide con la documentación oficial de Claude Code |
| A6 | **Lección = causa raíz + regla verificable + evento trazable.** "Una regla sin evento trazable no tiene autoridad" | Convierte LECCIONES.md en algo con criterio de entrada, no en un cajón de sensaciones |
| A7 | **Doble puerta de cierre:** puertas mecánicas en verde **Y** veredicto de un auditor adversarial. "Nadie se auto-aprueba" | Ya lo teníamos en espíritu; gb2 aporta la implementación |
| A8 | **Testbed sintético con resultado fijo conocido** (en gb2, "DUMMY": factor 0,914152 / 500 operaciones). Si tocas el motor y ese número cambia sin causa, has roto algo | Test de regresión de extremo a extremo. Barato y detecta lo que ninguna revisión humana ve |
| A9 | **Prueba de cordura del precio en el pipeline de datos.** En gb2 un divisor mal puesto ponía el oro a 17 $/onza y nadie lo vio | Una comprobación de dos líneas que habría ahorrado días |

## 2. Lo que EVITAMOS (los diez errores, traducidos a reglas nuestras)

| # | Error de gb2 | Regla que lo evita |
|---|---|---|
| E1 | El motor se comió al propósito (70% del esfuerzo, 1 de 13 hipótesis) | **Cada tirada autónoma cierra al menos una tarea que avanza el producto.** La infraestructura que no desbloquee mecánicamente una tarea de producto se registra como deuda y no se ejecuta sin permiso |
| E2 | Una capa de seguridad anunciada que nunca existió (el aislamiento del sistema no funcionaba en su entorno, y nadie lo comprobó en meses) | **Toda barrera se verifica por ejecución** —inyectando el caso prohibido y comprobando que se bloquea— antes de documentarla como activa. Sin prueba, se marca "no verificada" |
| E3 | Guardias verificados por presencia, no por ejecución; y cableados al evento equivocado | Mismo remedio que E2, más: **el guardia se cablea al vector real de la amenaza**, no al que parece obvio |
| E4 | Cada ronda de reparación introducía un defecto nuevo; tres tareas murieron por agotar rondas | **Quien implementa ejecuta y lee su artefacto completo antes de entregar.** Las puertas confirman, no descubren por primera vez |
| E5 | Citas inventadas a decisiones firmadas, dentro del código de producción (4 casos) | **Ninguna referencia a una decisión entra en código o informe sin un `grep` previo que la localice.** Solo se cita lo firmado y guardado, nunca en pasado ni antes de existir |
| E6 | Guardias afinados perdiendo el "bloquea todo salvo lo permitido"; exenciones que el propio agente activaba escribiendo una palabra en el mensaje | **Los guardias se escriben bloqueando por defecto.** La condición que activa una exención debe ser un hecho que imponga el sistema, nunca un dato que elija el vigilado |
| E7 | Diagnosticar un componente sin leerlo (se decidió cuál de dos scripts era el bueno leyendo sus cabeceras, y se concluyó lo contrario de la verdad) | **Un fallo reportado por un agente no es un fallo verificado:** antes de encolar o reparar, se lee el componente y se reproduce el fallo |
| E8 | Estado disperso en cinco registros que no cuadraban entre sí (dos días de desfase) | **Una sola fuente de verdad del estado, con campos que se puedan leer automáticamente**, no prosa. Al parar una tirada, la sección "en curso" se vacía o se archiva |
| E9 | Ficha de tarea creada al cerrar, no al empezar | **El identificador y la ficha se escriben en la cola ANTES de trabajar.** Sin ficha en la cola, no hay tarea |
| E10 | Referencias a código por número de línea, que cualquier commit desplaza | **Se referencia por nombre de símbolo, nunca por línea.** Toda retirada de un símbolo pasa un `grep` por todo el repositorio |

## 3. Errores de higiene que también evitamos

- **50.089 ficheros de datos versionados contra su propio `.gitignore`** (1,4 GB en cada clon). Los datos **nunca** entran en git; se descargan con un script y se ignoran de verdad, comprobándolo el día 1.
- **El fichero de tareas llegó a 218 KB y se leía entero en cada arranque de sesión.** Nuestro WBS se rota: la cola viva y el archivo histórico son ficheros distintos.
- **Dos encadenadores de sesión vivos a la vez** (uno antiguo sin retirar). Lo sustituido se borra.
- **Un agente fantasma** (`housekeeping`) nombrado en la documentación sin fichero que lo respalde. La lista de agentes se genera desde los ficheros reales, no se escribe a mano.
- **Triple copia del resumen de reglas** en tres ficheros. Una sola.

## 4. LA CORRECCIÓN MÁS IMPORTANTE: por qué no se activaban los agentes

**Nuestra hipótesis era incorrecta.** Dábamos por hecho que los agentes no se activaban por tener descripciones vagas. La auditoría demuestra otra cosa: los tres agentes inactivos de gb2 (`backtest-runner`, `datos`, `mql5-ea`) tenían **fichas claras y permisos suficientes**. No se activaron porque **la cola nunca contuvo una tarea de su tipo**, agravado por un defecto de enrutado que durante dos semanas mandó todo al implementador ignorando el tipo de tarea.

Es un fallo de **diseño de la cola**, no de los agentes. Cambia nuestra tarea 03.01.02: no basta con escribir buenas descripciones.

**Reglas nuevas:**
- El reparto de trabajo enruta **por tipo de tarea**, no solo por quién está libre.
- Antes de crear un agente se comprueba que **el WBS contiene tareas de su tipo**. Agente sin tareas previstas = agente que no se crea.
- Un agente que pasa **dos semanas sin ninguna tarea** se elimina o se justifica por escrito en la revisión del lunes.

## 5. Corrección sobre los modelos

gb2 tenía escrita la política correcta y no la cumplía: **7 de 13 agentes usaban alias** (`opus`, `sonnet`, `haiku`) en lugar del identificador exacto, justo lo que su propia norma prohibía porque *"un alias resuelve a lo que toque ese mes: deriva silenciosa que contamina la telemetría"*. Peor: el agente que **firmaba las decisiones** no tenía modelo asignado y heredaba el del hilo que lo llamara — nadie podía saber con qué modelo se firmó una decisión.

**Regla nuestra:** cada archivo de agente lleva el identificador exacto (`claude-fable-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`). Ningún agente sin modelo. Ningún alias.

## 6. Piezas de gb2 que podrían trasplantarse (no código copiado a ciegas)

Sujeto a la decisión D6, y cada una pasando por revisión del crítico antes de entrar:

1. **Dataset XAUUSD 2015-2022** ya descargado, verificado al 100% de cobertura, 0 duplicados, 0 spreads negativos. Reconstruirlo cuesta días.
2. **Motor de backtest con costes reales nativos**: entradas en el precio de compra y salidas en el de venta, ejecución de stops sin mejora de precio, coste de financiación asimétrico con triple miércoles, dimensionado de posición.
3. **El testbed sintético de invarianza** y su número de referencia.
4. **Los guardias de cuarentena de datos** que sí demostraron morder.
5. **Los 18 informes de investigación y las especificaciones** de las 13 hipótesis del embudo (F01-F13), como material de partida para nuestra fase de hipótesis — con la nota de que **12 de 13 nunca se llegaron a probar**.

---

## FICHA D6 — ¿Partimos de cero de verdad?

**Qué se decide:** cuánto de gb2 entra en el proyecto nuevo.

**A) Cero absoluto.** Repositorio vacío, se reescribe todo.
**B) Repositorio nuevo + trasplante de piezas verificadas.** Estructura, reglas y agentes desde cero; se traen únicamente el dataset validado, el motor de backtest, el testbed de invarianza y los guardias de datos, cada pieza revisada por el crítico antes de entrar. No se trae nada de la configuración de agentes, ni la cola de tareas, ni el historial.
**C) Seguir en gb2 y limpiarlo.**

**RECOMENDADA: B.** Tu plazo es un mes. Reescribir un motor de backtest con costes reales y volver a descargar y validar ocho años de datos se come ese mes entero y no te acerca ni un paso a saber si existe una estrategia que funcione. Y lo que querías evitar de gb2 —el desorden, la configuración enmarañada, el motor que se come el proyecto— no está en el motor: está en la capa de gestión, que es justo lo que **no** traemos.

**SI ELIGES OTRA:** A cuesta 2-3 semanas de las 4 que tienes y te deja sin datos ni motor para la fase de hipótesis. C arrastra los 50.000 ficheros versionados, el fichero de tareas de 218 KB y el historial entero: es exactamente el problema del que quieres salir.

**BLOQUEA:** el montaje del repositorio (03.01.01) y toda la fase 04.

**RESPUESTA:** _____
