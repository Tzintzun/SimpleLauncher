"""
Funciones principales del launcher.
"""

import os
from typing import Optional, Dict, List
from pathlib import Path
from services.version_services import fetch_version_manifest, fetch_version_data
from services.download_service import load_json
from services import jvm_services
from model.version_manifests import VersionManifest, VersionInfo
from model.version import Version
from model.user import User


__docformat__ = "Google-style"
def update_version_manifests(gameDir: Path) -> Optional[VersionManifest]:
    """
    Actualiza el manifiesto de versiones o lo descarga en caso de no existir.

    Args:
        gameDir (Path): Directorio donde se instalara el juego
    Returns:
        VersionManifest en caso de haber acutualizado correctamente el version_manifest, None sí no pudo actualizarlo.
    """
    if not isinstance(gameDir, (str, Path)):
        raise TypeError("gameDir tiene que ser un str o Path")
    
    manifest_path = Path(gameDir) / "versions" / "version_manifests.json"
    if not manifest_path.exists():
        os.makedirs(os.path.dirname(manifest_path.expanduser()), exist_ok=True)

    versionManifest = fetch_version_manifest(manifest_path.expanduser())
    return versionManifest

def load_version_manifest(gameDir: Path) -> Optional[VersionManifest]:
    """
    Carga el manifiesto de versiones desde el directorio del juego. Si no lo encuentro lo actualiza con update_version_manifests()

    Args:
        gameDir (Path): Directorio de la instalacion del juego.
    
    Returns:
        VersionManifest en caso de encontrar o actualizar un version_manifests.json, de lo contrario retorna None.
    """
    if not isinstance(gameDir, (str, Path)):
        raise TypeError("gameDir tiene que ser un str o Path")
    
    manifest_path = Path(gameDir) / "versions" / "version_manifests.json"
    if manifest_path.exists():
        manifest_json =  load_json(manifest_path)
        if isinstance(manifest_json, dict):
            return VersionManifest.form_dict(manifest_json)
        return None
    return update_version_manifests(gameDir)
    
def get_release_versions(versionManifest: VersionManifest) -> Optional[List[VersionInfo]]:
    """
    Obtiene las versiones release del manifiesto de versiones.

    Args:
        versionManifest (VersionManifest): Recive un manifiesto de versiones.
    Returns:
        List[VersionInfo] lista cons las versiones release
    """
    if not isinstance(versionManifest, VersionManifest):
        raise TypeError(f"Se esperaba un VersionManifest {type(versionManifest)}")
    return [versionInfo for versionInfo in versionManifest.versions if versionInfo.type_version == "release"]

def get_version_data (versionInfo: VersionInfo) -> Optional[Version]:
    """
    Obtiene el manifiesto de una version en especifico. 

    Args:
        versionInfo (VersionInfo): informacion de la version a descargar.
    
    Return:
        Version en caso de poder descargar el manifiesto de la version, None de lo contrario.
    """
    if not isinstance(versionInfo, VersionInfo):
        raise TypeError("Se esperaba un VersionInfo")
    return fetch_version_data(versionInfo.id, versionInfo.url)

def get_installed_versions(game_dir: Path) -> Optional[List[Version]]:
    """
    Obtiene las versiones del juego instaladas.

    Args:
        game_dir (Path): Directorio de la instalacion del juego.

    Returns: 
        List[Version] lista de versiones instaladas en el directorio.
    """
    version_manifest = load_version_manifest(game_dir)
    if version_manifest is None:
        return []
    if not isinstance(game_dir, (Path, str)):
        raise TypeError(f"Se esperaba un Path o str, se recibio {type(game_dir)}")
    versions_dir = Path(game_dir) /"versions"
    installed_list = []
    if not versions_dir.exists():
        return []
    try: 
        content = os.listdir(versions_dir)
        for item in content:
            version_data_path = versions_dir/item/ f"{item}.json"
            if version_data_path.exists():
                version_client = versions_dir/item/ f"{item}.jar"
                if version_client.exists():
                    version_data = load_json(version_data_path)
                    if version_data is not None:
                        try:
                            installed_list.append(Version.from_dict(version_data, "localhost"))
                        except Exception as e:
                            print(f"Error al instanciar la Version: {item}")
                            continue
        return installed_list
    except FileNotFoundError:
        print(f"Directorio no encontrado: {versions_dir}")
        return []
    

def init_launcher(version: Version, username: str, game_dir: Path):
    
    """
    Inicia una version del juego. 
    

    Args:
        version (Version): version del juego que se desea instalar.
        username (str): Nombre del usuario.
        game_dir (Path): Directorio donde se encuentra instalado el juego.
    """
    if game_dir is None:
        print("No se pudo cargar el directorio del juego.")

    launch_command = jvm_services.build_launc_comand(version, User(username), game_dir)

    if launch_command is None:
        print("No se pudo crear el comando de lanzamiento")
        return
    
    print(launch_command)
    jvm_services.run_minecraft(launch_command)
