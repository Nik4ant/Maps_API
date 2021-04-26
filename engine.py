import math
import requests
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


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a: (float, float), b: (float, float)):
    degree_to_meters_factor = 111 * 1000   # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def organisation_info(coords) -> ((float, float), str):
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

    request = 'https://search-maps.yandex.ru/v1/'
    geo_params = {
        'apikey': api_key,
        'text': "организация",
        'll': ",".join(map(str, coords)),
        'type': 'biz',
        'lang': 'ru_RU',
        'results': '1',
    }
    response = requests.get(request, params=geo_params)

    if response:
        response = response.json()["features"][0]

        info = [
            'Название: ' + response["properties"]["name"],
            'Адрес: ' + response["properties"]["description"],
            'Сайт: ' + response["properties"]["CompanyMetaData"].get("url", 'Нет сайта'),
            'Телефон: ' + response["properties"]["CompanyMetaData"].get("Phones", [{}])[0].get("formatted", 'Нет телефонов'),
            'Режим работы: ' + response["properties"]["CompanyMetaData"].get("Hours", {}).get("text", 'Не указано время работы'),
            'Координаты: ' + ', '.join(map(str, response["geometry"]["coordinates"]))
        ]

        return response["geometry"]["coordinates"], '\n'.join(info)

    raise RuntimeError(f"""Ошибка выполнения запроса: {response.url}
Http статус: {str(response.status_code) + " (" + str(response.reason) + ")"}""")
