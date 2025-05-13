"""
Futuras actualizaciones
    - Actualizar archivo de versiones.
    - Agregar archivo de configuracion
    - Agregar verificacion de archivo

Pendientes
    - Arreglar descarga de versiones. 
"""
import os
from utils.files import download_json, download_file, safe_json_file


VERSIONS_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
ASSETS_URL = "https://resources.download.minecraft.net"

class Launcher():

    def __init__(self, game_dir:str):
        self.game_dir = game_dir


    def download_new_version(self, version_id:str):
        all_versions = Launcher.get_allversion()
        versions_ids = [version["id"] for version in all_versions]
        print(versions_ids)
        if  (version_id not in versions_ids):
            print(f"No se econtro la version {version_id}")
            return False
        
        version_url = next((version["url"] for version in all_versions if version["id"] == version_id) , None)
        if version_url is None:
            print("No se pudo descargar la nueva version")
            return False
        
        version_manifest = download_json(version_url)

        if version_manifest is None:
            print("No se logro obtener la informacion de la version")

        #descargar Assets
        if not self.dowloand_assets(version_manifest["assetIndex"]):
            print("No se logro descargar los recursos del juego")
            return False
        
        #descargar librerias
        if not self.dowload_libraries(version_manifest.get("libraries", [])):
            print("Error al descargar las librerias")
            return False
        
        #descarglar cliente
        if not self.download_client(version_manifest):
            print(f"No se logoro descargar el cliente")
            return False
        
        print(f"Version Minecraft {version_id} decargada correctamente")
        return True

    def download_client(self, version_manifest: dict = {}):
        client_url = version_manifest.get("downloads", {}).get("client", {}).get("url", {})
        client_version = version_manifest.get("id", {})
        if not client_version:
            print(f"No se pudo obtener la version del cliente")
        if not client_url :
            print(f"No se pudo obtener el URL del cliente")
            return False
        
        version_folder = os.path.join(self.game_dir, "versions", client_version )

        try:
            os.makedirs(version_folder, exist_ok=True)
        except OSError as e:
            print(f"No se pudo crear la ruta {version_folder}: {e}")
            return False

        version_path_manifest = os.path.join(version_folder, f"{client_version}.json")
        if not safe_json_file(version_path_manifest, version_manifest):
            print("No se pudo guardar la informacion de la version")
            return False
        
        version_path_jar = os.path.join(version_folder, f"{client_version}.jar")

        if not download_file(client_url, version_path_jar):
            print(f"No se pudo descargar el cliente para la version {client_version}")
            return False
        
        print(f"Cliente {client_version} descargado correctamente")
        return True
        

    def dowload_libraries(self, libraries_data:list = []):
        print(f"Descargando librerias")

        for lib in libraries_data:
            artifact = lib.get("downloads", {}).get("artifact")
            name = lib["name"]
            if not artifact:
                continue

            url = artifact["url"]
            path = artifact["path"]
            full_path = os.path.join(self.game_dir, "libraries", path)

            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
            except OSError as directory_error:
                print(f"No se pudo crear la ruta {os.path.dirname(full_path)}: {directory_error}")
                return False

            if os.path.exists(full_path):
                print(f"Directorio creado: {path}")
                continue

            print(f"Descargado libreria: {name}")

            if not download_file(url, full_path):
                return False
        
        print(f"Se descargaron correctamente {len(libraries_data)} librerias")
        return True   


    def dowloand_assets(self, asset_data: dict):
        id = asset_data["id"]
        url = asset_data["url"]
        print("Descargando Recursos...")
        
        assetIndex_full_path = os.path.join(self.game_dir, "assets", "indexes", f"{id}.json")
        if os.path.exists(assetIndex_full_path):
            print("Recursos descargados previamente")
            return True
        assets_info = download_json(url)

        if not assets_info:
            return False
        
        assets_objects = assets_info["objects"]
        assets_keys = assets_objects.keys()
        for key in assets_keys:
            asset = assets_objects[key]
            asset_hash = asset["hash"]
            asset_sub_hash = asset_hash[0:2]

            asset_full_path = os.path.join(self.game_dir, "assets", "objects", asset_sub_hash,asset_hash)

            try:
                os.makedirs(os.path.dirname(asset_full_path), exist_ok=True)
            except OSError as directory_error:
                print(f"No se pudo crear la ruta {os.path.dirname(asset_full_path)}: {directory_error}")
                return False
            
            
            asset_url = f"{ASSETS_URL}/{asset_sub_hash}/{asset_hash}"
            print(f"Descargando: {asset_url}")
            if not download_file(asset_url, asset_full_path):
                return False
        
        
        try:
            os.makedirs(os.path.dirname(assetIndex_full_path), exist_ok=True)
        except OSError as directory_error:
            print(f"No se pudo crear la ruta {os.path.dirname(assetIndex_full_path)}: {directory_error}")
            return False
        
        if not download_file(url, assetIndex_full_path):
            return False

        print("Recursos descargados correctamente")
        return True

    @staticmethod
    def get_allversion():
        return [version for version in download_json(VERSIONS_MANIFEST_URL)["versions"]]
    
    @staticmethod
    def get_release_versions():
        return [version for version in download_json(VERSIONS_MANIFEST_URL)["versions"] if version["type"] == "release"]
    
    @staticmethod
    def get_snapshot_versions():
        return [version for version in download_json(VERSIONS_MANIFEST_URL)["versions"] if version["type"] == "snapshot"]
    
    @staticmethod
    def get_latest_relese_version():
        return download_json(VERSIONS_MANIFEST_URL)["latest"]["release"]
    
    @staticmethod
    def get_latest_snapshot_version():
        return download_json(VERSIONS_MANIFEST_URL)["latest"]["snapshot"]
    @staticmethod
    def get_latest_versions():
        return download_json(VERSIONS_MANIFEST_URL)["latest"]
    

        