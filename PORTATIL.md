# Trabajar desde el portátil (semana del 15/08/2026, server apagado)

> Este fichero existe porque el servidor de casa se apaga durante un viaje y el trabajo sigue
> en un portátil. **Lee los cuatro pasos en orden.** El paso 2 no es opcional: sin él, los tres
> muros mecánicos del proyecto desaparecen sin avisar y nadie te lo dice.

## 0. Dar de alta el portátil en GitHub (solo la primera vez)

El repo es **privado**: `https://github.com/martinreina23/bot-trading`. La clave SSH del
servidor **no está en el portátil** y no debe copiarse. El portátil necesita su propia
credencial. Lo más rápido, desde el portátil:

```bash
ssh-keygen -t ed25519 -C "portatil"      # Enter a todo
cat ~/.ssh/id_ed25519.pub                 # copia la linea entera
```

Pega esa línea en **https://github.com/settings/ssh/new** (título: «portátil») y comprueba:

```bash
ssh -T git@github.com                     # debe responder: Hi martinreina23!
```

## 1. Clonar

```bash
git clone git@github.com:martinreina23/bot-trading.git
cd bot-trading
```

## 2. Activar los muros — OBLIGATORIO, Y ES LO PRIMERO

`core.hooksPath` es configuración **local** de git: **no se clona**. Un repo recién clonado
tiene los ficheros de `.githooks/` en disco pero **git no los ejecuta**. Sin este comando,
los tres muros de la sección «Qué tiene muro mecánico» de `CLAUDE.md` —datos fuera de git,
código WBS en el mensaje de commit, registros que solo admiten añadir— son **solo prosa**.

```bash
git config core.hooksPath .githooks
chmod +x .githooks/*
```

**Compruébalo por ejecución antes de trabajar** (regla 24 de CLAUDE.md), no te fíes de que el
comando no diera error:

```bash
git config --get core.hooksPath          # debe imprimir: .githooks
git commit --allow-empty -m "prueba sin codigo wbs"
# DEBE fallar con: BLOQUEADO (regla 1). Si te deja commitear, el paso 2 no ha funcionado: PARA.
```

Si el commit de prueba pasa por error, deshazlo con `git reset --hard HEAD~1`.

## 3. Entorno de Python

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Python 3.12 en el servidor. Todo se ejecuta con `.venv/bin/python`, nunca con el `python3` del
sistema.

## 4. Los datos

`02-datos/` **no está en git y no debe estarlo** (regla 26 de CLAUDE.md). Viajan aparte, en
`datos-bot-trading-2026-08-15.tar` (89 MB, 811 ficheros). Desde la raíz del repo clonado:

```bash
tar -xf /ruta/al/datos-bot-trading-2026-08-15.tar
```

El `.tar` está en la raíz del repo del servidor, pero **no está en git**: lo tapa `*.tar` en
`.gitignore`, porque el guardia de datos de `.githooks/pre-commit` solo mira rutas que empiezan
por `02-datos/` y un `.tar` en la raíz no lo dispara. Cópialo a mano al pendrive o a la nube.

Debe dejarte `02-datos/bruto/` con 8 instrumentos y `02-datos/limpio/`.

**`02-datos/reservado/` NO viaja y es deliberado.** El cajón sellado se queda en el servidor
apagado, que es el sitio más seguro para él. Un portátil que viaja se pierde o se roba. Por
tanto, **durante esta semana ninguna tarea que toque el cajón reservado se puede ejecutar**
(regla 21 de CLAUDE.md) — no por falta de permiso, sino porque el fichero no está.

## Al volver a casa

El servidor ha estado apagado, así que **no puede haber divergencia**: el portátil es la única
rama que ha avanzado. En el servidor:

```bash
git pull --ff-only origin main
```

Si `--ff-only` falla, **para y avisa**: significa que alguien tocó el servidor mientras no
estabas y hay que mirarlo a mano antes de mezclar nada.

Los datos no hace falta traerlos de vuelta: el servidor conserva los suyos y son los mismos.

## Diferencias del portátil que conviene saber

- **La memoria de sesión no viaja.** Vive en `~/.claude/projects/…/memory/` del servidor, fuera
  del repositorio. En el portátil, Claude Code arranca sin ella.
- **Los permisos de usuario tampoco.** `.claude/settings.json` sí viaja (está en el repo), pero
  la configuración de usuario del servidor no: en el portátil te pedirá permiso más a menudo.
  Es ruido, no un fallo.
