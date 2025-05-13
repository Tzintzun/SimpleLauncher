import os
import platform
import re
import subprocess
import sys
from model.user import User
from utils.files import import_file_json


class Installation():

    def __init__(self, game_dir: str, version_dir_name:str):
        self.game_dir = game_dir
        manifest_version_dir = os.path.join(game_dir, "versions", version_dir_name, f"{version_dir_name}.json")
        self.manifest_version = import_file_json(manifest_version_dir)
        if (self.manifest_version is None):
            raise FileNotFoundError(f"No se encontro archivo de manifiesto para {manifest_version_dir}")
        #print(self.manifest_version)


    def launch(self, user:User):

        print("Preparando...")

        #build args
        #Minecraft arguments
        print(f"Construyendo argumentos de juego")

        game_args_values = {
            "auth_player_name" : user.user_name,
            "auth_uuid" : user.user_uuid,
            "auth_access_token" : user.access_toke,
            "auth_xuid" : "ofline-client",
            "user_type" : "mojang",
            "clientid" : "ofline-client-tz",
            "version_name" : self.manifest_version["id"],
            "version_type" : self.manifest_version["type"],
            "game_directory": self.game_dir,
            "assets_root" : os.path.join(self.game_dir, "assets"),
            "assets_index_name" : self.manifest_version["assets"]
        }
        game_args_parameters = self.manifest_version["arguments"]["game"]
        game_args =[]
        for argument in game_args_parameters:
            if(type(argument) == str): 
                game_args.append(re.sub(r"\$\{(.+?)\}", lambda m: game_args_values.get( m.group(1), m.group(0)), argument))
        
        # JAVA virtual machine arguments
        jvm_args = []

        #jvm rules
        system = platform.uname().system.lower()
        machine = platform.uname().machine.lower()

        for rules in self.manifest_version["arguments"]["jvm"]:
            if type(rules) == dict:
                for rule in rules["rules"]:
                    if "name" in rule["os"].keys():
                        if system == rule["os"]["name"]:
                            if(type(rules["value"]) == list):
                                jvm_args.extend(rules["value"])
                                continue
                            jvm_args.append(rules["value"])
                    if "arch" in rule["os"].keys():
                        if machine == rule["os"]["arch"]:
                            if(type(rules["value"]) == list):
                                jvm_args.extend(rules["value"])
                                continue
                            jvm_args.append(rules["value"])
        #only use classpath and java.library.path
        jvm_args.append("-Djava.library.path=natives")
        jvm_args.extend(["-Dminecraft.launcher.brand=TzintzunLauncher"])
        jvm_args.extend(["-Dminecraft.launcher.version=0.0.1"])
        jvm_args.append("-cp")
        jvm_args.append(Installation._build_class_path(self.game_dir, self.manifest_version["id"], self.manifest_version["libraries"]))
        #print(jvm_args)
        print(f"Ejecutando Minecraft {self.manifest_version["id"]}")
        launch_args = ["java"]
        launch_args.extend(jvm_args)
        launch_args.append(self.manifest_version["mainClass"])
        launch_args.extend(game_args)
        with open(os.devnull, "w") as devnull:
            subprocess.Popen(launch_args, stdout=devnull, stderr=devnull)
        sys.exit()

    @staticmethod
    def _build_class_path(game_dir:str, version_id:str, libraries:dict ):
        separator = ";" if platform.system() == "Windows" else ":"
        classpath = []
        for lib in libraries:
            artifact = lib.get("downloads", {}).get("artifact")
            if artifact:
                path = os.path.join(game_dir, "libraries", artifact["path"])
                classpath.append(path)

        client_jar = os.path.join(game_dir, "versions", version_id, f"{version_id}.jar")
        classpath.append(client_jar)

        return separator.join(classpath)


    @staticmethod
    def get_installations(game_dir:str):
        
        try:
            if os.path.isdir(game_dir):
                versions_dir = os.path.join(game_dir, "versions")
                if os.path.exists(versions_dir):
                    return [version for version in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, version)) ] 
                else:
                    raise FileNotFoundError(f"No se encontro el directorio {versions_dir}")
            else:
                raise NotADirectoryError(f"No se encontro el directorio {game_dir}")
        except (FileNotFoundError, NotADirectoryError, PermissionError, TypeError) as e:
            print(f"Error al acceder a las versiones: {e}")
            raise e