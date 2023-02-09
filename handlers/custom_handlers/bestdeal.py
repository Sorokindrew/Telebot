from telebot.types import Message

from loader import bot
from utils.bestdeal import bestdeal


@bot.message_handler(commands=['bestdeal'])
def bestdeal_handler(message: Message) -> None:
	"""
    Функция обработки команды bestdeal
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, bestdeal())