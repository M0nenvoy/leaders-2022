import httpx
import definitions

from . import schemas


"""
Запросы для сервиса 2GIS
"""

def get_building_geocode(address: str) -> schemas.Result:
    """
    Запрос прямого геокодирования и ответ (поиск по адресу). Находит гео объект здания по адресу
    """

    response = httpx.get("https://catalog.api.2gis.com/3.0/items/geocode?q={}&key={}&type=building&fields=items.point".format(address, definitions.GIS_KEY))
    if response.status_code != 200:
        raise Exception("get_geocode() has failed: {}".format(response.json()['error']))

    response_json = response.json()
    result_json   = response_json['result']
    items         = result_json['items']

    # Превратим результат запроса в schemas.Result объект
    result = schemas.Result(items = [])

    # TODO: 2gis может вернуть нам гео объекты, которые... очень отдаленно подходят по переданному адрему, но нам, очевидно не подходят.
    # Как бы мы могли от этого перестраховаться?

    for item in items:
        point: schemas.Point = schemas.Point(
            lad = item['point']['lat'],
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


def get_position_by_address_string(address: str) -> schemas.Point | None:
    """
    Передает строку, содержащую адрес некоего географического объекта.
    Возвращает точку с широтой и долготой. Если здание не было найдено, возвращает None
    """
    try:
        point: schemas.Point = get_building_geocode(address).items[0].point
        return point
    except:
        return None
