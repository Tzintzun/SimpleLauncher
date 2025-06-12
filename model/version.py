from dataclasses import dataclass
from typing import Optional, Dict, List
from model.asset_index import AssetIndex
from model.library import Library
from model.downloads import Downloads
from model.argument import Rule
from model.java_version import JavaVersion


__docformat__ = "Google-style"

##Correir nombres de atributos y agregar .get a Optionals

@dataclass
class Version:
    """
    Contiene toda la informacion, de una version, necesaria para: descargar y/o ejecutar el juego.
    """

    id: str
    """ID de la version."""
    assets: str
    """Indice que contiene todos los assets."""
    asset_index: Optional[AssetIndex]
    """Contiene toda la informaccion de los assets de la version."""
    downloads: Optional['Downloads']
    """Contiene la informacion de todas las posibles descagas del juego (cliente, servidor)"""
    java_version: Optional[JavaVersion]
    """Informacion de la version de java utilizada."""
    compliance_level: int
    libraries: Optional[List[Library]]
    """Lista con las librerias utilizadas por la version."""
    logging: Optional[Dict]
    main_class: str
    """Clase principal del cliente."""
    type_version: str
    """Tipo de version (release, snapshot)"""
    game_arguments: Optional[List[str | Rule]]
    """Argumentos requeridos por el juego."""
    java_arguments: Optional[List[str | Rule]]
    """Argumentos requeridos para la ejecucion de java."""
    url: str
    """URL del manifiesto de la version"""

    @staticmethod
    def from_dict(data:dict, version_url) -> "Version":
        """
        Obtiene un objeto Version apartir de un diccionario.

        Args:

            data (dict):

        Returns:

            Version:
        """
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
            compliance_level=data["complianceLevel"],
            main_class=data["mainClass"],
            type_version = data["type"],
            asset_index=AssetIndex.from_dict(asset_index_data) if asset_index_data else None,
            downloads=Downloads.from_dict(downloads) if downloads else None,
            java_version=data["javaVersion"],
            logging=data["logging"],
            game_arguments=game_arguments or None,
            java_arguments= java_arguments or None,
            libraries=list_libraries or None,
            url = version_url
        )
    def __str__(self):

        return f"Version: {self.id}\n Type: {self.type_version}\n MainClass: {self.main_class}"