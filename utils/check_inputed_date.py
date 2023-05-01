import re
import datetime


def date_from_str_to_datetime(date: str) -> object:
    """
    Функция преобразования даты из строкового формата в объект datetime
    :param date: Дата в строковом формате
    :return: Объект datetime.date
    """
    date_in_datetime = datetime.date(int(date[-4:]), int(date[3:5]),
                                     int(date[:2]))
    return date_in_datetime


def check_if_valid_date(date: str) -> bool:
    """
    Функция проверки корректности ввода даты
    :param date: Дата в строковом формате
    :return: True or False
    """
    if re.match('\d\d\-\d\d\-\d\d\d\d', date):
        [day, month, year] = date.split('-')
        if int(day) in range(0, 32) and int(month) in range(0, 13) and \
                int(year) >= 2023:
            return True
    else:
        return False


def checkin_before_checkout(checkin: str, checkout: str) -> bool:
    """
    Функция проверки, что дата выезда позже даты заезда
    :param checkin: Дата заезда в строковом формате
    :param checkout: Дата выезда в строковом формате
    :return: True or False
    """
    checkin_date = date_from_str_to_datetime(checkin)
    checkout_date = date_from_str_to_datetime(checkout)
    if checkout_date - checkin_date < datetime.timedelta(days=1):
        return False
    else:
        return True


def checkin_is_actual(checkin: str):
    """
    Функция проверки, что дата заезда не в прошлом
    :param checkin: Дата заезда в стороковом формате
    :return: True or False
    """
    checkin_date = date_from_str_to_datetime(checkin)
    if checkin_date - datetime.date.today() < datetime.timedelta(days=0):
        return False
    else:
        return True