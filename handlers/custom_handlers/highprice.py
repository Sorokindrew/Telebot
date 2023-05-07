import datetime

from telebot.types import Message

from loader import bot
from states.user_request import UserRequest


@bot.message_handler(commands=['highprice'])
def highprice_handler(msg: Message) -> None:
    """
    Обработка команды highprice
    :param msg: Объект полученного сообщения от пользователя
    :return: None

    """
    bot.set_state(msg.from_user.id, UserRequest.city, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['command'] = 'highprice'
        data['user_id'] = msg.from_user.id
        data['time_of_request'] = datetime.datetime.now()
    bot.send_message(msg.chat.id, 'Where are You going?')
