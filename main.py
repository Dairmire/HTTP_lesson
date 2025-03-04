import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image


kapitan = 'pochka'


def calc(a, b, x, y):
    x1 = abs(float(x) - float(a))
    y1 = abs(float(y) - float(b))
    return str(x1), str(y1)

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = input("".join(sys.argv[1:]))

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass
else:



    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    low = json_response["response"]["GeoObjectCollection"]['featureMember'][0]['GeoObject']['boundedBy']['Envelope']['lowerCorner']
    h = json_response["response"]["GeoObjectCollection"]['featureMember'][0]['GeoObject']['boundedBy']['Envelope']['upperCorner']
    sp = low.split()
    sp1 = h.split()
    a = sp[0]
    b = sp[1]
    x = sp1[0]
    y = sp1[1]



    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = "0.005"
    del1, del2 = calc(a, b, x, y)



    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([del1, del2]),
        "l": "map",
        'pt': ",".join([toponym_longitude, toponym_lattitude]),
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
    # Создадим картинку
    # и тут же ее покажем встроенным просмотрщиком операционной системы