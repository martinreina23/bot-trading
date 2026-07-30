# Como instalar esto — 4 pasos

## 1. Descomprimir donde quieras que viva el proyecto
No dentro de la carpeta de gb2. Carpeta nueva y separada.

## 2. Arrancar git
```
cd bot-trading
git init
git add -A
git commit -m "arranque del proyecto"
```

## 3. Comprobar que los datos NO entran en git (regla 27)
```
git status --porcelain 02-datos/
```
Tiene que salir **vacio**. Si sale algo, avisa antes de seguir: en el proyecto anterior este
mismo fallo metio 50.089 ficheros y 1,4 GB en el repositorio.

## 4. Abrir Claude Code en la carpeta y pegar esto

```
Lee CLAUDE.md y 00-direccion/WBS.md enteros.

Despues:
1. Dime cuantos agentes has cargado y sus nombres (deben ser 8). Si falta alguno, reinicia la
   sesion: Claude Code no carga agentes creados a mitad de sesion.
2. Comprueba con una tarea de prueba que puedes invocar a cada uno de los 8 por su nombre, y
   dime cuales responden y cuales no. Ningun agente fantasma.
3. Dime cual es la siguiente tarea del WBS por su codigo, y por que es esa y no otra.
4. NO ejecutes nada todavia.
```

Esa comprobacion es la tarea **03.01.02** del WBS y es obligatoria antes de empezar: en el proyecto
anterior tres agentes nunca llegaron a activarse y nadie se dio cuenta hasta la auditoria.

---

## Lo primero que hay que rellenar a mano

Tres ficheros estan vacios con un aviso dentro. Su contenido vive en la conversacion del CEO y hay
que **copiarlo y pegarlo**:

- `01-investigacion/mercados/entrega_brief_A.md`
- `01-investigacion/mercados/entrega_brief_B.md`
- `01-investigacion/herencia-gb2/INFORME_GB2.md`

Hasta que se peguen, las tareas que dependen de ellos estan bloqueadas.

## Lo primero que hay que ejecutar

```
pip install yfinance pandas
python3 03-motor/scripts/atr_local.py
```
Es la tarea **02.02.01**: calcula el movimiento medio real por vela. **Aviso conocido:** el script
usa el futuro de oro (GC=F) como aproximacion del oro al contado. Esta pendiente de corregir con
datos de Dukascopy — anotalo en el informe si lo usas asi.

## Que NO hacer todavia

- Nada de `awesome-claude-code` hasta que el proyecto este funcionando en Claude Code.
- Nada de elegir broker hasta cerrar la puerta G1.
- Nada de ejecucion desatendida 24/7 hasta pasar la prueba de barreras (tarea 03.01.08).
