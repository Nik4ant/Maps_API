def caclulate_spn(toponym: dict) -> str:
    """Функция вычисляет spn для масштабирования по топониму"""
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    spn_x = abs(float(lower_corner[0]) - float(upper_corner[0])) / 2
    spn_y = abs(float(lower_corner[1]) - float(upper_corner[1])) / 2
    result = f"{spn_x},{spn_y}"
    return result


def get_toponym_by_json(json: dict, index=0) -> dict:
    """Функция возвращает топоним по индексу (по умолчанию первый)"""
    return json["response"]["GeoObjectCollection"]["featureMember"][
        index]["GeoObject"]
