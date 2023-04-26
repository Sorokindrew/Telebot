from telebot.types import Message
import json

from loader import bot
import requests
from states.user_request import UserRequest

url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
sort_string = 'PRICE_LOW_TO_HIGH'


def lowprice(headers, querystring):
    """
    Функция для нахождения топ самых дешевых отелей.
    :return: list список самых дешевых отелей

    """
    response = requests.request('POST',
                                url=url,
                                headers=headers,
                                params=querystring)

    data = json.loads(response.text)
    return 'Узнать топ самых дешевых отелей в городе'


@bot.message_handler(commands=['lowprice'])
def lowprice_handler(message: Message) -> None:
    """
    Функция обработки команды lowprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
    bot.set_state(message.from_user, UserRequest.city, message.chat.id)
    bot.send_message(message.chat.id, 'Введите город для поиска отелей')


@bot.message_handler(state=UserRequest.city)
def get_city(message: Message):
    bot.set_state(message.from_user, UserRequest.hotels_quantity, message.chat.id)
    bot.send_message(message.chat.id, 'Введите необходимое количество отелей')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=UserRequest.hotels_quantity)
def get_qty(message: Message):
    print('Answer', message.text)
    bot.set_state(message.from_user, UserRequest.is_photo_enabled, message.chat.id)
    bot.send_message(message.chat.id, 'Нужно ли загружать фото')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity'] = message.text


@bot.message_handler(content_types=['text'])
def print_result(message: Message):
    if message.text == 'result':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['city']:
                print(data['city'])
            elif data['quantity']:
                print(data['quantity'])
            else:
                print('Нет данных')
