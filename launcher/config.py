import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path("config.ini"))

def get_version_manifest_url() -> "str":
    """
    Retorna la URL para descargar el manifiesto de versiones.

    Returns:
        str: url del manifiesto de versiones.
    """
    return config.get("URLS", "VERSIONS_MANIFEST_URL")