import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path("config.ini"))

def get_version_manifest_url() -> "str":
    return config.get("URLS", "VERSIONS_MANIFEST_URL")