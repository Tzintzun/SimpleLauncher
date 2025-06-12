from PySide6.QtWidgets import QTextBrowser
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices




class InfoArea(QTextBrowser):
    """
    Muestra la informacion de una version.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)

        self.anchorClicked.connect(self.on_anchor_clicked)

    def on_anchor_clicked(self, url: QUrl):
        """Abre un enlace en el navegador del sistema cuando se hace click sobre el."""
        if not isinstance(url, QUrl):
            raise TypeError("La url tiene que ser de tipo QUrl")
        QDesktopServices.openUrl(url)