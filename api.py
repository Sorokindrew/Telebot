from typing import List

import requests

from config_data import config

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


class Hotel:
    """
    Класс Отель.
    :param info: Словарь данных о отеле, полученный из API
    :param address: Адрес отеля
    :param hotel_photos: Массив URL фото отеля
    """

    def __init__(self, info: dict, address: str, hotel_photos: List):
        self.__name = info['name']
        self.__address = address
        self.__photos = hotel_photos
        self.__distance = \
            str(info['destinationInfo']['distanceFromDestination']['value']) \
            + ' ' + info['destinationInfo']['distanceFromDestination']['unit']
        self.__price_per_night = \
            info['price']['lead']['formatted'] \
            + ' ' \
            + info['price']['priceMessages'][0]['value']
        # if info['price']['displayMessages'] is not None:
        self.__total_price = \
            info['price']['displayMessages'][1]['lineItems'][0]['value'] \
            + ' ' \
            + info['price']['displayMessages'][2]['lineItems'][0]['value']
        # else:
        #     self.__total_price = 'No info'

    def get_name(self) -> str:
        """
        Получить названия отеля
        :return str: Название отеля
        """
        return self.__name

    def get_hotel_photos(self) -> List:
        """
        Получить массив URL фотографий отеля
        :return List: Массив с URL фотографий отеля
        """
        return self.__photos

    def get_hotel_info(self) -> str:
        """
        Получить информацию об отеле для отображения пользователю
        :return: hotel_info - Строка с полной информацией
        """
        hotel_info = 'Name of hotel: ' + self.__name + '\n' \
                     + 'Address: ' + self.__address + '\n' \
                     + 'Distance from centre: ' + self.__distance + '\n' \
                     + self.__price_per_night + '\n' \
                     + self.__total_price
        return hotel_info


def get_list_of_hotels(data: dict, start_index: int) -> List[Hotel]:
    """
    Получить данные об отелях, по заданным параметрам
    :param data: Словарь данных с запрашиваемыми параметрами
    :param start_index: Индекс с которого начинать поиск
    :return: Массив объектов класса Hotel
    """
    [checkin_day,
     checkin_month,
     checkin_year] = data['checkin_date'].split('-')
    [checkout_day,
     checkout_month,
     checkout_year] = data['checkout_date'].split('-')
    children: List = [{'age': ages} for ages in data['children_ages']]

    if data['command'] == 'lowprice':
        sort = 'PRICE_LOW_TO_HIGH'
        quantity = data['hotels_quantity']
        filters = {}
    elif data['command'] == 'highprice':
        sort = 'PRICE_LOW_TO_HIGH'
        quantity = 50
        filters = {}
    else:
        minimal_cost: int = data['minimal_cost']
        maximum_cost: int = data['maximum_cost']
        sort = 'DISTANCE'
        quantity = data['hotels_quantity']
        filters = {"price": {"max": maximum_cost,
                             "min": minimal_cost
                             }
                   }

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "EUR",
        "locale": "en_IE",
        "destination": {"regionId": data['regionId']},
        "checkInDate": {
            "day": int(checkin_day),
            "month": int(checkin_month),
            "year": int(checkin_year)
        },
        "checkOutDate": {
            "day": int(checkout_day),
            "month": int(checkout_month),
            "year": int(checkout_year)
        },
        "rooms": [
            {
                "adults": data['adults'],
                "children": children
            }
        ],
        "resultsStartingIndex": start_index,
        "resultsSize": quantity,
        "sort": sort,
        "filters": filters
    }
    print('Sending request to API...')
    response = requests.post(url, json=payload, headers=headers)

    hotels_data_from_response = \
        response.json()['data']['propertySearch']['properties']
    print('Got info from API')
    requested_hotels = []
    # Реализовано так, потому что при запросе большого числа отелей (бОльшего
    # чем есть в базе) возвращаются пустые объекты.
    # По этой причине, запрашивается порционно по 50 объектов, до тех пор пока
    # последний в массиве не будет пустым. Затем обрабатывается массив из
    # 50 объектов до первого пустого.
    if data['command'] == 'highprice' and \
            hotels_data_from_response[-1]['price']['lead']['amount'] != 0:
        return []
    for hotel in hotels_data_from_response:
        if hotel['price']['lead']['amount'] == 0:
            continue
        if data['is_photos_enabled'] == 'Yes':
            [hotel_address, hotel_photos] = get_hotel_photo_and_address(
                hotel_id=hotel['id'],
                quantity_of_photos=data['quantity_of_photos'])
        else:
            [hotel_address, hotel_photos] = get_hotel_photo_and_address(
                hotel_id=hotel['id'],
                quantity_of_photos=0
            )
        requested_hotels.append(Hotel(hotel, hotel_address, hotel_photos))
    return requested_hotels


def get_hotel_photo_and_address(hotel_id: int, quantity_of_photos: int) -> \
        List:
    """
    Получить список URL фото отеля и адреса
    :param hotel_id: ID отеля
    :param quantity_of_photos: Количество запрашиваемых фото
    :return: Массив [адрес, массив URL фото]
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "EUR",
        "eapid": 1,
        "locale": "en_IE",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = requests.post(url, json=payload, headers=headers)
    address = response.json()['data']['propertyInfo']['summary'][
        'location']['address']['addressLine']
    required_photos = []
    list_of_hotel_photos = \
        response.json()['data']['propertyInfo']['propertyGallery']['images']
    for image in range(quantity_of_photos):
        required_photos.append(list_of_hotel_photos[image]['image']['url'])
    return [address, required_photos]


def get_regionid_of_city(city_name: str) -> List:
    """
    Получить список городов с введенным названием
    :param city_name: Название города
    :return: Массив кортежей городов формата [(название города, regionId)]
    """
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": city_name, "locale": "en_IE"}
    response = requests.get(url, headers=headers, params=querystring)
    list_of_places = response.json()['sr']
    cities_with_requested_name = []
    for place in list_of_places:
        if place['type'] == 'CITY':
            cities_with_requested_name.append(
                (place['regionNames']['fullName'], place['gaiaId']))
    return cities_with_requested_name
