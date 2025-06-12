
"""
La UI principal se encuentra en la clase `ui.main.LauncherMainWindow` Este modulo solo se encarga de instanciar y ejecutar la UI.
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main import LauncherMainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LauncherMainWindow()
    window.show()
    app.exec()