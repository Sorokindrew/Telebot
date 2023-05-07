from typing import List

from api import Hotel


def sort_bestdeal_hotels(requested_hotels: List[Hotel], max_cost: int,
                         distance: int) -> List[Hotel]:
    """
    Функция сортировки по цене отелей в заданном радиусе от центра
    :param requested_hotels: Список отелей отсортированный по расстоянию от
    центра
    :param max_cost: Максимальная стоимость указанная пользователем
    :param distance: Расстояние от центра
    :return: Список отелей отсортированный по цене в заданном радиусе
    """
    sorted_list = []
    for _ in range(len(requested_hotels)):
        minimal_cost: int = max_cost
        for hotel in requested_hotels:
            distance_string = hotel.get_hotel_info().split('\n')[2]
            distance_text = distance_string.split(' ')[3]
            distance_from_downtown = float(distance_text.split('.')[0]) + \
                                     float(distance_text.split('.')[1]) / 10
            if hotel in sorted_list or distance_from_downtown > distance:
                continue
            price_string = hotel.get_hotel_info().split('\n')[3]
            if ',' not in price_string.split(' ')[0][1:]:
                price = int(price_string.split(' ')[0][1:])
            else:
                thousands = price_string.split(' ')[0][1:].split(',')[0]
                hundreds = price_string.split(' ')[0][1:].split(',')[1]
                price = int(thousands) * 1000 + int(hundreds)
            if price < minimal_cost:
                minimal_cost = price
                hotel_to_add = hotel
        if hotel_to_add not in sorted_list:
            sorted_list.append(hotel_to_add)
    return sorted_list
