import telebot

my_bot = telebot.TeleBot('5551354218:AAHKwAoizg50q8_euQeXeg7RsWWnZx1kDiM')


@my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'hello':
        my_bot.send_message(message.from_user.id, 'Hello. Can I help You?')
    elif message.text == '/help':
        my_bot.send_message(message.from_user.id, 'For request You may use following commands: \n/lowprice\n/highprice\n/bestdeal\n/history')
    else:
        my_bot.send_message(message.from_user.id, 'I do not understand You. Please write /help for instructions')

my_bot.polling(non_stop=True, interval=0)