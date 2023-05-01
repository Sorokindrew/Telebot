from telebot.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, InputMediaPhoto

from loader import bot
from states.user_request import UserRequest
import api
from utils.check_inputed_date import check_if_valid_date, \
    checkin_before_checkout, checkin_is_actual


@bot.message_handler(state=UserRequest.city)
def get_region_id(msg: Message):
    city_name = msg.text
    list_of_cities = api.get_regionid_of_city(city_name)
    if not list_of_cities:
        bot.send_message(msg.chat.id,
                         "I didn't find city with such name.Please try again.")
    else:
        markup = InlineKeyboardMarkup()
        for city in list_of_cities:
            callback = city[0] + '|' + city[1] + '|' + str(msg.from_user.id)
            markup.add(
                InlineKeyboardButton(city[0], callback_data=callback))
        bot.send_message(msg.chat.id, 'Please confirm your choice',
                         reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: not call.data.startswith('request'))
def print_region(call: CallbackQuery):
    [city_name, region_id, user_id] = call.data.split('|')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['regionId'] = region_id
        data['city_name'] = city_name
    bot.set_state(int(user_id), UserRequest.hotels_quantity,
                  call.message.chat.id)
    bot.send_message(int(user_id), 'Input requested quantity of hotels?')


@bot.message_handler(state=UserRequest.hotels_quantity)
def get_hotels_quantity(msg: Message):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['hotels_quantity'] = int(msg.text)
    bot.set_state(msg.from_user.id, UserRequest.is_photo_enabled,
                  msg.chat.id)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_yes = KeyboardButton('Yes')
    btn_no = KeyboardButton('No')
    markup.add(btn_yes, btn_no)
    bot.send_message(msg.chat.id, 'Would You like to get photos?',
                     reply_markup=markup)


@bot.message_handler(state=UserRequest.is_photo_enabled)
def is_photos_enabled(msg: Message):
    markup = ReplyKeyboardRemove()
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['is_photos_enabled'] = msg.text
    if msg.text == 'Yes':
        bot.set_state(msg.from_user.id, UserRequest.photo_quantity,
                      msg.chat.id)
        bot.send_message(msg.chat.id, 'Input quantity of photos? '
                                      'Not more then 10.', reply_markup=markup)
    else:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['quantity_of_photos'] = 0
        bot.set_state(msg.from_user.id, UserRequest.checkin_date,
                      msg.chat.id)
        bot.send_message(msg.chat.id,
                         'Input check-in date in format dd-mm-yyyy?',
                         reply_markup=markup)


@bot.message_handler(state=UserRequest.photo_quantity)
def get_quantity_of_photos(msg: Message):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['quantity_of_photos'] = int(msg.text)
    bot.set_state(msg.from_user.id, UserRequest.checkin_date,
                  msg.chat.id)
    bot.send_message(msg.chat.id, 'Input check-in date in format dd-mm-yyyy?')


@bot.message_handler(state=UserRequest.checkin_date)
def get_checkin_date(msg: Message):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        if check_if_valid_date(msg.text) \
                and checkin_is_actual(msg.text):
            data['checkin_date'] = msg.text
            bot.set_state(msg.from_user.id, UserRequest.checkout_date,
                          msg.chat.id)
            bot.send_message(msg.chat.id,
                             'Input check-out date in format dd-mm-yyyy?')
        elif not checkin_is_actual(msg.text):
            bot.send_message(msg.chat.id,
                             'Check-in date should be not later then today. '
                             'Input check-in date in format dd-mm-yyyy?')
        else:
            bot.send_message(msg.chat.id,
                             'Format date is not valid. Try again. '
                             'Input check-in date in format dd-mm-yyyy?')


@bot.message_handler(state=UserRequest.checkout_date)
def get_checkout_date(msg: Message):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        if check_if_valid_date(msg.text) \
                and checkin_before_checkout(data['checkin_date'], msg.text):
            data['checkout_date'] = msg.text
            bot.set_state(msg.from_user.id, UserRequest.adults,
                          msg.chat.id)
            bot.send_message(msg.chat.id,
                             'Please input number of adults?')
        elif not checkin_before_checkout(data['checkin_date'], msg.text):
            bot.send_message(
                msg.chat.id,
                f"Date should be later then {data['checkin_date']}. "
                f"Input check-out date in format dd-mm-yyyy?")
        else:
            bot.send_message(msg.chat.id,
                             'Format date is not valid. Try again. '
                             'Input check-out date in format dd-mm-yyyy?')


@bot.message_handler(state=UserRequest.adults)
def get_adults_quantity(msg: Message):
    try:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['adults'] = int(msg.text)
        bot.set_state(msg.from_user.id, UserRequest.children_num,
                      msg.chat.id)
        bot.send_message(msg.chat.id, "Input number of children?")
    except ValueError:
        bot.send_message(msg.chat.id, 'Quantity should be a number. '
                                      ' Try again. Input number of adults?')


@bot.message_handler(state=UserRequest.children_num)
def get_children_quantity(msg: Message):
    try:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['children_num'] = int(msg.text)
            data['children_ages'] = []
        bot.set_state(msg.from_user.id, UserRequest.children_ages,
                      msg.chat.id)
        if int(msg.text) == 0:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                'Request',
                callback_data='request' + '|' + str(msg.from_user.id)))
            with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                bot.send_message(
                    msg.chat.id,
                    f"City: {data['city_name']}\n "
                    f"Quantity of hotels requested: {data['hotels_quantity']}\n "
                    f"Download photos: {data['is_photos_enabled']}\n "
                    f"Quantity of photos: {data['quantity_of_photos']}\n "
                    f"Check in date: {data['checkin_date']}\n "
                    f"Check out date: {data['checkout_date']}\n "
                    f"Number of adults: {data['adults']}\n "
                    f"Number of children: {msg.text}\n ", reply_markup=markup)
        elif int(msg.text) == 1:
            bot.send_message(msg.chat.id, "Input ages of your child?")
            bot.set_state(msg.from_user.id, UserRequest.children_ages,
                          msg.chat.id)
        else:
            bot.send_message(msg.chat.id, "Input ages of first child?")
            bot.set_state(msg.from_user.id, UserRequest.children_ages,
                          msg.chat.id)
    except ValueError:
        bot.send_message(msg.chat.id, 'Input number please.')


@bot.message_handler(state=UserRequest.children_ages)
def get_children_ages(msg: Message):
    try:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            number_of_child = {
                0: 'first',
                1: 'second',
                2: 'third',
                3: 'fourth',
                4: 'fifth'
            }
            data['children_ages'].append(int(msg.text))
            if data['children_num'] == len(data['children_ages']):
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(
                    'Request',
                    callback_data='request' + '|' + str(msg.from_user.id)))
                bot.send_message(
                    msg.chat.id,
                    f"City: {data['city_name']}\n "
                    f"Quantity of hotels requested: {data['hotels_quantity']}\n "
                    f"Download photos: {data['is_photos_enabled']}\n "
                    f"Quantity of photos: {data['quantity_of_photos']}\n "
                    f"Check in date: {data['checkin_date']}\n "
                    f"Check out date: {data['checkout_date']}\n "
                    f"Number of adults: {data['adults']}\n "
                    f"Number of children: {data['children_num']}\n "
                    f"Ages of children: {data['children_ages']}",
                    reply_markup=markup
                )
            else:
                count_of_child = len(data['children_ages'])
                bot.send_message(
                    msg.chat.id,
                    f"Input ages of {number_of_child[count_of_child]} child?")
    except ValueError:
        bot.send_message(msg.chat.id, 'Input number please.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('request'))
def request_list_of_hotels(call: CallbackQuery):
    [call_data, user_id] = call.data.split('|')
    with bot.retrieve_data(int(user_id), call.message.chat.id) as data:
        for hotel in api.get_list_of_hotels(data):
            if data['is_photos_enabled'] == 'No':
                bot.send_message(call.message.chat.id, hotel.get_hotel_info())
            else:
                media = []
                for index in range(data['quantity_of_photos']):
                    if index == 0:
                        media.append(
                            InputMediaPhoto(
                                hotel.get_hotel_photos()[index],
                                caption=hotel.get_hotel_info()))
                    else:
                        media.append(
                            InputMediaPhoto(
                                hotel.get_hotel_photos()[index]))
                bot.send_media_group(call.message.chat.id, media)