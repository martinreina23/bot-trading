# Como instalar esto — 5 pasos

## 1. Descomprimir
Carpeta nueva, separada de gb2.

## 2. Arrancar git e instalar el muro mecanico
```
cd bot-trading
git init
git config core.hooksPath .githooks     # <-- IMPRESCINDIBLE: sin esto los hooks no corren
pip install -r requirements.txt
git add -A
git commit -m "arranque: estructura inicial del proyecto"
```

## 3. Probar que las barreras muerden (regla 25)
```
python3 03-motor/scripts/verificar_barreras.py
```
Cada barrera sale **VERIFICADA** o **NO VERIFICADA**. Lo que salga NO VERIFICADA se documenta como
tal, nunca como muro. Es la tarea **03.01.08**.

## 4. Comprobar los agentes en Claude Code
Abre Claude Code en la carpeta y pega:
```
Lee CLAUDE.md y 00-direccion/WBS.md enteros.
1. Dime cuantos agentes has cargado (deben ser 8) y cuantos comandos (deben ser 8).
2. Invoca a cada agente por su nombre con una tarea trivial y dime cuales responden.
3. Dime la siguiente tarea del WBS por su codigo y por que esa.
4. NO ejecutes nada todavia.
```
Si falta algun agente o comando, reinicia la sesion: Claude Code no carga lo creado a mitad de sesion.

## 5. Rellenar los tres huecos
Estos ficheros tienen un aviso dentro y su contenido esta en la conversacion del CEO:
- `01-investigacion/mercados/entrega_brief_A.md`
- `01-investigacion/mercados/entrega_brief_B.md`
- `01-investigacion/herencia-gb2/INFORME_GB2.md`

---

## Comandos disponibles

| Comando | Que hace |
|---|---|
| `/autonomo` | Una tirada de trabajo completa siguiendo el WBS, sin intervencion |
| `/estado` | Donde esta el proyecto, en una pantalla, incluidas las desalineaciones |
| `/fin` | Cierra la tarea en curso pasando las dos puertas |
| `/informe` | Informe semanal del CEO (lunes) |
| `/verificar` | Prueba por ejecucion que las barreras muerden |
| `/leccion` | Registra una leccion (exige causa raiz + regla + evento) |
| `/decision` | Registra una decision firmada (con test de compuerta) |
| `/ficha` | Prepara una decision para el CEO en el formato obligatorio |

## Que NO hacer todavia
- Nada de `awesome-claude-code` hasta que el proyecto funcione.
- Nada de broker hasta cerrar G1.
- Nada de ejecucion desatendida hasta que `/verificar` salga limpio.
