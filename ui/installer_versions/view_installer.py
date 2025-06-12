from PySide6.QtWidgets import (QVBoxLayout,
                               QHBoxLayout,
                               QFormLayout,
                               QPushButton,
                               QWidget,
                               QComboBox,
                               QMessageBox,
                               QProgressBar)
from PySide6.QtCore import Qt, QThread,Signal
from pathlib import Path
from launcher import config
from launcher import core
from model.version_manifests import VersionInfo
from ui.installer_versions.info_area import InfoArea
from ui.installer_versions.button_group_filter import ButtonGroupFilter
from ui.installer_versions.downloader import Downloader

class InstallerView(QVBoxLayout):
    """
    Control para la visualizacion y descarga de versiones.
    
    ## Signals:
        - update_installed_versions: Se emite cuando una nueva version fue instalada.
    """
    update_installed_versions = Signal()
    def __init__(self, parent: QWidget):
        super().__init__(parent)


        #Cargamos directorio de juego y manifiesto de versiones.
        self.game_dir = config.get_game_dir()
        self.game_dir = self.game_dir.expanduser()
        self.version_manifest = core.load_version_manifest(self.game_dir)


        #Creamos formulario de seleccion de versiones.

        #Añadimos los Botones para filtrar las versiones
        self.form_versions = QFormLayout()
        self.button_group_filter = ButtonGroupFilter()
        self.form_versions.addRow("Tipo de version: ", self.button_group_filter)

        #Añadimos un combobox para seleccionar la version
        self.version_combobox = QComboBox()
        view = self.version_combobox.view()
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.on_type_version_changed(1)
        self.form_versions.addRow("Versiones:", self.version_combobox)


        #Añadimos los botones para descargar la version seleccionada o recargar versiones.
        self.acction_button_group = QHBoxLayout()
        self.install_version_button = QPushButton("Instalar")
        self.reload_version_button = QPushButton("Recargar Versiones")
        self.acction_button_group.addWidget(self.install_version_button)
        self.acction_button_group.addWidget(self.reload_version_button)

        self.form_versions.addRow(self.acction_button_group)


        #Añadimos el formulario de versiones.
        self.addLayout(self.form_versions)

        #Creamos un InfoArea para visualizar la informacion de la version a descargar.
        self.info_area = InfoArea()
        current_version_data = self.version_combobox.currentData()
        self.info_area.setText(current_version_data.toHtml())
        self.addWidget(self.info_area)

        #Creamos Progress Bar
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(100)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(0)

        self.addWidget(self.progressbar)

        #Configuramos las señales para mostrar la informacion y para recargar las versiones en el combobox.
        self.version_combobox.currentIndexChanged.connect(self.on_index_change)
        self.button_group_filter.button_group.idClicked.connect(self.on_type_version_changed)
        self.install_version_button.clicked.connect(self.download_new_version)

    def on_index_change(self,index):
        """Muestra la informacion de la version seleccionada."""
        currente_data = self.version_combobox.currentData()
        if isinstance(currente_data, VersionInfo):
            self.info_area.setText(currente_data.toHtml())

    def on_type_version_changed(self, id):
        """Filtra las versiones mostradas en el selector."""
        versions_type =[]
        if id == 0:
            versions_type.append("release")
            versions_type.append("snapshot")
        elif id ==1:
            versions_type.append("release")
        elif id==2:
            versions_type.append("snapshot")
        else:
            print("Opcion no conocida.")

        self.version_combobox.clear()
        for version in self.version_manifest.versions:
            if version.type_version in versions_type:
                self.version_combobox.addItem(version.id,version)

    def download_new_version(self):
        """
        Descarga la version seleccionada.
        """
        version_info = self.version_combobox.currentData()

        if version_info is None:
            mgs_box = QMessageBox()
            mgs_box.setText("Por favor seleccione una version para descargar")
            mgs_box.icon(QMessageBox.Icon.Information)
            mgs_box.exec()
            return
        
        version  = core.get_version_data(version_info)

        if version is None:
            mgs_box = QMessageBox()
            mgs_box.setText("La version seleccionada no se pudo encontrar.")
            mgs_box.icon(QMessageBox.Icon.Information)
            mgs_box.exec()
            return
        
        self.progressbar.setValue(0)
        self.qthread = QThread()
        self.donwloader = Downloader(version, config.get_game_dir())
        self.donwloader.moveToThread(self.qthread)

        self.qthread.started.connect(self.donwloader.run)
        self.donwloader.finish_download.connect(self.finished)
        self.donwloader.progress.connect(self.update_progress)
        self.qthread.start()
        
    def finished(self, result: bool, message: str):
        """Se ejecuta cuando la instalacion de una version termina"""
        if not result:
            self.info_area.setText(f"Error al descargar: {message}")
            self.progressbar.setValue(0)
        else:
            self.info_area.setText(f"EXITO: {message}")
            self.progressbar.setValue(100)
            self.update_installed_versions.emit()
        self.qthread.quit()
        self.donwloader.deleteLater()
        self.qthread.finished.connect(self.qthread.deleteLater)
    
    def update_progress(self, percentage: int, message:str):
        """Actualiza la barra de progreso y muestra el mensaje en un `ui.installer_versions.info_area.InfoArea`"""
        self.progressbar.setValue(percentage)
        self.info_area.append(message)