from telebot.types import Message

from loader import bot


def highprice():
	"""
	Функция для нахождения топ самых дорогих отелей.
	:return: list список самых дорогих отелей

	"""
	return 'Узнать топ самых дорогих отелей в городе'


@bot.message_handler(commands=['highprice'])
def highprice_handler(message: Message) -> None:
	"""
    Функция обработки команды highprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, highprice())