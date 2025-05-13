import json
import requests
import os
import time
import hashlib
from  pathlib import Path

"""
Funciones para la descarga, almacenamiento, lectura y comprobacion de archivos,
"""

def download_file(url: str, destination: Path, retries = 5) -> "bool":
    """
    Descarga un archivo y lo almacena.
    Args:
        url (str): Direccion de descarga del archivo
        detination (str): Ubicacion donde se almacenara el archivo
        reties (int): numero de intentos en caso de error
    Returns:
        bool: 
            True: Si se descargo correctamente
            False: Si existio algun error en la descarga.
    """
    for attem in range(1, retries):
        try:
            response = requests.get(url, timeout=40)
            response.raise_for_status()

            os.makedirs(os.path.dirname(destination), exist_ok=True)
            try:
                with open(destination, "wb") as f:
                    f.write(response.content)

                print(f"Descargado: {os.path.basename(destination)}")
                return True
            except OSError as file_error:
                print(f"No se pudo escribir el archivo {destination}: {file_error}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {os.path.basename(destination)} (Intento {attem}/{retries}): {e}")
            time.sleep(1)
    
    print(f"No se pudo descargar: {os.path.basename(destination)}")
    return False

def download_json(url: str, retries: int =5) -> "dict | None":
    """
        Descarga un JSON de una direccion remota.
        Args:
            url (str): Direccion de descarga del archivo JSON
            retries (int): Numero de intentos en caso de error
        Returns:
            Optional[dict]: Retorna el contenido del archivo JSON como un diccionario o None En caso de no poder descargar el archivo.
    """
    for attemp in range(1, retries):
        try:
            response = requests.get(url, timeout=40)
            response.raise_for_status()
            print(f"Obteniendo informacion: {url} | Intento ({attemp}/{retries})")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a {url} : {e}")
            time.sleep(1)
    print(f"No se pudo obtener la informacion de: {url}")
    return None

def safe_json(full_path: Path, json_data:dict) -> "bool":
    """
    Almacena un diccionario, en formato JSON, en un archivo.
    
    Args:
        full_path (str): Path del archivo.
        json_data (dict): Diccionario a guardar en el archivo.

    Returns:
        bool:
            True: Si se almaceno correctamente el JSON. 
            False: Si hubo un error al almacenar el JSON.
    """
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as file:
            print(f"Escribiendo archivo: {full_path}")
            json.dump(json_data, file, indent=2)
        return True
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al abrir el archivo {full_path}: {e}")
        return False
    except (TypeError, ValueError) as e:
        print(f"Error al escribir la informacion: {e}")
        return False
    except (Exception) as e:
        print(f"Error al guardar el archivo: {e}")
        return False
    
def load_json(full_path: Path) -> "dict | None":
    """
    Carga un archivo JSON y lo retorna como un diccionario.

    Args:
        full_path (Path): Ruta del archivo JSON a cargar

    Returns:
        Optional[dict]: Diccionario del archivo JSON o None Si no se pudo cargar el archivo.
    """
    try:
        with open(full_path, "r") as file:
            print(f"Leyendo {full_path}")
            return json.load(file)
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error al abrir el archivo {full_path}")
        return None
    except (ValueError) as e:
        print(f"El formato del archivo {full_path} no es JSON")
        return None
    except Exception as e:
        print(f"Error al cargar el JSON: {full_path}")


def calculate_sha1(file_path: Path) -> "str | None":
    """
    Calcula el hash SHA1 de un archivo.

    Args:
        file_path (Path): Ruta del archivo.

    Returns:
        Optional[str]: codigo hash del archivo o None si no se pudo carlcular el hash
    """
    try:
        with open(file_path, "rb") as file:
            hash_sha1 = hashlib.sha1()
            while chunk := file.read(4096):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()
    except Exception as e:
        print(f"Error al calcular SHA1")
        return None

def verify_sha1(file_path: Path, expected_sha1: str) -> "bool":

    """

    Verifica el hash SHA1 de un archivo. 

    Args:
        file_path (Path): Path del archivo al que se le quiere calcular el hash
        expected:sha1 (str): Hash esperado

    Returns:
        bool:
            True: Si el hash calculado es igual al hash esperado.
            False: Si los hashes no coinciden.
    """
    file_hash = calculate_sha1(file_path)
    if file_hash is None:
        return False
    return file_hash.lower() == expected_sha1.lower()

