from dataclasses import dataclass, field
from typing import Optional, Dict
from utils.files import download_json


@dataclass
class AssetObject:
    hash: str
    size: int

@dataclass
class AssetIndex:
    id: str
    sha1: str
    size: int
    total_size: int
    url: str
    objects: Optional[Dict[str, AssetObject]] = None

    @staticmethod
    def from_dict(data:dict) ->"AssetIndex":
        return AssetIndex(
            id=data["id"],
            sha1=data["sha1"],
            size=data["size"],
            total_size= data["totalSize"],
            url=data["url"]
        )
    
    def fetch_objects(self):
        data_objects = download_json(self.url)
        if data_objects is None:
            return False
        
        self.objects = {
            key: AssetObject(**value)
            for key, value in data_objects["objects"].items()
        }