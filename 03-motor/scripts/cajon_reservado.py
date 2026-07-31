#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guardia del cajon reservado (reglas 22, 25 y 26).

EL PROBLEMA QUE CIERRA
El 31/07/2026 `verificar_barreras.py` demostro por ejecucion que el cajon reservado NO estaba
protegido: el bloqueo era un filtro sobre el TEXTO del comando. Un comando que nombraba la ruta
se bloqueaba; un programa que la construia por dentro entraba sin obstaculo. Es decir, la
condicion que activaba la exencion la elegia el vigilado, que es exactamente lo que prohibe la
regla 26.

COMO LO CIERRA
El cajon deja de protegerse con una norma y pasa a protegerse con matematicas. Todo fichero de
02-datos/reservado/ se guarda CIFRADO con una contraseña que solo conoce el CEO. Quien lea la
carpeta sin ella —agente, script o terminal— obtiene ruido.

PROPIEDADES QUE SE MANTIENEN (decision del CEO, 31/07/2026)
  · La contraseña NO se guarda en ningun sitio: ni fichero, ni variable de entorno, ni memoria
    entre ejecuciones. Se teclea, se usa y se descarta.
  · No hay sesion ni "puerta abierta": cada operacion la pide otra vez.
  · Nada se descifra a disco. `abrir()` devuelve los datos en memoria y nada mas.
  · Toda apertura y todo guardado quedan anotados en 04-resultados/registro-cajon.md, que solo
    admite añadir (regla 21). La contraseña nunca se anota.
  · El cajon se queda dentro del proyecto, como pidio el CEO.

USO
    python3 03-motor/scripts/cajon_reservado.py sellar          # fija la contraseña por primera vez
    python3 03-motor/scripts/cajon_reservado.py comprobar       # ¿es correcta la contraseña?
    python3 03-motor/scripts/cajon_reservado.py guardar <fich>  # mete un fichero cifrado
    python3 03-motor/scripts/cajon_reservado.py listar          # que hay dentro (sin contraseña)

Para LEER datos, un script de prueba debe importar `abrir()`. No existe ninguna orden de linea de
comandos que vuelque el contenido descifrado: asi no se puede redirigir a un fichero por descuido.
"""
import os
import sys
import base64
import getpass
import hashlib
from datetime import datetime, timezone

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CAJON = os.path.join(RAIZ, "02-datos", "reservado")
REGISTRO = os.path.join(RAIZ, "04-resultados", "registro-cajon.md")
CANARIO = "_sello.enc"

SAL_BYTES = 16
SCRYPT_N = 2 ** 15          # coste de derivacion: hace lenta la fuerza bruta
SCRYPT_R = 8
SCRYPT_P = 1


# --------------------------------------------------------------------------- clave

def _derivar(password: str, sal: bytes) -> bytes:
    """Convierte la contraseña en clave. Sal distinta por fichero: dos ficheros iguales
    cifrados con la misma contraseña no se parecen en nada."""
    bruto = Scrypt(salt=sal, length=32, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P).derive(
        password.encode("utf-8")
    )
    return base64.urlsafe_b64encode(bruto)


def _pedir_password(confirmar: bool = False) -> str:
    """Pide la contraseña por terminal, sin eco. Nunca se devuelve a ningun registro."""
    if not sys.stdin.isatty():
        raise SystemExit(
            "BLOQUEADO: la contraseña solo se teclea en una terminal real.\n"
            "   No se acepta por tuberia, fichero ni variable de entorno: eso la dejaria guardada."
        )
    p = getpass.getpass("Contraseña del cajon reservado: ")
    if not p:
        raise SystemExit("Contraseña vacia. Cancelado.")
    if confirmar:
        if p != getpass.getpass("Repitela: "):
            raise SystemExit("No coinciden. Cancelado, no se ha escrito nada.")
    return p


# --------------------------------------------------------------------------- registro

def _anotar(operacion: str, fichero: str, motivo: str, resultado: str) -> None:
    """Añade una linea al registro. Solo se añade, nunca se reescribe (regla 21)."""
    if not os.path.exists(REGISTRO):
        with open(REGISTRO, "w", encoding="utf-8") as f:
            f.write(
                "# Registro del cajon reservado\n\n"
                "**Solo se AÑADE. Nunca se reescribe.** Regla 21.\n\n"
                "Cada linea es una apertura o un guardado del cajon de datos reservados (OOS).\n"
                "Sirve para comprobar la regla de **una sola pasada por variante**: si un codigo\n"
                "de variante aparece dos veces en una lectura, la segunda prueba no vale.\n\n"
                "La contraseña no aparece aqui ni puede deducirse de aqui.\n\n"
                "| Fecha (UTC) | Operacion | Fichero | Motivo / variante | Resultado |\n"
                "|---|---|---|---|---|\n"
            )
    sello = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(f"| {sello} | {operacion} | {fichero} | {motivo} | {resultado} |\n")


# --------------------------------------------------------------------------- guardar / abrir

def guardar(ruta_origen: str, motivo: str = "carga de datos") -> str:
    """Cifra un fichero y lo mete en el cajon. Pide la contraseña."""
    if not os.path.isfile(ruta_origen):
        raise SystemExit(f"No existe el fichero: {ruta_origen}")
    if os.path.abspath(ruta_origen).startswith(os.path.abspath(CAJON)):
        raise SystemExit("El origen ya esta dentro del cajon. Cancelado.")

    nombre = os.path.basename(ruta_origen) + ".enc"
    destino = os.path.join(CAJON, nombre)
    if os.path.exists(destino):
        raise SystemExit(
            f"Ya existe {nombre} en el cajon. No se sobrescribe: borra el anterior a mano si de\n"
            "   verdad quieres reemplazarlo (y anota por que)."
        )

    password = _pedir_password()
    datos = open(ruta_origen, "rb").read()
    huella = hashlib.sha256(datos).hexdigest()[:16]

    sal = os.urandom(SAL_BYTES)
    token = Fernet(_derivar(password, sal)).encrypt(datos)
    del password

    os.makedirs(CAJON, exist_ok=True)
    with open(destino, "wb") as f:
        f.write(sal + token)

    _anotar("GUARDAR", nombre, motivo, f"cifrado, sha256[:16]={huella}")
    print(f"Guardado cifrado: 02-datos/reservado/{nombre}  ({len(datos)} bytes en claro)")
    print("   El original NO se ha borrado. Borralo tu si no debe quedar copia en claro.")
    return destino


def abrir(nombre: str, motivo: str) -> bytes:
    """Descifra un fichero del cajon y devuelve su contenido EN MEMORIA.

    `motivo` es obligatorio y debe identificar la variante que se va a probar: queda anotado en
    el registro y es lo que permite comprobar la regla de una sola pasada por variante.

    NO escribe nada descifrado en disco. Si quien llama lo guarda, es cosa suya y va contra la
    regla 22: que este metodo no lo haga es deliberado.
    """
    if not motivo or motivo.strip() in ("", "-"):
        raise SystemExit(
            "BLOQUEADO: abrir el cajon exige declarar el motivo (codigo de variante).\n"
            "   Sin motivo no se puede comprobar la regla de una sola pasada por variante."
        )
    if not nombre.endswith(".enc"):
        nombre += ".enc"
    ruta = os.path.join(CAJON, nombre)
    if not os.path.exists(ruta):
        raise SystemExit(f"No existe en el cajon: {nombre}")

    password = _pedir_password()
    crudo = open(ruta, "rb").read()
    sal, token = crudo[:SAL_BYTES], crudo[SAL_BYTES:]
    try:
        datos = Fernet(_derivar(password, sal)).decrypt(token)
    except InvalidToken:
        _anotar("ABRIR", nombre, motivo, "RECHAZADO: contraseña incorrecta")
        raise SystemExit("Contraseña incorrecta. No se ha descifrado nada.")
    finally:
        del password

    _anotar("ABRIR", nombre, motivo, f"descifrado en memoria, {len(datos)} bytes")
    return datos


# --------------------------------------------------------------------------- ordenes

def sellar() -> None:
    """Fija la contraseña por primera vez cifrando un sello de prueba.

    No guarda la contraseña: guarda un fichero cifrado CON ella. Sirve para dos cosas: probar que
    el mecanismo funciona de punta a punta, y poder comprobar mas adelante que la recuerdas antes
    de que haya datos de verdad dentro.
    """
    destino = os.path.join(CAJON, CANARIO)
    if os.path.exists(destino):
        raise SystemExit(
            "El cajon ya esta sellado. Usa `comprobar` para verificar la contraseña.\n"
            "   Para cambiarla habria que descifrar y volver a cifrar todo el contenido."
        )
    password = _pedir_password(confirmar=True)
    sal = os.urandom(SAL_BYTES)
    marca = f"sello del cajon reservado · {datetime.now(timezone.utc).isoformat()}".encode("utf-8")
    token = Fernet(_derivar(password, sal)).encrypt(marca)
    del password

    os.makedirs(CAJON, exist_ok=True)
    with open(destino, "wb") as f:
        f.write(sal + token)
    _anotar("SELLAR", CANARIO, "fijar la contraseña del cajon", "sellado")
    print("\nCajon sellado.")
    print("  · La contraseña NO se ha guardado en ningun sitio. Si la pierdes, el contenido")
    print("    cifrado es irrecuperable (los datos de mercado se pueden volver a descargar).")
    print("  · A partir de ahora, guardar o abrir cualquier cosa te la pedira otra vez.")


def comprobar() -> None:
    """Comprueba que la contraseña es la correcta, sin revelar nada."""
    ruta = os.path.join(CAJON, CANARIO)
    if not os.path.exists(ruta):
        raise SystemExit("El cajon no esta sellado todavia. Ejecuta primero: sellar")
    password = _pedir_password()
    crudo = open(ruta, "rb").read()
    try:
        Fernet(_derivar(password, crudo[:SAL_BYTES])).decrypt(crudo[SAL_BYTES:])
    except InvalidToken:
        _anotar("COMPROBAR", CANARIO, "verificacion de contraseña", "RECHAZADO: incorrecta")
        raise SystemExit("Contraseña INCORRECTA.")
    finally:
        del password
    _anotar("COMPROBAR", CANARIO, "verificacion de contraseña", "correcta")
    print("Contraseña correcta. El cajon responde.")


def listar() -> None:
    """Que hay en el cajon. No pide contraseña: los nombres no son secretos, el contenido si."""
    if not os.path.isdir(CAJON):
        raise SystemExit("No existe el cajon.")
    hay = False
    print("Contenido del cajon reservado (todo cifrado):")
    for n in sorted(os.listdir(CAJON)):
        if n in ("README.md", ".gitkeep"):
            continue
        hay = True
        print(f"  · {n}  ({os.path.getsize(os.path.join(CAJON, n))} bytes cifrados)")
    if not hay:
        print("  (vacio)")


def _uso():
    print(__doc__.strip().split("USO")[-1].strip())
    sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _uso()
    orden = sys.argv[1]
    if orden == "sellar":
        sellar()
    elif orden == "comprobar":
        comprobar()
    elif orden == "listar":
        listar()
    elif orden == "guardar":
        if len(sys.argv) < 3:
            raise SystemExit("Uso: guardar <fichero>")
        guardar(sys.argv[2], motivo=sys.argv[3] if len(sys.argv) > 3 else "carga de datos")
    else:
        _uso()
