import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List

from services.download_service import download_file

__docformat__ = "Google-style"

@dataclass
class LibraryDownloads:
    """
    Contiene la informacion de descarga de la libreria.
    """
    artifact: Optional[Dict]
    """Contiene el path, sha1, tamaño y url de descarga de la libreria."""
    classifiers: Optional[Dict]
    """ Se usa en versiones viejas (no implementado)"""

@dataclass
class Library:
    """
    Informacion de una libreria utilizada por el juego.
    """
    name: str
    """Nombre la libreria"""
    downloads: Optional[LibraryDownloads]
    rules: Optional[List[Dict]]
    """Reglas para usar la libreria"""
    natives: Optional[Dict]
    """Se usa en versiones antiguas de Minecraft (no implementado.)"""

    @staticmethod
    def from_dict(data:dict) -> "Library":
        """
        Obtiene un Library apartir de un diccionario.

        Args:

            data (dict):

        Returns:

            Library:
        """
        downloads_data = data.get("downloads")
        downloads = (LibraryDownloads(
            artifact= downloads_data.get("artifact"),
            classifiers= downloads_data.get("classifiers")
            )if downloads_data else None
        ) 
        return Library(
            name=data["name"],
            downloads=downloads,
            rules=data.get("rules"),
            natives=data.get("natives")
        )
    

    def fetch_library(self, game_dir: Path)-> bool:
        """
        Descarga la libreria.

        Args:

            game_dir (str): Directorio de instalacion de la version.

        Returns:

            bool: true si la libreria se descargo correctamte, de lo contrario False.
        """
        if not isinstance(game_dir, (Path, str) ):
            raise TypeError("game_dir tiene que ser Path o str.")
        if not self.downloads.artifact:
            return True
        
        url = self.downloads.artifact.get("url")
        if not url:
            return False
        
        path = self.downloads.artifact.get("path")
        if not path:
            return False
        
        full_path = os.path.join(game_dir, "libraries", path)
        if os.path.exists(full_path):
            print(f"Libreria desgargada: {full_path}")
            return True


        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except OSError as directory_error:
                print(f"No se pudo crear la ruta {os.path.dirname(full_path)}: {directory_error}")
                return False
        
        if not download_file(url, full_path):
            return False
        
        return True