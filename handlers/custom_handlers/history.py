from telebot.types import Message

from loader import bot
from utils.history import history


@bot.message_handler(commands=['history'])
def history_handler(message: Message) -> None:
	"""
    Функция обработки команды history
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, history())