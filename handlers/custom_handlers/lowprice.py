from loader import bot
from utils.lowprice import lowprice


@bot.message_handler(commands=['lowprice'])
def lowprice_handler(message: dict) -> None:
	"""
    Функция обработки команды lowprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, lowprice())