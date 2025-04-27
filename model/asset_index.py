from dataclasses import dataclass, field
from typing import Optional, Dict
from utils.files import download_json


@dataclass
class AssetObject:
    hash: str
    size: int

@dataclass
class AssetIndex:
    """
    Contiene la informacion de los Assets de una version de Minecraft
    Attributes:
        id (str): Indice de los Assets
        sha1 (str): Hash de la lista de Assets
        size (int): Tamaño de archivo json que contiene los Assets
        total_size (int): Tamaño total de los Assets
        url (str): Direccion de descarga del JSON
        objects (dict): Diccionario que contiene el nombre del Asset (Key) y la informacion del Asset(AssetObject)  
    """
    id: str
    sha1: str
    size: int
    total_size: int
    url: str
    objects: Optional[Dict[str, AssetObject]] = None

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
            url=data["url"]
        )
    
    def fetch_objects(self):
        """
        Descarga la informacion de los Assets
        """
        data_objects = download_json(self.url)
        if data_objects is None:
            return False
        
        self.objects = {
            key: AssetObject(**value)
            for key, value in data_objects["objects"].items()
        }