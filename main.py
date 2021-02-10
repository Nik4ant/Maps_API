import sys
from io import BytesIO

from engine import *
from config import *

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

import requests
from PIL import Image


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("form.ui", self)

        # Инициализация UI
        self.initUI()

    def initUI(self):
        self.button_show.clicked.connect(self.show_map)
        self.setLayout(self.vlayout_main)

    def show_map(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec_())
