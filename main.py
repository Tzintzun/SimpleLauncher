import os
import json
import requests
import time
import platform
import subprocess
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from views.exampleWidget import ExampleWidget

from model.instalacion  import Installation
from model.user import User
from model.launcher import Launcher

MINECRAFT_DIR = os.path.expandvars("%APPDATA%/.minecraft/")


if __name__ == "__main__":

    launcher = Launcher(MINECRAFT_DIR)
    print(Installation.get_installations(MINECRAFT_DIR))

    installation = Installation(MINECRAFT_DIR, "1.21.5")
    installation.launch(User("Tzintzun"))
    #launcher.download_new_version("1.21.5")
    