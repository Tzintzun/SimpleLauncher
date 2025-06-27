import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict
from services.download_service import download_json, download_file

ASSETS_URL = "https://resources.download.minecraft.net"

__docformat__ = "Google-style"

@dataclass
class AssetObject:
    """Contiene la informacion de un asset"""
    hash: str
    """nombre del asset"""
    size: int
    """tamaño del asset"""

@dataclass
class AssetIndex:
    """
    Contiene la informacion de los Assets de una version de Minecraft  
    """
    id: str
    """Indice de los Assets"""
    sha1: str
    """Hash de la lista de Assets"""
    size: int
    """Tamaño de archivo json que contiene los Assets"""
    total_size: int
    """Tamaño total de los Assets"""  
    url: str
    """Direccion de descarga del JSON"""
    objects: Optional[Dict[str, AssetObject]]
    """Diccionario que contiene el nombre del Asset (Key) y la informacion del Asset(AssetObject)"""

    @staticmethod
    def from_dict(data:dict) ->"AssetIndex":
        """
        Crea un AssetIndex a partir de un diccionario
        
        Args:

            data (dict): Informacion del assetIndex
        
        Returns:

            AssetIndex: Objeto con la infacion de los assets
        
        """
        return AssetIndex(
            id=data["id"],
            sha1=data["sha1"],
            size=data["size"],
            total_size= data["totalSize"],
            url=data["url"],
            objects= None
        )
    
    def fetch_objects(self) -> bool:
        """
        Descarga la informacion de los Assets
        """
        data_objects = download_json(self.url)
        print(data_objects)
        if data_objects is None:
            return False
        
        self.objects = {
            key: AssetObject(**value)
            for key, value in data_objects["objects"].items()
        }
        return True

    def fetch_assets(self, game_dir: Path) -> bool:

        """
        Descarga los assets del juego en una ruta especificada.

        Args:

            game_dir (str): Directorio de instalacion del juego.

        Returns:

            bool: True si los assets se descargaron correctamente, False si hubo un problema al descargar los assets.
        """
        if not isinstance(game_dir, (Path, str) ):
            raise TypeError("game_dir tiene que ser Path o str.")
        assetIndex_full_path = os.path.join(game_dir, "assets", "indexes", f"{self.id}.json")
        if(os.path.exists(assetIndex_full_path)):
            print("Recursos descargados previamente")
            return True
        
        for asset  in self.objects:
            asset_hash = self.objects[asset].hash if self.objects[asset] else ""
            if not asset_hash:
                print(f"No se encontro el asset: {asset}")
                return False
            sub_hash = self.objects[asset].hash[0:2]
            asset_full_path = os.path.join(game_dir, "assets", "objects", sub_hash, asset_hash)

            try:
                os.makedirs(os.path.dirname(asset_full_path), exist_ok=True)
            except OSError as directory_error:
                print(f"No se pudo crear la ruta {os.path.dirname(asset_full_path)}: {directory_error}")
                return False
            
            asset_url = f"{ASSETS_URL}/{sub_hash}/{asset_hash}"

            if not download_file(asset_url, asset_full_path):
                print(f"No se pudo descargar el asset {asset}")
                return False
        
        try:
            os.makedirs(os.path.dirname(assetIndex_full_path), exist_ok=True)
        except OSError as directory_error:
            print(f"No se pudo crear la ruta {os.path.dirname(assetIndex_full_path)}: {directory_error}")
            return False
        
        if not download_file(self.url, assetIndex_full_path):
            return False

        print("Recursos descargados correctamente")
        return True
            
