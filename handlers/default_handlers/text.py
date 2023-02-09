from telebot.types import Message

from loader import bot


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message) -> None:
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