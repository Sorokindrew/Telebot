from telebot.custom_filters import StateFilter

from loader import bot
import handlers


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
