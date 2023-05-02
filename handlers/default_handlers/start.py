from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(msg: Message) -> None:
    """
    Функция обработки команды start
    :param msg: объект полученного сообщения от пользователя
    :return: None

    """
    bot.send_message(msg.chat.id,
                     f'Привет, {msg.from_user.first_name}! '
                     f'Чем могу помочь?\n'
                     'Чтобы начать поиск используйте одну из следующих команд:'
                     '\n/lowprice - вывод самых дешевых отелей в городе'
                     '\n/highprice - вывод самых дорогих отелей в городе'
                     '\n/bestdeal - вывод отелей наиболее подходящих по цене и'
                     'расположению'
                     '\n/history - вывод истории поиска отелей')
