from dataclasses import dataclass, field
from typing import Optional, Dict, List
from utils.files import download_json
from model.asset_index import AssetIndex
from model.library import Library
from model.downloads import Downloads
from model.argument import Rule
from model.java_version import JavaVersion

##Correir nombres de atributos y agregar .get a Optionals

@dataclass
class Version:
    id: str
    assets: str
    assetIndex: Optional[AssetIndex]
    downloads: Optional[Downloads]
    javaVersion: Optional[JavaVersion]
    complianceLevel: int
    libraries: Optional[List[Library]]
    logging: Optional[Dict]
    mainClass: str
    type_version: str
    game_arguments: Optional[List[str | Rule]]
    java_arguments: Optional[List[str | Rule]]

    @staticmethod
    def from_dict(data:dict) -> "Version":
        asset_index_data = data.get("assetIndex")
        list_libraries = [Library.from_dict(lib) for lib in data.get("libraries", [])]
        downloads = data.get("downloads")
        game_arguments = [Rule.from_dict(argument) if isinstance(argument, dict) else argument
                          for argument in data["arguments"]["game"]]
        java_arguments = [Rule.from_dict(argument) if isinstance(argument, dict) else argument
                          for argument in data["arguments"]["jvm"]]
        
        java_version_data= data.get("javaVersion")
        java_version = JavaVersion.from_dict(java_version_data) if java_version_data else None
        return Version(
            id = data["id"],
            assets= data["assets"],
            complianceLevel=data["complianceLevel"],
            mainClass=data["mainClass"],
            type_version = data["type"],
            assetIndex=AssetIndex.from_dict(asset_index_data) if asset_index_data else None,
            downloads=Downloads.from_dict(downloads) if downloads else None,
            javaVersion=data["javaVersion"],
            logging=data["logging"],
            game_arguments=game_arguments or None,
            java_arguments= java_arguments or None,
            libraries=list_libraries or None
        )
    