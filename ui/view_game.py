from PySide6.QtWidgets import (QVBoxLayout,
                               QHBoxLayout,
                               QFormLayout,
                               QLineEdit, 
                               QPushButton,
                               QTextBrowser,
                               QWidget,
                               QComboBox,
                               QMessageBox,
                               QRadioButton,
                               QButtonGroup)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from launcher import config
from launcher import core

class GameView(QVBoxLayout):

    """
    Muestra los controles para ejecutar una version. El boton de "Verifica la integridad de la instalacion." aun no esta implementado.
    """
    def __init__(self,parent: QWidget):
        super().__init__(parent)

        
        
        self.input_text_user = QLineEdit(placeholderText="User",text=config.get_user_name())
        """
        Requerido para lanzar una instalacion del juego.
        """
        self.form_installation_selector = QFormLayout()
        self.form_installation_selector.addRow("Nombre de usuario: ", self.input_text_user)

        self.installation_selector = QComboBox()
        self.installation_selector.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.form_installation_selector.addRow("Instalacion: ", self.installation_selector)
        self.load_installed_versions()

        self.acction_button_group = QHBoxLayout()
        self.launch_version_button = QPushButton("Lanzar")
        self.verify_version_button = QPushButton("Verificar")

        self.launch_version_button.setToolTip("Ejecuta la instalacion")
        self.verify_version_button.setToolTip("Verifica la integridad de la instalacion.")

        self.acction_button_group.addWidget(self.launch_version_button)
        self.acction_button_group.addWidget(self.verify_version_button)

        self.form_installation_selector.addRow(self.acction_button_group)


        self.addLayout(self.form_installation_selector)

        self.launch_version_button.clicked.connect(self.launch_installed_version)


        
    def load_installed_versions(self):
        """
        Carga las versiones instaladas en el directorio del juego.
        """
        self.installation_selector.clear()
        installed_versions = core.get_installed_versions(config.get_game_dir())

        if installed_versions is not None:
            for version in installed_versions:
                self.installation_selector.addItem(version.id,version)

    def launch_installed_version(self):
        """
        Ejecuta la version instalada seleccionada.
        """
        version = self.installation_selector.currentData()
        if version is None:
            message_box = QMessageBox()
            message_box.setText("No se encuentra ninguna version seleccionada")
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.exec()
            return 
        
        #get user
        user_name = self.input_text_user.text()
        if user_name == "":
            message_box = QMessageBox()
            message_box.setText("Por favor ingrese un Nombre de usuario.")
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.exec()
            self.input_text_user.setFocus()
            return 
        config.set_user_name(user_name)
        config.save_config()
        core.init_launcher(version, user_name, config.get_game_dir())

        
    