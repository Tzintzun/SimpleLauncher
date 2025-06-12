from PySide6.QtCore import QObject, Signal
from pathlib import Path
from model.version import Version



class Downloader(QObject):
    """
    Permite descargar distintas versiones del juego.
    ---
    Apesar de que en `services.version_services` se encuentra `install_version()`. Se reprogramo esa misma funcion en el metodo `run()` de esta clase.
    De esta manera se puede controlar el proceso de instalacion.

    ## Signals
        - progress (int, str): se emite cuando el progreso de la instalacion de actualiza 
            Parametros:
                - int: porcentage de progreso.
                - str: Mensaje de avance.
        - finish_download (bool, str): se emite cuando la descarga finalizo.
            Parametros:
                - bool: True si la descarga se completo con exito, False si hubo un error.
                - str: Mensaje de resultado de la descarga.
    """
    progress = Signal(int,str)
    finish_download = Signal(bool,str)

    def __init__(self, version: Version, game_dir: Path):

        if not isinstance(version, Version):
            raise TypeError(f"Se espera un Version, pero se recibio un {type(version)}")
        if not isinstance(game_dir, (Path, str)):
            raise TypeError(f"Se espera un Path o str, pero se recibio un {type(game_dir)}")
        
        super().__init__()
        self.game_dir = Path(game_dir).expanduser().resolve()
        self.version = version

    def run(self):
        """Descarga una nueva version"""
        #Descargamos los Assets
        self.progress.emit(0, "Obteniendo informacion de los assets")
        if not self.version.asset_index.fetch_objects():
            self.finish_download.emit(False, "No se pudo obtener la informacion de los assets")
            return

        self.progress.emit(10, "Descargando los assets")
        if not self.version.asset_index.fetch_assets(self.game_dir):
            self.finish_download(False, "No se pudieron descargar los assets")
            return
    
        #Descargar librerias
        self.progress.emit(50, "Descargando las librerias")
        library_count = len (self.version.libraries)
        library_index= 0
        for l in self.version.libraries:
            if not l.fetch_library(self.game_dir):
                self.finish_download.emit(False,f"No se pudo descargar la libreria: {l.name}")
                return
            self.progress.emit(int(50 +(library_index*(40/library_count))),f"Descargando libreria: {l.name}")
            library_count = library_count +1
        
        #Descargado Cliente

        self.progress.emit(90, "Descargando Cliente.")

        if not self.version.downloads.fetch_client(self.game_dir, self.version.id, self.version.url):
            self.finish_download.emit(False,"No se pudo descargar el cliente")
            return
        
        self.progress.emit(100, f"Version {self.version.id}, descargado correctamente.")
        self.finish_download.emit(True, "Descarga Completada")
        return