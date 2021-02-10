import sys
from io import BytesIO

from engine import *
from config import *

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests
from PIL import Image
from PIL.ImageQt import ImageQt


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("form.ui", self)
        self.coordinates = [0, 0]

        # Инициализация UI
        self.initUI()

    def initUI(self):
        self.button_show.clicked.connect(self.show_map)
        self.setLayout(self.vlayout_main)

    def show_map(self):
        # toponym_to_find = " ".join(self.lineEdit_cordinates.text())
        #
        # geocoder_params = {
        #     "apikey": GEOCODER_API_KEY,
        #     "geocode": toponym_to_find,
        #     "format": "json"}
        #
        # response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)
        #
        # if not response:
        #     print('Все плохо')
        #     self.massege_module.setText('Ничего не найдено')
        #     exit(1)
        #
        # json_response = response.json()
        # toponym = json_response["response"]["GeoObjectCollection"][
        #     "featureMember"][0]["GeoObject"]
        #
        # span = caclulate_spn(toponym)
        #
        # # Координаты центра топонима:
        # toponym_coodrinates = toponym["Point"]["pos"]
        # # Долгота и широта:
        # toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        self.coordinates = list(map(float, self.lineEdit_cordinates.text().replace(',', ' ').split()))
        if not self.coordinates:
            self.lineEdit_cordinates.setText('0,0')
            self.coordinates = list(map(float, self.lineEdit_cordinates.text().replace(',', ' ').split()))

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ','.join(map(str, self.coordinates)),
            "spn": ','.join((str(DEFAULT_SCALE),) * 2),
            "l": "map",
            # 'pt': ",".join([toponym_longitude, toponym_lattitude]) + ',pm2rdl',
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        data = BytesIO(response.content)

        pixmap = QPixmap.fromImage(ImageQt(Image.open(data)))

        self.pixmap_map.setPixmap(pixmap)

    def keyPressEvent(self, event):
        print(event.key(), Qt.Key_Up)
        if event.key() == Qt.Key_Up:
            self.coordinates[1] += DELTA_MOVE
        if event.key() == Qt.Key_Down:
            self.coordinates[1] -= DELTA_MOVE
        if event.key() == Qt.Key_Right:
            self.coordinates[0] += DELTA_MOVE
        if event.key() == Qt.Key_Left:
            self.coordinates[0] -= DELTA_MOVE
        self.lineEdit_cordinates.setText(', '.join(map(str, self.coordinates)))
        self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec_())
