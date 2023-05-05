import sqlite3
from typing import List
import datetime

from api import Hotel


# def create_table():
#     table_request = """
#     CREATE TABLE IF NOT EXISTS history (
#     request INTEGER PRIMARY KEY AUTOINCREMENT,
#     date_time VARCHAR(255) NOT NULL,
#     user_id INTEGER NOT NULL,
#     command VARCHAR(255) NOT NULL,
#     city VARCHAR(255) NOT NULL)
#     """
#
#     table_hotels = """
#     CREATE TABLE IF NOT EXISTS hotels (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     hotel_name VARCHAR(255) NOT NULL,
#     hotel_price VARCHAR(255) NOT NULL,
#     request INTEGER NOT NULL,
#     FOREIGN KEY (request) REFERENCES history (request)
#     )
#     """
#
#     with sqlite3.connect('history.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute(table_hotels)
#         cursor.execute(table_request)
#         conn.commit()
#

def insert_request_info_to_db(conn: sqlite3.Connection, data: dict):
    insert_request = f"""
    INSERT INTO history(date_time, user_id, command, city)
    VALUES (?, ?, ?, ?) 
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(insert_request, (data['time_of_request'].strftime('%d-%m-%Y %H:%M'),
                                    data['user_id'],
                                    data['command'],
                                    data['city_name']))
    conn.commit()


def get_request_id(conn: sqlite3.Connection, data: dict):
    get_request_id_sql = f"""
    SELECT request FROM history WHERE user_id = ? AND 
                                date_time = ?;
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(get_request_id_sql, (data['user_id'], data['time_of_request'].strftime('%d-%m-%Y %H:%M')))
    request_id, *_ = cursor.fetchone()
    return request_id


def insert_result_of_request_to_db(conn: sqlite3.Connection, hotels: List[Hotel], request_id: int):
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


def get_history(conn: sqlite3.Connection, user_id: int) -> str:
    all_requests = ''
    get_history_sql = """
    SELECT * FROM history WHERE user_id = ?;
    """

    get_hotels_sql = """
    SELECT * FROM hotels WHERE request = ?
    """
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(get_history_sql, (user_id,))
    requests = cursor.fetchall()
    for request in requests:
        cursor.execute(get_hotels_sql, (request[0],))
        hotels_in_result = cursor.fetchall()
        hotels_print = ''
        for hotel in hotels_in_result:
            hotels_print += f"\nHotel name: {hotel[1]}\n" \
                            f"Price: {hotel[2]}\n"
        all_requests += f"Command: {request[3]}\n" \
                        f"Time of request: {request[1]}\n" \
                        f"City: {request[4]}\n" \
                        f"{hotels_print}\n"
    return all_requests
