from dataclasses import dataclass, field
from typing import Optional, Dict, List
from utils.files import download_json




@dataclass
class LibraryDownloads:
    artifact: Optional[Dict]
    classifiers: Optional[Dict]

@dataclass
class Library:
    name: str
    downloads: Optional[LibraryDownloads]
    rules: Optional[list]
    natives: Optional[Dict]

    @staticmethod
    def from_dict(data:dict) -> "Library":
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
            for key, value in data_objects.items()
        }

##Correir nombres de atributos y agregar .get a Optionals

@dataclass
class Version:
    id: str
    assets: str
    assetIndex: Optional[AssetIndex]
    downloads: Optional[Dict]
    javaVersion: Optional[Dict]
    complianceLevel: int
    libraries: Optional[List[Library]]
    logging: Optional[Dict]
    mainClass: str
    type_version: str
    arguments: Optional[Dict]

    @staticmethod
    def from_dict(data:dict) -> "Version":
        asset_index_data = data.get("assetIndex")
        list_libraries = [Library.from_dict(lib) for lib in data.get("libraries", [])]
        return Version(
            id = data["id"],
            assets= data["assets"],
            complianceLevel=data["complianceLevel"],
            mainClass=data["mainClass"],
            type_version = data["type"],
            assetIndex=AssetIndex.from_dict(asset_index_data) if asset_index_data else None,
            downloads=data.get("downloads"),
            javaVersion=data["javaVersion"],
            logging=data["logging"],
            arguments=data["arguments"],
            libraries=list_libraries or None
        )
    