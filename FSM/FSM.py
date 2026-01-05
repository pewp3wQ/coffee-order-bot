from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class OrderSG(StatesGroup):
    set_category = State()
    set_location = State()
    set_volume = State()
    set_coffee = State()
    set_coffee_base = State()
    set_sugar = State()
    set_toppings = State()
    set_additional = State()
    set_temperature = State()
    set_wait_time = State()
    set_finish = State()

class AdminMenuSG(StatesGroup):
    admin_menu_start = State()