import sys

from engine import *
from config import *
from form import Ui_Form

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests


class MapKeyFilter(QObject):
    """
    Это класс представляющий фильтр событий, нужный для решения проблемы
    "карты". Т.к. некоторын виджеты могут перехватывать эти события => метод
    keyPressEvent у окна с картой не будет получать события.
    (Например, виджет QLineEdit перехватывал нажатия левой и правой стрелок)
    """

    KEYS_FOR_MAP = (Qt.Key_Right, Qt.Key_Left)

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if event.type() == QEvent.KeyRelease:
            key = event.key()
            if key in MapKeyFilter.KEYS_FOR_MAP:
                self.parent().keyPressEvent(event)
                return True
        return False


class MapWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.cordinates = [40.0, 52.0]
        self.mark_position = None
        self.scale = DEFAULT_SCALE
        self.map_view = 'map'

        # Инициализация UI
        self.setupUi(self)
        # pyuic5 form.ui
        self.initUI()
        self.show_map()

    def initUI(self):
        # "Руками" создадим кнопку, которая будет располагаться не в лайаотах, а просто над всем
        self.btn_view = QPushButton(self)
        self.btn_view.setIcon(QIcon(QPixmap('layers.png')))
        self.btn_view.setFixedSize(35, 35)

        self.btn_view.clicked.connect(self.change_map_view)
        self.button_show.clicked.connect(self.show_map)
        self.button_clean.clicked.connect(self.clean_search)
        self.lineEdit_cordinates.setText(','.join(map(str, self.cordinates)))
        self.lineEdit_scale.setText(str(self.scale))

        # Фильтр для событий, чтобы события нажатий стрелок вправо и влево не
        # перехватывались только сторонними виджетами
        self.installEventFilter(MapKeyFilter(self))

        self.setLayout(self.vlayout_main)

    def paintEvent(self, event):
        indent = 15
        self.btn_view.move(indent, self.minimumHeight() - self.btn_view.height() - indent)

    def show_map(self):
        # Координаты
        old_cordinates = self.cordinates
        cordinates = self.lineEdit_cordinates.text().split(',')
        if (not self.check_param(cordinates[0], float) or
                not self.check_param(cordinates[-1], float)):
            self.show_error_message("Некорректные координаты")
            self.lineEdit_cordinates.setText(','.join(map(str, old_cordinates)))
            return
        else:
            self.cordinates = list(map(float, cordinates))

        # Масштаб
        old_scale = self.scale
        scale = self.lineEdit_scale.text()
        if not self.check_param(scale, int) or 0 > int(scale) or int(scale) > 17:
            self.show_error_message("Некорректный масштаб")
            self.lineEdit_scale.setText(str(old_scale))
            return
        self.scale = int(scale)

        # Дополнительные параметры к карте, либо их замена при запросе к поиску
        extra_map_params = dict()
        # Если нужен поиск, то делается дополнительный запрос к Search API
        if self.check_param(self.lineEdit_search.text(), str):
            seacrh_response = requests.get(SEARCH_API_SERVER,
                                           params=self.get_seacrh_params())
            if not seacrh_response:
                self.show_error_message("кривой запрос к поиску: " +
                                        str(seacrh_response.status_code))
                return
            # Позиция для метки (по условию в центре)
            try:
                self.mark_position = get_toponym_center_pos(seacrh_response.json())
            # На случай, если ничего не будет найдено
            except IndexError:
                self.show_error_message("кривой запрос к поиску: " +
                                        str(seacrh_response.status_code))
                return

            # Дополнительные/новые параметры
            extra_map_params = {
                "pt": f"{self.mark_position[0]},{self.mark_position[1]},pm2blm",
                "ll": f"{self.mark_position[0]},{self.mark_position[1]}",
            }

            self.lineEdit_cordinates.setText(','.join(map(str, self.mark_position)))
            self.cordinates = self.mark_position[:]
            self.lineEdit_search.setText('')

        elif self.mark_position:
            extra_map_params = {
                "pt": f"{self.mark_position[0]},{self.mark_position[1]},pm2blm",
            }

        # Параметры для запроса к StaticMapsAPI
        map_params = self.get_map_params()
        map_params.update(extra_map_params)
        response = requests.get(MAP_API_SERVER, params=map_params)
        if not response:
            self.show_error_message(f"кривой запрос к картам {response.content}")
            return

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        self.pixmap_map.setPixmap(pixmap)

    def show_error_message(self, error: str):
        error_text = f'''
Невозможно отобразить участок карты с параметрами:
Координаты - {self.lineEdit_cordinates.text()}
Масштаб - {self.lineEdit_scale.text()}
Тип - {self.map_view}

Ошибка: {error}
'''

        messege = QMessageBox(QMessageBox.Warning,
                              "ОШИБКА", error_text.strip())
        messege.resize(300, 150)
        messege.exec()

    def get_seacrh_params(self) -> dict:
        params = {
            "apikey": SEARCH_API_KEY,
            "lang": "ru_RU",
            "text": self.lineEdit_search.text(),
            "results": 1,
            "type": "geo",  # тип возвращаемого объекта - топоним
        }

        return params

    def get_map_params(self) -> dict:
        """
        Метод возвращает параметры для запроса на основании введённых данных
        """

        params = {
            "ll": ','.join(map(str, self.cordinates)),
            "z": str(self.scale),
            "l": self.map_view,
        }

        return params

    @staticmethod
    def check_param(param: any, supposed_type: type):
        """Метод по проверке корректности параметра"""
        if supposed_type == float:
            return not any(char not in "-1234567890." for char in param)
        elif supposed_type == int:
            return not any(char not in "-1234567890" for char in param)
        elif supposed_type == str:
            return bool(param.replace(' ', ''))

        return False

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Изменение размера
        if event.angleDelta().y() >= 120:
            self.scale += 1
        else:
            self.scale -= 1
        self.scale = max(0, min(17, self.scale))
        self.lineEdit_scale.setText(str(self.scale))

        # Обновление карты
        self.show_map()

    def keyPressEvent(self, event):
        move = 2 ** (DELTA_MOVE - self.scale)
        key = event.key()

        # Проверка на движение
        if key == Qt.Key_Up:
            self.cordinates[1] = round(self.cordinates[1] + move, ndigits=5)
        elif key == Qt.Key_Down:
            self.cordinates[1] = round(self.cordinates[1] - move, ndigits=5)
        elif key == Qt.Key_Right:
            self.cordinates[0] = round(self.cordinates[0] + move, ndigits=5)
        elif key == Qt.Key_Left:
            self.cordinates[0] = round(self.cordinates[0] - move, ndigits=5)

        # Такая проверка нужна для учёта двух enter'ов на клавиатуре
        elif key in (Qt.Key_Enter, Qt.Key_Return):
            self.show_map()
            return

        # Проверка на изменение масштаба
        elif key == Qt.Key_PageDown:
            self.scale += DELTA_SCALE
        elif key == Qt.Key_PageUp:
            self.scale -= DELTA_SCALE
        else:
            return

        self.scale = max(min(self.scale, 17), 0)
        self.lineEdit_cordinates.setText(','.join(map(str, self.cordinates)))
        self.lineEdit_scale.setText(str(self.scale))
        self.show_map()

    def change_map_view(self):
        views = ['map', 'sat', 'sat,skl']
        self.map_view = views[(views.index(self.map_view) + 1) % len(views)]
        self.show_map()

    def clean_search(self):
        self.lineEdit_search.clear()
        self.mark_position = None
        self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec())
