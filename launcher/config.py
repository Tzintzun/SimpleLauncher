"""
Para almacenar  y consumir distintas configuraciones se utiliza configparser.
Todo se encuentra almacenado en config.ini. 
Algunas configuraciones como el username por defecto se encuentran vacias.
"""
import configparser
import os
import sys
from pathlib import Path

def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(sys.argv[0]).resolve().parent


_config = configparser.ConfigParser()
_config.read(get_base_path()/Path("config.ini"))

def get_version_manifest_url() -> "str":
    """
    Retorna un str con la URL para descargar el manifiesto de versiones.
    """
    return _config.get("URLS", "VERSIONS_MANIFEST_URL")

def set_version_manifest_url(url: str) -> bool:
    """
    Configura un str con la URL para descargr el manifiesto de versiones.
    """
    if not  isinstance(url, str):
        raise TypeError("Se esperaba un str.")
    _config.set("URLS", "VERSIONS_MANIFEST_URL", url)
    return True

def get_config_java_path () -> "str":
    """
    Retorna la ruta del binario de java configuruda.
    """
    return str(get_base_path() / _config.get("JVM", "JAVA_PATH"))

def set_config_java_path (java_path: Path) -> bool:
    """
    Configura un str como ruta al binario de java.

    Args:
        java_path (Path): path al binario de java.
    """
    if not isinstance(java_path, (Path, str)):
        raise TypeError("Se espera un Path o un str")
   
    _config.set("JVM", "JAVA_PATH", str(java_path))
    return True

def get_game_dir () ->"Path | None":
    """
    Retorna un Path con el direcctorio de juego configurado.
    Verifica que exista y crea el directorio en caso de no existir.
    """
    game_dir = Path(_config.get("PATHS","GAME_DIR")).expanduser().resolve()
    if(game_dir.exists()):
        return game_dir
    os.makedirs(game_dir, exist_ok=True)
    return game_dir

def set_game_dir(game_dir: Path) -> bool:
    if not isinstance(game_dir, Path):
        raise TypeError(f"se esperaba un Path o str")
    if not (game_dir.expanduser().resolve(strict=False).exists()):
        os.makedirs(game_dir.expanduser(), exist_ok= True)

    _config.set("PATHS","GAME_DIR",str(game_dir))
    return True


def get_user_name() -> str:
    """
    Obtiene un nombre de usuario almacenado. Por defecto esta vacio.
    """
    user_name = _config.get("USER","NAME")
    if user_name is None:
        user_name = ""
    return user_name

def set_user_name(user_name: str) -> bool:
    """
    Permite configurar el nombre de usuario.
    """
    if not isinstance(user_name, str):
        raise TypeError(f"Se esperana un Str, se recibio un {type(user_name)}")
    _config.set("USER", "NAME", user_name)
    return True


def get_launcher_version()-> "str":
    return _config.get("LAUNCHER_INFO","VERSION")

def get_launcher_name() -> "str":
    return _config.get("LAUNCHER_INFO","NAME")

def save_config():
    """
    Guarda todos los cambios relizados en el archivo de configuracion config.ini
    """
    with open("config.ini", "w") as configfile:
        _config.write(configfile)

def reload_config():
    """
    Recarga las configuracion desde config.ini
    """
    _config.read(Path("config.ini"))

