import sqlite3
import datetime

from telebot.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto

from loader import bot
from states.user_request import UserRequest
import api
from utils.sort_bestdeal_hotels import sort_bestdeal_hotels
import data_base
import utils.select_date_from_calendar as sd


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def request_command_handler(msg: Message) -> None:
    """
    Обработка команды запроса
    :param msg: Объект полученного сообщения от пользователя с командой
    :return: None

    """
    bot.set_state(msg.from_user.id, UserRequest.city, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['command'] = msg.text[1:]
        print(msg.text[1:])
        data['user_id'] = msg.from_user.id
        data['time_of_request'] = datetime.datetime.now()
        data['number_of_request'] = 0  # параметр для повторного запроса
    bot.send_message(msg.chat.id, 'Where are You going?')


@bot.message_handler(state=UserRequest.city)
def get_region_id(msg: Message) -> None:
    """
    Получить regionId по названию города для последующего запроса списка отелей
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    city_name = msg.text
    list_of_cities = api.get_regionid_of_city(city_name)
    if not list_of_cities:
        bot.send_message(msg.chat.id,
                         "I didn't find city with such name.Please try again.")
    else:
        markup = InlineKeyboardMarkup()
        for city in list_of_cities:
            callback = city[0] + '|' + city[1]
            markup.add(
                InlineKeyboardButton(city[0], callback_data=callback))
        bot.send_message(msg.chat.id, 'Please confirm your choice',
                         reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: not call.data.startswith('request') and not
    call.data.startswith('photo'))
def print_region(call: CallbackQuery) -> None:
    """
    Уточнить город назначения
    :param call: Объект callback от пользователя при нажатии на конкретный
    город
    :return: None
    """
    [city_name, region_id] = call.data.split('|')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['regionId'] = region_id
        data['city_name'] = city_name
    bot.set_state(call.from_user.id, UserRequest.hotels_quantity,
                  call.message.chat.id)
    bot.send_message(call.message.chat.id,
                     'Input requested quantity of hotels?')


@bot.message_handler(state=UserRequest.hotels_quantity)
def get_hotels_quantity(msg: Message) -> None:
    """
    Получить количество запрашиваемых отелей
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['hotels_quantity'] = int(msg.text)
    bot.set_state(msg.from_user.id, UserRequest.is_photo_enabled,
                  msg.chat.id)
    markup = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton('Yes', callback_data='photo_Yes')
    btn_no = InlineKeyboardButton('No', callback_data='photo_No')
    markup.add(btn_yes, btn_no)
    bot.send_message(msg.chat.id, 'Would You like to get photos?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('photo'))
def is_photos_enabled(call: CallbackQuery):
    """
    Получить ответ нужно ли загружать фото.
    :param call: Объект callback от пользователя с ответом ДА или НЕТ
    :return: None
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        is_photo = call.data.split('_')[1]
        data['is_photos_enabled'] = is_photo
    if is_photo == 'Yes':
        bot.set_state(call.from_user.id, UserRequest.photo_quantity,
                      call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Input quantity of photos? '
                                               'Not more then 10.')
    else:
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            data['quantity_of_photos'] = 0
        bot.set_state(call.from_user.id, UserRequest.checkin_date,
                      call.message.chat.id)
        bot.send_message(call.message.chat.id,
                         'Please select check-in date?',
                         reply_markup=sd.calendar_markup)


@bot.message_handler(state=UserRequest.photo_quantity)
def get_quantity_of_photos(msg: Message) -> None:
    """
    Получить количество запрашиваемых фотографий
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['quantity_of_photos'] = int(msg.text)
    bot.set_state(msg.from_user.id, UserRequest.checkin_date,
                  msg.chat.id)
    bot.send_message(msg.chat.id,
                     'Please select check-in date?',
                     reply_markup=sd.calendar_markup)


@bot.message_handler(state=UserRequest.adults)
def get_adults_quantity(msg: Message) -> None:
    """
    Уточнить количество взрослых
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
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
def get_children_quantity(msg: Message) -> None:
    """
    Уточнить количество детей. Если без детей для запросов lowprice и
    bestdeal подтвердить введенные данные
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    try:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['children_num'] = int(msg.text)
            data['children_ages'] = []
        bot.set_state(msg.from_user.id, UserRequest.children_ages,
                      msg.chat.id)
        if int(msg.text) == 0 and data['command'] != 'bestdeal':
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                'Request',
                callback_data='request'))
            with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
                bot.send_message(
                    msg.chat.id,
                    f"City: {data['city_name']}\n "
                    f"Quantity of hotels requested: "
                    f"{data['hotels_quantity']}\n"
                    f"Download photos: {data['is_photos_enabled']}\n"
                    f"Quantity of photos: {data['quantity_of_photos']}\n"
                    f"Check in date: {data['checkin_date']}\n"
                    f"Check out date: {data['checkout_date']}\n"
                    f"Number of adults: {data['adults']}\n"
                    f"Number of children: {msg.text}\n", reply_markup=markup)
        elif int(msg.text) == 0 and data['command'] == 'bestdeal':
            bot.set_state(msg.from_user.id, UserRequest.distance_range,
                          msg.chat.id)
            bot.send_message(msg.chat.id,
                             'Please input distance from downtown in km:')
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
def get_children_ages(msg: Message) -> None:
    """
    Получить возраст детей и для запросов lowprice и
    bestdeal подтвердить введенные данные
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
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
            if data['children_num'] == len(data['children_ages']) and \
                    data['command'] != 'bestdeal':
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(
                    'Request',
                    callback_data='request'))
                bot.send_message(
                    msg.chat.id,
                    f"City: {data['city_name']}\n "
                    f"Quantity of hotels requested: "
                    f"{data['hotels_quantity']}\n"
                    f"Download photos: {data['is_photos_enabled']}\n"
                    f"Quantity of photos: {data['quantity_of_photos']}\n"
                    f"Check in date: {data['checkin_date']}\n"
                    f"Check out date: {data['checkout_date']}\n"
                    f"Number of adults: {data['adults']}\n"
                    f"Number of children: {data['children_num']}\n"
                    f"Ages of children: {data['children_ages']}",
                    reply_markup=markup
                )
            elif data['children_num'] == len(data['children_ages']) and \
                    data['command'] == 'bestdeal':
                bot.set_state(msg.from_user.id, UserRequest.distance_range,
                              msg.chat.id)
                bot.send_message(msg.chat.id,
                                 'Please input distance from downtown in km:')
            else:
                count_of_child = len(data['children_ages'])
                bot.send_message(
                    msg.chat.id,
                    f"Input ages of {number_of_child[count_of_child]} child:")

    except ValueError:
        bot.send_message(msg.chat.id, 'Input number please.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('request'))
def request_list_of_hotels(call: CallbackQuery) -> None:
    """
    Получить список отелей по запросу
    :param call: Объект callback при нажатии Request от пользователя
    :return: None
    """
    if call.data.endswith('yes') or call.data.endswith('request'):
        m = bot.send_message(call.from_user.id, 'Working on your request ...')
        with bot.retrieve_data(call.from_user.id,
                               call.message.chat.id) as data:
            if data['number_of_request'] > 0:
                data['time_of_request'] = datetime.datetime.now()
            if data['command'] == 'bestdeal':
                requested_hotels = \
                    sort_bestdeal_hotels(api.get_list_of_hotels(
                        data,
                        start_index=data['number_of_request']
                                    * data['hotels_quantity']),
                        data['maximum_cost'],
                        data['distance_range'])
            elif data['command'] == 'highprice':
                start_index = 0
                hotels_list = []
                while not hotels_list:
                    hotels_list = \
                        api.get_list_of_hotels(data,
                                               start_index=start_index)
                    start_index += 50
                # hotels_list = api.get_list_of_hotels(data, start_index)
                requested_hotels = []
                for index in range(len(hotels_list)
                                   - (data['number_of_request'] - 1)
                                   * data['hotels_quantity']
                                   - 1,
                                   len(hotels_list)
                                   - data['hotels_quantity']
                                   * data['number_of_request']
                                   - 1,
                                   -1):
                    requested_hotels.append(hotels_list[index])
            else:
                requested_hotels = api.get_list_of_hotels(
                    data,
                    start_index=data['number_of_request']
                                * data['hotels_quantity'])
            for hotel in requested_hotels:
                if data['is_photos_enabled'] == 'No':
                    bot.send_message(call.message.chat.id,
                                     hotel.get_hotel_info())
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
            with sqlite3.connect('history.db') as conn:
                data_base.insert_request_info_to_db(conn, data)
                request_id = data_base.get_request_id(conn, data)
                data_base.insert_result_of_request_to_db(
                    conn,
                    hotels=requested_hotels,
                    request_id=request_id)
            data['number_of_request'] += 1
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Yes', callback_data='request_yes'),
                   InlineKeyboardButton('No', callback_data='request_no'))
        bot.send_message(chat_id=call.message.chat.id,
                         text='Request more hotels with same parameters?',
                         reply_markup=markup)
    else:
        bot.delete_state(call.from_user.id, call.message.chat.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="For new request use one of the following command "
                 "\n/lowprice\n/highprice\n/bestdeal\n/history"
        )


@bot.message_handler(state=UserRequest.distance_range)
def get_distance_from_downtown(msg: Message) -> None:
    """
    Получить радиус поиска от центра города
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    try:
        with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['distance_range'] = int(msg.text)
            bot.set_state(msg.from_user.id, UserRequest.cost_range,
                          msg.chat.id)
            bot.send_message(msg.chat.id,
                             'Input minimal cost in $:')
    except ValueError:
        bot.send_message(msg.chat.id, 'Input number please')


@bot.message_handler(state=UserRequest.cost_range)
def get_cost_range(msg: Message) -> None:
    """
    Получить диапазон цен запрашиваемых отелей и подтвердить
    введенные данные
    :param msg: Объект полученного сообщения от пользователя
    :return: None
    """
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        if 'minimal_cost' not in data.keys():
            data['minimal_cost'] = int(msg.text)
            bot.send_message(msg.chat.id,
                             'Input maximum cost in $:')
        else:
            data['maximum_cost'] = int(msg.text)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                'Request',
                callback_data='request'))
            bot.send_message(
                msg.chat.id,
                f"City: {data['city_name']}\n "
                f"Quantity of hotels requested: {data['hotels_quantity']}\n"
                f"Download photos: {data['is_photos_enabled']}\n"
                f"Quantity of photos: {data['quantity_of_photos']}\n"
                f"Check in date: {data['checkin_date']}\n"
                f"Check out date: {data['checkout_date']}\n"
                f"Number of adults: {data['adults']}\n"
                f"Number of children: {data['children_num']}\n"
                f"Ages of children: {data['children_ages']}\n"
                f"Maximum distance from downtown: {data['distance_range']}km\n"
                f"Minimal cost: {data['minimal_cost']}$\n"
                f"Maximum cost: {data['maximum_cost']}$\n",
                reply_markup=markup
            )
