import datetime

from telebot.custom_filters import StateFilter

from loader import bot
import handlers
from handlers.custom_handlers.request_handler import request


if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), 'Bot is online')
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()

