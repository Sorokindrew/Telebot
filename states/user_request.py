from telebot.handler_backends import State, StatesGroup


class UserRequest(StatesGroup):
    city = State()
    hotels_quantity = State()
    is_photo_enabled = State()
    photo_quantity = State()
    checkin_date = State()
    checkout_date = State()
    adults = State()
    children_num = State()
    children_ages = State()
    distance_range = State()
    cost_range = State()



