import os
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": API_KEY,
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
        self.__total_price = \
            info['price']['displayMessages'][1]['lineItems'][0]['value'] \
            + ' ' \
            + info['price']['displayMessages'][2]['lineItems'][0]['value']

    def get_name(self) -> str:
        return self.__name

    def get_hotel_photos(self) -> List:
        return self.__photos

    def get_hotel_info(self) -> str:
        """
        Метод получения информации об отеле для отображения пользователю
        :return: hotel_info - строка с полной информацией
        """
        hotel_info = 'Name of hotel: ' + self.__name + '\n' \
                     + 'Address: ' + self.__address + '\n' \
                     + 'Distance from centre: ' + self.__distance + '\n' \
                     + self.__price_per_night + '\n' \
                     + self.__total_price
        return hotel_info


def get_list_of_hotels(data: dict) -> List:
    """
    Функция получения данных об отелях, по заданным параметрам
    :param data: Словарь данных с запрашиваемыми параметрами
    :return: Массив объектов класса Hotel
    """
    [checkin_day, checkin_month, checkin_year] = data['checkin_date'].split(
        '-')
    [checkout_day, checkout_month, checkout_year] = data[
        'checkout_date'].split('-')
    children = [{'age': ages} for ages in data['children_ages']]

    if data['command'] == 'lowprice':
        sort = 'PRICE_LOW_TO_HIGH'
    elif data['command'] == 'highprice':
        sort = 'PRICE_HIGH_TO_LOW'
    else:
        sort = 'DISTANCE'

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
        "resultsStartingIndex": 0,
        "resultsSize": data['hotels_quantity'],
        "sort": sort,
    }
    print('Sending request to API...')
    response = requests.post(url, json=payload, headers=headers)

    hotels_data_from_response = \
        response.json()['data']['propertySearch']['properties']
    requested_hotels = []
    for hotel in hotels_data_from_response:
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
    print('Got info from API')
    return requested_hotels


def get_hotel_photo_and_address(hotel_id: int, quantity_of_photos: int) -> \
        List:
    """
    Функция получения списка URL фото отеля и адреса
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
    Фнукция получения городов с введенным названием
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
