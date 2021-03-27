import math
from config import COORD_TO_GEO_X, COORD_TO_GEO_Y


def calculate_spn(toponym: dict) -> str:
    """Функция вычисляет spn для масштабирования по топониму"""
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    spn_x = abs(float(lower_corner[0]) - float(upper_corner[0])) / 2
    spn_y = abs(float(lower_corner[1]) - float(upper_corner[1])) / 2
    result = f"{spn_x},{spn_y}"
    return result


def get_center_pos(json: dict) -> tuple:
    return tuple(map(float, get_geo_object(json)["Point"]["pos"].split()))


def get_geo_object(json):
    return json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


def XY_to_lon_lat(screen_x: int, screen_y: int,
                  z: int, previous_lon: float, previous_lat: float) -> tuple:
    """
    Функция преобразует координаты с экрана в географические координаты
    (Имеется погрешность, т.к. координаты с экрана это целое число)
    """
    dy = 225 - screen_y
    dx = screen_x - 300
    lx = previous_lon + dx * COORD_TO_GEO_X * math.pow(2, 15 - z)
    ly = previous_lat + dy * COORD_TO_GEO_Y * math.cos(math.radians(previous_lat)) * math.pow(2, 15 - z)
    return lx, ly