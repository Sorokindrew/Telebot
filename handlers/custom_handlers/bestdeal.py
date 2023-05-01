import datetime

from telebot.types import Message

from loader import bot
from states.user_request import UserRequest


@bot.message_handler(commands=['bestdeal'])
def bestdeal_handler(msg: Message) -> None:
    """
    Функция обработки команды bestdeal
    :param msg: Объект полученного сообщения от пользователя
    :return: None

    """
    bot.set_state(msg.from_user.id, UserRequest.city, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['command'] = 'bestdeal'
        data['user_id'] = msg.from_user.id
        data['time_of_request'] = datetime.datetime.now()
    bot.send_message(msg.chat.id, 'Where are You going?')
