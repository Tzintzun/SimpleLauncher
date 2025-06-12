"""Funsiones relacionadas con la configuracion y ejecucion de la Java Virtual Machine"""
from pathlib import Path
import os
import re
import platform
import subprocess
from typing import Optional, List
from launcher.config import get_launcher_name, get_launcher_version,get_config_java_path
from model.version import Version
from model.user  import User
from model.argument import Rule

__docformat__ = "Google-style"

def get_java_path() -> Optional[Path]:
    """
    Obtiene el Path de Java configurado y conprueba su existencia.
    Returns:
        Path: ruta absoluta al binario de java.
        None: no encontro un binario de java.
    """
    java_path = Path(get_config_java_path())
    if java_path.exists():
        return java_path.expanduser().resolve()
    return None


def build_class_path(version: Version, system: str, game_dir: Path) -> str:

    """
    Construye un string con el path de las librerias necesarias para ejecutar el juego.
    Args:
        version (Version): version de la que se quiere contruir el class_path.
        system (str): Sistema operativo del la maquina local.
        game_dir (Path): Directorio de la instalacion del juego.
    Returns:
        str: String que contiene todas las librerias del juego necesarias para su ejecucion.
    """
    separator = ";" if system == "windows" else ":"
    classpath = []
    if not isinstance(game_dir, (Path, str) ):
        raise TypeError("game_dir tiene que ser Path o str.")
    if not isinstance(version, Version):
        raise TypeError("version tiene que ser de tipo Version")
    for lib in version.libraries:
        if lib.downloads.artifact:
            path = os.path.join(game_dir, "libraries", lib.downloads.artifact["path"])
            classpath.append(path)
    
    client_jar = os.path.join(game_dir, "versions", version.id, f"{version.id}.jar")
    classpath.append(client_jar)
    return separator.join(classpath)


def build_launc_comand(version: Version, user: User, game_dir: Path) -> Optional[List[str]]:
    
    """
    Genera un comando para ejecutar una version de minecraft.
    Args:
        version (Version): Version de minecraft a la que se quiere generar un comando.
        user (User): Informacion del usuario que va a ejecutar el juego
        game_dir (Path): Directorio donde se encuentra instalada la version del juego.
    Returns:
        Optional[List[str]]: Comando a ejecutar.
    """

    if not isinstance(game_dir, (Path, str) ):
        raise TypeError("game_dir tiene que ser Path o str.")
    if not isinstance(version, Version):
        raise TypeError("version tiene que ser de tipo Version")
    if not isinstance(user, User):
        raise TypeError("user tiene que ser de tipo User")

    if not game_dir.exists():
       return None
    
    game_dir_full_path = game_dir.expanduser().resolve()


    game_args_values = {
        "auth_player_name" : user.user_name,
        "auth_uuid" : user.user_uuid,
        "auth_access_token" : user.access_token,
        "auth_xuid" : "ofline-client",
        "user_type" : "mojang",
        "clientid" : "ofline-client-tz",
        "version_name" : version.id,
        "version_type" : version.type_version,
        "game_directory": str(game_dir),
        "assets_root" : os.path.join(game_dir_full_path, "assets"),
        "assets_index_name" : version.asset_index.id
    }

    game_args = []
    for argument in version.game_arguments:
        if(type(argument) == str):
            game_args.append(re.sub(r"\$\{(.+?)\}", 
                                    lambda m: game_args_values.get(m.group(1), 
                                                                   m.group(0)), 
                                                                   argument))
    
    java_args = []

    system = platform.uname().system.lower()
    machine = platform.uname().machine.lower()

    for rules in version.java_arguments:
        if(type(rules) == Rule):
            for rule in rules.rule:
                if "name" in rule.get("os",{}).keys():
                    if system == rule["os"]["name"]:
                        java_args.extend[rules.value]
                if "arch"  in rule.get("os",{}).keys():
                    if machine == rule["os"]["arch"]:
                        java_args.extend(rules.value)
    
    
    # Automatizar esto
    java_args.append("-Djava.library.path=natives")
    java_args.extend([f"-Dminecraft.launcher.brand={get_launcher_name()}"])
    java_args.extend([f"-Dminecraft.launcher.version={get_launcher_version()}"])
    java_args.append("-cp")
    java_args.append(build_class_path(version, system, game_dir))

    

    launch_args = [get_java_path()]
    launch_args.extend(java_args)
    launch_args.append(version.main_class)
    launch_args.extend(game_args)

    
    return launch_args

def run_minecraft(command: List[str]) -> None:
    """
    Ejectua una version de minecraft.

    Args:
        command (List[str]): Lista que contiene el comando a ejecutar, con argumentos y librerias incluidas.
    
    """
    with open(os.devnull, "w") as devnull:
        subprocess.Popen(command)
    
                            