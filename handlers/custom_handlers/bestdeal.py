from telebot.types import Message

from loader import bot


def bestdeal():
	"""
	Функция для нахождения топ самых выгодных предложений.
	:return: list список отелей оптимальных по сооьношению цена / качество
	"""
	return 'Узнать топ отелей, наиболее подходящих по цене и расположению ' \
	       'от центра'


@bot.message_handler(commands=['bestdeal'])
def bestdeal_handler(message: Message) -> None:
	"""
    Функция обработки команды bestdeal
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, bestdeal())