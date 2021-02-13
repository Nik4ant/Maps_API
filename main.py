import sys
from io import BytesIO

from engine import *
from config import *
from form import Ui_Form

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests
from PIL import Image
from PIL.ImageQt import ImageQt


class MapKeyFilter(QObject):
    """
    Это класс представляющий фильтр событий, нужный для решения проблемы
    "карты". Т.к. некоторын виджеты могут перехватывать эти события => метод
    keyPressEvent у окна с картой не будет получать события.
    (Например, виджет QLineEdit перехватывал нажатия левой и правой стрелок)
    """

    KEYS_FOR_MAP = (Qt.Key_Right, Qt.Key_Left)

    def eventFilter(self, object: 'QObject', event: 'QEvent') -> bool:
        if event.type() == QEvent.KeyRelease:
            key = event.key()
            if key in MapKeyFilter.KEYS_FOR_MAP:
                self.parent().keyPressEvent(event)
                return True
        return False


class MapWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.coordinates = [0, 0]
        self.scale = DEFAULT_SCALE

        # Инициализация UI
        self.initUI()

    def initUI(self):
        self.button_show.clicked.connect(self.show_map)
        self.lineEdit_cordinates.setText('0.0,0.0')
        self.lineEdit_scale.setText(str(self.scale))

        # Фильтр для событий, чтобы события нажатий стрелок вправо и влево не
        # перехватывались только сторонними виджетами
        self.installEventFilter(MapKeyFilter(self))

        self.setLayout(self.vlayout_main)

    def show_map(self):
        # Координаты
        cordinates = self.lineEdit_cordinates.text().split(',')
        if (not self.check_param(cordinates[0], float) or
                not self.check_param(cordinates[-1], float)):
            self.lineEdit_cordinates.setText('0.0,0.0')
            self.show_error_message("Некорректные координаты")
            return
        self.coordinates = list(map(float, cordinates))

        # Масштаб
        scale = self.lineEdit_scale.text()
        if not self.check_param(scale, int):
            self.lineEdit_scale.setText(str(DEFAULT_SCALE))
            self.show_error_message("Некорректный масштаб")
            return
        self.scale = int(scale)

        # Параметры для запроса к StaticMapsAPI
        map_params = self.get_params_from_inputs()

        response = requests.get(MAP_API_SERVER, params=map_params)
        if not response:
            self.show_error_message(f"http: {response.status_code}")
            return

        data = BytesIO(response.content)
        pixmap = QPixmap.fromImage(ImageQt(Image.open(data)))
        self.pixmap_map.setPixmap(pixmap)

    def show_error_message(self, error_text: str):
        error_text = f'''
Невозможно отобразить участок карты с параметрами:
Координаты - {self.lineEdit_cordinates.text()}
Масштаб - {self.lineEdit_scale.text()}\n
Ошибка: {error_text}
'''

        messege = QMessageBox(QMessageBox.Warning,
                              "ОШИБКА", error_text)
        messege.resize(300, 150)
        messege.exec()

    def get_params_from_inputs(self) -> dict:
        """
        Метод возвращает параметры для запроса на основании введённых данных,
        если они корректные
        """
        # NOTE: Метод важен, т.к. от задачи к задаче функционал будет менятся,
        # и чтобы не парится, всё будет тут (Никита)

        '''
        Этот код был намерено оставлен тут.

        search_object = self.lineEdit_search.text()
        # Параметры для поиска отличаются от параметров для геокодера и карт
        if search_object:
            params = {
                "apikey": SEARCH_API_KEY,
                "lang": "ru_RU",
                "text": search_object,
                "type": "geo",  # тип возвращаемого объекта - топоним
            }
        else:
        '''

        params = {
            "ll": ','.join(map(str, self.coordinates)),
            "z": str(self.scale),
            "l": "map",
        }

        return params

    def check_param(self, param: any, supposed_type: type):
        """Метод по проверке корректности параметра"""
        if supposed_type == float:
            return not any(char not in "-1234567890." for char in param)
        elif supposed_type == int:
            return not any(char not in "-1234567890" for char in param)
        elif supposed_type == str:
            return bool(param.replace(' ', ''))

        return False

    def keyPressEvent(self, event):
        move = DELTA_MOVE * 2 ** (7 - self.scale)
        key = event.key()

        # Проверка на движение
        if key == Qt.Key_Up:
            self.coordinates[1] = round(self.coordinates[1] + move, ndigits=5)
        elif key == Qt.Key_Down:
            self.coordinates[1] = round(self.coordinates[1] - move, ndigits=5)
        elif key == Qt.Key_Right:
            self.coordinates[0] = round(self.coordinates[0] + move, ndigits=5)
        elif key == Qt.Key_Left:
            self.coordinates[0] = round(self.coordinates[0] - move, ndigits=5)

        # Такая проверка нужна для учёта двух enter'ов на клавиатуре
        elif key in (Qt.Key_Enter, Qt.Key_Enter - 1):
            self.coordinates = list(map(float, self.lineEdit_cordinates.text().split(',')))
            if not self.coordinates:
                self.lineEdit_cordinates.setText('0.0,0.0')
                self.coordinates = [0, 0]
            self.scale = int(self.lineEdit_scale.text())

        # Проверка на изменение масштаба
        elif key == Qt.Key_PageDown:
            self.scale += DELTA_SCALE
        elif key == Qt.Key_PageUp:
            self.scale -= DELTA_SCALE
        else:
            return

        self.scale = max(min(self.scale, 17), 0)
        self.lineEdit_cordinates.setText(','.join(map(str, self.coordinates)))
        self.lineEdit_scale.setText(str(self.scale))
        self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec_())
