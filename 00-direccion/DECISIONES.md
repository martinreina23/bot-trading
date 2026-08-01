# Registro de decisiones

**Solo se AÑADE. Nunca se reescribe una entrada.** Una correccion es una entrada nueva que cita a la
anterior. Regla 21 de CLAUDE.md.

Formato: `## D-N · AAAA-MM-DD · [decision en una linea]` + Motivo + Quien decide + Que bloqueaba.

---

## D-1 · 2026-07-29 · Producto antes que motor; el motor en paralelo con techo del 20%
**Motivo:** en el proyecto anterior el 70% del esfuerzo se fue al motor y se probo 1 de 13 hipotesis.
**Decide:** CEO.

## D-2 · 2026-07-29 · Portafolio de 3-5 mercados poco correlacionados, no un solo par
**Motivo:** repartir riesgo y ganar muestra de operaciones.
**Decide:** CEO.

## D-3 · 2026-07-29 · Mercado y tamaño de vela se deciden en la puerta G1 con datos, no de antemano
**Motivo:** evitar decisiones por corazonada.
**Decide:** CEO.

## D-4 · 2026-07-29 · El CEO revisa una hora los lunes y decide en las puertas; no firma tareas
**Motivo:** direccion por excepcion.
**Decide:** CEO.

## D-5 · 2026-07-29 · Horizonte de 1 mes con evaluacion el 1 de septiembre de 2026 (puerta GM)
**Motivo:** obligar a mirar los numeros pronto. NO es fecha de demo: el objetivo del mes es tener
veredicto sobre si existe una estrategia que merezca ir a demo.
**Decide:** CEO.

## D-6 · 2026-07-30 · Repositorio nuevo con trasplante de 5 piezas verificadas de gb2
**Motivo:** reescribir motor y datos desde cero se comeria el mes sin acercar la respuesta. Lo que
fallaba en gb2 no era el motor, era la capa de gestion, que no se hereda.
**Decide:** CEO. **Condicion:** cada pieza pasa su criterio de aceptacion, ejecutado aqui.

## D-7 · 2026-07-30 · Jerarquia de la prueba: ejecucion > verificacion documental > contraste entre agentes
**Motivo:** el consenso entre agentes no es prueba. En gb2 hubo tres diagnosticos seguidos del mismo
componente, dos falsos; los corrigio leer el codigo y reproducir el fallo, no debatir mas.
**Decide:** CEO.

## D-8 · 2026-07-30 · Cada agente lleva identificador exacto de modelo; ningun alias, ningun agente sin modelo
**Motivo:** en gb2, 7 de 13 agentes usaban alias contra su propia politica, y el agente que firmaba
decisiones no tenia modelo asignado.
**Decide:** direccion tecnica.

## D-9 · 2026-07-30 · Los datos nunca entran en git
**Motivo:** gb2 versiono 50.089 ficheros de datos (1,4 GB por clon) contra su propio .gitignore.
**Decide:** direccion tecnica.

## D-10 · 2026-07-31 · El cajon reservado se protege cifrandolo con una contraseña que solo tiene el CEO
**Motivo:** el 31/07 `verificar_barreras.py` demostro POR EJECUCION que el guardia anterior era un filtro sobre el TEXTO del comando: un comando que nombraba la ruta se bloqueaba, pero un programa que la construia por dentro entraba sin obstaculo. La condicion que activaba la exencion la elegia el vigilado, que es justo lo que prohibe la regla 26. Cifrar convierte el bloqueo en un hecho matematico que no depende de la buena voluntad de ningun agente.
**Decide:** CEO. **Condicion:** la contraseña no se guarda en ningun sitio (ni fichero, ni variable de entorno, ni sesion); cada operacion la vuelve a pedir; nada se descifra a disco; el cajon se queda dentro del proyecto. Toda apertura queda anotada en `04-resultados/registro-cajon.md`.
**Que bloqueaba:** 04.01.03 (partir el historico en tres cajones) y, detras, toda la puerta G2.

## D-11 · 2026-08-01 · Siete criterios de G1 aprobados (G1-C1 a G1-C7)
**Motivo:** definicion de la barra de elegibilidad de mercados y vela. **G1-C1** presupuesto de coste TOTAL al año ≤5% del capital, formula compuesta, con el coste de mantener DENTRO de ese mismo 5% (no aparte); anclado en la regla publicada de Robert Carver ("no gastar mas de un tercio del retorno esperado en costes") con retorno objetivo del 15% anual, que ES UN SUPUESTO ELEGIDO POR EL ORQUESTADOR Y APROBADO POR EL CEO, NO UN DATO MEDIDO. **G1-C2** coste de ida y vuelta ÷ ATR de la vela tranquila (percentil 10) ≤10%. **G1-C3** coste de mantener, sin umbral propio, suma dentro de G1-C1. **G1-C4** minimo 1.000 velas/año en la vela elegida, sin minimo de operaciones (ninguna fuente primaria lo respalda). **G1-C5** correlacion ≤0,7 entre los elegidos en las tres ventanas (3 meses, 1 año, 2 años), filtra la CESTA y no instrumentos sueltos. **G1-C6** tamaño minimo operable con capital de 1.000-2.000 €, medido con ATR MEDIANA, que no elimina instrumentos sino que impone requisito al broker de 04.01.01. **G1-C7** criterio nuevo del hueco de fin de semana: percentil 90 del salto del lunes ÷ stop de 1xATR ≤0,5, que no cumple ningun instrumento. Recorrido: constructor-datos, investigador, critico-codigo y validador; la propuesta del orquestador fue corregida en cuatro puntos por el critico y el validador antes de llegar al CEO. Lo que SALE de G1: "operable sin nadie delante", que pasa a la Fase 03. Hueco declarado: el deslizamiento, sin factor publicado, se mide con precios del broker real en la tarea 04.01.02 y obliga a re-verificar G1 si algun resultado cambia.
**Decide:** CEO.
**Que bloqueaba:** 02.03.01 (revision transversal, RECHAZA 31/07 por criterios sin numerar ni aprobar) y puerta G1 completa.

## D-12 · 2026-08-01 · Fecha tope el 01/12/2026, con revision de avance el dia 1 de cada mes
**Motivo:** D-5 fijaba la evaluacion GM del 01/09/2026 pero NO fijaba ninguna fecha de parada, y las
tres salidas de GM (arrancar demo, dar otra vuelta, replantear) tampoco cerraban el proyecto: no
existia fecha tope en ningun documento. Sin fecha de parada el proyecto puede derivar
indefinidamente, que es lo que ocurrio en gb2.
**Forma operativa:** revision de avance el dia 1 de cada mes (01/09 = GM, 01/10, 01/11), cada una
con poder explicito de PARAR el proyecto ademas de las tres salidas que GM ya tenia. La pregunta de
cada revision la fija el CEO: "¿avanza por buen camino?". El 01/12/2026 es fecha tope dura: si a esa
fecha no hay ninguna estrategia en demo, el proyecto se cierra y se escribe el informe de por que.
**Decide:** CEO (opcion B de la ficha, con el seguimiento mensual añadido por el CEO).
**Que bloqueaba:** cierre de 01.01.03 y puerta G0.
**Consecuencia:** GM gana una cuarta salida explicita (parar) y el proyecto gana una fecha tope que
antes no existia. No toca G4, que sigue siendo la puerta mensual de la fase de dinero real.

## D-13 · 2026-08-01 · Tope de 5 fichas por revision del lunes; la hora es minimo garantizado, no techo
**Motivo:** D-4 fija 1 h los lunes, pero lo que se desborda no es el tiempo sino el numero de
decisiones acumuladas: cerrar solo la tarea 01.01.03 genero 3 fichas en un dia.
**Forma operativa:** maximo 5 fichas de decision por revision del lunes; si hay mas, el orquestador
prioriza y las sobrantes esperan al lunes siguiente. El CEO declara que ademas sigue el proyecto dia
a dia y que pasar de la hora no le supone problema: la hora del lunes es un MINIMO GARANTIZADO, no
un techo.
**Decide:** CEO (opcion B de la ficha, con la aclaracion del CEO de que la hora no es techo).
**Que bloqueaba:** cierre de 01.01.03 y puerta G0.
**Aviso registrado:** el modelo de autonomia de CLAUDE.md esta construido sobre un CEO escaso. Con
un CEO disponible a diario el riesgo deja de ser su tiempo y pasa a ser que el equipo consulte en
vez de decidir. Se mantiene SIN CAMBIO la lista de lo que el equipo cierra sin consultar: que el CEO
este disponible no amplia lo que se le puede preguntar.

## D-14 · 2026-08-01 · Dinero real: aviso a -25% y parada dura automatica a -30% del capital inicial
**Motivo:** el WBS registraba una contradiccion viva sin resolver — parada dura propuesta en -25%
frente a una tolerancia del 50-60% mencionada por el CEO. El CEO fija el nivel entre el 25% y el 30%
y pide explicitamente que no se pare solo, porque una estrategia puede bajar y recuperar. Eso obliga
a DOS niveles, no a uno.
**Forma operativa:** (1) AVISO a -25% del capital inicial ingresado: NO para nada, se reporta al CEO
y decide el CEO. (2) PARADA DURA a -30% del capital inicial: el bot deja de abrir posiciones,
automaticamente y sin exencion activable desde dentro (regla 26). Se mide sobre el CAPITAL INICIAL
INGRESADO, no sobre el maximo alcanzado. Recuperar desde -30% exige +43%.
**Decide:** CEO (opcion A de la ficha refinada). SIN recomendacion del equipo:
`.claude/commands/ficha.md` prohibe recomendar en decisiones de tolerancia al riesgo.
**Que bloqueaba:** cierre de 01.01.03 y puerta G0. Da numero a G4, que hasta hoy decia "si pierde
mas de lo escrito en 01.01.03" sin que existiera nada escrito.
**Requisito tecnico que genera:** la parada dura la aplica EL BOT de forma continua, no la revision
mensual. Comprobada una vez al mes, una caida del -30% puede ser del -45% cuando alguien mire. Pasa
a ser requisito de 05.01.01 y 06.01.01, y se verifica por inyeccion antes de declararla activa
(regla 25).
**Declarado como NO resuelto:** el CEO declara que su tolerancia real llega mas abajo ("mientras no
pierda la cuenta entera"). La parada de -30% NO refleja esa tolerancia: la limita a proposito,
porque la condicion con la que el CEO toleraria mas ("si se que puede recuperar") no se puede
conocer por adelantado ni la puede verificar el sistema.
