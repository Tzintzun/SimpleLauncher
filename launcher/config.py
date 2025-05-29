import configparser
from pathlib import Path

_config = configparser.ConfigParser()
_config.read(Path("config.ini"))

def get_version_manifest_url() -> "str":
    """
    Retorna la URL para descargar el manifiesto de versiones.

    Returns:
        str: url del manifiesto de versiones.
    """
    return _config.get("URLS", "VERSIONS_MANIFEST_URL")

def get_config_java_path () -> "str":
    """
    Retorna la ruta de la intalacion de java configuruda en config.ini

    Returns:
        str: Path de java configurado.
    """
    return _config.get("JVM", "JAVA_PATH")

def get_game_dir () ->"str | None":
    """
    Retorna el direcctorio de juego configurado.
    
    Returns:
        str: Encontro un directorio configurado.
        None: No hay directorio configurado.

    """
    return _config.get("PATHS","GAME_DIR")

def get_launcher_version()-> "str":
    return _config.get("LAUNCHER_INFO","VERSION")

def get_launcher_name() -> "str":
    return _config.get("LAUNCHER_INFO","NAME")