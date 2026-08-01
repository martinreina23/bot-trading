---
description: Genera el informe semanal del CEO para la revision del lunes
---

**Tu no escribes el informe: lo encarga el `secretario`.** Invocalo con la plantilla
`00-direccion/informes/PLANTILLA_informe_semanal.md` y las fuentes de abajo, y cuando te lo
devuelva **pasalo por tu filtro del Paso 5 de `/autonomo`** antes de enseñarselo al CEO: ¿responde a
lo que el CEO necesita saber?, ¿es plausible?, ¿falta algo que el CEO no deberia tener que
preguntar? Si no pasa, se lo devuelves al `secretario` con lo que falta.

## Fuentes (leelas todas)
- `00-direccion/WBS.md` — estados y avance.
- `git log --since="7 days ago" --oneline` — que se hizo de verdad.
- `04-resultados/registro-pruebas.md` — que se probo y que murio.
- `00-direccion/LECCIONES.md` — lecciones nuevas de la semana.

## Reglas del informe
- **UNA pagina.** El CEO tiene una hora. Si no cabe, recorta: no adjuntes, resume.
- La seccion "lo que murio y por que" es obligatoria. Si no murio nada, dilo y señalalo como
  sospechoso: o no se probo nada, o no se esta filtrando.
- **Reparto producto/motor en porcentaje.** Si el motor pasa del 20%, explica por que en dos lineas.
- Las decisiones van en formato ficha: opciones cerradas, recomendada con motivo, consecuencias,
  que se bloquea, respuesta de una letra. **Si tu ficha obliga al CEO a redactar, buscar o calcular
  algo, esta mal hecha: rehazla.**
- Nada de adjetivos de progreso ("buen avance", "vamos bien"). Numeros y hechos.

Guarda en `00-direccion/informes/informe_AAAA-MM-DD.md`.
