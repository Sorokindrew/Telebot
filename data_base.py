import sqlite3
from typing import List

from api import Hotel


def insert_request_info_to_db(conn: sqlite3.Connection, data: dict) -> None:
    """
    Записать информацию о запросе в БД
    :param conn: Соединение с БД
    :param data: Словарь с полной информацией о запросе
    :return: None
    """
    insert_request = f"""
    INSERT INTO history(date_time, user_id, command, city)
    VALUES (?, ?, ?, ?) 
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(insert_request,
                   (data['time_of_request'].strftime('%d-%m-%Y %H:%M'),
                    data['user_id'],
                    data['command'],
                    data['city_name']))
    conn.commit()


def get_request_id(conn: sqlite3.Connection, data: dict) -> int:
    """
    Получить информацию о порядковом номере запроса в БД
    :param conn: Соединение с БД
    :param data: Словарь с полной информацией о запросе
    :return: Порядковый номер запроса в БД
    """
    get_request_id_sql = f"""
    SELECT request FROM history WHERE user_id = ? AND 
                                date_time = ?;
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(get_request_id_sql,
                   (data['user_id'],
                    data['time_of_request'].strftime('%d-%m-%Y %H:%M')))
    request_id, *_ = cursor.fetchone()
    return request_id


def insert_result_of_request_to_db(conn: sqlite3.Connection,
                                   hotels: List[Hotel],
                                   request_id: int) -> None:
    """
    Записать информацию о результатах запроса в БД
    :param conn: Соединение с БД
    :param hotels: Список полученных отелей
    :param request_id: Порядковый номер запроса в БД
    :return: None
    """
    hotels_info_to_db = []
    for hotel in hotels:
        hotel_info = hotel.get_hotel_info()
        name_of_hotel = hotel_info.split('\n')[0][15:]
        hotel_price = hotel_info.split('\n')[3]
        hotels_info_to_db.append((name_of_hotel, hotel_price, request_id))

    insert_hotels = f"""
    INSERT INTO hotels (hotel_name, hotel_price, request)
    VALUES (?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.executemany(insert_hotels, hotels_info_to_db)


def get_history(conn: sqlite3.Connection, user_id: int) -> List:
    """
    Получить историю запросов пользователя
    :param conn: Соединение с БД
    :param user_id: ID пользователя
    :return: Массив с информацией о запросах пользователя
    """
    get_history_sql = """
    SELECT * FROM history WHERE user_id = ?;
    """

    get_hotels_sql = """
    SELECT * FROM hotels WHERE request = ?
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(get_history_sql, (user_id,))
    requests = cursor.fetchall()
    all_requests = []
    for request in requests:
        cursor.execute(get_hotels_sql, (request[0],))
        hotels_in_result = cursor.fetchall()
        hotels_print = ''
        for hotel in hotels_in_result:
            hotels_print += f"\nHotel name: {hotel[1]}\n" \
                            f"Price: {hotel[2]}\n"
        request_info = f"Command: {request[3]}\n" \
                       f"Time of request: {request[1]}\n" \
                       f"City: {request[4]}\n" \
                       f"{hotels_print}\n"
        all_requests.append(request_info)
    return all_requests
