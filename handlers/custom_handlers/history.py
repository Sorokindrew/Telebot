import sqlite3

from telebot.types import Message

from loader import bot
import data_base


@bot.message_handler(commands=['history'])
def history_handler(msg: Message) -> None:
	"""
    Функция обработки команды history
    :param message: объект полученного сообщения от пользователя
    :return: None

    """

	user_id = msg.from_user.id
	with sqlite3.connect('history.db') as conn:
		all_requests = data_base.get_history(conn, user_id)
		for request in all_requests:
			bot.send_message(msg.chat.id, request)
