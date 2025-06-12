import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict
from services.download_service import download_file

__docformat__ = "Google-style"

@dataclass
class DownloadObject:
    """
    Contiene la información para descargar un jar de Minecraft
    """
    sha1: str
    """Hash de verificacion de la descarga."""
    size: int
    """Tamaño del archivo."""
    url: str
    """Direccion de descarga."""

    @staticmethod
    def from_dict(download_data: dict) -> "DownloadObject":
        """
        Conviente un diccionario a un objeto DownloadObject

        Args:

            download_data (dic): Diccionario que contiene la informacion de un DownloadObject
        """
        return DownloadObject(
            sha1= download_data["sha1"],
            size= download_data["size"],
            url= download_data["url"]
        )

@dataclass
class Downloads:
    """
    Información de las posibles descargas de una version de minecraft.
    """
    objects: Optional[Dict[str, DownloadObject]]
    """Diccionario con las posibles descagas del juego."""

    @staticmethod
    def from_dict(downloads: dict) -> "Downloads":
        """
        Convierte el atributo downloads{} del manifiesto de una version en formato JSON a un objeto de tipo Downloads.

        Args:

            donloads (dict): Diccionario con la informacion de las descargas del juego.

        Returns:

            Downloads
        """
        return Downloads(
            objects={key: DownloadObject(**value)
                     for key, value in downloads.items()}   if downloads else {}
        )
    
    def fetch_client(self, game_dir: Path, version_id: str, version_url:str) -> bool:
        """
        Descarga el cliente de una version.
        Args:

            game_dir (str | Path): Directorio de instlacion del juego.
            version (Version): Version del juego que se desea intalar.

        Returns:

            bool: True si el cliente se descargo correctamente, de lo contrario False.
        """

        if not isinstance(game_dir, (Path, str) ):
            raise TypeError("game_dir tiene que ser Path o str.")
        
        client = self.objects.get("client")
        if client is None:
            return False
        
        version_folder = os.path.join(game_dir, "versions", version_id)
        try:
            os.makedirs(version_folder, exist_ok=True)
        except OSError as e:
            print(f"No se pudo crear la ruta {version_folder}: {e}")
            return False
        
        #Descargando Manifest

        manifest_version_path = os.path.join(version_folder, f"{version_id}.json")
        if not download_file(version_url, manifest_version_path):
            print(f"No se pudo descargar: {version_url} en: {manifest_version_path}")
            return False

        version_path_jar = os.path.join(version_folder, f"{version_id}.jar")
        if not download_file(client.url, version_path_jar):
            print(f"No se pudo descargar el cliente: {client.url}")
            return False
        
        print(f"Cliente de la version {version_id} descargado correctamente")
        return True