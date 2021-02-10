import sys
from io import BytesIO

from engine import *
from config import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import requests
from PIL import Image


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("f   orm.ui", self)

        # Инициализация UI
        self.initUI()

    def initUI(self):
        self.button_show.clicked.connect(self.show_map)
        # Слои для переключения
        self.combo_type.addItem("Схема")
        self.combo_type.addItem("Спутник")
        self.combo_type.addItem("Гибрид")

        self.setLayout(self.vlayout_main)

    def show_map(self):
        toponym_to_find = " ".join(self.lineEdit_cordinates.text())

        geocoder_params = {
            "apikey": GEOCODER_API_KEY,
            "geocode": toponym_to_find,
            "format": "json"
        }

        response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)
        if not response:
            QMessageBox(QMessageBox.Warning, "Всё плохо", "ОШИБКА!").exec()
            sys.exit(-1)

        json_response = response.json()
        toponym = get_toponym_by_json(json_response)
        scale = caclulate_spn(toponym)

        # Координаты центра топонима
        toponym_coodrinates = get_toponym_center_pos(toponym)
        # Долгота и широта
        # toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        self.cordinates = list(map(float, self.lineEdit_cordinates.text().replace(',', ' ').split()))

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ','.join(map(str, self.coordinates)),
            "spn": ','.join((str(DEFAULT_SCALE),) * 2),
            "l": "map",
            # 'pt': ",".join([toponym_longitude, toponym_lattitude]) + ',pm2rdl',
        }

        response = requests.get(MAP_API_SERVER, params=map_params)

        data = BytesIO(response.content)

        pixmap = QPixmap.fromImage(ImageQt(Image.open(data)))

        self.pixmap_map.setPixmap(pixmap)

    def format_params_for_request(self):
        # TODO: magic stuff here
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec_())
