import configparser
from model.version_manifests import VersionManifest
from model.version import Version
from model.library import Library
from services.download_service import download_json
from launcher.config import get_version_manifest_url


VERSIONS_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


def fetch_version_manifest() -> "VersionManifest | None":
    """
    Descarga el manifiesto de vertsiones.
    Returns:
        VersionManifest: Objeto que contiene los datos de las versiones.
    """
    version_manifest_url = get_version_manifest_url()
    version_manifest = download_json(version_manifest)

    if version_manifest is None:
        print(f"No se pudo obtener el Manifiesto de versiones de: {version_manifest}")
        return None
    
    return VersionManifest.form_dict(version_manifest)

def fetch_version_info(version_id: str, manifest: VersionManifest) -> "Version | None":
    """
    Descarga la infromacion de una version en concreto
    Arrgs:
        version_id (str): id de la version que se desea obtener la informacion.
        manifest (VersionManifest): manifiesto de las versiones disponibles.
    Returns:
        Version: Objeto con la informacion de la version.
    """
    version_url = manifest.versions_dcit[version_id].url if manifest.versions_dcit[version_id] else None
    if(version_id is None):
        return None
    version = download_json(version_url)

    return Version.from_dict(version)

def install_version(version: Version, game_dir: str) ->bool:
    """"
    Instalal un version del juego.
    Args:
        version (Version): Version del juego que se desea instalar.
        game_dir (str): direcctorio donde se desea instalar el juego.
    Returns:
        bool: True si el juego se instalo correctamente, False si el hubo algun error al instalar el juego.
    """
    #Desgargando Assets
    if not version.asset_index.fetch_assets(game_dir):
        print(f"No se pudo descargar los assets para la version: {version.id}")
        return False
    
    #Descargando librerias.
    for l in version.libraries:
        if not l.fetch_library(game_dir):
            print(f"No se pudo descargar la libreria {l.name}")
            return False
        
    #Descargando cliente.
    if not version.downloads.fetch_client(game_dir,version):
        print(f"No se pudo descargar el cliente")
        return False
    
    print(f"Minecraft {version.id} descargado correctamente")
    return True

    
