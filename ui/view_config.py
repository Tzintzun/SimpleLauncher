from PySide6.QtWidgets import QFormLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from pathlib import Path
import launcher.config as config


class ConfigView(QFormLayout):
    """
    Permite modificar la configuracion del launcher.
    ## Configuraciones habilitadas.
        - Directorio de instalacion: directorio de instalacion del juego.
        - Java Path: rutal al binario de java.
        - Manifest Version Url: url de descarga del manifiesto de versiones.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.inputTextGameDir = QLineEdit(placeholderText="/ruta/del/juego", text=str(config.get_game_dir()))
        self.addRow("Directorio de instalacion: ",self.inputTextGameDir)

        self.inputTextJavaPath = QLineEdit(placeholderText="/ruta/de/java", text=config.get_config_java_path())
        self.addRow("Java Path: ", self.inputTextJavaPath)

        self.inputTextManifestVersionUrl = QLineEdit(placeholderText="https://tu-dominio.com/manifest_versions.json", text=config.get_version_manifest_url())
        self.addRow("Manifest Versions Url:", self.inputTextManifestVersionUrl)

        self.buttonSaveConfig = QPushButton("Guardar Configuracion")
        self.buttonReloadConfig = QPushButton("Recargar Configuracio")
        self.buttonBox = QHBoxLayout()
        self.buttonBox.addWidget(self.buttonSaveConfig)
        self.buttonBox.addWidget(self.buttonReloadConfig)
        self.addRow(self.buttonBox)

        self.buttonSaveConfig.clicked.connect(self.save_config)

        

    def save_config(self):
        """
        Guarda la configuracion del launcher, en un archivo config.ini
        """
        if not config.set_game_dir(Path(self.inputTextGameDir.text())):
            print(f"No se pudo configurar el dicrectorio del juego como {self.inputTextGameDir.text()}")

        if not config.set_config_java_path(Path(self.inputTextJavaPath.text())):
            print(f"No se pudo configurar el dicrectorio de java como {self.inputTextJavaPath.text()}")

        if not config.set_version_manifest_url(self.inputTextManifestVersionUrl.text()):
            print(f"No se pudo configurar la url del manifest como {self.inputTextManifestVersionUrl.text()}")
        
        config.save_config()

    def load_config(self):
        """
        Carga la configuracion del launcher de un config.ini
        """
        config.reload_config()
        self.inputTextGameDir.setText(str(config.get_game_dir()))
        self.inputTextJavaPath.setText(str(config.get_config_java_path()))
        self.inputTextManifestVersionUrl.setText(str(config.get_version_manifest_url()))