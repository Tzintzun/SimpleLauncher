import os
from dataclasses import dataclass, field
from typing import Optional, Dict

from model.version import Version
from services.download_service import download_file

@dataclass
class DownloadObject:
    """
    Contiene la información para descargar un jar de Minecraft
    Attributes:
        sha1 (str): hash de verificacion de la descarga.
        size (int): tamaño del archivo.
        url (str): direccion de descarga.
    """
    sha1: str
    size: int
    url: str

    @staticmethod
    def from_dict(download_data: dict) -> "DownloadObject":
        return DownloadObject(
            sha1= download_data["sha1"],
            size= download_data["size"],
            url= download_data["url"]
        )

@dataclass
class Downloads:
    """
    Información de las posibles descargas de una version de minecraft.
    Attributes:
        objects (Optional[Dict[str, DownloadObject]]): Diccionario con las posibles descagas del juego.
    """
    objects: Optional[Dict[str, DownloadObject]]

    @staticmethod
    def from_dict(downloads: dict) -> "Downloads":
        """
        Convierte el atributo downloads{} del manifiesto de una version en formato JSON a un objeto de tipo Downloads.

        Args:
            donloads (dict): Diccionario con la informacion de las descargas del juego.

        Returns:
            Downloads:
        """
        return Downloads(
            objects={key: DownloadObject(**value)
                     for key, value in downloads.items()}   if downloads else {}
        )
    
    def fetch_client(self, game_dir: str, version: Version) -> bool:
        """
        Descarga el cliente de una version.
        Args:
            game_dir (str): Directorio de instlacion del juego.
            version (Version): Version del juego que se desea intalar.
        Returns:
            bool: True si el cliente se descargo correctamente, de lo contrario False.
        """
        client = self.objects.get("client")
        if not client:
            return False
        
        version_folder = os.path.join(game_dir, "versions", version.id)
        try:
            os.makedirs(version_folder, exist_ok=True)
        except OSError as e:
            print(f"No se pudo crear la ruta {version_folder}: {e}")
            return False
        
        #Descargando Manifest

        manifest_version_path = os.path.join(version_folder, f"{version.id}.json")
        if not download_file(version.url, manifest_version_path):
            print(f"No se pudo descargar: {version.url} en: {manifest_version_path}")
            return False

        version_path_jar = os.path.join(version_folder, f"{version.id}.jar")
        if not download_file(client.url, version_path_jar):
            print(f"No se pudo descargar el cliente: {client.url}")
            return False
        
        print(f"Cliente de la version {version.id} descargado correctamente")
        return True