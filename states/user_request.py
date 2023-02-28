from telebot.handler_backends import State, StatesGroup


class UserRequest(StatesGroup):
    city = State()
    hotels_quantity = State()
    is_photo_enabled = State()
    photo_quantity = State()


class DBRequest(UserRequest):
    user_id = State()
    user_command = State()
    request_datetime = State()
    hotel_list = State()