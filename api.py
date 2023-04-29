import json
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
    def __init__(self, info: dict, address: str):
        self.__name = info['name']
        self.__address = address
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

    def get_name(self):
        return self.__name

    def get_hotel_info(self):
        hotel_info = 'Name of hotel: ' + self.__name + '\n' \
                     + 'Address: ' + self.__address + '\n' \
                     + 'Distance from centre: ' + self.__distance + '\n' \
                     + self.__price_per_night + '\n' \
                     + self.__total_price
        return hotel_info


def get_list_of_hotels(data: dict) -> List:
    [checkin_day, checkin_month, checkin_year] = data['checkin_date'].split(
        '-')
    [checkout_day, checkout_month, checkout_year] = data[
        'checkout_date'].split('-')
    children = [{'age': ages} for ages in data['children_ages']]

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
        "sort": "PRICE_LOW_TO_HIGH",
    }
    print('Sending request to API...')
    response = requests.post(url, json=payload, headers=headers)

    hotels_data_from_response = \
        response.json()['data']['propertySearch']['properties']
    requested_hotels = []
    for hotel in hotels_data_from_response:
        if data['is_photos_enabled'] == 'Yes':
            hotel_address = get_hotel_photo_and_address(
                hotel_id=hotel['id'],
                quantity_of_photos=data['quantity_of_photos'])
        else:
            hotel_address = get_hotel_photo_and_address(
                hotel_id=hotel['id'],
                quantity_of_photos=0
            )
        requested_hotels.append(Hotel(hotel, hotel_address))
    print('Got info from API')
    return requested_hotels


def get_hotel_photo_and_address(hotel_id: int, quantity_of_photos: int) -> str:
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "EUR",
        "eapid": 1,
        "locale": "en_IE",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = requests.post(url, json=payload, headers=headers)
    name = response.json()['data']['propertyInfo']['summary']['name']
    address = response.json()['data']['propertyInfo']['summary'][
        'location']['address']['addressLine']
    if quantity_of_photos > 0:
        os.mkdir(f'hotels/{name}')

    list_of_hotel_photos = \
        response.json()['data']['propertyInfo']['propertyGallery']['images']
    for image in range(quantity_of_photos):
        with open(f"hotels/{name}/img{image}.jpg", 'wb') as f:
            f.write(requests.get(
                list_of_hotel_photos[image]['image']['url']).content)
    return address


def get_regionid_of_city(city_name: str) -> List:
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
