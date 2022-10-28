import httpx
import definitions

from . import schemas


"""
Запросы для сервиса 2GIS
"""

def get_geocode(address: str) -> schemas.Result:
    """
    Запрос прямого геокодирования и ответ (поиск по адресу)
    """

    # Превратим результат запроса в schemas.Result объект
    response = httpx.get("https://catalog.api.2gis.com/3.0/items/geocode?q={}&key={}".format(address, definitions.GIS_KEY))
    if response.status_code != 200:
        raise Exception("get_geocode() has failed")

    response_json = response.json()
    result_json   = response_json['result']
    items         = result_json['items']

    result = schemas.Result(items = [])

    for item in items:
        point: schemas.Point = schemas.Point(
            lat = item['point']['lat'],
            lon = item['point']['lon'],
        );

        schema_item: schemas.Item = schemas.Item(
            address_name    = item['address_name'],
            full_name       = item['full_name'],
            id              = item['id'],
            purpose_name    = item['purpose_name'],
            type            = item['type'],
            name            = item['name'],
            point           = point,
        );

        result.items.append(schema_item)

    return result


def get_position_by_address_string(address: str) -> schemas.Point:
    """
    Передает строку, содержащую адрес некоего географического объекта.
    Возвращает гео позицию данного объекта
    """
    return get_geocode(address).items[0].point
