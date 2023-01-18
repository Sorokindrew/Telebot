import telebot
import requests
from lowprice import lowprice
from bestdeal import bestdeal
from highprice import highprice
from history import history

"""Создание бота с полученным токеном"""
bot = telebot.TeleBot('5551354218:AAHKwAoizg50q8_euQeXeg7RsWWnZx1kDiM')


@bot.message_handler(commands=['start'])
def start(message: dict) -> None:
	"""
    Функция обработки команды start
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, 'Привет! Чем могу помочь?')


@bot.message_handler(commands=['help'])
def help(message: dict) -> None:
	"""
    Функция обработки команды help
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.from_user.id,
	                 'Для работы с ботом, используйте следующие команды:'
	                 '\n/lowprice\n/highprice\n/bestdeal\n/history')


@bot.message_handler(commands=['lowprice'])
def lowprice_handler(message: dict) -> None:
	"""
    Функция обработки команды lowprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, lowprice())


@bot.message_handler(commands=['highprice'])
def highprice_handler(message: dict) -> None:
	"""
    Функция обработки команды highprice
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, highprice())


@bot.message_handler(commands=['bestdeal'])
def bestdeal_handler(message: dict) -> None:
	"""
    Функция обработки команды bestdeal
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, bestdeal())


@bot.message_handler(commands=['history'])
def history_handler(message: dict) -> None:
	"""
    Функция обработки команды history
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	bot.send_message(message.chat.id, history())


@bot.message_handler(content_types=['text'])
def get_text_messages(message: dict) -> None:
	"""
    Функция обработки текстового сообщения
    :param message: объект полученного сообщения от пользователя
    :return: None

    """
	if message.text.lower() == 'hello':
		bot.send_message(message.from_user.id, 'Hello. Can I help You?')
	# elif message.text.lower() == 'photo':
	# 	data = requests.get('https://images.trvl-media.com/hotels/'
	# 	                    '67000000/66900000/66891600/66891527/'
	# 	                    'a03acf9a.jpg?'
	# 	                    'impolicy=resizecrop&rw=670&ra=fit').content
	# 	with open('image.jpeg', 'wb') as f:
	# 		f.write(data)
	# 	bot.send_photo(message.chat.id,
	# 	               'image.jpeg')
	else:
		bot.send_message(message.from_user.id,
		                 'I do not understand You. Please write'
		                 ' /help for instructions.'
		                 )


bot.polling(non_stop=True, interval=0)
