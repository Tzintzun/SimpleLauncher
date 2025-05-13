from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

@dataclass
class VersionInfo:

    """
    Almacena los datos de acceso de una version en especifico.
    Attributes:
        id (str): ID de la version relesea o snapshot
        type_version (str): version del juego release o snapshot
        url (str): enlace de descarga del manifiesto de la version
        time_version (str):
        release_version (str):
    """
    id: str
    type_version: str
    url: str
    time_version: datetime
    release_time: datetime

    @staticmethod
    def from_dict(version_info:dict) ->"VersionInfo":
        """
        Obtiene un VersionInfo apartir de un diccionari.

        Args:
            version_info (dict):

        Returns:
            VersionInfo:
        """
        time_version = datetime.fromisoformat(version_info["time"]) if version_info["time"] else datetime.now()
        release_time = datetime.fromisoformat(version_info["releaseTime"]) if version_info["releaseTime	"] else datetime.now()
        return VersionInfo(
            id=version_info["id"],
            type_version= version_info["type"],
            url=version_info["url"],
            time_version=time_version,
            release_time=release_time
        )

@dataclass
class VersionManifest:
    """
    Contiene una lista de todas las versiones.
    release_id (str): ID de la ultima version release
    snapshot_id (str): ID de la ultima version snapshot
    versions (List[VersionInfo]): Lista con todas las versiones del manifiesto
    versions_dict (Dict): Diccionario con todas las versiones del manifiesto, donde la llave de acceso a cada version es el ID de la varsion misma.
    """
    release_id: str
    snapshot_id: str
    versions: List[VersionInfo]
    versions_dcit: Dict[str, VersionInfo] = field(default_factory=dict)

    @staticmethod
    def form_dict(version_manifest:dict) -> "VersionManifest":
        """
        Obtiene un VersionManifest apartir de un diccionario.

        Args:
            version_manifest (dict):
        
        Returns:
            VersionManifest:
        """
        versions = [VersionInfo.from_dict(version) for version in version_manifest.get("versions", {})]
        versions_dict = {version.id : version
                         for version in versions}
        latest_versions = version_manifest.get("latest",{})
        return VersionManifest(
            release_id=latest_versions.get("release", ""),
            snapshot_id=latest_versions.get("snapshot", ""),
            versions=versions,
            versions_dcit=versions_dict
        )