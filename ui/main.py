from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget
from ui.view_config import ConfigView
from ui.view_game import GameView
from ui.installer_versions.view_installer import InstallerView
import launcher.config as config


class LauncherMainWindow(QMainWindow):
    """
        Ventana principal del launcher.
    """
    def __init__(self):
        super().__init__()
        print(config.get_launcher_name())
        self.setWindowTitle(config.get_launcher_name())
        
        self.tab_menu = QTabWidget()

        self.tab_config = QWidget()
        self.tab_game_selector = QWidget()
        self.tab_installer_version = QWidget()

        self.tab_config_layout = ConfigView(self.tab_config)
        self.tab_game_selector_layout = GameView(self.tab_game_selector)
        self.tab_installer_version_layout = InstallerView(self.tab_installer_version)

        
        self.tab_menu.addTab(self.tab_game_selector, "Juego")
        self.tab_menu.addTab(self.tab_installer_version, "Versiones")
        self.tab_menu.addTab(self.tab_config, "Configuracion")


        self.setCentralWidget(self.tab_menu)

        self.tab_installer_version_layout.update_installed_versions.connect(self.tab_game_selector_layout.load_installed_versions)

