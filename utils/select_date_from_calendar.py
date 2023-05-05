import datetime

from telebot_calendar import Calendar, CallbackData
from telebot.types import CallbackQuery, InlineKeyboardMarkup
from states.user_request import UserRequest

from loader import bot
from utils.check_inputed_date import checkin_is_actual, checkin_before_checkout

# Creates a unique calendar
calendar = Calendar()
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month",
                                   "day")

now = datetime.datetime.now()

calendar_markup: InlineKeyboardMarkup = calendar.create_calendar(
    name=calendar_1_callback.prefix,
    year=now.year,
    month=now.month)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    # At this point, we are sure that this calendar is ours.
    # So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date
    # or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month,
        day=day
    )

    # There are additional steps. Let's say if the date DAY is selected,
    # you can execute your code. I sent a message.
    if action == "DAY":
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as \
                data:
            state = bot.get_state(call.from_user.id, call.message.chat.id)
            if state == 'UserRequest:checkin_date':
                if not checkin_is_actual(date.strftime('%d-%m-%Y')):
                    bot.send_message(call.message.chat.id,
                                     'Check-in date should be not later then today. '
                                     'Please select correct check-in date',
                                     reply_markup=calendar_markup)
                else:
                    data['checkin_date'] = date.strftime('%d-%m-%Y')
                    bot.set_state(call.from_user.id, UserRequest.checkout_date)
                    bot.send_message(call.message.chat.id,
                                     "Please select checkout date?",
                                     reply_markup=calendar_markup)
            elif state == 'UserRequest:checkout_date':
                if not checkin_before_checkout(data['checkin_date'],
                                               date.strftime('%d-%m-%Y')):
                    bot.send_message(
                        call.message.chat.id,
                        f"Date should be later then {data['checkin_date']}. "
                        f"Please select correct check-out date",
                        reply_markup=calendar_markup)
                else:
                    data['checkout_date'] = date.strftime('%d-%m-%Y')
                    bot.set_state(call.from_user.id, UserRequest.adults,
                                  call.message.chat.id)
                    bot.send_message(call.message.chat.id,
                                     'Please input number of adults?')
            elif action == "CANCEL":
                bot.delete_state(call.from_user.id, call.message.chat.id)
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text="You have cancelled your request."
                    "For new request use one of the following command "
                         "\n/lowprice\n/highprice\n/bestdeal\n/history"
                )
