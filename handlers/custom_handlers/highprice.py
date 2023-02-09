from telebot.types import Message

from loader import bot
from utils.highprice import highprice


@bot.message_handler(commands=['highprice'])
def highprice_handler(message: Message) -> None:
	"""
    Функция обработки команды highprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, highprice())