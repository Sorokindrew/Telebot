from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
	"""
    Функция обработки команды help
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id,
	                 'Для работы с ботом, используйте следующие команды:'
	                 '\n/lowprice - вывод самых дешевых отелей в городе'
					 '\n/highprice - вывод самых дорогих отелей в городе'
					 '\n/bestdeal - вывод отелей наиболее подходящих по цене и '
					 'расположению'
					 '\n/history - вывод истории поиска отелей')