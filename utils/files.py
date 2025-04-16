import json
import requests
import os
import time


def import_file_json(dir):
    try:
        with open(dir, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error al convertir archivo a JSON: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except IOError as e:
        print(f"Error de E/S al abrir el archivo: {e}")
    except UnicodeDecodeError as e:
        print(f"Error de decodificación de caracteres: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def download_file(url, destination, retries = 5):
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

def download_json(url, retries=5):
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

def safe_json_file(full_path: str, json_data:dict):
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