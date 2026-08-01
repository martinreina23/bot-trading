---
description: Prueba por ejecucion que las barreras del proyecto muerden de verdad (regla 25 de CLAUDE.md)
---

**Regla 25 de CLAUDE.md: una barrera no verificada por ejecucion NO es una barrera.** En el proyecto anterior,
una capa entera de seguridad estuvo documentada como activa durante meses sin funcionar nunca.

Ejecuta `python3 03-motor/scripts/verificar_barreras.py` y ademas comprueba a mano lo que el script
no puede probar:

1. **Cajon reservado.** Intenta leer `02-datos/reservado/` de tres formas: con la herramienta Read,
   con `cat` por terminal, y con un script de Python. **Las tres deben fallar.**
2. **Datos fuera de git.** Con ficheros reales en `02-datos/`, `git status --porcelain 02-datos/`
   debe salir vacio.
3. **Ficheros sensibles.** Intenta leer `.env`, `*.pem`, `*.key`. Deben bloquearse.
4. **Modelo por agente.** Invoca al `validador` y comprueba en el informe de uso si hubo consumo de
   la gama alta. Si no lo hubo, no corrio en el modelo de su ficha.

## Como reportar
Para cada barrera: **VERIFICADA** (se probo y bloqueo) o **NO VERIFICADA** (no bloqueo, o no se
pudo probar). Nunca "parece que funciona".

Escribe el resultado en `00-direccion/informes/barreras_AAAA-MM-DD.md` y, si alguna sale NO
VERIFICADA, **escala al CEO como excepcion inmediata**: estamos operando creyendo tener una
proteccion que no existe.
