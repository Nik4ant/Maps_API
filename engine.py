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
