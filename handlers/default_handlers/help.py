from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
	"""
    Функция обработки команды help
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.from_user.id,
	                 'Для работы с ботом, используйте следующие команды:'
	                 '\n/lowprice\n/highprice\n/bestdeal\n/history')