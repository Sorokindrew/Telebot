import telebot
from lowprice import lowprice
from bestdeal import bestdeal
from highprice import highprice
from history import history

bot = telebot.TeleBot('5551354218:AAHKwAoizg50q8_euQeXeg7RsWWnZx1kDiM')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Чем могу помочь?')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id,
                     'Для работы с ботом, используйте следующие команды:'
                     '\n/lowprice\n/highprice\n/bestdeal\n/history')


@bot.message_handler(commands=['lowprice'])
def lowprice_handler(message):
    bot.send_message(message.chat.id, lowprice())


@bot.message_handler(commands=['highprice'])
def highprice_handler(message):
    bot.send_message(message.chat.id, highprice())


@bot.message_handler(commands=['bestdeal'])
def bestdeal_handler(message):
    bot.send_message(message.chat.id, bestdeal())


@bot.message_handler(commands=['history'])
def history_handler(message):
    bot.send_message(message.chat.id, history())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.from_user.id, 'Hello. Can I help You?')
    else:
        bot.send_message(message.from_user.id,
                         'I do not understand You. Please write'
                         ' /help for instructions')


bot.polling(non_stop=True, interval=0)