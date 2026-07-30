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
