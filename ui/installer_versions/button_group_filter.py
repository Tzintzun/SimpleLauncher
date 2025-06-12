from PySide6.QtWidgets import QHBoxLayout, QButtonGroup, QRadioButton


class ButtonGroupFilter(QHBoxLayout):
    """
    Control para seleccionar el tipo de version a filtrar.
    ## Tipo de versiones
        - todas
        - release
        - snapshot
    Los radio buttons se concentran en un `QHBoxLayout` para ser mostrados en la UI. Tambien se encuentran agrupados en un `QButtonGroup` para su control.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

        self.all_radiobutton = QRadioButton("todas")
        self.release_radiobutton = QRadioButton("release")
        self.snapshot_radiobutton = QRadioButton("snapshot")
        self.release_radiobutton.setChecked(True)

        self.addWidget(self.release_radiobutton)
        self.addWidget(self.snapshot_radiobutton)
        self.addWidget(self.all_radiobutton)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.all_radiobutton, id=0)
        self.button_group.addButton(self.release_radiobutton, id=1)
        self.button_group.addButton(self.snapshot_radiobutton, id=2)