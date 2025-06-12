from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

__docformat__ = "Google-style"

@dataclass
class VersionInfo:

    """
    Almacena los datos de acceso de una version en especifico.
    """
    id: str
    """ID de la version relesea o snapshot"""
    type_version: str
    """Tipo version del juego release o snapshot"""
    url: str
    """Enlace de descarga del manifiesto de la version"""
    time_version: datetime
    release_time: datetime

    def __str__(self):
        return f"Version: {self.id}\nTipo: {self.type_version}\nURL: {self.url}\nRelease Time: {self.release_time}"
    
    def toHtml(self):
        """Retorna un parrafo HTML con la informacion de la version"""
        return f"""<p><span style="color: green">Version:</span> {self.id} <br>
                    <span style="color: green">Tipo:</span> {self.type_version}<br>
                    <span style="color: blue">URL:</span> <a href="{self.url}">{self.url}</a><br>
                    <span style="color: red">Release Time:</span> {self.release_time}</p>"""
    @staticmethod
    def from_dict(version_info:dict) ->"VersionInfo":
        """
        Obtiene un VersionInfo apartir de un diccionary.

        Args:
            version_info(dict)

        Returns:
            VersionInfo
        """
        time_version = datetime.fromisoformat(version_info["time"]) if version_info["time"] else datetime.now()
        release_time = datetime.fromisoformat(version_info["releaseTime"]) if version_info["releaseTime"] else datetime.now()
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
    """
    release_id: str
    """ID de la ultima version release"""
    snapshot_id: str
    """ID de la ultima version snapshot"""
    versions: List[VersionInfo]
    """Lista con todas las versiones del manifiesto"""
    versions_dcit: Dict[str, VersionInfo] = field(default_factory=dict)
    """Diccionario con todas las versiones del manifiesto, indexadas por ID de la varsion."""

    @staticmethod
    def form_dict(version_manifest:dict) -> "VersionManifest":
        """
        Obtiene un VersionManifest apartir de un diccionario.

        Args:

            version_manifest (dict)
        
        Returns:

            VersionManifest
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