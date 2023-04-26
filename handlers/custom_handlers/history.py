from telebot.types import Message

from loader import bot


def history():
	"""
	Функция для запроса истории поиска.
	:return: list список предыдущих запросов

	"""
	return 'Узнать историю поиска отелей'


@bot.message_handler(commands=['history'])
def history_handler(message: Message) -> None:
	"""
    Функция обработки команды history
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, history())